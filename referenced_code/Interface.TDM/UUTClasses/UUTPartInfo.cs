extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Sub part information
    /// </summary>
    public class UUTPartInfo
    {
        internal napi.UUTPartInfo _instance;
        internal UUTPartInfo(napi.UUTPartInfo instance) { _instance = instance; }

        /// <summary>
        /// Type of subpart
        /// </summary>
        public string PartType
        {
            get => _instance.PartType;
            set => _instance.PartType = value;
        }

        /// <summary>
        /// Part number of subpart
        /// </summary>
        public string PartNumber
        {
            get => _instance.PartNumber;
            set => _instance.PartNumber = value;
        }

        /// <summary>
        /// Sub parts serial number
        /// </summary>
        public string SerialNumber
        {
            get => _instance.SerialNumber;
            set => _instance.SerialNumber = value;
        }

        /// <summary>
        /// Sub part revision number
        /// </summary>
        public string PartRevisionNumber
        {
            get => _instance.PartRevisionNumber;
            set => _instance.PartRevisionNumber = value;
        }
    }
}
