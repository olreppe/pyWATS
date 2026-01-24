extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using wrml = newclientapi::Virinco.WATS.Schemas.WRML;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Runtime.CompilerServices;
using System.Xml.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Common properties to a UUT or UUR report, cannot be used directly
    /// </summary>
    public class Report
    {
        internal napi.Report _baseinstance;
        internal Report(napi.Report instance) { _baseinstance = instance; }

        /// <summary>
        /// Unique Global Identifier of Report (GUID)
        /// Normal operation is that this is generated automatically when report is created.
        /// ReportId can be set manually if you need to replace a report with a new one.
        /// </summary>
        public Guid ReportId
        {
            get => _baseinstance.ReportId;
            set => _baseinstance.ReportId = value;
        }

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



        //internal Report(TDM apiRef, bool createHeader)
        //{
        //    //Trace.WriteLine("Report constructor");
        //    api = apiRef;
        //    //Create dataset
        //    reportRow = createHeader
        //        ? new WATSReport()
        //        {
        //            ID = Guid.NewGuid().ToString(),
        //            MachineName = apiRef.StationName,
        //            Location = apiRef.Location,
        //            Purpose = apiRef.Purpose,
        //            Start_offset = DateTimeOffset.Now,
        //            //Start = DateTime.Now,
        //            //Start_utc = DateTime.UtcNow,
        //            Start_utcSpecified = false,
        //            Result = ReportResultType.Passed,
        //            ResultSpecified = true
        //        }
        //        : new WATSReport();
        //    ReportTransferStatus = ReportTransferStatusEnum.InMemory;
        //}

        //internal Report(TDM apiRef, WATSReport wr)
        //{
        //    api = apiRef;
        //    reportRow = wr;
        //    ReportTransferStatus = ReportTransferStatusEnum.InMemory;

        //    if (!reportRow.Start_utcSpecified)
        //        reportRow.Start_utc = reportRow.Start_offset.UtcDateTime;

        //    isStartDateTimeOffsetSet = true;
        //}

        /// <summary>
        /// Serial number of unit. Unique combined with PartNumber
        /// </summary>
        public string SerialNumber
        {
            get => _baseinstance.SerialNumber;
            set => _baseinstance.SerialNumber = value;
        }

        /// <summary>
        /// Part number of the product
        /// </summary>
        public string PartNumber
        {
            get => _baseinstance.PartNumber;
            set => _baseinstance.PartNumber = value;
        }

        /// <summary>
        /// Hardware revision of the product
        /// </summary>
        public string PartRevisionNumber
        {
            get => _baseinstance.PartRevisionNumber;
            set => _baseinstance.PartRevisionNumber = value;
        }

        /// <summary>
        /// Station name. NB This property is initiated from TDM.Station name when report is created. Can be modified here.
        /// </summary>
        public string StationName
        {
            get => _baseinstance.StationName;
            set => _baseinstance.StationName = value;
        }

        /// <summary>
        /// Location of the station, initialized from api to client setup values
        /// </summary>
        public string Location
        {
            get => _baseinstance.Location;
            set => _baseinstance.Location = value;
        }

        /// <summary>
        /// Purpose of the station, initialized from api to client setup values
        /// </summary>
        public string Purpose
        {
            get => _baseinstance.Purpose;
            set => _baseinstance.Purpose = value;
        }

        /// <summary>
        /// Sets Start Date/Time with offset.
        /// If you need different timezone than the client - use this instead of StartDateTime/StartDateTimeUTC
        /// </summary>
        public DateTimeOffset StartDateTimeOffset
        {
            get => _baseinstance.StartDateTimeOffset;
            set => _baseinstance.StartDateTimeOffset = value;
        }

        /// <summary>
        /// Local execution date/time.
        /// </summary>
        public DateTime StartDateTime
        {
            get => _baseinstance.StartDateTime;
            set => _baseinstance.StartDateTime = value;
        }

        /// <summary>
        /// UTC execution date/time.
        /// </summary>
        public DateTime StartDateTimeUTC
        {
            get => _baseinstance.StartDateTimeUTC;
            set => _baseinstance.StartDateTimeUTC = value;
        }

        /// <summary>
        /// Reserved for use with TestStand. Does not show up in analysis.
        /// Additional data can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
        /// </summary>
        /// <param name="name">Name of additional data.</param>
        /// <param name="contents">The xml data.</param>
        /// <returns></returns>
        public AdditionalData AddAdditionalData(string name, System.Xml.Linq.XElement contents)
            => new AdditionalData(_baseinstance.AddAdditionalData(name, contents));

        /// <summary>
        /// Reserved for use with TestStand. Does not show up in analysis.
        /// Additional station info can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
        /// </summary>
        /// <param name="contents">The station info.</param>
        /// <returns></returns>
        public AdditionalData AddAdditionalStationInfo(System.Xml.Linq.XElement contents)
            => new AdditionalData(_baseinstance.AddAdditionalStationInfo(contents));

        /// <summary>
        /// Load a report from WRML
        /// </summary>
        /// <param name="apiRef"></param>
        /// <param name="wr"></param>
        /// <returns></returns>
        public static Report Load(TDM apiRef, wrml.WATSReport wr)
        {
            var r = napi.Report.Load(apiRef._instance, wr);
            if (r is napi.UUTReport) return new UUTReport((napi.UUTReport)r);
            else if (r is napi.UURReport) return new UURReport((napi.UURReport)r);
            else
                throw new NotImplementedException(String.Format("ReportItemType {0} is not supported", wr.type));
        }

        /// <summary>
        /// Validates required reportdata.
        /// Exception is thrown if invalid or missing data is found.
        /// </summary>
        public void ValidateForSubmit()
            => _baseinstance.ValidateForSubmit();

        /// <summary>
        /// Validate and correct field sizes, truncate if neccessary. 
        /// Validate and correct local vs. utc date if mismatch or missing.
        /// </summary>
        /// <returns>Returns true!</returns>
        public bool ValidateReport()
            => _baseinstance.ValidateReport();


    }

    ///// <summary>
    ///// Exception class thrown from WATSReport.ValidateForSubmit if one or more Errors was found.
    ///// </summary>
    //public class WATSReportValidationException : System.Exception
    //{
    //    internal WATSReportValidationException(System.Collections.Generic.IEnumerable<ReportValidationResult> results)
    //    {
    //        this.Errors = results;
    //    }
    //    public System.Collections.Generic.IEnumerable<ReportValidationResult> Errors;
    //}

    ///// <summary>
    ///// WATSReport validation result item. An IEnumerable list of ReportValidationResult is found in the Error property of the WATSReportValidationException.
    ///// </summary>
    //public class ReportValidationResult
    //{
    //    /// <summary>
    //    /// Report Id (Guid) of the report causing the validation error
    //    /// </summary>
    //    public System.Guid ReportId { get; set; }
    //    /// <summary>
    //    /// Table name causing the validation error
    //    /// </summary>
    //    public string Table { get; set; }
    //    /// <summary>
    //    /// Field/Property name causing the validation error
    //    /// </summary>
    //    public string Field { get; set; }
    //    /// <summary>
    //    /// Validation error description
    //    /// </summary>
    //    public string Message { get; set; }
    //}
}
