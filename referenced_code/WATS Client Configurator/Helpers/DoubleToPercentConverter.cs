using System.Windows.Data;
using System.Windows;
using System;

namespace Virinco.WATS.Client.Configurator.Helpers
{
    public class DoubleToPercentConverter : IValueConverter
    {
        #region IValueConverter Members

        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {   
                double v = 0;
                double.TryParse(value.ToString(), out v);
                return v * 100;
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            string v = value.ToString().Trim().Replace("%","");
            double v2 = 0;
            double.TryParse(v, out v2);
            return v2 / 100;
        }

        #endregion
    }
}