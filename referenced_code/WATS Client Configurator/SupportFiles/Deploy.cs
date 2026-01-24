using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.Xml.XPath;
using System.IO;
using Virinco.WATS.Client.Configurator.View;
using Virinco.WATS.Interface.Models;
using System.IO.Compression;

namespace Virinco.WATS.Client.Configurator.SupportFiles
{
    public class Deploy
    {
        public static readonly XNamespace xmlns = "http://schemas.virinco.com/WATS/Wats-Client/Deployment.xsd";

        public const string ConfigFile = @"Virinco\WATS\Deploy.xml";

        public static readonly IReadOnlyDictionary<string, string> DefaultValues = new Dictionary<string, string>
        {
            { "WATS_SequentialModel.Seq|WATS_BatchModel.Seq|WATS_ParallelModel.Seq", "SequentialModel.seq|BatchModel.seq|ParallelModel.seq" },
            { "WATS_SequentialModel.Seq", "SequentialModel.seq" }
        };

        public Deploy() { }

        public static void UnDeployAll()
        {
            foreach (Product p in GetDeploymentConfigurations().Where(p => p.IsTSInstalled))
            {
                try { p.UnDeployFiles(); }
                catch { } //Don't care
            }
        }

        public static string GetAssemblyFolder() => Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);

        public static string GetSupportFilesRoot() => Path.Combine(GetAssemblyFolder(), "SupportFiles");

        public static string GetDeployConfigFilePath() => Env.GetConfigFilePath(Env.DeployConfigFileName);

        public static string GetConvertersFilePath() => Env.GetConfigFilePath(Env.ConvertersFileName);

        public static System.Collections.ObjectModel.ObservableCollection<Product> GetDeploymentConfigurations() => GetDeploymentConfigurations(true);

        public static System.Collections.ObjectModel.ObservableCollection<Product> GetDeploymentConfigurations(bool updateState)
        {
            System.Collections.ObjectModel.ObservableCollection<Product> lst = new System.Collections.ObjectModel.ObservableCollection<Product>();
            string SupportFilesRoot = GetSupportFilesRoot();
            var deployConfigPath = GetDeployConfigFilePath();
            XDocument doc = XDocument.Load(deployConfigPath);
            foreach (XElement config in doc.Root.Elements(Deploy.xmlns + "Product"))
            {
                Product p = new Product(config, SupportFilesRoot, updateState);
                lst.Add(p);
            }
            doc.Save(deployConfigPath);
            return lst;
        }

