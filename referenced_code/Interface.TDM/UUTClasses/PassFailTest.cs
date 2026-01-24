extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A pass fail test in a PassFailStep. 
    /// </summary>
    /// <remarks></remarks>
    public class PassFailTest
    {
        internal napi.PassFailTest _instance;
        internal PassFailTest(napi.PassFailTest instance) { _instance = instance; }

        /// <summary>
        /// Measure name (used for multiple values).
        /// </summary>
        public string MeasureName
        {
            get => _instance.MeasureName;
            set => _instance.MeasureName = value;
        }

        /// <summary>
        /// Measure status (used for multiple values)
        /// </summary>
        public bool Passed
        {
            get => _instance.Passed;
            set => _instance.Passed = value;
        }
    }
}
