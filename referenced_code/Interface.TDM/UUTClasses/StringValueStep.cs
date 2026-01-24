extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A string value step will contain one or more <see cref="StringValueTest"/>.
    /// If there are multiple tests to a step use one of the overloads of <see cref="AddMultipleTest(CompOperatorType, string, string, string)"/>. 
    /// <example>
    /// uut.RootSequenceCall.AddStringValueStep("StringTest").AddTest(CompOperatorType.GELE, "value", "limit");
    /// </example>
    /// </summary>
    public class StringValueStep : Step
    {
        internal napi.StringValueStep _instance;
        internal StringValueStep(napi.StringValueStep instance) : base(instance) { _instance = instance; }

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
        public StringValueTest[] Tests // r/o
        {
            get => _instance.Tests.Select(test => new StringValueTest(test)).ToArray();
            //set { throw new NotImplementedException(); }
        }


        #region Add single tests

        /// <summary>
        /// Adds a string value test - with validation. 
        /// </summary>
        /// <param name="compOperator">Type of comparison. See <see cref="StringValueTest.CompOperator"/> for valid values.</param>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="stringLimit">Test limit.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddTest(CompOperatorType compOperator, string stringValue, string stringLimit)
            => new StringValueTest(_instance.AddTest(compOperator.CastTo<napi.CompOperatorType>(), stringValue, stringLimit));

        /// <summary>
        /// Adds a string value test - without validation. 
        /// </summary>
        /// <param name="compOperator">Type of comparison. See <see cref="StringValueTest.CompOperator"/> for valid values.</param>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="stringLimit">Test limit.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddTest(CompOperatorType compOperator, string stringValue, string stringLimit, StepStatusType status)
            => new StringValueTest(_instance.AddTest(compOperator.CastTo<napi.CompOperatorType>(), stringValue, stringLimit, status.CastTo<napi.StepStatusType>()));

        /// <summary>
        /// Adds a string value test without limit, no comparison is done, just log - with validation. 
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddTest(string stringValue)
            => new StringValueTest(_instance.AddTest(stringValue));

        /// <summary>
        /// Adds a string value test without limit, no comparison is done, just log - without validation. 
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddTest(string stringValue, StepStatusType status)
            => new StringValueTest(_instance.AddTest(stringValue, status.CastTo<napi.StepStatusType>()));

        #endregion

        #region Add multiple tests

        /// <summary>
        /// Adds a multiple string value test with limit - with validation.
        /// </summary>
        /// <param name="compOperator">Type of comparison. See <see cref="StringValueTest.CompOperator"/> for valid values.</param>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="stringLimit">Test limit.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddMultipleTest(CompOperatorType compOperator, string stringValue, string stringLimit, string measureName)
                    => new StringValueTest(_instance.AddMultipleTest(compOperator.CastTo<napi.CompOperatorType>(), stringValue, stringLimit, measureName));

        /// <summary>
        /// Adds a multiple string value test with limit - without validation.
        /// Status will be applied to the step, the test will have Passed or Failed.
        /// </summary>
        /// <param name="compOperator">Type of comparison. See <see cref="StringValueTest.CompOperator"/> for valid values.</param>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="stringLimit">Test limit.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddMultipleTest(CompOperatorType compOperator, string stringValue, string stringLimit, string measureName, StepStatusType status)
            => new StringValueTest(_instance.AddMultipleTest(compOperator.CastTo<napi.CompOperatorType>(), stringValue, stringLimit, measureName, status.CastTo<napi.StepStatusType>()));

        /// <summary>
        /// Adds a multiple string value test without limit, no comparison is done, just log - with validation.
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddMultipleTest(string stringValue, string measureName)
            => new StringValueTest(_instance.AddMultipleTest(stringValue, measureName));

        /// <summary>
        /// Adds a multiple string value test without limit, no comparison is done, just log - without validation.
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddMultipleTest(string stringValue, string measureName, StepStatusType status)
            => new StringValueTest(_instance.AddMultipleTest(stringValue, measureName, status.CastTo<napi.StepStatusType>()));

        #endregion

    }
}
