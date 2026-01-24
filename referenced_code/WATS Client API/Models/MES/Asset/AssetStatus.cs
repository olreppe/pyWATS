//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;

//namespace Virinco.WATS.Interface.MES.Asset
//{
//    /// <summary>
//    /// Common status class for Asset calls
//    /// </summary>
//    public class AssetStatus
//    {
//        /// <summary>
//        /// Read-write instance property for an Asset_Status enum type
//        /// </summary>
//        public Asset_Status Status { get; set; }

//        /// <summary>
//        ///  Read-write instance property for an AssetStatus message.
//        /// </summary>
//        public string Message { get; set; }

//        /// <summary>
//        ///  Number of days overdue for a scheduled asset calibration.
//        /// </summary>
//        public decimal CalibrationDaysOverdue { get; set; }

//        /// <summary>
//        /// Nnumber of days overdue for scheduled asset maintenance.
//        /// </summary>
//        public decimal MaintenanceDaysOverdue { get; set; }

//        /// <summary>
//        /// Asset's Total usage count.
//        /// Set property only allows higher values than already stored.
//        /// </summary>
//        public int TotalCount { get; set; }

//        /// <summary>
//        /// Total count has exceeded it's limit.
//        /// </summary>
//        public int TotalCountExceeded { get; set; }

//        /// <summary>
//        /// Number of uses since last calibration
//        /// </summary>
//        public int RunningCount { get; set; }

//        /// <summary>
//        /// Number of uses since last calibration, with exceeded limit.
//        /// </summary>
//        public int RunningCountExceeded { get; set; }
//    }
//}