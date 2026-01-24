using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using Virinco.WATS.Client.Configurator.SupportFiles;
using System.Collections.ObjectModel;
using System.Xml.Linq;
using System.IO.Compression;
using System.Runtime.Versioning;

namespace Virinco.WATS.Client.Configurator.Pages
{
    public class LabViewToolkitViewModel : Helpers.ObservableObject, IPageViewModel
    {
        [SupportedOSPlatform("windows")]
        public LabViewToolkitViewModel(ConfigViewModel config)
        {
            this.Config = config;

            var labViews = GetLabViews();
            foreach(var labView in labViews)
            {
                if (labView.Installed)
                    LabViews.Add(labView);
            }            
        }

        [SupportedOSPlatform("windows")]
        public static IEnumerable<LabView> GetLabViews()
        {
            const string tdmSourceFile = @"WATS TDM - LabVIEW Toolkit.zip";
            const string tdmDestinationPath = @"vi.lib\addons\WATS TDM - LabVIEW Toolkit\";

            const string mesSourceFile = @"WATS MES.zip";
            const string mesDestinationPath = @"vi.lib\addons\WATS MES\";

            var labViews = new[]
            {
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\12.0", "LabVIEW 2012 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\12.0", "LabVIEW 2012 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\13.0", "LabVIEW 2013 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\13.0", "LabVIEW 2013 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\14.0", "LabVIEW 2014 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\14.0", "LabVIEW 2014 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\15.0", "LabVIEW 2015 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\15.0", "LabVIEW 2015 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\16.0", "LabVIEW 2016 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\16.0", "LabVIEW 2016 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\17.0", "LabVIEW 2017 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\17.0", "LabVIEW 2017 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\18.0", "LabVIEW 2018 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\18.0", "LabVIEW 2018 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\19.0", "LabVIEW 2019 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\19.0", "LabVIEW 2019 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\20.0", "LabVIEW 2020 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                //new LabView(@"SOFTWARE\National Instruments\LabVIEW\20.0", "LabVIEW 2020 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\21.0", "LabVIEW 2021 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\21.0", "LabVIEW 2021 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\22.0", "LabVIEW 2022 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\22.0", "LabVIEW 2022 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\23.0", "LabVIEW 2023 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\23.0", "LabVIEW 2023 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\24.0", "LabVIEW 2024 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\24.0", "LabVIEW 2024 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\25.0", "LabVIEW 2025 32-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, true, false),
                new LabView(@"SOFTWARE\National Instruments\LabVIEW\25.0", "LabVIEW 2025 64-bit", tdmSourceFile, tdmDestinationPath, mesSourceFile, mesDestinationPath, false, true),
            };

            SaveLabViewState(labViews);

            return labViews;
        }

        [SupportedOSPlatform("windows")]
        public static void SaveLabViewState(LabView labView)
        {
            SaveLabViewState(new[] { labView });
        }

        [SupportedOSPlatform("windows")]
        public static void SaveLabViewState(IEnumerable<LabView> labViews)
        {
            try
            {
                var deployFilePath = Deploy.GetDeployConfigFilePath();
                if (File.Exists(deployFilePath))
                {
                    var xDeploy = XDocument.Load(deployFilePath);
                    var xLabViews = xDeploy.Root.Elements(Deploy.xmlns + "LabView");

                    foreach (var labView in labViews)
                    {
                        var xLabView = xLabViews.SingleOrDefault(e => e.Attribute("Id").Value == labView.Id);
                        if (xLabView == null)
                        {
                            xLabView = new XElement(Deploy.xmlns + "LabView",
                                new XAttribute("Id", labView.Id),
                                new XAttribute("Name", ""),
                                new XAttribute("Version", ""),
                                new XAttribute("State", ""));
                            xDeploy.Root.Add(xLabView);
                        }

                        xLabView.Attribute("Name").SetValue(labView.ProductName);
                        xLabView.Attribute("Version").SetValue(labView.Version);
                        xLabView.Attribute("State").SetValue(GetState(labView).ToString());
                    }

                    xDeploy.Save(deployFilePath);
                }
            }
            catch (Exception e)
            {
                Env.LogException(e, "Failed to save LabView state");
            }

            Product.ProductState GetState(LabView labView)
            {
                if (!labView.Installed)
                    return Product.ProductState.Not_found;
                if (!labView.Deployed)
                    return Product.ProductState.Not_installed;
                else
                    return Product.ProductState.Installed;
            }
        }

        public string Name
        {
            get { return "LabViewToolkit"; }
        }

        public ConfigViewModel Config { get; set; }


        ObservableCollection<LabView> _labViews;
        public ObservableCollection<LabView> LabViews
        {
            get
            {
                if (_labViews == null) _labViews = new System.Collections.ObjectModel.ObservableCollection<LabView>();
                return _labViews;
            }
            set
            {
                if (_labViews != value)
                {
                    _labViews = value;
                    this.RaisePropertyChanged("LabViews");
                }
            }
        }

        public LabView SelectedLabView { get; set; }

        public class LabView : Helpers.ObservableObject
        {
            public string Id { get; }

            public string Version { get; }

            public bool Installed { get; }

            public bool Deployed
            {
                get { return deployed; }
                set
                {
                    if (deployed != value)
                    {
                        deployed = value;
                        RaisePropertyChanged("Deployed");
                    }
                }
            }

            public string ProductName { get; set; }

            private bool deployed = false;

