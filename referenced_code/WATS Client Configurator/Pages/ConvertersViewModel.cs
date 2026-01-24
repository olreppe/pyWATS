using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Reflection;
using System.ServiceProcess;
using System.Threading;
using System.Windows.Forms;
using System.Windows.Input;
using System.Xml.Serialization;
using Virinco.WATS.Client.Configurator.Helpers;
using Virinco.WATS.Configuration;
using Virinco.WATS.Interface.Statistics;

namespace Virinco.WATS.Client.Configurator.Pages
{
    public class ConvertersViewModel : ObservableObject, IPageViewModel_v2
    {
        #region Control properties

        public string Name { get; } = "Converters";

        public bool IsModified
        {
            get { return isModified; }
            set
            {
                if (isModified != value)
                {
                    isModified = value;
                    RaisePropertyChanged("IsModified");
                }
            }
        }

        #endregion

        #region Data properties

        public ConverterItem SelectedConverter
        {
            get { return selectedConverter; }
            set
            {
                if (selectedConverter != value)
                {
                    selectedConverter = value;
                    RaisePropertyChanged("SelectedConverter");
                }
            }
        }

        public ObservableCollection<ConverterItem> Converters { get; } = new ObservableCollection<ConverterItem>();

        #endregion

        #region Commands

        public ICommand AddCommand { get; }

        public ICommand DeleteCommand { get; }

        #endregion

        #region Fields

        private bool isModified;

        private ConverterItem selectedConverter;

        #endregion

        public List<string> InitializeErrorMessages { get; set; } = new List<string>();

        public List<string> FailedConverters { get; set; } = new List<string>();

        private const string replacedAssemblyDirectoryName = "Replaced Assemblies";

        private System.Timers.Timer tmrUpdateStatus;

        private readonly ServiceStatus status;

        public ConvertersViewModel(ConfigViewModel config)
        {
            AddCommand = new RelayCommand(param => AddNewConverterItem());
            DeleteCommand = new RelayCommand(param => DeleteConverter());

            DeleteReplacedConverters();
            LoadConverters();

            //Set WATS Standard Text Format Converter as default selected item
            SelectedConverter = Converters.FirstOrDefault(c => c.Name == "WSTFImporter");
            status = new ServiceStatus();
        }

        public void Initialize()
        {
            tmrUpdateStatus = new System.Timers.Timer(30000);
            tmrUpdateStatus.Elapsed += UpdateConverterStatus;
            tmrUpdateStatus.Start();

            UpdateConverterStatus(null, null);
        }

        public void Uninitialize()
        {
            if (tmrUpdateStatus != null)
            {
                tmrUpdateStatus.Dispose();
                tmrUpdateStatus = null;
            }
        }

        private void LoadConverters()
        {
            converters converters;
            using (var convertersStream = new FileStream(Env.GetConfigFilePath(Env.ConvertersFileName), FileMode.Open, FileAccess.Read))
            {
                converters = (converters)new XmlSerializer(typeof(converters)).Deserialize(convertersStream);
            }

            foreach (var converter in converters.converter)
            {
                var converterItem = new ConverterItem(converter);
                if (!string.IsNullOrEmpty(converterItem.ErrorMessage))
                {
                    InitializeErrorMessages.Add(converterItem.ErrorMessage);
                    converterItem.ErrorMessage = null;
                }

                Converters.Add(converterItem);
            }

            var standardConverters = new List<ConverterItem>
            {
                Converters.FirstOrDefault(c => c.Name == "WSTFImporter"),
                Converters.FirstOrDefault(c => c.Name == "WSXFImporter"),
                Converters.FirstOrDefault(c => c.Name == "WSJFImporter"),
                Converters.FirstOrDefault(c => c.Name == "ATMLImporter")
            };

            foreach (var converter in Converters)
            {
                converter.Deletable = !standardConverters.Contains(converter);
                converter.Editable = converter.Deletable;
                converter.PropertyChanged += ConverterPropertyChanged;
            }
        }

        private void ConverterPropertyChanged(object sender, PropertyChangedEventArgs e)
        {
            if (e.PropertyName == "IsModified")
                IsModified = true;
        }

        private void AddNewConverterItem()
        {
            var converterItem = new ConverterItem
            {
                Name = "(New)",
                Editable = true,
                Deletable = true
            };
            converterItem.PropertyChanged += ConverterPropertyChanged;

            Converters.Add(converterItem);
            IsModified = true;

            SelectedConverter = converterItem;
        }

        public void SaveConverters()
        {
            if (!IsModified)
                return;

            var converters = new converters
            {
                converter = Converters.Select(ci => ci.ToConvertersConverter()).ToArray()
            };

            using (var convertersStream = new FileStream(Env.GetConfigFilePath(Env.ConvertersFileName), FileMode.Truncate, FileAccess.Write))
                new XmlSerializer(typeof(converters)).Serialize(convertersStream, converters);

            CopyNewAssemblies();           
            RestartService();
            ResetConverterStatus();
        }

