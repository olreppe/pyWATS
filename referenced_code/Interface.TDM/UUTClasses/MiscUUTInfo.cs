extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represents information that can be connected to a UUT. An example could be firmware version.
    /// </summary>
    public class MiscUUTInfo
    {
        internal napi.MiscUUTInfo _instance;
        internal MiscUUTInfo(napi.MiscUUTInfo instance) { _instance = instance; }

        /// <summary>
        /// The information description, e.g. SWVer1.
        /// Try to keep it short, as it will use space in the WATS database.
        /// </summary>
        public string Description
        {
            get => _instance.Description;
            set => _instance.Description = value;
        }

        /// <summary>
        /// The text value, e.g. 1.15.3.
        /// </summary>
        public string DataString
        {
            get => _instance.DataString;
            set => _instance.DataString = value;
        }

        /// <summary>
        /// The numeric value.
        /// </summary>
        public Int16 DataNumeric
        {
            get => _instance.DataNumeric;
            set => _instance.DataNumeric = value;
        }

        /// <summary>
        /// The number format for the numeric data. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string DataNumericFormat
        {
            get => _instance.DataNumericFormat;
            set => _instance.DataNumericFormat = value;
        }
    }
}
