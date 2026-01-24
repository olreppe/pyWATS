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
using Virinco.WATS.Client.Configurator.ViewModel;

namespace Virinco.WATS.Client.Configurator.Pages
{
    /// <summary>
    /// Interaction logic for TDM_LVSupport.xaml
    /// </summary>
    public partial class LabViewToolkitView : UserControl
    {
        public LabViewToolkitView()
        {
            InitializeComponent();
        }

        //LabViewToolkitViewModel ViewModel
        //{
        //    get { return (LabViewToolkitViewModel)this.DataContext; }
        //}
        
        private void btnInstall_Click(object sender, RoutedEventArgs e)
        {
         //ViewModel.SelectedLabView.DeployFiles();

         ((LabViewToolkitViewModel.LabView)((Button)sender).DataContext).DeployFiles();
        }

        private void btnUninstall_Click(object sender, RoutedEventArgs e)
        {
            ((LabViewToolkitViewModel.LabView)((Button)sender).DataContext).UnDeployFiles();
        }
    }
}
