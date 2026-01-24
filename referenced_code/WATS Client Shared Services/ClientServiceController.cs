using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Versioning;
using System.ServiceProcess;
using System.Text;

namespace Virinco.WATS.Configuration
{
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    public class ClientServiceController : IDisposable
    {
        private const string WATSServiceName = "WATSSERVICE";

        public ClientServiceController()
        {
            Service = ServiceController.GetServices().FirstOrDefault(ctl => ctl.ServiceName == WATSServiceName);
        }

        public ServiceController Service { get; private set; }

        public ServiceControllerStatus Start(TimeSpan Timeout)
        {
            // Start or continue
            Service.Refresh();
            if (Service.Status == ServiceControllerStatus.Stopped) Service.Start();
            else if (Service.Status == ServiceControllerStatus.Paused) Service.Continue();
            Service.WaitForStatus(ServiceControllerStatus.Running, Timeout);
            Service.Refresh();
            return Service.Status;
        }
        public ServiceControllerStatus Stop(TimeSpan Timeout)
        {
            Service.Refresh();
            if (Service.Status != ServiceControllerStatus.Stopped) Service.Stop();
            Service.WaitForStatus(ServiceControllerStatus.Stopped, Timeout);
            Service.Refresh();
            return Service.Status;
        }
        public ServiceControllerStatus Pause(TimeSpan Timeout)
        {
            Service.Refresh();
            if (Service.Status == ServiceControllerStatus.Running) Service.Pause();
            Service.WaitForStatus(ServiceControllerStatus.Paused, Timeout);
            Service.Refresh();
            return Service.Status;
        }
        
        public void Dispose()
        {
            if (Service != null) Service.Dispose();
        }
    }
}
