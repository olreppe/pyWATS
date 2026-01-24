using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS.Client.PackageManager
{
    public class SelectableItem<T> : ObservableObject
    {
        public T Item { get; }

        public bool IsSelected
        {
            get => isSelected;
            set
            {
                isSelected = value;
                OnPropertyChanged(nameof(IsSelected));
            }
        }

        private bool isSelected;

        public SelectableItem(T item)
            : this(item, false) { }

        public SelectableItem(T item, bool isSelected)
        {
            Item = item;
            this.isSelected = isSelected;
        }
    }
}
