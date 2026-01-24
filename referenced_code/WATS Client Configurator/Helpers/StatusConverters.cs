using System.Windows.Data;
using System.Windows;
using System;

namespace Virinco.WATS.Client.Configurator.Helpers
{
    public class StatusToClientDescriptionConverter : IValueConverter
    {
        #region IValueConverter Members

        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            return String.Format("WATS Client: {0}", value);
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotImplementedException();
        }

        #endregion
    }
    /*
    public class StatusToIconConverter : IValueConverter
    {
        #region IValueConverter Members
        
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            switch (value.ToString())
            {

                case "Online": return Properties.Resources.WATSBee; 
                case "Running": return Properties.Resources.WATSBee; 
                case "Offline": return Properties.Resources.WATSBee_normal_offline; 
                case "Error": return Properties.Resources.WATSBee_error; 
                case "Not activated": return Properties.Resources.WATSBee_notactivated; 
                case "Unknown":
                default:
                    return Properties.Resources.WATSBee_unknown;
            }
        }
        
        /-*-
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            System.Drawing.Icon ico;
            //System.Windows.Media.ImageSource src;
            //src=System.Windows.Media.
            switch (value.ToString())
            {

                case "Online": ico = Properties.Resources.WATSBee; break;
                case "Running": ico = Properties.Resources.WATSBee; break;
                case "Offline": ico = Properties.Resources.WATSBee_offline; break;
                case "Error": ico = Properties.Resources.WATSBee_error; break;
                case "Not activated": ico = Properties.Resources.WATSBee_notactivated; break;
                case "Unknown":
                default:
                    ico = Properties.Resources.WATSBee_unknown; break;
            }
            return System.Windows.Interop.Imaging.CreateBitmapSourceFromHIcon(
                ico.Handle,
                Int32Rect.Empty,
                System.Windows.Media.Imaging.BitmapSizeOptions.FromEmptyOptions());
        }
        *-/
        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotImplementedException();
        }

        #endregion
    }
    */
}