            private readonly string rootPath;
            private readonly string tdmSourceArchive;
            private readonly string mesSourceArchive;
            private readonly string tdmDestinationPath;
            private readonly string mesDestinationPath;

            public LabView(string regKey, string productName, string tdmSource, string tdmDestination, string mesSource, string mesDestination, bool x86, bool x64)
            {
                Id = regKey;
                rootPath = getRegKey(regKey, "Path", x86, x64);
                if (!string.IsNullOrEmpty(rootPath))
                    Installed = Directory.Exists(rootPath);

                ProductName = productName;//getRegKey(regKey, "ProductName", x86, x64) + (x86 ? " 32-bit" : " 64-bit");
                Version = regKey.Substring(regKey.LastIndexOf('\\') + 1);

                string supportFilesRoot = SupportFiles.Deploy.GetSupportFilesRoot();
                tdmSourceArchive = Path.Combine(supportFilesRoot, tdmSource);
                mesSourceArchive = Path.Combine(supportFilesRoot, mesSource);

                tdmDestinationPath = Path.Combine(rootPath, tdmDestination);
                mesDestinationPath = Path.Combine(rootPath, mesDestination);

                Deployed = Directory.Exists(tdmDestinationPath) || Directory.Exists(mesDestinationPath);
            }

            public bool DeployFiles(bool suppressMessageBox = false)
            {
                try 
                { 
                    if (suppressMessageBox || System.Windows.MessageBox.Show("Please ensure that LabView is closed.", "Confirm Application Closed", System.Windows.MessageBoxButton.OKCancel) == System.Windows.MessageBoxResult.OK)
                    {
                        DeployArchive(tdmSourceArchive, tdmDestinationPath);
                        DeployArchive(mesSourceArchive, mesDestinationPath);

                        if (!suppressMessageBox)
                            System.Windows.Forms.MessageBox.Show("Succesfully installed WATS Add-on for LabView", "LabViewintegration completed", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Information);

                        SaveLabViewState(this);
                        return true;
                    }
                }
                catch (Exception ex)
                {
                    if (!suppressMessageBox)
                        System.Windows.Forms.MessageBox.Show(ex.Message, "WATS LabVIEW ToolKit integration failed", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
                }

                return false;
            }

            private void DeployArchive(string source, string destination)
            {
                using var zipOnDisk = File.Open(source, FileMode.Open, FileAccess.Read); //Test!
                DeleteFolderContents(destination);

                var zip = new ZipArchive(zipOnDisk);
                zip.ExtractToDirectory(destination, true);

                Deployed = true;

                //Microsoft.Deployment.Compression.Zip.ZipInfo zi = new Microsoft.Deployment.Compression.Zip.ZipInfo(source);                   
                //DeleteFolderContents(destination);
                //zi.Unpack(destination);
                //Deployed = true;                           
            }
            [SupportedOSPlatform("windows")]
            public void UnDeployFiles()
            {
                try
                {
                    if (System.Windows.Forms.DialogResult.OK == System.Windows.Forms.MessageBox.Show("WATS LabVIEW ToolKit folder is going to be removed.\r\n" + tdmDestinationPath, "Confirm removal", System.Windows.Forms.MessageBoxButtons.OKCancel, System.Windows.Forms.MessageBoxIcon.Question))
                    {
                        if (Directory.Exists(tdmDestinationPath))
                            Directory.Delete(tdmDestinationPath, true);

                        if (Directory.Exists(mesDestinationPath))
                            Directory.Delete(mesDestinationPath, true);

                        Deployed = false;
                        SaveLabViewState(this);
                    }
                }
                catch (Exception ex)
                {
                    System.Windows.Forms.MessageBox.Show(ex.Message, "WATS LabVIEW ToolKit removal failed", System.Windows.Forms.MessageBoxButtons.OK, System.Windows.Forms.MessageBoxIcon.Error);
                }
            }

            private void DeleteFolderContents(string folderPath)
            {
                DirectoryInfo root = new DirectoryInfo(folderPath);
                if (!root.Exists) return;
                DirectoryInfo[] dirs = root.GetDirectories("*", SearchOption.AllDirectories);
                foreach (DirectoryInfo di in dirs.Reverse())
                {
                    foreach (FileInfo fi in di.GetFiles())
                    {
                        try { fi.Delete(); }
                        catch { } // dont care, just continue...
                    }
                    try { di.Delete(); }
                    catch { } // dont care, just continue...
                }
            }

            public static void CopyAll(DirectoryInfo source, DirectoryInfo target)
            {
                foreach (DirectoryInfo dir in source.GetDirectories())
                    CopyAll(dir, target.CreateSubdirectory(dir.Name));
                foreach (FileInfo file in source.GetFiles())
                    file.CopyTo(Path.Combine(target.FullName, file.Name), true);
            }

            [SupportedOSPlatform("windows")]
            private string getRegKey(string regkey, string keyName, bool x86, bool x64)
            {
                string regValue;

                if (x86 && Registry.TryReadHKLM32Value(regkey, keyName, out regValue) && !string.IsNullOrEmpty(regValue))
                    return regValue;
                else if (x64 && Registry.ProcessType == Registry.ProcessTypeEnum.w32on32) //32-bit OS, do not search for 64-bit installation.
                    return string.Empty;
                else if (x64 && Registry.TryReadHKLM64Value(regkey, keyName, out regValue) && !string.IsNullOrEmpty(regValue)) 
                    return regValue;
                else return string.Empty;
            }
        }
    }
}