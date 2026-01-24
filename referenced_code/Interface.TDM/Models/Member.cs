using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Interface.Models
{
    public class Member
    {
        public Guid Id { get; set; }
        public DateTime RegDate { get; set; }
        public RecordState Status { get; set; }
        public Guid ParentId { get; set; }
        public string MiscInfo { get; set; }
        public DateTime MiscInfo_updated { get; set; }
        public TimeSpan BaseUtcOffset { get; set; }

        //MemberAccess[] access { get; set; }
        public Syslog[] logs { get; set; }
        public MemberPropset[] propsets { get; set; }
        public MemberExtInfo[] extinfos { get; set; }
    }

    //public class MemberAccess
    //{
    //}
    public class Syslog
    {
        public Virinco.WATS.Logging.LogCategory Category { get; set; }
        public Virinco.WATS.Logging.LogSeverity Severity { get; set; }
        public DateTime LogDate { get; set; }
        public Virinco.WATS.Transfer.TransferItemType? ItemType{ get; set; }
        public Guid? ItemId{ get; set; }
        public TimeSpan? TotalTime { get; set; }
        public Guid? Source { get; set; }
        public Guid? Destination { get; set; }
        public string Description { get; set; }
        public string Comment { get; set; }
        public Exception exception { get; set; }
    }

    public class MemberPropset
    {
        public string StationId { get; set; }
        public string Location { get; set; }
        public string Purpose { get; set; }
        public bool IsActivePropset { get; set; }
    }
    public class MemberExtInfo
    {
        public string Key { get; set; }
        public string Value { get; set; }
    }
}
