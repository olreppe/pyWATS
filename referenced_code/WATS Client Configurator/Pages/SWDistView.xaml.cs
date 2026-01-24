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
using System.IO;

namespace Virinco.WATS.Client.Configurator.Pages
{
    /// <summary>
    /// Interaction logic for MESGeneral.xaml
    /// </summary>
    public partial class SWDistView : UserControl
    {
        public SWDistView()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new System.Windows.Forms.FolderBrowserDialog();            
            if (Directory.Exists(textBoxRootFolder.Text)) 
                dialog.SelectedPath = textBoxRootFolder.Text;

            var result = dialog.ShowDialog();
            if (result == System.Windows.Forms.DialogResult.OK)
            {
                var directory = new DirectoryInfo(dialog.SelectedPath);
                if (!directory.Exists)
                    MessageBox.Show("Folder must exist.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                else if (directory.GetFileSystemInfos().Any())
                    MessageBox.Show("Folder must be empty.", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                else
                    textBoxRootFolder.Text = dialog.SelectedPath;
            }
        }
    }
}
