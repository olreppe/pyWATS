using System.Collections.ObjectModel;
using System.Xml.Linq;
using System.Linq;

namespace Virinco.WATS.Service.MES.Contract
{
    public partial class Process
    {
        bool _isModified = false;
        public bool IsModified
        {
            get
            {
                return _isModified;
            }

            set
            {
                if (_isModified != value)
                {
                    _isModified = value;
                    OnPropertyChanged("IsModified");
                }
            }
        }

    }
}