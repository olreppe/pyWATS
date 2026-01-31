using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary> 
    /// Steps are the content of a UUT report. WATS support 
    /// </summary>
    public class Step
    {
        internal Step_type stepRow;
        internal WATSReport reportRow;
        internal UUTReport report;
        internal short measureIndex = 0;
        //protected short stepOrder = 0;
        private bool failParentOnFail = true;

        internal Step(UUTReport report, WATSReport reportRow, SequenceCall parentStep, string stepName)
        {
            //Trace.WriteLine("Step Constructor " + stepName);
            this.reportRow = reportRow;
            this.report = report;
            // parent = parentStep == null ? uut.RootSequenceCall : parentStep;
            stepRow = new Step_type()
            {
                Name = report.api.SetPropertyValidated<Step_type>("Name", stepName, ""),
                StepIndex = parentStep?.GetNextStepIndex() ?? 0,
                StepIndexSpecified = true,
                total_time = 0d,
                total_timeSpecified = true,
                //Start = reportRow.Start,
                StartSpecified = false,
                Group = StepGroup_type.Main
            };
            reportRow.Items.Add(stepRow);

            if (parentStep != null)
            {
                stepRow.ParentStepID = parentStep.stepRow.StepID;
                stepRow.ParentStepIDSpecified = true;
            }
            stepRow.StepID = report.GetNextStepOrder();
            stepRow.Status = StepResultType.Passed;
        }

        internal Step(Step_type step, WATSReport report, UUTReport uut)
        {
            this.stepRow = step;
            this.reportRow = report;
            this.report = uut;
        }

        internal static Step Create(Step_type step, WATSReport reportRow, UUTReport uut)
        {
            var numtests = reportRow.Items.OfType<NumericLimit_type>().Where(s => s.StepID == step.StepID).ToArray();
            if (numtests.Length > 0)
                return new NumericLimitStep(step, reportRow, numtests, uut);

            var passFails = reportRow.Items.OfType<PassFail_type>().Where(s => s.StepID == step.StepID).ToArray();
            if (passFails.Length > 0)
                return new PassFailStep(step, reportRow, passFails, uut);

            var stringValues = reportRow.Items.OfType<StringValue_type>().Where(s => s.StepID == step.StepID).ToArray();
            if (stringValues.Length > 0)
                return new StringValueStep(step, reportRow, stringValues, uut);

            var sequenceCalls = reportRow.Items.OfType<SequenceCall_type>().Where(s => s.StepID == step.StepID).ToArray();
            if (sequenceCalls.Length == 1) //Can only be one
                return new SequenceCall(step, sequenceCalls[0], reportRow, uut);

            var messagePopups = reportRow.Items.OfType<MessagePopup_type>().Where(s => s.StepID == step.StepID).ToArray();
            if (messagePopups.Length == 1)
                return new MessagePopupStep(step, reportRow, messagePopups[0], uut);

            var callExes = reportRow.Items.OfType<Callexe_type>().Where(s => s.StepID == step.StepID).ToArray();
            if (callExes.Length == 1)
                return new CallExeStep(step, reportRow, callExes[0], uut);

            var propertyLoaders = reportRow.Items.OfType<PropertyLoader_type>().Where(s => s.StepID == step.StepID).ToArray();
            if (propertyLoaders.Length == 1)
                return new PropertyLoaderStep(step, reportRow, propertyLoaders[0], uut);

            return new Step(step, reportRow,uut);
        }

        /// <summary>
        /// Set/Get unique identifier of a step (Teststand TSGuid, optional)
        /// </summary>
        public string StepGuid
        {
            get { return this.stepRow.TSGuid; }
            set { this.stepRow.TSGuid = report.api.SetPropertyValidated<Step_type>(nameof(Step_type.TSGuid), value, nameof(StepGuid)); }
        }

        /// <summary>
        /// Parent Step
        /// </summary>
        public SequenceCall Parent
        {
            get 
            {
                if (this.stepRow.ParentStepIDSpecified)
                {
                    var step = reportRow.Items.OfType<Step_type>().Where(s => s.StepID == this.stepRow.ParentStepID).First();
                    var sequence = reportRow.Items.OfType<SequenceCall_type>().Where(s => s.StepID == this.stepRow.ParentStepID).First();

                    return new SequenceCall(step, sequence, reportRow, report);
                }

                return null;
            }
        }

        /// <summary>
        /// Returns full path of a step. The path is built from names of all parent steps separated by /. Main Sequence Callback is omitted
        /// </summary>
        public string StepPath
        {
            get
            {
                string path = "/";
                Step_type s = this.stepRow;
                while (s.ParentStepIDSpecified)
                {
                    s = reportRow.Items.OfType<Step_type>().Where(st => st.StepID == s.ParentStepID).First();
                    if (s.Name.ToLower() != "mainsequence callback")
                        path = "/" + s.Name.ToLower() + path;
                }
                return path;
            }
        }

        /// <summary>
        /// Returns step type
        /// </summary>
        public string StepType
        {
            get { return stepRow.StepType; }
            set { stepRow.StepType = report.api.SetPropertyValidated<Step_type>(nameof(Step_type.StepType), value, nameof(StepType)); ; }
        }

        /// <summary>
        /// Global step order number
        /// </summary>
        public int StepOrderNumber
        {
            get { return stepRow.StepID; }
        }

        /// <summary>
        /// Step position within a sequence
        /// </summary>
        public short StepIndex
        {
            get { return stepRow.StepIndexSpecified ? (short)stepRow.StepIndex : (short)-1; }
            set { stepRow.StepIndex = value; }
        }

        /// <summary>
        /// Name of step
        /// </summary>
        public string Name
        {
            get { return stepRow.Name; }
            set { stepRow.Name = report.api.SetPropertyValidated<Step_type>("Name", value, "StepName"); }
        }

        /// <summary>
        /// Normally, a failed step will propagate up to parent step. To prevent this, set this property to false
        /// </summary>
        public bool FailParentOnFail
        {
            get { return failParentOnFail; }
            set { failParentOnFail = value; }
        }

        /// <summary>
        /// Indicates that this step caused the sequence to fail.
        /// </summary>
        public bool CausedSequenceFailure
        {
            get { return stepRow.StepCausedSequenceFailure; }
            set { stepRow.StepCausedSequenceFailure = value; }
        }

        internal void ApplyMultipleStatusToStep(StepStatusType newStatus)
        {
            if (newStatus == StepStatusType.Failed)
            {
                if (Status == StepStatusType.Passed || Status == StepStatusType.Skipped)
                    Status = StepStatusType.Failed;
            }
            else if (newStatus == StepStatusType.Passed)
            {
                if (Status == StepStatusType.Skipped)
                    Status = StepStatusType.Passed;
            }
        }

        /// <summary>
        /// Step status
        /// </summary>
        public virtual StepStatusType Status
        {
            get
            {
                StepStatusType status;
                if (Utilities.EnumTryParse<StepStatusType>(stepRow.Status.ToString(), out status))
                    return status;
                else
                    return StepStatusType.Passed;
            }
            set
            {
                StepResultType status;
                if (!Utilities.EnumTryParse<StepResultType>(value.ToString(), out status))
                {
                    throw new ArgumentOutOfRangeException("Status", value, "Invalid Step Status code");
                }
                stepRow.Status = status;

                //Skipped steps should not have content (but still properties like name, status, time, id, etc.)
                if (status == StepResultType.Skipped)
                    RemoveStepData();

                //Parent status change is only working when TestMode is Active and failParentOnFail is true
                if (report.api.TestMode == TestModeType.Active && failParentOnFail &&
                    (value == StepStatusType.Failed || value == StepStatusType.Error || value == StepStatusType.Terminated))
                {
                    if (Parent != null) //Step has a parent step
                    {
                        if ((int)Parent.Status < (int)value) //Only set status if new status is ranges higher (order: Failed,Error,Terminated)
                            Parent.Status = value;
                    }
                    else //Root step, adjust UUT status
                    {
                        UUTStatusType newUUTStatus;
                        if (Utilities.EnumTryParse<UUTStatusType>(value.ToString(), out newUUTStatus) && (int)report.Status < (int)newUUTStatus)
                            report.Status = newUUTStatus;
                    }
                }
            }
        }

        /// <summary>
        /// Step status
        /// </summary>
        public string StatusText
        {
            get
            {
                return stepRow.Status.ToString();
            }
            internal set
            {
                if (report.api.TestMode != TestModeType.TestStand) throw new InvalidOperationException("TestMode must be TestStand for setting StatusText");
                StepResultType status;
                if (Utilities.EnumTryParse<StepResultType>(value, out status))
                    stepRow.Status = status;
                else
                    stepRow.Status = StepResultType.Unknown; // Really should not happend...
            }
        }

        /// <summary>
        /// Report text
        /// </summary>
        public string ReportText
        {
            get { return stepRow.ReportText; }
            set { stepRow.ReportText = report.api.SetPropertyValidated<Step_type>("ReportText", value); }
        }

        /// <summary>
        /// Step execution time (in seconds)
        /// </summary>
        public double StepTime
        {
            get { return stepRow.total_timeSpecified ? stepRow.total_time : 0; }
            set { stepRow.total_time = value; stepRow.total_timeSpecified = true; }
        }

        /// <summary>
        /// The number format for the step execution time. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string StepTimeFormat
        {
            get => stepRow.total_timeFormat;
            set => stepRow.total_timeFormat = value;
        }

        /// <summary>
        /// Step module-execution time (in seconds)
        /// </summary>
        public double ModuleTime
        {
            get { return stepRow.module_timeSpecified ? stepRow.module_time : 0; }
            set { stepRow.module_time = value; stepRow.module_timeSpecified = true; }
        }

        /// <summary>
        /// The number format for the step module-execution time. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ModuleTimeFormat
        {
            get => stepRow.module_timeFormat;
            set => stepRow.module_timeFormat = value;
        }

        /// <summary>
        /// Step’s start date/time
        /// </summary>
        public DateTime StartDateTime
        {
            get { return stepRow.StartSpecified ? stepRow.Start : TDM.dt1900; }
            set { stepRow.Start = value; stepRow.StartSpecified = true; }
        }

        /// <summary>
        /// Main step group (Setup, Main, Cleanup)
        /// </summary>
        public StepGroupEnum StepGroup
        {
            get
            {
                switch (stepRow.Group)
                {
                    case StepGroup_type.Setup: return StepGroupEnum.Setup;
                    case StepGroup_type.Main: return StepGroupEnum.Main;
                    case StepGroup_type.Cleanup: return StepGroupEnum.Cleanup;
                    default: return StepGroupEnum.Main;
                }
            }
            set
            {
                switch (value)
                {
                    case StepGroupEnum.Setup: stepRow.Group = StepGroup_type.Setup; break;
                    case StepGroupEnum.Main: stepRow.Group = StepGroup_type.Main; break;
                    case StepGroupEnum.Cleanup: stepRow.Group = StepGroup_type.Cleanup; break;
                    default: throw new ArgumentException("Invalid StepGroup", "StepGroup");
                }
            }
        }

        /// <summary>
        /// Error message connected to step
        /// </summary>
        public string StepErrorMessage
        {
            get { return stepRow.StepErrorMessage; }
            set { stepRow.StepErrorMessage = report.api.SetPropertyValidated<Step_type>("StepErrorMessage", value); }
        }

        /// <summary>
        /// Error code connected to step
        /// </summary>
        public int StepErrorCode
        {
            get { return stepRow.StepErrorCodeSpecified ? stepRow.StepErrorCode : 0; }
            set { stepRow.StepErrorCode = value; stepRow.StepErrorCodeSpecified = true; }
        }

        /// <summary>
        /// The number format for the step error code. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string StepErrorCodeFormat
        {
            get => stepRow.StepErrorCodeFormat;
            set => stepRow.StepErrorCodeFormat = value;
        }

        /// <summary>
        /// Adds a chart to a step
        /// </summary>
        /// <param name="chartType">Linear or logaritmic can be selected</param>
        /// <param name="chartLabel">Chart label</param>
        /// <param name="xLabel">X-Label</param>
        /// <param name="xUnit">X-Unit</param>
        /// <param name="yLabel">Y-Label</param>
        /// <param name="yUnit">Y-Unit</param>
        /// <returns></returns>
        public Chart AddChart(ChartType chartType, string chartLabel, string xLabel, string xUnit, string yLabel, string yUnit)
        {
            if (reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == stepRow.StepID).FirstOrDefault() != null)
                throw new ApplicationException("Only one chart can be added to a step");
            Chart chart = new Chart(report, this.reportRow, this, chartType, chartLabel, xLabel, xUnit, yLabel, yUnit);
            //Change steptype if graph is added
            stepRow.StepType = "WATS_XYGMNLT";
            return chart;
        }

        /// <summary>
        /// Get chart if present
        /// </summary>
        public Chart Chart
        {
            get
            {
                Chart_type chart = reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == stepRow.StepID).FirstOrDefault();
                if (chart != null)
                    return new Chart(report, reportRow, this);
                else
                    return null;
            }
        }

        /// <summary>
        /// Attaches a file to a step.
        /// </summary>
        /// <remarks>File size is limited to 100KB</remarks>
        /// <param name="fileName">Full path and name of file</param>
        /// <param name="deleteAfterAttach">If true, the file is deleted after being attached</param>
        /// <returns></returns>
        public Attachment AttachFile(string fileName, bool deleteAfterAttach)
        {
            if (reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == stepRow.StepID).FirstOrDefault() != null)
                throw new ApplicationException("Only one attachment can be added to a step");
            Attachment attachment = new Attachment(report, this.reportRow, this, fileName, deleteAfterAttach);
            //stepRow.StepType = "WATS_AttachFile";
            return attachment;
        }

        /// <summary>
        /// Gets an attachment
        /// </summary>
        public Attachment Attachment
        {
            get
            {
                return new Attachment(report, this.reportRow, this);
            }
        }

        /// <summary>
        /// Reserved for use with TestStand. Does not show up in analysis.
        /// An additional result can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
        /// </summary>
        /// <param name="Name"></param>
        /// <param name="contents"></param>
        /// <returns></returns>
        public AdditionalResult AddAdditionalResult(string Name, System.Xml.Linq.XElement contents)
        {
            AdditionalResult adr = new AdditionalResult(report, this, Name, contents);
            return adr;
        }

        public AdditionalResult AdditionalResult
        {
            get
            {
                AdditionalResults_type additionalResult = reportRow.Items.OfType<AdditionalResults_type>().Where(ar => ar.StepID == stepRow.StepID).FirstOrDefault();
                if (additionalResult != null)
                    return new AdditionalResult(report, additionalResult);
                else
                    return null;
            }
        }

        /// <summary>
        /// Attaches a byte array to a step
        /// </summary>
        /// <remarks>File size is limited to 100KB</remarks>
        /// <param name="label">Will be showed in WATS as a label to the attachment</param>
        /// <param name="content">Byte array (binary data) to be attached</param>
        /// <param name="mimeType">Will decide how the browser opens the attachement. see: http://en.wikipedia.org/wiki/Internet_media_type for details
        /// <para>If blank, mimeType application/octet-stream will be used</para></param>
        /// <returns></returns>
        public Attachment AttachByteArray(string label, byte[] content, string mimeType)
        {
            if (reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == stepRow.StepID).FirstOrDefault() != null)
                throw new ApplicationException("Only one attachment can be added to a step");
            Attachment attachment = new Attachment(report, this.reportRow, this, label, content, mimeType);
            //stepRow.StepType = "WATS_AttachFile";
            return attachment;
        }

        /// <summary>
        /// Get/Set loop index of the step
        /// </summary>
        public short LoopIndex
        {
            get { return stepRow.Loop.index; }
            set { stepRow.Loop.index = value; stepRow.Loop.indexSpecified = true; }
        }

        internal StepStatusType GetMeasureStatusFromExplicitStepStatus(StepStatusType status)
        {
            switch (status)
            {
                case StepStatusType.Passed:
                case StepStatusType.Failed:
                case StepStatusType.Skipped:
                    return status;
                case StepStatusType.Done:
                    throw new ArgumentException("Status Done is not supported for test.");
                case StepStatusType.Error:
                case StepStatusType.Terminated:
                    return StepStatusType.Failed;
            }
            return status;
        }

        /// <summary>
        /// Override to implement removing data when step is set to skipped status. Remember to call base!
        /// </summary>
        protected internal virtual void RemoveStepData() 
        {
            reportRow.Items.RemoveAll(o => o is Chart_type c && c.StepID == stepRow.StepID);
            reportRow.Items.RemoveAll(o => o is AdditionalResults_type a && a.StepID == stepRow.StepID);
        }
    }
}

