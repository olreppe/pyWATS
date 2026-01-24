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
using Virinco.WATS.Client.Configurator.View;
using Virinco.WATS.Interface;

namespace Virinco.WATS.Client.Configurator.Pages
{
    /// <summary>
    /// Interaction logic for TDMGeneral.xaml
    /// </summary>
    public partial class TDMView : UserControl
    {
        public TDMView()
        {
            InitializeComponent();
        }

        private void TestConnection(object sender, RoutedEventArgs e)
        {
            ConnectionTest ct = new ConnectionTest(true, true);
            ct.BaseAddress = textBoxServiceAddress.Text;
            ct.ShowDialog();
        }
        private void ConfirmDisconnect(object sender, RoutedEventArgs e)
        {

            var dlg = new ConfirmDisconnect();
            if (dlg.ShowDialog().GetValueOrDefault(false))
            {
                ((TDMViewModel)this.DataContext).Config.DisconnectServer();
            }
        }

        private void CheckboxMesEnabled_Checked(object sender, RoutedEventArgs e)
        {
            // User should not be able to check the enable mes checkbox, but block activation just in case...
            var ver = ViewModel.ViewModelLocator.TDMAPIStatic.ServerVersion;
            if (ver != null && ver < ((TDMViewModel)this.DataContext).Config.MinimumRequiredServerVersionForMES)
            {
                MessageBox.Show($"MES Functions require the server to be at least version {((TDMViewModel)this.DataContext).Config.MinimumRequiredServerVersionForMES}. The server reports version {ver}", "Minimum MES Requirements", MessageBoxButton.OK);
                ((TDMViewModel)this.DataContext).Config.MESActivated = false;
            }
        }
    }
}
