using System;
using System.Collections.Generic;
using System.IO;
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
    /// Interaction logic for General.xaml
    /// </summary>
    public partial class GeneralView : UserControl
    {
        public GeneralView()
        {
            InitializeComponent();
        }
        private void Hyperlink_RequestNavigate(object sender, System.Windows.Navigation.RequestNavigateEventArgs e)
        {
            var url = e.Uri.ToString();
            Utilities.OpenUrlInSystemDefaultProgram(url);
        }

        private void OpenGeneralOptions_Click(object sender, RoutedEventArgs e)
        {
            var filepath = Env.GetConfigFilePath(Env.GeneralSettingsFileName);
            bool fileExists = File.Exists(filepath) ? true : false;

            if (fileExists)
            {
                Utilities.OpenFileInSystemDefaultProgram(filepath);
            }
            else
            {
                FailMessage.Visibility = Visibility.Visible;
            }
        }
    }
}
