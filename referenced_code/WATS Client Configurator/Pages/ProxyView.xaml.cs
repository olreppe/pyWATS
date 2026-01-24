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

namespace Virinco.WATS.Client.Configurator.Pages
{
    /// <summary>
    /// Interaction logic for Proxy.xaml
    /// </summary>
    public partial class ProxyView : UserControl
    {
        public ProxyView()
        {
            InitializeComponent();
        }

        private void textBoxPxyPwd_LostFocus(object sender, RoutedEventArgs e)
        {
            var pbx = sender as PasswordBox;
            if (pbx.Password != "#!DefaultPasswordNotChanged!#")
                ((ProxyViewModel)DataContext).Config.ProxyPassword = pbx.Password;
        }

        private void cbPxyMethod_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }
    }
}
