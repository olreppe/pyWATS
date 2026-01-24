using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Client.Configurator.ViewModel;

namespace Virinco.WATS.Client.Configurator.Pages
{
    class ApiViewModel : IPageViewModel
    {
        internal ApiViewModel(ConfigViewModel config)
        {
            this.Config = config;

        }

        public string Name
        {
            get { return "Api"; }
        }

        public ConfigViewModel Config { get; set; }

    }
}
