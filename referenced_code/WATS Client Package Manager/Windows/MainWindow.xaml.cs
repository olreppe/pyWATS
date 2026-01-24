using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Windows.Threading;
using System.Xml.Linq;
using System.IO;
using System.Diagnostics;

namespace Virinco.WATS.Client.PackageManager
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private MainViewModel viewModel => DataContext as MainViewModel;

        private bool forceExit = false;

        public MainWindow()
        {
            Initialized += (s, e) => WindowIntialized();
            InitializeComponent();

            Closing += (s, e) =>
            {
                Hide();
                if (!forceExit)
                    e.Cancel = true;                
            };

            StateChanged += (s, e) =>
            {
                if (WindowState == WindowState.Minimized)
                    Visibility = Visibility.Collapsed;
            };
        }       

        private async void WindowIntialized()
        {
            viewModel.StartTimer();
            viewModel.PackagesUpdated += (s, e) =>
            {
                if (Utils.BringToFront && viewModel.AvailablePackages.Count() > 0 && viewModel.TotalSize.HasValue && viewModel.TotalSize.Value > 0)
                {
                    viewModel.SelectedTab = 0;
                    BrintToFront();
                }
            };

            await viewModel.CheckForPackages();
        }

        private void BrintToFront()
        {
            Show();
            if (WindowState != WindowState.Maximized)
                WindowState = WindowState.Normal;
            Activate();
        }

        protected override void OnClosing(CancelEventArgs e)
        {
            var processes = Process.GetProcessesByName("Virinco.WATS.Client.PackageManager").ToList();

            if (processes.Count > 1)
            {
                Process originalProcess = null;

                foreach (var process in processes)
                {
                    if (originalProcess == null)
                    {
                        originalProcess = process;
                        continue;
                    }
                    else if (process.StartTime < originalProcess.StartTime)
                    {
                        originalProcess.Kill();
                        originalProcess.WaitForExit();
                        originalProcess = null;
                        originalProcess = process;
                    }
                }
                var currentProcess = Process.GetCurrentProcess();

                if (!currentProcess.Equals(originalProcess))
                {
                    Environment.Exit(0);
                }
            }
            base.OnClosing(e);
        }

        private void Exit(object sender, RoutedEventArgs e)
        {
            forceExit = true;
            Close();
        }

        

        private async void OpenConfiguration(object sender, RoutedEventArgs e)
        {
            Configuration cfg = new Configuration();
            bool refresh = cfg.ShowDialog() ?? false;

            await viewModel.StopTimer();
            viewModel.StartTimer();

            if(refresh)
                await viewModel.CheckForPackages();
        }

        private void OpenHelp(object sender, RoutedEventArgs e)
        {
            Help hlp = new Help();
            hlp.ShowDialog();
        }

        private async void Refresh(object sender, RoutedEventArgs e)
        {
            await viewModel.CheckForPackages();
        }

        private async void InstallPackages(object sender, RoutedEventArgs e)
        {
            await viewModel.InstallPackages();
        }

        /// <summary>
        /// Star width columns in DataGrid do not shrink when other content get bigger. 
        /// Set star width columns to 0 width, update layout, then put width configuration back.
        /// </summary>
        private void UpdateDataGridLayout(object sender, DataTransferEventArgs e)
        {            
            // TODO DataGrid is no longer supported. Use DataGridView instead. For more details see https://docs.microsoft.com/en-us/dotnet/core/compatibility/winforms#removed-controls
            var dataGrid = (DataGrid)sender;
            var starSizedColumns = dataGrid.Columns.Where(c => c.Width.IsStar).ToDictionary(c => c, c => c.Width.Value);
            foreach (var column in starSizedColumns)
                column.Key.Width = 0;

            dataGrid.UpdateLayout();

            foreach (var column in starSizedColumns)
                column.Key.Width = new DataGridLength(column.Value, DataGridLengthUnitType.Star);
        }
    }
}

/* 
 
select * from Software.Package
where Tags.exist( '//*[PartNumber[.="5555000055"] or PartNumber[.="5555000066"]]  [StationName[.="main-source.wats.no" or .="Any"]]' ) = 0x1

where Tags.exist( '//*[StationName[.="main-source.wats.nso" or .="LDCT2-P1C"] or Misc[.="misc" or .="misc2"]] ' ) = 0x1

 */
