using Newtonsoft.Json;
using System;
using System.Collections.Generic;

namespace Virinco.WATS.Schemas.WSJF
{
    public class Report
    {
        /// <summary>
        /// Report type, valid values: T,R (Test, Repair).
        /// </summary>
        [JsonProperty("type")]
        public char ReportType { get; set; }

        /// <summary>
        /// Report unique identifier (Guid).
        /// </summary>
        [JsonProperty("id")]
        public Guid ReportId { get; set; }

        /// <summary>
        /// Part number of the unit.
        /// </summary>
        [JsonProperty("pn")]
        public string PartNumber { get; set; }

        /// <summary>
        /// Serial number of the unit.
        /// </summary>
        [JsonProperty("sn")]
        public string SerialNumber { get; set; }

        /// <summary>
        /// Revision number of the unit.
        /// </summary>
        [JsonProperty("rev")]
        public string Revision { get; set; }

        /// <summary>
        /// Product name of the unit.
        /// </summary>
        [JsonProperty("productName")]
        public string ProductName { get; set; }

        /// <summary>
        /// Process code of the report.
        /// </summary>
        [JsonProperty("processCode")]
        public short? ProcessCode { get; set; }

        /// <summary>
        /// Number format of process code.
        /// </summary>
        [JsonProperty("processCodeFormat")]
        public string ProcessCodeFormat { get; set; }

        /// <summary>
        /// Name of process of the report.
        /// </summary>
        [JsonProperty("processName")]
        public string ProcessName { get; set; }

        /// <summary>
        /// Status code, valid values: P,F,E,T (Passed, Failed, Error, Terminated).
        /// </summary>
        [JsonProperty("result")]
        public char Result { get; set; }

        /// <summary>
        /// Station's machine name.
        /// </summary>
        [JsonProperty("machineName")]
        public string MachineName { get; set; }

        /// <summary>
        /// Station's location.
        /// </summary>
        [JsonProperty("location")]
        public string Location { get; set; }

        /// <summary>
        /// Station's purpose.
        /// </summary>
        [JsonProperty("purpose")]
        public string Purpose { get; set; }

        /// <summary>
        /// The client or user the report belongs to.
        /// </summary>
        [JsonProperty("origin")]
        public string Origin { get; set; }

        /// <summary>
        /// Report start date/time in local timezone.
        /// </summary>
        [JsonProperty("start")]
        public DateTimeOffset Start { get; set; }

        /// <summary>
        /// Report start date/time in utc timezone.
        /// </summary>
        [JsonProperty("startUTC")]
        public DateTime StartUTC { get; set; }

        /// <summary>
        /// Report root step (only valid in test).
        /// </summary>
        [JsonProperty("root", NullValueHandling = NullValueHandling.Ignore)]
        public Step RootStep { get; set; }

        /// <summary>
        /// UUT additional headerinfo.
        /// </summary>
        [JsonProperty("uut", NullValueHandling = NullValueHandling.Ignore)]
        public UUT UUTHeader { get; set; }

        /// <summary>
        /// UUR additional headerinfo.
        /// </summary>
        [JsonProperty("uur", NullValueHandling = NullValueHandling.Ignore)]
        public UUR UURHeader { get; set; }

        /// <summary>
        /// List of misc-infos.
        /// </summary>
        [JsonProperty("miscInfos")]
        public IEnumerable<MiscInfo> MiscInfos { get; set; }

        /// <summary>
        /// List of subunits.
        /// Can also be specified a hierachy (currently used only in repairs) using parent relation.
        /// </summary>
        [JsonProperty("subUnits")]
        public IEnumerable<SubUnit> SubUnits { get; set; }

