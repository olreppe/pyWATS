using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Input;
using System.Xml.Linq;
using Virinco.WATS.Client.Configurator.Helpers;
using Virinco.WATS.Client.Configurator.Pages;
using Virinco.WATS.Client.Configurator.SupportFiles;
using Virinco.WATS.Configuration;
using Virinco.WATS.Interface;
using Virinco.WATS.Interface.Statistics;

namespace Virinco.WATS.Client.Configurator
{
    public enum ApplicationState { Login, Setup, Configured }

    public class ConfigViewModel : ObservableObject, IPageViewModel
    {
        private IPageViewModel _currentPageViewModel;
        private List<IPageViewModel> _pageViewModels;
        internal ConfigViewModel()
        {            
            Load();
            _instance = this;


            // Create default viewmodel instance:
            //TODO: select general or Setup based on clientstate
            var setup = new SetupViewModel(this);
            var general = new GeneralViewModel(this);
            PageViewModels.Add(setup);
            PageViewModels.Add(general);
            PageViewModels.Add(new ProxyViewModel(this));
            var conv = new ConvertersViewModel(this);
            PageViewModels.Add(conv);
            PageViewModels.Add(new TDMViewModel(this));
            PageViewModels.Add(new TSSupportViewModel(this));
            PageViewModels.Add(new LabViewToolkitViewModel(this));
            PageViewModels.Add(new ApiViewModel(this));
            PageViewModels.Add(new YieldSettingsViewModel(this));
            PageViewModels.Add(new SWDistViewModel(this));
            PageViewModels.Add(new SerialNumberViewModel());
            PageViewModels.Add(new GPSSettingsViewModel(this));
            CurrentPageViewModel = setup;

            // TODO: Change CurrentState to Login to enforce server login to access configurator functions.
            this.CurrentState = ViewModel.ViewModelLocator.TDMAPIStatic.ClientState == Interface.ClientStateType.NotConfigured ? ApplicationState.Setup : ApplicationState.Configured;
            if (this.CurrentState == ApplicationState.Setup)
                CurrentPageViewModel = setup;
            else
                CurrentPageViewModel = general;

            if (CurrentPageViewModel is IPageViewModel_v2 vm2)
                vm2.Initialize();

            this.IsConfigured = this.CurrentState == ApplicationState.Configured;
            this.CurrentStateChanged += ConfigViewModel_CurrentStateChanged;

            conv.PropertyChanged += Conv_PropertyChanged;
            this.ApplyCommand = new RelayCommand(param => Save());
            this.OkCommand = new RelayCommand(param => { Save(); CloseWindow(param as Window); });
            this.CancelCommand = new RelayCommand(param => CloseWindow(param as Window));

            this.WeblinkCommand = new RelayCommand(param => OpenWebPage(param as string));
        }

        private void CloseWindow(Window window)
        {
            // any cleanup before closing?
            if (window != null) window.Close();
        }

        public static void OpenWebPage(string url)
        {
            Utilities.OpenUrlInSystemDefaultProgram(url);
        }

        private void Conv_PropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        {
            if (e.PropertyName == "IsModified") this.isDirty = true;
        }

        private ICommand _changePageCommand;
        public ICommand ChangePageCommand
        {
            get
            {
                if (_changePageCommand == null)
                {
                    _changePageCommand = new RelayCommand(
                        param => ShowPage((string)param),
                        param => param is string
                    );
                }
                return _changePageCommand;
            }
        }
        public ICommand WeblinkCommand { get; private set; }
        public ICommand ApplyCommand { get; private set; }
        public ICommand OkCommand { get; private set; }
        public ICommand CancelCommand { get; private set; }


        private void ConfigViewModel_CurrentStateChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        {
            // Set setup-visibility and 
            this.IsConfigured = this.CurrentState == ApplicationState.Configured;
            RaisePropertyChanged("IsConfigured");
            if (this.IsConfigured && CurrentPageViewModel is SetupViewModel)
                CurrentPageViewModel = PageViewModels.OfType<GeneralViewModel>().Single();
        }
        public bool IsConfigured { get; private set; }
        public List<IPageViewModel> PageViewModels
        {
            get
            {
                if (_pageViewModels == null)
                    _pageViewModels = new List<IPageViewModel>();

                return _pageViewModels;
            }
        }
        public IPageViewModel CurrentPageViewModel
        {
            get
            {
                return _currentPageViewModel;
            }
            set
            {
                if (_currentPageViewModel != value)
                {
                    _currentPageViewModel = value;
                    OnPropertyChanged("CurrentPageViewModel");
                }
            }
        }
        private void ChangeViewModel(IPageViewModel viewModel)
        {
            if (!PageViewModels.Contains(viewModel))
                PageViewModels.Add(viewModel);

            var newViewModel = PageViewModels.FirstOrDefault(vm => vm == viewModel);

            //Temporary until Initialize is added to all viewmodels
            if (newViewModel is IPageViewModel_v2 newVM2)
                newVM2.Initialize();

            if (CurrentPageViewModel is IPageViewModel_v2 currentVM2)
                currentVM2.Uninitialize();

            CurrentPageViewModel = newViewModel;
        }
        public void ShowPage(string page)
        {
            IPageViewModel model = PageViewModels.FirstOrDefault(m => m.Name == page);
            if (model == null) model = PageViewModels.OfType<GeneralViewModel>().Single(); // Fallback to GeneralPage (specified model not found)
            ChangeViewModel(model);

        }
        public Version MinimumRequiredServerVersionForMES { get; set; } = new Version(2017, 3);

