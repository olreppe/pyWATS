extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS;
using Virinco.WATS.Interface.Models;

namespace Virinco.WATS.Interface
{


    /// <summary>
    /// Repair failcodes, defined in WATS
    /// </summary>
    public class FailCode
    {
        internal napi.FailCode _instance;
        internal FailCode(napi.FailCode instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Unique failcode ID
        /// </summary>
        public Guid Id // r/o
        {
            get => _instance.Id;
            //set => _instance.Id = value;
        }

        /// <summary>
        /// True if this is a selectable failcode, False if it is a failcode category
        /// </summary>
        public bool Selectable // r/o
        {
            get => _instance.Selectable;
            //set => _instance.Selectable = value;
        }

        /// <summary>
        /// Failcode description
        /// </summary>
        public string Description // r/o
        {
            get => _instance.Description;
            //set => _instance.Description = value;
        }

        /// <summary>
        /// Sorting order
        /// </summary>
        public int SortOrder // r/o
        {
            get => _instance.SortOrder;
            //set => _instance.SortOrder = value;
        }

        /// <summary>
        /// For WATS reporting purposes, use this enum
        /// </summary>
        public FailureTypeEnum FailureType
        {
            get { return _instance.FailureType.CastTo<FailureTypeEnum>(); }
        }
    }


    /// <summary>
    /// 
    /// </summary>
    public class FailCodes
    {
        internal napi.FailCodes _instance;
        internal FailCodes(napi.FailCodes instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Returns an array of failcodes on the root level
        /// </summary>
        /// <returns></returns>
        public FailCode[] GetRootFailCodes(RepairType repairType)
            => _instance.GetRootFailCodes(repairType._instance).Select(fc => new FailCode(fc)).ToArray();
        /// <summary>
        /// Get child failcodes of a failcode
        /// </summary>
        /// <param name="failCode"></param>
        /// <returns></returns>
        public FailCode[] GetChildFailCodes(FailCode failCode)
            => _instance.GetChildFailCodes(failCode._instance).Select(fc => new FailCode(fc)).ToArray();
    }


}
