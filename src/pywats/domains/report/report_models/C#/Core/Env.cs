using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.IO;
using System.Configuration;
using Virinco.WATS.Configuration;
using Virinco.WATS.REST;
using System.Runtime.Versioning;

namespace Virinco.WATS
{
    /// <summary>
    /// 
    /// </summary>
    [SupportedOSPlatform("windows")]
    public static class Env
    {
        const string eventSource = "WATS";
        const string dataDirKey = "DataDir";
        const string installDirKey = "InstallDir";
        //const string memberIdKey = "MemberID"; NOT In use, now MAC adress is used
        const string MACAddressRegisteredKey = "MACAddressRegistered";
        const string IdentifierTypeKey = "IdentifierType";
        const string stationNameKey = "StationName";
        const string locationKey = "Location";
        const string purposeKey = "Purpose";
        const string gpspositionKey = "GPSPosition";
        const string gpspositionenabledKey = "GPSPositionEnabled";
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
        private static Dictionary<string, string> volreg { get { if (_volatileReg == null)_volatileReg = new Dictionary<string, string>(); return _volatileReg; } }
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

        /// <summary>
        /// Logs an exception to WATS.LOG and Server
        /// NB: Rethrow exception has been removed. Must be handled by caller.
        /// </summary>
        /// <param name="e"></param>
        /// <param name="userMessage"></param>
        public static void LogException(Exception e, string userMessage)
        {
            Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = userMessage });
            LastException = e;
        }
        public static void LogExceptionToLocalFile(Exception e, string userMessage)
        {
            _watslog?.Write(e, userMessage);
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
                    if (Boolean.TryParse(getValue(LogExceptionsKey, PersistValues), out logex)) _logexceptions = logex;
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
            SourceLevels level = LoggingLevel;

            if (!_logging.HasValue || _logging.Value != level) // Check if firsttime or level changed...
            {
                if (_tracesource == null)
                {
                    _tracesource = new TraceSource("Virinco.WATS.Logging.Client");
                    _tracesource.Switch.Level = SourceLevels.ActivityTracing | SourceLevels.Verbose;
                }
                
                // Create new rolling text logger
                _watslog = level == SourceLevels.Off ? null : new RollingTextWriterTraceListener(GetConfigFilePath(WatsLogFileName)) { Filter = new EventTypeFilter(level) };
                if (_watslog != null)
                {
                    _tracesource.Listeners.Add(_watslog);
                }
                _logging = level;
            }
        }

        public static SourceLevels LoggingLevel
        {
            get
            {
                var proxy = new ServiceProxy();
                proxy.LoadSettings();
                return proxy._settings.LoggingSettings.LoggingLevel;
            }
            set 
            {
                var proxy = new ServiceProxy();
                proxy.LoadSettings();
                proxy._settings.LoggingSettings.LoggingLevel = value;
                proxy.SaveSettings();

                InitializeLogging();
            }
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

        internal static string getValue(string key, bool persist)
        {
            if (persist) return Registry.GetWATSRegistryValue(key);
            else
            {
                if (volreg.ContainsKey(key)) return volreg[key];
                else
                {
                    string val = Registry.GetWATSRegistryValue(key);
                    volreg[key] = val;
                    return val;
                }
            }
        }

        internal static void setValue(string key, string value, bool persist)
        {
            if (persist) Registry.SetWATSRegistryValue(key, value);
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
        [Obsolete("MemberId is no longer in use starting from WATS Client version 5.0")]
        public static Guid MemberId
        {
            get
            {
                return Guid.Empty;
            }
        }

        /// <summary>
        /// Disk location for storage of pending reports, WCF config and other
        /// </summary>
        public static string DataDir
        {
            get
            {
                string dataDir = getValue(dataDirKey, PersistValues);// GetWATSRegistryValue(dataDirKey);
                if (string.IsNullOrEmpty(dataDir))
                {
                    dataDir = Path.Combine(System.Environment.GetFolderPath(Environment.SpecialFolder.CommonApplicationData),
                        @"Virinco\WATS\");
                    setValue(dataDirKey, dataDir, PersistValues);
                }
                return dataDir;
            }
            set
            {
                try
                {
                    if (!Directory.Exists(value))
                    {
                        Directory.CreateDirectory(value);
                        Utilities.SetModifyControlPermissionsToEveryone(value);
                    }
                    setValue(dataDirKey, value, PersistValues);
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
            get { return getValue(installDirKey, PersistValues); }
            set { setValue(installDirKey, value, PersistValues); }
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
            get { return getValue(purposeKey, PersistValues); }
            set { setValue(purposeKey, value, PersistValues); }
        }

        /// <summary>
        /// Test station location
        /// </summary>
        public static string Location
        {
            get { return getValue(locationKey, PersistValues); }
            set { setValue(locationKey, value, PersistValues); }
        }

        public static string GPSPosition 
        {
            get { return getValue(gpspositionKey, PersistValues); }
            set { setValue(gpspositionKey, value, PersistValues); }
        }

        public static bool GPSPositionEnabled
        {
            get
            {
                bool value;
                if (bool.TryParse(getValue(gpspositionenabledKey, PersistValues), out value)) return value;
                else return false;
            }
            set { setValue(gpspositionenabledKey, value.ToString(), PersistValues); }
        }

        /// <summary>
        /// Operator Name
        /// </summary>
        public static string Operator
        {
            get { return getValue(operatorNameKey, false); }
            set { setValue(operatorNameKey, value, false); }
        }

        /// <summary>
        /// File name for WCF Configuration 
        /// </summary>
        public static string WCFConfigFile
        {
            get { 
                string path = getValue(WCFConfigFileKey, PersistValues);
                if (string.IsNullOrEmpty(path))
                {
                    path = Path.Combine(DataDir, "WATS_WCF.config");
                    setValue(WCFConfigFileKey, path, PersistValues);
                }
                return path;
            }
            set { setValue(WCFConfigFileKey, value, PersistValues); }
        }

        /// <summary>
        /// Full Path to WCF Configuration File - depreciated
        /// </summary>
        /// <remarks>DEPRECEATED, use WCFConfigFile instead. This property getter wil be removed in a forthcoming release!</remarks>
        public static string WCFConfigFileFullName
        {
            get { return getValue(WCFConfigFileKey, PersistValues); }
        }

        /// <summary>
        /// Default Endpoint for TDM
        /// </summary>
        public static string TDMEndpoint
        {
            get
            {
                string ep = getValue(TDMEndPointKey, PersistValues);
                if (string.IsNullOrEmpty(ep)) return "TDM-Default";
                else return ep;
            }
            set { setValue(TDMEndPointKey, value, PersistValues); }
        }

        /// <summary>
        /// Default endpoint name for MES
        /// </summary>
        public static string MESEndpointName
        {
            get
            {
                string ep = getValue(MESEndPointNameKey, PersistValues);
                if (string.IsNullOrEmpty(ep)) return "MES-Default";
                else return ep;
            }
            set { setValue(MESEndPointNameKey, value, PersistValues); }
        }
        /// <summary>
        /// Default endpoint name for Old MES (0.9.x)
        /// </summary>
        public static string MESEndpoint
        {
            get
            {
                string ep = getValue(MESEndPointKey, PersistValues);
                if (string.IsNullOrEmpty(ep)) return "MES-Default";
                else return ep;
            }
            set { setValue(MESEndPointKey, value, PersistValues); }
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
                    string ct = getValue(ClientFunctionKey, PersistValues);
                    return string.IsNullOrEmpty(ct) ? ClientFunctions.None : (ClientFunctions)Enum.Parse(typeof(ClientFunctions), ct);
                }
                catch { }
                return ClientFunctions.None;
            }
            set { setValue(ClientFunctionKey, value.ToString(), PersistValues); }
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
                    string ct = getValue(ClientLicenseKey, PersistValues);
                    return string.IsNullOrEmpty(ct) ? ClientLicenseTypes.Development : (ClientLicenseTypes)Enum.Parse(typeof(ClientLicenseTypes), ct);
                }
                catch { }
                return ClientLicenseTypes.Production;
            }
        }

        //Used to store last used mac address as identification of the machine
        public static string MACAddressRegistered
        {
            get
            {
                return getValue(MACAddressRegisteredKey, PersistValues);
            }
            set { setValue(MACAddressRegisteredKey, value.ToString(), PersistValues); }
        }


        public static ClientIdentifierType IdentifierType
        {
            get
            {
                try
                {
                    if (int.TryParse(getValue(IdentifierTypeKey, PersistValues), out int i))
                    {
                        if (Enum.IsDefined(typeof(ClientIdentifierType), i))
                            return (ClientIdentifierType)i;
                    }
                }
                catch { }
                return ClientIdentifierType.MacAddress;
            }
            set { setValue(IdentifierTypeKey, ((int)value).ToString(), PersistValues); }
        }


        /// <summary>
        /// Get or Set TransferCompressed value, indicates if reports are compressed using GZipStream before transfer to server. This value 
        /// </summary>
        public static bool CompressionEnabled
        {
            get
            {
                bool value;
                if (bool.TryParse(getValue(compressionEnabledKey, PersistValues), out value)) return value;
                else return false;
            }
            set { setValue(compressionEnabledKey, value.ToString(), PersistValues); }
        }


        /// <summary>
        /// Software distribution from MES will use this root directory
        /// </summary>
        public static string MESSoftwareDistributionRoot
        {
            get
            {
                string regValue = getValue(SoftwareDistributionRootKey, PersistValues);
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

                    setValue(SoftwareDistributionRootKey, regValue, PersistValues);
                }
                return regValue;
            }
            set { setValue(SoftwareDistributionRootKey, value, PersistValues); }
        }

        /// <summary>
        /// Default MES FileTransfer ChunkSize
        /// </summary>
        public static string FileTransferChunkSize
        {
            get
            {
                string regValue = getValue(FileTransferChunkSizeKey, PersistValues);
                if (string.IsNullOrEmpty(regValue))
                {
                    regValue = @"65000";
                    setValue(FileTransferChunkSizeKey, regValue, PersistValues);
                }
                return regValue;
            }
            set { setValue(FileTransferChunkSize, value, PersistValues); }
        }

        /*
        /// <summary>
        /// Possible to change default certificate name
        /// </summary>
        public static string TDMEndpointCertificateName
        {
            get
            {
                string regValue = getValue(EndpointCertificateName, PersistValues);
                if (string.IsNullOrEmpty(regValue))
                {
                    regValue = "certificates.p7b";
                    setValue(EndpointCertificateName, regValue, PersistValues);
                }
                return regValue;
            }
            set { setValue(EndpointCertificateName, value, PersistValues); }
        }
        */
        /*
        // Rollback to framework 2.0: use PInvoke to access common registry (avoid WoW3264 node mixups)
        private static string GetWATSRegistryValue(string keyName)
        {
            var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS");
            if (key != null)
            {
                return key.getValue(keyName, PersistValues) as string;
            }
            else
                return null;
        }

        private static void SetWATSRegistryValue(string keyName, string stringValue)
        {
            var key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Virinco\WATS", true);
            if (key == null) throw new ApplicationException("Required registry key missing, re-run setup to repair this WATS installation");
            else key.setValue(keyName, stringValue, PersistValues);
        }
        */
        /*
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
        */
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
        public const string DownloadManagerFileName = "DownloadManager.xml";
        public const string DeployConfigFileName = "Deploy.xml";
        public const string ConvertersFileName = "Converters.xml";
        public const string GeneralSettingsFileName = "GeneralOptions.config";
        public const string StandardTextFileName = "StandardText.txt";
        public const string SettingsFileName = "settings.json";
        public const string WatsLogFileName = "wats.log";

        public static string GetConfigFilePath(string ConfigFileName)
        {
            return Path.Combine(DataDir, ConfigFileName);
        }
    }
}
