using System;
using System.Collections.Generic;
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
using System.Windows.Shapes;

namespace Virinco.WATS.Client.PackageManager
{
    /// <summary>
    /// Interaction logic for Configuration.xaml
    /// </summary>
    public partial class Configuration : Window
    {
        private ConfigurationViewModel viewModel => DataContext as ConfigurationViewModel;

        public Configuration()
        {
            InitializeComponent();
        }

        private void Cancel(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();            
        }

        private void Exit(object sender, RoutedEventArgs e)
        {
            viewModel.SaveConfiguration();
            DialogResult = true;
            Close();
        }
    }
}
