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
using System.Windows.Shapes;
using System.Net;
using Virinco.WATS.Client.Configurator.ViewModel;
using System.IO;
using System.ComponentModel;
using Virinco.WATS.Interface.Statistics;

namespace Virinco.WATS.Client.Configurator.View
{
    public partial class Download : Window
    {
        private DownloadViewModel viewModel
        {
            get { return DataContext as DownloadViewModel; }
        }

        private readonly Uri uri;

        public Download(Uri uri)
        {
            InitializeComponent();
            this.uri = uri;

            Loaded += WindowLoaded;
        }

        private async void WindowLoaded(object sender, RoutedEventArgs e)
        {
            viewModel.CleanUp();

            try
            {
                var file = await viewModel.DownloadAsync(uri);

                ServiceStatus.SetInstallStatus(ServiceStatus.InstallStatus.Installing);

                var processStartInfo = new System.Diagnostics.ProcessStartInfo("msiexec.exe", $"/i \"{file.FullName}\" /passive")
                {
                    CreateNoWindow = true
                };

                using (var process = new System.Diagnostics.Process { StartInfo = processStartInfo })                
                    process.Start();                

                DialogResult = true;
            }
            catch (Exception ex)
            {
                string message;
                if (ex is OperationCanceledException)
                {
                    if (viewModel.Cancelled)
                        return;

                    message = "The download has timed out.";
                }
                else
                    message = $"An error occurred while downloading: {ex.Message}";

                Env.LogException(ex, "Download client update exception.");
                ServiceStatus.SetInstallStatus(ServiceStatus.InstallStatus.DownloadError);

                MessageBox.Show(message, "Download error", MessageBoxButton.OK, MessageBoxImage.Error);

                DialogResult = false;
            }

            Close();
        }

        private void Cancel(object sender, RoutedEventArgs e)
        {
            viewModel.Cancel();
            ServiceStatus.SetInstallStatus(ServiceStatus.InstallStatus.Cancelled);

            DialogResult = false;
            Close();
        }

        protected override void OnClosing(CancelEventArgs e)
        {
            base.OnClosing(e);

            viewModel.Cancel();
        }
    }
}
