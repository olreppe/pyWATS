using System.IO;
using System.Reflection;
using System.Windows;

namespace Virinco.WATS.Client.StatusMonitor.View
{
    /// <summary>
    /// Interaction logic for About.xaml
    /// </summary>
    public partial class About : Window
    {
        public About()
        {
            InitializeComponent();
            Loaded += About_Loaded;
        }

        private void About_Loaded(object sender, RoutedEventArgs e)
        {
            string path = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "ABOUT.txt");
            textBox.Text = File.ReadAllText(path);
        }
    }
}
