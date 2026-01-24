extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A numeric test in a NumericLimitStep.
    /// </summary>
    public class NumericLimitTest
    {
        internal napi.NumericLimitTest _instance;
        internal NumericLimitTest(napi.NumericLimitTest instance) { _instance = instance; }

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
            get => _instance.CompOperator.CastTo<CompOperatorType>();
            set => _instance.CompOperator = value.CastTo<napi.CompOperatorType>();
        }

        /// <summary>
        /// Comparision limit (High).
        /// </summary>
        public double HighLimit
        {
            get => _instance.HighLimit;
            set => _instance.HighLimit = value;
        }

        /// <summary>
        /// The number format for the high limit. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string HighLimitFormat
        {
            get => _instance.HighLimitFormat;
            set => _instance.HighLimitFormat = value;
        }

        /// <summary>
        /// Comparision limit (Low)
        /// </summary>
        public double LowLimit
        {
            get => _instance.LowLimit;
            set => _instance.LowLimit = value;
        }

        /// <summary>
        /// The number format for the low limit. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string LowLimitFormat
        {
            get => _instance.LowLimitFormat;
            set => _instance.LowLimitFormat = value;
        }

        /// <summary>
        /// Numeric result unit
        /// </summary>
        public string Units
        {
            get => _instance.Units;
            set => _instance.Units = value;
        }

        /// <summary>
        /// Measured value.
        /// </summary>
        public double NumericValue
        {
            get => _instance.NumericValue;
            set => _instance.NumericValue = value;
        }

        /// <summary>
        /// The number format for the numeric value. Uses C printf style number format.
        /// Example: Integer: %i, Hexadecimal: %#x, With 3 decimals: %.3f
        /// </summary>
        public string NumericValueFormat
        {
            get => _instance.NumericValueFormat;
            set => _instance.NumericValueFormat = value;
        }

        /// <summary>
        /// Measure name (used for multiple values)
        /// </summary>
        public string MeasureName
        {
            get => _instance.MeasureName;
            set => _instance.MeasureName = value;
        }

        /// <summary>
        /// Measure status enum (used for multiple tests).
        /// </summary>
        public StepStatusType MeasureStatus
        {
            get => _instance.MeasureStatus.CastTo<StepStatusType>();
            set => _instance.MeasureStatus = value.CastTo<napi.StepStatusType>();
        }
    }
}
