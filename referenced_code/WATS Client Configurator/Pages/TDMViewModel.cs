using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Input;
using Virinco.WATS.Client.Configurator.Helpers;
using Virinco.WATS.Client.Configurator.ViewModel;
using Virinco.WATS.Interface.Statistics;

namespace Virinco.WATS.Client.Configurator.Pages
{
    class TDMViewModel : ObservableObject, IPageViewModel_v2
    {
        public string CurrentIdentifier { get; private set; }

        public string ServiceAPIStatus => status.ServiceAPIStatus;

        public string ServiceStatus => status.ClientServiceStatus;

        public ICommand GenerateCustomIdentifierCommand { get; }

        private readonly ServiceStatus status;

        internal TDMViewModel(ConfigViewModel config)
        {
            this.Config = config;
            status = new ServiceStatus();

            GenerateCustomIdentifierCommand = new RelayCommand(param => GenerateCustomIdentifier());

            status.UpdateServiceStatus();
        }

        public void Initialize()
        {
            Update();
        }

        public void Uninitialize()
        {

        }

        private void Update()
        {
            CurrentIdentifier = REST.ServiceProxy.GetCurrentMACAddress();
            if(string.IsNullOrEmpty(CurrentIdentifier))
                CurrentIdentifier = "No identifier";
            RaisePropertyChanged(nameof(CurrentIdentifier));

            status.UpdateServiceStatus();
            RaisePropertyChanged(nameof(ServiceAPIStatus));
            RaisePropertyChanged(nameof(ServiceStatus));
        }

        private void GenerateCustomIdentifier()
        {
            Config.CustomIdentifier = Guid.NewGuid().ToString();
        }

        public string Name
        {
            get { return "TDM"; }
        }

        public ConfigViewModel Config { get; set; }
    }
}
