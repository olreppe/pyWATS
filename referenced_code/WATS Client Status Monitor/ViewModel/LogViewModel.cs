using System;
using System.Windows;
using System.ServiceProcess;
using System.IO;
using System.Xml.Linq;
using System.Linq;
using System.Collections.Generic;

namespace Virinco.WATS.Client.StatusMonitor.ViewModel
{
    /// <summary>
    /// This class contains properties that a View can data bind to.
    /// <para>
    /// Use the <strong>mvvminpc</strong> snippet to add bindable properties to this ViewModel.
    /// </para>
    /// <para>
    /// You can also use Blend to data bind with the tool's support.
    /// </para>
    /// <para>
    /// See http://www.galasoft.ch/mvvm/getstarted
    /// </para>
    /// </summary>
    public class LogViewModel : Interface.Statistics.StatisticsReader
    {
        /// <summary>
        /// Initializes a new instance of the ClientMonitorViewModel class.
        /// </summary>
        internal LogViewModel(TDM_ClientConfig api) : base(api)
        {
            _watsLOGFileName = Env.GetConfigFilePath(Env.WCFConfigFile);
            _convertersFile = Env.GetConfigFilePath(Env.ConvertersFileName);

            this.PropertyChanged += new System.ComponentModel.PropertyChangedEventHandler(LogViewModel_PropertyChanged);
            UpdateConverters();
        }

        private string _watsLOGFileName;
        private string _convertersFile;

        public Uri WatsLOGFileName
        {
            get { return new Uri(_watsLOGFileName); }
        }

        int _exceptionCount = 0;
        public int ExceptionCount
        {
            get { return GetExceptionCount(); }
            set
            {
                if (_exceptionCount != value) { _exceptionCount = value; RaisePropertyChanged("ExceptionCount"); }
            }
        }

        private int GetExceptionCount()
        {
            if (!System.IO.File.Exists(_watsLOGFileName))
            {
                return 0;
            }
            else
            {
                ExceptionCount = System.IO.File.ReadAllLines(_watsLOGFileName).Where(line => line.Contains("Exception {")).Count();  //Count all exceptions in file.
                return _exceptionCount;
            }
        }

        List<string> _converters = new List<string>();
        List<string> _convPaths = new List<string>();

        string _converterOne;
        public string ConverterOne
        {
            get { return GetConverter(1); }
            set
            {
                if (_converterOne != value) { _converterOne = value; base.RaisePropertyChanged("ConverterOne"); }
            }
        }

        string _converterOneCount;
        public string ConverterOneCount
        {
            get { return GetConverterCount(1); }
            set
            {
                if (_converterOneCount != value) { _converterOneCount = value; base.RaisePropertyChanged("ConverterOneCount"); }
            }
        }



        string _converterTwo;
        public string ConverterTwo
        {
            get { return GetConverter(2); }
            set
            {
                if (_converterTwo != value) { _converterTwo = value; base.RaisePropertyChanged("ConverterTwo"); }
            }
        }

        string _converterTwoCount;
        public string ConverterTwoCount
        {
            get { return GetConverterCount(2); }
            set
            {
                if (_converterTwoCount != value) { _converterTwoCount = value; base.RaisePropertyChanged("ConverterTwoCount"); }
            }
        }

        string _converterThree;
        public string ConverterThree
        {
            get { return GetConverter(3); }
            set
            {
                if (_converterThree != value) { _converterThree = value; base.RaisePropertyChanged("ConverterThree"); }
            }
        }

        string _converterThreeCount;
        public string ConverterThreeCount
        {
            get { return GetConverterCount(3); }
            set
            {
                if (_converterThreeCount != value) { _converterThreeCount = value; base.RaisePropertyChanged("ConverterThreeCount"); }
            }
        }

        private string GetConverter(int convNumber)
        {
            if (convNumber <= _converters.Count)
            {
                return _converters[convNumber - 1];
            }
            else
            {
                return "-";
            }
        }


        internal void UpdateConverters()
        {
            try
            {
                XDocument doc = XDocument.Load(_convertersFile);
                _converters = (from el in doc.Root.Elements()
                               select el.Attribute("name").Value).ToList();

                _convPaths = (from el in doc.Root.Descendants()
                              where (string)el.Attribute("name") == "Path"
                              select el.Value).ToList();

                ConverterOne = GetConverter(1);
                ConverterTwo = GetConverter(2);
                ConverterThree = GetConverter(3);

                ConverterOneCount = GetConverterCount(1);
                ConverterTwoCount = GetConverterCount(2);
                ConverterThreeCount = GetConverterCount(3);
            }
            catch (Exception ex)
            {
                throw new Exception(ex.Message);
            }
        }

        private string GetConverterCount(int convNumber)
        {
            if (convNumber <= _convPaths.Count)
            {
                string filepath = _convPaths[convNumber - 1] + "/Error/";

                if (Directory.Exists(filepath))
                {
                    return Directory.GetFiles(filepath).Length.ToString();
                }
            }
            return "-";
        }


        internal void ResetLogFile()
        {
            if (System.IO.File.Exists(_watsLOGFileName))
            {
                System.IO.File.Delete(_watsLOGFileName);
                RaisePropertyChanged("ExceptionCount");
            }
        }

        internal string GetAllExceptions()
        {
            UpdateLogStatus();
            string exString = String.Empty;

            using (System.IO.StreamReader sr = System.IO.File.OpenText(_watsLOGFileName))
            {
                string s = String.Empty;
                bool exFound = false;
                while ((s = sr.ReadLine()) != null)
                {
                    if (exFound)
                    {
                        exString += s + "\r\n";
                        if (s.Contains("}"))
                        {
                            exFound = false;
                            exString += "\r\n\r\n";
                        }
                    }
                    else
                    {
                        if (s.StartsWith(" : Virinco.WATS.Logging.Client Error"))
                        {
                            exFound = true;
                            exString += s + "\r\n";
                        }
                    }
                }

            }
            return exString;
        }

        internal int UpdateLogStatus()
        {

            if (System.IO.File.Exists(_watsLOGFileName))
            {
                return GetExceptionCount();
            }

            return 0;
        }

        void LogViewModel_PropertyChanged(object sender, System.ComponentModel.PropertyChangedEventArgs e)
        {
            UpdateLogStatus();
            UpdateConverters();
        }

        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;

        private void NotifyPropertyChanged(String info)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new System.ComponentModel.PropertyChangedEventArgs(info));
            }
        }


    }
}
