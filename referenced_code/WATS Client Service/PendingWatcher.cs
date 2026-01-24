using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using Virinco.WATS.Interface;
using System.Threading;

namespace Virinco.WATS.ClientService
{
    internal class PendingWatcher : IDisposable
    {
        //private DirectoryInfo PendingFolder;
        private FileSystemWatcher fsw;
        private System.Timers.Timer tmr;
        private TDM_ClientService api;

        internal enum PendingWatcherState { Created, Initializing, Running, Stopping, Disposed, Paused }
        internal PendingWatcherState State = PendingWatcherState.Created;
        private const string Filter_queued = "*.queued";

        private TimeSpan TransferingTimeout
        {
            get { return new TimeSpan(0, 30, 0); /*TODO (maybe): Use configurable value ??? */ }
        }
        internal PendingWatcher(bool Initialize, bool async)
        {
            if (Initialize) Start(async);
        }
        internal PendingWatcher(bool Initialize)
        {
            if (Initialize) Start(false);
        }
        internal PendingWatcher()
        {
            Start(false);
        }
        internal void Start(bool async)
        {
            if (async) ThreadPool.QueueUserWorkItem(new WaitCallback(Start));
            else Start(null);
        }
        
        private void Start(object sender)
        {
            State = PendingWatcherState.Initializing;
            api = new TDM_ClientService();
            try { api.InitializeAPI(true); }
            catch { }
            
            fsw = new FileSystemWatcher(api.ReportsDirectory, Filter_queued);
            fsw.Changed += new FileSystemEventHandler(fsw_Changed);
            fsw.Renamed += new RenamedEventHandler(fsw_Renamed);
            fsw.EnableRaisingEvents=true;
            tmr = new System.Timers.Timer(300000); // Ensure "checking" evry 5 min.
            tmr.Elapsed += new System.Timers.ElapsedEventHandler(tmr_Elapsed);
            tmr.Start();
            State = PendingWatcherState.Running;
            StartPendingTransfer();
        }

        void tmr_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            try
            {
                tmr.Enabled = false;
                StartPendingTransfer();
            }
            finally
            {
                tmr.Enabled = true;
            }
        }

        void fsw_Renamed(object sender, RenamedEventArgs e)
        {
            StartPendingTransfer();
        }
        void fsw_Changed(object sender, FileSystemEventArgs e)
        {
            StartPendingTransfer();
        }

        private void StartPendingTransfer()
        {
            if (State != PendingWatcherState.Running) return;
            if (Monitor.TryEnter(api)) // ensure only one thread is running SubmitPendingReports simultaneously...
            {
                try
                {
                    try
                    {
                        fsw.EnableRaisingEvents = false;
                        Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "PendingWatcher is starting SubmitPendingReports");
                        if (api.Status == APIStatusType.Unknown) 
                                api.InitializeAPI(true);

                        api.CheckTransferingTimeout();
                    }
                    catch (Exception e)
                    {
                        Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = e, Message = "An error occurred during CheckTransferingTimeout" });
                    }

                    if (api.Status == APIStatusType.Online)
                        api.SubmitPendingReports();
                }
                catch (Exception e)
                {
                    Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = e, Message = "An error occurred during Transfer" });
                }
                finally
                {
                    Monitor.Exit(api);
                    fsw.EnableRaisingEvents = true;
                }
            }
            else
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Submitpending already running in another thread.");
        }

        public void Dispose()
        {
            State = PendingWatcherState.Stopping;
            tmr.Stop();
            if (Monitor.TryEnter(api, 10000))
            {
                Monitor.Exit(api); 
                api.Dispose();
                api = null;
            }
            State = PendingWatcherState.Disposed;
        }

        public bool Enabled
        {
            get { return fsw.EnableRaisingEvents; }
            set { fsw.EnableRaisingEvents = value; tmr.Enabled = value; State = value ? PendingWatcherState.Running : PendingWatcherState.Paused; }

        }

        internal void CheckState()
        {
            if (State==PendingWatcherState.Running && api.Status!=APIStatusType.Online)
            {
                if (api.Ping())
                    StartPendingTransfer();
            }            
        }
    }
}
