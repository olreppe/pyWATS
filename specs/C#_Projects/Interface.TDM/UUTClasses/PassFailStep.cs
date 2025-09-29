using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

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
        private readonly List<PassFailTest> tests;

        internal bool IsSingle { get; private set; } = false;

        internal bool IsMultiple { get; private set; } = false;

        internal PassFailStep(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName) 
            : base(uut, reportRow, parentStep, stepName)
        {
            tests = new List<PassFailTest>();

            //Assume single pass fail
            stepRow.StepType = StepTypeEnum.ET_PFT.ToString(); 
        }

        internal PassFailStep(Step_type step, WATSReport reportRow, PassFail_type[] passFails, UUTReport uut) 
            : base(step, reportRow, uut)
        {
            tests = passFails.Select(t => new PassFailTest(t, this, uut)).ToList();
            measureIndex = (short)tests.Count;

            if (tests.Any())
            {
                IsSingle = tests.Count == 1 && string.IsNullOrEmpty(tests.First().MeasureName);
                IsMultiple = !IsSingle;
            }
        }

        /// <summary>
        /// Step status
        /// </summary>
        public override StepStatusType Status
        {
            get => base.Status;
            set
            {
                if (IsSingle)
                {
                    if (tests.Count > 0)
                    {
                        var v = value;
                        if (v == StepStatusType.Done)
                            v = StepStatusType.Passed;

                        tests[0].Passed = StepStatusType.Passed == v;
                    }
                }
                base.Status = value;
            }
        }

        /// <summary>
        /// Returns one or more tests belonging to this step (Single/Multiple)
        /// </summary>
        public PassFailTest[] Tests
        {
            get { return tests.ToArray(); }
            //set { throw new NotImplementedException(); }
        }

        public PassFailTest AddSingleTest()
        {
            if (IsMultiple)
                throw new InvalidOperationException("Cannot add single test to multiple test step.");

            if (tests.Any())
                throw new InvalidOperationException("Cannot add multiple single tests to single test step.");

            IsSingle = true;
            var t = AddTestPrivate();

            return t;
        }

        private PassFailTest AddMultipleTest(string measureName)
        {
            if (IsSingle)
                throw new InvalidOperationException("Cannot add multiple test to single test step.");

            if (!IsMultiple)
                StepType = StepTypeEnum.ET_MPFT.ToString();

            IsMultiple = true;
            var test = AddTestPrivate();

            test.MeasureName = measureName;

            return test;
        }

        private PassFailTest AddTestPrivate()
        {
            PassFailTest t = new PassFailTest(report, this, StepOrderNumber, measureIndex, report.GetNextMeasOrder());
            tests.Add(t);
            measureIndex++;
            return t;
        }

        #region Add single tests

        [Obsolete]
        public PassFailTest AddTest()
        {
            return AddSingleTest();
        }

        /// <summary>
        /// Adds a pass fail test - with validation. 
        /// </summary>
        /// <param name="passed">Measured value.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddTest(bool passed)
        {
            var t = AddSingleTest();
            t.Passed = passed;
            
            if (!passed)
                base.Status = StepStatusType.Failed;

            return t;
        }

        /// <summary>
        /// Adds a pass fail test - without validation. 
        /// </summary>
        /// <param name="passed">Measured value.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddTest(bool passed, StepStatusType status)
        {
            PassFailTest t = AddSingleTest();
            t.Passed = passed;

            base.Status = status;

            return t;
        }

        #endregion

        #region Add multiple tests

        /// <summary>
        /// Adds a multiple pass fail test - with validation.
        /// </summary>
        /// <param name="passed">Measure value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddMultipleTest(bool passed, string measureName)
        {
            PassFailTest t = AddMultipleTest(measureName);
            t.Passed = passed;

            if (!passed)
                base.Status = StepStatusType.Failed;

            return t;
        }

        /// <summary>
        /// Adds a multiple pass fail test - without validation.
        /// Status will be applied to the step, the test will have Passed or Failed.
        /// </summary>        
        /// <param name="passed">Measured value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public PassFailTest AddMultipleTest(bool passed, string measureName, StepStatusType status)
        {
            PassFailTest t = AddMultipleTest(measureName);
            t.Passed = passed;  
            
            ApplyMultipleStatusToStep(status);

            return t;
        }

        #endregion

        protected internal override void RemoveStepData()
        {
            base.RemoveStepData();
            reportRow.Items.RemoveAll(o => o is PassFail_type p && p.StepID == stepRow.StepID);

            tests.Clear();
            measureIndex = 0;
            IsSingle = false;
            IsMultiple = false;
        }
    }
}
