using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.IO;
using System.Xml.Serialization;
using System.Xml;
using System.Threading;

using System.Diagnostics;
using System.ComponentModel;

#pragma warning disable 1591

namespace Virinco.WATS.Interface.Statistics
{
    /*
     * Refreshing Statistics.cs classes: Execute 
     * cmd-shell> xsd .\statistics.xsd /d /eld /n:Virinco.WATS.Interface.Statistics     
     */
    public class StatisticsReader : System.ComponentModel.INotifyPropertyChanged, IDisposable
    { 
        public StatisticsProduct CurrentProduct
        {
            get
            {
                if (_currentproduct == null)
                    _currentproduct = GetProduct(CurrentPartNumber);
                return _currentproduct;
            }
        }

        public StatisticsProductOperation CurrentProductOperation
        {
            get
            {
                if (_currentproductoperation == null)
                    _currentproductoperation = GetProductOperation(CurrentProduct, CurrentOperationKey);
                return _currentproductoperation;
            }
        }

        public int UURReportsSinceStartup
        {
            get
            {
                int result;
                if (!int.TryParse(this[cUUR_SS_Key], out result))
                    result = 0;
                return result;
            }
        }

        public int UUTReportsSinceStartup
        {
            get
            {
                int result;
                if (!int.TryParse(this[cUUT_SS_Key], out result))
                    result = 0; return result;
            }
        }

        //public int PendingReports 
        //{
        //    get 
        //    { 
        //        int result;
        //        if (!Int32.TryParse(this[cPending_Key], out result)) 
        //            result = 0; 
        //        return result; 
        //    } 
        //}

        public int UURReportsTotal
        {
            get
            {
                int result;
                if (!int.TryParse(this[cUUR_tot_Key], out result))
                    result = 0;
                return result;
            }
        }

        public int UUTReportsTotal
        {
            get
            {
                int result;
                if (!int.TryParse(this[cUUT_tot_Key], out result))
                    result = 0;
                return result;
            }
        }

        public DateTime Started
        {
            get
            {
                DateTime dt;
                if (!DateTime.TryParse(this[cStarted_Key], out dt))
                    dt = DateTime.Now;
                return dt;
            }
        }

        public string CurrentPartNumber
        {
            get { return this[cCPN_Key]; }
        }

        public string CurrentOperationKey
        {
            get { return this[cCOT_Key]; }
        }

        public string CurrentOperationName
        {
            get { return this[cCOTName_Key]; }
        }

        public bool RunOnStartUp
        {
            get { return ToBoolean(this[cRunOnStartUp_Key], true); }
        }

        public bool AlwaysOnTop
        {
            get { return ToBoolean(this[cAlwaysOnTop_Key], false); }
        }

        public double Transparency
        {
            get { return ToDouble(this[cTransparency_Key], 0.8); }
        }

        public List<int> Trend
        {
            get { return GetTrend(CurrentPartNumber, CurrentOperationKey); }
        }

        public int UUTReportsInLastStat
        {
            get { return GetLastCount(CurrentProduct, CurrentProductOperation); }
        }

        public int UUTReportsInStat
        {
            get { return GetTotalCount(CurrentProductOperation); }
        }

        public int UURReportsInStat
        {
            get { return 0; }
        }

        public double TestYieldTotal
        {
            get { return GetTestYieldTotal(CurrentProductOperation); }
        }

        public double TestYieldLast
        {
            get { return GetTestYieldLast(CurrentProduct, CurrentProductOperation); }
        }

        public double TestYieldDiff
        {
            get { return GetTestYieldDiff(CurrentProduct, CurrentProductOperation); }
        }

        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;

        public const string StatisticsFilename = "Statistics.xml";

        private Statistics stats
        {
            get { return _stats; }
            set
            {
                _stats = value;
                _vals = null;
                _products = null;
            }
        }

        private Dictionary<string, StatisticsValue> vals
        {
            get
            {
                if (_vals == null)
                    _vals = _stats.overview != null ? _stats.overview.ToDictionary(sv => sv.key) : new Dictionary<string, StatisticsValue>();
                return _vals;
            }
        }

