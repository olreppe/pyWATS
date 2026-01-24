using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using Virinco.WATS.REST;

namespace Virinco.WATS
{
    public static class InstallStatus
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="timeout">Channel's OperationTimeout in milliseconds</param>
        /// <returns></returns>
        public static Uri GetClientUpdateUri(ServiceProxy proxy, int timeout)
        {
            try
            {
                var version = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version;
                string platform = "x64";
                string updateUri = proxy.GetJson<string>($"api/internal/clientupdates/link?version={version}&platform={platform}", timeout);

                if (!string.IsNullOrEmpty(updateUri))
                {
                    var oldUpdateUri = Interface.Statistics.ServiceStatus.GetInstallerUri();
                    if (updateUri == oldUpdateUri)
                    {
                        //if update uri in different from last time, overwrite install error or download error anyway.
                        //need to store old uri somehow
                        var installStatus = Interface.Statistics.ServiceStatus.GetInstallStatus();
                        if (installStatus != Interface.Statistics.ServiceStatus.InstallStatus.InstallError && installStatus != Interface.Statistics.ServiceStatus.InstallStatus.DownloadError)
                            Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.Pending);
                    }
                    else
                    {
                        Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.Pending, updateUri);
                    }

                    return new Uri(updateUri);
                }
                else
                    Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.Upgraded);
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Check for updates failed." });
                Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.CheckError);
            }

            return null;
        }

        public static bool InsertServiceStatus(ServiceProxy proxy, XElement e)
        {
            //Update the install status
            GetClientUpdateUri(proxy, 5000);

            string fileName = Path.Combine(Env.DataDir, "ServiceStatus.xml");
            if (File.Exists(fileName))
            {
                try
                {
                    var status = XDocument.Load(fileName);
                    if (status.Root != null)
                    {
                        foreach (XElement el in status.Root.Elements())
                            e.Add(el);

                        return true;
                    }
                }
                catch { }
            }
            Env.Trace.TraceEvent(TraceEventType.Warning, 0, "Update memberinfo: Failed to read service status.");
            return false;
        }
    }
}
