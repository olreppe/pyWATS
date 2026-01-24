using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Xml.Linq;
using Virinco.WATS;
using Virinco.WATS.Interface.MES.Software;
using Virinco.WATS.Service.MES.Contract;
using Virinco.WATS.Client.PackageManager.Converters;
using Virinco.WATS.REST;

namespace Virinco.WATS.Client.PackageManager
{
    public class MainViewModel : ObservableObject
    {
        #region Binding properties

        public int SelectedTab 
        {
            get => selectedTab;
            set
            {
                selectedTab = value;
                OnPropertyChanged(nameof(SelectedTab));
            }
        }

        public bool IsRefreshEnabled 
        {
            get => isRefreshEnabled;
            private set
            {
                isRefreshEnabled = value;
                OnPropertyChanged(nameof(IsRefreshEnabled));
            }
        }

        public bool IsInstallEnabled
        {
            get => isInstallEnabled;
            private set
            {
                isInstallEnabled = value;
                OnPropertyChanged(nameof(IsInstallEnabled));
            }
        }

        public bool IsConfigurationEnabled
        {
            get => isConfigurationEnabled;
            private set
            {
                isConfigurationEnabled = value;
                OnPropertyChanged(nameof(IsConfigurationEnabled));
            }
        }

        public bool IsSelectingAvailablePackagesEnabled
        {
            get => isSelectingAvailablePackagesEnabled;
            private set
            {
                isSelectingAvailablePackagesEnabled = value;
                OnPropertyChanged(nameof(IsSelectingAvailablePackagesEnabled));
            }
        }

        public bool IsSelectingInstalledPackagesEnabled
        {
            get => isSelectingInstalledPackagesEnabled;
            private set
            {
                isSelectingInstalledPackagesEnabled = value;
                OnPropertyChanged(nameof(IsSelectingInstalledPackagesEnabled));
            }
        }

        public string TotalSelectedText
        {
            get => totalSelectedText;
            private set
            {
                totalSelectedText = value;
                OnPropertyChanged(nameof(TotalSelectedText));
            }
        }

        public long? TotalSize 
        {
            get => totalSize;
            private set
            {
                totalSize = value;
                OnPropertyChanged(nameof(TotalSize));
            }
        }

        public bool IsAvailablePackagesHeaderChecked 
        {
            get => isAvailablePackagesHeaderChecked;
            set
            {
                isAvailablePackagesHeaderChecked = value;
                SelectAll(AvailablePackages, value);
                OnPropertyChanged(nameof(IsAvailablePackagesHeaderChecked));
            }
        }

        public bool IsInstalledPackagesHeaderChecked
        {
            get => isInstalledPackagesHeaderChecked;
            set
            {
                isInstalledPackagesHeaderChecked = value;
                SelectAll(AvailablePackages, value);
                OnPropertyChanged(nameof(IsInstalledPackagesHeaderChecked));
            }
        }

        public Visibility NoAvailablePackagesTextVisibility 
        {
            get => noAvailablePackagesTextVisibility;
            private set
            {
                noAvailablePackagesTextVisibility = value;
                OnPropertyChanged(nameof(NoAvailablePackagesTextVisibility));
            }
        }

        public Visibility NoInstalledPackagesTextVisibility
        {
            get => noInstalledPackagesTextVisibility;
            private set
            {
                noInstalledPackagesTextVisibility = value;
                OnPropertyChanged(nameof(NoInstalledPackagesTextVisibility));
            }
        }

        #region Binding fields

        private bool isRefreshEnabled = true;

        private bool isInstallEnabled = true;

        private bool isConfigurationEnabled = true;

        private bool isSelectingAvailablePackagesEnabled = true;

        private bool isSelectingInstalledPackagesEnabled = true;

        private string totalSelectedText = noSelectedPackagesText;

        private bool isAvailablePackagesHeaderChecked = false;

        private bool isInstalledPackagesHeaderChecked = false;

        private bool cascadingSelectEnabled = true;

        private long? totalSize = null;

        private Visibility noAvailablePackagesTextVisibility = Visibility.Collapsed;

        private Visibility noInstalledPackagesTextVisibility = Visibility.Collapsed;

        private int selectedTab = 0;

        #endregion

        #endregion

        public event EventHandler PackagesUpdated;

        public ObservableCollection<SelectableItem<Package>> AvailablePackages { get; } = new ObservableCollection<SelectableItem<Package>>();

