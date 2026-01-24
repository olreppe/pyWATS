using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.InteropServices;
using System.ServiceProcess;
using System.Windows;
using System.Windows.Threading;
using Virinco.WATS.Interface;
using Virinco.WATS.Interface.Statistics;

namespace Virinco.WATS.Client.Configurator
{
    /// <summary>
    /// Configurator state enumeration, actual state is kept in ConfigViewModel (locator::Config)
    /// </summary>

    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private void Application_Startup(object sender, StartupEventArgs e)
        {
            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {
                var assemblyName = new AssemblyName(args.Name);
                var pkt = assemblyName.GetPublicKeyToken();

                var ourAssembly = typeof(TDM).Assembly;
                var ourAssemblyName = new AssemblyName(ourAssembly.FullName);
                var ourPkt = ourAssemblyName.GetPublicKeyToken();

                if (pkt != null && pkt.SequenceEqual(ourPkt))
                    return ourAssembly;

                //Public key token for WATS-Core.snk is 40e2cae0ae7be54b
                var watscorePkt = new byte[] { 0x40, 0xe2, 0xca, 0xe0, 0xae, 0x7b, 0xe5, 0x4b };
                if (pkt != null && pkt.SequenceEqual(watscorePkt))
                {
                    // Try to load the actual WATS-Core type forwarding assembly
                    string installDirectory = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
                    return Assembly.LoadFrom(Path.Combine(installDirectory, "Virinco.WATS.WATS-Core.dll"));
                }

                return null;
            };

            Env.Trace.TraceEvent(TraceEventType.Information, 0, "Starting WATS Client Config [v.{0}] starting @{1:o} ", System.Reflection.Assembly.GetExecutingAssembly().GetName().Version, DateTime.Now);
            CLUtil.ArgumentParser args;
            try { args = new CLUtil.ArgumentParser("WATSClient", e.Args); }
            catch (Exception ex) { Env.LogException(ex, "error during ArgumentParsing"); throw ex; }
            try { Virinco.WATS.Client.Configurator.SupportFiles.Deploy.ValidateConfiguration(args); } //should include check of connection string, username/password !
            catch (Exception ex) { Env.LogException(ex, "error during config validation"); throw ex; }
            //List<string> args = new List<string>(e.Args);
            bool startConfiguratorWindow = true;
            //these keys, installed|redeploy|uninstalling|reconfigure|updateclient should they be in Configurator?
            if (args.Options.ContainsKey("installed"))
            {
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Completing WATS Client installation");
                //string msg = "Initial install configuration done...";
                string msg = string.Empty;
                // Redeploy support files for all installed TS and LV instances....
                ConfigViewModel.RedeployAllFromBackup();
                ConfigViewModel.UpdateLabviewToolkits();
                //Logging start...
                ConfigViewModel.CompleteInstallation();

                // Retry tsdumps:
                ConfigViewModel.RetryTSErrorFiles();
                ConfigViewModel.RetryInvalidFiles();

                // Try-start service...
                try
                {
                    using (var svc = new Configuration.ClientServiceController())
                    {
                        // try to start service for up to 30 sec. before ending in warning message
                        for (int i = 0; i < 6; i++)
                        {
                            try
                            {
                                var timeout = TimeSpan.FromMilliseconds(5000);
                                var res = svc.Start(timeout);
                                if (res == ServiceControllerStatus.Running) break;
                            }
                            catch { System.Threading.Thread.Sleep(500); }
                        }
                        if (svc.Service.Status != ServiceControllerStatus.Running)
                            msg = String.Format("Failed to start Service, restart computer and check that WATS Client Service is running.\nCurrent Service status: {0}", svc.Service.Status);
                    }
                }
                catch (Exception ex) { msg = String.Format("An unhandled exception occurred while trying to start Service, restart computer and check that WATS Client Service is running.\nException: {0}", ex.Message); }
                //Logging end...

                try
                {
                    string trayExePath = Path.Combine("C:\\Program Files\\Virinco\\WATS", "WATSTray.exe");
                    if (Process.GetProcessesByName("WATSTray").Length == 0)
                    {
                        Process.Start(new ProcessStartInfo
                        {
                            FileName = trayExePath,
                            UseShellExecute = true,
                            Arguments = string.Empty,
                            WorkingDirectory = "C:\\Program Files\\Virinco\\WATS"
                        });
                    }
                }
                catch (Exception ex)
                {
                    Env.LogException(ex, "Could not start WATSTray after installation.");
                }

                if (msg != string.Empty)
                    System.Windows.Forms.MessageBox.Show(msg);

                startConfiguratorWindow = false;
            }
            else if (args.Options.ContainsKey("uninstalling"))
            {
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Completing WATS Client uninstall");
                ConfigViewModel.CompleteUnInstallation();
                startConfiguratorWindow = false;
            }
            else if (args.Options.ContainsKey("reconfigure"))
            {
                Env.Trace.TraceEvent(TraceEventType.Error, 0, "Configurator /reconfigure parameter is no longer supported in 5.0 client, exiting without doing anything");
                startConfiguratorWindow = false;
            }
            else if (args.Options.ContainsKey("updateclient"))
            {
                UpdateClient();
                startConfiguratorWindow = false;

                try
                {
                    string trayExePath = Path.Combine("C:\\Program Files\\Virinco\\WATS", "WATSTray.exe");
                    if (Process.GetProcessesByName("WATSTray").Length == 0)
                    {
                        Process.Start(new ProcessStartInfo
                        {
                            FileName = trayExePath,
                            UseShellExecute = true,
                            Arguments = string.Empty,
                            WorkingDirectory = "C:\\Program Files\\Virinco\\WATS"
                        });
                    }
                }
                catch (Exception ex) { Env.LogException(ex, "Could not start WATSTray"); }
            }

            //If automated update started installer, but /installed was not run, set install status to error
            try
            {
                if (ServiceStatus.GetInstallStatus() == ServiceStatus.InstallStatus.Installing)
                    ServiceStatus.SetInstallStatus(ServiceStatus.InstallStatus.InstallError);
            }
            catch (Exception ex)
            {
                Env.LogException(ex, "Check for install error failed.");
            }

            if (startConfiguratorWindow)
            {
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Starting WATS Configurator (application)");

                try
                {
                    ViewModel.ViewModelLocator.TDMAPIStatic.ConnectServer(true, TimeSpan.FromMilliseconds(5000));
                }
                catch
                {
                    Env.Trace.TraceEvent(TraceEventType.Error, 0, "ConnectServer failed to load process");
                }

                try
                {
                    _wConfig = new View.Configure();
                    _wConfig.Show();
                    _wConfig.Closing += new System.ComponentModel.CancelEventHandler(_wConfig_Closing);
                }
                catch (Exception ex)
                {
                    Env.LogException(ex, "Failed to start Configurator window.");
                    throw ex;
                }
            }
            else
            {
                Shutdown();
            }
        }