        private Dictionary<string, StatisticsProduct> products
        {
            get
            {
                if (_products == null)
                    _products = _stats.Product != null ? _stats.Product.ToDictionary(p => p.PN) : new Dictionary<string, StatisticsProduct>();
                return _products;
            }
        }

        private FileInfo fiStatistics;
        private FileSystemWatcher fsw;
        private Statistics _stats;
        private Dictionary<string, StatisticsValue> _vals;
        private Dictionary<string, StatisticsProduct> _products;
        private StatisticsProduct _currentproduct;
        private StatisticsProductOperation _currentproductoperation;
        private System.Collections.Generic.Queue<StatisticsItem> pndStats = new Queue<StatisticsItem>();
        //private TDM _api;

        private const string cUUR_SS_Key = "UURReportsSinceStartup";
        private const string cUUT_SS_Key = "UUTReportsSinceStartup";
        //private const string cPending_Key = "ReportsPending";
        private const string cUUR_tot_Key = "UURReportsTotal";
        private const string cUUT_tot_Key = "UUTReportsTotal";
        private const string cStarted_Key = "Started";
        private const string cCPN_Key = "CurrentPartnumber";
        private const string cCOT_Key = "CurrentOperation";
        private const string cCOTName_Key = "CurrentOperationName";

        private const string cRunOnStartUp_Key = "RunOnStartUp";
        private const string cAlwaysOnTop_Key = "AlwaysOnTop";
        private const string cTransparency_Key = "Transparency";

        public StatisticsReader()
        {
            //this._api = new TDM();
            fiStatistics = new FileInfo(Path.Combine(Env.DataDir, StatisticsFilename));
            Initialize();
        }

        public StatisticsReader(TDM api)
        {
            //this._api = new TDM();            
            fiStatistics = new FileInfo(Path.Combine(api.DataDir, StatisticsFilename));
            Initialize();
        }

        public StatisticsReader(string StatisticsFilePath)
        {
            fiStatistics = new FileInfo(StatisticsFilePath);
            //this._api = api;
            Initialize();
        }

        public StatisticsReader(FileInfo StatisticsFile)
        {
            fiStatistics = StatisticsFile;
            //this._api = api;
            Initialize();
        }

        private void Initialize()
        {
            //_api = api;
            Load();
            fsw = new FileSystemWatcher(fiStatistics.DirectoryName, StatisticsFilename);
            fsw.Changed += new FileSystemEventHandler(fsw_Changed);
            fsw.Renamed += new RenamedEventHandler(fsw_Renamed);
            fsw.Created += new FileSystemEventHandler(fsw_Created);
            fsw.EnableRaisingEvents = true;
            //PendingReports = api.GetPendingReportCount();
            //if(_api != null)
            //    this[cPending_Key] = _api.GetPendingReportCount().ToString();
        }

        public List<int> GetTrend(string PartNumber, string operationKey)
        {
            var product = GetProduct(PartNumber);
            var productOperation = GetProductOperation(product, operationKey);
            return GetTrend(product, productOperation);
        }

        public string GetLastResult(string PartNumber, string OperationKey)
        {
            StatisticsProduct p = GetProduct(PartNumber);
            StatisticsProductOperation po = GetProductOperation(p, OperationKey);
            return po != null ? GetLastResults(p, po) : String.Empty;
        }

        internal string GetTotalResults(StatisticsProductOperation productOperation)
        {
            return productOperation.Value;
        }

        internal string GetLastResults(StatisticsProduct product, StatisticsProductOperation productOperation)
        {
            return productOperation.Value.Length > product.LastCount ? productOperation.Value.Substring(0, product.LastCount) : productOperation.Value;
        }

        internal int GetTotalCount(StatisticsProductOperation productOperation)
        {
            return productOperation.Value.Length;
        }

        internal int GetLastCount(StatisticsProduct product, StatisticsProductOperation productOperation)
        {
            int i = productOperation.Value.Length;
            return i > product.LastCount ? product.LastCount : i;
        }

        internal double GetTestYieldTotal(StatisticsProductOperation productOperation)
        {
            string results = productOperation.Value;
            return GetPassPercent(results);
        }

