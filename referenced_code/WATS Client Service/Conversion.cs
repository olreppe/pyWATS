using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Xml.Linq;

namespace Virinco.WATS.ClientService
{
    class Conversion : IDisposable
    {
        internal List<Converter> cnvList;
        private Dictionary<string, ConversionItem> pending;
        //private Lookup<DateTime, ConversionItem> pending_lookup;
        private Queue<ConversionItem> pending_queue;

        private List<ConverterWorkerClass> workers;

        private bool _disposing = false;

        private int _maxWorkers;
        private const int DefaultMaxConversionWorkers = 1;

        internal Conversion()
        {
            using (var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS"))
            {
                _maxWorkers = (key == null)
                    ? DefaultMaxConversionWorkers
                    : (key.GetValue("MaxConversionWorkers") as string).ToInt32(DefaultMaxConversionWorkers);
            }
            pending = new Dictionary<string, ConversionItem>();
            pending_queue = new Queue<ConversionItem>();
            workers = new List<ConverterWorkerClass>();
        }

        private void CheckConversionStatus()
        {
            // Check 
        }

        internal void InitializeConverters(object state)
        {
            converters cfg = null;
            try
            {
                if (cnvList != null) foreach (var cnv in cnvList) cnv.Dispose();
                cnvList = new List<Converter>();
                // Load Configuration file
                //System.IO.FileInfo asmFile = new System.IO.FileInfo(System.Reflection.Assembly.GetExecutingAssembly().Location);
                string cfgFilePath = Env.GetConfigFilePath(Env.ConvertersFileName);
                System.IO.FileInfo cfgFile = new System.IO.FileInfo(cfgFilePath); // System.IO.Path.Combine(asmFile.DirectoryName, "converters.xml"));
                using (var fs = cfgFile.OpenRead())
                {
                    cfg = (converters)(new System.Xml.Serialization.XmlSerializer(typeof(converters))).Deserialize(fs);
                }
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Critical, 0, new WATSLogItem() { ex = ex, Message = "Error reading converters.xml" });
                throw;
            }
            // Create & Initialize configured converters...
            if (cfg != null)
            {
                foreach (convertersConverter conv in cfg.converter)
                {
                    try
                    {
                        Converter cnv = new Converter(conv, this);
                        cnvList.Add(cnv);
                        Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Initialized converter: {0}", cnv.Name);
                    }
                    catch (Exception ex)
                    {
                        Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = String.Format("Error starting converter: {0}", conv.name) });
                    }
                }
            }
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "{0} converters initialized", cnvList.Count);
            // if no converters where started, end with failure. ???
            StartAllConverters(null);
        }

        //internal void StopAllConverters()
        //{
        //    lock (cnvList)
        //    {
        //        foreach (Converter cnv in cnvList) cnv.Dispose();
        //        cnvList.Clear();
        //    }
        //}

        internal void StartAllConverters(object state)
        {
            // Wait 5 seconds before starting converters (syncronous)
            System.Threading.Thread.Sleep(5000);
            foreach (Converter cnv in cnvList)
            {
                try
                {
                    cnv.Start();
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Converter Started Name: {0}, pending count: {1}", cnv.Name, cnv.pendingitems.Count);
                }
                catch (Exception ex)
                {
                    Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = String.Format("Error starting converter: {0}", cnv.Name) });
                }
            }
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "{0} converters started", cnvList.Count(c => c.ConverterState == ConverterStateEnum.Running));
        }

        internal void PauseAllConverters()
        {
            foreach (Converter cnv in cnvList) cnv.Stop();
        }

        internal List<ConverterStatistics> GetConverterStatistics()
        {
            List<ConverterStatistics> res = null;
            if (cnvList != null && !_disposing)
            {
                res = new List<ConverterStatistics>();
                foreach (Converter cnv in cnvList)
                {
                    var stats = new ConverterStatistics(cnv.Name, cnv.ConverterState, cnv.version, cnv.PendingCount(), cnv.ErrorCount());
                    res.Add(stats);
                }
            }

            return res;
        }

        internal void CheckState()
        {
            foreach (Converter cnv in cnvList)
            {
                // Check converter "state"...
                System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(cnv.CheckState));
            }
            // Restart timed-out items (600sec)
            DateTime timeout = DateTime.Now.AddSeconds(-600);
            lock (pending)
                foreach (var p in pending.Where(p => p.Value.state != ConversionItemState.Pending && p.Value.processstart < timeout))
                    p.Value.state = ConversionItemState.Pending;
            CheckWorkerStatus();
        }

        public void Dispose()
        {
            _disposing = true;
            // Mark all workers as shutting down;
            if (workers != null)
                foreach (ConverterWorkerClass worker in workers) worker.ShutDownInProgress = true;
            if (cnvList != null)
            {
                foreach (Converter cnv in cnvList) cnv.Stop();
                cnvList.Clear();
            }
            // Wait up to 20 seconds for all workers to stop processing...
            int timeout = 200;
            while (workers != null && workers.Count > 0) { timeout--; System.Threading.Thread.Sleep(100); }
        }

        internal bool GetNextFileToConvert(out ConversionItem item)
        {
            lock (pending) // Ensure exclusive access to collection
            {
                if (pending.Count > 0 && pending_queue.Count == 0) // refill queue from pending...
                {
                    pending_queue = new Queue<ConversionItem>(pending.Values.Where(p => p.state == ConversionItemState.Pending).OrderBy(p => p.filedate));
                }
                if (pending_queue.Count > 0)
                {
                    item = pending_queue.Dequeue();
                    item.processstart = DateTime.Now;
                    item.state = ConversionItemState.Processing;
                    return true;
                }
                else
                {
                    item = null;
                    return false;
                }
            }
        }

        internal ConversionItem AddFile(FileInfo fi, Converter converter)
        {
            ConversionItem ci;
            lock (pending) // Ensure exclusive access to collection
            {
                if (pending.TryGetValue(fi.FullName, out ci))
                {
                    // Already queued... check for timeout ??
                }
                else // New file, create ConvertInfo class, and queue workitem...
                {
                    ci = new ConversionItem();
                    ci.file = fi;
                    ci.sourcePath = fi.FullName;
                    ci.queued = DateTime.Now;
                    ci.converter = converter;
                    ci.filedate = fi.LastWriteTime;
                    ci.state = ConversionItemState.Pending;
                    pending.Add(ci.sourcePath, ci);
                }
            }
            int wcount = workers.Count;
            if (wcount < 1 || (wcount < 10 && pending.Count > 10)) CheckWorkerStatus();
            return ci;
        }

        /// <summary>
        /// Spawn multiple workerprocesses if pending conversion count exceeds 10 files, use registry value to specify a maximum worker processes, and never exceed 50 processes.
        /// </summary>
        private void CheckWorkerStatus()
        {
            lock (workers)
            {
                int desiredWorkers = ((pending.Count + 9) / 10); // 1..10 > 1wp, 11..20 > 2wp ...
                if (_maxWorkers > 0 && desiredWorkers > _maxWorkers) desiredWorkers = _maxWorkers; // Never exceed configured maxWorkers set in registry (defaults to 1)
                if (desiredWorkers > 50) desiredWorkers = 50; // Never exceed 50 workers, even if registry defines more than 50 (considered a malconfiguration)
                int addworkers = desiredWorkers - workers.Count; // calculate "missing" workers
                if (addworkers > 0) Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Information, 0, "Starting {0} Converter Worker processes. Pending Count: {1}", addworkers, pending_queue.Count);
                for (int i = 0; i < addworkers; i++)
                    workers.Add(new ConverterWorkerClass(this));
            }
        }

        internal void WorkerShutDown(ConverterWorkerClass worker)
        {
            lock (workers)
            {
                if (workers.Contains(worker)) workers.Remove(worker);
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Converter Worker processes on thread #{0} is shutting down. Pending Count: {1}", System.Threading.Thread.CurrentThread.ManagedThreadId, pending_queue.Count);
                if (workers.Count == 0)
                {
                    foreach (Converter cnv in cnvList)
                        System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(cnv.ProcessArchiveQueue));
                }
            }
        }

        internal void RemoveFile(string FileFullName)
        {
            lock (pending) pending.Remove(FileFullName);
        }

        internal bool IsPending(ConversionItem ci)
        {
            lock (pending) return pending.ContainsValue(ci);
        }
    }
    internal enum ConversionItemState { Pending, Processing, PostProcessing, Done };

    internal class ConversionItem
    {
        internal Converter converter;
        internal string sourcePath;
        internal FileInfo file;
        internal DateTime filedate;
        internal DateTime queued;
        internal DateTime processstart;
        internal int lockiteration;
        internal int threadId;
        internal ConversionItemState state;
    }

    internal struct ConverterStatistics
    {
        public string Name { get; }

        public ConverterStateEnum State { get; }

        public Version Version { get; }

        public int PendingCount { get; }

        public int ErrorCount { get; }

        public ConverterStatistics(string name, ConverterStateEnum state, Version version, int pendingCount, int errorCount)
        {
            Name = name;
            State = state;
            Version = version;
            PendingCount = pendingCount;
            ErrorCount = errorCount;
        }
    }
}
