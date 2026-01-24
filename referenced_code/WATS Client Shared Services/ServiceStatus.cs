using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;
using Virinco.WATS.ClientService;

namespace Virinco.WATS.Interface.Statistics
{
    public class ServiceStatus
    {
        public string ClientServiceStatus { get; set; }

        public string ServiceAPIStatus { get; set; }

        public int PendingReports { get; set; }

        public Dictionary<string, ConverterStateEnum> ConverterStates { get; set; }

        public string ServiceStatusFileName { get; } = GetServiceStatusFileName();

        //[Obsolete("Service status handling has been removed from Client API")]
        public void UpdateServiceStatus()
        {
            bool usestatusfileassource = true;
            try
            {
                using (var ctrl = new Virinco.WATS.Configuration.ClientServiceController())
                {
                    if (ctrl.Service != null)
                    {
                        ClientServiceStatus = ctrl.Service.Status.ToString();
                        usestatusfileassource = false;
                    }
                }
            }
            catch (Exception e)
            {
                Env.LogException(e, "UpdateServiceStatus failed to get status of WATSSERVICE");
            } // Don't care (designtime exception??

            try
            {
                XDocument doc = XDocument.Load(ServiceStatusFileName);
                XElement cs = doc.Element("WATS");
                if (cs != null)
                {
                    ServiceAPIStatus = cs.Element("APIStatus").Value;
                    if (usestatusfileassource)
                        ClientServiceStatus = cs.Element("ServiceStatus").Value;

                    // Get pendingcount as a total of wrml+all converters
                    int total = 0;
                    try
                    {
                        int.TryParse(cs.Element("pending").Attribute("total").Value, out total);

                        ConverterStates = new Dictionary<string, ConverterStateEnum>();
                        foreach (var cnv in cs.Element("pending").Elements("converter"))
                        {
                            if (Enum.TryParse(cnv.Attribute("state").Value, out ConverterStateEnum state))
                                ConverterStates.Add(cnv.Attribute("name").Value, state);
                        }
                    }
                    catch { } //don't care... something is wrong with the xml file... assume it will be corrected shortly(!)
                    PendingReports = total;
                }
            }
            catch
            {
                if (usestatusfileassource)
                    ClientServiceStatus = "Service not found";
                ServiceAPIStatus = "Unknown";
            }
        }

        private const string installStatusElementName = "InstallStatus";
        private const string installStatusForVersionAttributeName = "forVersion";

        public static bool SetInstallStatus(InstallStatus installStatus, string forVersion = null)
        {
            try
            {
                string fileName = GetServiceStatusFileName();
                XDocument xDoc;
                if (File.Exists(fileName))
                    xDoc = XDocument.Load(fileName);
                else
                    xDoc = new XDocument(new XElement("WATS"));

                var xInstallStatus = xDoc.Root.Element(installStatusElementName);
                if (xInstallStatus == null)
                {
                    xInstallStatus = new XElement(installStatusElementName);
                    xDoc.Root.Add(xInstallStatus);
                }

                xInstallStatus.Value = installStatus.ToString();

                if (!string.IsNullOrEmpty(forVersion))
                    xInstallStatus.SetAttributeValue(installStatusForVersionAttributeName, forVersion);

                xDoc.Save(fileName);
                return true;
            }
            catch (Exception e)
            {
                Env.LogException(e, "Setting install status failed.");
                return false;
            }
        }

        public static InstallStatus? GetInstallStatus()
        {
            string fileName = GetServiceStatusFileName();
            if (File.Exists(fileName))
            {
                var xDoc = XDocument.Load(fileName);           
                var xInstallStatus = xDoc.Root.Element(installStatusElementName);
                if (xInstallStatus != null)
                {
                    if (Enum.TryParse(xInstallStatus.Value, out InstallStatus installStatus))
                        return installStatus;
                }
            }
            return null;
        }

        public static string GetInstallerUri()
        {
            string fileName = GetServiceStatusFileName();
            if (File.Exists(fileName))
            {
                var xDoc = XDocument.Load(fileName);
                var xInstallStatus = xDoc.Root.Element(installStatusElementName);
                if (xInstallStatus != null)
                {
                    var xForVersion = xInstallStatus.Attribute(installStatusForVersionAttributeName);
                    if (xForVersion != null)
                        return xForVersion.Value;
                }
            }
            return null;
        }

        private static string GetServiceStatusFileName()
        {
            return Env.GetConfigFilePath("ServiceStatus.xml");
        }

        public enum InstallStatus
        {
            Upgraded = 0,
            Pending,
            Cancelled,
            Installing,
            CheckError,
            DownloadError,
            InstallError
        }
    }
}
