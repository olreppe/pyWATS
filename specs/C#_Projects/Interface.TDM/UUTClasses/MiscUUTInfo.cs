using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represents information that can be connected to a UUT. An example could be firmware version.
    /// </summary>
    public class MiscUUTInfo
    {
        readonly MiscInfo_type miscRow;
        readonly UUTReport report;

        internal MiscUUTInfo(MiscInfo_type miscInfoRow, UUTReport uut)
        {
            miscRow = miscInfoRow;
            report = uut;
        }

        /// <summary>
        /// The information description, e.g. SWVer1.
        /// Try to keep it short, as it will use space in the WATS database.
        /// </summary>
        public string Description
        {
            get { return miscRow.Description; }
            set { miscRow.Description = report.api.SetPropertyValidated<MiscInfo_type>("Description", value); }
        }

        /// <summary>
        /// The text value, e.g. 1.15.3.
        /// </summary>
        public string DataString
        {
            get { return miscRow.Value; }
            set { miscRow.Value = report.api.SetPropertyValidated<MiscInfo_type>("Value", value,"DataString"); }
        }

        /// <summary>
        /// The numeric value.
        /// </summary>
        public Int16 DataNumeric
        {
            get { return miscRow.NumericSpecified ? miscRow.Numeric : (Int16)0; }
            set { miscRow.Numeric = value; miscRow.NumericSpecified = true; }
        }

        /// <summary>
        /// The number format for the numeric data. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string DataNumericFormat
        {
            get => miscRow.NumericFormat;
            set => miscRow.NumericFormat = value;
        }
    }
}
