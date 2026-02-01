using System.Collections.ObjectModel;
using System.Xml.Linq;
using System.Linq;
using System.Runtime.Serialization;

namespace Virinco.WATS.Service.MES.Contract
{
    public partial class Package
    {
        string _validation = null;
        [DataMember]
        public string Validation
        {
            get
            {
                return _validation;
            }

            set
            {
                if (_validation != value)
                {
                    _validation = value;
                    OnPropertyChanged("Validation");
                }
            }
        }

        string _validationDescription = null;
        [DataMember]
        public string ValidationDescription
        {
            get
            {
                return _validationDescription;
            }

            set
            {
                if (_validationDescription != value)
                {
                    _validationDescription = value;
                    OnPropertyChanged("ValidationDescription");
                }
            }
        }


        bool _isExpanded = false;
        public bool IsExpanded
        {
            get
            {
                return _isExpanded;
            }

            set
            {
                if (_isExpanded != value)
                {
                    _isExpanded = value;
                    OnPropertyChanged("IsExpanded");
                }
            }
        }

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

        public bool ReadOnly
        {
            get
            {
                return Status != (int)StatusEnum.Draft || (AccessDenied.HasValue && AccessDenied.Value);
            }
        }

        /// <summary>
        /// Set to true if RestrictedContent=true and user doesn't have permission
        /// </summary>
        private bool? AccessDenied { get; set; }

        [DataMember]
        public bool IsRestricted { get; set; }

        public bool HasAccess(bool HasRestrictedAccess)
        {
            AccessDenied = (IsRestricted && !HasRestrictedAccess);
            return !AccessDenied.Value;
        }

        /// <summary>
        /// Number of bytes needed to download the package. 
        /// A file will not be downloaded if an unmodified file already exists on the file system. 
        /// </summary>
        public long? DownloadSize { get; set; }

        /// <summary>
        /// New available version of the package. 
        ///  
        /// </summary>
        public int? AvailableVersion { get; set; }

        private ObservableCollection<Tag> _packageTags;
        public ObservableCollection<Tag> PackageTags
        {
            get
            {
                if (_packageTags == null)
                {
                    _packageTags = new ObservableCollection<Tag>();

                    if (!string.IsNullOrEmpty(Tags))
                    {
                        XDocument tags = XDocument.Parse(Tags, LoadOptions.PreserveWhitespace);
                        if (tags.Root != null)
                        {
                            var items = from tag in tags.Root.Descendants()
                                        select new Tag() { Name = tag.Name.LocalName, Value = tag.Value };
                            _packageTags = new ObservableCollection<Tag>(items);


                            foreach (Tag tag in _packageTags)
                            {
                                tag.MarkAsUnchanged();
                                tag.StartTracking();
                                tag.ChangeTracker.ObjectStateChanging += ChangeTracker_ObjectStateChanging;

                            }

                        }
                    }
                    _packageTags.CollectionChanged += new System.Collections.Specialized.NotifyCollectionChangedEventHandler(_packageTags_CollectionChanged);
                }

                return _packageTags;
            }
            set { _packageTags = value; OnPropertyChanged("PackageTags"); }
        }


        void ChangeTracker_ObjectStateChanging(object sender, ObjectStateChangingEventArgs e)
        {
            if (e.NewState == ObjectState.Modified)
                UpdateTagXml();
            else if (e.NewState == ObjectState.Deleted)
                ((Tag)sender).ChangeTracker.ObjectStateChanging -= ChangeTracker_ObjectStateChanging;
            else if (e.NewState == ObjectState.Added)
                ((Tag)sender).ChangeTracker.ObjectStateChanging += ChangeTracker_ObjectStateChanging;
        }

        void _packageTags_CollectionChanged(object sender, System.Collections.Specialized.NotifyCollectionChangedEventArgs e)
        {
            UpdateTagXml();
            foreach (Tag tag in _packageTags)
            {
                tag.MarkAsUnchanged();
                tag.StartTracking();
                tag.ChangeTracker.ObjectStateChanging -= ChangeTracker_ObjectStateChanging;
                tag.ChangeTracker.ObjectStateChanging += ChangeTracker_ObjectStateChanging;
            }
        }



        /// <summary>
        /// Update Tags xml with values from the PackageTags collection
        /// </summary>
        public void UpdateTagXml()
        {
            XDocument xdoc = new XDocument(new XElement("PackageInfo"));
            foreach (Tag item in PackageTags)
            {
                XElement el = new XElement(XName.Get(item.Name));
                el.Value = item.Value;
                xdoc.Root.Add(el);
            }
            Tags = xdoc.ToString();
        }
    }
}