        internal double GetTestYieldLast(StatisticsProduct product, StatisticsProductOperation productOperation)
        {
            string results = GetLastResults(product, productOperation);
            return GetPassPercent(results);
        }

        internal double GetTestYieldDiff(StatisticsProduct product, StatisticsProductOperation productOperation)
        {
            return GetTestYieldTotal(productOperation) - GetTestYieldLast(product, productOperation);
        }

        internal List<int> GetTrend(StatisticsProduct product, StatisticsProductOperation productOperation)
        {
            List<int> trend = new List<int>();

            string results = productOperation.Value;
            if (results.Length > product.LastCount)
                results = results.Substring(0, product.LastCount);

            int i = 0;
            trend.Add(i);
            foreach (char c in results.Reverse())
            {
                switch (c)
                {
                    case 'P': i++; break;
                    case 'F': i--; break;
                }
                trend.Add(i);
            }

            return trend;
        }

        private double GetPassPercent(string results)
        {
            return results.Length == 0 ? 0 : ((double)results.Count(c => c == 'P')) / results.Length;
        }

        private string this[string key]
        {
            get
            {
                if (vals.ContainsKey(key))
                    return vals[key].Value ?? "";
                else
                    return String.Empty;
            }
            set
            {
                if (vals.ContainsKey(key))
                    vals[key].Value = value?.ToString() ?? "";
                else
                {
                    StatisticsValue sv = new StatisticsValue();
                    sv.key = key;
                    sv.Value = value?.ToString() ?? "";
                    vals[key] = sv;
                }
                _stats.overview = vals.Values.ToArray();
            }
        }

        private bool ToBoolean(string value, bool Default)
        {
            bool b;
            if (bool.TryParse(value, out b))
                return b;
            else
                return Default;
        }

        private double ToDouble(string value, double Default)
        {
            double d;
            if (double.TryParse(value, out d))
                return d;
            else
                return Default;
        }

        //public string GetResult()
        //{
        //    return CurrentProductOperation.Value != null ? CurrentProductOperation.Value : String.Empty;
        //}

        //public string GetResult(string PartNumber, string OperationKey)
        //{
        //    StatisticsProductOperation po = GetProductOperation(GetProduct(PartNumber), OperationKey);
        //    return po != null ? po.Value : String.Empty;
        //}

        //private string GetLastResult()
        //{
        //    return CurrentProductOperation.Value.Length > CurrentProduct.LastCount ? CurrentProductOperation.Value.Substring(0, CurrentProduct.LastCount) : CurrentProductOperation.Value;
        //}

        //public void AddTest(string PartNumber, OperationType operation, StatusType status)
        //{
        //    lock (pndStats)
        //        pndStats.Enqueue(new StatTestResult(PartNumber, operation.Name, operation.Id, status));
        //    ThreadPool.QueueUserWorkItem(new WaitCallback(FlushPendingStats));
        //}

        internal void AddTest(string PartNumber, Schemas.WRML.Process_type process, StatusType status)
        {
            lock (pndStats)
                pndStats.Enqueue(new StatTestResult(PartNumber, process.Name, new Guid(process.Guid), status));
            ThreadPool.QueueUserWorkItem(new WaitCallback(FlushPendingStats));
        }

        internal void IncreaseUURCount()
        {
            lock (pndStats)
                pndStats.Enqueue(new StatAddRepair());
            ThreadPool.QueueUserWorkItem(new WaitCallback(FlushPendingStats));
        }

