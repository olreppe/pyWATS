using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.IO;
using System.Xml.Linq;
using Virinco.WATS.Interface;
using System.Globalization;
using System.Threading.Tasks;
using Virinco.WATS.Interface.Statistics;
using System.Reflection;
using System.Threading;

namespace Virinco.WATS.ClientService
{
    public partial class ClientSvc : ServiceBase
    {
        public ClientSvc()
        {
            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {
                var assemblyName = new AssemblyName(args.Name);
                var pkt = assemblyName.GetPublicKeyToken();

                var ourAssembly = typeof(TDM).Assembly;
                var ourAssemblyName = new AssemblyName(ourAssembly.FullName);
                var ourPkt = ourAssemblyName.GetPublicKeyToken();

                if (pkt != null && pkt.SequenceEqual(ourPkt))
                    return ourAssembly;

                //Public key token for WATS-Core.snk is 40e2cae0ae7be54b
                var watscorePkt = new byte[] { 0x40, 0xe2, 0xca, 0xe0, 0xae, 0x7b, 0xe5, 0x4b };
                if (pkt != null && pkt.SequenceEqual(watscorePkt))
                {
                    // Try to load the actual WATS-Core type forwarding assembly
                    string installDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                    return Assembly.LoadFrom(Path.Combine(installDirectory, "Virinco.WATS.WATS-Core.dll"));
                }

                return null;
            };

            InitializeComponent();
        }

        internal System.Timers.Timer wdt;
        //internal List<Converter> cnvList;
        private Conversion cnv;
        PendingWatcher tw;
        internal TDM_ClientService api;
        internal System.Timers.Timer tmrPing;
        internal System.Timers.Timer tmrReg;
        private ServiceController controller = null;
        private FileSystemWatcher fswSettings; /* WCF Config file watcher */

        public string APIStatus { get { return api?.Status.ToString(); } }

        protected override void OnStart(string[] args)
        {
            Env.StartLogicalTraceOperation();
            Env.Trace.TraceEvent(TraceEventType.Start, 0, "WATS Client Service [v.{0}] starting @{1:o} ", System.Reflection.Assembly.GetExecutingAssembly().GetName().Version, DateTime.Now);
            SaveStatus(ServiceControllerStatus.StartPending);

            TryUpdateGPSPosition();

            // Activate & Connect to server (syncronous)
            api = new TDM_ClientService();
            api.InitializeAPI(Interface.TDM.InitializationMode.Syncronous, true);

            /*
            if (api.Status == Interface.APIStatusType.NotActivated || api.Status == Interface.APIStatusType.NotRegistered || api.Status == Interface.APIStatusType.NotInstalled)
            {
                Env.Trace.TraceEvent(TraceEventType.Error, 0, "Unable to continue\r\nClient status returned from server: {0}\r\nWATS Client service is terminating.", api.Status);
                wdt.Enabled = false; wdt.Dispose(); wdt = null;
                SaveStatus(ServiceControllerStatus.Stopped);
                api.Dispose(); api = null;
                Env.StopLogicalTraceOperation();

                return;
            }*/
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "API Initialized.");
            api.Statistics.ResetStartupCounters();

            SaveStatus(ServiceControllerStatus.Running);

            if (api.Status == Interface.APIStatusType.Online) // Wait 60sec before reporting status to allow Converters to initialize
                Task.Run(() => { System.Threading.Thread.Sleep(60000); tmr1hr_Elapsed(null); });

            // Create & Activate Watchdog timer
            wdt = new System.Timers.Timer(60000);
            wdt.Elapsed += new System.Timers.ElapsedEventHandler(wdt_Elapsed);
            wdt.Enabled = true;
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Watchdog timer initialized");

            // Create & Activate Update timers
            tmrPing = new System.Timers.Timer(300000);
            tmrPing.Elapsed += new System.Timers.ElapsedEventHandler(tmr5m_Elapsed);
            tmrPing.Enabled = true;
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Ping timer configured (5min)");

