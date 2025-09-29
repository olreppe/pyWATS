using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.IO;
using System.Configuration;

namespace Virinco.WATS
{
    /// <summary>
    /// 
    /// </summary>
    public static class Env
    {
        const string eventSource = "WATS";
        const string dataDirKey = "DataDir";
        const string installDirKey = "InstallDir";
        const string memberIdKey = "MemberID";
        const string stationNameKey = "StationName";
        const string locationKey = "Location";
        const string purposeKey = "Purpose";
        const string operatorNameKey = "Operator";
        const string compressionEnabledKey = "CompressionEnabled";
        const string WCFConfigFileKey = "WCFConfigFile";
        const string TDMEndPointKey = "TDMEndpoint";
        const string MESEndPointKey = "MESEndpoint";
        const string MESEndPointNameKey = "MESEndpointName";
        const string ClientFunctionKey = "ClientFunction";
        const string ClientLicenseKey = "LicenseType";
        const string EndpointCertificateName = "TDMEndpointCertificateName";
        const string SoftwareDistributionRootKey = "MESSoftwareDistributionRoot";
        const string FileTransferChunkSizeKey = "FileTransferChunkSize";
        const string LogExceptionsKey = "LogExceptions";
        const string LoggingLevelKey = "LoggingLevel";
        const string LogFileSizeTruncateToKey = "LogFileTruncateTo";
        const string LogFileSizeMaximumKey = "LogFileMaxSize";

        private static Dictionary<string, string> _volatileReg;
        private static Dictionary<string, string> volreg { get { if (_volatileReg == null) _volatileReg = new Dictionary<string, string>(); return _volatileReg; } }
        /// <summary>
        /// Clears all non-persisted Env-values.
        /// </summary>
        public static void Reset()
        {
            _volatileReg = new Dictionary<string, string>();
        }
        /// <summary>
        /// Indicating if Env class persists values to registry, or keeps them in memory
        /// </summary>
        public static bool PersistValues = true;

        /// <summary>
        /// Starts to collect trace information to eventlog (API debug purpose)
        /// </summary>
        public static void StartTraceToEventLog()
        {
            Trace.Listeners.Add(new EventLogTraceListener(eventSource));
        }

        /// <summary>
        /// Stop trace information to eventlog (stop API debug)
        /// </summary>
        public static void StopTraceToEventLog()
        {
            //Remove last listener
            if (Trace.Listeners.Count > 0)
                Trace.Listeners.Remove(Trace.Listeners[Trace.Listeners.Count - 1]);
        }

        private static string constructExceptionMessage(string message, Exception ex)
        {
            if (ex != null)
            {
                message += "\r\nExeption message: " + ex.Message + "\r\nSource:\r\n" + ex.Source + "\r\nStack trace:\r\n" + ex.StackTrace + "\r\n";
                if (ex.InnerException != null)
                    message += constructExceptionMessage(message, ex.InnerException);
            }
            return message;
        }

