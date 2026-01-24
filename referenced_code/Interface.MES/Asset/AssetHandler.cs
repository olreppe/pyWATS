extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System;

namespace Virinco.WATS.Interface.MES.Asset
{
    /// <summary>
    /// Class that contains functions for Asset handling.
    /// </summary>
    public class AssetHandler : MesBase
    {
        private napi.Asset.AssetHandler _instance;

        internal AssetHandler(napi.Asset.AssetHandler assethandler)
        {
            this._instance = assethandler;
        }


        /// <summary>
        /// True if connected to server.
        /// </summary>
        /// <returns></returns>
        public new bool isConnected() => _instance.isConnected();

        /// <summary>
        /// Creates an Asset of specified type.
        /// </summary>
        /// <param name="serialNumber">Asset serial number</param>
        /// <param name="assetType">Asset type</param>
        /// <param name="parentAssetSerialNumber">Optional. Serial number of the parent asset. If blank, the new asset will have no parent</param>
        /// <param name="assetName">Optional. Asset name</param>
        /// <param name="assetDescription">Optional Asset description</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse CreateAsset(string serialNumber, string assetType, string parentAssetSerialNumber = null, string assetName = null, string assetDescription = null)
            => new AssetResponse(_instance.CreateAsset(serialNumber, assetType, parentAssetSerialNumber, assetName, assetDescription));
        /// <summary>
        /// Creates an Asset Type.
        /// </summary>
        /// <param name="name">Name of the type. Must be unique.</param>
        /// <param name="calibrationInterval">How often assets of this type must be calibrated in days (e.g 1.0 or 1.5).</param>
        /// <param name="maintenanceInterval">How often assets of this type must be maintained in days (e.g 1.0 or 1.5).</param>
        /// <param name="runningCountLimit">Max number of uses before the next calibration of the asset must be performed.</param>
        /// <param name="totalCountLimit">Max number of uses of the asset in its lifetime.</param>
        /// <param name="warningThreshold">How close to the limits an asset can be before a warning is issued (0-100)./param>
        /// <param name="alarmTreshold">How close to the limits an asset can be before an alarm is issued (0-100).</param>
        /// <returns></returns>
        public AssetResponse CreateAssetType(string name, decimal? calibrationInterval = null, decimal? maintenanceInterval = null, int? runningCountLimit = null, int? totalCountLimit = null, decimal? warningThreshold = null, decimal? alarmTreshold = null)
            => new AssetResponse(_instance.CreateAssetType(name, calibrationInterval, maintenanceInterval, totalCountLimit, totalCountLimit, warningThreshold, alarmTreshold));

        /// <summary>
        /// Fetches a specific asset.
        /// </summary>
        /// <param name="serialNumber">Asset serial number</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse GetAsset(string serialNumber)
            => new AssetResponse(_instance.GetAsset(serialNumber));

        /// <summary>
        /// Updates asset object changes.
        /// </summary>
        /// <param name="asset">Asset object to be updated</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse UpdateAsset(Asset asset)
            => new AssetResponse(_instance.UpdateAsset(asset._instance));

        /// <summary>
        /// Sets, updates or remove an asset's parent.
        /// </summary>
        /// <param name="serialNumber">Asset serial number for the asset whose parent will be set.</param>
        /// <param name="parentSerialNumber">New parent serialNumber for the asset (can be null).</param>
        /// <returns>AssetResponse object (with the asset's parent serial number set)</returns>
        public AssetResponse SetParent(string serialNumber, string parentSerialNumber)
            => new AssetResponse(_instance.SetParent(serialNumber, parentSerialNumber));

        /// <summary>
        /// Increment an asset's usage count by default (1) or specified int value.
        /// </summary>
        /// <param name="serialNumber">Asset serial number</param>
        /// <param name="usageCount">Value of usage count increment (default 1)</param>
        /// <param name="incrementSubAssets">Boolean with default=false. Set to true if you want to increment the asset's sub-assets.</param>
        /// <returns>AssetResponse object (with the incremented asset)</returns>
        public AssetResponse IncrementAssetUsageCount(string serialNumber, int usageCount = 1, bool incrementSubAssets = false)
            => new AssetResponse(_instance.IncrementAssetUsageCount(serialNumber, usageCount, incrementSubAssets));

