using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

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
        private readonly List<StringValueTest> tests;

        internal bool IsSingle { get; private set; } = false;

        internal bool IsMultiple { get; private set; } = false;

        internal StringValueStep(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName) 
            : base(uut, reportRow, parentStep, stepName)
        {
            tests = new List<StringValueTest>();

            //Assume single string value
            stepRow.StepType = StepTypeEnum.ET_SVT.ToString();
        }

        internal StringValueStep(Step_type step, WATSReport reportRow, StringValue_type[] stringValues, UUTReport uut) 
            : base(step, reportRow, uut)
        {
            tests = stringValues.Select(t => new StringValueTest(t, uut, this)).ToList();
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

                        tests[0].MeasureStatus = GetMeasureStatusFromExplicitStepStatus(v);
                    }
                }
                base.Status = value;
            }
        }

        /// <summary>
        /// Returns one or more tests belonging to this step (Single/Multiple)
        /// </summary>
        public StringValueTest[] Tests
        {
            get { return tests.ToArray(); }
            //set { throw new NotImplementedException(); }
        }

        private StringValueTest AddSingleTest()
        {
            if (IsMultiple)
                throw new InvalidOperationException("Cannot add single test to multiple test step.");

            if (tests.Any())
                throw new InvalidOperationException("Cannot add multiple single tests to single test step.");

            IsSingle = true;
            var t = AddTest();

            return t;
        }

        private StringValueTest AddMultipleTest(string measureName)
        {
            if (IsSingle)
                throw new InvalidOperationException("Cannot add multiple test to single test step.");

            if (!IsMultiple)
                StepType = StepTypeEnum.ET_MSVT.ToString();

            IsMultiple = true;
            var test = AddTest();

            test.MeasureName = measureName;

            return test;
        }

        private StringValueTest AddTest()
        {            
            StringValueTest t = new StringValueTest(report, this, StepOrderNumber, measureIndex, report.GetNextMeasOrder());
            tests.Add(t);
            measureIndex++;
            return t;
        }

        /// <summary>
        /// Set status based on limits and compOperator
        /// </summary>
        /// <param name="t"></param>
        private void Validate(StringValueTest t)
        {
            if (report.api.TestMode == TestModeType.Active)
            {
                StepStatusType newStatus = StepStatusType.Passed;
                switch (t.CompOperator)
                {
                    case CompOperatorType.IGNORECASE:
                        newStatus = (t.StringValue.ToLower() == t.StringLimit.ToLower() ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.CASESENSIT:
                        newStatus = (t.StringValue == t.StringLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.EQ:
                        newStatus = (t.StringValue == t.StringLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.NE:
                        newStatus = (t.StringValue != t.StringLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GT:
                        newStatus = (t.StringValue.CompareTo(t.StringLimit) > 0 ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LT:
                        newStatus = (t.StringValue.CompareTo(t.StringLimit) < 0 ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GE:
                        newStatus = (t.StringValue.CompareTo(t.StringLimit) >= 0 ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LE:
                        newStatus = (t.StringValue.CompareTo(t.StringLimit) <= 0 ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LOG:
                        newStatus = StepStatusType.Passed;
                        break;
                    default:
                        //Invalid comp operator!
                        Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = new ApplicationException("Invalid string compare operator (use EQ,NE,GT,LT,GE,LE or LOG"), Message = "String validate" });
                        break;
                }
                t.MeasureStatus = newStatus;
                if (Status == StepStatusType.Passed && newStatus == StepStatusType.Failed)
                    base.Status = newStatus;
            }
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
        {
            StringValueTest t = AddSingleTest();
            t.CompOperator = compOperator;
            t.StringValue = stringValue;
            t.StringLimit = stringLimit;

            Validate(t);

            return t;
        }

        /// <summary>
        /// Adds a string value test - without validation. 
        /// </summary>
        /// <param name="compOperator">Type of comparison. See <see cref="StringValueTest.CompOperator"/> for valid values.</param>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="stringLimit">Test limit.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddTest(CompOperatorType compOperator, string stringValue, string stringLimit, StepStatusType status)
        {
            StringValueTest t = AddSingleTest();
            t.CompOperator = compOperator;
            t.StringValue = stringValue;
            t.StringLimit = stringLimit;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            base.Status = status;

            return t;
        }

        /// <summary>
        /// Adds a string value test without limit, no comparison is done, just log - with validation. 
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddTest(string stringValue)
        {
            StringValueTest t = AddSingleTest();
            t.StringValue = stringValue;
            t.CompOperator = CompOperatorType.LOG;

            Validate(t);

            return t;
        }

        /// <summary>
        /// Adds a string value test without limit, no comparison is done, just log - without validation. 
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddTest(string stringValue, StepStatusType status)
        {
            StringValueTest t = AddSingleTest();
            t.StringValue = stringValue;
            t.CompOperator = CompOperatorType.LOG;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            base.Status = status;

            return t;
        }

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
        {
            StringValueTest t = AddMultipleTest(measureName);
            t.CompOperator = compOperator;
            t.StringValue = stringValue;
            t.StringLimit = stringLimit;

            Validate(t);

            return t;
        }

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
        {
            StringValueTest t = AddMultipleTest(measureName);
            t.CompOperator = compOperator;
            t.StringValue = stringValue;
            t.StringLimit = stringLimit;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            ApplyMultipleStatusToStep(status);

            return t;
        }

        /// <summary>
        /// Adds a multiple string value test without limit, no comparison is done, just log - with validation.
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddMultipleTest(string stringValue, string measureName)
        {
            StringValueTest t = AddMultipleTest(measureName);
            t.StringValue = stringValue;
            t.CompOperator = CompOperatorType.LOG;

            Validate(t);

            return t;
        }

        /// <summary>
        /// Adds a multiple string value test without limit, no comparison is done, just log - without validation.
        /// </summary>
        /// <param name="stringValue">Measured value.</param>
        /// <param name="measureName">Name of test.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public StringValueTest AddMultipleTest(string stringValue, string measureName, StepStatusType status)
        {
            StringValueTest t = AddMultipleTest(measureName);
            t.StringValue = stringValue;
            t.CompOperator = CompOperatorType.LOG;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            ApplyMultipleStatusToStep(status);

            return t;
        }

        #endregion

        protected internal override void RemoveStepData()
        {
            base.RemoveStepData();
            reportRow.Items.RemoveAll(o => o is StringValue_type n && n.StepID == stepRow.StepID);

            tests.Clear();
            measureIndex = 0;
            IsSingle = false;
            IsMultiple = false;
        }
    }
}
