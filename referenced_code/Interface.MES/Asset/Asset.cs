extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System.Collections.Generic;
using System;

namespace Virinco.WATS.Interface.MES.Asset
{
    /// <summary>
    /// Class that represent an asset. An asset is normally a device used in testing that can be controlled for service maintenance, running count etc.
    /// </summary>
    public class Asset
    {
        internal napi.Asset.Asset _instance;

        internal Asset(napi.Asset.Asset assetresponse)
        {
            this._instance = assetresponse;
        }
        /// <summary>
        /// Unique asset Id
        /// </summary>
        public string AssetId
        {
            get => _instance.AssetId;
            set => _instance.AssetId = value;
        }

        /// <summary>
        /// Unique serial number
        /// </summary>
        public string SerialNumber
        {
            get => _instance.SerialNumber;
            set => _instance.SerialNumber = value;
        }

        /// <summary>
        /// Identity for an assets parent. Can be null
        /// </summary>
        public string ParentAssetId
        {
            get => _instance.ParentAssetId;
            set => _instance.ParentAssetId = value;
        }

        /// <summary>
        /// Serial number for an assets parent. Can be null
        /// </summary>
        public string ParentSerialNumber
        {
            get => _instance.ParentSerialNumber;
            set => _instance.ParentSerialNumber = value;
        }

        /// <summary>
        /// Alternate name of asset
        /// </summary>
        public string AssetName
        {
            get => _instance.AssetName;
            set => _instance.AssetName = value;
        }

        /// <summary>
        /// Asset part number
        /// </summary>
        public string PartNumber
        {
            get => _instance.PartNumber;
            set => _instance.PartNumber = value;
        }

        /// <summary>
        /// Asset part revision
        /// </summary>
        public string Revision
        {
            get => _instance.Revision;
            set => _instance.Revision = value;
        }

        /// <summary>
        /// Asset description
        /// </summary>
        public string Description
        {
            get => _instance.Description;
            set => _instance.Description = value;
        }

        /// <summary>
        /// Asset location
        /// </summary>
        public string Location
        {
            get => _instance.Location;
            set => _instance.Location = value;
        }

        /// <summary>
        /// Id of asset type
        /// </summary>
        public Guid TypeId
        {
            get => _instance.TypeId;
            set => _instance.TypeId = value;
        }

        /// <summary>
        /// Asset states
        /// </summary>
        public State State
        {
            get { return (State)(int)_instance.State; }
            set { _instance.State = (napi.Asset.State)(int)value; }
        }

        /// <summary>
        /// Type of Asset
        /// </summary>
        public AssetType AssetType
        {
            get { return new AssetType(_instance.AssetType); }
            set { _instance.AssetType = value._instance; }
        }

        /// <summary>
        /// ToString that contains serial number, parent serial number, name, partNumber and state for an asset.
        /// </summary>
        /// <returns></returns>
        public string ToString()
        {
            return $"SerialNumber: {SerialNumber}, ParentSerialNumber: {ParentSerialNumber}, Name:{AssetName}, Partnumber:{PartNumber}, Status: {State}";
        }

        /// <summary>
        /// AssetStatus object.
        /// </summary>
        public AssetStatus AssetStatus
        {
            get { return new AssetStatus(_instance.AssetStatus); }
            set { _instance.AssetStatus = value._instance; }
        }

        /// <summary>
        /// TimeStamp for when the asset was created.
        /// </summary>
        public DateTime FirstSeenDate
        {
            get => _instance.FirstSeenDate;
            set => _instance.FirstSeenDate = value;
        }

        /// <summary>
        /// Timestamp for when the Asset was last seen/used.
        /// </summary>
        public DateTime? LastSeenDate
        {
            get => _instance.LastSeenDate;
            set => _instance.LastSeenDate = value;
        }

        /// <summary>
        /// Timestamp for when the Asset was last maintained
        /// </summary>
        public DateTime? LastMaintenanceDate
        {
            get => _instance.LastMaintenanceDate;
            set => _instance.LastMaintenanceDate = value;
        }

        /// <summary>
        /// Timestamp for when the Asset was last calibrated
        /// </summary>
        public DateTime? LastCalibrationDate
        {
            get => _instance.LastCalibrationDate;
            set => _instance.LastCalibrationDate = value;
        }

        /// <summary>
        /// Total asset usage
        /// </summary>
        public int TotalCount
        {
            get => _instance.TotalCount;
            set => _instance.TotalCount = value;
        }

        /// <summary>
        /// Running count for an instrument between each calibration.
        /// </summary>
        public int RunningCount
        {
            get => _instance.RunningCount;
            set => _instance.RunningCount = value;
        }

        /// <summary>
        /// List of asset tags and their values
        /// </summary>
        public List<KeyValuePair<string, string>> Tags => _instance.Tags;
    }
}