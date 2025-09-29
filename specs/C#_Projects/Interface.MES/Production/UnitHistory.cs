using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Virinco.Newtonsoft.Json;
using Virinco.WATS.Service.MES.Contract;

namespace Virinco.WATS.Interface.MES.Production
{
    public class UnitHistory
    {
        /// <summary>
        /// Unit serial number.
        /// </summary>
        [JsonProperty("serialNumber")]
        public string SN { get; set; }   
        
        /// <summary>
        /// Unit part number.
        /// </summary>
        [JsonProperty("partNumber")]
        public string PN { get; set; }

        /// <summary>
        /// Unit revision.
        /// </summary>
        [JsonProperty("revision")]
        public string Revision { get; set; }

        /// <summary>
        /// Unit type, Unit or Subunit.
        /// </summary>
        [JsonProperty("level")]
        public string Level { get; set; }

        /// <summary>
        /// The process the unit was in.
        /// </summary>
        [JsonProperty("toProcess")]
        public string Process { get; set; }

        /// <summary>
        /// The status the unit had.
        /// </summary>
        [JsonProperty("status")]
        public string Status { get; set; }

        /// <summary>
        /// <c>true</c> if this change was forced by a user.
        /// </summary>
        [JsonProperty("forced")]
        public bool Forced { get; set; }

        /// <summary>
        /// Id to a report, if the change was because of test or repair.
        /// </summary>
        [JsonProperty("uuid")]
        public Guid? ReportId { get; set; }

        /// <summary>
        /// If unit has report, this is the station name in the report.
        /// </summary>
        [JsonProperty("stationName")]
        public string StationName { get; set; }

        /// <summary>
        /// If unit has report, this is the location in the report.
        /// </summary>
        [JsonProperty("location")]
        public string Location { get; set; }

        /// <summary>
        /// If unit has report, this is the purpose in the report.
        /// </summary>
        [JsonProperty("purpose")]
        public string Purpose { get; set; }

        /// <summary>
        /// If unit has report, this is the operator in the report.
        /// </summary>
        [JsonProperty("userName")]
        public string Operator { get; set; }

        /// <summary>
        /// Date and time of when the change happened.
        /// </summary>
        [JsonProperty("startUtc")]
        public DateTime StartUtc { get; set; }

        /// <summary>
        /// If unit has report, this is when the test or repair ended.
        /// </summary>
        [JsonProperty("endUtc")]
        public DateTime? EndUtc { get; set; }

        /// <summary>
        /// If details is <c>true</c>, a list of info and error messages.
        /// </summary>
        [JsonProperty("details")]
        public List<UnitReportHistoryDetails> Details { get; set; }
    }

    public class UnitReportHistoryDetails
    {
        [JsonProperty("info")]
        public string Info { get; set; }

        [JsonProperty("error")]
        public string Error { get; set; }
    }
}