            tmrReg = new System.Timers.Timer(3600000);
            tmrReg.Elapsed += new System.Timers.ElapsedEventHandler(tmr1hr_Elapsed);
            tmrReg.Enabled = true;
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Update client timer configured (1hr)");

            tw = new PendingWatcher(true, true); /* Initialize PendingWatcher asyncronously */
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "PendingWather started, asyncronous initialization.");
            controller = GetController();
            api.StatusChanged += new Interface.TDM.StatusChangedEventHandler(api_StatusChanged);

            fswSettings = new FileSystemWatcher(Env.DataDir, Env.SettingsFileName);
            fswSettings.Changed += new FileSystemEventHandler(fswSettings_Changed);
            fswSettings.EnableRaisingEvents = true;
            Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Settingsfile listener started");

            cnv = new Conversion();
            System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(cnv.InitializeConverters));
            base.OnStart(args);
            //System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(DebugLogFiller));
            Env.Trace.TraceEvent(TraceEventType.Start, 0, "WATS Client Service started");
            Env.StopLogicalTraceOperation();
        }

        private async void TryUpdateGPSPosition()
        {
            try
            {
                if (Env.GPSPositionEnabled)
                {
                    if (await WindowsLocationService.IsAvailable())
                    {
                        if (await WindowsLocationService.IsEnabled())
                            Env.GPSPosition = (await WindowsLocationService.GetCoordinates()).ToString();
                    }
                }
            }
            catch (Exception e)
            {
                Env.LogException(e, "Failed to update GPS Position.");
            }
        }

        void fswSettings_Changed(object sender, FileSystemEventArgs e)
        {
            try
            {
                if (tmrReloadConfig == null)
                {
                    tmrReloadConfig = new System.Timers.Timer() { AutoReset = false, Interval = 1000f };
                    tmrReloadConfig.Elapsed += new System.Timers.ElapsedEventHandler(tmrReloadConfig_Elapsed);
                }
                else tmrReloadConfig.Interval = 500f;
                tmrReloadConfig.Start(); // "Schedule" a new configuration reload.
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "A Configuration change was detected, config reload will begin in {0}ms", tmrReloadConfig.Interval);
            }
            catch (Exception ex)
            {
                try { Env.LogException(ex, "Configuration file change detected, failed to schedule config-reload"); }
                catch { } // Error-reporting failed !!
            }
        }
        private static System.Timers.Timer tmrReloadConfig;
        private void tmrReloadConfig_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            try
            {
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Configuration reload is starting");
                ReloadConfig(null);
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Configuration reload completed");
            }
            catch (Exception ex)
            {
                try { Env.LogException(ex, "Configuration reload failed"); }
                catch { } // Error-reporting failed !!
            }
        }
        /*
        public void DebugLogFiller(object sender)
        {
            int i = 0; int j = 0;
            Env.Trace.TraceEvent(TraceEventType.Start, 0, "WATS LogFiller, debugging");
            while (_servicestatus==ServiceControllerStatus.Running)
            {
                Env.Trace.TraceInformation("Just some informational text to ensure that the logfile will get filled pretty quickly...");
                if (i++ > 10) { Env.Trace.TraceEvent(TraceEventType.Warning, 0, "A warning for every 10th informational texts. Also to ensure that the logfile will get filled pretty quickly..."); i = 0; j++; }
                if (j > 6) { Env.Trace.TraceEvent(TraceEventType.Error, 0, "An error for every 6th warnings. Also to ensure that the logfile will get filled pretty quickly..."); j = 0; }
                System.Threading.Thread.Sleep(1000);
            }
        }
        */
        void api_StatusChanged(object sender, Interface.TDM.StatusChangedEventArgs e)
        {
            try
            {
                lock (api) SaveStatus();
            }
            catch (Exception ex)
            {
                try { Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Unhandled exception caught in Savestatus procedure (api status changed event)!" }); }
                catch { } // Error-reporting failed !!
            }
        }

        void tmr1hr_Elapsed(object sender)
        {
            tmr1hr_Elapsed(sender, null);
        }
        void tmr1hr_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            try
            {
                lock (api)
                {
                    SaveStatus(); // Ensure pending count(s) are written to status file
                    InstallStatus.GetClientUpdateUri(api.proxy, 5000);
                }
                lock (api) api.ConnectServer(true, TimeSpan.FromSeconds(5));
                lock (api) api.UpdateClientInfo();
                lock (api) api.PostClientLog();
            }
            catch (Exception ex)
            {
                try { Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Unhandled exception caught in updateclientinfo procedure!" }); }
                catch { } // Error-reporting failed !!
            }
        }

        void tmr5m_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            try
            {
                lock (api)
                {
                    api.Ping();
                    SaveStatus();
                }
            }
            catch (Exception ex)
            {
                try { Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Unhandled exception caught in client-ping procedure!" }); }
                catch { } // Error-reporting failed !!
            }
        }

        void wdt_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            try
            {
                cnv.CheckState();
                tw.CheckState();
                SaveStatus();
            }
            catch (Exception ex)
            {
                try { Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Unhandled exception caught in watchdog timer procedure!" }); }
                catch { } // Error-reporting failed !!
            }
        }

        protected override void OnStop()
        {
            Env.Trace.TraceEvent(TraceEventType.Stop, 0, "WATS Client Service stopping");
            SaveStatus(ServiceControllerStatus.StopPending);
            tmrPing.Stop();
            tmrReg.Stop();
            wdt.Stop();

            tw.Dispose();
            cnv.Dispose();
            tmrPing.Dispose();
            tmrReg.Dispose();
            wdt.Dispose();
            tmrPing = null;
            tmrReg = null;
            wdt = null;
            tw = null;
            //ShutDownIPCService(); // IPC Service is not (yet) in use
            base.OnStop();
            SaveStatus(ServiceControllerStatus.Stopped);
            Env.Trace.TraceEvent(TraceEventType.Stop, 0, "WATS Client Service stopped");
        }
        protected override void OnContinue()
        {
            SaveStatus(ServiceControllerStatus.ContinuePending);
            wdt.Enabled = true;
            tw.Enabled = true;
            tmrPing.Enabled = true;
            tmrReg.Enabled = true;
            System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(cnv.StartAllConverters));

            base.OnContinue();
            SaveStatus(ServiceControllerStatus.Running);
            Env.Trace.TraceEvent(TraceEventType.Resume, 0, "WATS Client Service resumed");
        }
        protected override void OnPause()
        {
            SaveStatus(ServiceControllerStatus.PausePending);
            wdt.Enabled = false;
            tw.Enabled = false;
            tmrPing.Enabled = false;
            tmrReg.Enabled = false;
            cnv.PauseAllConverters();
            base.OnPause();
            SaveStatus(ServiceControllerStatus.Paused);
            Env.Trace.TraceEvent(TraceEventType.Suspend, 0, "WATS Client Service suspended");
        }
        protected override void OnCustomCommand(int command)
        {
            if (command == (int)WATSServiceCustomCommand.ReloadConfig) ReloadConfig(null);
            else if (command == (int)WATSServiceCustomCommand.CheckConnection) CheckConnection(null);
            else if (command == (int)WATSServiceCustomCommand.SubmitConnectionTestReport) SubmitConnectionTestReport(null);
            else
                base.OnCustomCommand(command);
        }

        private ServiceControllerStatus _servicestatus;

        protected void SaveStatus(ServiceControllerStatus ServiceStatus) { _servicestatus = ServiceStatus; SaveStatus(); }

        private readonly object saveStatusLock = new object();

        protected void SaveStatus()
        {
            /*
            <WATS>
              <ServiceStatus></ServiceStatus>
              <APIStatus></APIStatus>
              <pending total="" current="" future="" unprocessed="">
                [<converter name="" total="" /> ...n]
              </pending>
            </WATS>
            */

            if (api == null)
                return;

            if (Monitor.TryEnter(saveStatusLock))
            {
                try
                {
                    //Get the data
                    string serviceStatus = _servicestatus.ToString();
                    string apiStatus = api.Status.ToString();

                    string clientStatus;
                    switch (_servicestatus)
                    {
                        case ServiceControllerStatus.Stopped: clientStatus = "Stopped"; break;
                        case ServiceControllerStatus.Paused: clientStatus = "Paused"; break;
                        default:
                            clientStatus = api.Status switch
                            {
                                Interface.APIStatusType.Online => "Online",
                                Interface.APIStatusType.NotActivated or Interface.APIStatusType.NotInstalled or Interface.APIStatusType.NotRegistered => "Not Registered",
                                _ => "Offline",
                            };
                            break;
                    }

                    string launcherIcon = api.Status == APIStatusType.Online ? "Online" : "Offline";

                    bool isConverterStatsValid;
                    List<ConverterStatistics> converterStats = null;
                    try
                    {
                        converterStats = cnv?.GetConverterStatistics();
                        isConverterStatsValid = true;
                    }
                    catch (Exception ex)
                    {
                        isConverterStatsValid = false;
                        Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Unable to get converter statistics." });
                    }

                    int unprocessed = converterStats?.Sum(c => c.PendingCount) ?? 0;

                    int loaderror = 0;
                    int senderror = 0;
                    int future = 0;
                    int currentPending = 0;
                    try
                    {
                        currentPending = api.GetPendingReportCount(ref loaderror, ref senderror);
                    }
                    catch (Exception ex)
                    {
                        Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Unable to get pending reports count." });
                    }

                    int total = currentPending + unprocessed;
                    int reportCountSinceStartup = 0;
                    try
                    {
                        reportCountSinceStartup = api.Statistics.UUTReportsSinceStartup + api.Statistics.UURReportsSinceStartup;
                    }
                    catch (Exception ex)
                    {
                        Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Unable to get report since startup count." });
                    }


                    //Write to xml
                    string serviceStatusFilename = Path.Combine(api.DataDir, "ServiceStatus.xml");
                    XDocument doc;
                    try
                    {
                        if (File.Exists(serviceStatusFilename))
                            doc = XDocument.Load(serviceStatusFilename);
                        else
                            doc = CreateDefaultXDocument();
                    }
                    catch (Exception ex) //Exception during load => just create new
                    {
                        Env.Trace.TraceData(TraceEventType.Verbose, 0, new WATSLogItem() { ex = ex, Message = "Failed to load ServiceStatus." });
                        doc = CreateDefaultXDocument();
                    }

                    bool changed = false;
                    try
                    {
                        var xRoot = doc.Element("WATS");
                        if (xRoot == null)
                        {
                            doc = CreateDefaultXDocument();
                            xRoot = doc.Root;
                        }

                        changed |= SetElementValueIfChanged(xRoot, "ServiceStatus", serviceStatus);
                        changed |= SetElementValueIfChanged(xRoot, "APIStatus", apiStatus);
                        changed |= SetElementValueIfChanged(xRoot, "ClientStatus", clientStatus);

                        var xPending = xRoot.Element("pending");
                        if (xPending == null)
                        {
                            xPending = new XElement("pending");
                            xRoot.Add(xPending);
                            changed = true;
                        }

                        changed |= SetAttributeValueIfChanged(xPending, "total", total.ToString());
                        changed |= SetAttributeValueIfChanged(xPending, "current", currentPending.ToString());
                        changed |= SetAttributeValueIfChanged(xPending, "future", future.ToString());
                        changed |= SetAttributeValueIfChanged(xPending, "unprocessed", unprocessed.ToString());
                        changed |= SetAttributeValueIfChanged(xPending, "senderror", senderror.ToString());
                        changed |= SetAttributeValueIfChanged(xPending, "loaderror", loaderror.ToString());

                        //Converter stats is null if Conversion hasn't started or is disposing => Don't update converter stats
                        var xConverters = xPending.Elements("converter").ToList();
                        if (isConverterStatsValid)
                        {
                            if (converterStats != null)
                            {
                                foreach (var converterStat in converterStats)
                                {
                                    var xConverter = xConverters.FirstOrDefault(e => e.Attribute("name").Value == converterStat.Name);
                                    if (xConverter == null)
                                    {
                                        xConverter = new XElement("converter", new XAttribute("name", converterStat.Name));
                                        xPending.Add(xConverter);
                                        changed = true;
                                    }

                                    changed |= SetAttributeValueIfChanged(xConverter, "state", converterStat.State.ToString());
                                    changed |= SetAttributeValueIfChanged(xConverter, "version", converterStat.Version.ToString());
                                    changed |= SetAttributeValueIfChanged(xConverter, "total", converterStat.PendingCount.ToString());
                                    changed |= SetAttributeValueIfChanged(xConverter, "error", converterStat.ErrorCount.ToString());
                                }

                                var inactiveConverters = xConverters.Where(e => !converterStats.Any(c => c.Name == e.Attribute("name").Value)).ToList();
                                if (inactiveConverters.Any())
                                {
                                    changed = true;
                                    foreach (var converter in inactiveConverters)
                                        converter.Remove();
                                }
                            }
                            else
                            {
                                foreach (var xConverter in xConverters)
                                {
                                    changed |= SetAttributeValueIfChanged(xConverter, "state", ConverterStateEnum.NotStarted.ToString());
                                }
                            }
                        }
                        else
                        {
                            foreach (var xConverter in xConverters)
                            {
                                changed |= SetAttributeValueIfChanged(xConverter, "state", ConverterStateEnum.Failed.ToString());
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        Env.Trace.TraceData(TraceEventType.Verbose, 0, new WATSLogItem() { ex = ex, Message = "Unable to set new values to ServiceStatus." });
                    }

                    if (changed)
                    {
                        try
                        {
                            doc.Save(serviceStatusFilename);
                            Env.Trace.TraceEvent(TraceEventType.Information, 0, $"Status updated. New status={clientStatus}");
                        }
                        catch (Exception ex)
                        {
                            Env.Trace.TraceData(TraceEventType.Verbose, 0, new WATSLogItem() { ex = ex, Message = "Unable to save ServiceStatus." });
                        }
                    }


                    //Write launcher tooltip
                    string launcherTooltipFilename = Path.Combine(api.DataDir, "LauncherTooltip.txt");
                    var launcherTooltipLines = new KeyValuePair<string, string>[]
                    {
                        new ("#Icon", launcherIcon),
                        new ("Service", serviceStatus),
                        new ("Status", apiStatus),
                        new ("Created", reportCountSinceStartup.ToString()),
                        new ("Pending", currentPending.ToString())
                    };

                    bool tooltipChanged = false;
                    if (File.Exists(launcherTooltipFilename))
                    {
                        try
                        {
                            var currentTooltipLines = File.ReadAllLines(launcherTooltipFilename);
                            var currentTooltip = currentTooltipLines.Select(s => s.Split(":")).ToArray();

                            for (int i = 0; i < launcherTooltipLines.Length; i++)
                            {
                                var line = launcherTooltipLines[i];
                                var currentLine = currentTooltip[i];

                                if (currentLine.Length != 2)
                                {
                                    tooltipChanged = true;
                                    break;
                                }

                                if (line.Key != currentLine[0].Trim() || line.Value != currentLine[1].Trim())
                                {
                                    tooltipChanged = true;
                                    break;
                                }
                            }
                        }
                        catch
                        {
                            tooltipChanged = true;
                        }
                    }
                    else
                        tooltipChanged = true;

                    if (tooltipChanged)
                    {
                        try
                        {
                            var text = launcherTooltipLines.Select(l => $"{l.Key}: {l.Value}").ToArray();
                            File.WriteAllLines(launcherTooltipFilename, text);
                        }
                        catch (Exception ex)
                        {
                            Env.Trace.TraceData(TraceEventType.Verbose, 0, new WATSLogItem() { ex = ex, Message = "Unable to save LauncherTooltip." });
                        }
                    }
                }
                finally 
                {
                    Monitor.Exit(saveStatusLock);
                }
            }

            XDocument CreateDefaultXDocument() => new XDocument(new XElement("WATS"));

            bool SetElementValueIfChanged(XElement xParent, string elementName, string elementValue)
            {
                bool changed = false;
                XElement e = xParent.Element(elementName);
                if (e != null) 
                { 
                    if (e.Value != elementValue) 
                    { 
                        e.SetValue(elementValue); 
                        changed = true; 
                    } 
                }
                else 
                { 
                    e = new XElement(elementName, elementValue); 
                    xParent.Add(e); 
                    changed = true; 
                }
                return changed;
            }

            bool SetAttributeValueIfChanged(XElement xElement, string attributeName, string attributeValue)
            {
                bool changed = false;
                XAttribute xAttribute = xElement.Attribute(attributeName);
                if (xAttribute == null || xAttribute.Value != attributeValue) 
                { 
                    xElement.SetAttributeValue(attributeName, attributeValue); 
                    changed = true; 
                }
                return changed;
            }
        }

        private const string WATSServiceName = "WATSSERVICE";
        public System.ServiceProcess.ServiceController GetController()
        {
            System.ServiceProcess.ServiceController[] controllers = System.ServiceProcess.ServiceController.GetServices();
            List<System.ServiceProcess.ServiceController> svcControllers = (from controller in controllers where controller.ServiceName == WATSServiceName select controller).ToList();
            if (svcControllers.Count > 0) return svcControllers[0];
            else return null;
        }
        private void ReloadConfig(object sender)
        {
            Env.ResetTrace();

            lock (api)
            {
                cnv.Dispose();
                cnv = new Conversion();
                //api.Dispose();
                //api = new TDM_ClientService();
                api.InitializeAPI(Interface.TDM.InitializationMode.Syncronous, true);
                cnv.InitializeConverters(null);
            }
            SaveStatus();
        }
        private void CheckConnection(object sender)
        {
            lock (api)
            {
                api.CheckRemoteServer();
                SaveStatus();
            }
        }

        private void SubmitConnectionTestReport(object sender)
        {
            Env.Trace.TraceEvent(TraceEventType.Information, 0, "Submit connection test report from WATS Client Service.");
            try
            {
                var dir = new DirectoryInfo(api.ReportsDirectory);
                var file = dir.GetFiles("*.ConnectionTest").OrderByDescending(fi => fi.CreationTimeUtc).Take(1).Single();

                lock (api)
                    api.SubmitFromFile(SubmitMethod.Online, file);

                file.Delete();
                
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Submit connection test report from WATS Client Service complete.");
            }
            catch (Exception e)
            {
                Env.LogException(e, "Failed to submit connection test report from WATS Client Service.");
            }
        }
        /*
        private ClientIPC _ipcsvc;
        private System.ServiceModel.ServiceHost _ipchost;
        private void RegisterIPCService()
        {
            _ipcsvc = new ClientIPC(this);
            _ipchost = new System.ServiceModel.ServiceHost(_ipcsvc, new Uri("net.pipe://localhost/Virinco/WATS"));
            _ipchost.AddServiceEndpoint(typeof(IClientIPC), new System.ServiceModel.NetNamedPipeBinding(), "ClientIPC");
            //_ipchost = new System.ServiceModel.ServiceHost(_ipcsvc, new Uri("net.tcp://localhost:9950/Virinco/WATS/DSM/SMUXProxy"));
            //_ipchost.AddServiceEndpoint(typeof(IClientIPC), new System.ServiceModel.NetNamedPipeBinding(), "ClientIPC");
            _ipchost.Open();
        }
        
        private void ShutDownIPCService()
        {
            if (_ipchost != null)
            {
                if (_ipchost.State == System.ServiceModel.CommunicationState.Opened) _ipchost.Close(TimeSpan.FromMilliseconds(5000));
                _ipchost = null;
            }
            _ipcsvc = null;
        }
        */
    }
}
