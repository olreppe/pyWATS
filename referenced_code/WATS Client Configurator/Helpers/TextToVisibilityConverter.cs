using System.Windows.Data;
using System.Windows;
using System;

namespace Virinco.WATS.Client.Configurator.Helpers
{
    public class TextToVisibilityConverter : IValueConverter
    {
        #region IValueConverter Members

        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            if (parameter == null)
            {
                return Visibility.Visible;
            }
            else if (parameter != null)
            {
                string v = value.ToString();
                string p = parameter.ToString();
                Visibility vi = Visibility.Collapsed;

                if(p.EndsWith("!"))
                    vi = (v.Length != 0) ? Visibility.Visible : Visibility.Collapsed;                
                else
                    vi =  (v.Length==0) ? Visibility.Visible: Visibility.Collapsed;
                return vi;
            }
            return false;
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            throw new NotImplementedException();
        }

        #endregion
    }
}