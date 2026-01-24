using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Client.Configurator.ViewModel;

namespace Virinco.WATS.Client.Configurator.Pages
{
    class GeneralViewModel : Helpers.ObservableObject, IPageViewModel
    {
        internal GeneralViewModel(ConfigViewModel config)
        {
            this.Config = config;
            //this.Config.PropertyChanged += Config_PropertyChanged; //bubble through...

        }
        
        //private void Config_PropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        //{
        //    if (ReferenceEquals(null, e.PropertyName))
        //        RaisePropertyChanged(e.PropertyName);
        //    else if (System.ComponentModel.TypeDescriptor.GetProperties(this)[e.PropertyName] != null)
        //        RaisePropertyChanged(e.PropertyName);
        //}

        public string Name
        {
            get { return "General"; }
        }

        public ConfigViewModel Config { get; set; }
        /*
        internal string MachineName { get { return config.MachineName; } }
        internal string Location { get { return config.Location; } set { config.Location = value;  } }
        internal string Purpose { get { return config.Purpose; } set { config.Purpose = value; } }
        internal string GPSPosition { get { return config.GPSPosition; } set { config.GPSPosition = value; } }
        */
    }
}
