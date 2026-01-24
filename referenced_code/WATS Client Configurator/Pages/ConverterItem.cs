using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Windows;
using System.Windows.Input;
using Virinco.WATS.Client.Configurator.Helpers;

namespace Virinco.WATS.Client.Configurator.Pages
{
    public class ConverterItem : ObservableObject
    {
        #region Control properties

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

        public bool Editable { get; set; }

        public bool Deletable { get; set; }

        #endregion

        #region Data properties

        public string Name
        {
            get { return converterName; }
            set
            {
                converterName = value;
                OnPropertyChanged("Name");
                IsModified = true;
            }
        }

        public string AssemblyName
        {
            get { return assemblyName; }
            set
            {         
                assemblyName = value;
                OnPropertyChanged("AssemblyName");

                if (!isSetByFindFunction)
                {
                    AssemblyPath = Path.Combine(Path.GetDirectoryName(Assembly.GetEntryAssembly().Location), $"{value}.dll");
                    UpdateClasses();
                }

                IsModified = true;
            }
        }

        public string Class
        {
            get { return className; }
            set
            {
                className = value;
                OnPropertyChanged("Class");

                LoadParameters();

                IsModified = true;
            }
        }

        public string AssemblyVersion 
        { 
            get => assemblyVersion;
            set
            {
                assemblyVersion = value;
                RaisePropertyChanged(nameof(AssemblyVersion));
            }
        }

        public string InputPath
        {
            get { return inputPath; }
            set
            {
                inputPath = value;
                OnPropertyChanged("InputPath");
                IsModified = true;
            }
        }

        public string Filter
        {
            get { return inputFilter; }
            set
            {
                inputFilter = value;
                OnPropertyChanged("Filter");
                IsModified = true;
            }
        }

        public string PostProcessAction
        {
            get { return postProcessAction; }
            set
            {
                postProcessAction = value;
                OnPropertyChanged("PostProcessAction");
                IsModified = true;
            }
        }

        public string ConverterRunningState
        {
            get { return converterRunningState; }
            set
            {
                converterRunningState = value;
                OnPropertyChanged(nameof(ConverterRunningState));
            }
        }

        public bool ShowTroubleshootingLink
        {
            get { return showTroubleshootingLink; }
            set
            {
                showTroubleshootingLink = value;
                OnPropertyChanged(nameof(ShowTroubleshootingLink));
            }
        }

        public ObservableCollection<ConverterParameter> Parameters { get; } = new ObservableCollection<ConverterParameter>();

        public ObservableCollection<string> Classes { get; } = new ObservableCollection<string>();

        #endregion

        #region Fields

        private bool isModified;

        private string converterName;
        private string assemblyName;
        private string className;
        private string assemblyVersion;
        private string inputPath;
        private string inputFilter;
        private string postProcessAction;
        private string converterRunningState;
        private bool showTroubleshootingLink;

        private bool isSetByFindFunction = false;

        #endregion

        #region Commands

        public ICommand FindAssemblyCommand { get; }

        public ICommand FindPathCommand { get; }

        public ICommand AddParameterCommand { get; }

        public ICommand RemoveParameterCommand { get; }

        #endregion

        #region Constants

        private const string pathParameterName = "Path";
        private const string filterParameterName = "Filter";
        private const string postProcessActionParameterName = "PostProcessAction";
        private const string postProcessActionMove = "Move";
        private const string postProcessActionZip = "Zip";
        private const string postProcessActionDelete = "Delete";
        private const string sourceType = "folder";
        private const string destinationType = "api";

        #endregion

        public string AssemblyPath { get; set; }

        public string ErrorMessage { get; set; }

        public string[] PostProcessActions { get; } = new[] { postProcessActionMove, postProcessActionZip, postProcessActionDelete };

        public ConverterItem()
        {
            FindAssemblyCommand = new RelayCommand(param => FindAssembly());
            FindPathCommand = new RelayCommand(param => FindPath());
            AddParameterCommand = new RelayCommand(param => AddParameter(new ConverterParameter()));
            RemoveParameterCommand = new RelayCommand(param => RemoveParameter((ConverterParameter)param));
        }

        public ConverterItem(convertersConverter converter) : this()
        {
            Name = converter.name;
            AssemblyName = converter.assembly;
            Class = converter.@class;

            if (converter.Source?.Parameter != null)
            {
                InputPath = converter.Source.Parameter.FirstOrDefault(p => p.name == pathParameterName)?.Value;
                Filter = converter.Source.Parameter.FirstOrDefault(p => p.name == filterParameterName)?.Value;
                PostProcessAction = converter.Source.Parameter.FirstOrDefault(p => p.name == postProcessActionParameterName)?.Value;
            }

            if (converter.Destination?.Parameter != null)
            {
                foreach (var parameter in converter.Destination.Parameter)
                {
                    var existingParameter = Parameters.FirstOrDefault(p => p.Name == parameter.name);
                    if(existingParameter != null)
                        existingParameter.Value = parameter.Value;
                    else
                        AddParameter(new ConverterParameter { Name = parameter.name, Value = parameter.Value });
                }
            }

            IsModified = false;
        }

