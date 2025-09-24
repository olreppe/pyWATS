using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Interface.Models
{
    public class Codes
    {
        public Code[] codes { get; set; }
        public Process[] processes { get; set; }
    }
    public enum CodeType { Status, StepGroup, StepType }
    public class Code
    {
        public CodeType codetype { get; set; }
        public int enum_value { get; set; }
        public Guid GUID { get; set; }
        public string Description { get; set; }
        public string RelatedTable { get; set; }
    }

    // Is equal to Virinco.WATS.RecordState, but needs to be included with Codes.cs!!!
    public enum ProcessRecordState { Inactive = 0x00, Active = 0x01, Deleted = 0x02 }

    public class Process
    {
        public Guid GUID { get; set; }
        public short Code { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public ProcessRecordState State { get; set; }
        public int? ProcessIndex { get; set; }
        public bool IsTestOperation { get; set; }
        public bool IsWIPOperation { get; set; }
        public bool IsRepairOperation { get; set; }
        public ProcessProperties Properties { get; set; }
    }
    
    public abstract class ProcessProperties { }

    /* RepairType class based on/copied from ControlPanel/Views/UserControl/RepairOperation.xaml.cs */
    public class RepairType : ProcessProperties
    {
        //public string Code { get; set; } //Code == Process' Code
        public string Description { get; set; }
        public bool UUTRequired { get; set; }
        public string CompRefMask { get; set; }
        public string CompRefMaskDescription { get; set; }
        public string BomConstraint { get; set; }
        //public int Status { get; set; }
        public Failcode[] Categories { get; set; }
        public MiscInfo[] MiscInfos { get; set; }
    }

    public class Failcode 
    {
        public Guid GUID { get; set; }
        public bool Selectable { get; set; }
        public string Description { get; set; }
        public int SortOrder { get; set; }
        public int FailureType { get; set; }
        public string ImageConstraint { get; set; }
        public int Status { get; set; }
        public Failcode[] Failcodes { get; set; }
    }

    public class MiscInfo 
    {
        public Guid GUID { get; set; }
        public string Description { get; set; }
        public string InputMask { get; set; }
        public string ValidRegex { get; set; }
        public int Status { get; set; }
    }
}
