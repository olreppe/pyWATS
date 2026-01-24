using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using Virinco.WATS.Client.Configurator.Helpers;

namespace Virinco.WATS.Client.Configurator.Pages
{
    public class GPSSettingsViewModel : ObservableObject, IPageViewModel
    {
        public string Name
        {
            get { return "Location services"; }
        }

        public string ServiceStatus
        {
            get => status;
            set
            {
                status = value;
                RaisePropertyChanged(nameof(ServiceStatus));
            }
        }

        public bool IsServiceAvailable
        {
            get => isServiceAvailable;
            set
            {
                isServiceAvailable = value;
                RaisePropertyChanged(nameof(IsServiceAvailable));
            }
        }

        public bool IsServiceEnabled
        {
            get => isServiceEnabled;
            set
            {
                isServiceEnabled = value;
                RaisePropertyChanged(nameof(IsServiceEnabled));
                RaisePropertyChanged(nameof(GPSEnabled));
            }
        }

        public bool GPSEnabled
        {
            get => isServiceEnabled && Config.GPSPositionEnabled;
            set
            {
                Config.GPSPositionEnabled = value;

                if (value)
                    UpdateCoordinates();
                else
                    ClearCoordinates();

                SetGPSButtonText();
                RaisePropertyChanged(nameof(GPSEnabled));
            }
        }

        public string Coordinates
        {
            get => Config.GPSPosition;
            set
            {
                Config.GPSPosition = value;
                RaisePropertyChanged(nameof(Coordinates));
            }
        }

        public string GPSButtonText
        {
            get => gpsButtonText;
            set
            {
                gpsButtonText = value;
                RaisePropertyChanged(nameof(GPSButtonText));
            }
        }

        public bool GPSButtonEnabled
        {
            get => gpsButtonEnabled;
            set
            {
                gpsButtonEnabled = value;
                RaisePropertyChanged(nameof(GPSButtonEnabled));
            }
        }

        public ICommand OpenSettingsCommand { get; }

        public ICommand CheckServiceEnabledCommand { get; }

        public ICommand GPSButtonCommand { get; private set; }        

        public ConfigViewModel Config { get; set; }

        private string status = "Not available";
        private string gpsButtonText = "Update";
        private bool isServiceAvailable;
        private bool isServiceEnabled; 
        private bool gpsButtonEnabled;

        internal GPSSettingsViewModel(ConfigViewModel config)
        {
            this.Config = config;
            OpenSettingsCommand = new RelayCommand(o => OpenLocationSettings());
            CheckServiceEnabledCommand = new RelayCommand(o => CheckEnabled());

            SetAvailable();
        }

        private async void SetAvailable()
        {
            IsServiceAvailable = await WindowsLocationService.IsAvailable();
            if (IsServiceAvailable)
                CheckEnabled();
        }

        private async void CheckEnabled()
        {
            IsServiceEnabled = await WindowsLocationService.IsEnabled();
            SetGPSButtonText();
            SetServiceStatus();            
        }

        private void OpenLocationSettings()
        {
            if (IsServiceAvailable)
                WindowsLocationService.OpenLocationSettings();
        }

        private async void UpdateCoordinates()
        {
            try
            {
                var coordinates = (await WindowsLocationService.GetCoordinates()).ToString();
                Coordinates = coordinates;
            }
            catch(Exception e)
            {
                Env.LogException(e, "Failed to update coordinates");
                MessageBox.Show("Failed to update coordinates. See wats.log for more info.", "Update coordinates error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void ClearCoordinates()
        {
            Coordinates = string.Empty;
            SetGPSButtonText();
        }

        private void SetGPSButtonText()
        {
            if (GPSEnabled && IsServiceEnabled)
            {
                GPSButtonText = "Update";
                GPSButtonEnabled = true;
                GPSButtonCommand = new RelayCommand(o => UpdateCoordinates());
                RaisePropertyChanged(nameof(GPSButtonCommand));
            }
            else if (!string.IsNullOrEmpty(Coordinates))
            {
                GPSButtonText = "Clear";
                GPSButtonEnabled = true;
                GPSButtonCommand = new RelayCommand(o => ClearCoordinates());
                RaisePropertyChanged(nameof(GPSButtonCommand));
            }
            else
            {
                GPSButtonText = "Update";
                GPSButtonEnabled = false;
            }
        }

        private void SetServiceStatus()
        {
            if (IsServiceEnabled)
                ServiceStatus = "Enabled";
            else if (IsServiceAvailable)
                ServiceStatus = "Not Enabled";
            else
                ServiceStatus = "Not Available";
        }
    }
}
