using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace Virinco.WATS.Client.Configurator.Pages
{
    /// <summary>
    /// Interaction logic for General.xaml
    /// </summary>
    public partial class SetupView : UserControl
    {
        public SetupView()
        {
            InitializeComponent();
            serviceAddressTextbox.PreviewMouseLeftButtonDown += TextBoxServiceAddress_PreviewMouseLeftButtonDown;
        }

        private void TextBoxServiceAddress_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            //Remove?

            //if (serviceAddressTextbox.Foreground == Brushes.Black)
            //    return;
            //// textBoxServiceAddress.Text = "";
            //serviceAddressTextbox.Foreground = Brushes.Black;
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            // Set cbType based on existing serviceaddress
            string svcAdr = ((SetupViewModel)this.DataContext).Config?.ServiceAddress;
        }
    }
}
