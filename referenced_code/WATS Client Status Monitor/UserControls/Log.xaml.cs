using System;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace Virinco.WATS.Client.StatusMonitor.UserControls
{
    /// <summary>
    /// Interaction logic for Log.xaml
    /// </summary>
    public partial class Log : UserControl
    {
        public Log()
        {
            InitializeComponent();

            //this.IsVisibleChanged += Log_IsVisibleChanged;
            vm = DataContext as ViewModel.LogViewModel;
            this.Loaded += Log_Loaded;
        }

        /// <summary>
        /// Each time it is loaded again from the menu. 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Log_Loaded(object sender, RoutedEventArgs e)
        {

            if (vm != null)
            {
               int exCount = vm.UpdateLogStatus();
                ActivateLOGLink(exCount);

                vm.UpdateConverters();
            }
        }

        ViewModel.LogViewModel vm;

        private void Hyperlink_RequestNavigate(object sender, System.Windows.Navigation.RequestNavigateEventArgs e)
        {
            var url = e.Uri.ToString();
            Utilities.OpenUrlInSystemDefaultProgram(url);
        }

        /// <summary>
        /// Delete wats log file. 
        /// Update status. 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void resetButton_Click(object sender, RoutedEventArgs e)
        {
            if (vm != null)
            {
                vm.ResetLogFile();
            }
        }

        /// <summary>
        /// Goes through the log file and parses out the exceptions. 
        /// Shows a message box with them. 
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void showExButton_Click(object sender, RoutedEventArgs e)
        {
            if (vm != null)
            {
                string exString = vm.GetAllExceptions();
                MessageBox.Show(exString, "Info", MessageBoxButton.OK);
            }

        }      
       
        /// <summary>
        /// Activate or deactivate LOG link and exception button and count. 
        /// Checks the count, if 0, everything disables and the color is gray. 
        /// If more than one, everything enables and the color is blue. 
        /// </summary>
        /// <param name="exceptionCount">Count of all exceptions in current wats.log.</param>
        private void ActivateLOGLink(int exceptionCount)
        {
            if (exceptionCount == 0)
            {
                buttonShowEx.IsEnabled = false;
                labelHyperlink.IsEnabled = false;
                buttonResetStatus.IsEnabled = false;
                labelHyperlink.Foreground = Brushes.Gray;
            }
            else
            {
                buttonShowEx.IsEnabled = true;
                labelHyperlink.IsEnabled = true;
                buttonResetStatus.IsEnabled = true;
                labelHyperlink.Foreground = Brushes.Blue;
            }          

        }
    }
}
