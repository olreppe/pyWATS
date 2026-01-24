using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Client.Configurator.ViewModel;

namespace Virinco.WATS.Client.Configurator.Pages
{
    class SWDistViewModel : IPageViewModel
    {
        internal SWDistViewModel(ConfigViewModel config)
        {
            this.Config = config;

        }

        public string Name
        {
            get { return "SWDist"; }
        }

        public ConfigViewModel Config { get; set; }

    }
}
