using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Windows;
using Virinco.WATS.Client.Configurator.SupportFiles;
using Virinco.WATS.Client.Configurator.ViewModel;
using static Virinco.WATS.Client.Configurator.Pages.LabViewToolkitViewModel;

namespace Virinco.WATS.Client.Configurator.Pages
{
    class TSSupportViewModel : Helpers.ObservableObject, IPageViewModel_v2
    {
        public string Name
        {
            get { return "TestStand"; }
        }

        public ConfigViewModel Config { get; set; }

        public ObservableCollection<Product> Products
        {
            get
            {
                if (_products == null) 
                    _products = new System.Collections.ObjectModel.ObservableCollection<Product>();
                return _products;
            }
            set
            {
                if (_products != value)
                {
                    _products = value;
                    this.RaisePropertyChanged("Products");
                }
            }
        }

        public bool HasDeploymentPackages 
        {
            get => _hasDeploymentPackages;
            set
            {
                _hasDeploymentPackages = value;
                RaisePropertyChanged(nameof(HasDeploymentPackages));
            }
        }


        private ObservableCollection<Product> _products;
        private bool _hasDeploymentPackages;

        internal TSSupportViewModel(ConfigViewModel config)
        {
            this.Config = config;
        }


        public void Initialize()
        {
            try
            {
                var products = Deploy.GetDeploymentConfigurations(true);
                Products = new ObservableCollection<Product>(products.Where(p => p.IsTSInstalled));
                HasDeploymentPackages = products.Any(p => p.IsDeploymentPackage);
            }
            catch (Exception e)
            {
                Env.LogException(e, "Failed to load TestStand configurations");
                MessageBox.Show(e.Message, "Failed to load TestStand configurations", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        public void Uninitialize()
        {
            
        }
    }
}
