using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace Virinco.WATS.Client.Configurator.Pages
{
    /// <summary>
    /// Interaction logic for General.xaml
    /// </summary>
    public partial class ConvertersView : UserControl
    {
        private int parameterCount = 0;

        public ConvertersView()
        {
            InitializeComponent();
            ((INotifyCollectionChanged)ParameterList.Items).CollectionChanged += ListViewChanged;
            LayoutUpdated += ShowInitializeError;
        }        

        private void Hyperlink_RequestNavigate(object sender, System.Windows.Navigation.RequestNavigateEventArgs e)
        {
            var url = e.Uri.ToString();
            Utilities.OpenUrlInSystemDefaultProgram(url);
        }

        private void ListViewChanged(object sender, EventArgs e)
        {
            int count = ParameterList.Items.Count;

            if (VisualTreeHelper.GetChildrenCount(ParameterList) > 0 && count > parameterCount)
            {
                Border border = (Border)VisualTreeHelper.GetChild(ParameterList, 0);
                ScrollViewer scrollViewer = (ScrollViewer)VisualTreeHelper.GetChild(border, 0);
                scrollViewer.ScrollToBottom();
            }

            parameterCount = count;
        }

        private void ShowInitializeError(object sender, EventArgs e)
        {
            ThreadPool.QueueUserWorkItem(o =>
            {
                var errorMessages = (List<string>)o;
                if (errorMessages.Count > 0)
                {
                    Thread.Sleep(100);
                    MessageBox.Show(string.Join("\n", errorMessages.ToArray()), "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }

                errorMessages.Clear();
            }, ((ConvertersViewModel)DataContext).InitializeErrorMessages);

            LayoutUpdated -= ShowInitializeError;
        }

        private void TextBox_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.Key == Key.Return)            
                ((TextBox)sender).GetBindingExpression(TextBox.TextProperty).UpdateSource();
        }

        private void TabControl_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }

        private void TroubleshootingHelpClick(object sender, RoutedEventArgs e)
        {
            Utilities.OpenUrlInSystemDefaultProgram("https://virinco.zendesk.com/hc/en-us/articles/207425143");
        }
    }
}
