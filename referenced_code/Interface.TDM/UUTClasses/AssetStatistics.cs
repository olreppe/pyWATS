extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Statistics about an asset from the point in time when the report was submitted to WATS. Only available when getting the report from the server with <see cref="TDM.LoadReport"/>.
    /// </summary>
    public class AssetStatistics
    {
        internal napi.AssetStatistics _instance;
        internal AssetStatistics(napi.AssetStatistics instance) { _instance = instance; }

        /// <summary>
        /// Serial number of the asset.
        /// </summary>
        public string AssetSerialNumber // r/o
        {
            get => _instance.AssetSerialNumber;
            //set => _instance.AssetSerialNumber = value;
        } // r/o

        /// <summary>
        /// The asset's running count after being used in the test, or <c>null</c> if the asset did not exists when the report was submitted.
        /// </summary>
        public int? RunningCount // r/o
        {
            get => _instance.RunningCount;
            //set => _instance.RunningCount = value;
        } // r/o

        /// <summary>
        /// How much the asset's running count exceeded the limit by after being used in the test, or <c>null</c> if the asset does not have a running count limit or did not exists when the report was submitted.
        /// Is negative if the count had not exceeded the limit (flip the sign to get remaining).
        /// </summary>
        public int? RunningCountExceeded // r/o
        {
            get => _instance.RunningCountExceeded;
            //set => _instance.RunningCountExceeded = value;
        } // r/o

        /// <summary>
        /// The asset's total count after being used in the test, or <c>null</c> if the asset did not exists when the report was submitted.
        /// </summary>
        public int? TotalCount // r/o
        {
            get => _instance.TotalCount;
            //set => _instance.TotalCount = value;
        } // r/o

        /// <summary>
        /// How much the asset's total count exceeded the limit by after being used in the test, or <c>null</c> if the asset does not have a total count limit or did not exists when the report was submitted.
        /// Is negative if the count had not exceeded the limit (flip the sign to get remaining).
        /// </summary>
        public int? TotalCountExceeded // r/o
        {
            get => _instance.TotalCountExceeded;
            //set => _instance.TotalCountExceeded = value;
        } // r/o

        /// <summary>
        /// How many days since the asset had been calibrated when being used in the test, or <c>null</c> if the asset had never been calibrated or did not exists when the report was submitted.
        /// </summary>
        public decimal? DaysSinceCalibration // r/o
        {
            get => _instance.DaysSinceCalibration;
            //set => _instance.DaysSinceCalibration = value;
        } // r/o

        /// <summary>
        /// How many days the asset is overdue a calibration when being used in the test according to the asset's calibration interval, or <c>null</c> if the asset does not have a calibration interval or did not exists when the report was submitted.
        /// Is negative if the interval has not been exceeded (flip the sign to get days remaining).
        /// </summary>
        public decimal? CalibrationDaysOverdue // r/o
        {
            get => _instance.CalibrationDaysOverdue;
            //set => _instance.CalibrationDaysOverdue = value;
        } // r/o

        /// <summary>
        /// How many days since the asset had been maintenance when being used in the test, or <c>null</c> if the asset had never been calibrated or did not exists when the report was submitted.
        /// </summary>
        public decimal? DaysSinceMaintenance // r/o
        {
            get => _instance.DaysSinceMaintenance;
            //set => _instance.DaysSinceMaintenance = value;
        } // r/o

        /// <summary>
        /// How many days the asset is overdue a maintenance when being used in the test according to the asset's maintenance interval, or <c>null</c> if the asset does not have a maintenance interval or did not exists when the report was submitted.
        /// Is negative if the interval has not been exceeded (flip the sign to get days remaining).
        /// </summary>
        public decimal? MaintenanceDaysOverdue // r/o
        {
            get => _instance.MaintenanceDaysOverdue;
            //set => _instance.MaintenanceDaysOverdue = value;
        } // r/o

        /// <summary>
        /// Message from statistics calculation. Usually set if something went wrong, like the asset not existing.
        /// </summary>
        public string Message // r/o
        {
            get => _instance.Message;
            //set => _instance.Message = value;
        } // r/o
    }
}
