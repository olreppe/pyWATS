using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.ClientService
{
    internal enum WorkerState { Initializing, Idle, Running, Disposing }
    internal class ConverterWorkerClass
    {
        
        private Conversion conversion;

        
        internal WorkerState state;
        /// <summary>
        /// Setting Active to false will schedule this worker for disposal.
        /// </summary>
        internal bool ShutDownInProgress;
        internal ConversionItem CurrentItem; // {private set; internal get;}  
        private DateTime lastUse;
        internal ConverterWorkerClass(Conversion conversion)
        {
            state = WorkerState.Initializing;
            //api = new Interface.TDM();
            this.conversion = conversion;
            this.ShutDownInProgress = false;
            
            this.lastUse = DateTime.Now;
            System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(DoWork));
        }
        private void DoWork(object state)
        {
            //TODO: Rebuild worker to wait for signaling (with timeout). Conversion container must signal workers when new items arrive.

            try
            {
                int idleCounter = 0;
                state = WorkerState.Idle;
                while (!ShutDownInProgress)
                {
                    bool gotItem = false;
                    try
                    {
                        gotItem = conversion.GetNextFileToConvert(out CurrentItem);
                    }
                    catch (Exception ex)
                    {
                        Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("An unhandled exception was thrown during GetNextFileToConvert, the ConverterWorker has will be invalidated and removed from Worker collection. Thread ID:{0}", System.Threading.Thread.CurrentThread.ManagedThreadId) });
                        ShutDownInProgress = true;
                    }
                    if (gotItem)
                    {
                        idleCounter = 0;
                        try
                        {
                            using (Virinco.WATS.Interface.TDM api = new Interface.TDM())
                            {
                                api.InitializeAPI(Interface.TDM.InitializationMode.UseExistingStatus, false); // assumes that service api has performed registerclient & getcodes!
                                CurrentItem.state = ConversionItemState.Processing;
                                CurrentItem.converter.ConvertFile(CurrentItem, api);
                            }
                            this.lastUse = DateTime.Now;
                            //conversion.RemoveFile(CurrentItem); //May be async move/zip/delete, converter must call removefile after success (or giving up) move/zip/delete
                        }
                        catch (Exception ex)
                        {
                            // Report exception and terminate worker by setting ShutDownInProgress to true;
                            Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("An unhandled exception was thrown during ConvertFile, the ConverterWorker has will be invalidated and removed from Worker collection. Thread ID:{0}", System.Threading.Thread.CurrentThread.ManagedThreadId) });
                            ShutDownInProgress = true;
                        }
                    }
                    else
                    {
                        idleCounter++;
                        System.Threading.Thread.Sleep(500); //Nothing to do, sleep 0,5s
                        double idleTime = DateTime.Now.Subtract(this.lastUse).TotalSeconds;
                        if (idleCounter == 20) // Run once, after apx. 10 seconds idle time
                        {
                            foreach (Converter cnv in conversion.cnvList)
                                cnv.ProcessArchiveQueue(null);
                        }
                        else if (idleTime > 120) ShutDownInProgress = true;
                    }
                }
                state = WorkerState.Disposing;
                conversion.WorkerShutDown(this); // Signal to conversion that this worker is going down (remove from workers collection)!

            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("An unhandled exception was thrown in a ConverterWorker, the worker is beinginvalidated and removed from Worker collection. Thread ID:{0}", System.Threading.Thread.CurrentThread.ManagedThreadId) });
            }
        }
    }
}