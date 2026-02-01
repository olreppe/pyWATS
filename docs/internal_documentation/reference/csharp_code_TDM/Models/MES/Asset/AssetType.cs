//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;

//namespace Virinco.WATS.Interface.MES.Asset
//{
//    /// <summary>
//    /// Common AssetType Class
//    /// </summary>
//    public class AssetType
//    {
//        /// <summary>
//        /// AssetType identity
//        /// </summary>
//        public Guid TypeId { get; set; }

//        /// <summary>
//        /// AssetType name
//        /// </summary>
//        public string TypeName { get; set; }

//        /// <summary>
//        /// Max count until next calibration must be performed (interval)
//        /// </summary>
//        public int? RunningCountLimit { get; set; }

//        /// <summary>
//        /// Asset total count limit
//        /// </summary>
//        public int? TotalCountLimit { get; set; }

//        /// <summary>
//        /// Interval for maintenance (in days e.g 1.0 or 1.5)
//        /// </summary>
//        public decimal? MaintenanceInterval { get; set; }

//        /// <summary>
//        /// Interval for calibration (in days e.g 1.0 or 1.5)
//        /// </summary>
//        public decimal? CalibrationInterval { get; set; }

//        /// <summary>
//        /// Warning threshold percent
//        /// </summary>
//        public decimal? WarningThreshold { get; set; }

//        /// <summary>
//        /// Alarm threshold percent
//        /// </summary>
//        public decimal? AlarmThreshold { get; set; }
//    }
//}