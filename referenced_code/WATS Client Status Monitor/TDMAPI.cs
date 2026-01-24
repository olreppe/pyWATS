using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.IO;

namespace Virinco.WATS.Client.StatusMonitor
{
    internal class TDM_ClientConfig : Interface.TDM
    {
        internal int GetPendingTSConversions()
        {
            string dir = Path.Combine(DataDir, "TSDump");
            if (!Directory.Exists(dir))
                Directory.CreateDirectory(dir);

            DirectoryInfo di = new DirectoryInfo(dir);
            return di.GetFiles().Length;
        }


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
}
