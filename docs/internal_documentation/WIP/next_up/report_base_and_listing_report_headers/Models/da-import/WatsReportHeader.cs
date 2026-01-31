using System;
using System.Collections.Generic;
#if !(NET20 || NET35)
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
#endif
using System.Linq;
using System.Web;

namespace Virinco.WATS.Web.Api.Models
{
#if !(NET20 || NET35)
    [Table("WatsReportHeader", Schema = "api")]
#endif
    [Obsolete("Deprecated along with FindReports, use FindReportHeaders instead.")]
    public class WatsReportHeader
    {
#if !(NET20 || NET35)
        [Key]
#endif
        public Guid Guid { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName ="varchar")]
        //[StringLength(100)]
#endif
        public string SN { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string PN { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string ReportType { get; set; }

    //[Key]
        public DateTime Start_UTC { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string Rev { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string Result { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string OpCode { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string OpName { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string BatchNo { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "varchar")]
        //[StringLength(100)]
#endif
        public string Operator { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "nvarchar")]
        //[StringLength(100)]
#endif
        public string MachineName { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "nvarchar")]
        //[StringLength(100)]
#endif
        public string Location { get; set; }

#if !(NET20 || NET35)
        [Column(TypeName = "nvarchar")]
        //[StringLength(100)]
#endif
        public string Purpose { get; set; }

        public bool MeasuresDeleted { get; set; }
        // Possible alternative key (DB Primary key). Beware: Seriously affects performance if statistics is out of date!
        //public int Id { get; set; }

        public Int64 tstamp { get; set; }
  }
}