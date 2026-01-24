extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System.Linq;

namespace Virinco.WATS.Interface.MES.Asset
{
    /// <summary>
    /// Common response class for Asset calls
    /// </summary>
    public class AssetResponse
    {
        private napi.Asset.AssetResponse _instance;

        internal AssetResponse(napi.Asset.AssetResponse assetresponse)
        {
            this._instance = assetresponse;
        }

        /// <summary>
        /// Boolean 'status' for allowing use of an asset
        /// </summary>
        public bool Ok
        {
            get => _instance.Ok;
            set => _instance.Ok = value;
        }

        /// <summary>
        /// Asset_Status for an Asset
        /// </summary>
        public Asset_Status Status // r/o
        {
            get => (Asset_Status)(int)_instance.Status;
            //set => _instance.Status = (napi.Asset.Asset_Status)(int)value;
        }

        /// <summary>
        /// Error-message for the AssetResponse.
        /// </summary>
        public string ErrorMessage // r/o
        {
            get => _instance.ErrorMessage;
            //set => _instance.ErrorMessage = value;
        }

        /// <summary>
        /// Returns a AssetStatus message
        /// </summary>
        public string Description // r/o
        {
            get => _instance.Description;
            //set => _instance.Description = value;
        }

        /// <summary>
        /// Read-write instance property for an Asset Object (Get/Set)
        /// </summary>
        public Asset AssetObject
        {
            get { return new Asset(_instance.AssetObject); }
            set { _instance.AssetObject = value._instance; }
        }

        /// <summary>
        /// Read-write instance property for an array of SubAsset Object (Get/Set)
        /// </summary>
        public Asset[] SubAssets
        {
            get { return _instance.SubAssets.Select(i => new Asset(i)).ToArray(); }
            set { _instance.SubAssets = value.Select(i => i._instance).ToArray(); }
        }
    }
}