using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Virinco.WATS.Service.MES.Contract;

namespace Virinco.WATS.Client.PackageManager
{
    public class ConfigurationViewModel : ObservableObject
    {
        public IReadOnlyCollection<KeyValuePair<int, string>> Intervals { get; }

        public IReadOnlyCollection<KeyValuePair<int, string>> Statuses { get; }

        public int SelectedInterval 
        {
            get => selectedInterval;
            set
            {
                selectedInterval = value;
                OnPropertyChanged(nameof(SelectedInterval));
            }
        }

        public int SelectedStatus
        {
            get => selectedStatus;
            set
            {
                selectedStatus = value;
                OnPropertyChanged(nameof(SelectedStatus));
            }
        }

        public bool BringToFront 
        {
            get => bringToFront;
            set
            {
                bringToFront = value;
                OnPropertyChanged(nameof(BringToFront));
            }
        }

        public string Filter 
        {
            get => filter;
            set
            {
                filter = value;
                OnPropertyChanged(nameof(Filter));
            }
        }

        public string XPath 
        {
            get => xPath;
            set
            {
                xPath = value;
                OnPropertyChanged(nameof(XPath));
            }
        }

        private int selectedInterval = Utils.CheckInterval;

        private int selectedStatus = Utils.PackageStatus;

        private bool bringToFront = Utils.BringToFront;

        private string filter;

        private string xPath = "Generated XPath";

        public ConfigurationViewModel()
        {
            Intervals = new Dictionary<int, string>
            {
                { 1800, "30 minutes" },
                { 3600, "1 hour" },
                { 21600, "6 hours" },
                { 42300, "12 hours" },
                { 86400, "24 hours" }
            };

            Statuses = new Dictionary<int, string>
            {
                { (int)StatusEnum.Draft, StatusEnum.Draft.ToString() },
                { (int)StatusEnum.Pending, StatusEnum.Pending.ToString() },
                { (int)StatusEnum.Released, StatusEnum.Released.ToString() },
                { (int)StatusEnum.Revoked, StatusEnum.Revoked.ToString() }
            };

            string filter = Utils.getFilter();
            this.filter = filter;
            xPath = Utils.getXpath(filter);
        }

        public void SaveConfiguration()
        {
            Utils.CheckInterval = SelectedInterval;
            Utils.PackageStatus = SelectedStatus;
            Utils.BringToFront = BringToFront;           
            Utils.saveFilter(Filter);
        }
    }
}
