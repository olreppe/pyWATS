extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A string value test in a StringValueStep. 
    /// </summary>
    public class StringValueTest
    {
        internal napi.StringValueTest _instance;
        internal StringValueTest(napi.StringValueTest instance) { _instance = instance; }

        /// <summary>
        /// Comparison operator, see remarks for valid compare types. 
        /// </summary>
        /// <remarks>
        /// <para/><see cref="CompOperatorType.EQ"/> - Equal
        /// <para/><see cref="CompOperatorType.NE"/> - Not equal
        /// <para/><see cref="CompOperatorType.CASESENSIT"/> - Case sensitiv equal
        /// <para/><see cref="CompOperatorType.IGNORECASE"/> - Case insensitiv equal
        /// <para/><see cref="CompOperatorType.LOG"/> - No comparison
        /// </remarks>
        public CompOperatorType CompOperator
        {
            get => _instance.CompOperator.CastTo<CompOperatorType>();
            set => _instance.CompOperator = value.CastTo<napi.CompOperatorType>();
        }

        /// <summary>
        /// If compOperator is EQ, String value is compared
        /// </summary>
        public string StringLimit
        {
            get => _instance.StringLimit;
            set => _instance.StringLimit = value;
        }
        /// <summary>
        /// Measure string value
        /// </summary>
        public string StringValue
        {
            get => _instance.StringValue;
            set => _instance.StringValue = value;
        }

        /// <summary>
        /// Measure name (used for multiple values).
        /// </summary>
        public string MeasureName
        {
            get => _instance.MeasureName;
            set => _instance.MeasureName = value;
        }

        /// <summary>
        /// Measure status enum (used for multiple values)
        /// </summary>
        public StepStatusType MeasureStatus
        {
            get => _instance.MeasureStatus.CastTo<StepStatusType>();
            set => _instance.MeasureStatus = value.CastTo<napi.StepStatusType>();
        }
    }
}
