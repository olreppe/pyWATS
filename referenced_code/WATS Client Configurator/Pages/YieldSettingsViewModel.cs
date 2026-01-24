using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Client.Configurator.ViewModel;

namespace Virinco.WATS.Client.Configurator.Pages
{
    class YieldSettingsViewModel : IPageViewModel
    {
        internal YieldSettingsViewModel(ConfigViewModel config)
        {
            this.Config = config;

        }

        public string Name
        {
            get { return "YieldSettings"; }
        }

        public ConfigViewModel Config { get; set; }

    }
}
