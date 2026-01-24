using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WATS_Client_Service_DebugApp
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        protected internal enum ServiceStateEnum { Unknown, Stopped, Starting, Started, Pausing, Paused, Resuming, Stopping, Failed, Error }
        protected internal ServiceStateEnum svcstate;
        private Service_debugger svc;
        private void SetStatus(ServiceStateEnum serviceStateEnum)
        {
            svcstate = serviceStateEnum;
            txtStatus.Text = svcstate.ToString();
            txtAPIStatus.Text = svc?.APIStatus;
            switch (svcstate)
            {
                case ServiceStateEnum.Started: btnStart.IsEnabled = false; btnStop.IsEnabled = true; btnPause.IsEnabled = true; break;
                case ServiceStateEnum.Stopped: btnStart.IsEnabled = true; btnStop.IsEnabled = false; btnPause.IsEnabled = false; break;
                case ServiceStateEnum.Paused: btnStart.IsEnabled = true; btnStop.IsEnabled = true; btnPause.IsEnabled = false; break;
                default:
                    btnStart.IsEnabled = false; btnStop.IsEnabled = false; btnPause.IsEnabled = false; break;
            }
        }

        private void btnStart_Click(object sender, RoutedEventArgs e)
        {
            if (svcstate == ServiceStateEnum.Paused)
            {
                SetStatus(ServiceStateEnum.Resuming);
                if (svc == null) svc = new Service_debugger();
                svc.Continue();
                SetStatus(ServiceStateEnum.Started);
            }
            else
            {
                SetStatus(ServiceStateEnum.Starting);
                if (svc == null) svc = new Service_debugger();
                svc.Start();
                SetStatus(ServiceStateEnum.Started);
            }
        }

        private void btnStop_Click(object sender, RoutedEventArgs e)
        {
            SetStatus(ServiceStateEnum.Stopping);
            if (svc == null) svc = new Service_debugger();
            svc.Stop();
            SetStatus(ServiceStateEnum.Stopped);
        }

        private void btnPause_Click(object sender, RoutedEventArgs e)
        {
            SetStatus(ServiceStateEnum.Pausing);
            if (svc == null) svc = new Service_debugger();
            svc.Pause();
            SetStatus(ServiceStateEnum.Paused);
        }

        private void BtnRefresh_Click(object sender, RoutedEventArgs e)
        {
            SetStatus(svcstate);
        }
    }
    internal class Service_debugger : Virinco.WATS.ClientService.ClientSvc
    {
        internal void Start()
        {
            base.OnStart(new string[]{});            
        }

        internal void Pause()
        {
            base.OnPause();
        }
        internal void Continue()
        {
            base.OnContinue();
        }

        internal void Stop()
        {
            base.OnStop();
        }
    }
}
