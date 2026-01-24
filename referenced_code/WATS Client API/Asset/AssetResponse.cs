namespace Virinco.WATS.Interface.MES.Asset
{
    /// <summary>
    /// Common response class for Asset calls
    /// </summary>
    public class AssetResponse
    {
        /// <summary>
        /// String errorMessage used to provide feedback to the operator
        /// </summary>
        internal string _errorMessage;

        /// <summary>
        /// Boolean 'status' for allowing use of an asset
        /// </summary>
        public bool Ok { get; set; } = true;

        /// <summary>
        /// Asset_Status for an Asset
        /// </summary>
        public Asset_Status Status
        {
            get { return AssetObject?.AssetStatus?.Status ?? Asset_Status.NotRegistered; }
        }

        /// <summary>
        /// Error-message for the AssetResponse.
        /// </summary>
        public string ErrorMessage
        {
            get { return _errorMessage; }
        }

        /// <summary>
        /// Returns a AssetStatus message
        /// </summary>
        public string Description { get { return AssetObject?.AssetStatus?.Message ?? ""; } }

        /// <summary>
        /// Read-write instance property for an Asset Object (Get/Set)
        /// </summary>
        public Asset AssetObject { get; set; }

        /// <summary>
        /// Read-write instance property for an array of SubAsset Object (Get/Set)
        /// </summary>
        public Asset[] SubAssets { get; set; }

        /// <summary>
        /// Sets Asset_Status and provides an errorMessage.
        /// Asset_Status.Error is used if Asset_Status  is not specified.
        /// </summary>
        /// <param name="errorMessage">String errorMessage</param>
        /// <param name="asset_Status">Asset_Status enum, default = Error</param>
        internal void SetError(string errorMessage, Asset_Status asset_Status = Asset_Status.AssetError)
        {
            AssetObject = new Asset()
            {
                AssetStatus = new AssetStatus()
                {
                    Status = asset_Status
                }
            };
            _errorMessage = errorMessage;
            Ok = false;
        }

        /// <summary>
        /// Sets the status of an Asset to OK
        /// </summary>
        /// <param name="asset">Specified Asset object</param>
        internal void SetOK(Asset asset)
        {
            _errorMessage = null;
            AssetObject = asset;
            Ok = true;
        }
    }
}