        public void FlushPendingStats(object sender)
        {
            Exception ex = null;
            bool written = false;
            for (int i = 1; ; i++) /* "timeout" disabled... i <= 20 */
            {
                if (pndStats.Count == 0) return; // nothing to do... all stats already flushed.
                //Debug.WriteLine(String.Format("{2:F3};T#{0:D3};L#{1};INFO     entering", System.Threading.Thread.CurrentThread.ManagedThreadId, i, GetPFTime()));
                if (Monitor.TryEnter(fiStatistics, 250 * i))
                // Timeout (500ms) waiting for lock... wait (i*250 ms) :: 1-20*250 --> 0-5s --> total (0,5 + 2,5) * 20 = 60s
                {
                    try
                    {
                        if (pndStats.Count == 0) return; // nothing to do... all stats already flushed.
                        //Debug.WriteLine(String.Format("{2:F3};T#{0:D3};L#{1};LOCK     succesfully entered", System.Threading.Thread.CurrentThread.ManagedThreadId, i, GetPFTime()));
                        //string op = operation.Id.ToString();
                        /* Load (locked) dataset, read>modify>write*/
                        using (FileStream fs = fiStatistics.Open(FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None))
                        {
                            //Debug.WriteLine(String.Format("{2:F3};T#{0:D3};L#{1};INFO     succesfully locked file", System.Threading.Thread.CurrentThread.ManagedThreadId, i, GetPFTime()));
                            XmlSerializer ser = new XmlSerializer(typeof(Statistics));
                            try { stats = ser.Deserialize(fs) as Statistics; }
                            catch
                            {
                                stats = new Statistics();
                                //Debug.WriteLine(String.Format("{2:F3};T#{0:D3};L#{1};CRITICAL  Unable to read statistics file: Created new file", System.Threading.Thread.CurrentThread.ManagedThreadId, i, GetPFTime()));
                            }
                            lock (pndStats)
                            {
                                //while (pndStats.Count > 0)

                                foreach (StatisticsItem item in pndStats)
                                {
                                    if (item is StatTestResult)
                                    {
                                        StatTestResult str = (StatTestResult)item;
                                        //StatTestResult str = pndStats.Dequeue();
                                        StatisticsProduct product = GetProduct(str.PN);
                                        StatisticsProductOperation productoperation = GetProductOperation(product, str.OPGuid.ToString());
                                        productoperation.Value = str.Status.ToString().Substring(0, 1) + productoperation.Value;
                                        if (productoperation.Value.Length > product.TotalCount) productoperation.Value = productoperation.Value.Substring(0, product.TotalCount);
                                        productoperation.Name = str.OPName;
                                        this[cCPN_Key] = str.PN;
                                        this[cCOT_Key] = str.OPGuid.ToString();
                                        this[cCOTName_Key] = str.OPName;
                                        int result;
                                        if (!Int32.TryParse(this[cUUT_SS_Key], out result)) result = 0;
                                        this[cUUT_SS_Key] = (++result).ToString(); //this.UUTReportsTotal++;
                                        if (!Int32.TryParse(this[cUUT_tot_Key], out result)) result = 0;
                                        this[cUUT_tot_Key] = (++result).ToString(); //this.UUTReportsSinceStartup++;
                                        //Debug.WriteLine(String.Format("{2:F3};T#{0:D3};L#{1};ADDSTAT   Added PN:{3},OP:{4},S:{5}", System.Threading.Thread.CurrentThread.ManagedThreadId, i, GetPFTime(), str.PN, str.OPName, str.Status));
                                        //if (_api != null) this[cPending_Key] = _api.GetPendingReportCount().ToString();
                                    }
                                    else if (item is StatAddRepair)
                                    {
                                        int result;
                                        if (!Int32.TryParse(this[cUUR_SS_Key], out result)) result = 0;
                                        this[cUUR_SS_Key] = (++result).ToString(); //this.UUTReportsTotal++;
                                    }
                                }
                                fs.Position = 0; // resets position before rewriting entire file...
                                ser.Serialize(fs, stats);
                                fs.SetLength(fs.Position);
                                fs.Close();
                                pndStats.Clear(); // all stats taken care of and written, clear queue and release lock.
                                written = true;
                            }
                            _currentproduct = null;
                            _currentproductoperation = null;
                            //Debug.WriteLine(String.Format("{2:F3};T#{0:D3};L#{1};SUCCESS   succesfully added statistics ", System.Threading.Thread.CurrentThread.ManagedThreadId, i, GetPFTime()));
                            break; // Exits....
                        }
                    }
                    catch (Exception wex)
                    {
                        ex = wex;
                        Env.Trace.TraceData(System.Diagnostics.TraceEventType.Verbose, 0, new WATSLogItem() { ex = ex, Message = String.Format("T#{0:D3};L#{1};Statistics:AddTest failed, msg:{2}", System.Threading.Thread.CurrentThread.ManagedThreadId, i, wex.Message) });
                        Thread.Sleep(250);
                    }
                    finally
                    {
                        Thread.Sleep(100); // Sleep 100ms before releasing fiStatistics (allow file operation to  complete (!!??))
                        Monitor.Exit(fiStatistics);
                        //Debug.WriteLine(String.Format("{2:F3};T#{0:D3};L#{1};LOCK     released lock", System.Threading.Thread.CurrentThread.ManagedThreadId, i, GetPFTime()));
                    }
                }
            }
            if (written) RaisePropertyChanged(string.Empty);
            else
            {
                // Something went very wrong... write to EventLog...
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Failed to acquire lock on statistics file. Giving up after 20 attempts in 1 minute." });
                System.Diagnostics.EventLog.WriteEntry("WATS", String.Format("Failed to acquire lock on statistics file. Giving up after 20 attempts in 1 minute.\nLast exception message: {0}", ex != null ? ex.Message : "None"), System.Diagnostics.EventLogEntryType.Warning, 1001);
            }
        }

