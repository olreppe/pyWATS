extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.Xml.XPath;

namespace Virinco.WATS.Interface
{

    /// <summary>
    /// A repair type is a set of fail-codes. e.g. Module Repair has a different set of failcodes than System Repair
    /// </summary>
    public class RepairType
    {
        internal napi.RepairType _instance;
        internal RepairType(napi.RepairType instance)
        {
            _instance = instance;
        }

        /// <remarks>Code of repair type</remarks>
        public Int16 Code // r/o
        {
            get => _instance.Code;
            //set => _instance.Code = value;
        }

        /// <remarks>Name of repair type</remarks>
        public string Name // r/o
        {
            get => _instance.Name;
            //set => _instance.Name = value;
        }

        /// <remarks>Description of repair type</remarks>
        public string Description // r/o
        {
            get => _instance.Description;
            //set => _instance.Description = value;
        }

        /// <summary>
        /// Repair type identifier
        /// </summary>
        public Guid Id // r/o
        {
            get => _instance.Id;
            //set => _instance.Id = value;
        }

        /// <summary>
        /// True if repair type requires an UUT Id
        /// </summary>
        public bool UUTRequired // r/o
        {
            get => _instance.UUTRequired;
            //set => _instance.UUTRequired = value;
        }


        /// <summary>
        /// A regular expression that validates a  valid component reference
        /// </summary>
        public string ComponentReferenceMask // r/o
        {
            get => _instance.ComponentReferenceMask;
            //set => _instance.ComponentReferenceMask = value;
        }

        /// <summary>
        /// Description of a ComponentReferenceMask
        /// </summary>
        public string ComponentReferenceMaskDescription // r/o
        {
            get => _instance.ComponentReferenceMaskDescription;
            //set => _instance.ComponentReferenceMaskDescription = value;
        }
    }
}
