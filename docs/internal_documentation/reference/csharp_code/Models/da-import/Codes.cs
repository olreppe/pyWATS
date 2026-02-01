using System;

namespace Virinco.WATS.Interface.Models
{
    /*public class Codes
    {
        public Code[] codes { get; set; }
        public Process[] processes { get; set; }
    }*/
    public enum CodeType : Int16 { Status = 1, StepGroup = 2, StepType = 3 }
    public class Code
    {
        public CodeType codetype { get; set; }
        public Int16 enum_value { get; set; }
        public Guid GUID { get; set; }
        public string Description { get; set; }
        public string RelatedTable { get; set; }
    }

    // Is equal to Virinco.WATS.RecordState, but needs to be included with Codes.cs!!!
    public enum ProcessRecordState { Inactive = 0x00, Active = 0x01, Deleted = 0x02 }

    public class Process
    {
        public Guid ProcessID { get; set; }
        public short Code { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public ProcessRecordState State { get; set; }
        public int? ProcessIndex { get; set; }
        public bool IsTestOperation { get; set; }
        public bool IsWIPOperation { get; set; }
        public bool IsRepairOperation { get; set; }
        public RepairType Properties { get; set; }
    }

    /* RepairType class based on/copied from ControlPanel/Views/UserControl/RepairOperation.xaml.cs */
    public class RepairType
    {
        //public string Code { get; set; } //Code == Process' Code
        public string Description { get; set; }
        public int UUTRequired { get; set; } = (int)RequirementConstraint.Optional;
        public string CompRefMask { get; set; }
        public string CompRefMaskDescription { get; set; }
        [Obsolete]
        public string BomConstraint { get; set; }
        public int BOMRequired { get; set; } = (int)RequirementConstraint.Optional;
        public int VendorRequired { get; set; } = (int)RequirementConstraint.Never;
        //public int Status { get; set; }
        public Failcode[] Categories { get; set; }
        public MiscInfo[] MiscInfos { get; set; }

        internal static RepairType Parse(string v)
        {
            if (string.IsNullOrEmpty(v)) return null;
            var reader = new System.IO.StringReader(v);
            System.Xml.Serialization.XmlSerializer ser = new System.Xml.Serialization.XmlSerializer(typeof(RepairType));
            var repairType = (RepairType)ser.Deserialize(reader);

            if(repairType.MiscInfos != null)
            {
                const string regexAll = ".*";
                foreach (var miscInfo in repairType.MiscInfos)
                {
                    if (string.IsNullOrEmpty(miscInfo.InputMask))
                        miscInfo.InputMask = regexAll;
                    if (string.IsNullOrEmpty(miscInfo.ValidRegex))
                        miscInfo.ValidRegex = regexAll;
                }
            }

            return repairType;
        }
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
