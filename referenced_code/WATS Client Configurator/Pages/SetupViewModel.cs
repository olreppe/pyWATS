using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Mail;
using System.Text;
using System.Windows.Input;
using Virinco.WATS.Client.Configurator.Helpers;
using Virinco.WATS.Client.Configurator.ViewModel;
using Virinco.WATS.Configuration;

namespace Virinco.WATS.Client.Configurator.Pages
{
    class SetupViewModel : ObservableObject, IPageViewModel_v2
    {
        public string Name
        {
            get { return "Setup"; }
        }

        public string ServiceAddress
        {
            get { return serviceAddress; }
            set
            {
                //System.Diagnostics.Debug.Print($"ServiceAddress change from {serviceAddress} to {value}");
                if (value != serviceAddress)
                {
                    serviceAddress = value; RaisePropertyChanged("ServiceAddress");
                    // TODO: Implement scheme + fqdn "live-helper" (?)... Enable login button on validated url
                    //var validUri = Uri.IsWellFormedUriString(serviceAddress, UriKind.Absolute);
                    //if (ServiceAddressIsValid != validUri) { ServiceAddressIsValid = validUri; RaisePropertyChanged("ServiceAddressIsValid"); }
                }
            }
        }

        //public bool ServiceAddressIsValid { get; private set; }

        public string UserName
        {
            get { return userName; }
            set { if (value != userName) { userName = value; RaisePropertyChanged("UserName"); } }
        }

        public string ServerType
        {
            get { return serverType; }
            set { if (value != serverType) { serverType = value; RaisePropertyChanged("ServerType"); } }
        }

        public string Location
        {
            get => location;
            set
            {
                location = value;
                RaisePropertyChanged(nameof(Location));
            }
        }

        public string Purpose
        {
            get => purpose;
            set
            {
                purpose = value;
                RaisePropertyChanged(nameof(Purpose));
            }
        }

        public bool UseCustomIdentifier
        {
            get => useCustomIdentifier;
            set
            {
                useCustomIdentifier = value;
                RaisePropertyChanged(nameof(UseCustomIdentifier));
            }
        }

        public string CustomIdentifier
        {
            get => customIdentifier;
            set
            {
                customIdentifier = value;
                RaisePropertyChanged(nameof(CustomIdentifier));
            }
        }

        public ConfigViewModel Config { get; set; }

        public ICommand ConnectCommand { get; }

        public ICommand NewCustomerCommand { get; }

        public ICommand GenerateCustomIdentifierCommand { get; }

        private string serviceAddress;
        private string userName;
        private string serverType;
        private string location;
        private string purpose;
        private bool useCustomIdentifier;
        private string customIdentifier;

        internal SetupViewModel(ConfigViewModel config)
        {
            Config = config;
            ConnectCommand = new RelayCommand(param => Login(((System.Windows.Controls.PasswordBox)param).Password), param => param is System.Windows.Controls.PasswordBox);
            NewCustomerCommand = new RelayCommand(param => Utilities.OpenUrlInSystemDefaultProgram("https://register.wats.com/"));
            GenerateCustomIdentifierCommand = new RelayCommand(param => GenerateCustomIdentifier());
        }

        public void Initialize()
        {
            serviceAddress = Config.ServiceAddress;
            Location = Config.Location;
            Purpose = Config.Purpose;
            UseCustomIdentifier = Config.UseCustomIdentifier;
            CustomIdentifier = Config.CustomIdentifier;
        }

        public void Uninitialize() { }