        public ObservableCollection<StatusItem<Package>> InstalledPackages { get; } = new ObservableCollection<StatusItem<Package>>();

        private Software mes;

        private readonly FileSystemWatcher settingsWatcher;

        private bool checkingForPackages;

        private DateTime lastChecked = DateTime.UtcNow;

        private const string noSelectedPackagesText = "No packages selected";

        private readonly string installedPackagesXml = Env.GetConfigFilePath(Env.InstalledPackagesFileName);

        private Task timerTask;

        private CancellationTokenSource cancellationTokenSource;

        public MainViewModel()
        {
            isConfigurationEnabled = Utils.AllowConfiguration;
            mes = new Software();
            settingsWatcher = new FileSystemWatcher(Env.DataDir, Env.SettingsFileName)
            {
                IncludeSubdirectories = false,
                NotifyFilter = NotifyFilters.LastWrite
            };
            settingsWatcher.Changed += (s, e) => RefreshWATSConfig();
            settingsWatcher.EnableRaisingEvents = true;
        }

        public void StartTimer()
        {
            if (cancellationTokenSource != null && timerTask != null)
                throw new InvalidOperationException("Timer already started");

            cancellationTokenSource = new CancellationTokenSource();
            timerTask = CheckPackagesTimer(cancellationTokenSource.Token);
        }

