extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Linq;

namespace Virinco.WATS.Interface.Models
{
    /*public class Codes
    {
        public Code[] codes { get; set; }
        public Process[] processes { get; set; }
    }*/
    /*
    // Code class is not referenced by any reachable internal code - removed from 7.0
    public enum CodeType : Int16 { Status = 1, StepGroup = 2, StepType = 3 }
    public class Code
    {
        public CodeType codetype { get; set; }
        public Int16 enum_value { get; set; }
        public Guid GUID { get; set; }
        public string Description { get; set; }
        public string RelatedTable { get; set; }
    }
    */
    // Is equal to Virinco.WATS.RecordState, but needs to be included with Codes.cs!!!
    public enum ProcessRecordState { Inactive = 0x00, Active = 0x01, Deleted = 0x02 }

    public class Process
    {
        internal napi.Models.Process _instance;
        internal Process(napi.Models.Process instance) { _instance = instance; }

        public Guid ProcessID
        {
            get => _instance.ProcessID;
            set => _instance.ProcessID = value;
        }
        public short Code
        {
            get => _instance.Code;
            set => _instance.Code = value;
        }
        public string Name
        {
            get => _instance.Name;
            set => _instance.Name = value;
        }
        public string Description
        {
            get => _instance.Description;
            set => _instance.Description = value;
        }
        public ProcessRecordState State
        {
            get => _instance.State.CastTo<ProcessRecordState>();
            set => _instance.State = value.CastTo<napi.Models.ProcessRecordState>();
        }
        public int? ProcessIndex
        {
            get => _instance.ProcessIndex;
            set => _instance.ProcessIndex = value;
        }
        public bool IsTestOperation
        {
            get => _instance.IsTestOperation;
            set => _instance.IsTestOperation = value;
        }
        public bool IsWIPOperation
        {
            get => _instance.IsWIPOperation;
            set => _instance.IsWIPOperation = value;
        }
        public bool IsRepairOperation
        {
            get => _instance.IsRepairOperation;
            set => _instance.IsRepairOperation = value;
        }
        public RepairType Properties
        {
            get => new RepairType(_instance.Properties);
            set => _instance.Properties = value._instance;
        }
    }

    /* RepairType class based on/copied from ControlPanel/Views/UserControl/RepairOperation.xaml.cs */
    public class RepairType
    {
        internal napi.Models.RepairType _instance;
        internal RepairType(napi.Models.RepairType instance) { _instance = instance; }

        //public string Code { get; set; } //Code == Process' Code
        public string Description
        {
            get => _instance.Description;
            set => _instance.Description = value;
        }
        public int UUTRequired
        {
            get => _instance.UUTRequired;
            set => _instance.UUTRequired = value;
        }
        public string CompRefMask
        {
            get => _instance.CompRefMask;
            set => _instance.CompRefMask = value;
        }
        public string CompRefMaskDescription
        {
            get => _instance.CompRefMaskDescription;
            set => _instance.CompRefMaskDescription = value;
        }
        [Obsolete]
        public string BomConstraint
        {
            get => _instance.BomConstraint;
            set => _instance.BomConstraint = value;
        }
        public int BOMRequired
        {
            get => _instance.BOMRequired;
            set => _instance.BOMRequired = value;
        }
        public int VendorRequired
        {
            get => _instance.VendorRequired;
            set => _instance.VendorRequired = value;
        }

        public Failcode[] Categories
        {
            get => _instance.Categories.Select(fc => new Failcode(fc)).ToArray();
            set => _instance.Categories = value.Select(fc => fc._instance).ToArray();
        }
        public MiscInfo[] MiscInfos
        {
            get => _instance.MiscInfos.Select(mi => new MiscInfo(mi)).ToArray();
            set => _instance.MiscInfos = value.Select(mi => mi._instance).ToArray();
        }

    }

    public class Failcode
    {
        internal napi.Models.Failcode _instance;
        internal Failcode(napi.Models.Failcode instance) { _instance = instance; }

        public Guid GUID
        {
            get => _instance.GUID;
            set => _instance.GUID = value;
        }
        public bool Selectable
        {
            get => _instance.Selectable;
            set => _instance.Selectable = value;
        }
        public string Description
        {
            get => _instance.Description;
            set => _instance.Description = value;
        }
        public int SortOrder
        {
            get => _instance.SortOrder;
            set => _instance.SortOrder = value;
        }
        public int FailureType
        {
            get => _instance.FailureType;
            set => _instance.FailureType = value;
        }
        public string ImageConstraint
        {
            get => _instance.ImageConstraint;
            set => _instance.ImageConstraint = value;
        }
        public int Status
        {
            get => _instance.Status;
            set => _instance.Status = value;
        }
        public Failcode[] Failcodes
        {
            get => _instance.Failcodes.Select(fc => new Failcode(fc)).ToArray();
            set => _instance.Failcodes = value.Select(fc => fc._instance).ToArray();
        }
    }

    public class MiscInfo
    {
        internal napi.Models.MiscInfo _instance;
        internal MiscInfo(napi.Models.MiscInfo instance) { _instance = instance; }

        public Guid GUID
        {
            get => _instance.GUID;
            set => _instance.GUID = value;
        }
        public string Description
        {
            get => _instance.Description;
            set => _instance.Description = value;
        }
        public string InputMask
        {
            get => _instance.InputMask;
            set => _instance.InputMask = value;
        }
        public string ValidRegex
        {
            get => _instance.ValidRegex;
            set => _instance.ValidRegex = value;
        }
        public int Status
        {
            get => _instance.Status;
            set => _instance.Status = value;
        }
    }
}
