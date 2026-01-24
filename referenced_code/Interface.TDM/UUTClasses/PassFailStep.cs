extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A pass fail step will contain one or more <see cref="PassFailTest"/>.
    /// If there are multiple tests to a step use one of the overloads of <see cref="AddMultipleTest(bool, string)"/>. 
    /// <example>
    /// uut.RootSequenceCall.AddPassFailStep("PassFailTest").AddTest(false);
    /// </example>
    /// </summary>
    public class PassFailStep : Step
    {
        internal napi.PassFailStep _instance;
        internal PassFailStep(napi.PassFailStep instance) : base(instance) { _instance = instance; }

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
        public PassFailTest[] Tests // r/o
        {
            get => _instance.Tests.Select(t => new PassFailTest(t)).ToArray();
            //set => _instance.Tests = value.Select(t => t._instance).ToArray();
        }

        public PassFailTest AddSingleTest()
            => new PassFailTest(_instance.AddSingleTest());


        #region Add single tests
        /// <summary>
        /// Adds a pass fail test - with validation. 
        /// </summary>
        /// <param name="passed">Measured value.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddTest(bool passed)
            => new PassFailTest(_instance.AddTest(passed));

        /// <summary>
        /// Adds a pass fail test - without validation. 
        /// </summary>
        /// <param name="passed">Measured value.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddTest(bool passed, StepStatusType status)
            => new PassFailTest(_instance.AddTest(passed, status.CastTo<napi.StepStatusType>()));

        #endregion

        #region Add multiple tests

        /// <summary>
        /// Adds a multiple pass fail test - with validation.
        /// </summary>
        /// <param name="passed">Measure value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddMultipleTest(bool passed, string measureName)
            => new PassFailTest(_instance.AddMultipleTest(passed, measureName));

        /// <summary>
        /// Adds a multiple pass fail test - without validation.
        /// Status will be applied to the step, the test will have Passed or Failed.
        /// </summary>        
        /// <param name="passed">Measured value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddMultipleTest(bool passed, string measureName, StepStatusType status)
            => new PassFailTest(_instance.AddMultipleTest(passed, measureName, status.CastTo<napi.StepStatusType>()));
        #endregion
    }
}