        private ApplicationState _state;
        internal ApplicationState CurrentState
        {
            get { return _state; }
            set
            {
                if (value != _state) { _state = value; if (this.CurrentStateChanged != null) this.CurrentStateChanged(this, new System.ComponentModel.PropertyChangedEventArgs(_state.ToString())); }
            }
        }

        public Version ServerVersion { get; set; } = ViewModel.ViewModelLocator.TDMAPIStatic.ServerVersion;

        private static ConfigViewModel _instance;

        public static ConfigViewModel Instance { get { return _instance; } }

        public string CopyrightText { get; } = $"Virinco © {DateTime.Now.Year}";

        private Values _original;
        private Values _current;

        public string MESServiceAddress { get { return _current.ServiceAddress; } }

        public string MESSWDistRoot { get { return _current.MESSWDistRoot; } set { if (_current.MESSWDistRoot != value) { _current.MESSWDistRoot = value; this.RaisePropertyChanged(nameof(MESSWDistRoot)); } } }
        public int MESFileTransferChunkSize { get { return _current.MESFileTransferChunkSize; } set { if (_current.MESFileTransferChunkSize != value) { _current.MESFileTransferChunkSize = value; this.RaisePropertyChanged(nameof(MESFileTransferChunkSize)); } } }

        internal void DisconnectServer()
        {
            bool success = true;
            try
            {
                Interface.MES.Production.SerialNumberHandler.CancelAllReservations();
            }
            catch (Exception e)
            {
                var result = MessageBox.Show($"{e.Message} See wats.log for more information. If you continue, they can be freed manually from the Serial Number Handler in your WATS Web app. Continue disconnect?" , "Disconnect", MessageBoxButton.YesNo, MessageBoxImage.Warning);
                success = result == MessageBoxResult.Yes;
            }

            if (success)
            {
                ViewModel.ViewModelLocator.TDMAPIStatic.UnRegisterClient();
                this.CurrentState = ApplicationState.Setup;

                ChangeViewModel(PageViewModels.OfType<SetupViewModel>().Single());
            }
        }

        public bool MESActivatedAndNotDirty { get { return (MESActivated && !isDirty); } }

        public bool MESActivated
        {
            get { return ((_current.ClientFunctions & ClientFunctions.MES) == ClientFunctions.MES); }
            set
            {
                if (value)
                    _current.ClientFunctions = _current.ClientFunctions | WATS.ClientFunctions.MES;
                else
                    _current.ClientFunctions = _current.ClientFunctions ^ WATS.ClientFunctions.MES;
                this.RaisePropertyChanged("MESActivated");
                this.RaisePropertyChanged("MESActivatedAndNotDirty");
            }
        }

        public bool TDMActivated { get { return ((Env.ClientFunction & ClientFunctions.TDM) == ClientFunctions.TDM); } }
        //public ClientFunctions ClientFunctions { get { return _current.ClientFunctions; } set { _current.ClientFunctions = value; this.RaisePropertyChanged("ClientFunctions"); } }

        private const string GPSPosisitionKey = "gpscoord";

        public string ClientVersion
        {
            get
            {
                var v = typeof(Virinco.WATS.Interface.TDM).Assembly.GetName().Version;
                return Utilities.GetMSIVersionString(v);
            }
        }

        public string WCFConfigFile { get { return _current.WCFConfigFile; } set { _current.WCFConfigFile = value; this.RaisePropertyChanged("WCFConfigFile"); } }
        public string ServiceAddress { get { return _current.ServiceAddress; } set { string tvalue = value.Trim(); if (_current.ServiceAddress != tvalue) { _current.ServiceAddress = tvalue; this.RaisePropertyChanged("ServiceAddress"); } } }
        public string ServiceAddressShort
        {
            get
            {
                //if https, then show skywats in dropdown and trim only to (https://)demo(.skywats.com)
                return _current.ServiceAddress;
            }
            set
            {
            }
        } //should trim it


        public string MachineName { get { return _current.MachineName; } }
        public string Location { get { return _current.Location; } set { _current.Location = value; this.RaisePropertyChanged("Location"); } }
        public string Purpose { get { return _current.Purpose; } set { _current.Purpose = value; this.RaisePropertyChanged("Purpose"); } }
        public string GPSPosition { get { return _current.GPSPosition; } set { _current.GPSPosition = value; this.RaisePropertyChanged("GPSPosition"); } }
        public bool GPSPositionEnabled { get { return _current.GPSPositionEnabled; } set { _current.GPSPositionEnabled = value; this.RaisePropertyChanged("GPSPositionEnabled"); } }
        public bool CompressionEnabled { get { return _current.CompressionEnabled; } set { _current.CompressionEnabled = value; this.RaisePropertyChanged("CompressionEnabled"); } }
        public System.Diagnostics.SourceLevels LoggingLevel { get { return _current.LoggingLevel; } set { _current.LoggingLevel = value; this.RaisePropertyChanged("LoggingLevel"); } }

        public bool UseCustomIdentifier
        {
            get => _current.UseCustomIdentifier;
            set
            {
                _current.UseCustomIdentifier = value;
                RaisePropertyChanged(nameof(UseCustomIdentifier));
            }
        }

        public string CustomIdentifier
        {
            get => _current.CustomIdentifier;
            set
            {
                _current.CustomIdentifier = value;
                RaisePropertyChanged(nameof(CustomIdentifier));
            }
        }

        public string ProxyMethod
        {
            get { return _current.ProxyMethod.ToString(); }
            set
            {
                Configuration.ProxyMethodEnum pxm;
                if (Utilities.EnumTryParse<Configuration.ProxyMethodEnum>(value, out pxm)) _current.Proxy.Method = pxm;
                this.RaisePropertyChanged("ProxyMethod");
                this.RaisePropertyChanged("ProxyMethodIsCustom");
            }
        }