        private void UpdateClient()
        {
            Uri updateUri = InstallStatus.GetClientUpdateUri(ViewModel.ViewModelLocator.TDMAPIStatic.Proxy, 5000);
            if (updateUri != null)
            {
                //const string question = "A new version of the WATS Client is available. Would you like to install it now?";
                //const string title = "Update client";
                //if (MessageBox.Show(question, title, MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes)
                //{
                    var downloadView = new View.Download(updateUri);
                    bool? result = downloadView.ShowDialog();
                //}
            }
        }

        void Application_DispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs args)
        {
            Env.LogException(args.Exception, "An unexpected application exception occurred");

            MessageBox.Show(
                "An unexpected exception has occurred. Shutting down the application. Please check the log file for more details and contact support.",
                "WATS Client Configurator crash",
                MessageBoxButton.OK,
                MessageBoxImage.Error
            );

            // Prevent default unhandled exception processing
            args.Handled = true;

            Environment.Exit(0);
        }

        //removed showNotifyIconBaloon
        //removed wYieldMonitor
        //removed wStatus

        private View.Configure _wConfig;

        internal View.Configure wConfig
        {
            get
            {
                if (this._wConfig == null)
                {
                    this._wConfig = new View.Configure();
                    _wConfig.Closing += new System.ComponentModel.CancelEventHandler(_wConfig_Closing);
                }
                return _wConfig;
            }
        }

        private void _wConfig_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            _wConfig = null;
            this.Shutdown();
        }

        //is this needed in configurator? (or anywhere?)
        [DllImport("kernel32.dll")]
        private static extern bool AttachConsole(int dwProcessId);

        private const int ATTACH_PARENT_PROCESS = -1;

        internal void StartElevatedReconfigure()
        {
            try { StartElevatedProcess("/reconfigure", true); }
            catch (Exception e)
            {
                // Log exception, and display warning message.
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = "Start elevated reconfigure/autoconfig failed." });
                MessageBox.Show("Failed to start autoconfigure as elevated process\nElevated process is required to make the requested changes.", "Autoconfigure failed", System.Windows.MessageBoxButton.OK, System.Windows.MessageBoxImage.Error);
            }
        }

        internal void StartNewProcess(string arguments, bool WaitForExit, bool elevated)
        {
            // runs with the same arguments plus flag mentioning the main action performing
            var info = new ProcessStartInfo(System.Reflection.Assembly.GetEntryAssembly().Location, arguments);
            if (elevated) info.Verb = "runas";
            info.UseShellExecute = false;
            var process = new Process { EnableRaisingEvents = WaitForExit, StartInfo = info };
            process.Start();
            if (WaitForExit) process.WaitForExit();
        }

        internal void StartElevatedProcess(string arguments, bool WaitForExit)
        {
            StartNewProcess(arguments, WaitForExit, (Environment.OSVersion.Version.Major >= 6));
        }
    }
}