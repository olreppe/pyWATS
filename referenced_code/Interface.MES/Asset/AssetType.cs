extern alias newclientapi;

using System;
using napi = newclientapi::Virinco.WATS.Interface.MES;

namespace Virinco.WATS.Interface.MES.Asset
{
    /// <summary>
    /// Common AssetType Class
    /// </summary>
    public class AssetType
    {
        internal napi.Asset.AssetType _instance;

        internal AssetType(napi.Asset.AssetType assettype)
        {
            this._instance = assettype;
        }

        /// <summary>
        /// AssetType identity
        /// </summary>
        public Guid TypeId
        {
            get => _instance.TypeId;
            set => _instance.TypeId = value;
        }

        /// <summary>
        /// AssetType name
        /// </summary>
        public string TypeName
        {
            get => _instance.TypeName;
            set => _instance.TypeName = value;
        }

        /// <summary>
        /// Max count until next calibration must be performed (interval)
        /// </summary>
        public int? RunningCountLimit
        {
            get => _instance.RunningCountLimit;
            set => _instance.RunningCountLimit = value;
        }

        /// <summary>
        /// Asset total count limit
        /// </summary>
        public int? TotalCountLimit
        {
            get => _instance.TotalCountLimit;
            set => _instance.TotalCountLimit = value;
        }

        /// <summary>
        /// Interval for maintenance (in days e.g 1.0 or 1.5)
        /// </summary>
        public decimal? MaintenanceInterval
        {
            get => _instance.MaintenanceInterval;
            set => _instance.MaintenanceInterval = value;
        }

        /// <summary>
        /// Interval for calibration (in days e.g 1.0 or 1.5)
        /// </summary>
        public decimal? CalibrationInterval
        {
            get => _instance.CalibrationInterval;
            set => _instance.CalibrationInterval = value;
        }

        /// <summary>
        /// Warning threshold percent
        /// </summary>
        public decimal? WarningThreshold
        {
            get => _instance.WarningThreshold;
            set => _instance.WarningThreshold = value;
        }

        /// <summary>
        /// Alarm threshold percent
        /// </summary>
        public decimal? AlarmThreshold
        {
            get => _instance.AlarmThreshold;
            set => _instance.AlarmThreshold = value;
        }
    }
}