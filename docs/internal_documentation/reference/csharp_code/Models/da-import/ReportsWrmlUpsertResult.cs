using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Virinco.WATS.Web.Dashboard.Models.procs
{
    public class ReportsWrmlUpsertResult
    {
        public String type { get; set; }
        public Guid ID { get; set; }
        public DateTimeOffset Start_utc { get; set; }
        public string SN { get; set; }
        public string PN { get; set; }
        public int report_result { get; set; }
        public int Report_ID { get; set; }
        public int insert_result { get; set; }
        public string insert_message { get; set; }
        public char reportstate { get; set; }
        public int receivecount { get; set; }
    }
}