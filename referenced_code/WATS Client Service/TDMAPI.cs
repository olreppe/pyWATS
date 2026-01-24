using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Interface;
using System.IO;
using System.Net;
using System.Diagnostics;
using Virinco.WATS.REST;
using System.Xml.Linq;
using System.Xml.Serialization;
using Virinco.WATS.Schemas.WRML;
using static Virinco.WATS.Interface.Statistics.ServiceStatus;

namespace Virinco.WATS.ClientService
{
    internal class TDM_ClientService : Interface.TDM
    {
        /// <summary>
        /// Forced recheck of server status
        /// </summary>
        /// <returns>True if server is online, otherwise false</returns>
        internal bool CheckRemoteServer()
        {
            return IsConnectedToServer(false);
        }

        new internal bool Ping() {return base.Ping(); }


        /// <summary>
        /// Checks all files in ReportsDirectory marked as "transfering", resets to Saved if not accessed the last 30 minutes.
        /// </summary>
        internal void CheckTransferingTimeout()
        {
            // Allow transfering status for 30 minutes before retrying
            string searchPattern = "*." + Report.ReportTransferStatusEnum.Transfering.ToString();
            DateTime now = DateTime.Now;
            TimeSpan TransferTimeout = new TimeSpan(0, 30, 0);
            foreach (FileInfo f in
                (from f in (new DirectoryInfo(ReportsDirectory)).GetFiles(searchPattern, SearchOption.TopDirectoryOnly)
                 where f.LastAccessTime.Add(TransferTimeout) < now
                 select f))
            {
                string fname = Path.GetFileNameWithoutExtension(f.FullName);
                f.MoveTo(Path.Combine(f.DirectoryName, fname + "." + Report.ReportTransferStatusEnum.Queued.ToString()));
            }
            // Allow error status for 5 minutes before retrying
            searchPattern = "*." + Report.ReportTransferStatusEnum.Error.ToString();
            TransferTimeout = new TimeSpan(0, 5, 0);
            foreach (FileInfo f in
                (from f in (new DirectoryInfo(ReportsDirectory)).GetFiles(searchPattern, SearchOption.TopDirectoryOnly)
                 where f.LastAccessTime.Add(TransferTimeout) < now
                 select f))
            {
                string fname = Path.GetFileNameWithoutExtension(f.FullName);
                f.MoveTo(Path.Combine(f.DirectoryName, fname + "." + Report.ReportTransferStatusEnum.Queued.ToString()));
            }
        }

        internal new void PostClientLog() => base.PostClientLog();

        internal new bool SubmitFromFile(SubmitMethod submitMethod, FileInfo file)
        {
            return base.SubmitFromFile(submitMethod, file);
        }

        internal new ServiceProxy proxy => base.proxy;
    }
}
