using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Interface.Models
{
    public class ModuleVersion
    {
        public string Module { get; set; }

        public string Name { get; set; }

        public string Version { get; set; }
    }
    public class PingBack
    {
        public string ServerName { get; set; }

        public DateTimeOffset? ServerTime { get; set; }
    }
}
