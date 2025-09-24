using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Virinco.Newtonsoft.Json;

namespace Virinco.WATS.Interface.Models
{
    /// <summary>
    /// Return value of <see cref="TDM.FindReportHeaders(string, int, int, string, string, string)"/>.
    /// </summary>
    public class ReportHeader
    {
        /// <summary>     
        /// Report id. Can be used in order by     
        /// </summary>
        [JsonProperty("uuid")]
        public Guid UUID { get; set; }

        /// <summary>
        /// Report serial number. Can be using in order by
        /// </summary>
        [JsonProperty("serialNumber")]
        public string SerialNumber { get; set; }

        /// <summary>
        /// Report part number
        /// </summary>
        [JsonProperty("partNumber")]
        public string PartNumber { get; set; }

        /// <summary>
        /// Report type.T = UUT, R = UUR
        /// </summary>
        [JsonProperty("reportType")]
        public string ReportType { get; set; }

        /// <summary>
        /// Report start time. In format yyyy-MM-ddTHH:mm:ssZ. Default order by descending
        /// </summary>
        [JsonProperty("start")]
        public DateTimeOffset Start { get; set; }

        /// <summary>
        /// Report revision
        /// </summary>
        [JsonProperty("revision")]
        public string Revision { get; set; }

        /// <summary>
        /// Report result. Passed, Failed, Error, or Terminated
        /// </summary>
        [JsonProperty("result")]
        public string Result { get; set; }

        /// <summary>
        /// Report batch number
        /// </summary>
        [JsonProperty("batchNumber")]
        public string BatchNumber { get; set; }

        /// <summary>
        /// Report operator
        /// </summary>  
        [JsonProperty("userName")]
        public string UserName { get; set; }

        /// <summary>
        /// Test station name.
        /// </summary>
        [JsonProperty("stationName")]
        public string StationName { get; set; }

        /// <summary>
        /// Test station location
        /// </summary>
        [JsonProperty("location")]
        public string Location { get; set; }

        /// <summary>
        /// Test station purpose.
        /// </summary>
        [JsonProperty("purpose")]
        public string Purpose { get; set; }

        /// <summary>
        /// 
        /// </summary>
        [JsonProperty("measuresDeleted")]
        public bool MeasuresDeleted { get; set; }

        /// <summary>
        /// Report processing order. Does not represent time, instead is an incrementing number used as processing order. Can be used in order by
        /// </summary>
        [JsonProperty("timeStamp")]
        public long TimeStamp { get; set; }

        /// <summary>
        /// Report test/repair operation code
        /// </summary>
        [JsonProperty("processCode")]
        public short ProcessCode { get; set; }

        /// <summary>
        /// Report test/repair operation name
        /// </summary>
        [JsonProperty("processName")]
        public string ProcessName { get; set; }

        /// <summary>
        /// Report comment
        /// </summary>
        [JsonProperty("comment")]
        public string Comment { get; set; }

        /// <summary>
        /// Report execution time. Available from 2022.2
        /// </summary>
        [JsonProperty("executionTime")]
        public double? ExecutionTime { get; set; }

        /// <summary>
        /// Report test software filename. Available from 2022.2
        /// </summary>
        [JsonProperty("swFilename")]
        public string SwFilename { get; set; }

        /// <summary>
        /// Report test software version. Available from 2022.2
        /// </summary>
        [JsonProperty("swVersion")]
        public string SwVersion { get; set; }

        /// <summary>
        /// Report test socket index. Available from 2022.2
        /// </summary>
        [JsonProperty("testSocketIndex")]
        public short? TestSocketIndex { get; set; }

        /// <summary>
        /// Report fixture id. Available from 2022.2
        /// </summary>
        [JsonProperty("fixtureId")]
        public string FixtureId { get; set; }

        /// <summary>
        /// Report error code. Available from 2022.2
        /// </summary>
        [JsonProperty("errorCode")]
        public int? ErrorCode { get; set; }

        /// <summary>
        /// Report error message. Available from 2022.2
        /// </summary>
        [JsonProperty("errorMessage")]
        public string ErrorMessage { get; set; }

        /// <summary>
        /// Report test run number (same serial number in same test operation). Available from 2022.2
        /// </summary>
        [JsonProperty("run")]
        public int? Run { get; set; }

        /// <summary>
        /// Report receive count. Available from 2022.2
        /// </summary>
        [JsonProperty("receiveCount")]
        public int? ReceiveCount { get; set; }

        /// <summary>
        /// Report size in KB. Available from 2022.2
        /// </summary>
        [JsonProperty("reportSize")]
        public int? ReportSize { get; set; }

        /// <summary>
        /// Step name that caused the report to fail. Available from 2022.2
        /// </summary>
        [JsonProperty("causedUutFailure")]
        public string CausedUutFailure { get; set; }

        /// <summary>
        /// Step path that caused the report to fail. Available from 2022.2
        /// </summary>
        [JsonProperty("causedUutFailurePath")]
        public string CausedUutFailurePath { get; set; }

        /// <summary>
        /// Run number the report first passed in. Available from 2022.2
        /// </summary>
        [JsonProperty("passedInRun")]
        public int? PassedInRun { get; set; }

        /// <summary>
        /// Repair report referencing a test report. Available from 2022.2
        /// </summary>
        [JsonProperty("referencedUut")]
        public Guid? ReferencedUut { get; set; }