        public Configuration.ProxySettings Proxy { get => _current.Proxy; }
        public string ProxyAddress { get { return _current.ProxyAddress; } set { _current.ProxyAddress = value; this.RaisePropertyChanged("ProxyAddress"); } }
        public string ProxyUsername { get { return _current.ProxyUsername; } set { _current.ProxyUsername = value; this.RaisePropertyChanged("ProxyUsername"); } }
        public string ProxyPassword { get { return _current.ProxyPassword; } set { _current.ProxyPassword = value; this.RaisePropertyChanged("ProxyPassword"); } }
        public string[] ProxyMethods { get { return Enum.GetNames(typeof(Configuration.ProxyMethodEnum)); } }
        public bool ProxyMethodIsCustom { get { return _current.ProxyMethod == Configuration.ProxyMethodEnum.Custom; } }

        public Virinco.WATS.Interface.Statistics.StatisticsReader.Settings YieldMonitor { get { return _current.YieldMonitor; } }
        public double YieldMonitor_Transparency { get { return _current.YieldMonitor.Transparency; } set { _current.YieldMonitor.Transparency = value; this.RaisePropertyChanged("YieldMonitor_Transparency"); } }
        public bool YieldMonitor_RunOnStartUp { get { return _current.YieldMonitor.RunOnStartUp; } set { _current.YieldMonitor.RunOnStartUp = value; this.RaisePropertyChanged("YieldMonitor_RunOnStartUp"); } }
        public bool YieldMonitor_AlwaysOnTop { get { return _current.YieldMonitor.AlwaysOnTop; } set { _current.YieldMonitor.AlwaysOnTop = value; this.RaisePropertyChanged("YieldMonitor_AlwaysOnTop"); } }

        public double YieldMonitor_SP_WarningLevel { get { return _selectedpartnumber.WarningLevel; } set { _selectedpartnumber.WarningLevel = value; this.RaisePropertyChanged("YieldMonitor_SP_WarningLevel"); } }
        public double YieldMonitor_SP_CriticalLevel { get { return _selectedpartnumber.CriticalLevel; } set { _selectedpartnumber.CriticalLevel = value; this.RaisePropertyChanged("YieldMonitor_SP_WarningLevel"); } }
        public int YieldMonitor_SP_LastCount { get { return _selectedpartnumber.LastCount; } set { _selectedpartnumber.LastCount = value; this.RaisePropertyChanged("YieldMonitor_SP_LastCount"); } }
        public int YieldMonitor_SP_TotalCount { get { return _selectedpartnumber.TotalCount; } set { _selectedpartnumber.TotalCount = value; this.RaisePropertyChanged("YieldMonitor_SP_TotalCount"); } }

        public IEnumerable<Virinco.WATS.Interface.Statistics.StatisticsReader.Levels> YieldMonitor_PartNumbers { get { return _current.YieldMonitor.Levels.Values; } }

        private Virinco.WATS.Interface.Statistics.StatisticsReader.Levels _selectedpartnumber;
        public Virinco.WATS.Interface.Statistics.StatisticsReader.Levels SelectedPartnumber
        {
            get { return _selectedpartnumber; }
            set
            {
                System.ComponentModel.PropertyChangedEventHandler handler = new System.ComponentModel.PropertyChangedEventHandler(_selectedpartnumber_PropertyChanged);
                if (_selectedpartnumber != null) _selectedpartnumber.PropertyChanged -= handler;
                _selectedpartnumber = value;
                _selectedpartnumber.PropertyChanged += handler;
                this.RaisePropertyChanged("SelectedPartnumber");
                this.RaisePropertyChanged("YieldMonitor_SP_WarningLevel");
                this.RaisePropertyChanged("YieldMonitor_SP_CriticalLevel");
                this.RaisePropertyChanged("YieldMonitor_SP_LastCount");
                this.RaisePropertyChanged("YieldMonitor_SP_TotalCount");
            }
        }

        void _selectedpartnumber_PropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        {
            this.RaisePropertyChanged("SelectedPartnumber");
        }

        private string[] getEndpointsImplementingContract(string p)
        {
            throw new NotImplementedException();
        }

        private bool _forcedIsDirty = false;

        public bool isDirty
        {
            get
            {
                if (!_forcedIsDirty && (_current != _original))
                {
                    return true;
                }
                else return _forcedIsDirty;
            }
            set
            {
                _forcedIsDirty = value;
                RaisePropertyChanged("isDirty");
            }
        }

