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
    /// Interaction logic for TDMGeneral.xaml
    /// </summary>
    public partial class ApiView : UserControl
    {
        public ApiView()
        {
            InitializeComponent();
            
        }

        /// <summary>
        /// Only works if file path exists, there has to be a better way of doing this
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void Link_Click(object sender, RoutedEventArgs e)
        {
            var filepath = System.IO.Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), @"Virinco\WATS\WATS Client API Documentation.pdf");
            bool fileExists = File.Exists(filepath) ? true : false;

            if(fileExists)
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