        /// <summary>
        /// UUT sub units. Must be expanded. Available from 2022.2
        /// </summary>
        [JsonProperty("subUnits")]
        public List<Subunit> SubUnits { get; set; }

        /// <summary>
        /// UUT miscellaneous info. Must be expanded. Available from 2022.2
        /// </summary>
        [JsonProperty("miscInfo")]
        public List<Miscinfo> MiscInfo { get; set; }

        /// <summary>
        /// UUT asset info. Must be expanded. Available from 2022.2
        /// </summary>
        [JsonProperty("assets")]
        public List<Asset> Assets { get; set; }

        /// <summary>
        /// UUT attachments. Must be expanded. Available from 2022.2
        /// </summary>
        [JsonProperty("attachments")]
        public List<Attachment> Attachments { get; set; }

        /// <summary>
        /// UUR sub units. Must be expanded. Available from 2022.2
        /// </summary>
        [JsonProperty("uurSubUnits")]
        public List<UURSubunit> UurSubUnits { get; set; }

        /// <summary>
        /// UUR miscellaneous info. Must be expanded. Available from 2022.2
        /// </summary>
        [JsonProperty("uurMiscInfo")]
        public List<UURMiscinfo> UurMiscInfo { get; set; }

        /// <summary>
        /// UUR attachments. Must be expanded. Available from 2022.2
        /// </summary>
        [JsonProperty("uurAttachments")]
        public List<UURAttachment> UurAttachments { get; set; }
    }
    
    public class Subunit
    {
        /// <summary>
        /// Sub unit part type. Available from 2022.2
        /// </summary>
        [JsonProperty("partType")]
        public string PartType { get; set; }

        /// <summary>
        /// Sub unit serial number. Available from 2022.2
        /// </summary>
        [JsonProperty("serialNumber")]
        public string SerialNumber { get; set; }

        /// <summary>
        /// Sub unit part number. Available from 2022.2
        /// </summary>
        [JsonProperty("partNumber")]
        public string PartNumber { get; set; }

        /// <summary>
        /// Sub unit revision. Available from 2022.2
        /// </summary>
        [JsonProperty("revision")]
        public string Revision { get; set; }
    }

    public class Miscinfo
    {

        /// <summary>
        /// Misc info description/name. Available from 2022.2
        /// </summary>
        [JsonProperty("description")]
        public string Description { get; set; }

        /// <summary>
        /// Misc info string value. Available from 2022.2
        /// </summary>
        [JsonProperty("value")]
        public string Value { get; set; }
    }

    public class Asset
    {
        /// <summary>
        /// Asset serial number. Available from 2022.2
        /// </summary>
        [JsonProperty("serialNumber")]
        public string SerialNumber { get; set; }

        /// <summary>
        /// Asset running count when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("runningCount")]
        public int? RunningCount { get; set; }

        /// <summary>        
        /// Asset running count limit execeeded by when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("runningCountExceeded")]
        public int? RunningCountExceeded { get; set; }

        /// <summary>
        /// Asset total count when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("totalCount")]
        public int? TotalCount { get; set; }

        /// <summary>
        /// Asset total count limit execeeded when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("totalCountExceeded")]
        public int? TotalCountExceeded { get; set; }

        /// <summary>
        /// Days since previous asset maintenance when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("daysSinceMaintenance")]
        public decimal? DaysSinceMaintenance { get; set; }

        /// <summary>
        /// Days overdue asset maintenance limit when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("maintenanceDaysOverdue")]
        public decimal? MaintenanceDaysOverdue { get; set; }

        /// <summary>
        /// Days since previous asset calibration when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("daysSinceCalibration")]
        public decimal? DaysSinceCalibration { get; set; }

        /// <summary>
        /// Days overdue asset calibration limit when report was processed. Available from 2022.2
        /// </summary>
        [JsonProperty("calibrationDaysOverdue")]
        public decimal? CalibrationDaysOverdue { get; set; }
    }
    
    public class Attachment
    {
        /// <summary>
        /// Attachment filename. Available from 2022.2
        /// </summary>
        [JsonProperty("filename")]
        public string Filename { get; set; }
    }

    public class UURSubunit
    {
        /// <summary>
        /// Sub unit serial number. Available from 2022.2
        /// </summary>
        [JsonProperty("serialNumber")]
        public string SerialNumber { get; set; }

        /// <summary>
        /// Sub unit part number. Available from 2022.2
        /// </summary>
        [JsonProperty("partNumber")]
        public string PartNumber { get; set; }

        /// <summary>
        /// Sub unit revision. Available from 2022.2
        /// </summary>
        [JsonProperty("revision")]
        public string Revision { get; set; }
    }

    public class UURMiscinfo
    {
        /// <summary>
        /// Misc info description/name. Available from 2022.2
        /// </summary>
        [JsonProperty("description")]
        public string Description { get; set; }

        /// <summary>
        /// Misc info string value. Available from 2022.2
        /// </summary>
        [JsonProperty("value")]
        public string Value { get; set; }
    }
    public class UURAttachment
    {
        /// <summary>
        /// Attachment id. Available from 2022.2
        /// </summary>
        [JsonProperty("id")]
        public Guid? ID { get; set; }

        /// <summary>
        /// Attachment filename. Available from 2022.2
        /// </summary>
        [JsonProperty("filename")]
        public string Filename { get; set; }
    }
}
