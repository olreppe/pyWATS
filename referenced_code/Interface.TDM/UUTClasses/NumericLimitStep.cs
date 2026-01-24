extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A numeric limit step will contain one or more <see cref="NumericLimitTest"/>.    
    /// An example of a numeric limit test is to test that the input voltage is within limits.
    /// If there are multiple tests to a step use one of the overloads of <see cref="AddMultipleTest(double,CompOperatorType,double,double,string,string)"/>. 
    /// <example>
    /// uut.RootSequenceCall.AddNumericLimitStep("NumTest").AddTest(231, CompOperatorType.GELE, 235, 233, "V");
    /// </example>
    /// </summary>
    public class NumericLimitStep : Step
    {
        internal napi.NumericLimitStep _instance;
        internal NumericLimitStep(napi.NumericLimitStep instance) : base(instance) { _instance = instance; }

        /// <summary>
        /// Step status
        /// </summary>
        public override StepStatusType Status
        {
            get => _instance.Status.CastTo<StepStatusType>();
            set => _instance.Status = value.CastTo<napi.StepStatusType>();
        }

        /// <summary>
        /// Returns one or more tests belonging to this step (Single/Multiple)
        /// </summary>
        public NumericLimitTest[] Tests
        {
            get => _instance.Tests.Select(t => new NumericLimitTest(t)).ToArray();
            //set { throw new NotImplementedException(); }
        }

        #region Add single tests

        /// <summary>
        /// Adds a numeric limit test with two limits - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="lowLimit">Lower test limit.</param>
        /// <param name="highLimit">Upper test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, CompOperatorType compOperator, double lowLimit, double highLimit, string units)
            => new NumericLimitTest(_instance.AddTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), lowLimit, highLimit, units));

        /// <summary>
        /// Adds a numeric limit test with two limits - without Validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="lowLimit">Lower test limit.</param>
        /// <param name="highLimit">Upper test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, CompOperatorType compOperator, double lowLimit, double highLimit, string units, StepStatusType status)
            => new NumericLimitTest(_instance.AddTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), lowLimit, highLimit, units, status.CastTo<napi.StepStatusType>()));

        /// <summary>
        /// Adds a numeric limit test with one limit - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="limit">Test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, CompOperatorType compOperator, double limit, string units)
            => new NumericLimitTest(_instance.AddTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), limit, units));

        /// <summary>
        /// Adds a numeric limit test with one limit - without validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="limit">Test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, CompOperatorType compOperator, double limit, string units, StepStatusType status)
            => new NumericLimitTest(_instance.AddTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), limit, units, status.CastTo<napi.StepStatusType>()));

        /// <summary>
        /// Adds a numeric limit test without limits, no comparison is done, just log - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="units">Measure units.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, string units)
            => new NumericLimitTest(_instance.AddTest(numericValue, units));

        /// <summary>
        /// Adds a numeric limit test without limits, no comparison is done, just log - without validation.                
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, string units, StepStatusType status)
            => new NumericLimitTest(_instance.AddTest(numericValue, units, status.CastTo<napi.StepStatusType>()));
        #endregion

        #region Add multiple test

        /// <summary>
        /// Adds a multiple numeric limit test with two limits - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="lowLimit">Lower test limit.</param>
        /// <param name="highLimit">Upper test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddMultipleTest(double numericValue, CompOperatorType compOperator, double lowLimit, double highLimit, string units, string measureName)
            => new NumericLimitTest(_instance.AddMultipleTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), lowLimit, highLimit, units, measureName));

        /// <summary>
        /// Adds a multiple numeric limit test with two limits - without validation.
        /// Status will be applied to the step, the test will have Passed or Failed.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="lowLimit">Lower test limit.</param>
        /// <param name="highLimit">Upper test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddMultipleTest(double numericValue, CompOperatorType compOperator, double lowLimit, double highLimit, string units, string measureName, StepStatusType status)
            => new NumericLimitTest(_instance.AddMultipleTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), lowLimit, highLimit, units, measureName, status.CastTo<napi.StepStatusType>()));

        /// <summary>
        /// Adds a multiple numeric limit test with one limit - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="limit">Test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddMultipleTest(double numericValue, CompOperatorType compOperator, double limit, string units, string measureName)
            => new NumericLimitTest(_instance.AddMultipleTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), limit, units, measureName));


        /// <summary>
        /// Adds a multiple numeric limit test with one limit - without validation.
        /// Status will be applied to the step, the test will have Passed or Failed.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="limit">Test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddMultipleTest(double numericValue, CompOperatorType compOperator, double limit, string units, string measureName, StepStatusType status)
            => new NumericLimitTest(_instance.AddMultipleTest(numericValue, compOperator.CastTo<napi.CompOperatorType>(), limit, units, measureName, status.CastTo<napi.StepStatusType>()));

        /// <summary>
        /// Adds a multiple numeric limit test without limits, no comparison is done, just log - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddMultipleTest(double numericValue, string units, string measureName)
            => new NumericLimitTest(_instance.AddMultipleTest(numericValue, units, measureName));

        /// <summary>
        /// Adds a multiple numeric limit test without limits, no comparison is done, just log - without validation.
        /// Status will be applied to the step, the test will have Passed or Failed.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddMultipleTest(double numericValue, string units, string measureName, StepStatusType status)
            => new NumericLimitTest(_instance.AddMultipleTest(numericValue, units, measureName, status.CastTo<napi.StepStatusType>()));
        #endregion
    }
}
