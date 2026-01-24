extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represent a call to external program.
    /// </summary>
    public class CallExeStep : Step
    {
        internal napi.CallExeStep _instance;
        internal CallExeStep(napi.CallExeStep instance) : base(instance) { _instance = instance; }

        /// <summary>
        /// Exit code of the executable.
        /// </summary>
        public double ExitCode
        {
            get => _instance.ExitCode;
            set => _instance.ExitCode = value;
        }

        /// <summary>
        /// The number format for the exit code. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ExitCodeFormat
        {
            get => _instance.ExitCodeFormat;
            set => _instance.ExitCodeFormat = value;
        }
    }
}
