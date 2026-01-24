using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.Windows.Data;
using System.Windows;


namespace Virinco.WATS.Client.Configurator.ViewModel
{
    /// <summary>
    /// This class contains properties that a View can data bind to.
    /// </summary>
    public class YieldMonitorViewModel : Interface.Statistics.StatisticsReader
    {
        /// <summary>
        /// Initializes a new instance of the YieldMonitorViewModel class.
        /// </summary>
        public YieldMonitorViewModel()
        {
            base.PropertyChanged += new System.ComponentModel.PropertyChangedEventHandler(YieldMonitorViewModel_PropertyChanged);
        }
        internal YieldMonitorViewModel(TDM_ClientConfig api)
        {
            base.PropertyChanged += new System.ComponentModel.PropertyChangedEventHandler(YieldMonitorViewModel_PropertyChanged);
        }

        void YieldMonitorViewModel_PropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        {
            if (e.PropertyName == "TestYieldLast" || e.PropertyName == "TestYieldTotal")
            {
                base.RaisePropertyChanged("YAxisLowRange");
                if (e.PropertyName == "TestYieldLast")
                {
                    base.RaisePropertyChanged("YieldLevel");
                    base.RaisePropertyChanged("IsWarning");
                    base.RaisePropertyChanged("IsCritical");
                }
            }
        }
        public double YAxisLowRange
        {
            get
            {
                double low = Lowest(TestYieldLast, TestYieldTotal, CurrentProduct.CriticalLevel);
                return Math.Round(low*0.99 - 0.005, 2);
            }
        }

        private double Lowest(params double[] dbls)
        {
            return dbls.Min();
        }
        public Visibility WarningVisibility
        {
            get { return (TestYieldLast < CurrentProduct.WarnLevel)?Visibility.Visible:Visibility.Hidden; }
        }
        public Visibility CriticalVisibilty
        {
            get { return (TestYieldLast < CurrentProduct.CriticalLevel) ? Visibility.Visible : Visibility.Hidden; }
        }
        public enum YieldLevels {none, warning, critical}
        public YieldLevels YieldLevel
        //public string YieldLevel
        {
            get
            {
                double y = TestYieldLast;
                if (UUTReportsInLastStat < CurrentProduct.LastCount) return YieldLevels.none; // No warning until smallcount is reached
                if (y < CurrentProduct.CriticalLevel) return YieldLevels.critical;
                if (y < CurrentProduct.WarnLevel) return YieldLevels.warning;
                return YieldLevels.none;
                /*
                if (y < CurrentProduct.CriticalLevel) return "critical";// YieldLevels.critical;
                if (y < CurrentProduct.WarnLevel) return "warning";//YieldLevels.warning;
                return "none";//YieldLevels.none;
                */
            }
        }
        public System.Windows.Media.Brush BackgroundColor
        {
            get
            {
                return new System.Windows.Media.SolidColorBrush(System.Windows.Media.Color.FromArgb(System.Convert.ToByte(this.Transparency * 255), 255, 255, 255));
            }
        }
    }
    public class MyThicknessConverter : IValueConverter
    {
        #region IValueConverter Members
        public object Convert(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            return new Thickness(5, System.Convert.ToDouble(value), 5, 0);
        }

        public object ConvertBack(object value, Type targetType, object parameter, System.Globalization.CultureInfo culture)
        {
            Thickness thickness = (Thickness)value;
            return thickness.Top;
        }
        #endregion
    }

}