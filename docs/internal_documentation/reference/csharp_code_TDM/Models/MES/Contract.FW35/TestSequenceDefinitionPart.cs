using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Service.MES.Contract
{
    public partial class TestSequenceDefinition
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

        bool _hasRelationWarning = false;
        public bool HasRelationWarning
        {
            get
            {
                return _hasRelationWarning;
            }

            set
            {
                if (_hasRelationWarning != value)
                {
                    _hasRelationWarning = value;
                    OnPropertyChanged("HasRelationWarning");
                }
            }
        }

        ObservableCollection<TestSequenceDefinition> _relationWarningObjects;
        public ObservableCollection<TestSequenceDefinition> RelationWarningObjects
        {
            get
            {
                if (_relationWarningObjects == null)
                    _relationWarningObjects = new ObservableCollection<TestSequenceDefinition>();
                return _relationWarningObjects;
            }

            set
            {
                if (_relationWarningObjects != value)
                {
                    _relationWarningObjects = value;
                    OnPropertyChanged("RelationWarningObjects");
                }
            }
        }

        private bool _readOnly;
        public bool ReadOnly
        {
            get
            {
                return _readOnly || Status == (int)StatusEnum.Released || Status == (int)StatusEnum.Pending;
            }
            set
            {
                if (_readOnly != value)
                {
                    _readOnly = value;
                    OnPropertyChanged("ReadOnly");
                }
            }
        }

        public string NameAndVersion
        {
            get
            {
                return string.Format("{0} v{1}", Name, Version);
            }
        }
    }
}
