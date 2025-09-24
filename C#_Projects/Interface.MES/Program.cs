using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using Virinco.WATS.Interface.MES.Production;

namespace Virinco.WATS.Interface.MES
{
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            //Application.Run(new TestGUI());
           // Virinco.WATS.Interface.MES.MES mes = new Virinco.WATS.Interface.MES.MES();
            //bool s = false;
            //mes.Production.IdentifyUUT(out s);
          //  Production.Production p = mes.Production;
          //  UnitInfo ui = p.GetUnitInfo("095271103129");
        }
    }
}