        internal StatisticsProduct GetProduct(string PartNumber)
        {
            StatisticsProduct product;
            if (products.ContainsKey(PartNumber)) product = products[PartNumber];
            else if (PartNumber == "") // Requesting "default" partnumber failed... creating with "factory defaults"...
            {
                product = new StatisticsProduct();
                product.PN = PartNumber;
                product.TotalCount = 2000;
                product.LastCount = 100;
                product.CriticalLevel = 0.90;
                product.WarnLevel = 0.95;
                products.Add(PartNumber, product);
                stats.Product = products.Values.ToArray();
            }
            else
            {
                StatisticsProduct defaultproduct = GetProduct("");
                product = new StatisticsProduct();
                product.PN = PartNumber;
                product.TotalCount = defaultproduct.TotalCount;
                product.LastCount = defaultproduct.LastCount;
                product.CriticalLevel = defaultproduct.CriticalLevel;
                product.WarnLevel = defaultproduct.WarnLevel;
                products.Add(PartNumber, product);
                stats.Product = products.Values.ToArray();
            }
            return product;
        }

        internal StatisticsProductOperation GetProductOperation(StatisticsProduct product, string operationKey)
        {
            Dictionary<string, StatisticsProductOperation> operations = product.Operation != null ? product.Operation.ToDictionary(o => o.Id) : new Dictionary<string, StatisticsProductOperation>();
            StatisticsProductOperation productoperation;
            if (operations.ContainsKey(operationKey)) productoperation = operations[operationKey];
            else
            {
                productoperation = new StatisticsProductOperation();
                productoperation.Id = operationKey;
                productoperation.Name = "";
                productoperation.Value = "";
                operations.Add(operationKey, productoperation);
                product.Operation = operations.Values.ToArray();
            }
            return productoperation;
        }

        public void ResetStartupCounters()
        {
            lock (fiStatistics)
            {
                using (FileStream fs = fiStatistics.Open(FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None))
                {
                    XmlSerializer ser = new XmlSerializer(typeof(Statistics));
                    try { stats = ser.Deserialize(fs) as Statistics; }
                    catch { stats = new Statistics(); }
                    this[cUUR_SS_Key] = "0";
                    this[cUUT_SS_Key] = "0";
                    this[cStarted_Key] = DateTime.Now.ToString("u");
                    stats.overview = vals.Values.ToArray();
                    fs.Position = 0; // resets position before rewriting entire file...
                    ser.Serialize(fs, stats);
                    fs.SetLength(fs.Position);
                    fs.Close();
                }
            }
            RaisePropertyChanged(string.Empty);
        }

        public void SetAlertLevels(string PartNumber, double WarningLevel, double CriticalLevel, int TotalCount, int LastCount)
        {
            lock (fiStatistics)
            {
                using (FileStream fs = fiStatistics.Open(FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None))
                {
                    XmlSerializer ser = new XmlSerializer(typeof(Statistics));
                    try { stats = ser.Deserialize(fs) as Statistics; }
                    catch { stats = new Statistics(); }
                    StatisticsProduct product = GetProduct(PartNumber);
                    product.WarnLevel = WarningLevel;
                    product.CriticalLevel = CriticalLevel;
                    product.TotalCount = TotalCount;
                    product.LastCount = LastCount;
                    fs.Position = 0; // resets position before rewriting entire file...
                    ser.Serialize(fs, stats);
                    fs.SetLength(fs.Position);
                    fs.Close();
                }
            }
            RaisePropertyChanged(string.Empty);
        }