        /// <summary>
        /// List of assets used in test.
        /// </summary>
        [JsonProperty("assets", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<Asset> Assets { get; set; }

        /// <summary>
        /// List of stats for assets used in test.
        /// </summary>
        [JsonProperty("assetStats", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<AssetStats> AssetStats { get; set; }

        /// <summary>
        /// List of attachments on main unit (only valid for repair).
        /// </summary>
        [JsonProperty("binaryData", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<BinaryData> BinaryData { get; set; }

        /// <summary>
        /// List of additional header data.
        /// </summary>
        [JsonProperty("additionalData", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<AdditionalData> AdditionalData { get; set; }
    }

    public class UUT
    {
        /// <summary>
        /// Execution time of the report.
        /// </summary>
        [JsonProperty("execTime")]
        public double? ExecutionTime { get; set; }

        /// <summary>
        /// Numeric format of execution time.
        /// </summary>
        [JsonProperty("execTimeFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string ExecutionTimeFormat { get; set; }

        /// <summary>
        /// Index of socket used in test.
        /// </summary>
        [JsonProperty("testSocketIndex")]
        public short? TestSocketIndex { get; set; }

        /// <summary>
        /// Numeric format of test socket index.
        /// </summary>
        [JsonProperty("testSocketIndexFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string TestSocketIndexFormat { get; set; }

        /// <summary>
        /// Serial number of batch the report belongs to.
        /// </summary>
        [JsonProperty("batchSN")]
        public string BatchSN { get; set; }

        /// <summary>
        /// Comment of the report.
        /// </summary>
        [JsonProperty("comment")]
        public string Comment { get; set; }

        /// <summary>
        /// Error code of the report.
        /// </summary>
        [JsonProperty("errorCode")]
        public int? ErrorCode { get; set; }

        /// <summary>
        /// Numeric format of error code.
        /// </summary>
        [JsonProperty("errorCodeFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string ErrorCodeFormat { get; set; }

        /// <summary>
        /// Error message of the report.
        /// </summary>
        [JsonProperty("errorMessage")]
        public string ErrorMessage { get; set; }

        /// <summary>
        /// Id of fixture used in report.
        /// </summary>
        [JsonProperty("fixtureId")]
        public string FixtureId { get; set; }

        /// <summary>
        /// Name of test operator.
        /// </summary>
        [JsonProperty("user")]
        public string UserName { get; set; }

        /// <summary>
        /// Batch fail count.
        /// </summary>
        [JsonProperty("batchFailCount")]
        public int? BatchFailCount { get; set; }

        /// <summary>
        /// Numeric format of batch fail count.
        /// </summary>
        [JsonProperty("batchFailCountFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string BatchFailCountFormat { get; set; }

        /// <summary>
        /// Batch loop index.
        /// </summary>
        [JsonProperty("batchLoopIndex")]
        public int? BatchLoopIndex { get; set; }

        /// <summary>
        /// Numeric format of batch loop index.
        /// </summary>
        [JsonProperty("batchLoopIndexFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string BatchLoopIndexFormat { get; set; }

        /// <summary>
        /// Id of step that caused uut failure.
        /// </summary>
        [JsonProperty("stepIdCausedUUTFailure")]
        public int? StepIdCausedUUTFailure { get; set; }

        /// <summary>
        /// Repair reports that reference this test report.
        /// </summary>
        [JsonProperty("refUURs", NullValueHandling = NullValueHandling.Ignore)]
        public List<ReferencedByUUR> ReferencedByUURs { get; set; }
    }

    public class UUR
    {
        /// <summary>
        /// Comment of the report.
        /// </summary>
        [JsonProperty("comment")]
        public string Comment { get; set; }

        /// <summary>
        /// Name of repair operator.
        /// </summary>
        [JsonProperty("user")]
        public string UserName { get; set; }

        /// <summary>
        /// Referenced UUT process code.
        /// </summary>
        [JsonProperty("processCode")]
        public short ProcessCode { get; set; }

        /// <summary>
        /// Numeric format of UUT process code.
        /// </summary>
        [JsonProperty("processCodeFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string ProcessCodeFormat { get; set; }

        /// <summary>
        /// Referenced UUT process code.
        /// </summary>
        [JsonProperty("processName")]
        public string ProcessName { get; set; }

        /// <summary>
        /// Referenced UUT id.
        /// </summary>
        [JsonProperty("refUUT")]
        public Guid? ReferencedUUT { get; set; }

        /// <summary>
        /// Confirm date/time of repair.
        /// </summary>
        [JsonProperty("confirmDate")]
        public DateTime? ConfirmDate { get; set; }

        /// <summary>
        /// Finalize date/time of repair.
        /// </summary>
        [JsonProperty("finalizeDate")]
        public DateTime? FinalizeDate { get; set; }

        /// <summary>
        /// Execution time of repair.
        /// </summary>
        [JsonProperty("execTime")]
        public double? ExecutionTime { get; set; }

        /// <summary>
        /// Id of parent repair report. If set, this report will be considered a sub-repair report.
        /// </summary>
        [JsonProperty("parent")]
        public Guid? Parent { get; set; }

        /// <summary>
        /// Ids of sub repair reports.
        /// </summary>
        [JsonProperty("children")]
        public IEnumerable<Guid> Children { get; set; }
    }

    public class Step
    {
        /// <summary>
        /// StepID = "step order number". Runtime index of step. Also used as unique step identifier within a report.
        /// </summary>
        [JsonProperty("id")]
        public int? StepId { get; set; }

        /// <summary>
        /// Step group, valid values: S,M,C (Setup, Main, Cleanup).
        /// </summary>
        [JsonProperty("group")]
        public char Group { get; set; }

        /// <summary>
        /// Step type, textual description of step.
        /// </summary>
        [JsonProperty("stepType")]
        public string StepType { get; set; }

        /// <summary>
        /// Interactive exe number of step.
        /// </summary>
        [JsonProperty("interactiveExeNum", NullValueHandling = NullValueHandling.Ignore)]
        public int? InteractiveExeNum { get; set; }

        /// <summary>
        /// Numeric format of interactive exe number.
        /// </summary>
        [JsonProperty("interactiveExeNumFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string InteractiveExeNumFormat { get; set; }

        /// <summary>
        /// Step loop info.
        /// </summary>
        [JsonProperty("loop", NullValueHandling = NullValueHandling.Ignore)]
        public LoopInfo Loop { get; set; }

        /// <summary>
        /// Step name.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Start date/time of step (with utc offset).
        /// </summary>
        [JsonProperty("start", NullValueHandling = NullValueHandling.Ignore)]
        public DateTimeOffset? Start { get; set; }

        /// <summary>
        /// Step status, valid values: P,F,D,S,E,T,U (Passed, Failed, Done, Skipped, Error, Terminated, Unknown). 
        /// </summary>
        [JsonProperty("status")]
        public char Status { get; set; }

        /// <summary>
        /// Step error code.
        /// </summary>
        [JsonProperty("errorCode", NullValueHandling = NullValueHandling.Ignore)]
        public int? ErrorCode { get; set; }

        /// <summary>
        /// Numeric format of error code.
        /// </summary>
        [JsonProperty("errorCodeFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string ErrorCodeFormat { get; set; }

        /// <summary>
        /// Step error message.
        /// </summary>
        [JsonProperty("errorMessage", NullValueHandling = NullValueHandling.Ignore)]
        public string ErrorMessage { get; set; }

        /// <summary>
        /// TestStand identifier (Format: #TS:<id>).
        /// </summary>
        [JsonProperty("tsGuid", NullValueHandling = NullValueHandling.Ignore)]
        public string TSGuid { get; set; }

        /// <summary>
        /// Total time of step.
        /// </summary>
        [JsonProperty("totTime")]
        public double? TotalTime { get; set; }

        /// <summary>
        /// Numeric format of total time.
        /// </summary>
        [JsonProperty("totTimeFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string TotalTimeFormat { get; set; }

        /// <summary>
        /// Did the step cause the sequence to fail?
        /// </summary>
        [JsonProperty("causedSeqFailure", NullValueHandling = NullValueHandling.Ignore)]
        public bool? StepCausedSequenceFailure { get; set; }

        /// <summary>
        /// Did the step cause the UUT to fail?
        /// </summary>
        [JsonProperty("causedUUTFailure")]
        public bool StepCausedUUTFailure { get; set; }

        /// <summary>
        /// Step comment.
        /// </summary>
        [JsonProperty("reportText", NullValueHandling = NullValueHandling.Ignore)]
        public string ReportText { get; set; }

        /// <summary>
        /// List of sub steps.
        /// </summary>
        [JsonProperty("steps", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<Step> Steps { get; set; }

        /// <summary>
        /// List of numeric limit measurements.
        /// </summary>
        [JsonProperty("numericMeas", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<NumericMeasurement> NumericMeasurements { get; set; }

        /// <summary>
        /// List of string value measurements.
        /// </summary>
        [JsonProperty("stringMeas", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<StringMeasurement> StringMeasurements { get; set; }

        /// <summary>
        /// List of pass/fail measurements.
        /// </summary>
        [JsonProperty("booleanMeas", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<BooleanMeasurement> BooleanMeasurements { get; set; }

        /// <summary>
        /// List of additional results (free xml).
        /// </summary>
        [JsonProperty("additionalResults", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<AdditionalData> AdditionalResults { get; set; }

        /// <summary>
        /// Sequence call.
        /// </summary>
        [JsonProperty("seqCall", NullValueHandling = NullValueHandling.Ignore)]
        public SequenceCall SequenceCall { get; set; }

        /// <summary>
        /// EXE call.
        /// </summary>
        [JsonProperty("callExe", NullValueHandling = NullValueHandling.Ignore)]
        public CallExe CallExe { get; set; }

        /// <summary>
        /// Popup message.
        /// </summary>
        [JsonProperty("messagePopup", NullValueHandling = NullValueHandling.Ignore)]
        public MessagePopup MessagePopup { get; set; }

        /// <summary>
        /// Chart data.
        /// </summary>
        [JsonProperty("chart", NullValueHandling = NullValueHandling.Ignore)]
        public Chart ChartData { get; set; }

        /// <summary>
        /// Attachment.
        /// </summary>
        [JsonProperty("attachment", NullValueHandling = NullValueHandling.Ignore)]
        public Attachment Attachment { get; set; }
    }

    public class LoopInfo
    {
        /// <summary>
        /// Index (iteration) of loop (iteration only).
        /// </summary>
        [JsonProperty("idx")]
        public short? Index { get; set; }

        /// <summary>
        /// Number of iterations in loop.
        /// </summary>
        [JsonProperty("num")]
        public short? Num { get; set; }

        /// <summary>
        /// Last index of loop.
        /// </summary>
        [JsonProperty("endingIndex")]
        public short? EndingIndex { get; set; }

        /// <summary>
        /// Number of iterations passed.
        /// </summary>
        [JsonProperty("passed")]
        public short? NumPassed { get; set; }

        /// <summary>
        /// Number of iterations failed.
        /// </summary>
        [JsonProperty("failed")]
        public short? NumFailed { get; set; }
    }

    public class NumericMeasurement
    {
        /// <summary>
        /// Comparison operator, valid values: LOG,EQ,NE,GT,GE,LT,LE,GTLT,GTLE,GELT,GELE,LTGT,LTGE,LEGT,LEGE
        /// </summary>
        [JsonProperty("compOp")]
        public string CompOperator { get; set; }

        /// <summary>
        /// Name of measurement (required if multiple measurements in same step).
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Status of measurement, valid values: P,F,S (Passed, Failed, Skipped).
        /// </summary>
        [JsonProperty("status")]
        public char Status { get; set; }

        /// <summary>
        /// Unit of measurement.
        /// </summary>
        [JsonProperty("unit")]
        public string Unit { get; set; }

        /// <summary>
        /// Value measured.
        /// </summary>
        [JsonProperty("value")]
        public double Value { get; set; }

        /// <summary>
        /// Numeric format of value.
        /// </summary>
        [JsonProperty("valueFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string ValueFormat { get; set; }

        /// <summary>
        /// High limit, used in dual comparisons.
        /// </summary>
        [JsonProperty("highLimit")]
        public double? HighLimit { get; set; }

        /// <summary>
        /// Numeric format of high limit.
        /// </summary>
        [JsonProperty("highLimitFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string HighLimitFormat { get; set; }

        /// <summary>
        /// Low limit, used also as limit if not dual comparison.
        /// </summary>
        [JsonProperty("lowLimit")]
        public double? LowLimit { get; set; }

        /// <summary>
        /// Numeric format of low limit.
        /// </summary>
        [JsonProperty("lowLimitFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string LowLimitFormat { get; set; }
    }

    public class StringMeasurement
    {
        /// <summary>
        /// Comparison operator, valid values: LOG,EQ,NE,IGNORECAS,CASESENIT
        /// </summary>
        [JsonProperty("compOp")]
        public string CompOperator { get; set; }

        /// <summary>
        /// Name of measurement (required if multiple measurements in same step).
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Status of measurement, valid values: P,F,S (Passed, Failed, Skipped).
        /// </summary>
        [JsonProperty("status")]
        public char Status { get; set; }

        /// <summary>
        /// Measured value.
        /// </summary>
        [JsonProperty("value")]
        public string Value { get; set; }

        /// <summary>
        /// String to compare against.
        /// </summary>
        [JsonProperty("limit")]
        public string StringLimit { get; set; }
    }

    public class BooleanMeasurement
    {
        /// <summary>
        /// Name of measurement (required if multiple measurements in same step).
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Status of measurement, valid values: P,F,S (Passed, Failed, Skipped).
        /// </summary>
        [JsonProperty("status")]
        public char Status { get; set; }
    }

    public class SequenceCall
    {
        /// <summary>
        /// Path to sequence file location.
        /// </summary>
        [JsonProperty("path")]
        public string Filepath { get; set; }

        /// <summary>
        /// Name of sequence.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Sequence version.
        /// </summary>
        [JsonProperty("version")]
        public string Version { get; set; }
    }

    public class MessagePopup
    {
        /// <summary>
        /// Response from popup.
        /// </summary>
        [JsonProperty("response")]
        public string Response { get; set; }

        /// <summary>
        /// Index of button on popup pressed.
        /// </summary>
        [JsonProperty("button")]
        public short? Button { get; set; }

        /// <summary>
        /// Numeric format of button.
        /// </summary>
        [JsonProperty("buttonFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string ButtonFormat { get; set; }
    }

    public class SubUnit
    {
        /// <summary>
        /// Type of unit.
        /// </summary>
        [JsonProperty("partType")]
        public string PartType { get; set; }

        /// <summary>
        /// Unit part number.
        /// </summary>
        [JsonProperty("pn")]
        public string PartNumber { get; set; }

        /// <summary>
        /// Unit revision number.
        /// </summary>
        [JsonProperty("rev")]
        public string Revision { get; set; }

        /// <summary>
        /// Unit serial number.
        /// </summary>
        [JsonProperty("sn")]
        public string SerialNumber { get; set; }

        /// <summary>
        /// Unit index (only used in repair).
        /// </summary>
        [JsonProperty("idx", NullValueHandling = NullValueHandling.Ignore)]
        public int? Idx { get; set; }

        /// <summary>
        /// Index of parent unit (only used in repair).
        /// </summary>
        [JsonProperty("parentIdx", NullValueHandling = NullValueHandling.Ignore)]
        public int? ParentIDX { get; set; }

        /// <summary>
        /// Position of unit.
        /// </summary>
        [JsonProperty("position", NullValueHandling = NullValueHandling.Ignore)]
        public short? Position { get; set; }

        /// <summary>
        /// Index of unit this unit was replaced by (only valid for repair).
        /// </summary>
        [JsonProperty("replacedIdx", NullValueHandling = NullValueHandling.Ignore)]
        public int? ReplacedIDX { get; set; }

        /// <summary>
        /// Failures in this unit.
        /// </summary>
        [JsonProperty("failures", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<Failure> Failures { get; set; }
    }

    public class MiscInfo
    {
        /// <summary>
        /// Description of misc info.
        /// </summary>
        [JsonProperty("description")]
        public string Description { get; set; }

        /// <summary>
        /// Type definition (deprecated?).
        /// </summary>
        [JsonProperty("typedef", NullValueHandling = NullValueHandling.Ignore)]
        public string Typedef { get; set; }

        /// <summary>
        /// Textual value of misc info.
        /// </summary>
        [JsonProperty("text")]
        public string TextValue { get; set; }

        /// <summary>
        /// Numeric value of misc info.
        /// </summary>
        [JsonProperty("numeric")]
        public short? NumericValue { get; set; }

        /// <summary>
        /// Numeric format of numeric.
        /// </summary>
        [JsonProperty("numericFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string NumericValueFormat { get; set; }

        /// <summary>
        /// Id of misc info (only valid for repair).
        /// </summary>
        [JsonProperty("id", NullValueHandling = NullValueHandling.Ignore)]
        public Guid? Id { get; set; }
    }

    public class Asset
    {
        /// <summary>
        /// Serial number of the asset.
        /// </summary>
        [JsonProperty("assetSN")]
        public string AssetSN { get; set; }

        /// <summary>
        /// How much the asset was used.
        /// </summary>
        [JsonProperty("usageCount")]
        public int UsageCount { get; set; }

        /// <summary>
        /// Number format of usageCount.
        /// </summary>
        [JsonProperty("usageCountFormat")]
        public string UsageCountFormat { get; set; }
    }

    public class AssetStats
    {
        /// <summary>
        /// Serial number of the asset.
        /// </summary>
        [JsonProperty("assetSN")]
        public string AssetSN { get; set; }

        /// <summary>
        /// How many times the asset has been used since last calibration.
        /// </summary>
        [JsonProperty("runningCount", NullValueHandling = NullValueHandling.Ignore)]
        public int? RunningCount { get; set; }

        /// <summary>
        /// How many times more than the limit the asset has been used since last calibration.
        /// </summary>
        [JsonProperty("runningCountExceeded", NullValueHandling = NullValueHandling.Ignore)]
        public int? RunningCountExceeded { get; set; }

        /// <summary>
        /// How many times the asset has been used in its lifetime.
        /// </summary>
        [JsonProperty("totalCount", NullValueHandling = NullValueHandling.Ignore)]
        public int? TotalCount { get; set; }

        /// <summary>
        /// How many times more than the limit the asset has been used in its lifetime.
        /// </summary>
        [JsonProperty("totalCountExceeded", NullValueHandling = NullValueHandling.Ignore)]
        public int? TotalCountExceeded { get; set; }

        /// <summary>
        /// How many days since the last calibration.
        /// </summary>
        [JsonProperty("daysSinceCalibration", NullValueHandling = NullValueHandling.Ignore)]
        public decimal? DaysSinceCalibration { get; set; }

        /// <summary>
        /// If the asset has never been calibrated, then it is unknown.
        /// </summary>
        [JsonProperty("isDaysSinceCalibrationUnknown", NullValueHandling = NullValueHandling.Ignore)]
        public bool? IsDaysSinceCalibrationUnknown { get; set; }

        /// <summary>
        /// How many days since calibration was overdue.
        /// </summary>
        [JsonProperty("calibrationDaysOverdue", NullValueHandling = NullValueHandling.Ignore)]
        public decimal? CalibrationDaysOverdue { get; set; }

        /// <summary>
        /// How many days since maintenance was overdue.
        /// </summary>
        [JsonProperty("daysSinceMaintenance", NullValueHandling = NullValueHandling.Ignore)]
        public decimal? DaysSinceMaintenance { get; set; }

        /// <summary>
        /// If the asset has never been maintenance, then it is unknown.
        /// </summary>
        [JsonProperty("isDaysSinceMaintenanceUnknown", NullValueHandling = NullValueHandling.Ignore)]
        public bool? IsDaysSinceMaintenanceUnknown { get; set; }

        /// <summary>
        /// How many days since maintenance was overdue.
        /// </summary>
        [JsonProperty("maintenanceDaysOverdue", NullValueHandling = NullValueHandling.Ignore)]
        public decimal? MaintenanceDaysOverdue { get; set; }

        /// <summary>
        /// Message from stats calulation.
        /// </summary>
        [JsonProperty("message", NullValueHandling = NullValueHandling.Ignore)]
        public string Message { get; set; }
    }

    public class ReferencedByUUR
    {
        /// <summary>
        /// Id of the referencing repair report.
        /// </summary>
        [JsonProperty("id")]
        public Guid Id { get; set; }

        /// <summary>
        /// Start date time of the referencing repair report.
        /// </summary>
        [JsonProperty("start")]
        public DateTimeOffset Start { get; set; }
    }

    public class Failure
    {
        /// <summary>
        /// Article number of failed component.
        /// </summary>
        [JsonProperty("artNumber")]
        public string ArticleNumber { get; set; }

        /// <summary>
        /// Failed component revision.
        /// </summary>
        [JsonProperty("artRev")]
        public string ArticleRevision { get; set; }

        /// <summary>
        /// Vendor of failed component.
        /// </summary>
        [JsonProperty("artVendor")]
        public string ArticleVendor { get; set; }

        /// <summary>
        /// Description of failed component.
        /// </summary>
        [JsonProperty("artDescription")]
        public string ArticleDescription { get; set; }

        /// <summary>
        /// Failure category.
        /// </summary>
        [JsonProperty("category")]
        public string Category { get; set; }

        /// <summary>
        /// Failure code.
        /// </summary>
        [JsonProperty("code")]
        public string Code { get; set; }

        /// <summary>
        /// Failure comment.
        /// </summary>
        [JsonProperty("comment")]
        public string Comment { get; set; }

        /// <summary>
        /// Component reference.
        /// </summary>
        [JsonProperty("comRef")]
        public string CompRef { get; set; }

        /// <summary>
        /// Function block reference.
        /// </summary>
        [JsonProperty("funcBlock")]
        public string FunctionBlock { get; set; }

        /// <summary>
        /// Id of step from referenced UUT that uncovered failure.
        /// </summary>
        [JsonProperty("refStepId")]
        public int ReferencedStepId { get; set; }

        /// <summary>
        /// Name of step from referenced UUT that uncovered failure.
        /// </summary>
        [JsonProperty("refStepName")]
        public string ReferencedStepName { get; set; }

        /// <summary>
        /// List of attachments in failure.
        /// </summary>
        [JsonProperty("attachments", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<BinaryData> BinaryData { get; set; }
    }

    public class Chart
    {
        /// <summary>
        /// Type of chart, valid values:
        /// </summary>
        [JsonProperty("chartType")]
        public string ChartType { get; set; }

        /// <summary>
        /// Chart label.
        /// </summary>
        [JsonProperty("label")]
        public string Label { get; set; }

        /// <summary>
        /// X-axis label.
        /// </summary>
        [JsonProperty("xLabel")]
        public string XLabel { get; set; }

        /// <summary>
        /// X-axis unit.
        /// </summary>
        [JsonProperty("xUnit")]
        public string XUnit { get; set; }

        /// <summary>
        /// Y-axis label.
        /// </summary>
        [JsonProperty("yLabel")]
        public string YLabel { get; set; }

        /// <summary>
        /// Y-axis unit.
        /// </summary>
        [JsonProperty("yUnit")]
        public string YUnit { get; set; }

        /// <summary>
        /// List of chart series.
        /// </summary>
        [JsonProperty("series")]
        public IEnumerable<ChartSeries> Series { get; set; }
    }

    public class ChartSeries
    {
        /// <summary>
        /// Data type of series, valid values: XYG.
        /// </summary>
        [JsonProperty("dataType")]
        public string DataType { get; set; }

        /// <summary>
        /// Name of series.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Semicolon separated string of X-coordinates.
        /// </summary>
        [JsonProperty("xdata")]
        public string XData { get; set; }

        /// <summary>
        /// Semicolon separated string of Y-coordinates.
        /// </summary>
        [JsonProperty("ydata")]
        public string YData { get; set; }
    }

    public class Attachment
    {
        /// <summary>
        /// Name of attachment.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Content type of attachment.
        /// </summary>
        [JsonProperty("contentType")]
        public string ContentType { get; set; }

        /// <summary>
        /// The data of attachment.
        /// </summary>
        [JsonProperty("data")]
        public string Data { get; set; }
    }

    public class CallExe
    {
        /// <summary>
        /// Exit code of called exe.
        /// </summary>
        [JsonProperty("exitCode")]
        public double? ExitCode { get; set; }

        /// <summary>
        /// Numeric format of exit code.
        /// </summary>
        [JsonProperty("exitCodeFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string ExitCodeFormat { get; set; }
    }

    public class BinaryData
    {
        /// <summary>
        /// Content type of attachment.
        /// </summary>
        [JsonProperty("contentType")]
        public string ContentType { get; set; }

        /// <summary>
        /// The data of attachment.
        /// </summary>
        [JsonProperty("data")]
        public string Data { get; set; }

        /// <summary>
        /// Name of attachment.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Id of Binary data.
        /// </summary>
        [JsonProperty("id")]
        public Guid? Id { get; set; }
    }

    public class AdditionalData
    {
        /// <summary>
        /// Name of additional data.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Properties of additional data.
        /// </summary>
        [JsonProperty("props")]
        public IEnumerable<AdditionalDataProperty> Properties { get; set; }
    }

    public class AdditionalDataProperty
    {
        /// <summary>
        /// Name of property.
        /// </summary>
        [JsonProperty("name")]
        public string Name { get; set; }

        /// <summary>
        /// Value type of property.
        /// </summary>
        [JsonProperty("type")]
        public string Type { get; set; }

        /// <summary>
        /// Bit flags of property.
        /// </summary>
        [JsonProperty("flags", NullValueHandling = NullValueHandling.Ignore)]
        public int? Flags { get; set; }

        /// <summary>
        /// Value string of property.
        /// </summary>
        [JsonProperty("value", NullValueHandling = NullValueHandling.Ignore)]
        public string Value { get; set; }

        /// <summary>
        /// Number format for value with type Number.
        /// </summary>
        [JsonProperty("numFormat", NullValueHandling = NullValueHandling.Ignore)]
        public string NumberFormat { get; set; }

        /// <summary>
        /// Comment of property.
        /// </summary>
        [JsonProperty("comment", NullValueHandling = NullValueHandling.Ignore)]
        public string Comment { get; set; }

        /// <summary>
        /// Array of sub-properties. Used for type Obj.
        /// </summary>
        [JsonProperty("props", NullValueHandling = NullValueHandling.Ignore)]
        public IEnumerable<AdditionalDataProperty> Properties { get; set; }

        /// <summary>
        /// Array information. Used for type Array.
        /// </summary>
        [JsonProperty("array", NullValueHandling = NullValueHandling.Ignore)]
        public AdditionalDataArray Array { get; set; }
    }

    public class AdditionalDataArray
    {
        /// <summary>
        /// Dimension of array.
        /// </summary>
        [JsonProperty("dimension")]
        public int Dimension { get; set; }

        /// <summary>
        /// Type of the values in the array.
        /// </summary>
        [JsonProperty("type")]
        public string Type { get; set; }

        /// <summary>
        /// List of indexes in the array.
        /// </summary>
        [JsonProperty("indexes")]
        public IEnumerable<AdditionalDataArrayIndex> Indexes { get; set; }
    }

    public class AdditionalDataArrayIndex
    {
        /// <summary>
        /// The index as text.
        /// </summary>
        [JsonProperty("text")]
        public string IndexText { get; set; }

        /// <summary>
        /// List of indexes ordered by dimension.
        /// </summary>
        [JsonProperty("indexes")]
        public IEnumerable<int> Indexes { get; set; }

        /// <summary>
        /// Value of index.
        /// </summary>
        [JsonProperty("value")]
        public AdditionalDataProperty Value { get; set; }
    }
}
