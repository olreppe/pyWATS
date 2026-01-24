using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A pass fail test in a PassFailStep. 
    /// </summary>
    /// <remarks></remarks>
    public class PassFailTest
    {
        private readonly PassFail_type testRow;
        private readonly PassFailStep step;
        private readonly UUTReport report;

        internal  PassFailTest(PassFail_type testRow, PassFailStep step, UUTReport report)
        {
            this.testRow = testRow;
            this.step = step;
            this.report = report;
        }

        internal PassFailTest(UUTReport uut, PassFailStep pfs, int stepOrder, int measIndex, short measOrder)
        {
            testRow = new PassFail_type()
            {
                StepID = stepOrder,
                MeasIndex = measIndex,
                MeasOrderNumber = measOrder,
                Status = MeasurementResultType.Passed
            };

            report = uut;
            step = pfs;
            report.reportRow.Items.Add(testRow);
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
                        testRow.Name = report.api.SetPropertyValidated<PassFail_type>(nameof(PassFail_type.Name), value, nameof(MeasureName));
                }
                else
                    throw new InvalidOperationException($"Cannot set {nameof(MeasureName)} on a single test");
            }
        }

        /// <summary>
        /// Measure status (used for multiple values)
        /// </summary>
        public bool Passed
        {
            get => testRow.Status == MeasurementResultType.Passed;
            set
            {
                testRow.Status = value ? MeasurementResultType.Passed : MeasurementResultType.Failed;
                
                //Fail step if test failes
                if (!Passed && (step.stepRow.Status == StepResultType.Passed))
                    step.stepRow.Status = StepResultType.Failed;
            }
        }
    }
}