        private void Login(string password)
        {
            if (ValidateAddress())
            {
                var originalIdentifierType = Env.IdentifierType;
                var originalIdentifier = Env.MACAddressRegistered;

                ClientIdentifierType newIdentifierType;
                string newIdentifier;
                if (UseCustomIdentifier)
                {
                    Env.IdentifierType = ClientIdentifierType.Custom;
                    Env.MACAddressRegistered = CustomIdentifier;

                    newIdentifierType = ClientIdentifierType.Custom;
                    newIdentifier = CustomIdentifier;
                }
                else
                {
                    Env.IdentifierType = ClientIdentifierType.MacAddress;

                    newIdentifierType = ClientIdentifierType.MacAddress;
                    newIdentifier = originalIdentifier;
                }

                Env.Location = location ?? string.Empty;
                Env.Purpose = purpose ?? string.Empty;

                bool result = SetServerAddress(ServiceAddress, UserName, password, Config.Proxy);
                if (result)
                {
                    ViewModel.ViewModelLocator.TDMAPIStatic.InitializeAPI(true);
                    Config.Load();

                    if (!String.IsNullOrEmpty(ViewModel.ViewModelLocator.TDMAPIStatic.TargetURL))
                    {
                        ViewModel.ViewModelLocator.TDMAPIStatic.UpdateClientInfo();
                        Config.CurrentState = ApplicationState.Configured;
                    }
                    // Trigger service restart
                    System.Threading.ThreadPool.QueueUserWorkItem(r =>
                    {
                        try
                        {
                            using (var ctrl = new Configuration.ClientServiceController())
                            {
                                ctrl.Stop(TimeSpan.FromMilliseconds(10000));
                                ctrl.Start(TimeSpan.FromMilliseconds(10000));
                            }
                        }
                        catch (Exception ex)
                        {
                            Env.LogException(ex, "Failed to restart WATS Client Service after login");
                        }
                    });
                }
                else
                {
                    if (newIdentifier != originalIdentifier)
                        Env.MACAddressRegistered = originalIdentifier;

                    if (newIdentifierType != originalIdentifierType)
                        Env.IdentifierType = originalIdentifierType;
                }
            }
            else
            {
                string message = $"'{ServiceAddress}' is not a valid server address. Please specify a valid server address.";
                System.Windows.Forms.MessageBox.Show(message, "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);         
            }        
        }

        private bool ValidateAddress()
        {
            bool valid = false;
            Uri address;
            if (ServiceAddress.Contains("://"))
            {
                // assume entire string, just verify Uri
                valid = Uri.TryCreate(ServiceAddress, UriKind.Absolute, out address);
                if (valid && address.Scheme != "http" && address.Scheme != "https")
                    return false;
            }
            else if (ServiceAddress.Contains(".skywats.com"))
            {
                // No protocol specified, but contains skywats.com, add https and change to skywats
                valid = Uri.TryCreate($"https://{ServiceAddress}", UriKind.Absolute, out address);
                ServerType = "skyWATS";

            }
            else if (ServiceAddress.Contains("."))
            {
                // assume server.fqdn, add default protocol (https)
                valid = Uri.TryCreate($"https://{ServiceAddress}", UriKind.Absolute, out address);

            }
            else if (string.Compare(ServerType, "skywats", true) == 0)
            {
                // assume tenant-name only, add protocol and skywats domainname
                valid = Uri.TryCreate($"https://{ServiceAddress}.skywats.com", UriKind.Absolute, out address);
            }
            else
            {
                // assume servername only, just add default internal protocol (http)
                valid = Uri.TryCreate($"http://{ServiceAddress}", UriKind.Absolute, out address);
            } 
            // Update address if uri is valid
            if (valid)
            {
                ServiceAddress = address.ToString();
            }
            return valid;
        }

        public static bool SetServerAddress(string serverAddress, string username, string password, ProxySettings proxy)
        {
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: SetServerAddress: {0}, {1}, {2}, *password*", serverAddress, username, password);
            // Register client
            try
            {
                /*
                if (isDirty)
                {
                    if (pxy.ProxySettings != _current.Proxy)
                        //if (_current.ProxyMethod != _original.ProxyMethod || _current.ProxyAddress != _original.ProxyAddress || _current.ProxyUsername != _original.ProxyUsername || _current.ProxyPassword != _original.ProxyPassword)
                        
                    //pxy.LoadSettings();
                }
                */

                if (!serverAddress.EndsWith("/")) 
                    serverAddress += "/"; //Ensure url ends with a /

                //Check/save proxy settings if different
                if (proxy != ViewModel.ViewModelLocator.TDMAPIStatic.ProxySettings)
                    ViewModel.ViewModelLocator.TDMAPIStatic.ProxySettings = proxy;


                //Verify that the WATS Client isn't overwriting another client with the same name but different mac
                if (ViewModel.ViewModelLocator.TDMAPIStatic.HasRegisterClientConflict(serverAddress, username, password))
                {
                    var result = System.Windows.Forms.MessageBox.Show("Another WATS Client with the same computer name already exists. If you have recently changed network adapter or custom identifier, this is expected. Otherwise connecting this WATS Client will disconnect the other.\n\nContinue connecting?", "Register Client", System.Windows.Forms.MessageBoxButtons.YesNo, System.Windows.Forms.MessageBoxIcon.Question);
                    if (result == System.Windows.Forms.DialogResult.No)
                        return false;
                }

                // Must use tdm api (not resthelper) to register client!
                ViewModel.ViewModelLocator.TDMAPIStatic.RegisterClient(serverAddress, username, password);

                System.Windows.Forms.MessageBox.Show("Succesfully registered client", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);
            }
            catch (Virinco.WATS.REST.HttpRequestException e)
            {
                Env.LogException(e, "Unexpected server response during register client");

                switch (e.HttpStatusCode)
                {
                    case System.Net.HttpStatusCode.Unauthorized:
                        System.Windows.Forms.MessageBox.Show("Incorrect username or password.\nUser could not log in to the specified server. ", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
                        break;
                    case System.Net.HttpStatusCode.PaymentRequired: //402, Used when user requires two-factor authentication, which is not supported with basic authentication.
                        System.Windows.Forms.MessageBox.Show("User with Two-factor authentication enabled is not supported. Instead use a RegisterClient token in the password field, with empty username.", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
                        break;
                    case System.Net.HttpStatusCode.Forbidden:
                        System.Windows.Forms.MessageBox.Show("User is not authorized to register client on the specified server.\nContact your system administrator to correct this problem.", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
                        break;
                    case System.Net.HttpStatusCode.NotFound:
                        System.Windows.Forms.MessageBox.Show("Specified server does not exist.\nCheck network connection to the specified address.", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
                        break;
                    case System.Net.HttpStatusCode.Conflict:
                        string reason = e.HttpContent.ReadAsStringAsync().Result.Trim('\"');
                        System.Windows.Forms.MessageBox.Show($"Conflict: {reason}", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
                        break;
                    default:
                        System.Windows.Forms.MessageBox.Show($"Register client failed with {e.Message}", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
                        break;
                }
                return false;
            }
            catch (AggregateException e) //HttpClient throws aggregate exception when network error (unable to establish connection, timeout, connection rejected)
            {
                Env.LogException(e, "Unexpected server response during register client");
                
                var dlgResult = System.Windows.Forms.MessageBox.Show("Specified server could not be reached!\nDo you want to configure this address anyway?\nThe client will continue to ask for valid registration credentials on startup.", "Register Client", System.Windows.Forms.MessageBoxButtons.YesNo, System.Windows.Forms.MessageBoxIcon.Warning);
                if (dlgResult == System.Windows.Forms.DialogResult.Yes)
                {
                    ViewModel.ViewModelLocator.TDMAPIStatic.setTargetUrlUnchecked(serverAddress);
                    return true;
                }
                return false;
            }
            catch (Exception e)
            {
                Env.LogException(e, "Client setup failed");
                System.Windows.Forms.MessageBox.Show($"Failed to register client with specified server\n{e.Message}", "Register Client", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Warning);
                return false;
            }

            return true;
        }      

        private void GenerateCustomIdentifier()
        {
            CustomIdentifier = Guid.NewGuid().ToString();
        }
    }
}
