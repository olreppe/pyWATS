using System;
using System.Collections.Generic;
using System.Linq;
using System.ServiceProcess;
using System.Windows;

namespace Virinco.WATS.Client.StatusMonitor
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private void Application_Startup(object sender, StartupEventArgs e)
        {
            try
            {
                //Env.Trace.TraceEvent(TraceEventType.Information, 0, "Starting WATS Client Log Monitor [v.{0}] starting @{1:o} ", System.Reflection.Assembly.GetExecutingAssembly().GetName().Version, DateTime.Now); 
                this._wStatus = new View.ClientMonitor();
                this._wStatus.Show();
                this._wStatus.Closing += new System.ComponentModel.CancelEventHandler(_wStatus_Closing);
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Critical, 0, new WATSLogItem() { ex = ex, Message = "Failed to initialize status monitor." });
                throw;
            }
        }

        private View.ClientMonitor _wStatus;

        void _wStatus_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _wStatus = null;
            this.Shutdown();
        }
    }
}
