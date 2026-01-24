using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS.Client.PackageManager
{
    public class StatusItem<T> : ObservableObject
    {
        public T Item { get; }

        public PackageStatus Status
        {
            get => status;
            set
            {
                status = value;
                OnPropertyChanged(nameof(Status));
            }
        }

        private PackageStatus status;

        public StatusItem(T item)
            : this(item, PackageStatus.None) { }

        public StatusItem(T item, PackageStatus status)
        {
            Item = item;
            this.status = status;
        }
    }

    public enum PackageStatus
    {
        None = 0,
        Warning,
        NewVersionAvailable
    }
}