        private void fsw_Created(object sender, FileSystemEventArgs e)
        {
            Load();
        }

        private void fsw_Renamed(object sender, RenamedEventArgs e)
        {
            Load();
        }

        private void fsw_Changed(object sender, FileSystemEventArgs e)
        {
            Load();
        }

        private void Load()
        {
            lock (fiStatistics)
            {
                if (fiStatistics.Exists)
                {
                    XmlSerializer ser = new XmlSerializer(typeof(Statistics));
                    for (int i = 0; i < 20; i++)
                    {
                        try
                        {
                            using (FileStream fs = fiStatistics.Open(FileMode.Open, FileAccess.Read, FileShare.Read))
                                stats = ser.Deserialize(fs) as Statistics;
                            break;
                        }
                        catch
                        {
                            Thread.Sleep(i * 100);
                            if (i >= 19) stats = new Statistics();
                        }
                    }

                }
                else
                {
                    stats = new Statistics();
                }
            }
            _currentproduct = null;
            _currentproductoperation = null;
            RaisePropertyChanged(string.Empty);
        }

        public static Settings LoadSettings(FileInfo File)
        {
            Settings settings = new Settings();
            settings.Levels = new Dictionary<string, Levels>();
            if (File.Exists)
            {
                XmlSerializer ser = new XmlSerializer(typeof(Statistics));
                try
                {
                    Statistics st;
                    using (FileStream fs = File.Open(FileMode.Open, FileAccess.Read, FileShare.Read))
                        st = ser.Deserialize(fs) as Statistics;

                    StatisticsValue sv;
                    sv = st.overview.FirstOrDefault(v => v.key == cAlwaysOnTop_Key);
                    if (sv == null || !bool.TryParse(sv.Value, out settings._alwaysontop))
                        settings.AlwaysOnTop = false;

                    sv = st.overview.FirstOrDefault(v => v.key == cRunOnStartUp_Key);
                    if (sv == null || !bool.TryParse(sv.Value, out settings._runonstartup))
                        settings.RunOnStartUp = false;

                    sv = st.overview.FirstOrDefault(v => v.key == cTransparency_Key);
                    if (sv == null || !double.TryParse(sv.Value, out settings._transparency))
                        settings.Transparency = 0.8;

                    if (st.Product != null)
                    {
                        foreach (StatisticsProduct p in st.Product)
                        {
                            settings.Levels.Add(p.PN, new Levels
                            {
                                PartNumber = p.PN,
                                WarningLevel = p.WarnLevel,
                                CriticalLevel = p.CriticalLevel,
                                TotalCount = p.TotalCount,
                                LastCount = p.LastCount
                            });
                        }
                    }
                }
                catch { } // Whatever: dontcare... (?)
            }
            return settings;
        }

