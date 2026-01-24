using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Client.Configurator.ViewModel
{
    public class About
    {
        public About()
        {
            this.TestStation = Utilities.GetMSIVersionString(System.Reflection.Assembly.GetExecutingAssembly().GetName().Version);
            this.CoreVersion = Utilities.GetMSIVersionString(System.Reflection.Assembly.GetAssembly(typeof(Env)).GetName().Version);
            TDM_ClientConfig api = new TDM_ClientConfig();
            this.ServiceUptime = DateTime.Now.Subtract(api.Statistics.Started);
            Microsoft.Win32.RegistryKey wkey=Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS");
            /*
            this.LicenseCompany = wkey.GetValue("UserName");
            this.LicenseCompany = wkey.GetValue("UserName");
            this.LicenseCompany = wkey.GetValue("UserName");*/
        }
        public string TestStation { get; private set; }
        public string CoreVersion { get; private set; }
        public TimeSpan ServiceUptime { get; private set; }
        public string LicenseUser { get; private set; }
        public string LicenseCompany { get; private set; }
        public string LicenseKey { get; private set; }
    }
}
