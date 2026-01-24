using System;
using System.Windows;
using System.ServiceProcess;
using System.IO;
using System.Xml.Linq;
using System.IO.Compression;
using System.Windows.Forms;
using Virinco.WATS.Interface.Statistics;
using Newtonsoft.Json;

namespace Virinco.WATS.Client.StatusMonitor.ViewModel
{
    /// <summary>
    /// This class contains properties that a View can data bind to.
    /// <para>
    /// Use the <strong>mvvminpc</strong> snippet to add bindable properties to this ViewModel.
    /// </para>
    /// <para>
    /// You can also use Blend to data bind with the tool's support.
    /// </para>
    /// <para>
    /// See http://www.galasoft.ch/mvvm/getstarted
    /// </para>
    /// </summary>
    public class ClientMonitorViewModel : Interface.Statistics.StatisticsReader
    {
        public string CopyrightText { get; } = $"Virinco © {DateTime.Now.Year}";

        /// <summary>
        /// Initializes a new instance of the ClientMonitorViewModel class.
        /// </summary>
        internal ClientMonitorViewModel(TDM_ClientConfig api) : base(api)
        {
            this.url = api.TargetURL;
            /* Put filewatcher on ServiceStatus file */
            fsw = new FileSystemWatcher(Path.GetDirectoryName(status.ServiceStatusFileName), Path.GetFileName(status.ServiceStatusFileName));
            fsw.Changed += new FileSystemEventHandler(ServiceStatusFile_Changed);
            fsw.EnableRaisingEvents = true;
            UpdateServiceStatus(); // Force update;
            /* Use timer (30s) to check Service status through the ServiceController */
            tmrUpdateStatus = new System.Timers.Timer(30000f);
            tmrUpdateStatus.Elapsed += new System.Timers.ElapsedEventHandler(tmrUpdateStatus_Elapsed);
            tmrUpdateStatus.Start();
        }

        public int PendingReports
        {
            get { return _pendingReports; }
            set
            {
                if (_pendingReports != value) { _pendingReports = value; RaisePropertyChanged("PendingReports"); RaisePropertyChanged("NotifyIconTooltip"); }
            }
        }

        public string url { get; set; }

        int _pendingReports = 0;

        private FileSystemWatcher fsw;
        private System.Timers.Timer tmrUpdateStatus;

        private readonly ServiceStatus status = new ServiceStatus();

        void ServiceStatusFile_Changed(object sender, FileSystemEventArgs e)
        {
            UpdateServiceStatus();
        }

        void tmrUpdateStatus_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            UpdateServiceStatus();
        }

        public string LicensedToCompany { get { return GetLicensedTo(); } }

        string _licensedTo = null;
        private string GetLicensedTo()
        {
            if (_licensedTo == null)
            {
                Microsoft.Win32.RegistryKey rk = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS");
                if (rk != null) _licensedTo = rk.GetValue("Company") as String;
            }
            return _licensedTo;
        }

        public string LicenseKey { get { return GetLicenseKey(); } }
        string _licenseKey = null;
        private string GetLicenseKey()
        {
            if (_licenseKey == null)
            {
                Microsoft.Win32.RegistryKey rk = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS");
                if (rk != null) _licenseKey = rk.GetValue("PID") as String;
            }
            return _licenseKey;
        }

        public string ClientVersion
        {
            get
            {
                var v = typeof(Virinco.WATS.Interface.TDM).Assembly.GetName().Version;
                return Utilities.GetMSIVersionString(v);
            }
        }

        public string CoreVersion
        {
            get
            {
                var v = typeof(Virinco.WATS.Env).Assembly.GetName().Version;
                return Utilities.GetMSIVersionString(v);
            }
        }
      
        public string ClientMonitorVersion
        {
            get
            {
                var v = this.GetType().Assembly.GetName().Version;
                return Utilities.GetMSIVersionString(v);
            }
        }

