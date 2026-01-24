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
using System.Windows.Shapes;

namespace Virinco.WATS.Client.Configurator.View
{
    /// <summary>
    /// Interaction logic for ImageBox.xaml
    /// </summary>
    public partial class ImageBox : Window
    {
        public ImageBox(string title, string message, string imageUri)
        {
            InitializeComponent();
            this.Title = title;
            TextBoxMessage.Text = message;
            BitmapImage bitmap = new BitmapImage();
            bitmap.BeginInit();
            bitmap.UriSource = new Uri(imageUri);
            bitmap.EndInit();
            ImageViewer.Source = bitmap;
        }

        

        private void ButtonOK_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}
