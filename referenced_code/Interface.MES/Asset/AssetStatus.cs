extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;

namespace Virinco.WATS.Interface.MES.Asset
{
    /// <summary>
    /// Common status class for Asset calls
    /// </summary>
    public class AssetStatus
    {
        internal napi.Asset.AssetStatus _instance;

        internal AssetStatus(napi.Asset.AssetStatus assetstatus)
        {
            this._instance = assetstatus;
        }

        /// <summary>
        /// Read-write instance property for an Asset_Status enum type
        /// </summary>
        public Asset_Status Status
        {
            get { return (Asset_Status)(int)_instance.Status; }
            set { _instance.Status = (napi.Asset.Asset_Status)(int)value; }
        }

        /// <summary>
        ///  Read-write instance property for an AssetStatus message.
        /// </summary>
        public string Message
        {
            get => _instance.Message;
            set => _instance.Message = value;
        }

        /// <summary>
        ///  Number of days overdue for a scheduled asset calibration.
        /// </summary>
        public decimal CalibrationDaysOverdue
        {
            get => _instance.CalibrationDaysOverdue;
            set => _instance.CalibrationDaysOverdue = value;
        }

        /// <summary>
        /// Nnumber of days overdue for scheduled asset maintenance.
        /// </summary>
        public decimal MaintenanceDaysOverdue
        {
            get => _instance.MaintenanceDaysOverdue;
            set => _instance.MaintenanceDaysOverdue = value;
        }

        /// <summary>
        /// Asset's Total usage count.
        /// Set property only allows higher values than already stored.
        /// </summary>
        public int TotalCount
        {
            get => _instance.TotalCount;
            set => _instance.TotalCount = value;
        }

        /// <summary>
        /// Total count has exceeded it's limit.
        /// </summary>
        public int TotalCountExceeded
        {
            get => _instance.TotalCountExceeded;
            set => _instance.TotalCountExceeded = value;
        }

        /// <summary>
        /// Number of uses since last calibration
        /// </summary>
        public int RunningCount
        {
            get => _instance.RunningCount;
            set => _instance.RunningCount = value;
        }

        /// <summary>
        /// Number of uses since last calibration, with exceeded limit.
        /// </summary>
        public int RunningCountExceeded
        {
            get => _instance.RunningCountExceeded;
            set => _instance.RunningCountExceeded = value;
        }
    }
}