        internal static void ValidateConfiguration(CLUtil.ArgumentParser args)
        {
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: ValidateConfiguration started");
            /*
            string wcfFilePath = Env.WCFConfigFile;
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking WCF Config file existence");
            if (!System.IO.File.Exists(wcfFilePath))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Writing default WCF Config");
                XDocument wcfXDoc = XDocument.Parse(Virinco.WATS.Client.Configurator.Properties.Resources.WATS_WCF);
                try { wcfXDoc.Save(wcfFilePath); } // using exception catching to eliminate racecondition...
                catch (Exception ex) { if (!System.IO.File.Exists(wcfFilePath)) throw ex; } // Rethrow exception if non-exisiting
            }
            */
            //
            //Configuration.ClientSettings settings=Configuration.ClientSettings
            var settings = new ServiceProxy();
            settings.ConvertFromWCFSettings(Path.Combine(Env.DataDir, "wats_wcf.config"));

            /*
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking for url parameters");
            if (args.Options.ContainsKey("tdmurl") || args.Options.ContainsKey("mesurl"))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Setting Service url(s)");
                Virinco.WATS.Client.Configurator.ViewModel.ConfigViewModel cfg = new ViewModel.ConfigViewModel();
                if (args.Options.ContainsKey("tdmurl") && !string.IsNullOrEmpty(args.Options["tdmurl"].Value))
                {
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: TDM Service url: [{0}]", args.Options["tdmurl"].Value);
                    cfg.SetServerAddress(args.Options["tdmurl"].Value);
                }
                if (args.Options.ContainsKey("mesurl") && !string.IsNullOrEmpty(args.Options["mesurl"].Value))
                {
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: MES Service url: [{0}]", args.Options["mesurl"].Value);
                    cfg.SetServerAddress(args.Options["mesurl"].Value);
                }
            }
            */
            /*
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking for deployfail existence");
            string deployFilePath = Env.GetConfigFilePath(Env.DeployConfigFileName);
            if (!System.IO.File.Exists(deployFilePath))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Writing default Deployfile");
                XDocument deployXDoc = XDocument.Parse(Virinco.WATS.Client.Configurator.Properties.Resources.Deploy);
                try { deployXDoc.Save(deployFilePath); } // using exception catching to eliminate racecondition...
                catch (Exception ex) { if (!System.IO.File.Exists(deployFilePath)) throw ex; } // Rethrow exception if non-exisiting
            }
            else // deployfile exists, check that all products exists, merge new products into exisiting file
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking Deployfile");
                bool modified = false;
                XDocument deployXDoc = XDocument.Parse(Virinco.WATS.Client.Configurator.Properties.Resources.Deploy);
                XDocument currentXDoc = XDocument.Load(deployFilePath);
                XNamespace ns = "http://schemas.virinco.com/WATS/Wats-Client/Deployment.xsd";
                IEnumerable<XElement> currentProducts = currentXDoc.Root.Elements(ns + "Product");
                IEnumerable<XElement> deployProducts = deployXDoc.Root.Elements(ns + "Product");
                foreach (XElement el in deployProducts)
                {
                    var currentProduct = currentProducts.FirstOrDefault(c => c.Attribute("Id").Value == el.Attribute("Id").Value);
                    if (currentProduct == null) // el (new) was not found in currentProducts!
                    {
                        currentXDoc.Root.Add(el);
                        modified = true;
                    }
                    else if (currentProduct.Elements(ns + "CopyFolder").Count() > 0)
                    {
                        // product element with CopyFolder element exists, replace content :o
                        currentProduct.ReplaceNodes(el.Nodes());
                        modified = true;
                    }
                }
                try
                {
                    if (modified)
                    {
                        Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Writing changes to Deployfile");
                        currentXDoc.Save(deployFilePath);
                    }
                } // using exception catching to eliminate racecondition...
                catch (Exception ex) { if (!System.IO.File.Exists(deployFilePath)) throw ex; } // Rethrow exception if non-exisiting
            }
            */
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking for converter file exsistence");
            string convertersFilePath = Env.GetConfigFilePath(Env.ConvertersFileName);
            XDocument DefaultconvertersXDoc = XDocument.Parse(Virinco.WATS.Client.Configurator.Properties.Resources.Converters);
            XNamespace nsConv = "http://schemas.virinco.com/WATS/Wats-Client-Service/Converters.xsd";           
            // Set StdText folder
            var conv = DefaultconvertersXDoc.Element(nsConv + "converters").Elements(nsConv + "converter").Where(cv => cv.Attribute("name").Value == "WSTFImporter").First();
            conv.Element(nsConv + "Source").Elements(nsConv + "Parameter").Where(p => p.Attribute("name").Value == "Path").First().Value = Path.Combine(Env.DataDir, "WatsStandardTextFormat");
            // Set StdXML folder
            conv = DefaultconvertersXDoc.Element(nsConv + "converters").Elements(nsConv + "converter").Where(cv => cv.Attribute("name").Value == "WSXFImporter").First();
            conv.Element(nsConv + "Source").Elements(nsConv + "Parameter").Where(p => p.Attribute("name").Value == "Path").First().Value = Path.Combine(Env.DataDir, "WatsStandardXmlFormat");
            // Set ATML folder
            conv = DefaultconvertersXDoc.Element(nsConv + "converters").Elements(nsConv + "converter").Where(cv => cv.Attribute("name").Value == "ATMLImporter").First();
            conv.Element(nsConv + "Source").Elements(nsConv + "Parameter").Where(p => p.Attribute("name").Value == "Path").First().Value = Path.Combine(Env.DataDir, "ATMLFormat");
            // Set WSJF folder
            conv = DefaultconvertersXDoc.Element(nsConv + "converters").Elements(nsConv + "converter").Where(cv => cv.Attribute("name").Value == "WSJFImporter").First();
            conv.Element(nsConv + "Source").Elements(nsConv + "Parameter").Where(p => p.Attribute("name").Value == "Path").First().Value = Path.Combine(Env.DataDir, "WatsStandardJsonFormat");
            //// Set Legacy-TSDump folder
            //conv = DefaultconvertersXDoc.Element(nsConv + "converters").Elements(nsConv + "converter").Where(cv => cv.Attribute("name").Value == "Legacy-TSImporter").First();
            //conv.Element(nsConv + "Source").Elements(nsConv + "Parameter").Where(p => p.Attribute("name").Value == "Path").First().Value = Path.Combine(Env.DataDir, "TSDump");

            if (!System.IO.File.Exists(convertersFilePath))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Writing default converters file");
                // Save converters.xml
                try { DefaultconvertersXDoc.Save(convertersFilePath); } // using exception catching to eliminate racecondition...
                catch (Exception ex) { if (!System.IO.File.Exists(convertersFilePath)) throw ex; } // Rethrow exception if non-exisiting
            }
            else // Converters.xml exists, merge missing default converters
            {
                bool changed = false;
                XDocument convertersXDoc = XDocument.Load(convertersFilePath);
                foreach (XElement e_default in DefaultconvertersXDoc.Root.Elements(nsConv + "converter"))
                {
                    XElement converter = convertersXDoc.Root.Elements(nsConv + "converter").FirstOrDefault(e => e.Attribute("name").Value == e_default.Attribute("name").Value);
                    if (converter == null)
                    {
                        convertersXDoc.Root.Add(e_default);
                        changed = true;
                    }
                }

                //Remove legacy converter
                var legacyConverterNames = new[] { "Legacy4.2-Importer", "TSImporter", "Legacy-TSImporter" };
                var legacyConverters = convertersXDoc.Element(nsConv + "converters").Elements(nsConv + "converter").Where(cv => legacyConverterNames.Contains(cv.Attribute("name").Value));
                foreach(var legacyConverter in legacyConverters)
                {
                    legacyConverter.Remove();
                    changed = true;
                }

                if (changed)
                {
                    bool saved = false; Exception ex = null;
                    for (int i = 0; i < 10; i++)
                    {
                        try { convertersXDoc.Save(convertersFilePath); saved = true; break; }
                        catch (Exception e) { System.Threading.Thread.Sleep(50); ex = e; }
                    }
                    if (!saved) Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Failed to save the merged convertes.xml file" });
                }
            }
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking for generalsettings file exsistence");
            XDocument DefaultGeneralSettingsXDoc = XDocument.Parse(Virinco.WATS.Client.Configurator.Properties.Resources.GeneralSettings_default);
            string GeneralSettingsFilePath = Env.GetConfigFilePath(Env.GeneralSettingsFileName);
            if (!System.IO.File.Exists(GeneralSettingsFilePath))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Writing default GeneralSettings file");
                try { DefaultGeneralSettingsXDoc.Save(GeneralSettingsFilePath); } // using exception catching to eliminate racecondition...
                catch (Exception ex) { if (!System.IO.File.Exists(GeneralSettingsFilePath)) throw ex; } // Rethrow exception if non-exisiting
            }
            else // GeneralConfig file exists, merge new keys into file
            {
                bool changed = false;
                XDocument GeneralSettingsXDoc = XDocument.Load(GeneralSettingsFilePath);
                XElement appSettings = GeneralSettingsXDoc.Root.Element("appSettings");
                foreach (XElement e_default in DefaultGeneralSettingsXDoc.Root.Element("appSettings").Elements("add"))
                {
                    XElement e_setting = appSettings.Elements("add").FirstOrDefault(e => e.Attribute("key").Value == e_default.Attribute("key").Value);
                    if (e_setting == null)
                    {
                        appSettings.Add(e_default);
                        changed = true;
                    }
                }
                if (changed)
                {
                    bool saved = false; Exception ex = null;
                    for (int i = 0; i < 10; i++)
                    {
                        try { GeneralSettingsXDoc.Save(GeneralSettingsFilePath); saved = true; break; }
                        catch (Exception e) { System.Threading.Thread.Sleep(50); ex = e; }
                    }
                    if (!saved) Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Failed to save the merged GeneralOptions.config file" });
                }
            }

            /*
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking for codes file exsistence");
            string DefaultInstanceCodesFilePath = System.IO.Path.Combine(Env.DataDir, String.Format("Codes_{0}.xml", Env.TDMEndpoint));
            if (!System.IO.File.Exists(DefaultInstanceCodesFilePath))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Writing codes file for default instance file");
                XDocument CodesXDoc = XDocument.Parse(Virinco.WATS.Client.Configurator.Properties.Resources.DefaultInstanceCodes_default);
                try { CodesXDoc.Save(DefaultInstanceCodesFilePath); } // using exception catching to eliminate racecondition...
                catch (Exception ex) { if (!System.IO.File.Exists(DefaultInstanceCodesFilePath)) throw ex; } // Rethrow exception if non-exisiting
            }
            */

            //Add default process code even if offline
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Checking for codes file exsistence");
            string DefaultInstanceCodesFilePath = System.IO.Path.Combine(Env.DataDir, "Processes.json");
            if (!System.IO.File.Exists(DefaultInstanceCodesFilePath))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: Writing codes file for default instance file");
                Process[] processes = new Process[]{
                    new Process()
                    {
                        ProcessID = Guid.Empty,
                        Code = 10,
                        Name = "SW Debug",
                        Description = "Used for SW debugging",
                        State = ProcessRecordState.Active,
                        ProcessIndex = 0,
                        IsTestOperation = true,
                        IsWIPOperation = false,
                        IsRepairOperation = false,
                        Properties = null,
                    }
                };
                using (var txtwriter = new StreamWriter(Path.Combine(Env.DataDir, "Processes.json")))
                {
                    var writer = new Newtonsoft.Json.JsonTextWriter(txtwriter);
                    var serializer = new Newtonsoft.Json.JsonSerializer();
                    try { serializer.Serialize(writer, processes); }                        
                    catch (Exception ex) { if (!System.IO.File.Exists(DefaultInstanceCodesFilePath)) throw ex; }
                }
            }

            //Add empty clientinfo
            using (var txtwriter = new StreamWriter(Path.Combine(Env.DataDir, "ClientInfo.json")))
            {
                txtwriter.Write("{}");
                txtwriter.Flush();
                txtwriter.Close();
            }

            //Update Product state in deploy.xml


            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "WATS Client Config: ValidateConfiguration completed");
        }
    }

    public class Product : System.ComponentModel.INotifyPropertyChanged
    {
        public enum ProductState 
        { 
            Unknown, 
            Not_found, 
            Not_installed, 
            Installed 
        }

        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;

        public string Name => configuration.Attribute("Name").Value;

        public string Id => configuration.Attribute("Id").Value;

        public ProductState State
        {
            get
            {
                if (Utilities.EnumTryParse(configuration.Attribute("State").Value, out ProductState state))
                    return state;
                else
                    return ProductState.Unknown;
            }
            set
            {
                configuration.Attribute("State").SetValue(value);
                OnPropertyChanged(nameof(State));
                OnPropertyChanged(nameof(StateDescription));
                OnPropertyChanged(nameof(IsTSInstalled));
                OnPropertyChanged(nameof(IsDeployed));
                OnPropertyChanged(nameof(InstallVisibility));
                OnPropertyChanged(nameof(ReinstallVisibility));
                OnPropertyChanged(nameof(StateBackground));
            }
        }

        public string StateDescription
        {
            get
            {
                switch (State)
                {
                    case ProductState.Installed: return "Installed";
                    case ProductState.Not_installed: return "Not installed";
                    case ProductState.Not_found: return "";
                    case ProductState.Unknown:
                    default: return "Unknown";
                }
            }
        }

        public System.Drawing.Brush StateBackground => new System.Drawing.SolidBrush((State == ProductState.Not_installed) ? System.Drawing.Color.Red : System.Drawing.Color.Green);

        public System.Windows.Visibility ReinstallVisibility => State == ProductState.Installed ? System.Windows.Visibility.Visible : System.Windows.Visibility.Collapsed;

        public System.Windows.Visibility InstallVisibility => State == ProductState.Not_installed ? System.Windows.Visibility.Visible : System.Windows.Visibility.Collapsed;

        public bool IsTSInstalled => State == ProductState.Installed || State == ProductState.Not_installed;

        public bool IsDeployed => State == ProductState.Installed;

        public bool IsDeploymentPackage { get; private set; }

        public string this[string attribute] => configuration.Attribute(attribute).Value;

        private FileInfo deploylog;

        private readonly XElement configuration;

        private readonly string rootSource;

        public Product(XElement configuration, string rootSource, bool updateState)
        {
            this.configuration = configuration;
            this.rootSource = rootSource;
            if (updateState) 
                UpdateState();
        }

        private void UpdateState()
        {
            if (State != ProductState.Installed)
            {
                string regKey;
                bool x86;
                bool x64;
                switch (Id)
                {
                    //case "TS2012":      regKey = @"SOFTWARE\National Instruments\TestStand\5.0" ;   x86 = true;     x64 = true;     break;
                    //case "TS2013":      regKey = @"SOFTWARE\National Instruments\TestStand\5.1" ;   x86 = true;     x64 = true;     break;
                    //case "TS2014x86":   regKey = @"SOFTWARE\National Instruments\TestStand\14.0";   x86 = true;     x64 = false;    break;
                    //case "TS2014x64":   regKey = @"SOFTWARE\National Instruments\TestStand\14.0";   x86 = false;    x64 = true;     break;
                    //case "TS2016x86":   regKey = @"SOFTWARE\National Instruments\TestStand\16.0";   x86 = true;     x64 = false;    break;
                    //case "TS2016x64":   regKey = @"SOFTWARE\National Instruments\TestStand\16.0";   x86 = false;    x64 = true;     break;
                    //case "TS2017x86":   regKey = @"SOFTWARE\National Instruments\TestStand\17.0";   x86 = true;     x64 = false;    break;
                    //case "TS2017x64":   regKey = @"SOFTWARE\National Instruments\TestStand\17.0";   x86 = false;    x64 = true;     break;
                    //case "TS2019x86":   regKey = @"SOFTWARE\National Instruments\TestStand\19.0";   x86 = true;     x64 = false;    break;
                    //case "TS2019x64":   regKey = @"SOFTWARE\National Instruments\TestStand\19.0";   x86 = false;    x64 = true;     break;
                    //case "TS2020x86":   regKey = @"SOFTWARE\National Instruments\TestStand\20.0";   x86 = true;     x64 = false;    break;
                    //case "TS2020x64":   regKey = @"SOFTWARE\National Instruments\TestStand\20.0";   x86 = false;    x64 = true;     break;
                    case "TS2021x86":   regKey = @"SOFTWARE\National Instruments\TestStand\21.0";   x86 = true;     x64 = false;    break;
                    case "TS2021x64":   regKey = @"SOFTWARE\National Instruments\TestStand\21.0";   x86 = false;    x64 = true;     break;
                    case "TS2022x86":   regKey = @"SOFTWARE\National Instruments\TestStand\22.0";   x86 = true;     x64 = false;    break;
                    case "TS2022x64":   regKey = @"SOFTWARE\National Instruments\TestStand\22.0";   x86 = false;    x64 = true;     break;
                    case "TS2023x86":   regKey = @"SOFTWARE\National Instruments\TestStand\23.0";   x86 = true;     x64 = false;    break;
                    case "TS2023x64":   regKey = @"SOFTWARE\National Instruments\TestStand\23.0";   x86 = false;    x64 = true;     break;
                    case "TS2024x86":   regKey = @"SOFTWARE\National Instruments\TestStand\24.0";   x86 = true;     x64 = false;    break;
                    case "TS2024x64":   regKey = @"SOFTWARE\National Instruments\TestStand\24.0";   x86 = false;    x64 = true;     break;
                    case "TS2025x86":   regKey = @"SOFTWARE\National Instruments\TestStand\25.0";   x86 = true;     x64 = false;    break;
                    case "TS2025x64":   regKey = @"SOFTWARE\National Instruments\TestStand\25.0";   x86 = false;    x64 = true;     break;
                    default:
                        State = ProductState.Unknown;
                        IsDeploymentPackage = false;
                        return;
                }

                //TestStand 2024 not supported, only 2025 (24.9) and newer
                if (Id == "TS2024x64")
                {
                    var regValue = GetRegistryValue(regKey, x86, x64, "Version");
                    if (!string.IsNullOrEmpty(regValue))
                    {
                        var tsVersion = Version.Parse(regValue);
                        if (tsVersion < new Version(24, 9))
                        {
                            State = ProductState.Not_found;
                            IsDeploymentPackage = false;
                            return;
                        }
                    }
                }

                bool found = GetInstallState(regKey, x86, x64, "ProductCode");
                if (found)
                {
                    State = ProductState.Not_installed;
                    IsDeploymentPackage = false;
                }
                else
                {
                    State = ProductState.Not_found;
                    IsDeploymentPackage = GetInstallState(regKey, x86, x64, "Version");
                }
            }
        }

        private bool GetInstallState(string regkey, bool x86, bool x64, string keyName)
        {
            string regValue = GetRegistryValue(regkey, x86, x64, keyName);
            return !string.IsNullOrEmpty(regValue);
        }

        private string GetRegistryValue(string regkey, bool x86, bool x64, string keyName)
        {
            string regValue;
            if (x86 && Registry.TryReadHKLM32Value(regkey, keyName, out regValue))
                return regValue;
            else if (x64 && Registry.ProcessType == Registry.ProcessTypeEnum.w32on32)
                return null; // 32bit os, do not search for 64 bit installation.
            else if (x64 && Registry.TryReadHKLM64Value(regkey, keyName, out regValue))
                return regValue;
            return null;
        }

        public bool DeployFiles(bool SuppressSuccessMessageBox, bool isRedeployFromBackup)
        {
            try
            {
                deploylog = new FileInfo(Env.GetConfigFilePath($"{Id}-deploy.log"));
                if (IsTeststandPrepared(configuration.Elements(Deploy.xmlns + "ModifyINI")) && IsTeststandPrepared(configuration.Elements(Deploy.xmlns + "ModifyXml")))
                {
                    using (var logWriter = deploylog.AppendText()) 
                        logWriter.WriteLine($"# Begin deploy to {Id} @{DateTime.Now}");

                    //Parse and execute each line...
                    foreach (XElement xItem in configuration.Elements())
                    {
                        switch (xItem.Name.LocalName)
                        {
                            case "Archive": // Unpack all files in archive
                                using (var fileStream = File.Open(Path.Combine(rootSource, xItem.Attribute("source").Value), FileMode.Open, FileAccess.Read))
                                using (var zip = new ZipArchive(fileStream, ZipArchiveMode.Read))
                                {
                                    var path = GetFullPath(xItem.Attribute("destination").Value);
                                    zip.ExtractToDirectory(path, true);
                                }
                                break;
                                //Microsoft.Deployment.Compression.Zip.ZipInfo zi = new Microsoft.Deployment.Compression.Zip.ZipInfo(Path.Combine(rootSource, xItem.Attribute("source").Value));
                                //zi.Unpack(GetFullPath(xItem.Attribute("destination").Value), new EventHandler<ArchiveProgressEventArgs>(Unzip));
                                //break;
                            case "ModifyINI":
                                if (!isRedeployFromBackup)
                                    ModifyINI(xItem);
                                break;
                            case "ModifyXml":
                                if (!isRedeployFromBackup)
                                    ModifyXml(xItem);
                                break;
                            /*TODO: Insert other actions here.... */
                            default: break;
                        }
                    }

                    State = ProductState.Installed;
                    SaveConfig();

                    if (!SuppressSuccessMessageBox)
                    {
                        //todo:display deployed image
                        string deployImage = Path.Combine(rootSource, "deployCompleted.jpg");
                        if (File.Exists(deployImage))
                        {
                            ImageBox imageBox = new ImageBox("Teststand integration completed", $"Succesfully installed WATS Add-on for {Name}", deployImage);
                            imageBox.ShowDialog();
                        }
                        else
                            System.Windows.Forms.MessageBox.Show($"Succesfully installed WATS Add-on for {Name}", "Teststand integration completed", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);

                    }

                    using (var logWriter = deploylog.AppendText()) 
                        logWriter.WriteLine($"# Finished deploy to {Id} @{DateTime.Now}");

                    return true;
                }
                return false;
            }
            catch (Exception e)
            {
                Env.LogException(e, "Teststand integration failed");
                using (var logWriter = this.deploylog.AppendText()) 
                    logWriter.WriteLine($"# Deploy failed for product {Id}: {e.Message} @{DateTime.Now}");

                System.Windows.Forms.MessageBox.Show(e.Message, "Teststand integration failed", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Exclamation);
                return false;
            }

            bool IsTeststandPrepared(IEnumerable<XElement> xModify)
            {
                foreach(var xItem in xModify)
                {
                    if (!File.Exists(GetFullPath(xItem.Attribute("file").Value)))
                    {
                        System.Windows.Forms.MessageBox.Show("Teststand is not initialized.\nTeststand must be started at least once before WATS Integration. Please start and exit Teststand and try again.", "Teststand integration failed", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Exclamation);
                        return false;
                    }
                }
                return true;
            }

            //void Unzip(object sender, ArchiveProgressEventArgs e)
            //{
            //    switch (e.ProgressType)
            //    {
            //        case ArchiveProgressType.StartArchive:
            //            using (var logWriter = deploylog.AppendText()) 
            //                logWriter.WriteLine($"extract-start '{e.CurrentArchiveName}' #ArchiveNo:{e.CurrentArchiveNumber}, Size:{e.CurrentArchiveTotalBytes}");
            //            break;
            //        case ArchiveProgressType.FinishFile:
            //            using (var logWriter = deploylog.AppendText()) 
            //                logWriter.WriteLine($"extract-file '{e.CurrentFileName}' #FileNo:{e.CurrentFileNumber}, Size:{e.CurrentFileBytesProcessed}");
            //            break;
            //        case ArchiveProgressType.FinishArchive:
            //            using (var logWriter = deploylog.AppendText()) 
            //                logWriter.WriteLine($"extract-complete '{e.CurrentArchiveName}' #ArchiveNo:{e.CurrentArchiveNumber}, Size:{e.CurrentArchiveTotalBytes}");
            //            break;
            //    }
            //}
        }

        public void UnDeployFiles()
        {
            deploylog = new FileInfo(Path.Combine(Env.DataDir, $"{Id}-deploy.log"));
            using (var logWriter = deploylog.AppendText()) 
                logWriter.WriteLine($"# Begin uninstallation of {Id} @{DateTime.Now}");

            // Parse and execute each line...
            foreach (XElement item in configuration.Elements())
            {
                switch (item.Name.LocalName)
                {
                    case "Archive": // Remove all files that exists in archive
                        using (var logWriter = deploylog.AppendText()) 
                            logWriter.WriteLine($"remove-files start");

                        using (var fileStream = File.Open(Path.Combine(rootSource, item.Attribute("source").Value), FileMode.Open, FileAccess.Read)) //Test!
                        {
                            ZipArchive zip = new(fileStream);


                            //Microsoft.Deployment.Compression.Zip.ZipInfo zi = new Microsoft.Deployment.Compression.Zip.ZipInfo(Path.Combine(rootSource, item.Attribute("source").Value));
                            string destination = GetFullPath(item.Attribute("destination").Value);

                            foreach (var f in zip.Entries)
                            {
                                using (var logWriter = deploylog.AppendText())
                                    logWriter.WriteLine($"remove-file: {f.FullName}"); //\\{f.Name}

                                string fpath = Path.Combine(destination, f.FullName) /*+ @"\" + f.Name*/;
                                if (File.Exists(fpath))
                                    File.Delete(fpath);
                            }

                            // Remove (sub-)directories if empty
                            foreach (var directory in new DirectoryInfo(destination).GetDirectories())
                                DeleteDirectoryIfEmpty(directory);

                            using (var logWriter = deploylog.AppendText())
                                logWriter.WriteLine($"remove-files end");
                        }
                        break;
                    case "ModifyINI":
                        RestoreINI(item);
                        break;
                    case "ModifyXml":
                        RestoreXml(item);
                        break;
                    /*TODO: Insert other actions here.... */
                    default:
                        break;
                }
            }

            State = ProductState.Unknown;
            UpdateState();
            SaveConfig();

            using (var logWriter = deploylog.AppendText()) 
                logWriter.WriteLine($"# Finished uninstallation of {Id} @{DateTime.Now}");

            void DeleteDirectoryIfEmpty(DirectoryInfo directory)
            {
                foreach (var subDirectory in directory.GetDirectories()) 
                    DeleteDirectoryIfEmpty(subDirectory);

                if (!directory.GetFileSystemInfos().Any()) 
                    directory.Delete();
            }
        }

        private void ModifyINI(XElement item)
        {
            IniFile f = new IniFile(GetFullPath(item.Attribute("file").Value));
            List<XElement> newbackup = new List<XElement>();
            foreach (XElement subitem in item.Elements())
            {
                switch (subitem.Name.LocalName)
                {
                    case "set-value":
                        string section = subitem.Attribute("section").Value;
                        string key = subitem.Attribute("key").Value;
                        string oldvalue = f[section, key];
                        f[section, key] = subitem.Value;
                        IEnumerable<XElement> records = (from e in item.Elements(Deploy.xmlns + "original-value") where e.Attribute("section").Value == section && e.Attribute("key").Value == key select e);
                        if (records == null || records.Count() == 0)
                            newbackup.Add(new XElement(Deploy.xmlns + "original-value", new XAttribute("section", section), new XAttribute("key", key), new XText(oldvalue)));
                        
                        using (var logWriter = deploylog.AppendText()) 
                            logWriter.WriteLine($"ini-set-value: section:'{section}',key:'{key}', oldvalue:'{oldvalue}'");
                        break;
                }
            }

            if (newbackup.Count > 0) 
                item.Add(newbackup);
        }

        private void ModifyXml(XElement item)
        {
            XDocument f = XDocument.Load(GetFullPath(item.Attribute("file").Value));
            List<XElement> newbackup = new List<XElement>();
            foreach (XElement subitem in item.Elements())
            {
                switch (subitem.Name.LocalName)
                {
                    case "set-value":
                        var xpath = subitem.Attribute("xpath").Value;
                        var element = f.XPathSelectElement(xpath);
                        string oldvalue = element.Value;
                        element.SetValue(subitem.Value);
                        IEnumerable<XElement> records = (from e in item.Elements(Deploy.xmlns + "original-value") where e.Attribute("xpath").Value == xpath select e);
                        if (records == null || records.Count() == 0)
                            newbackup.Add(new XElement(Deploy.xmlns + "original-value", new XAttribute("xpath", xpath), new XText(oldvalue)));

                        using (var logWriter = deploylog.AppendText()) 
                            logWriter.WriteLine($"xml-set-value: xpath:'{xpath}',oldvalue:'{oldvalue}'");
                        break;
                }
            }

            f.Save(GetFullPath(item.Attribute("file").Value));
            if (newbackup.Count > 0) 
                item.Add(newbackup);
        }

        private void RestoreINI(XElement item)
        {
            var fpath = item.Attribute("file").Value;
            using (var s = this.deploylog.AppendText()) s.WriteLine($"restore-ini-begin: {fpath}");
            IniFile f = new IniFile(GetFullPath(fpath));
            List<XElement> remove = new List<XElement>();
            foreach (XElement subitem in item.Elements())
            {
                switch (subitem.Name.LocalName)
                {
                    case "original-value":
                        string section = subitem.Attribute("section").Value;
                        string key = subitem.Attribute("key").Value;
                        f[section, key] = subitem.Value;
                        remove.Add(subitem);
                        break;
                }
            }

            foreach (XElement el in remove) 
                el.Remove();

            using (var logWriter = deploylog.AppendText()) 
                logWriter.WriteLine($"restore-ini-end: {fpath}");
        }

        private void RestoreXml(XElement item)
        {
            var fpath = item.Attribute("file").Value;

            using (var logWriter = deploylog.AppendText()) 
                logWriter.WriteLine($"restore-xml-begin: {fpath}");

            XDocument f = XDocument.Load(GetFullPath(fpath));
            List<XElement> remove = new List<XElement>();
            foreach (XElement subitem in item.Elements())
            {
                switch (subitem.Name.LocalName)
                {
                    case "original-value":

                        var xpath = subitem.Attribute("xpath").Value;
                        f.XPathSelectElement(xpath).SetValue(subitem.Value);
                        remove.Add(subitem);

                        using (var logWriter = deploylog.AppendText()) 
                            logWriter.WriteLine($"restore-xml: {xpath} restored to {subitem.Value}");
                        break;
                }
            }

            f.Save(GetFullPath(fpath));

            foreach (XElement el in remove) 
                el.Remove();

            using (var logWriter = deploylog.AppendText()) 
                logWriter.WriteLine($"restore-xml-end: {fpath}");
        }

        private void SaveConfig() => configuration.Document.Save(Deploy.GetDeployConfigFilePath());        

        /// <summary>
        /// Replaces starting $(SpecialFolder) with the physical path.
        /// </summary>
        /// <param name="p"></param>
        /// <returns></returns>
        private static string GetFullPath(string path)
        {
            path = path.Trim();
            if (path.StartsWith("$("))
            {
                int idx = path.IndexOf(')');
                path = Path.Combine(
                    GetFolderPath(path.Substring(2, idx - 2)),
                    //Environment.GetFolderPath((Environment.SpecialFolder)Enum.Parse(typeof(Environment.SpecialFolder), path.Substring(2, idx - 2))),
                    path.Substring(idx + 1).Trim('\\'));
            }
            //(new Shell32.Shell).NameSpace(46).Items.Item.Path
            return path;
        }

        private static void DirectoryCopy(string sourceDirName, string destDirName, bool copySubDirs, bool BackupFiles)
        {
            DirectoryInfo dir = new DirectoryInfo(sourceDirName);
            DirectoryInfo[] dirs = dir.GetDirectories();

            // If the source directory does not exist, throw an exception.
            if (!dir.Exists)
            {
                throw new DirectoryNotFoundException(
                    "Source directory does not exist or could not be found: "
                    + sourceDirName);
            }

            // If the destination directory does not exist, create it.
            if (!Directory.Exists(destDirName))
            {
                Directory.CreateDirectory(destDirName);
            }


            // Get the file contents of the directory to copy.
            FileInfo[] files = dir.GetFiles();

            foreach (FileInfo file in files)
            {
                // Create the path to the new copy of the file.
                string temppath = Path.Combine(destDirName, file.Name);

                // Copy the file.
                file.CopyTo(temppath, false);
            }

            // If copySubDirs is true, copy the subdirectories.
            if (copySubDirs)
            {

                foreach (DirectoryInfo subdir in dirs)
                {
                    // Create the subdirectory.
                    string temppath = Path.Combine(destDirName, subdir.Name);

                    // Copy the subdirectories.
                    DirectoryCopy(subdir.FullName, temppath, copySubDirs, BackupFiles);
                }
            }
        }

        protected void OnPropertyChanged(string name) => PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(name));


        /// <summary>
        /// Returns Special Folder's path using Environment.GetFolderPath(). If SpecialFolderName cannot be resolved (Framework 3.5 has no definition for SpecialFolder.CommonDocuments) it will try to resolved from Environment variable(s)
        /// </summary>
        /// <param name="specialFolderName"></param>
        /// <returns></returns>
        public static string GetFolderPath(string specialFolderName)
        {
            //Environment.GetFolderPath((Environment.SpecialFolder)Enum.Parse(typeof(Environment.SpecialFolder), path.Substring(2, idx - 2)))
            if (Utilities.EnumTryParse(specialFolderName, out Environment.SpecialFolder folder))
                return Environment.GetFolderPath(folder);
            else
            {
                switch (specialFolderName.ToLower())
                {
                    case "commondocuments":
                        if (Environment.OSVersion.Version.Major < 6) // isXP, use %ALLUSERSPROFILE%\Documents
                            return Path.Combine(Environment.GetEnvironmentVariable("ALLUSERSPROFILE"), "Documents");
                        else // isVista/W7/W8, use %PUBLIC%\Documents
                            return Path.Combine(Environment.GetEnvironmentVariable("PUBLIC"), "Documents");
                    default:
                        string path = Environment.GetEnvironmentVariable(specialFolderName);
                        if (Directory.Exists(path))
                            return path;
                        else
                            throw new ArgumentException("Unable to resolve this folder", "SpecialFolderName");
                }
            }
        }
    }

    internal class ServiceProxy : REST.ServiceProxy
    {
        internal void ConvertFromWCFSettings(string wcfConfigPath)
        {
            // if wcfConfigPath exists and rest not confgured, convert server url from wcf config into rest service base address...
            var settingsFilepath = Env.GetConfigFilePath(Env.SettingsFileName);
            if (!File.Exists(settingsFilepath) && File.Exists(wcfConfigPath))
            {
                var doc = XDocument.Load(wcfConfigPath);
                var eps = doc?.Element("configuration")?.Element("system.serviceModel")?.Element("client")?.Elements("endpoint");
                var rc = eps?.FirstOrDefault(ep => ep.Attribute("name").Value == "TDM-Default");
                var adr = rc?.Attribute("address").Value;
                if (!string.IsNullOrEmpty(adr) && adr.EndsWith("/wats-dc/ReportCenter.svc", StringComparison.InvariantCultureIgnoreCase))
                {
                    var svcbase = adr.Substring(0, adr.Length - 25);
                    this.LoadSettings();
                    this._settings.TargetURL = svcbase;
                    this.SaveSettings();
                }
            }
        }
    }
}
