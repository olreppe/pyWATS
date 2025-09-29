using System;
using System.Collections.Generic;
using System.Linq;
using Virinco.WATS.Schemas.WRML;

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
        private readonly List<NumericLimitTest> tests;

        internal bool IsSingle { get; private set; } = false;

        internal bool IsMultiple { get; private set; } = false;

        internal NumericLimitStep(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName) 
            : base(uut, reportRow, parentStep, stepName)
        {
            tests = new List<NumericLimitTest>();

            //Assume single numeric
            stepRow.StepType = StepTypeEnum.ET_NLT.ToString(); 
        }

        internal  NumericLimitStep(Step_type step, WATSReport reportRow, NumericLimit_type[] numericTests, UUTReport uut) 
            : base(step, reportRow, uut)
        {
            tests = numericTests.Select(t => new NumericLimitTest(t, uut, this)).ToList();
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
        public NumericLimitTest[] Tests 
        { 
            get { return tests.ToArray(); }
            //set { throw new NotImplementedException(); }
        }

        private NumericLimitTest AddSingleTest()
        {
            if (IsMultiple)
                throw new InvalidOperationException("Cannot add single test to multiple test step.");

            if (tests.Any())
                throw new InvalidOperationException("Cannot add multiple single tests to single test step.");

            IsSingle = true;
            var t = AddTest();

            return t;
        }
        
        private NumericLimitTest AddMultipleTest(string measureName)
        {
            if (IsSingle)
                throw new InvalidOperationException("Cannot add multiple test to single test step.");

            if(!IsMultiple)
                StepType = StepTypeEnum.ET_MNLT.ToString();

            IsMultiple = true;
            var test = AddTest();

            test.MeasureName = measureName;

            return test;
        }

        private NumericLimitTest AddTest()
        {
            NumericLimitTest t = new NumericLimitTest(report, this, StepOrderNumber, measureIndex, report.GetNextMeasOrder());
            tests.Add(t);
            measureIndex++;
            return t;
        }

        /// <summary>
        /// Set status of measurement and step based on limits and compOperator
        /// </summary>
        /// <param name="t"></param>
        private void Validate(NumericLimitTest t)
        {
            if (report.api.TestMode == TestModeType.Active)
            {
                StepStatusType newStatus = StepStatusType.Passed;
                switch (t.CompOperator)
                {
                    //NB: Use LowLimit for all operators EQ,NE,GT,GE and even for LE og LT
                    case CompOperatorType.EQ:
                        newStatus = (t.NumericValue == t.LowLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.NE:
                        newStatus = (t.NumericValue != t.LowLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GT:
                        newStatus = (t.NumericValue > t.LowLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LT:
                        newStatus = (t.NumericValue < t.LowLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GE:
                        newStatus = (t.NumericValue >= t.LowLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LE:
                        newStatus = (t.NumericValue <= t.LowLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GTLT:
                        newStatus = (t.NumericValue > t.LowLimit && t.NumericValue < t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GELE:
                        newStatus = (t.NumericValue >= t.LowLimit && t.NumericValue <= t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GELT:
                        newStatus = (t.NumericValue >= t.LowLimit && t.NumericValue < t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.GTLE:
                        newStatus = (t.NumericValue > t.LowLimit && t.NumericValue <= t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LTGT:
                        newStatus = (t.NumericValue < t.LowLimit || t.NumericValue > t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LEGE:
                        newStatus = (t.NumericValue <= t.LowLimit || t.NumericValue >= t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LEGT:
                        newStatus = (t.NumericValue <= t.LowLimit || t.NumericValue > t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LTGE:
                        newStatus = (t.NumericValue < t.LowLimit || t.NumericValue >= t.HighLimit ? StepStatusType.Passed : StepStatusType.Failed);
                        break;
                    case CompOperatorType.LOG:
                        newStatus = StepStatusType.Passed;
                        break;
                    default:
                        break;
                }

                t.MeasureStatus = newStatus;
                if (Status == StepStatusType.Passed && newStatus == StepStatusType.Failed)
                    base.Status = newStatus;
            }
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
        {
            NumericLimitTest t = AddSingleTest();
            t.CompOperator = compOperator;
            t.HighLimit = highLimit;
            t.LowLimit = lowLimit;
            t.Units = units;
            t.NumericValue = numericValue;

            Validate(t);

            return t;
        }

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
        {
            NumericLimitTest t = AddSingleTest();
            t.CompOperator = compOperator;
            t.HighLimit = highLimit;
            t.LowLimit = lowLimit;
            t.Units = units;
            t.NumericValue = numericValue;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            base.Status = status;

            return t;
        }

        /// <summary>
        /// Adds a numeric limit test with one limit - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="compOperator">Type of comparison. See <see cref="NumericLimitTest.CompOperator"/> for valid values.</param>
        /// <param name="limit">Test limit.</param>
        /// <param name="units">Measure units.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, CompOperatorType compOperator, double limit, string units)
        {
            NumericLimitTest t = AddSingleTest();
            if (compOperator.ToString().Length != 2)
            {
                ApplicationException ex = new ApplicationException("Invalid method called for " + compOperator.ToString() + " use another overloaded method");
            }
            t.CompOperator = compOperator;
            t.LowLimit = limit;
            t.Units = units;
            t.NumericValue = numericValue;

            Validate(t);

            return t;
        }

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
        {
            NumericLimitTest t = AddSingleTest();
            if (compOperator.ToString().Length != 2)
            {
                ApplicationException ex = new ApplicationException("Invalid method called for " + compOperator.ToString() + " use another overloaded method");
            }
            t.CompOperator = compOperator;
            t.LowLimit = limit;
            t.Units = units;
            t.NumericValue = numericValue;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            base.Status = status;

            return t;
        }

        /// <summary>
        /// Adds a numeric limit test without limits, no comparison is done, just log - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="units">Measure units.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, string units)
        {
            NumericLimitTest t = AddSingleTest();
            t.CompOperator = CompOperatorType.LOG;
            t.Units = units;
            t.NumericValue = numericValue;

            Validate(t);

            return t;
        }

        /// <summary>
        /// Adds a numeric limit test without limits, no comparison is done, just log - without validation.                
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="status">Status to set without validation.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddTest(double numericValue, string units, StepStatusType status)
        {
            NumericLimitTest t = AddSingleTest();
            t.CompOperator = CompOperatorType.LOG;
            t.NumericValue = numericValue;
            t.Units = units;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            base.Status = status;

            return t;
        }

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
        {
            NumericLimitTest t = AddMultipleTest(measureName);
            t.CompOperator = compOperator;
            t.HighLimit = highLimit;
            t.LowLimit = lowLimit;
            t.Units = units;
            t.NumericValue = numericValue;

            Validate(t);

            return t;
        }

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
        {
            NumericLimitTest t = AddMultipleTest(measureName);
            t.CompOperator = compOperator;
            t.HighLimit = highLimit;
            t.LowLimit = lowLimit;
            t.Units = units;
            t.NumericValue = numericValue;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            ApplyMultipleStatusToStep(status);

            return t;
        }

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
        {
            NumericLimitTest t = AddMultipleTest(measureName);
            if (compOperator.ToString().Length != 2)
            {
                ApplicationException ex = new ApplicationException("Invalid method called for " + compOperator.ToString() + " use another overloaded method");
            }
            t.CompOperator = compOperator;
            t.LowLimit = limit;
            t.Units = units;
            t.NumericValue = numericValue;

            Validate(t);

            return t;
        }


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
        {
            NumericLimitTest t = AddMultipleTest(measureName);
            if (compOperator.ToString().Length != 2)
            {
                ApplicationException ex = new ApplicationException("Invalid method called for " + compOperator.ToString() + " use another overloaded method");
            }
            t.CompOperator = compOperator;
            t.LowLimit = limit;
            t.Units = units;
            t.NumericValue = numericValue;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            ApplyMultipleStatusToStep(status);

            return t;
        }

        /// <summary>
        /// Adds a multiple numeric limit test without limits, no comparison is done, just log - with validation.
        /// </summary>
        /// <param name="numericValue">Measured value.</param>
        /// <param name="units">Measure units.</param>
        /// <param name="measureName">Name of test.</param>
        /// <returns>Returns a reference to the test.</returns>
        public NumericLimitTest AddMultipleTest(double numericValue, string units, string measureName)
        {
            NumericLimitTest t = AddMultipleTest(measureName);
            t.CompOperator = CompOperatorType.LOG;
            t.Units = units;
            t.NumericValue = numericValue;

            Validate(t);

            return t;
        }

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
        {
            NumericLimitTest t = AddMultipleTest(measureName);
            t.CompOperator = CompOperatorType.LOG;
            t.Units = units;
            t.NumericValue = numericValue;

            t.MeasureStatus = GetMeasureStatusFromExplicitStepStatus(status);
            ApplyMultipleStatusToStep(status);

            return t;
        }

        #endregion

        protected internal override void RemoveStepData()
        {
            base.RemoveStepData();
            reportRow.Items.RemoveAll(o => o is NumericLimit_type n && n.StepID == stepRow.StepID);

            tests.Clear();
            measureIndex = 0;
            IsSingle = false;
            IsMultiple = false;
        }
    }
}