        /// <summary>
        /// Fetches all assets, filtered by a specified OData (REST) filter.
        /// </summary>
        /// <param name="filter">OData filter (syntax example: ($"startswith(serialNumber,'{Prefix}')"). NB! Uses camel casing.</param>
        /// <returns>AssetResponse object with filtered assets in SubAssets property</returns>
        public AssetResponse GetAssets(string filter)
            => new AssetResponse(_instance.GetAssets(filter));

        /// <summary>
        /// Fetches all assets, filtered by tag.
        /// </summary>
        /// <param name="tag">Name of tag.</param>
        /// <returns>AssetResponse object with filtered assets in SubAssets property</returns>
        public AssetResponse GetAssetsByTag(string tag)
            => new AssetResponse(_instance.GetAssetsByTag(tag));

        /// <summary>
        /// Fetches all sub assets of a parent asset.
        /// </summary>
        /// <param name="serialNumber">Parent asset serial number</param>
        /// <returns>AssetResponse object (with sub-assets)</returns>
        public AssetResponse GetSubAssets(string serialNumber)
            => new AssetResponse(_instance.GetSubAssets(serialNumber));

        /// <summary>
        /// Fetches sub assets of a parent asset down to and including level.
        /// </summary>
        /// <param name="serialNumber">Parent asset serial number</param>
        /// <param name="level">How many sub assets of sub assets to get. 0 to get all, 1 to get direct children only.</param>
        /// <returns>AssetResponse object (with sub-assets)</returns>
        public AssetResponse GetSubAssets(string serialNumber, int level)
            => new AssetResponse(_instance.GetSubAssets(serialNumber, level));

        /// <summary>
        /// Register calibration to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Calibration asset's serial number.</param>
        /// <param name="dateTime">If specified, sets the LastCalibrationDate to the specified date and time. Default = null (today).</param>
        /// <param name="comment">Asset log comment.</param>
        /// <returns>AssetResponse object (with the calibrated asset).</returns>
        public AssetResponse Calibration(string serialNumber, DateTime? dateTime = null, string comment = null)
            => new AssetResponse(_instance.Calibration(serialNumber, dateTime, comment));

        /// <summary>
        /// Register calibration to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Calibration asset's serial number.</param>
        /// <param name="dateTime">Sets the LastCalibrationDate to the specified date and time.</param>
        /// <param name="comment">Asset log comment.</param>
        /// <returns>AssetResponse object (with the calibrated asset)</returns>
        public AssetResponse Calibration(string serialNumber, DateTime dateTime, string comment)
            => new AssetResponse(_instance.Calibration(serialNumber, dateTime, comment));

        /// <summary>
        /// Register maintenance to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Maintenance asset serialNumber.</param>
        /// <param name="dateTime">If specified, sets the LastMaintenanceDate to the specified date and time. Default = null (today).</param>
        /// <param name="comment">Asset log comment.</param>
        /// <returns>AssetResponse Object (with the maintenanced asset).</returns>
        public AssetResponse Maintenance(string serialNumber, DateTime? dateTime = null, string comment = null)
            => new AssetResponse(_instance.Maintenance(serialNumber, dateTime, comment));

        /// <summary>
        /// Register maintenance to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Maintenance asset serialNumber</param>
        /// <param name="dateTime">Sets the LastMaintenanceDate to the specified date and time.</param>
        /// <param name="comment">Asset log comment</param>
        /// <returns>AssetResponse Object (with the maintenanced asset)</returns>
        public AssetResponse Maintenance(string serialNumber, DateTime dateTime, string comment)
            => new AssetResponse(_instance.Maintenance(serialNumber, dateTime, comment));

        /// <summary>
        /// Reset running count to 0.
        /// </summary>
        /// <param name="serialNumber">Maintenance asset serialNumber</param>
        /// <param name="comment">Asset log comment</param>
        /// <returns>AssetResponse Object (with the reset asset)</returns>
        public AssetResponse ResetRunningCount(string serialNumber, string comment = null)
            => new AssetResponse(_instance.ResetRunningCount(serialNumber, comment));

        /// <summary>
        /// Deletes the specified asset.
        /// Sub-assets will be updated to no longer contain have a parent.
        /// Client must have admin credentials to delete an asset.
        /// </summary>
        /// <param name="serialNumber">Delete asset serial number</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse DeleteAsset(string serialNumber)
            => new AssetResponse(_instance.DeleteAsset(serialNumber));
    }
}