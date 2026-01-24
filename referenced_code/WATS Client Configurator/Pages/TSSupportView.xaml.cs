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
using Virinco.WATS.Client.Configurator.SupportFiles;

namespace Virinco.WATS.Client.Configurator.Pages
{
    /// <summary>
    /// Interaction logic for TDM_TSSupport.xaml
    /// </summary>
    public partial class TSSupportView : UserControl
    {
        public TSSupportView()
        {
            InitializeComponent();
        }
        private void btnUninstall_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.Controls.Button btn = sender as System.Windows.Controls.Button;
            if (btn != null)
            {
                Product p = btn.DataContext as Product;
                if (p != null)
                {
                    try
                    {
                        p.UnDeployFiles();
                    }
                    catch (Exception ex)
                    {
                        Env.LogException(ex, $"Failed to uninstall WATS Support for {p.Name}");
                        MessageBox.Show($"Failed to uninstall WATS Support for {p.Name}", "Uninstall supportfiles", MessageBoxButton.OK);
                    }
                }
            }
        }

        private void btnInstall_Click(object sender, RoutedEventArgs e)
        {
            System.Windows.Controls.Button btn = sender as System.Windows.Controls.Button;
            if (btn != null)
            {
                Product p = btn.DataContext as Product;
                if (p != null)
                {
                    if (ConfirmAppClosed(p.Name))
                    {
                        try
                        {
                            p.DeployFiles(false, false);
                        }
                        catch (Exception ex)
                        {
                            Env.LogException(ex, $"Failed to install WATS Support for {p.Name}");
                            MessageBox.Show($"Failed to install WATS Support for {p.Name}", "Install supportfiles", MessageBoxButton.OK);
                        }
                    }
                }
            }
        }

        private bool ConfirmAppClosed(string p)
        {
            return MessageBox.Show(String.Format("Ensure that {0} is closed.", p), "Confirm Application Closed", MessageBoxButton.OKCancel) == MessageBoxResult.OK;
        }

        private void ListView_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }
    }
}
