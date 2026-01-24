extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Misc information attached to an UUR
    /// </summary>
    public class MiscUURInfo
    {
        internal napi.MiscUURInfo _instance;
        internal MiscUURInfo(napi.MiscUURInfo instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// A regular expression will be validated 
        /// </summary>
        public string ValidRegularExpression
        {
            get => _instance.ValidRegularExpression;
        }

        /// <summary>
        /// GUI mask
        /// </summary>
        public string InputMask // r/o
        {
            get => _instance.InputMask;
        }


        /// <summary>
        /// The information description, e.g. SWVer1
        /// </summary>
        public string Description
        {
            get => _instance.Description;
        }

        /// <summary>
        /// The string value of the info, e.g. 1.15.3
        /// </summary>
        public string DataString
        {
            get => _instance.DataString;
            set => _instance.DataString= value;
        }
    }
}

