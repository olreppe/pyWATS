using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.IO;
using Virinco.WATS.REST;
using Virinco.WATS.Configuration;

namespace Virinco.WATS.Client.Configurator
{
    internal class TDM_ClientConfig : Interface.TDM
    {
        //new internal Uri GetClientUpdateUri(int timeout) { return base.GetClientUpdateUri(timeout); }

        internal int GetPendingTSConversions()
        {
            string dir = Path.Combine(DataDir, "TSDump");
            if (!Directory.Exists(dir))
                Directory.CreateDirectory(dir);

            DirectoryInfo di = new DirectoryInfo(dir);
            return di.GetFiles().Length;
        }

        internal void setTargetUrlUnchecked(string targetUrl)
        {
            proxy.TargetURL = targetUrl;
            proxy.SaveSettings();
        }

        internal Dictionary<string, string> GetServerInfo(string targetUrl, int timeout = 10000, string token = null)
        {
            return proxy.GetJson<Dictionary<string, string>>("api/internal/Client/ServerInfo", Timeout: timeout, Authorization: token, baseAddress: targetUrl);
        }

        internal int DownloadClientUpdateTimeout => proxy.DownloadClientUpdateTimeout;

        internal Schemas.WRML.WATSReport GetAsWRML(Interface.Report report)
        {
            return base.GetAsWRML(report);
        }

        internal ProxySettings ProxySettings 
        { 
            get => proxy.ProxySettings;
            set => proxy.ProxySettings = value;
        }

        internal string GetClientToken()
        {
            var proxy = new ServiceProxy_ClientConfig();
            proxy.LoadSettings();
            return proxy.GetClientToken();
        }

        internal ServiceProxy Proxy => base.proxy;

        /*
        private bool AutoConfigRemoteServer()
        {
            //TODO: TimeCheck force resync / 
            int certs = -1;
            try { certs = CheckCertificates(); }
            catch (Exception ex) { Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Certificate chain installation failed" }); }
            try { if (certs < 0) certs = Virinco.WATS.Security.Licensing.installDefaultChain(); }
            catch (Exception ex) { Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Certificate chain installation failed" }); }
            int dns = 0;
            try { if (CheckWsdl()) dns = 1; }
            catch (Exception ex) { Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Server wsdl autoconfig: FAILED" }); dns = -1; }
            bool valid = (certs >= 0) && (dns >= 0);
            Status = valid ? APIStatusType.Offline : APIStatusType.Error;
            return valid;
        }
        */
    }

    internal class ServiceProxy_ClientConfig : ServiceProxy
    {
        internal new string GetClientToken() => base.GetClientToken();
    }
}