        public async Task StopTimer()
        {
            if(cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
            {
                cancellationTokenSource.Cancel();
                await timerTask;

                timerTask = null;
                cancellationTokenSource = null;
            }
        }

        private async Task CheckPackagesTimer(CancellationToken cancellationToken)
        {
            int checkInterval = Utils.CheckInterval * 1000;
            while (!cancellationToken.IsCancellationRequested)
            {
                //Packages are default selected. Updating the list removes any unselection.
                if ((DateTime.UtcNow - lastChecked).TotalMinutes > 30 && AvailablePackages.All(p => p.IsSelected))
                    await CheckForPackages();

                try
                {
                    await Task.Delay(checkInterval, cancellationToken);
                }
                catch { }
            }
        }

        private void SelectAll<T>(IEnumerable<SelectableItem<T>> items, bool select)
        {
            if (cascadingSelectEnabled)
            {
                cascadingSelectEnabled = false;

                foreach (var selectable in items)
                    selectable.IsSelected = select;

                UpdateTotalSelected();

                cascadingSelectEnabled = true;
            }
        }

        private void UpdateTotalSelected()
        {
            var selectedPackages = AvailablePackages.Where(p => p.IsSelected);
            if (!selectedPackages.Any())
            {
                TotalSelectedText = noSelectedPackagesText;
                IsInstallEnabled = false;
            }            
            else
            {
                int count = selectedPackages.Count();

                string package = "package";
                if (count > 1)
                    package += 's';

                TotalSelectedText = $"{count} {package} selected, {selectedPackages.Sum(p => p.Item.DownloadSize).Value.FormatBytes()}";
                IsInstallEnabled = true;
            }
        }

        public async Task CheckForPackages()
        {
            try
            {
                checkingForPackages = true;

                Env.Trace.TraceInformation("Package Manager is checking for packages.");
                Console.WriteLine("Checking for packages");

                lastChecked = DateTime.UtcNow;

                IsRefreshEnabled = false;
                IsConfigurationEnabled = false;
                IsInstallEnabled = false;
                IsSelectingAvailablePackagesEnabled = false;
                IsSelectingInstalledPackagesEnabled = false;

                await Task.Delay(500);

                string xpath = Utils.getXpath();
                Package[] packages = mes.GetPackagesByTag(xpath, out _, out _, false, false, true, (StatusEnum)Utils.PackageStatus);

                XDocument installedPackagesXDocument;
                IEnumerable<Package> installedPackages;
                if (File.Exists(installedPackagesXml))
                {
                    installedPackagesXDocument = XDocument.Load(installedPackagesXml);
                    installedPackages = installedPackagesXDocument.Descendants("Package")
                        .Where(e => e.Attribute("Installed")?.Value?.ToLower() == bool.TrueString.ToLower())
                        .OrderBy(e => e.Attribute("Name").Value)
                        .Select(e => new Package
                        {
                            Name = e.Attribute("Name")?.Value,
                            Version = Utilities.ParseInt32(e.Attribute("Version")?.Value, 0),
                            PackageId = new Guid(e.Attribute("PackageId")?.Value),
                            DownloadSize = Utilities.ParseInt32(e.Attribute("DownloadSize")?.Value, 0) == 0 ? (long?)null : Utilities.ParseInt32(e.Attribute("DownloadSize")?.Value, 0),
                            AvailableVersion = e.Attribute("AvailableVersion") == null ? (int?)null : Utilities.ParseInt32(e.Attribute("AvailableVersion").Value, 0),
                            Description = e.Attribute("Description")?.Value
                        });
                }
                else
                {
                    installedPackages = Enumerable.Empty<Package>();
                    installedPackagesXDocument = new XDocument();
                }

                InstalledPackages.Clear();
                foreach (var package in installedPackages)
                {
                    var status = PackageStatus.None;
                    if (package.DownloadSize > 0)
                        status = PackageStatus.Warning;
                    if (package.AvailableVersion > 0)
                        status = PackageStatus.NewVersionAvailable;

                    InstalledPackages.Add(new StatusItem<Package>(package, status));
                } 

                if (packages != null)
                {
                    foreach(var selectableItem in AvailablePackages)
                        selectableItem.PropertyChanged -= AvailablePackagePropertyChanged;

                    AvailablePackages.Clear();

                    var availablePackages = packages.Where(p => p.DownloadSize > 0 || (installedPackagesXDocument.Descendants("Package").Any(e => e.Attribute("PackageId").Value == p.PackageId.ToString() && e.Attribute("Installed")?.Value?.ToLower() == bool.FalseString.ToLower())));
                    if(availablePackages.Count() > 0)
                    {
                        foreach (var package in availablePackages)
                        {
                            var selectablePackage = new SelectableItem<Package>(package);
                            selectablePackage.PropertyChanged += AvailablePackagePropertyChanged;

                            AvailablePackages.Add(selectablePackage);
                        }
                    }
                }
                
                Env.Trace.TraceInformation("Package Manager checking for packages completed.");
            }
            catch (Exception e)
            {
                Env.LogException(e, "Package Manager checking for packages failed.");
            }
            finally
            {
                IsRefreshEnabled = true;
                IsConfigurationEnabled = Utils.AllowConfiguration;
                IsSelectingAvailablePackagesEnabled = true;
                IsSelectingInstalledPackagesEnabled = true;

                if (AvailablePackages.Count > 0)
                {
                    IsAvailablePackagesHeaderChecked = true;
                    TotalSize = AvailablePackages.Sum(p => p.Item.DownloadSize);
                    NoAvailablePackagesTextVisibility = Visibility.Collapsed;
                }
                else
                {
                    IsAvailablePackagesHeaderChecked = false;
                    TotalSize = null;
                    NoAvailablePackagesTextVisibility = Visibility.Visible;
                }

                if (InstalledPackages.Count > 0)
                    NoInstalledPackagesTextVisibility = Visibility.Collapsed;
                else
                    NoInstalledPackagesTextVisibility = Visibility.Visible;

                checkingForPackages = false;
                PackagesUpdated?.Invoke(this, new EventArgs());
            }
        }

        public async Task InstallPackages()
        {
            IsRefreshEnabled = false;
            IsInstallEnabled = false;

            var selectedPackages = AvailablePackages.Where(i => i.IsSelected).Select(i => i.Item);

            if (Utils.DeleteRevokedPackages)
                mes.DeleteRevokedPackages(false);

            mes.InstallPackage(selectedPackages.ToArray(), true, true);

            await CheckForPackages();

            IsRefreshEnabled = true;
        }

        private void AvailablePackagePropertyChanged(object sender, PropertyChangedEventArgs e)
        {
            var selectabelItem = (SelectableItem<Package>)sender;

            if (cascadingSelectEnabled)
            {
                cascadingSelectEnabled = false;

                if (e.PropertyName == nameof(selectabelItem.IsSelected) && !selectabelItem.IsSelected)                
                        IsAvailablePackagesHeaderChecked = false;

                UpdateTotalSelected();

                cascadingSelectEnabled = true;
            }
        }

        private void RefreshWATSConfig()
        {
            if (checkingForPackages)
                PackagesUpdated += DelayedRefresh;
            else
            {
                mes = new Software();
                ServiceProxy.GetMACAddress(false);
            }
            
            void DelayedRefresh(object sender, EventArgs e)
            {
                PackagesUpdated -= DelayedRefresh;
                mes = new Software();
                ServiceProxy.GetMACAddress(false);
            }
        }
    }
}