        private string _servicestatus = "Unknown";
        public string ServiceStatus
        {
            get { return _servicestatus; }
            private set
            {
                if (_servicestatus != value)
                {
                    _servicestatus = value;
                    base.RaisePropertyChanged("ServiceStatus");
                    base.RaisePropertyChanged("StartServiceVisibility");
                    base.RaisePropertyChanged("NotifyIconTooltip");
                    //((App)App.Current).setNotifyIconStatus(_servicestatus, _serviceapistatus);
                    //TBD: Set status.txt ???
                }
            }
        }
        public string NotifyIconTooltip
        {
            get
            {
                string statustext;
                if (ServiceStatus == "Running") statustext = ServiceAPIStatus;
                else if (_serviceapistatus == Interface.APIStatusType.NotActivated) statustext = "Client Not Activated";
                else statustext = "Service not running";
                return string.Format("Status: {0}\r\nPending: {1}\r\nTotal: {2}", statustext, PendingReports, UUTReportsSinceStartup + UURReportsSinceStartup, UUTReportsTotal + UURReportsTotal);
            }
        }

        public Visibility StartServiceVisibility { get { return (_servicestatus == "Running") ? Visibility.Hidden : Visibility.Visible; } }

        void UpdateServiceStatus()
        {
            status.UpdateServiceStatus();
            ServiceStatus = status.ClientServiceStatus;
            ServiceAPIStatus = status.ServiceAPIStatus;
            PendingReports = status.PendingReports;
        }

        private Virinco.WATS.Interface.APIStatusType _serviceapistatus;
        public string ServiceAPIStatus
        {
            get { return _serviceapistatus.ToString(); }
            private set
            {
                Virinco.WATS.Interface.APIStatusType newserviceapistatus;
                if (Utilities.EnumTryParse<Virinco.WATS.Interface.APIStatusType>(value, out newserviceapistatus))
                    if (_serviceapistatus != newserviceapistatus)
                    {
                        _serviceapistatus = newserviceapistatus;
                        RaisePropertyChanged("ServiceAPIStatus");
                        RaisePropertyChanged("NotifyIconTooltip");
                        
                        //((App)App.Current).setNotifyIconStatus(ServiceStatus, newserviceapistatus);
                        //TBD: Set status.txt ???

                    }
            }
        }


        public void GenerateSupportLog(string zipPath)
        {           
            try
            {
                using (var zipFile = new FileStream(zipPath, FileMode.Create, FileAccess.Write))
                using (var zipArchive = new ZipArchive(zipFile, ZipArchiveMode.Create))
                {
                    AddToArchive(zipArchive, Env.GetConfigFilePath(Env.WatsLogFileName), Env.WatsLogFileName, true);
                    AddToArchive(zipArchive, status.ServiceStatusFileName, Path.GetFileName(status.ServiceStatusFileName), false);
                    AddToArchive(zipArchive, Env.GetConfigFilePath(Env.DeployConfigFileName), Env.DeployConfigFileName, false);                    
                    AddToArchive(zipArchive, Env.GetConfigFilePath(Env.ConvertersFileName), Env.ConvertersFileName, false);
                }
            }
            catch(Exception e)
            {
                string message = "Generating support log failed";
                Env.LogException(e, message);
                System.Windows.MessageBox.Show($"{message}: {e.Message}");
            }

            void AddToArchive(ZipArchive zipArchive, string filePath, string entryName, bool throwOnError)
            {
                var zipEntry = zipArchive.CreateEntry(entryName, CompressionLevel.Optimal);
                using (var entryStream = zipEntry.Open())
                {
                    try
                    {
                        using (var sourceStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                            sourceStream.CopyTo(entryStream);
                    }
                    catch (Exception e)
                    {
                        if (throwOnError)
                            throw;
                        else
                        {
                            using (var writer = new StreamWriter(entryStream))
                            {
                                writer.WriteLine($"Failed to add {entryName}.");
                                writer.Write(JsonConvert.SerializeObject(e));
                            }
                        }
                    }
                }
            }
        }
    }
}
