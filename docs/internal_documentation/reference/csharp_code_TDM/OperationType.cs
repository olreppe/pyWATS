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
        internal Models.Process process;
        internal OperationType(Models.Process process)
        {
            this.process = process;
        }
        /// <summary>
        /// Operation type identifier
        /// </summary>
        public Guid Id
        {
            get { return process.ProcessID; }
        }

        /// <summary>
        /// Name of operation type e.g. PCBA test
        /// </summary>
        public string Name
        {
            get { return process.Name; }
        }

        /// <summary>
        /// Code for operation type
        /// </summary>
        public string Code
        {
            get { return process.Code.ToString(); }
        }

        /// <summary>
        /// Description of operation type
        /// </summary>
        public string Description
        {
            get { return process.Description; }
        }
    }
}
