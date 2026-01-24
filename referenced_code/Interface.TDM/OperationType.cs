extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// This class represents a type of test defined in WATS
    /// </summary>
    public class OperationType
    {
        internal napi.OperationType _instance;

        internal OperationType(napi.OperationType instance) { _instance = instance; }

        /// <summary>
        /// Operation type identifier
        /// </summary>
        public Guid Id // r/o
        {
            get => _instance.Id;
            //set => _instance.Id = value;
        }

        /// <summary>
        /// Name of operation type e.g. PCBA test
        /// </summary>
        public string Name // r/o
        {
            get => _instance.Name;
            //set => _instance.Name = value;
        }

        /// <summary>
        /// Code for operation type
        /// </summary>
        public string Code // r/o
        {
            get => _instance.Code;
            //set => _instance.Code = value;
        }

        /// <summary>
        /// Description of operation type
        /// </summary>
        public string Description // r/o
        {
            get => _instance.Description;
            //set => _instance.Description = value;
        }
    }
}
