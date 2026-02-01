using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Statistics about an asset from the point in time when the report was submitted to WATS. Only available when getting the report from the server with <see cref="TDM.LoadReport"/>.
    /// </summary>
    public class AssetStatistics    
    {
        private readonly AssetStats_type assetStatsRow;

        private readonly UUTReport report;

        internal AssetStatistics(AssetStats_type assetStatsRow, UUTReport uut)
        {
            report = uut;
            this.assetStatsRow = assetStatsRow;
        }

        /// <summary>
        /// Serial number of the asset.
        /// </summary>
        public string AssetSerialNumber => assetStatsRow.AssetSN;

        /// <summary>
        /// The asset's running count after being used in the test, or <c>null</c> if the asset did not exists when the report was submitted.
        /// </summary>
        public int? RunningCount => assetStatsRow.RunningCountSpecified ? assetStatsRow.RunningCount : (int?)null;

        /// <summary>
        /// How much the asset's running count exceeded the limit by after being used in the test, or <c>null</c> if the asset does not have a running count limit or did not exists when the report was submitted.
        /// Is negative if the count had not exceeded the limit (flip the sign to get remaining).
        /// </summary>
        public int? RunningCountExceeded => assetStatsRow.RunningCountExceededSpecified ? assetStatsRow.RunningCountExceeded : (int?)null;

        /// <summary>
        /// The asset's total count after being used in the test, or <c>null</c> if the asset did not exists when the report was submitted.
        /// </summary>
        public int? TotalCount => assetStatsRow.TotalCountSpecified ? assetStatsRow.TotalCount : (int?)null;

        /// <summary>
        /// How much the asset's total count exceeded the limit by after being used in the test, or <c>null</c> if the asset does not have a total count limit or did not exists when the report was submitted.
        /// Is negative if the count had not exceeded the limit (flip the sign to get remaining).
        /// </summary>
        public int? TotalCountExceeded => assetStatsRow.TotalCountExceededSpecified ? assetStatsRow.TotalCountExceeded : (int?)null;

        /// <summary>
        /// How many days since the asset had been calibrated when being used in the test, or <c>null</c> if the asset had never been calibrated or did not exists when the report was submitted.
        /// </summary>
        public decimal? DaysSinceCalibration => assetStatsRow.DaysSinceCalibrationSpecified ? assetStatsRow.DaysSinceCalibration : (decimal?)null;

        /// <summary>
        /// How many days the asset is overdue a calibration when being used in the test according to the asset's calibration interval, or <c>null</c> if the asset does not have a calibration interval or did not exists when the report was submitted.
        /// Is negative if the interval has not been exceeded (flip the sign to get days remaining).
        /// </summary>
        public decimal? CalibrationDaysOverdue => assetStatsRow.CalibrationDaysOverdueSpecified ? assetStatsRow.CalibrationDaysOverdue : (decimal?)null;

        /// <summary>
        /// How many days since the asset had been maintenance when being used in the test, or <c>null</c> if the asset had never been calibrated or did not exists when the report was submitted.
        /// </summary>
        public decimal? DaysSinceMaintenance => assetStatsRow.DaysSinceMaintenanceSpecified ? assetStatsRow.DaysSinceMaintenance : (decimal?)null;

        /// <summary>
        /// How many days the asset is overdue a maintenance when being used in the test according to the asset's maintenance interval, or <c>null</c> if the asset does not have a maintenance interval or did not exists when the report was submitted.
        /// Is negative if the interval has not been exceeded (flip the sign to get days remaining).
        /// </summary>
        public decimal? MaintenanceDaysOverdue => assetStatsRow.MaintenanceDaysOverdueSpecified ? assetStatsRow.MaintenanceDaysOverdue : (decimal?)null;

        /// <summary>
        /// Message from statistics calculation. Usually set if something went wrong, like the asset not existing.
        /// </summary>
        public string Message => assetStatsRow.Message;
    }
}
