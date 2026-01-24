using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS.Interface.MES.Production
{
    internal class UnitStateHistory
    {
        public string[] processes { get; set; }

        public string[] phases { get; set; }

        public DateTime[] dateTimes { get; set; }
    }
}