        public static void SaveSettings(FileInfo File, Settings settings)
        {
            if (File.Exists)
            {
                using (FileStream fs = File.Open(FileMode.OpenOrCreate, FileAccess.ReadWrite, FileShare.None))
                {
                    Statistics st;
                    XmlSerializer ser = new XmlSerializer(typeof(Statistics));
                    try
                    {
                        st = ser.Deserialize(fs) as Statistics;
                    }
                    catch
                    {
                        st = new Statistics();
                    }

                    if (st.overview == null)
                        st.overview = new StatisticsValue[0];

                    Dictionary<string, StatisticsValue> olst = st.overview.ToDictionary(o => o.key);
                    if (olst.ContainsKey(cAlwaysOnTop_Key))
                        olst[cAlwaysOnTop_Key].Value = settings.AlwaysOnTop.ToString();
                    else
                    {
                        olst.Add(cAlwaysOnTop_Key, new StatisticsValue
                        {
                            key = cAlwaysOnTop_Key,
                            Value = settings.AlwaysOnTop.ToString()
                        });
                    }

                    if (olst.ContainsKey(cRunOnStartUp_Key))
                        olst[cRunOnStartUp_Key].Value = settings.RunOnStartUp.ToString();
                    else
                    {
                        olst.Add(cRunOnStartUp_Key, new StatisticsValue
                        {
                            key = cRunOnStartUp_Key,
                            Value = settings.RunOnStartUp.ToString()
                        });
                    }

                    if (olst.ContainsKey(cTransparency_Key))
                        olst[cTransparency_Key].Value = settings.Transparency.ToString();
                    else
                    {
                        olst.Add(cTransparency_Key, new StatisticsValue
                        {
                            key = cTransparency_Key,
                            Value = settings.Transparency.ToString(System.Globalization.CultureInfo.InvariantCulture)
                        });
                    }
                    st.overview = olst.Values.ToArray();

                    if (st.Product == null)
                        st.Product = new StatisticsProduct[0];

                    Dictionary<string, StatisticsProduct> plst = st.Product.ToDictionary(o => o.PN);
                    foreach (Levels lvl in settings.Levels.Values)
                    {
                        if (plst.ContainsKey(lvl.PartNumber))
                        {
                            StatisticsProduct sp = plst[lvl.PartNumber];
                            sp.WarnLevel = lvl.WarningLevel;
                            sp.CriticalLevel = lvl.CriticalLevel;
                            sp.LastCount = lvl.LastCount;
                            sp.TotalCount = lvl.TotalCount;
                        }
                        else
                        {
                            plst.Add(lvl.PartNumber, new StatisticsProduct
                            {
                                PN = lvl.PartNumber,
                                WarnLevel = lvl.WarningLevel,
                                CriticalLevel = lvl.CriticalLevel,
                                LastCount = lvl.LastCount,
                                TotalCount = lvl.TotalCount
                            });
                        }
                    }

                    st.Product = plst.Values.ToArray();

                    fs.Position = 0; // resets position before rewriting entire file...
                    ser.Serialize(fs, st);
                    fs.SetLength(fs.Position);
                    fs.Close();
                }
            }
        }

