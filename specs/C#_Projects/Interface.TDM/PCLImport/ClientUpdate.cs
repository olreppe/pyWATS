using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Models.PCLImport
{
    /// <summary>
    /// WATS Client updatefile
    /// </summary>
    public class ClientUpdate
    {
        /// <summary>
        /// Filename
        /// </summary>
        public string Name { get; set; }
        /// <summary>
        /// Version number (3 or 4 part version number)
        /// </summary>
        public string Version { get; set; }
        /// <summary>
        /// Platform, allowed values: x86 or x64 
        /// </summary>
        public string Platform{ get; set; }
    }
}