        public convertersConverter ToConvertersConverter()
        {
            return new convertersConverter
            {
                name = Name,
                assembly = AssemblyName,
                @class = Class,
                Source = new ParametersCollection
                {
                    type = sourceType,
                    Parameter = new[]
                    {
                        new ParametersCollectionParameter { name = pathParameterName, Value = InputPath, },
                        new ParametersCollectionParameter { name = filterParameterName, Value = Filter, },
                        new ParametersCollectionParameter { name = postProcessActionParameterName, Value = PostProcessAction, }
                    }
                },
                Destination = new ParametersCollection
                {
                    type = destinationType,
                    Parameter = Parameters.Select(p => new ParametersCollectionParameter { name = p.Name, Value = p.Value }).ToArray()
                }
            };
        }

        private void FindAssembly()
        {
            Microsoft.Win32.OpenFileDialog openFileDialog = new Microsoft.Win32.OpenFileDialog
            {
                Filter = "Assembly files (*.dll)|*.dll",
                CheckFileExists = true,
                CheckPathExists = true,
                ValidateNames = true
            };

            if (openFileDialog.ShowDialog() == true)
            {
                isSetByFindFunction = true;
                AssemblyName = Path.GetFileNameWithoutExtension(openFileDialog.FileName);
                isSetByFindFunction = false;

                AssemblyPath = openFileDialog.FileName;
                UpdateClasses();
            }
        }

        private void UpdateClasses()
        {
            if (AssemblyExists())
            {
                try
                {
                    var assembly = Assembly.LoadFile(AssemblyPath);
                    AssemblyVersion = $"v {assembly.GetName().Version}";

                    var converterType = typeof(Interface.IReportConverter);

                    Classes.Clear();
                    foreach (var type in assembly.GetTypes())
                    {
                        if (converterType.IsAssignableFrom(type)) //gets too  many answers, should be Is Implemented ?
                            Classes.Add(type.FullName);
                    }
                }
                catch (Exception e)
                {
                    MessageBox.Show("Could not load classes. This is usually because the DLL is blocked by Windows. Open it's properties and under General check the Unblock option. See the WATS Client troubleshooting article for more.", "No classes, DLL blocked?", MessageBoxButton.OK, MessageBoxImage.Warning);
                    Env.LogException(e, "Failed to load class list");
                }
            }
        }

        private void LoadParameters()
        {
            if (AssemblyExists() && !string.IsNullOrEmpty(Class))
            {
                try
                {
                    var converterClass = Assembly.LoadFile(AssemblyPath)?.GetType(Class, false, true);
                    if (converterClass != null && typeof(Interface.IReportConverter_v2).IsAssignableFrom(converterClass) && converterClass.GetConstructor(Type.EmptyTypes) != null)
                    {
                        var converterParameters = ((Interface.IReportConverter_v2)Activator.CreateInstance(converterClass)).ConverterParameters;
                        if (converterParameters != null)
                        {
                            foreach (var parameter in converterParameters)
                            {
                                if(!Parameters.Any(p => p.Name == parameter.Key))
                                    AddParameter(new ConverterParameter { Name = parameter.Key, Value = parameter.Value });
                            }
                        }
                    }
                }
                catch (Exception e)
                {
                    Env.LogException(e, "Failed to load default converter parameters");
                }           
            }
        }

        private void FindPath()
        {
            var folderBrowserDialog = new System.Windows.Forms.FolderBrowserDialog
            {
                Description = "Browse to folder for converter input files",
                //RootFolder = Environment.SpecialFolder.CommonApplicationData,
                ShowNewFolderButton = true,
                SelectedPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData), Path.Combine("Virinco", "WATS"))
            };

            if (folderBrowserDialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                InputPath = folderBrowserDialog.SelectedPath;
        }

        private void AddParameter(ConverterParameter parameter)
        {
            parameter.PropertyChanged += ParameterPropertyChanged;

            Parameters.Add(parameter);
            IsModified = true;            
        }

        private void RemoveParameter(ConverterParameter parameter)
        {
            parameter.PropertyChanged -= ParameterPropertyChanged;

            Parameters.Remove(parameter);
            IsModified = true;
        }

        private void ParameterPropertyChanged(object sender, PropertyChangedEventArgs e)
        {
            IsModified = true;
        }

        private bool AssemblyExists()
        {
            bool exists = File.Exists(AssemblyPath);
            if (!exists)            
                ErrorMessage = $"Could not find assembly {AssemblyName}";
            
            return exists;
        }
    }

    public class ConverterParameter : ObservableObject
    {
        public string Name
        {
            get { return name; }
            set
            {
                name = value;
                OnPropertyChanged("Name");
            }
        }

        public string Value
        {
            get { return value; }
            set
            {
                this.value = value;
                OnPropertyChanged("Value");
            }
        }

        private string name;
        private string value;
    }
}
