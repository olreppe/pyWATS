using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{    
    /// <summary>
    /// A numeric test in a NumericLimitStep.
    /// </summary>
    public class NumericLimitTest
    {
        private readonly NumericLimit_type testRow;
        private readonly UUTReport report;
        private readonly NumericLimitStep step;

        internal NumericLimitTest(NumericLimit_type testRow, UUTReport report, NumericLimitStep step)
        {
            this.testRow = testRow;
            this.report = report;
            this.step = step;
        }

        internal NumericLimitTest(UUTReport uut, NumericLimitStep nls, int stepOrder, int measIndex, short measOrder)
        {
            testRow = new NumericLimit_type()
            {
                StepID = stepOrder,
                MeasIndex = measIndex,
                MeasOrderNumber = measOrder,
                Status = MeasurementResultType.Passed
            };

            report = uut;
            step = nls;
            report.reportRow.Items.Add(testRow);
        }

        /// <summary>
        /// Comparison operator, see remarks for valid compare types.
        /// </summary>
        /// <remarks>
        /// <para/><see cref="CompOperatorType.EQ"/> - Equal
        /// <para/><see cref="CompOperatorType.NE"/> - Not equal
        /// <para/><see cref="CompOperatorType.GT"/> - Greater than
        /// <para/><see cref="CompOperatorType.LT"/> - Less than
        /// <para/><see cref="CompOperatorType.GE"/> - Greater than or equal
        /// <para/><see cref="CompOperatorType.LE"/> - Less than or equal
        /// <para/><see cref="CompOperatorType.GTLT"/> - Between, exclusive
        /// <para/><see cref="CompOperatorType.GELE"/> - Between, inclusive
        /// <para/><see cref="CompOperatorType.GELT"/> - Between, inclusive low, exclusive high
        /// <para/><see cref="CompOperatorType.GTLE"/> - Between, exclusive low, inclusive high
        /// <para/><see cref="CompOperatorType.LTGT"/> - Not between, exclusive
        /// <para/><see cref="CompOperatorType.LEGE"/> - Not between, inclusive
        /// <para/><see cref="CompOperatorType.LEGT"/> - Not between, inclusive low, exclusive high
        /// <para/><see cref="CompOperatorType.LTGE"/> - Not between, exclusive low, inclusive high
        /// <para/><see cref="CompOperatorType.LOG"/> - No comparison
        /// </remarks>
        public CompOperatorType CompOperator
        {
            get => Utilities.EnumTryParse(testRow.CompOperator, out CompOperatorType op) ? op : CompOperatorType.LOG;
            set => testRow.CompOperator = value.ToString();
        }

        /// <summary>
        /// Comparision limit (High).
        /// </summary>
        public double HighLimit
        {
            get => testRow.HighLimitSpecified ? testRow.HighLimit : double.MaxValue;
            set
            {
                testRow.HighLimit = value;
                testRow.HighLimitSpecified = true;
            }
        }

        /// <summary>
        /// The number format for the high limit. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string HighLimitFormat
        {
            get => testRow.HighLimitFormat;
            set => testRow.HighLimitFormat = value;
        }

        /// <summary>
        /// Comparision limit (Low)
        /// </summary>
        public double LowLimit
        {
            get => testRow.LowLimitSpecified ? testRow.LowLimit : double.MinValue;
            set 
            { 
                testRow.LowLimit = value; 
                testRow.LowLimitSpecified = true; 
            }
        }

        /// <summary>
        /// The number format for the low limit. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string LowLimitFormat
        {
            get => testRow.LowLimitFormat;
            set => testRow.LowLimitFormat = value;
        }

        /// <summary>
        /// Numeric result unit
        /// </summary>
        public string Units
        {
            get => testRow.Units;
            set => testRow.Units = report.api.SetPropertyValidated<NumericLimit_type>(nameof(NumericLimit_type.Units), value, nameof(Units));
        }

        /// <summary>
        /// Measured value.
        /// </summary>
        public double NumericValue
        {
            get => testRow.NumericValue;
            set => testRow.NumericValue = value;
        }

        /// <summary>
        /// The number format for the numeric value. Uses C printf style number format.
        /// Example: Integer: %i, Hexadecimal: %#x, With 3 decimals: %.3f
        /// </summary>
        public string NumericValueFormat
        {
            get => testRow.NumericValueFormat;
            set => testRow.NumericValueFormat = value;
        }

        /// <summary>
        /// Measure name (used for multiple values)
        /// </summary>
        public string MeasureName
        {
            get => testRow.Name;
            set 
            {
                if (step.IsMultiple)
                {
                    if (value == null)
                        throw new ArgumentNullException(nameof(MeasureName));
                    else if (value == string.Empty)
                        throw new ArgumentException("Cannot be empty", nameof(MeasureName));
                    else
                        testRow.Name = report.api.SetPropertyValidated<NumericLimit_type>(nameof(NumericLimit_type.Name), value, nameof(MeasureName));
                }
                else
                    throw new InvalidOperationException($"Cannot set {nameof(MeasureName)} on a single test");
            }
        }

        /// <summary>
        /// Measure status enum (used for multiple tests).
        /// </summary>
        public StepStatusType MeasureStatus
        {
            get
            {
                if (testRow.Status == MeasurementResultType.Passed)
                    return StepStatusType.Passed;
                if (testRow.Status == MeasurementResultType.Failed)
                    return StepStatusType.Failed;
                if (testRow.Status == MeasurementResultType.Skipped)
                    return StepStatusType.Skipped;
                return StepStatusType.Skipped;
            }
            set
            {
                if (!Utilities.EnumTryParse(value.ToString(), out MeasurementResultType status))
                    throw new ApplicationException("Not recognized status value.");

                testRow.Status = status;
            }
        }
    }
}