        public static void LogException(Exception e, string userMessage)
        {
            //if (LogExceptions) 
            Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = userMessage });
            //{
            //    string errormessage = constructExceptionMessage(userMessage, e);
            //    EventLog.WriteEntry(eventSource, errormessage, EventLogEntryType.Error);
            //}
            LastException = e;
            if (RethrowException)
                throw new ApplicationException(userMessage + ": " + e.Message);
        }

        public static void LogException(Exception e, string userMessage, string operatorMessage)
        {
            LogException(e, userMessage);
            System.Windows.Forms.MessageBox.Show(operatorMessage, "An error occurred", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
        }

        /// <summary>
        /// Property to set if any Exception should be thrown
        /// </summary>
        public static bool RethrowException { get; set; }


        private static bool? _logexceptions;
        /// <summary>
        /// Property to set if any Exception should be written to eventlog
        /// </summary>
        public static bool LogExceptions //{ get; set; }
        {
            get
            {
                if (_logexceptions.HasValue) return _logexceptions.Value;
                else
                {
                    bool logex;
                    if (Boolean.TryParse(getValue(LogExceptionsKey), out logex)) _logexceptions = logex;
                    else _logexceptions = false; // Default value if unparsable...
                    return _logexceptions.Value;

                }
            }
            set { _logexceptions = value; }
        }

        private static TraceSource _tracesource = null;
        public static TraceSource Trace { get { if (_tracesource == null) InitializeLogging(); return _tracesource; } }

        private static SourceLevels? _logging;
        private static RollingTextWriterTraceListener _watslog;
        private static WATSDatabaseTraceListener _dblogger;

        public static void InitializeLogging()
        {
            //SourceLevels level;
            //if (!Utilities.EnumTryParse<SourceLevels>(getValue(LoggingLevelKey), out level)) level = SourceLevels.Error;
            SourceLevels level = LoggingLevel;

            if (!_logging.HasValue || _logging.Value != level) // Check if firsttime or level changed...
            {
                if (_watslog != null) /* remove existing listeners */
                {
                    if (System.Diagnostics.Debug.Listeners.Contains(_watslog)) System.Diagnostics.Debug.Listeners.Remove(_watslog);
                    if (System.Diagnostics.Trace.Listeners.Contains(_watslog)) System.Diagnostics.Trace.Listeners.Remove(_watslog);
                }

                if (_tracesource == null)
                {
                    _tracesource = new TraceSource("Virinco.WATS.Logging.Client");
                    _tracesource.Switch.Level = SourceLevels.ActivityTracing | SourceLevels.Verbose;
                    //_tracesource.Listeners.Add(new TextWriterTraceListener(Path.Combine(DataDir, "wats.log")) { Filter = new EventTypeFilter(level) });
                }
                // Create "default logger" (rolling log spcified in registry)
                _watslog = level == SourceLevels.Off ? null : new RollingTextWriterTraceListener(Path.Combine(DataDir, "wats.log")) { Filter = new EventTypeFilter(level) };

                if (_watslog != null)
                {
                    _tracesource.Listeners.Add(_watslog);
                    System.Diagnostics.Trace.Listeners.Add(_watslog);
                    System.Diagnostics.Trace.AutoFlush = true;
                }

                // Create "database logger" if WATS Connectionstring exists
                _dblogger = level == SourceLevels.Off ? null : WATSDatabaseTraceListener.Create(new EventTypeFilter(level));// { Filter = new EventTypeFilter(level) };
                if (_dblogger != null)
                {
                    _tracesource.Listeners.Add(_dblogger);
                    System.Diagnostics.Trace.Listeners.Add(_dblogger);
                }

                _logging = level;
            }

        }
        //public static SourceLevels LoggingLevel
        //{
        //    get { if (!_logging.HasValue) InitializeLogging(); return _logging.Value; }
        //    set { setValue(LoggingLevelKey, value.ToString()); }
        //}
        public static SourceLevels LoggingLevel
        {
            get
            {
                //string level = getValue(LoggingLevelKey);
                SourceLevels level;
                if (!Enum.TryParse<SourceLevels>(getValue(LoggingLevelKey), out level)) level = SourceLevels.Error | SourceLevels.ActivityTracing;
                return level;
            }
            set { setValue(LoggingLevelKey, value.ToString()); InitializeLogging(); }
        }



        private static Exception _lastException;
        /// <summary>
        /// Property to retrive the last Exception thrown
        /// </summary>
        public static Exception LastException
        {
            get
            {
                Exception tmp = _lastException;
                _lastException = null;
                return tmp;
            }
            set
            {
                _lastException = value;
            }
        }



        public static void LogMessageToEventLog(string message, EventLogEntryType type)
        {
            try //catch full event
            {
                System.Diagnostics.EventLog.WriteEntry(eventSource, message, type);
            }
            catch (Exception e)
            {
                throw new ApplicationException("Cannot write to eventlog", e);
            }
        }

        internal static string getValue(string key, string defaultValue = null)
        {
            if (PersistValues) return GetWATSRegistryValue(key, defaultValue);
            else
            {
                if (volreg.ContainsKey(key)) return volreg[key];
                else
                {
                    string val = GetWATSRegistryValue(key, defaultValue);
                    volreg[key] = val;
                    return val;
                }
            }
        }


        internal static void setValue(string key, string value)
        {
            if (PersistValues) SetWATSRegistryValue(key, value);
            else
            {
                if (volreg.ContainsKey(key)) volreg[key] = value;
                else volreg.Add(key, value);
            }
        }

        /// <summary>
        /// Guid identifying Station
        /// </summary>
        /// <remarks>Automatically generated and saved on workstation on first time connection</remarks>
        [Obsolete("MemberId should not be depended on. Starting from WATS Version 5.0 the client is identified by primary network adapter's MAC Address.", false)]
        public static Guid MemberId
        {
            get
            {
                return Guid.Empty;
                /*
                Guid id = Guid.Empty;
                try { id = GetWATSRegistryGuidValue(memberIdKey); }
                catch { }

                if (id == Guid.Empty) // Generate a new GUID and save in registry
                {
                    id = Guid.NewGuid();
                    SetWATSRegistryValue(memberIdKey, id);
                }
                return id;
                */
            }
        }



        /// <summary>
        /// Disk location for storage of pending reports, WCF config and other
        /// </summary>
        public static string DataDir
        {
            get
            {
                string dataDir = getValue(dataDirKey);// GetWATSRegistryValue(dataDirKey);
                if (string.IsNullOrEmpty(dataDir))
                {
                    dataDir = Path.Combine(
                        System.Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),
                        @"Virinco\WATS\");
                    setValue(dataDirKey, dataDir);
                }
                return dataDir;
            }
            set
            {
                try
                {
                    if (!Directory.Exists(value))
                        Directory.CreateDirectory(value);
                    setValue(dataDirKey, value);
                }
                catch (Exception ex)
                {
                    ApplicationException nex = new ApplicationException("Error setting DataDir (creating directory '" + value + "')", ex);
                    LogException(nex, "Prop1 Env.DataDir");
                    throw nex;
                }
            }
        }







        /// <summary>
        /// WATS Installation root
        /// </summary>
        public static string InstallDir
        {
            get { return getValue(installDirKey); }
            set { setValue(installDirKey, value); }
        }


        public static void SetApplicationEventLogToOverwriteAsNeeded()
        {
            Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Eventlog\Application", true);
            if (key != null)
            {
                key.SetValue("Retention", 0);
            }
            key.Close();
        }


        /// <summary>
        /// Name of test machine
        /// </summary>
        public static string StationName
        {
            get { return Environment.MachineName; }
        }

        /// <summary>
        /// Purpose of test machine
        /// </summary>
        public static string Purpose
        {
            get { return getValue(purposeKey); }
            set { setValue(purposeKey, value); }
        }

        /// <summary>
        /// Test station location
        /// </summary>
        public static string Location
        {
            get { return getValue(locationKey); }
            set { setValue(locationKey, value); }
        }

        /// <summary>
        /// Operator Name
        /// </summary>
        public static string Operator
        {
            get { return getValue(operatorNameKey); }
            set { setValue(operatorNameKey, value); }
        }

        /// <summary>
        /// File name for WCF Configuration 
        /// </summary>
        public static string WCFConfigFile
        {
            get
            {
                string path = getValue(WCFConfigFileKey);
                if (string.IsNullOrEmpty(path))
                {
                    path = Path.Combine(DataDir, "WATS_WCF.config");
                    setValue(WCFConfigFileKey, path);
                }
                return path;
            }
            set { setValue(WCFConfigFileKey, value); }
        }

        /// <summary>
        /// Full Path to WCF Configuration File - depreciated
        /// </summary>
        /// <remarks>DEPRECEATED, use WCFConfigFile instead. This property getter wil be removed in a forthcoming release!</remarks>
        public static string WCFConfigFileFullName
        {
            get { return getValue(WCFConfigFileKey); }
        }

        /// <summary>
        /// Default Endpoint for TDM
        /// </summary>
        [Obsolete("No longer in use", false)]
        public static string TDMEndpoint
        {
            get
            {
                string ep = getValue(TDMEndPointKey);
                if (string.IsNullOrEmpty(ep)) return "TDM-Default";
                else return ep;
            }
            set { setValue(TDMEndPointKey, value); }
        }

        /// <summary>
        /// Default endpoint name for MES
        /// </summary>
        [Obsolete("No longer in use", false)]
        public static string MESEndpointName
        {
            get
            {
                string ep = getValue(MESEndPointNameKey);
                if (string.IsNullOrEmpty(ep)) return "MES-Default";
                else return ep;
            }
            set { setValue(MESEndPointNameKey, value); }
        }
        /// <summary>
        /// Default endpoint name for Old MES (0.9.x)
        /// </summary>
        [Obsolete("No longer in use", false)]
        public static string MESEndpoint
        {
            get
            {
                string ep = getValue(MESEndPointKey);
                if (string.IsNullOrEmpty(ep)) return "MES-Default";
                else return ep;
            }
            set { setValue(MESEndPointKey, value); }
        }

        /// <summary>
        /// Returns the WATS Client Type
        /// </summary>
        public static ClientFunctions ClientFunction
        {
            get
            {
                try
                {
                    string ct = getValue(ClientFunctionKey);
                    return string.IsNullOrEmpty(ct) ? ClientFunctions.None : (ClientFunctions)Enum.Parse(typeof(ClientFunctions), ct);
                }
                catch { }
                return ClientFunctions.None;
            }
            set { setValue(ClientFunctionKey, value.ToString()); }
        }

        /// <summary>
        /// Returns the WATS Client Type
        /// </summary>
        public static ClientLicenseTypes ClientLicense
        {
            get
            {
                try
                {
                    string ct = getValue(ClientLicenseKey);
                    return string.IsNullOrEmpty(ct) ? ClientLicenseTypes.Development : (ClientLicenseTypes)Enum.Parse(typeof(ClientLicenseTypes), ct);
                }
                catch { }
                return ClientLicenseTypes.Production;
            }
            //set { setValue(ClientTypeKey, value.ToString()); }
        }


        /// <summary>
        /// Get or Set TransferCompressed value, indicates if reports are compressed using GZipStream before transfer to server. This value 
        /// </summary>
        public static bool CompressionEnabled
        {
            get
            {
                bool value;
                if (bool.TryParse(getValue(compressionEnabledKey), out value)) return value;
                else return false;
            }
            set { setValue(compressionEnabledKey, value.ToString()); }
        }


        /// <summary>
        /// Software distribution from MES will use this root directory
        /// </summary>
        public static string MESSoftwareDistributionRoot
        {
            get
            {
                string regValue = getValue(SoftwareDistributionRootKey);
                if (string.IsNullOrEmpty(regValue))
                {
                    regValue = Path.Combine(DataDir, "SoftwareDistribution");

                    try
                    {
                        Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders");
                        string root = Microsoft.Win32.Registry.GetValue(key.Name, "Common Documents", "") as string;
                        if (!string.IsNullOrEmpty(root))
                            regValue = Path.Combine(root, "SoftwareDistribution"); ;
                    }
                    catch { }

                    setValue(SoftwareDistributionRootKey, regValue);
                }
                return regValue;
            }
            set { setValue(SoftwareDistributionRootKey, value); }
        }

        /// <summary>
        /// Default MES FileTransfer ChunkSize
        /// </summary>
        public static string FileTransferChunkSize
        {
            get
            {
                string regValue = getValue(FileTransferChunkSizeKey);
                if (string.IsNullOrEmpty(regValue))
                {
                    regValue = @"65000";
                    setValue(FileTransferChunkSizeKey, regValue);
                }
                return regValue;
            }
            set { setValue(FileTransferChunkSize, value); }
        }


        /// <summary>
        /// Possible to change default certificate name
        /// </summary>
        public static string TDMEndpointCertificateName
        {
            get
            {
                string regValue = getValue(EndpointCertificateName);
                if (string.IsNullOrEmpty(regValue))
                {
                    regValue = "certificates.p7b";
                    setValue(EndpointCertificateName, regValue);
                }
                return regValue;
            }
            set { setValue(EndpointCertificateName, value); }
        }

        /// <summary>
        /// Gets a string value from WCFConfig file
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public static string GetAppSetting(string key)
        {
            ExeConfigurationFileMap map = new ExeConfigurationFileMap();
            map.ExeConfigFilename = WCFConfigFile;
            System.Configuration.Configuration cfg = ConfigurationManager.OpenMappedExeConfiguration(map, ConfigurationUserLevel.None);
            return cfg.AppSettings.Settings[key].Value;
        }

        //public static string LoggingFileName { get { return DataDir + "debug.log"; } }

        public static void StartLogicalTraceOperation()
        {
            GetCorrelationManager().StartLogicalOperation();
        }
        public static void StopLogicalTraceOperation()
        {
            GetCorrelationManager().StopLogicalOperation();

        }
        public static CorrelationManager GetCorrelationManager()
        {
            return System.Diagnostics.Trace.CorrelationManager;
        }

        public const string InstalledPackagesFileName = "InstalledPackages.xml";
        public const string DeployConfigFileName = "Deploy.xml";
        public const string ConvertersFileName = "Converters.xml";
        public const string GeneralSettingsFileName = "GeneralOptions.config";
        public const string StandardTextFileName = "StandardText.txt";
        public static string GetConfigFilePath(string ConfigFileName)
        {
            return Path.Combine(DataDir, ConfigFileName);
        }


        /// <summary>
        /// Returns Special Folder's path using Environment.GetFolderPath(). If SpecialFolderName cannot be resolved (Framework 3.5 has no definition for SpecialFolder.CommonDocuments) it will try to resolved from Environment variable(s)
        /// </summary>
        /// <param name="SpecialFolderName"></param>
        /// <returns></returns>
        public static string GetFolderPath(string SpecialFolderName)
        {
            //Environment.GetFolderPath((Environment.SpecialFolder)Enum.Parse(typeof(Environment.SpecialFolder), path.Substring(2, idx - 2)))
            Environment.SpecialFolder folder;
            if (Enum.TryParse<Environment.SpecialFolder>(SpecialFolderName, out folder)) return Environment.GetFolderPath(folder);
            else
            {
                switch (SpecialFolderName.ToLower())
                {
                    case "commondocuments":
                        if (Environment.OSVersion.Version.Major < 6) // isXP, use %ALLUSERSPROFILE%\Documents
                            return Path.Combine(Environment.GetEnvironmentVariable("ALLUSERSPROFILE"), "Documents");
                        else // isVista/W7/W8, use %PUBLIC%\Documents
                            return Path.Combine(Environment.GetEnvironmentVariable("PUBLIC"), "Documents");
                    default:
                        string path = Environment.GetEnvironmentVariable(SpecialFolderName);
                        if (Directory.Exists(path)) return path;
                        else throw new ArgumentException("Unable to resolve this folder", "SpecialFolderName");
                }
            }
        }
        private static string GetWATSRegistryValue(string key, string defaultValue)
        {
            throw new NotImplementedException();
        }
        private static string GetWATSRegistryValue(string keyName)
        {
            var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS");
            if (key != null)
            {
                return key.GetValue(keyName) as string;
            }
            else
                return null;
        }

        private static void SetWATSRegistryValue(string keyName, string stringValue)
        {
            var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS");
            if (key == null) throw new ApplicationException("Required registry key missing, re-run setup to repair this WATS installation");
            else key.SetValue(keyName, stringValue);
        }

    }


}
