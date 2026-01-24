using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.Windows.Data;
using System.Windows;
using System.Windows.Threading;
using System.ServiceProcess;
using System.IO;

namespace Virinco.WATS.Client.Configurator.ViewModel
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
        /// <summary>
        /// Initializes a new instance of the ClientMonitorViewModel class.
        /// </summary>
        internal ClientMonitorViewModel(TDM_ClientConfig api) :base(api)
        {

            ServiceStatusFileName = Path.Combine(api.DataDir, "ServiceStatus.xml");            
            /* Put filewatcher on ServiceStatus file */
            fsw = new FileSystemWatcher(api.DataDir, "ServiceStatus.xml");
            fsw.Changed += new FileSystemEventHandler(ServiceStatusFile_Changed);
            fsw.EnableRaisingEvents = true;
            UpdateServiceStatus(); // Force update;
            /* Use timer (30s) to check Service status through the ServiceController */
            tmrUpdateStatus = new System.Timers.Timer(30000f);
            tmrUpdateStatus.Elapsed += new System.Timers.ElapsedEventHandler(tmrUpdateStatus_Elapsed);
            tmrUpdateStatus.Start();
            PendingReports = api.GetPendingReportCount() + api.GetPendingTSConversions();
            this.PropertyChanged += new System.ComponentModel.PropertyChangedEventHandler(ClientMonitorViewModel_PropertyChanged);
        }

        int _pendingReports = 0;
        public int PendingReports { 
            get { return _pendingReports; }
            set
            {
                if (_pendingReports != value) { _pendingReports = value; RaisePropertyChanged("PendingReports"); RaisePropertyChanged("NotifyIconTooltip"); }
            }
        }

        void ClientMonitorViewModel_PropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        {          
            if(e.PropertyName == "")
                UpdateNotifyIcon();
        }
        private string ServiceStatusFileName;        
        private FileSystemWatcher fsw;
        private System.Timers.Timer tmrUpdateStatus;
        void ServiceStatusFile_Changed(object sender, FileSystemEventArgs e)
        {
            UpdateServiceStatus();
        }

        void tmrUpdateStatus_Elapsed(object sender, System.Timers.ElapsedEventArgs e)
        {
            UpdateServiceStatus();
            UpdateNotifyIcon();
        }

        private void UpdateNotifyIcon()
        {
            PendingReports = ViewModelLocator.TDMAPIStatic.GetPendingReportCount() + ViewModelLocator.TDMAPIStatic.GetPendingTSConversions();
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

        public Version ClientVersion { get { return typeof(Virinco.WATS.Interface.TDM).Assembly.GetName().Version; } }
        public Version CoreVersion { get { return typeof(Virinco.WATS.Env).Assembly.GetName().Version; } }
        public Version ClientMonitorVersion { get { return this.GetType().Assembly.GetName().Version; } }
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
                    ((App)App.Current).setNotifyIconStatus(_servicestatus, _serviceapistatus);
                }
            }
        }
        public string NotifyIconTooltip
        {
            get
            {
                string statustext;
                if (ServiceStatus == "Running") statustext=ServiceAPIStatus;
                else if (_serviceapistatus==Interface.APIStatusType.NotActivated ) statustext="Client Not Activated";
                else statustext="Service not running";
                return string.Format("Status: {0}\r\nPending: {1}\r\nTotal: {2}", statustext, PendingReports, UUTReportsSinceStartup + UURReportsSinceStartup, UUTReportsTotal + UURReportsTotal);
            }
        }

        public Visibility StartServiceVisibility { get { return (_servicestatus == "Running") ? Visibility.Hidden : Visibility.Visible; } }

        void UpdateServiceStatus()
        {
            bool usestatusfileassource = true;
            try
            {
                ServiceController ctrl = ((App)App.Current).GetWATSService();
                if (ctrl != null) { ServiceStatus = ctrl.Status.ToString(); usestatusfileassource = false; }
                    
            }
            catch { } // Don't care (designtime exception??
            try
            {
                XDocument doc = XDocument.Load(ServiceStatusFileName);
                XElement cs = doc.Element("WATS");
                if (cs != null)
                {
                    ServiceAPIStatus = cs.Element("APIStatus").Value;
                    if (usestatusfileassource) ServiceStatus = cs.Element("ServiceStatus").Value;
                }
            }
            catch
            {
                if (usestatusfileassource) ServiceStatus = "Service not found";
                ServiceAPIStatus = "Unknown";
            }
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
                    ((App)App.Current).setNotifyIconStatus(ServiceStatus, newserviceapistatus);
                }
            }
        }

        public void StartWATSService(object sender)
        {
            ServiceController ctrl = ((App)App.Current).GetWATSService();

            if (ctrl == null) this.ServiceStatus = "Service not found";
            else
            {
                int i = 60;
                while (ctrl.Status != ServiceControllerStatus.Running)
                {
                    this.ServiceStatus = String.Format("{0} Timeout:{1}", ctrl.Status, i);
                    if (ctrl.Status == ServiceControllerStatus.Paused) try { ctrl.Continue(); } catch { }
                    else if (ctrl.Status == ServiceControllerStatus.Stopped) try { ctrl.Start(); } catch { }
                    if (i-- <= 0) break;
                    System.Threading.Thread.Sleep(1000);
                    ctrl.Refresh();
                }
                this.ServiceStatus = String.Format("{0}", ctrl.Status);
            }
        }
    }
}
