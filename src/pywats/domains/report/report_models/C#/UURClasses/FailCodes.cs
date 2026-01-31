using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS;
using System.Data;
using Virinco.WATS.Interface.Models;

namespace Virinco.WATS.Interface
{


    /// <summary>
    /// Repair failcodes, defined in WATS
    /// </summary>
    public class FailCode
    {
        internal Models.Failcode fc;
        internal FailCode(Models.Failcode fc)
        {
            this.fc = fc;
        }
        /// <summary>
        /// Unique failcode ID
        /// </summary>
        public Guid Id
        {
            get { return fc.GUID; }
        }

        /// <summary>
        /// True if this is a selectable failcode, False if it is a failcode category
        /// </summary>
        public bool Selectable
        {
            get { return fc.Status > 0; }
        }

        /// <summary>
        /// Failcode description
        /// </summary>
        public string Description
        {
            get { return fc.Description; }
        }

        /// <summary>
        /// Sorting order
        /// </summary>
        public int SortOrder
        {
            get { return fc.SortOrder; }
        }

        /// <summary>
        /// For WATS reporting purposes, use this enum
        /// </summary>
        public FailureTypeEnum FailureType
        {
            get { return (FailureTypeEnum)fc.FailureType; }
        }

    }


    /// <summary>
    /// 
    /// </summary>
    public class FailCodes
    {
        //private Codes.FailcodeDataTable failCodes;
        private IEnumerable<Process> repairProcesses;
        internal FailCodes(IEnumerable<Process> Processes)
        {
            this.repairProcesses = Processes.Where(p => p.IsRepairOperation);
        }

        /// <summary>
        /// Returns an array of failcodes on the root level
        /// </summary>
        /// <returns></returns>
        public FailCode[] GetRootFailCodes(RepairType repairType)
        {
            return repairType.repairtype.Categories.Select(fc=>new FailCode(fc)).ToArray();
        }

        /// <summary>
        /// Get child failcodes of a failcode
        /// </summary>
        /// <param name="failCode"></param>
        /// <returns></returns>
        public FailCode[] GetChildFailCodes(FailCode failCode)
        {
            return failCode.fc.Failcodes.Select(fc => new FailCode(fc)).ToArray();
        }
        /*
        internal FailCode GetFailCode(Guid failCodeId)
        {
            repairProcesses.
            FailCode f = new FailCode();
            Codes.FailcodeRow r = failCodes.FindByGUID(failCodeId);
            copyTableToObject(r, f);
            return f;
        }
        */
    }
    

}
