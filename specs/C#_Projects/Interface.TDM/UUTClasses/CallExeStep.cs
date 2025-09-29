using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represent a call to external program.
    /// </summary>
    public class CallExeStep : Step
    {
        private readonly Callexe_type row;

        internal CallExeStep(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName, double exitCode) :
            base(uut, reportRow, parentStep, stepName)
        {
            row = new Callexe_type()
            {
                ExitCode = exitCode,
                ExitCodeSpecified = true,
                MeasIndex = 0,
                MeasIndexSpecified = true,
                StepID = base.stepRow.StepID
            };
            stepRow.StepType = StepTypeEnum.CallExecutable.ToString();

            reportRow.Items.Add(row);
        }

        internal CallExeStep(Step_type step, WATSReport reportRow, Callexe_type callExe, UUTReport uut) : base(step, reportRow, uut)
        {
            row = callExe;
        }

        /// <summary>
        /// Exit code of the executable.
        /// </summary>
        public double ExitCode
        {
            get { return row.ExitCode; }
            set { row.ExitCode = value; }
        }

        /// <summary>
        /// The number format for the exit code. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ExitCodeFormat
        {
            get => row.ExitCodeFormat;
            set => row.ExitCodeFormat = value;
        }

        protected internal override void RemoveStepData()
        {
            base.RemoveStepData();
            reportRow.Items.RemoveAll(o => o is Callexe_type c && c.StepID == stepRow.StepID);
        }
    }
}
