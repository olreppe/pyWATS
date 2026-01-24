using System;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Forms;
using Virinco.WATS.REST;

namespace Virinco.WATS.Client.StatusMonitor.View
{
    /// <summary>
    /// Interaction logic for Config.xaml
    /// </summary>
    public partial class ClientMonitor : Window
    {
        public ClientMonitor()
        {
            InitializeComponent();
        }

        private void Hyperlink_RequestNavigate(object sender, System.Windows.Navigation.RequestNavigateEventArgs e)
        {
            var url = e.Uri.ToString();
            Utilities.OpenUrlInSystemDefaultProgram(url);
        }


        private void GenerateSupportLog_Click(object s, RoutedEventArgs e)
        {
            ViewModel.ClientMonitorViewModel vm = DataContext as ViewModel.ClientMonitorViewModel;
            if (vm != null)
            {
                var selectZipPath = new SaveFileDialog
                {
                    AddExtension = true,
                    CheckPathExists = true,
                    DefaultExt = ".zip",
                    FileName = "WATS Support Log",
                    OverwritePrompt = true,
                    Title = "Save WATS Support log",
                    ValidateNames = true
                };

                if(selectZipPath.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                    System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(state => vm.GenerateSupportLog(selectZipPath.FileName)));
            }
        }

        private void EnableVerboseLogging_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var proxy = new ServiceProxy();
                proxy.LoadSettings();

                if(!proxy.LoggingSettings.Overridden)
                    proxy.LoggingSettings.OverriddenLoggingLevel = proxy.LoggingSettings.LoggingLevel;

                proxy.LoggingSettings.Overridden = true;
                proxy.LoggingSettings.OverrideExpiresDate = DateTimeOffset.UtcNow.AddDays(1);
                proxy.LoggingSettings.LoggingLevel = System.Diagnostics.SourceLevels.All;

                proxy.SaveSettings();

                using (var ctrl = new Configuration.ClientServiceController())
                    ctrl.Service.ExecuteCommand((int)ClientService.WATSServiceCustomCommand.ReloadConfig);

                System.Windows.MessageBox.Show("Verbose logging enabled for 24 hours.", "Logging", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                string message = "Failed to enable verbose logging";
                System.Windows.MessageBox.Show(message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                Env.LogException(ex, message);
            }

            Env.InitializeLogging();
        }

        private void About_Click(object sender, RoutedEventArgs e)
        {
            var about = new About();
            about.ShowDialog();
        }
    }
}
