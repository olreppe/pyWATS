using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A string value test in a StringValueStep. 
    /// </summary>
    public class StringValueTest
    {
        private readonly StringValue_type testRow;
        private readonly UUTReport report;
        private readonly StringValueStep step;

        internal StringValueTest(StringValue_type testRow, UUTReport report, StringValueStep step)
        {
            this.testRow = testRow;
            this.report = report;
            this.step = step;
        }

        internal StringValueTest(UUTReport uut, StringValueStep svs, int stepOrder, int measIndex, short measOrder)
        {
            testRow = new StringValue_type()
            {
                StepID = stepOrder,
                MeasIndex = measIndex,
                MeasOrderNumber = measOrder,
                Status = MeasurementResultType.Passed
            };

            report = uut;
            step = svs;
            report.reportRow.Items.Add(testRow);
        }

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
            get => Utilities.EnumTryParse(testRow.CompOperator, out CompOperatorType op) ? op : CompOperatorType.LOG;
            set => testRow.CompOperator = value.ToString();
        }

        /// <summary>
        /// If compOperator is EQ, String value is compared
        /// </summary>
        public string StringLimit
        {
            get => testRow.StringLimit;
            set => testRow.StringLimit = report.api.SetPropertyValidated<StringValue_type>("StringLimit", value);
        }

        /// <summary>
        /// Measure string value
        /// </summary>
        public string StringValue
        {
            get => testRow.StringValue;
            set => testRow.StringValue = report.api.SetPropertyValidated<StringValue_type>("StringValue", value);
        }

        /// <summary>
        /// Measure name (used for multiple values).
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
                        testRow.Name = report.api.SetPropertyValidated<StringValue_type>(nameof(StringValue_type.Name), value, nameof(MeasureName));
                }
                else
                    throw new InvalidOperationException($"Cannot set {nameof(MeasureName)} on a single test");
            }
        }

        /// <summary>
        /// Measure status enum (used for multiple values)
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