        private void CopyNewAssemblies()
        {
            var errorMessages = new List<string>();
            string workingFolder = Path.GetDirectoryName(Assembly.GetEntryAssembly().Location);
            string replacedAssemblyFolder = Path.Combine(workingFolder, replacedAssemblyDirectoryName);

            bool didAttemptCreateDirectory = false;

            foreach (var converter in Converters)
            {
                if (!string.IsNullOrEmpty(converter.AssemblyPath) && Path.GetDirectoryName(converter.AssemblyPath) != workingFolder)
                {
                    if (!didAttemptCreateDirectory && !Directory.Exists(replacedAssemblyFolder))
                    {
                        try
                        {
                            Directory.CreateDirectory(replacedAssemblyFolder);
                        }
                        catch (Exception e)
                        {
                            string message = $"Could not copy assemblies: {e.Message}";
                            errorMessages.Add(message + $"\nRestart the Client configurator as Administrator or\nPlace assemblies manually in {workingFolder} and restart the service.");
                            Env.LogException(e, message);
                        }
                        didAttemptCreateDirectory = true;
                    }

                    string fileName = Path.GetFileName(converter.AssemblyPath);
                    string installedFilePath = Path.Combine(workingFolder, fileName);
                    if (File.Exists(installedFilePath))
                    {
                        try
                        {
                            File.Move(installedFilePath, Path.Combine(replacedAssemblyFolder, fileName));
                        }
                        catch { }
                    }

                    try
                    {
                        File.Copy(converter.AssemblyPath, installedFilePath);
                        converter.AssemblyPath = installedFilePath;
                    }
                    catch (Exception e)
                    {
                        string message = $"Failed to copy assembly: {e.Message}";
                        errorMessages.Add(message);
                        Env.LogException(e, message);
                    }
                }

                converter.IsModified = false;
            }
            IsModified = false;

            if (errorMessages.Count > 0)
            {
                string errors = string.Join("\n", errorMessages.ToArray());
                MessageBox.Show(errors, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void RestartService()
        {
            var serviceController = new ClientServiceController().Service;
            if (serviceController != null && serviceController.Status != ServiceControllerStatus.Stopped)
            {
                const string restartQuestion = "The WATS Client Service needs to be restarted before changes take effect. Do you want to restart the service now?";
                bool restartService = MessageBox.Show(restartQuestion, "Restart WATS Client Service", MessageBoxButtons.YesNo, MessageBoxIcon.Question) == DialogResult.Yes;
                if (restartService)
                {
                    ThreadPool.QueueUserWorkItem(new WaitCallback((o) =>
                    {
                        var service = (ServiceController)o;
                        if (service != null)
                        {
                            service.Stop();
                            service.WaitForStatus(ServiceControllerStatus.Stopped);
                            service.Start();
                        }
                    }), serviceController);
                }
            }
        }

        private void DeleteConverter()
        {
            SelectedConverter.PropertyChanged -= ConverterPropertyChanged;
            Converters.Remove(SelectedConverter);
            IsModified = true;
        }

        private void DeleteReplacedConverters()
        {
            var replacedAssemblyFolder = new DirectoryInfo(Path.Combine(Path.GetDirectoryName(Assembly.GetEntryAssembly().Location), replacedAssemblyDirectoryName));
            if (replacedAssemblyFolder.Exists)
            {
                foreach (var replacedAssembly in replacedAssemblyFolder.GetFiles())
                {
                    try
                    {
                        replacedAssembly.Delete();
                    }
                    catch { }
                }
            }
        }

        private void UpdateConverterStatus(object sender, EventArgs e)
        {
            status.UpdateServiceStatus();

            if (status.ConverterStates != null)
            {
                foreach (var kvp in status.ConverterStates)
                {
                    var converter = Converters.SingleOrDefault(c => c.Name == kvp.Key);
                    if (converter != null)
                    {
                        converter.ConverterRunningState = ToFriendlyString(kvp.Value);
                        converter.ShowTroubleshootingLink = kvp.Value == ClientService.ConverterStateEnum.FailedToStart;
                    }
                }
            }

            string ToFriendlyString(ClientService.ConverterStateEnum state)
            {
                switch (state)
                {
                    case ClientService.ConverterStateEnum.FailedToStart:
                        return "Failed to start";
                    case ClientService.ConverterStateEnum.NotStarted:
                        return "Not started";
                    default:
                        return state.ToString();
                }
            }
        }

        private void ResetConverterStatus()
        {
            foreach (var converter in Converters)
            {
                converter.ConverterRunningState = "";
                converter.ShowTroubleshootingLink = false;
            }

            //Reset timer so service has time to start converters
            tmrUpdateStatus.Stop();
            tmrUpdateStatus.Start();
        }
    }
}