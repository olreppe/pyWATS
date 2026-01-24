extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represents an asset to track the use of.
    /// </summary>
    public class Asset
    {
        internal napi.Asset _instance;
        internal Asset(napi.Asset instance) { _instance = instance; }
        
        /// <summary>
        /// Serial number of the asset.
        /// </summary>
        public string AssetSerialNumber
        {
            get => _instance.AssetSerialNumber;
            set => _instance.AssetSerialNumber = value;
        }

        /// <summary>
        /// How much the asset was used.
        /// </summary>
        public int UsageCount
        {
            get => _instance.UsageCount;
            set => _instance.UsageCount = value;
        }

        /// <summary>
        /// The number format for the usage count. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string UsageCountFormat
        {
            get => _instance.UsageCountFormat;
            set => _instance.UsageCountFormat = value;
        }
    }
}
