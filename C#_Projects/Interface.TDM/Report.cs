using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;
using System.Text.RegularExpressions;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Common properties to a UUT or UUR report, cannot be used directly
    /// </summary>
    public class Report
    {
        /*
        /// <summary>
        /// Internal data
        /// </summary>
        protected internal WATSReport reportDataSet;
        */
        /// <summary>
        /// Internal data
        /// </summary>
        protected internal WATSReport reportRow;
        /// <summary>
        /// Internal data
        /// </summary>
        protected internal TDM api;

        /// <summary>
        /// Unique Global Identifier of Report (GUID)
        /// Normal operation is that this is generated automatically when report is created.
        /// ReportId can be set manually if you need to replace a report with a new one.
        /// </summary>
        public Guid ReportId
        {
            get { return new Guid(reportRow.ID); }
            set { reportRow.ID = value.ToString(); }
        }
        /*
        internal int Report_ID
        {
            get { return reportRow.Report_ID; }
        }
        */
        /// <summary>
        /// Represents a report's transfer status. The report file extension reflects the report's current transfer status.
        /// </summary>
        public enum ReportTransferStatusEnum
        {
            /// <summary>
            /// Not submitted
            /// </summary>
            InMemory,
            //Saved,
            /// <summary>
            /// Ready for transferring
            /// </summary>
            Queued,
            /// <summary>
            /// In processs of being transferred
            /// </summary>
            Transfering,
            /// <summary>
            /// An error occured during transfer
            /// </summary>
            Error,
            /// <summary>
            /// Not possible to send to server
            /// </summary>
            InvalidReport

        }

        private bool isStartDateTimeOffsetSet = false;

        private bool isStartDateTimeSet = false;

        internal void SaveToFile()
        {
            EnsureStatisticsUpdated();
            ReportTransferStatus = ReportTransferStatusEnum.Queued;
            Reports r = new Reports();
            r.Report.Add(reportRow);
            string reportFileName = ReportFileName;
            try
            {
                System.Xml.Serialization.XmlSerializer s = new System.Xml.Serialization.XmlSerializer(typeof(Reports));
                using (System.Xml.XmlWriter writer = System.Xml.XmlWriter.Create(reportFileName))
                    s.Serialize(writer, r);
            }
            catch (Exception)
            {
                if (File.Exists(reportFileName))
                    File.Delete(reportFileName);

                throw;
            }
        }
        internal void EnsureStatisticsUpdated()
        {
            bool clientstat;
            ReportInfo_type cstat = this.reportRow.Items.OfType<ReportInfo_type>().FirstOrDefault(ri => ri.key == "clientstat");
            if (cstat == null)
            {
                cstat = new ReportInfo_type() { key = "clientstat", value = "False" };
                this.reportRow.Items.Add(cstat);
            }
            if (!bool.TryParse(cstat.value, out clientstat) || !clientstat)
            {
                System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(AddStatistics), this);
                cstat.value = true.ToString();
            }
        }
        private void AddStatistics(object state)
        {
            Report report = state as Report;
            if (report != null)
            {
                try
                {
                    if (report is UURReport) api.Statistics.IncreaseUURCount();
                    else if (report is UUTReport) api.Statistics.AddTest(report.PartNumber, report.reportRow.Process, api.ReportResultToStatus(report.reportRow.Result));
                    else
                        throw new ArgumentException(String.Format("Unsupported Reporttype: {0}", report.GetType()));
                }
                catch (Exception e)
                {
                    Env.Trace.TraceData(TraceEventType.Warning, 0, new WATSLogItem() { ex = e, Message = "Unhandled exception during AddStstistics" });
                }
            }
            /*
            if (report != null)
            {
                if (report.reportRow.IsOperationNull())
                    Debug.Print("pn:{0}, ot:{1}, res:{2}", report.PartNumber, null, (Virinco.WATS.StatusType)report.reportRow.Result);
                else
                    Debug.Print("pn:{0}, ot:{1}, res:{2}", report.PartNumber, report.reportRow.Operation, (Virinco.WATS.StatusType)report.reportRow.Result);

            } */
        }


        internal void ReadFromFile(string fileName, ReportTransferStatusEnum status)
        {
            Reports r;
            System.Xml.Serialization.XmlSerializer s = new System.Xml.Serialization.XmlSerializer(typeof(Reports));
            using (System.Xml.XmlReader reader = System.Xml.XmlReader.Create(ReportFileName))
                r = s.Deserialize(reader) as Reports;
            reportRow = r.Report.First();
            ReportTransferStatus = status;
        }

        internal static string GetReportFileName(TDM apiRef, ReportTransferStatusEnum status, Guid reportId)
        {
            string fileName = reportId.ToString() + "." + status.ToString();
            return Path.Combine(apiRef.ReportsDirectory, fileName); ;
        }

        internal string ReportFileName
        {
            get
            {
                return GetReportFileName(api, ReportTransferStatus, ReportId);
            }
        }

        ReportTransferStatusEnum reportTransferStatus = ReportTransferStatusEnum.InMemory;
        internal ReportTransferStatusEnum ReportTransferStatus
        {
            get { return reportTransferStatus; }
            set
            {
                if (reportTransferStatus != value)
                {
                    string filePath = Path.Combine(api.ReportsDirectory, ReportId.ToString());
                    string oldName = filePath + "." + reportTransferStatus.ToString();
                    if (File.Exists(oldName))
                    {
                        string newName = filePath + "." + value.ToString();
                        if (File.Exists(newName)) File.Delete(newName);
                        File.Move(oldName, newName);
                    }
                }
                reportTransferStatus = value;
            }
        }

        internal void DeleteFile()
        {
            if (File.Exists(ReportFileName))
            {
                File.Delete(ReportFileName);
            }
        }


        internal Report(TDM apiRef, bool createHeader)
        {
            //Trace.WriteLine("Report constructor");
            api = apiRef;
            //Create dataset
            reportRow = createHeader
                ? new WATSReport()
                {
                    ID = Guid.NewGuid().ToString(),
                    MachineName = apiRef.StationName,
                    Location = apiRef.Location,
                    Purpose = apiRef.Purpose,
                    Start_offset = DateTimeOffset.Now,
                    //Start = DateTime.Now,
                    //Start_utc = DateTime.UtcNow,
                    Start_utcSpecified = false,
                    Result = ReportResultType.Passed,
                    ResultSpecified = true
                }
                : new WATSReport();
            ReportTransferStatus = ReportTransferStatusEnum.InMemory;
        }

        internal Report(TDM apiRef, WATSReport wr)
        {
            api = apiRef;
            reportRow = wr;
            ReportTransferStatus = ReportTransferStatusEnum.InMemory;

            if (!reportRow.Start_utcSpecified)
                reportRow.Start_utc = reportRow.Start_offset.UtcDateTime;

            isStartDateTimeOffsetSet = true;
        }

        /// <summary>
        /// Serial number of unit. Unique combined with PartNumber
        /// </summary>
        public string SerialNumber
        {
            get { return reportRow.SN; }
            set { reportRow.SN = api.SetPropertyValidated<WATSReport>("SN", value, "SerialNumber"); }
        }

        /// <summary>
        /// Part number of the product
        /// </summary>
        public string PartNumber
        {
            get { return reportRow.PN; }
            set { reportRow.PN = api.SetPropertyValidated<WATSReport>("PN", value, "PartNumber"); }
        }
        /// <summary>
        /// Hardware revision of the product
        /// </summary>
        public string PartRevisionNumber
        {
            get { return reportRow.Rev; }
            set { reportRow.Rev = api.SetPropertyValidated<WATSReport>("Rev", value, "PartRevisionNumber"); }
        }


        /// <summary>
        /// Station name. NB This property is initiated from TDM.Station name when report is created. Can be modified here.
        /// </summary>
        public string StationName
        {
            get { return reportRow.MachineName; }
            set { reportRow.MachineName = api.SetPropertyValidated<WATSReport>("MachineName", value, "StationName"); }
        }

        /// <summary>
        /// Location of the station, initialized from api to client setup values
        /// </summary>
        public string Location
        {
            get { return reportRow.Location; }
            set { reportRow.Location = api.SetPropertyValidated<WATSReport>("Location", value); }
        }

        /// <summary>
        /// Purpose of the station, initialized from api to client setup values
        /// </summary>
        public string Purpose
        {
            get { return reportRow.Purpose; }
            set { reportRow.Purpose = api.SetPropertyValidated<WATSReport>("Purpose", value); }
        }

        /// <summary>
        /// Sets Start Date/Time with offset.
        /// If you need different timezone than the client - use this instead of StartDateTime/StartDateTimeUTC
        /// </summary>
        public DateTimeOffset StartDateTimeOffset
        {
            get { return reportRow.Start_offset; }
            set 
            { 
                reportRow.Start_offset = value;
                isStartDateTimeOffsetSet = true;
            }
        }


        /// <summary>
        /// Local execution date/time.
        /// </summary>
        public DateTime StartDateTime
        {
            get { return reportRow.Start; }
            set
            {
                if (value < dt1970) return; //Do not set if invalid
                // Ensure value is local
                if (value.Kind != DateTimeKind.Local) reportRow.Start = new DateTime(value.Ticks, DateTimeKind.Local);
                else reportRow.Start = value;

                isStartDateTimeSet = true;
                //Always keep Start and StartUtc in sync.ValidateReportRow handles this now.
                //reportRow.Start_utc = reportRow.Start.ToUniversalTime();
            }
        }

        /// <summary>
        /// UTC execution date/time.
        /// </summary>
        public DateTime StartDateTimeUTC
        {
            get { return reportRow.Start_utc; }
            set
            {
                if (value < dt1970) return; //Do not set if invalid
                // Ensure value is UtcKind
                if (value.Kind != DateTimeKind.Utc) reportRow.Start_utc = new DateTime(value.Ticks, DateTimeKind.Utc);
                else reportRow.Start_utc = value;
                
                //Always keep StartUTC and Start in sync. ValidateReportRow handles this now.
                //reportRow.Start = reportRow.Start_utc.ToLocalTime();
            }
        }

        /// <summary>
        /// Reserved for use with TestStand. Does not show up in analysis.
        /// Additional data can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
        /// </summary>
        /// <param name="name">Name of additional data.</param>
        /// <param name="contents">The xml data.</param>
        /// <returns></returns>
        public AdditionalData AddAdditionalData(string name, System.Xml.Linq.XElement contents)
        {
            return new AdditionalData(this, name, contents);
        }

        /// <summary>
        /// Reserved for use with TestStand. Does not show up in analysis.
        /// Additional station info can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
        /// </summary>
        /// <param name="contents">The station info.</param>
        /// <returns></returns>
        public AdditionalData AddAdditionalStationInfo(System.Xml.Linq.XElement contents)
        {
            return new AdditionalData(this, "Station info", contents);
        }

        /// <summary>
        /// Load a report from WRML
        /// </summary>
        /// <param name="apiRef"></param>
        /// <param name="wr"></param>
        /// <returns></returns>
        public static Report Load(TDM apiRef, WATSReport wr)
        {
            if (wr.type == ReportType.UUT)
                return new UUTReport(apiRef, wr);
            else if (wr.type == ReportType.UUR)
                return new UURReport(apiRef, wr);
            else
                throw new NotImplementedException(String.Format("ReportItemType {0} is not supported", wr.type));
        }

        /// <summary>
        /// Validates required reportdata.
        /// Exception is thrown if invalid or missing data is found.
        /// </summary>
        public void ValidateForSubmit()
        {
            System.Collections.Generic.List<ReportValidationResult> result = new System.Collections.Generic.List<ReportValidationResult>();
            //foreach (WATSReport.ReportRow report in this.Report)
            //if (string.IsNullOrEmpty(reportRow.PN))
            //    result.Add(new ReportValidationResult() { ReportId = new Guid(reportRow.ID), Table = "Report", Field = "PN", Message = "Missing Partnumber. Partnumber cannot be NULL or empty." });
            //TODO: 15.01.2018: Skip this test for 5.0. Re-introduce this in Client 5.1             

            if (this is UUTReport)
            {
                var uut = (UUTReport)this;
                result.AddRange(uut.PartInfo.Where(p => string.IsNullOrEmpty(p.SerialNumber)).Select(p => new ReportValidationResult
                {
                    ReportId = new Guid(reportRow.ID),
                    Table = "PartInfo",
                    Field = "SerialNumber",
                    Message = "PartInfo serial number cannot be empty"
                }));

                if (string.IsNullOrEmpty(uut.SequenceName))                
                    uut.SequenceName = reportRow.PN;                

                foreach (var sq in reportRow.Items.OfType<SequenceCall_type>().Where(sq => string.IsNullOrEmpty(sq.Filepath)))                
                    sq.Filepath = uut.SequenceName;
            }

            if (this is UURReport)
            {
                UURReport uur = (UURReport)this;

                if (uur.Finalized < uur.StartDateTimeUTC)
                    uur.Finalized = DateTime.UtcNow;

                //Check UURMiscInfo into rows
                short idx = 0;
                MiscInfo_type[] miscInfos = reportRow.Items.OfType<MiscInfo_type>().ToArray();
                //var miscInfos = reportRow.Items.OfType<MiscInfo_type>().ToDictionary(e => e.Id);
                foreach (MiscUURInfo mi in uur.MiscInfo)
                {
                    if (!string.IsNullOrEmpty(mi.DataString))
                    {
                        var regex = new Regex(mi.ValidRegularExpression);
                        var list = mi.ValidRegularExpression.Split(';');

                        if (regex.IsMatch(mi.DataString) || list.Contains(mi.DataString))
                        {
                            mi.miData.idx = idx;
                            mi.miData.idxSpecified = true;
                            idx++;
                            if (!miscInfos.Any(m => m.Description == mi.miData.Description)) //add to items                            
                                reportRow.Items.Add(mi.miData);
                        }
                        else
                        {
                            result.Add(new ReportValidationResult
                            {
                                ReportId = new Guid(reportRow.ID),
                                Table = "UURReport",
                                Field = "MiscInfo",
                                Message = $"Invalid format for Misc Info field {mi.Description} Input mask:{mi.ValidRegularExpression}, value:{ mi.DataString}"
                            });
                        }
                    }
                    else //Validate against blank, if blank is valid - skip without failure
                    {
                        Regex ex = new Regex(mi.ValidRegularExpression);
                        if (!ex.IsMatch(""))
                        {
                            result.Add(new ReportValidationResult
                            {
                                ReportId = new Guid(reportRow.ID),
                                Table = "UURReport",
                                Field = "MiscInfo",
                                Message = $"Misc Info field {mi.Description} cannot be blank. Input mask:{mi.ValidRegularExpression}"
                            });
                        }
                    }
                }

                if (result.Count > 0)
                    throw new WATSReportValidationException(result);
            }
        }

        private static readonly System.DateTime dt1970 = new System.DateTime(1970, 1, 1);
        /// <summary>
        /// Validate and correct field sizes, truncate if neccessary. 
        /// Validate and correct local vs. utc date if mismatch or missing.
        /// </summary>
        /// <returns>Returns true!</returns>
        public bool ValidateReport()
        {
            ValidateReportRow(reportRow, isStartDateTimeOffsetSet, isStartDateTimeSet);
            return true;
        }

        internal static void ValidateReportRow(WATSReport row, bool isStartDateTimeOffsetSet, bool isStartDateTimeSet)
        {
            // local vs utc time validation is no longer valid since both reference the same backgroud datetimeoffset field ????

            // Validate utc & local datetime...
            //System.DateTime dtLocal = new System.DateTime(row.Start.Ticks, System.DateTimeKind.Local);
            //System.DateTime dtUtc = new System.DateTime(row.Start_utc.Ticks, System.DateTimeKind.Utc); // Ensure 

            if ((isStartDateTimeOffsetSet || isStartDateTimeSet) && row.Start_offset.UtcDateTime > dt1970)
            {
                if (row.Start_utcSpecified)
                {
                    // Start_offset is valid, use as source
                    // check if utc is within +/-14hrs:
                    var dtLocalAsUtc = new System.DateTime(row.Start_offset.Ticks, System.DateTimeKind.Utc); // Ensure no conversion during subtract
                    // Calculate offset as difference between specified start_utc and start rounded to nearest 15minutes
                    var calcoffset = TimeSpan.FromMinutes(Math.Round(dtLocalAsUtc.Subtract(row.Start_utc).TotalMinutes / 15) * 15);
                    if (calcoffset >= TimeSpan.FromHours(-14) && calcoffset <= TimeSpan.FromHours(14))
                    {
                        // use calculated offset to set correct timezone
                        row.Start_offset = new DateTimeOffset(row.Start_offset.Ticks, calcoffset);
                    }
                    // else // calc. offset is too high (more than +/-14hrs) keep using start_offset with offset=0 (UTC/GMT)
                }
            }
            else
            {
                // StartOffset is invalid, check utc value
                var dtUtc = new System.DateTime(row.Start_utc.Ticks, System.DateTimeKind.Utc); // Ensure correct DateTimeKind for dtUtc
                if (dtUtc > dt1970)
                {
                    // dtUtc is valid (start_offset is not). Use dtUtc with local timezone:
                    row.Start_offset = new DateTimeOffset(dtUtc.ToLocalTime());
                }
                else
                {
                    // both datefields are invalid. Use local time (with local timezone)
                    row.Start_offset = DateTimeOffset.Now;
                }
            }
            
            row.Start_utcSpecified = false; // Do not serialize utc datetime, timezone is specified in start (start_offset).
        }
    }

    /// <summary>
    /// Exception class thrown from WATSReport.ValidateForSubmit if one or more Errors was found.
    /// </summary>
    public class WATSReportValidationException : System.Exception
    {
        internal WATSReportValidationException(System.Collections.Generic.IEnumerable<ReportValidationResult> results)
        {
            this.Errors = results;
        }
        public System.Collections.Generic.IEnumerable<ReportValidationResult> Errors;
    }

    /// <summary>
    /// WATSReport validation result item. An IEnumerable list of ReportValidationResult is found in the Error property of the WATSReportValidationException.
    /// </summary>
    public class ReportValidationResult
    {
        /// <summary>
        /// Report Id (Guid) of the report causing the validation error
        /// </summary>
        public System.Guid ReportId { get; set; }
        /// <summary>
        /// Table name causing the validation error
        /// </summary>
        public string Table { get; set; }
        /// <summary>
        /// Field/Property name causing the validation error
        /// </summary>
        public string Field { get; set; }
        /// <summary>
        /// Validation error description
        /// </summary>
        public string Message { get; set; }
    }
}
