using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Virinco.WATS.Web.Api.Models
{

    [Obsolete("Deprecated along with FindReports, use FindReportHeaders instead.")]
    public class WatsReportHeader
    {
        public Guid Guid { get; set; }

        public string SN { get; set; }

        public string PN { get; set; }

        public string ReportType { get; set; }

        public DateTime Start_UTC { get; set; }

        public string Rev { get; set; }

        public string Result { get; set; }

        public string OpCode { get; set; }

        public string OpName { get; set; }

        public string BatchNo { get; set; }

        public string Operator { get; set; }

        public string MachineName { get; set; }

        public string Location { get; set; }

        public string Purpose { get; set; }

        public bool MeasuresDeleted { get; set; }

        public Int64 tstamp { get; set; }
    }
}