        public void Save()
        {
            try
            {
                if (isDirty)
                {
                    if (_current.ProxyMethod != _original.ProxyMethod || _current.ProxyAddress != _original.ProxyAddress || _current.ProxyUsername != _original.ProxyUsername || _current.ProxyPassword != _original.ProxyPassword)
                        ViewModel.ViewModelLocator.TDMAPIStatic.ProxySettings = _current.Proxy;               
                    if (_current.CompressionEnabled != _original.CompressionEnabled)
                        Env.CompressionEnabled = _current.CompressionEnabled;
                    if (_current.LoggingLevel != _original.LoggingLevel)
                        Env.LoggingLevel = _current.LoggingLevel;
                    if (_current.ClientFunctions != _original.ClientFunctions)
                        Env.ClientFunction = _current.ClientFunctions;
                    if (_current.GPSPosition != _original.GPSPosition)
                        Env.GPSPosition = _current.GPSPosition;
                    if (_current.GPSPositionEnabled != _original.GPSPositionEnabled)
                        Env.GPSPositionEnabled = _current.GPSPositionEnabled;
                    if (_current.YieldMonitor != _original.YieldMonitor)
                    {
                        Interface.Statistics.StatisticsReader.SaveSettings(
                            new System.IO.FileInfo(
                                System.IO.Path.Combine(Env.DataDir, Interface.Statistics.StatisticsReader.StatisticsFilename)),
                            _current.YieldMonitor);
                    }
                    if (_current.MESSWDistRoot != _original.MESSWDistRoot)
                        Interface.MES.Software.Software.SetRootFolderPath(_current.MESSWDistRoot);
                    if (_current.MESFileTransferChunkSize != _original.MESFileTransferChunkSize)
                        Env.FileTransferChunkSize = _current.MESFileTransferChunkSize.ToString();
                    if (_current.UseCustomIdentifier != _original.UseCustomIdentifier || (_current.UseCustomIdentifier && _current.CustomIdentifier != _original.CustomIdentifier))
                    {
                        var dialog = new View.AuthorizeClient();
                        var dialogResult = dialog.ShowDialog();

                        //Get the original values so they can be restored if register fails
                        var originalIdentifierType = Env.IdentifierType;
                        string originalIdentifier = Env.MACAddressRegistered;

                        bool success = false;
                        if (dialogResult.HasValue && dialogResult.Value)
                        {
                            //Change how username is retrived
                            if (_current.UseCustomIdentifier)
                            {
                                Env.IdentifierType = ClientIdentifierType.Custom;
                                Env.MACAddressRegistered = _current.CustomIdentifier;
                            }
                            else
                            {
                                Env.IdentifierType = ClientIdentifierType.MacAddress;
                            }

                            //Use credentials for user with RegisterClient permission to register client with new username
                            success = SetupViewModel.SetServerAddress(_current.ServiceAddress, dialog.authUsername, dialog.authUserpass, _current.Proxy);
                        }

                        if (success)
                        {
                            System.Threading.ThreadPool.QueueUserWorkItem(r =>
                            {
                                try
                                {
                                    using (var ctrl = new ClientServiceController())
                                    {
                                        ctrl.Stop(TimeSpan.FromMilliseconds(10000));
                                        ctrl.Start(TimeSpan.FromMilliseconds(10000));
                                    }
                                }
                                catch (Exception ex)
                                {
                                    Env.LogException(ex, "Failed to restart WATS Client Service after changing identifier.");
                                }
                            });
                        }
                        else
                        {
                            Env.IdentifierType = originalIdentifierType;
                            Env.MACAddressRegistered = originalIdentifier;
                            _current.UseCustomIdentifier = _original.UseCustomIdentifier;
                        }

                        PageViewModels.OfType<TDMViewModel>().Single().Initialize();
                    }



                    // Save converter if changed:
                    PageViewModels.OfType<ConvertersViewModel>().Single().SaveConverters();

                    ViewModel.ViewModelLocator.TDMAPIStatic.UpdateClientInfo();

                    _original = _current.Clone();
                    this.RaisePropertyChanged(null);

                    this.isDirty = false;

                    try
                    {
                        const string yieldMonitorShortcut = "WATS Yield Monitor.lnk";
                        string yieldMonitorShortcutPath = Path.Combine(SupportFiles.Deploy.GetAssemblyFolder(), yieldMonitorShortcut);
                        string startupShortcutPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Startup), yieldMonitorShortcut);
                        if (_current.YieldMonitor.RunOnStartUp)
                        {
                            if (!System.IO.File.Exists(startupShortcutPath))
                                System.IO.File.Copy(yieldMonitorShortcutPath, startupShortcutPath);
                        }
                        else
                        {
                            if (System.IO.File.Exists(startupShortcutPath))
                                System.IO.File.Delete(startupShortcutPath);
                        }
                    }
                    catch (Exception e)
                    {
                        Env.LogException(e, "Add shortcut to startup failed.");
                    }
                }
            }
            catch (Exception ex)
            {
                Env.LogException(ex, "Failed to save configuration");
                System.Windows.Forms.MessageBox.Show($"Failed to save configuration file: {ex.Message}.\nException details logged to wats.log");
            }
        }
        internal void CancelChanges()
        {
            _current = _original.Clone();
            //TODO: cancel converters changes...
            //PageViewModels.Single(p => p.Name == "Converters").CancelChanges();
        }       
        public bool SetMESEndpoint(string WCFConfigFile, string endpoint, string address)
        {
            bool retVal = true;
            XDocument cfg = XDocument.Load(WCFConfigFile); //WCF config file still in use for MES
            try
            {
                int changes = 0;
                try { changes += SetEndpointAddress(cfg, endpoint, address); }
                catch (Exception ex) { Env.LogException(ex, "Failed to set MES endpoint"); }
                try { changes += SetEndpointAddress(cfg, endpoint + "-Production", address + "/ProductionService"); }
                catch (Exception ex) { Env.LogException(ex, "Failed to set MES:Production endpoint"); }
                try { changes += SetEndpointAddress(cfg, endpoint + "-Product", address + "/ProductService"); }
                catch (Exception ex) { Env.LogException(ex, "Failed to set MES:Product endpoint"); }
                try { changes += SetEndpointAddress(cfg, endpoint + "-Software", address + "/SoftwareService"); }
                catch (Exception ex) { Env.LogException(ex, "Failed to set MES:Software endpoint"); }
                try { changes += SetEndpointAddress(cfg, endpoint + "-Stream", address + "/SoftwareServiceStream"); }
                catch (Exception ex) { Env.LogException(ex, "Failed to set MES:Stream endpoint"); }
                try { changes += SetEndpointAddress(cfg, endpoint + "-Equipment", address + "/EquipmentService"); }
                catch (Exception ex) { Env.LogException(ex, "Failed to set MES:Equipment endpoint"); }
                try { changes += SetEndpointAddress(cfg, endpoint + "-Workflow", address + "/WorkflowService"); }
                catch (Exception ex) { Env.LogException(ex, "Failed to set MES:Workflow endpoint"); }
                try
                {
                    if (changes > 0)
                    {
                        cfg.Save(WCFConfigFile);
                        _current.MESServiceAddress = address;
                        this.RaisePropertyChanged("MESServiceAddress");
                    }
                }
                catch (Exception ex)
                {
                    retVal = false;
                    Env.LogException(ex, "Failed to save MES endpoint settings.");
                    System.Windows.Forms.MessageBox.Show("Unable to save MES endpoint settings.", "Error", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                retVal = false;
                Env.LogException(ex, "Missing endpoint definition in WCF Config file.");
                System.Windows.Forms.MessageBox.Show("Missing endpoint definition in WCF Config file.\nDelete file and restart the WATS Client, or manually correct the file.", "Error", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
            }
            return retVal;
        }

        private int SetEndpointAddress(XDocument cfg, string endpoint, string address)
        {
            IEnumerable<XElement> endpoints = cfg.Descendants("client").Single().Descendants("endpoint");
            XElement ep = endpoints.Single(x => x.Attribute("name").Value == endpoint);
            if (ep.Attribute("address").Value == address)
                return 0;
            else
            {
                ep.SetAttributeValue("address", address);

                try
                {
                    string bindingConfigName = ep.Attribute("bindingConfiguration").Value;
                    if (!string.IsNullOrEmpty(bindingConfigName))
                    {
                        bool tdm = bindingConfigName.Contains("IReportCenter");
                        bool ssl = address.StartsWith("https");

                        XElement binding = cfg.Descendants("binding").Single(b => b.Attribute("name").Value == bindingConfigName);
                        if (tdm)
                            binding.Element("security").Attribute("mode").Value = ssl ? "TransportWithMessageCredential" : "Message";
                        else
                            binding.Element("security").Attribute("mode").Value = ssl ? "Transport" : "None";
                    }
                }
                catch { }

                return 1;
            }
        }

        public void Load()
        {
            _original = new Values();
            _original.MachineName = Env.StationName;
            _original.Location = Env.Location;
            _original.Purpose = Env.Purpose;
            _original.WCFConfigFile = Env.WCFConfigFile;
            _original.ClientFunctions = Env.ClientFunction;
            _original.ServiceAddress = ViewModel.ViewModelLocator.TDMAPIStatic.TargetURL;
            _original.Proxy = ViewModel.ViewModelLocator.TDMAPIStatic.ProxySettings == null ? new Configuration.ProxySettings() : ViewModel.ViewModelLocator.TDMAPIStatic.ProxySettings.Clone();
            _original.GPSPosition = Env.GPSPosition;
            _original.GPSPositionEnabled = Env.GPSPositionEnabled;
            _original.CompressionEnabled = Env.CompressionEnabled;
            _original.LoggingLevel = Env.LoggingLevel;
            _original.MESSWDistRoot = Env.MESSoftwareDistributionRoot;
            _original.MESFileTransferChunkSize = Utilities.ParseInt32(Env.FileTransferChunkSize, 65000);
            _original.UseCustomIdentifier = Env.IdentifierType == ClientIdentifierType.Custom;
            _original.CustomIdentifier = _original.UseCustomIdentifier ? Env.MACAddressRegistered : string.Empty;

            // Load YieldMonitor settings
            _original.YieldMonitor = Interface.Statistics.StatisticsReader.LoadSettings(
                    new System.IO.FileInfo(
                        System.IO.Path.Combine(Env.DataDir, Interface.Statistics.StatisticsReader.StatisticsFilename)));
            if (_original.YieldMonitor.Levels.ContainsKey(""))
                this.SelectedPartnumber = _original.YieldMonitor.Levels[""];

            _current = _original.Clone();
            this.RaisePropertyChanged(null);
        }

        public event System.ComponentModel.PropertyChangedEventHandler CurrentStateChanged;
        /*
        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;

        private void RaisePropertyChanged(String info)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new System.ComponentModel.PropertyChangedEventArgs(info));
                //if (!String.IsNullOrEmpty(info) && info != "isDirty")
                PropertyChanged(this, new System.ComponentModel.PropertyChangedEventArgs("isDirty"));
            }
        }
        */

        internal static void CompleteInstallation()
        {
            Env.PersistValues = true;

            try
            {
                {
                    int attempts = 10;
                    bool success = false;
                    while (!success && attempts > 0)
                    {
                        success = ServiceStatus.SetInstallStatus(ServiceStatus.InstallStatus.Upgraded);
                        attempts--;

                        System.Threading.Thread.Sleep(500);
                    }
                }

                if (string.IsNullOrEmpty(Env.GPSPosition))
                {
                    // locate 4.2 WCF-Config and try to recover gps setting from appSettings:
                    System.IO.FileInfo wcfcfg = new System.IO.FileInfo(Env.GetConfigFilePath("WATS_WCF.config"));
                    if (wcfcfg != null && wcfcfg.Exists)
                    {
                        XDocument xd = XDocument.Load(wcfcfg.FullName);
                        if (xd != null)
                        {
                            var gps = xd.Root.Element("appSettings")?.Elements("add").SingleOrDefault(e => e.Attribute("key").Value == "gpscoord")?.Attribute("value")?.Value;
                            if (!string.IsNullOrEmpty(gps)) Env.GPSPosition = gps;
                        }
                    }
                }
                
                var oldSoftwareRootPath = Path.Combine(Env.MESSoftwareDistributionRoot, Env.InstalledPackagesFileName);
                var newSoftwareRootPath = Env.GetConfigFilePath(Env.InstalledPackagesFileName);
                if (File.Exists(oldSoftwareRootPath) && !File.Exists(newSoftwareRootPath))
                    ConvertInstalledXMLToRelativePaths(oldSoftwareRootPath, newSoftwareRootPath);

                var oldDownloadManagerConfigPath = Path.Combine(Env.MESSoftwareDistributionRoot, Env.DownloadManagerFileName);
                var newDownloadManagerConfigPath = Env.GetConfigFilePath(Env.DownloadManagerFileName);
                if (File.Exists(oldDownloadManagerConfigPath) && !File.Exists(newDownloadManagerConfigPath))
                    File.Move(oldDownloadManagerConfigPath, newDownloadManagerConfigPath);

                //Try to change domain from skywats.com to wats.com
                var tdm = new TDM_ClientConfig();
                tdm.InitializeAPI(false);
                if (tdm.ClientState != ClientStateType.NotConfigured)
                {
                    var reachableSubdomains = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

                    //Change API target url
                    {
                        var regex = new Regex(@"^https:\/\/([^\.]+)\.skywats\.com\/?$", RegexOptions.IgnoreCase);
                        var match = regex.Match(tdm.TargetURL);
                        if (match.Success)
                        {
                            var subdomain = match.Groups[1].Value;
                            var newUrl = $"https://{subdomain}.wats.com/";

                            try
                            {
                                bool success = false;
                                try
                                {
                                    var info = tdm.GetServerInfo(newUrl);
                                    success = info != null;
                                }
                                catch
                                {
                                    throw;
                                }

                                if (success)
                                {
                                    tdm.setTargetUrlUnchecked(newUrl);
                                    reachableSubdomains.Add(subdomain);
                                }
                            }
                            catch (Exception e)
                            {
                                Env.LogException(e, $"Attempt to update Target URL to {newUrl} failed.");
                            }
                        }
                    }

                    //Try to change url in each Serial number handler
                    var dir = new DirectoryInfo(Env.GetConfigFilePath("AddressStore"));
                    if (dir.Exists)
                    {
                        var regex = new Regex(@"^https:\/\/([^\.]+)\.skywats\.com\/api\/internal\/production\/?$", RegexOptions.IgnoreCase);
                        foreach (var file in dir.GetFiles("*.xml"))
                        {
                            var xmlSerializer = new System.Xml.Serialization.XmlSerializer(typeof(SerialNumbers));
                            SerialNumbers sn;
                            using (var stream = new FileStream(file.FullName, FileMode.Open, FileAccess.Read))
                                sn = (SerialNumbers)xmlSerializer.Deserialize(stream);

                            var match = regex.Match(sn.url);
                            if (match.Success)
                            {
                                var subdomain = match.Groups[1].Value;
                                var newUrl = $"https://{subdomain}.wats.com/";

                                try
                                {
                                    bool success = reachableSubdomains.Contains(subdomain);
                                    if (!success)
                                    {
                                        try
                                        {
                                            var info = tdm.GetServerInfo(newUrl, 1000, sn.tokenId);
                                            success = info != null;
                                        }
                                        catch
                                        {
                                            throw;
                                        }
                                    }

                                    if (success)
                                    {
                                        sn.url = $"{newUrl}api/Internal/Production/";
                                        reachableSubdomains.Add(subdomain);

                                        using (var stream = new FileStream(file.FullName, FileMode.OpenOrCreate, FileAccess.Write))
                                            xmlSerializer.Serialize(stream, sn);
                                    }
                                }
                                catch (Exception e)
                                {
                                    Env.LogException(e, $"Attempt to update Target URL to {newUrl} for {sn.serialNumberType} Serial Number Handler failed.");
                                }
                            }
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Env.LogException(e, "Failed to complete installation.");
            }
        }

        internal static void RedeployAllFromBackup()
        {
            try
            {
                // Overwrite existing deploy.xml with new
                string supportFilesRootPath = Deploy.GetSupportFilesRoot();
                string newDeployFilePath = Path.Combine(supportFilesRootPath, Env.DeployConfigFileName);
                string deployFilePath = Deploy.GetDeployConfigFilePath();
                File.Copy(newDeployFilePath, deployFilePath, true);

                string backupDeployFilePath = deployFilePath + ".bak";
                if (File.Exists(backupDeployFilePath))
                {
                    var xBackupDeploy = XDocument.Load(backupDeployFilePath);
                    var xBackupProducts = xBackupDeploy.Root.Elements(xBackupDeploy.Root.Name.Namespace + "Product")
                        .Where(p => p.Attribute("State").Value == "Installed")
                        .Select(p => new 
                        { 
                            Id = p.Attribute("Id").Value,
                            ModifyXml = p.Element(xBackupDeploy.Root.Name.Namespace + "ModifyXml"),
                            ModifyINI = p.Element(xBackupDeploy.Root.Name.Namespace + "ModifyINI")
                        }).ToArray();

                    var xDeploy = XDocument.Load(deployFilePath);
                    foreach(var xProduct in xDeploy.Root.Elements(Deploy.xmlns + "Product"))
                    {
                        var product = new Product(xProduct, supportFilesRootPath, true);
                        var xBackupProduct = xBackupProducts.FirstOrDefault(p => p.Id == product.Id);
                        if (xBackupProduct != null)
                        {                            
                            product.DeployFiles(true, true);

                            //Keep restore values or add default ones
                            var xModifyXml = xProduct.Element(Deploy.xmlns + "ModifyXml");
                            if (xModifyXml != null && xBackupProduct.ModifyXml != null)                            
                                CopyOriginalValues(xBackupProduct.ModifyXml, xModifyXml);

                            var xModifyIni = xProduct.Element(Deploy.xmlns + "ModifyINI");
                            if (xModifyIni != null && xBackupProduct.ModifyINI != null)
                                CopyOriginalValues(xBackupProduct.ModifyINI, xModifyIni);
                        }
                    }
                    xDeploy.Save(deployFilePath);
                }
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Failed to get deployment configuration" });
            }

            void CopyOriginalValues(XElement xSource, XElement xTarget)
            {
                var xOriginalValues = xSource.Elements(Deploy.xmlns + "original-value");
                if (xOriginalValues == null || !xOriginalValues.Any())
                    xOriginalValues = xSource.Elements(Deploy.xmlns + "set-value");

                foreach (var xOriginalValue in xOriginalValues)
                {
                    string value = xOriginalValue.Value;
                    if (Deploy.DefaultValues.ContainsKey(xOriginalValue.Value))
                        value = Deploy.DefaultValues[xOriginalValue.Value];
                    xTarget.Add(new XElement(Deploy.xmlns + "original-value", xOriginalValue.Attributes(), new XText(value)));
                }
            }
        }        

        internal static void UpdateLabviewToolkits()
        {
            try
            {
                var labViews = LabViewToolkitViewModel.GetLabViews();

                foreach (var labView in labViews)
                {
                    if (labView.Deployed)
                    {
                        //Update
                        bool success = labView.DeployFiles(true);
                        if (success)
                            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, $"Successfully updated LabVIEW Toolkit for {labView.ProductName}.");
                        else
                            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, $"Failed to update LabVIEW Toolkit for {labView.ProductName}.");
                    }
                }
            }
            catch (Exception e)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = "An unhandled error occured while updating LabVIEW Toolkits." });
            }
        }
        internal static void RetryTSErrorFiles()
        {
            try
            {
                var dumpfolder = System.IO.Path.Combine(Env.DataDir, "TSDump");
                var errfolder = System.IO.Path.Combine(dumpfolder, "Error");
                var files = System.IO.Directory.GetFiles(errfolder, "*.xml");
                int skipped = 0; int retried = 0; int failed = 0;
                foreach (var src in files)
                {
                    try
                    {
                        var dest = System.IO.Path.Combine(dumpfolder, System.IO.Path.GetFileName(src));
                        if (!System.IO.File.Exists(dest))
                        {
                            System.IO.File.Move(src, dest); // skip if already exists...
                            retried++;
                        }
                        else
                        {
                            skipped++;
                        }
                    }
                    catch
                    {
                        failed++;
                    }
                }
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Information, 0, new WATSLogItem() { Message = $"Rescheduling TSDump files: {retried} re-scheduled, {skipped} skipped, {failed} failed." });
            }
            catch (Exception e) // report exception
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = "An unhandled error occured while scheduling retry of TSDump files." });
            }
        }

        internal static void RetryInvalidFiles()
        {
            try
            {
                var files = new DirectoryInfo(new TDM().ReportsDirectory).GetFiles($"*.{Report.ReportTransferStatusEnum.InvalidReport}");
                int skipped = 0; int retried = 0; int failed = 0;
                foreach (var file in files)
                {
                    try
                    {
                        string newName = Path.Combine(file.DirectoryName, $"{Path.GetFileNameWithoutExtension(file.Name)}.{Report.ReportTransferStatusEnum.Queued}");
                        if (!File.Exists(newName))
                        {
                            file.MoveTo(newName);
                            retried++;
                        }
                        else
                            skipped++;
                    }
                    catch
                    {
                        failed++;
                    }
                }
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Information, 0, new WATSLogItem() { Message = $"Rescheduling Invalid reports: {retried} re-scheduled, {skipped} skipped, {failed} failed." });
            }
            catch (Exception e) // report exception
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = "An unhandled error occured while scheduling retry of Invalid reports." });
            }
        }

        private static void ConvertInstalledXMLToRelativePaths(string oldSoftwareRootPath, string newSoftwareRootPath)
        {
            //Convert installedPackages.xml to use relative paths, and move installedPackages.xml to config folder
            var xDoc = XDocument.Load(oldSoftwareRootPath);
            foreach (var xPackage in xDoc.Root.Elements("Package").Where(e => bool.Parse(e.Attribute("Installed")?.Value)))
            {
                var filePath = xPackage.Descendants("File").FirstOrDefault()?.Attribute("Path")?.Value;
                if (!string.IsNullOrEmpty(filePath))
                {
                    string rootPath = null;
                    var hasRootDirectory = !IsSubDirectory(Env.MESSoftwareDistributionRoot, new FileInfo(filePath).Directory.FullName);
                    if (hasRootDirectory)
                    {
                        DirectoryInfo target = null;
                        bool isPackageFolder = bool.Parse(xPackage.Attribute("PackageFolder")?.Value);
                        var rootFolders = isPackageFolder ? new[] { xPackage.Attribute("Name")?.Value } : xPackage.Descendants("Folder").Select(e => e.Attribute("Name")?.Value).ToArray();
                        var directory = new FileInfo(filePath).Directory;
                        while (directory != null)
                        {
                            if (rootFolders.Contains(directory.Name))
                                target = directory;

                            directory = directory.Parent;
                        }

                        rootPath = isPackageFolder ? target.FullName : (target.Parent?.FullName ?? target.FullName);
                        xPackage.Add(new XAttribute("RootDirectory", target.Parent?.FullName ?? target.FullName));
                    }
                    else
                    {
                        rootPath = Path.Combine(Env.MESSoftwareDistributionRoot, bool.Parse(xPackage.Attribute("PackageFolder")?.Value) ? xPackage.Attribute("Name")?.Value : "");
                        xPackage.Add(new XAttribute("RootDirectory", ""));
                    }

                    foreach (var xFile in xPackage.Descendants("File"))
                    {
                        var path = xFile.Attribute("Path")?.Value;
                        var relativePath = Path.GetRelativePath(rootPath, path);

                        xFile.SetAttributeValue("Path", relativePath);
                    }
                }
            }

            xDoc.Save(newSoftwareRootPath);
            File.Move(oldSoftwareRootPath, newSoftwareRootPath + ".bak");

            bool IsSubDirectory(string parentPath, string path)
            {
                var parentDir = new DirectoryInfo(parentPath);
                var dir = new DirectoryInfo(path);

                while (dir != null)
                {
                    if (dir.FullName == parentDir.FullName)
                        return true;
                    else
                        dir = dir.Parent;
                }

                return false;
            }            
        } 

        internal static void CompleteUnInstallation()
        {
            try { Deploy.UnDeployAll(); }
            catch { } // Dont care...

            try
            {
                var proxy = new REST.ServiceProxy();
                proxy.LoadSettings();
                proxy.ClearTarget();
            }
            catch { } // Dont care...

            //Reset identifier type on uninstall?
            //try
            //{
            //    Env.IdentifierType = ClientIdentifierType.MacAddress;
            //}
            //catch { }
        }

        public string GPSExampleUrl { get { return Virinco.WATS.Client.Configurator.Resources.Strings.Cfg_Gen_Gen_gps_ExampleUrl; } }

        public string Name
        {
            get
            {
                return "Config";
            }
        }
        private struct Values
        {
            public string WCFConfigFile;
            public string ServiceAddress;
            public string MachineName;
            public string Location;
            public string Purpose;
            public string GPSPosition;
            public bool GPSPositionEnabled;
            public bool CompressionEnabled;
            public System.Diagnostics.SourceLevels LoggingLevel;
            public ClientFunctions ClientFunctions;
            public bool UseCustomIdentifier;
            public string CustomIdentifier;

            public Configuration.ProxySettings Proxy;

            public Interface.Statistics.StatisticsReader.Settings YieldMonitor;

            public Configuration.ProxyMethodEnum ProxyMethod { get { return Proxy.Method; } set { Proxy.Method = value; } }
            public string ProxyAddress { get { return Proxy.Address; } set { Proxy.Address = value; } }
            public string ProxyUsername { get { return Proxy.Username; } set { Proxy.Username = value; } }
            public string ProxyPassword { get { return Proxy.Password; } set { Proxy.Password = value; } }
            public string ProxyDomain { get { return Proxy.Domain; } set { Proxy.Domain = value; } }


            public string MESServiceAddress;
            public string MESSWDistRoot;
            public int MESFileTransferChunkSize;


            public static bool operator ==(Values a, Values b)
            {
                if (object.ReferenceEquals(a, null)) return object.ReferenceEquals(b, null);
                if (object.ReferenceEquals(b, null)) return object.ReferenceEquals(a, null);
                return (a.WCFConfigFile == b.WCFConfigFile) &&
                    (a.ServiceAddress == b.ServiceAddress) &&
                    (a.MachineName == b.MachineName) &&
                    (a.Location == b.Location) &&
                    (a.Purpose == b.Purpose) &&
                    (a.Proxy == b.Proxy) &&
                    (a.YieldMonitor == b.YieldMonitor) &&
                    (a.GPSPosition == b.GPSPosition) &&
                    (a.CompressionEnabled == b.CompressionEnabled) &&
                    (a.GPSPositionEnabled == b.GPSPositionEnabled) &&
                    (a.LoggingLevel == b.LoggingLevel) &&
                    (a.MESServiceAddress == b.MESServiceAddress) &&
                    (a.MESSWDistRoot == b.MESSWDistRoot) &&
                    (a.MESFileTransferChunkSize == b.MESFileTransferChunkSize) &&
                    (a.ClientFunctions == b.ClientFunctions) &&
                    (a.UseCustomIdentifier == b.UseCustomIdentifier) &&
                    (a.CustomIdentifier == b.CustomIdentifier)
                    ;
            }
            public static bool operator !=(Values a, Values b) { return !(a == b); }
            public override bool Equals(object obj)
            {
                return this == (Values)obj;
            }
            public override int GetHashCode()
            {
                return
                    WCFConfigFile.GetHashCode() ^
                    ServiceAddress.GetHashCode() ^
                    MachineName.GetHashCode() ^
                    Location.GetHashCode() ^
                    Purpose.GetHashCode() ^
                    Proxy.GetHashCode() ^
                    YieldMonitor.GetHashCode() ^
                    GPSPosition.GetHashCode() ^
                    CompressionEnabled.GetHashCode() ^
                    GPSPositionEnabled.GetHashCode() ^
                    LoggingLevel.GetHashCode() ^
                    MESServiceAddress.GetHashCode() ^
                    MESSWDistRoot.GetHashCode() ^
                    MESFileTransferChunkSize.GetHashCode() ^
                    ClientFunctions.GetHashCode() ^
                    UseCustomIdentifier.GetHashCode() ^
                    CustomIdentifier.GetHashCode();
            }

            internal Values Clone()
            {
                Values val = this; /* copies struct-based values */
                val.Proxy = ReferenceEquals(this.Proxy, null) ? new Configuration.ProxySettings() : this.Proxy.Clone();
                val.YieldMonitor.Levels = new Dictionary<string, Interface.Statistics.StatisticsReader.Levels>();
                foreach (Virinco.WATS.Interface.Statistics.StatisticsReader.Levels level in this.YieldMonitor.Levels.Values)
                    val.YieldMonitor.Levels.Add(level.PartNumber, level.Clone());
                return val;
            }
        }
    }
}