        protected void RaisePropertyChanged(String info)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new System.ComponentModel.PropertyChangedEventArgs(info));
            }
        }

        public void Dispose()
        {
            if (fsw != null)
            {
                fsw.EnableRaisingEvents = false;
                fsw.Dispose();
                fsw = null;
            }
            fiStatistics = null;
        }

        private class StatisticsItem
        {

        }

        private class StatTestResult : StatisticsItem
        {
            public StatTestResult(string PN, string OPName, Guid OPGuid, StatusType Status) { this.PN = PN; this.OPName = OPName; this.OPGuid = OPGuid; this.Status = Status; }
            public string PN;
            public string OPName;
            public Guid OPGuid;
            public StatusType Status;
        }

        private class StatAddRepair : StatisticsItem
        {

        }

        public struct Settings : INotifyPropertyChanged
        {
            public bool RunOnStartUp
            {
                get { return _runonstartup; }
                set
                {
                    if (_runonstartup != value)
                    {
                        _runonstartup = value;
                        RaisePropertyChanged("RunOnStartUp");
                    }
                }
            }

            public bool AlwaysOnTop
            {
                get { return _alwaysontop; }
                set
                {
                    if (_alwaysontop != value)
                    {
                        _alwaysontop = value;
                        RaisePropertyChanged("AlwaysOnTop");
                    }
                }
            }

            public double Transparency
            {
                get { return _transparency; }
                set
                {
                    if (_transparency != value)
                    {
                        _transparency = value;
                        RaisePropertyChanged("Transparency");
                    }
                }
            }

            public Dictionary<string, Levels> Levels;

            public event PropertyChangedEventHandler PropertyChanged;

            internal bool _runonstartup;
            internal bool _alwaysontop;
            internal double _transparency;

            public static bool operator ==(Settings a, Settings b)
            {
                if (object.ReferenceEquals(a, null))
                    return object.ReferenceEquals(b, null);

                if (object.ReferenceEquals(b, null))
                    return object.ReferenceEquals(a, null);

                return (a.RunOnStartUp == b.RunOnStartUp) &&
                    (a.AlwaysOnTop == b.AlwaysOnTop) &&
                    (a.Transparency == b.Transparency) &&
                    a.Levels.OrderBy(x => x.Key).SequenceEqual(b.Levels.OrderBy(x => x.Key));
            }

            public static bool operator !=(Settings a, Settings b)
            {
                return !(a == b);
            }

            public override bool Equals(object obj)
            {
                return this == (Settings)obj;
            }

            public override int GetHashCode()
            {
                return RunOnStartUp.GetHashCode() ^ AlwaysOnTop.GetHashCode() ^ Transparency.GetHashCode() ^ Levels.GetHashCode();
            }

            private void RaisePropertyChanged(String info)
            {
                if (PropertyChanged != null)
                    PropertyChanged(this, new System.ComponentModel.PropertyChangedEventArgs(info));
            }
        }

        public class Levels
        {
            public string PartNumber
            {
                get { return _partnumber; }
                set
                {
                    if (_partnumber != value)
                    {
                        _partnumber = value;
                        RaisePropertyChanged("PartNumber");
                    }
                }
            }

            public double WarningLevel
            {
                get { return _warninglevel; }
                set
                {
                    if (_warninglevel != value)
                    {
                        _warninglevel = value;
                        RaisePropertyChanged("WarningLevel");
                    }
                }
            }

            public double CriticalLevel
            {
                get { return _criticallevel; }
                set
                {
                    if (_criticallevel != value)
                    {
                        _criticallevel = value;
                        RaisePropertyChanged("CriticalLevel");
                    }
                }
            }

            public int TotalCount
            {
                get { return _totalcount; }
                set
                {
                    if (_totalcount != value)
                    {
                        _totalcount = value;
                        RaisePropertyChanged("TotalCount");
                    }
                }
            }

            public int LastCount
            {
                get { return _lastcount; }
                set
                {
                    if (_lastcount != value)
                    {
                        _lastcount = value;
                        RaisePropertyChanged("LastCount");
                    }
                }
            }

            public event PropertyChangedEventHandler PropertyChanged;

            private string _partnumber;
            private double _warninglevel;
            private double _criticallevel;
            private int _totalcount;
            private int _lastcount;

            public static bool operator ==(Levels a, Levels b)
            {
                if (object.ReferenceEquals(a, null))
                    return object.ReferenceEquals(b, null);

                if (object.ReferenceEquals(b, null))
                    return object.ReferenceEquals(a, null);

                return (a.PartNumber == b.PartNumber) &&
                    (a.WarningLevel == b.WarningLevel) &&
                    (a.CriticalLevel == b.CriticalLevel) &&
                    (a.TotalCount == b.TotalCount) &&
                    (a.LastCount == b.LastCount);
            }

            public static bool operator !=(Levels a, Levels b)
            {
                return !(a == b);
            }

            public override bool Equals(object obj)
            {
                if (object.ReferenceEquals(obj, null) || !(obj is Levels))
                    return false;

                Levels b = (Levels)obj;
                return (this.PartNumber == b.PartNumber) &&
                    (this.WarningLevel == b.WarningLevel) &&
                    (this.CriticalLevel == b.CriticalLevel) &&
                    (this.TotalCount == b.TotalCount) &&
                    (this.LastCount == b.LastCount);
            }

            public override int GetHashCode()
            {
                return PartNumber.GetHashCode() ^ WarningLevel.GetHashCode() ^ CriticalLevel.GetHashCode() ^ TotalCount.GetHashCode() ^ LastCount.GetHashCode();
            }

            public Levels Clone()
            {
                Levels l = new Levels
                {
                    _criticallevel = this._criticallevel,
                    _lastcount = this._lastcount,
                    _partnumber = this._partnumber,
                    _totalcount = this._totalcount,
                    _warninglevel = this._warninglevel
                };

                return l;
            }

            private void RaisePropertyChanged(String info)
            {
                if (PropertyChanged != null) PropertyChanged(this, new System.ComponentModel.PropertyChangedEventArgs(info));
            }
        }
    }
}
