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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Virinco.WATS.Client.PackageManager
{
    public partial class CaptionButtons : UserControl
    {
        public BitmapImage CloseSource 
        {
            get => (BitmapImage)GetValue(CloseSourceProperty);
            set => SetValue(CloseSourceProperty, value);
        }

        public BitmapImage MaximizeSource
        {
            get => (BitmapImage)GetValue(MaximizeSourceProperty);
            set => SetValue(MaximizeSourceProperty, value);
        }

        public BitmapImage MinimizeSource
        {
            get => (BitmapImage)GetValue(MinimizeSourceProperty);
            set => SetValue(MinimizeSourceProperty, value);
        }

        public Visibility CloseVisibility
        {
            get => (Visibility)GetValue(MinimizeSourceProperty);
            set => SetValue(MinimizeSourceProperty, value);
        }

        public Visibility MaximizeVisibility
        {
            get => (Visibility)GetValue(MinimizeSourceProperty);
            set => SetValue(MinimizeSourceProperty, value);
        }

        public Visibility MinimizeVisibility
        {
            get => (Visibility)GetValue(MinimizeSourceProperty);
            set => SetValue(MinimizeSourceProperty, value);
        }

        public static readonly DependencyProperty CloseSourceProperty = DependencyProperty.Register(nameof(CloseSource), typeof(BitmapImage), typeof(CaptionButtons));

        public static readonly DependencyProperty MaximizeSourceProperty = DependencyProperty.Register(nameof(MaximizeSource), typeof(BitmapImage), typeof(CaptionButtons));

        public static readonly DependencyProperty MinimizeSourceProperty = DependencyProperty.Register(nameof(MinimizeSource), typeof(BitmapImage), typeof(CaptionButtons));

        public static readonly DependencyProperty CloseVisibilityProperty = DependencyProperty.Register(nameof(CloseVisibility), typeof(Visibility), typeof(CaptionButtons));

        public static readonly DependencyProperty MaximizeVisibilityProperty = DependencyProperty.Register(nameof(MaximizeVisibility), typeof(Visibility), typeof(CaptionButtons));
        
        public static readonly DependencyProperty MinimizeVisibilityProperty = DependencyProperty.Register(nameof(MinimizeVisibility), typeof(Visibility), typeof(CaptionButtons));
                
        public CaptionButtons()
        {
            InitializeComponent();
            root.DataContext = this;
        }

        private void Close(object sender, RoutedEventArgs e)
        {
            Window.GetWindow(this).Close();
        }

        private void Maximize(object sender, RoutedEventArgs e)
        {
            var window = Window.GetWindow(this);
            if (window.WindowState == WindowState.Maximized)            
                window.WindowState = WindowState.Normal;            
            else            
                window.WindowState = WindowState.Maximized;            
        }


        private void Minimize(object sender, RoutedEventArgs e)
        {
            Window.GetWindow(this).WindowState = WindowState.Minimized;
        }
    }
}
