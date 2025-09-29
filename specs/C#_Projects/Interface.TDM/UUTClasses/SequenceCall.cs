using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// 
    /// </summary>
    public class SequenceCall : Step
    {
        internal SequenceCall_type seqRow;

        int currentStepIndex = 0;

        internal SequenceCall(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName, string sequenceName, string sequenceVersion)
            : base(uut, reportRow, parentStep, stepName)
        {
            seqRow = new SequenceCall_type()
            {
                StepID = base.stepRow.StepID,
                Name = report.api.SetPropertyValidated<SequenceCall_type>("Name", stepName, "SequenceName"),
                MeasIndex = 0,
                Version = report.api.SetPropertyValidated<SequenceCall_type>("Version", sequenceVersion, "SequenceVersion"),
                Filename = report.api.SetPropertyValidated<SequenceCall_type>("Filename", sequenceName, "SequenceFileName"),
                Filepath = report.api.SetPropertyValidated<SequenceCall_type>("Filepath", sequenceName, "SequenceFilePath")
            };
            //Trace.WriteLine("SequenceCall Constructor");
            //AddSequenceCallRow(int Report_ID, int STEP_ORDER_NUMBER, int SS_LCID, int MEAS_IDX, string SEQUENCE_NAME, string SEQUENCE_VERSION, string SEQUENCE_FILE_NAME, string SEQUENCE_FILE_PATH)
            //seqRow = reportRow.SequenceCall.AddSequenceCallRow(reportDS.Report[0].Report_ID, StepOrderNumber, 0, 0, sequenceName, sequenceVersion, sequenceName, sequenceName);
            stepRow.StepType = StepTypeEnum.SequenceCall.ToString();
            reportRow.Items.Add(seqRow);
        }

        internal SequenceCall(Step_type step, SequenceCall_type sequence, WATSReport report, UUTReport uut) : base(step, report, uut)
        {
            seqRow = sequence;

            var substeps = report.Items.OfType<Step_type>().Where(s => s.ParentStepIDSpecified && s.ParentStepID == step.StepID).ToList();
            currentStepIndex = substeps.Any() ? substeps.Max(s => s.StepIndex) + 1 : 0;
        }

        internal int GetNextStepIndex()
        {
            if (loopingActive)
                return currentStepIndex;

            return currentStepIndex++;
        }


        /*
        internal SequenceCall(UUTReport uut, WATSReport reportRow, Step parentStep, string stepGroup, string stepType, int stepIndex, string stepName, string sequenceName, string sequenceFile, string sequenceFileVersion)
            : base(uut, reportRow, parentStep, stepName)
        {
            //Trace.WriteLine("SequenceCall (TS-)Constructor");
            if (report.api.TestMode != TestModeType.TestStand) throw new InvalidOperationException("TestMode must be TestStand for setting StatusText");
            seqRow = reportDS.SequenceCall.AddSequenceCallRow(reportDS.Report[0].Report_ID, StepOrderNumber, 0, 0, sequenceName, sequenceFileVersion, sequenceFile, string.Empty);
            stepRow.Step_type = StepTypeEnum.SequenceCall.ToString();
        }
        */

        /// <summary>
        /// Sequence name - name of test program
        /// </summary>
        public string SequenceName
        {
            get { return seqRow.Filepath; }
            set
            {
                seqRow.Filepath= report.api.SetPropertyValidated<SequenceCall_type>("Name", value, "SequenceName");
            }
        }

        /// <summary>
        /// Version of sequence
        /// </summary>
        public string SequenceVersion
        {
            get { return seqRow.Version; }
            set { seqRow.Version = report.api.SetPropertyValidated<SequenceCall_type>("Version", value, "SequenceVersion"); }
        }

        /// <summary>
        /// Adds a new sequencecall.
        /// </summary>
        /// <param name="stepName">Name of sequence</param>
        /// <returns>new sequencecall, use this to add sub-steps</returns>
        public SequenceCall AddSequenceCall(string stepName)
        {
            //Trace.WriteLine("AddSequenceCall " + stepName);
            return AddSequenceCall(stepName, report.SequenceName, report.SequenceVersion);
        }

        /// <summary>
        /// Adds a new sequence call
        /// </summary>
        /// <param name="stepName">Name of sequence step</param>
        /// <param name="sequenceName">Alternate name of sequence</param>
        /// <param name="sequenceVersion">Alternate sequence version</param>
        /// <returns></returns>
        public SequenceCall AddSequenceCall(string stepName, string sequenceName, string sequenceVersion)
        {
            //Trace.WriteLine(String.Format("AddSequenceCall {0} seqName={1} seqVer={2}",stepName,sequenceName,sequenceVersion));
            SequenceCall seqCall = new SequenceCall(report, reportRow, this, stepName, sequenceName, sequenceVersion);

            if (loopingActive)
                loopSteps.Add(seqCall);

            return seqCall;
        }

        /// <summary>
        /// Add a Numeric limit test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Name of step</param>
        /// <returns></returns>
        public NumericLimitStep AddNumericLimitStep(string stepName)
        {
            //Trace.WriteLine("AddNumericLimitStep " + stepName);
            NumericLimitStep step = new NumericLimitStep(report, reportRow, this, stepName);

            if (loopingActive)
                loopSteps.Add(step);

            return step;
        }

        /// <summary>
        /// Adds a Pass/Fail (boolean) step, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        public PassFailStep AddPassFailStep(string stepName)
        {
            //Trace.WriteLine("AddPasFailStep " + stepName);
            PassFailStep step = new PassFailStep(report, reportRow, this, stepName);

            if (loopingActive)
                loopSteps.Add(step);

            return step;
        }

        /// <summary>
        /// Adds a string value step, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName"></param>
        /// <returns></returns>
        public StringValueStep AddStringValueStep(string stepName)
        {
            //Trace.WriteLine("AddStringValueStep " + stepName);
            StringValueStep step = new StringValueStep(report, reportRow, this, stepName);

            if (loopingActive)
                loopSteps.Add(step);

            return step;
        }


        /// <summary>
        /// Adds a call to external program with exitCode
        /// </summary>
        /// <param name="stepName"></param>
        /// <param name="exitCode"></param>
        /// <returns></returns>
        public CallExeStep AddCallExeStep(string stepName, double exitCode)
        {
            //Trace.WriteLine("AddCallExeStep " + stepName);
            CallExeStep step = new CallExeStep(report, reportRow, this, stepName, exitCode);

            if (loopingActive)
                loopSteps.Add(step);

            return step;
        }

        /// <summary>
        /// Adds a generic step, see GenericStepTypes 
        /// </summary>
        /// <param name="stepType"></param>
        /// <param name="stepName"></param>
        /// <returns></returns>
        public GenericStep AddGenericStep(GenericStepTypes stepType, string stepName)
        {
            //Trace.WriteLine("AddStringValueStep " + stepName);
            iconNames icon = (iconNames)stepType;
            GenericStep step = new GenericStep(report, reportRow, this, stepName, icon.ToString());

            if (loopingActive)
                loopSteps.Add(step);

            return step;
        }

        /// <summary>
        /// Adds the result of a message popop.
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="buttonPressed">The button (numeric value) that was pressed</param>
        /// <param name="response">Response from the popup</param>
        /// <returns></returns>
        public MessagePopupStep AddMessagePopupStep(string stepName, short buttonPressed, string response)
        {
            MessagePopupStep step = new MessagePopupStep(report, reportRow, this, stepName, buttonPressed, response);

            if (loopingActive)
                loopSteps.Add(step);

            return step;
        }

        /// <summary>
        /// Adds a Teststand Description loader step
        /// </summary>
        /// <param name="stepName"></param>
        /// <param name="numPropApplied"></param>
        /// <param name="numPropRead"></param>
        /// <returns></returns>
        public PropertyLoaderStep AddPropertyLoaderStep(string stepName, short numPropApplied, short numPropRead)
        {
            PropertyLoaderStep step = new PropertyLoaderStep(report, reportRow, this, stepName, numPropApplied, numPropRead);
            return step;
        }

        /// <summary>
        /// Internal function
        /// </summary>
        /// <param name="ParentStep"></param>
        /// <param name="stepIndex"></param>
        /// <param name="stepGroup"></param>
        /// <param name="stepType"></param>
        /// <param name="stepName"></param>
        /// <param name="sequenceName"></param>
        /// <param name="sequenceFile"></param>
        /// <param name="sequenceFileVersion"></param>
        /// <param name="stepStatusText"></param>
        /// <param name="startDateTime"></param>
        /// <param name="errorCode"></param>
        /// <param name="errorMessage"></param>
        /// <param name="stepTime"></param>
        /// <param name="moduleTime"></param>
        /// <returns></returns>
        public static SequenceCall Create(Step ParentStep, int stepIndex, string stepGroup, string stepType,
                        string stepName, string sequenceName, string sequenceFile, string sequenceFileVersion, string stepStatusText, DateTime startDateTime, int errorCode, string errorMessage, double stepTime, double moduleTime)
        {
            var parentSeq = ParentStep as SequenceCall;
            if (parentSeq == null)
                throw new InvalidCastException("ParentStep must be a SequenceCall step.");

            SequenceCall seqCall = new SequenceCall(ParentStep.report, ParentStep.reportRow, parentSeq, stepName, sequenceName, sequenceFileVersion);
            seqCall.StepType = stepType;
            StepGroupEnum group;
            seqCall.StepGroup = (Utilities.EnumTryParse<StepGroupEnum>(stepGroup, out group)) ? group : StepGroupEnum.Main;
            seqCall.StepIndex = (short)stepIndex;
            seqCall.seqRow.Filename = sequenceFile;
            seqCall.seqRow.Filepath = sequenceFile;
            seqCall.StatusText = stepStatusText;
            seqCall.StartDateTime = startDateTime;
            seqCall.StepErrorCode = errorCode;
            seqCall.StepErrorMessage = errorMessage;
            seqCall.StepTime = stepTime;
            seqCall.ModuleTime = moduleTime;
            return seqCall;
        }

        #region Looping

        private Step mainLoopStep = null;
        private List<Step> loopSteps = null;
        private bool loopingActive = false;

        /// <summary>
        /// <para>Start a loop of a specified step type. Each Step added between calling StartLoop and StopLoop is added to the loop.</para>
        /// <para>If no steps will be added to the loop, all parameters should be set.</para>
        /// <para>In Active mode: iterations, passed, failed and endingIndex will be set be set based on steps in the loop.</para>
        /// <para>In Import mode: iterations, passed, failed and endingIndex must be set.</para>
        /// <para>Valid step types are: SequenceCall, NumericLimitStep, StringValueStep, PassFailStep, CallExeStep, MessagePopupStep and GenericStep</para>
        /// </summary>
        /// <param name="stepName">Name of the loop. All steps in the loop must have same name.</param>
        /// <param name="iterations">Number of iterations contained in the loop. In Active mode will be set to the amount of steps the loop contains.</param>
        /// <param name="passed">Number of passed loop iterations.</param>
        /// <param name="failed">Number of failed loop iterations.</param>
        /// <param name="endingIndex">Index of the last loop iteration.</param>
        /// <exception cref="ArgumentException">Is thrown when T is invalid.</exception>  
        /// <returns>The summary step of the loop. If StartLoop has already been called, returns null.</returns>
        public T StartLoop<T>(string stepName, short? iterations = null, short? passed = null, short? failed = null, short? endingIndex = null) where T : Step
        {
            if (loopingActive)
                return null;

            loopSteps = new List<Step>();
            loopingActive = true;

            T step;
            if (typeof(T) == typeof(SequenceCall))
                step = new SequenceCall(report, reportRow, this, stepName, "", "") as T;
            else if (typeof(T) == typeof(NumericLimitStep))
                step = new NumericLimitStep(report, reportRow, this, stepName) as T;
            else if (typeof(T) == typeof(StringValueStep))
                step = new StringValueStep(report, reportRow, this, stepName) as T;
            else if (typeof(T) == typeof(PassFailStep))
                step = new PassFailStep(report, reportRow, this, stepName) as T;
            else if (typeof(T) == typeof(GenericStep))
                step = new GenericStep(report, reportRow, this, stepName, GenericStepTypes.Action.ToString()) as T;
            else if (typeof(T) == typeof(CallExeStep))
                step = new CallExeStep(report, reportRow, this, stepName, 0) as T;
            else if (typeof(T) == typeof(MessagePopupStep))
                step = new MessagePopupStep(report, reportRow, this, stepName, 0, "") as T;
            else
                throw new ArgumentException($"{typeof(T)} is not a valid loop step type.");

            step.stepRow.Loop = new Step_typeLoop()
            {
                num = iterations ?? 0,
                numSpecified = iterations != null ? true : false,
                passed = passed ?? 0,
                passedSpecified = passed != null ? true : false,
                failed = failed ?? 0,
                failedSpecified = failed != null ? true : false,
                ending_index = endingIndex ?? 0,
                ending_indexSpecified = endingIndex != null ? true : false,
            };

            mainLoopStep = step;

            return step;
        }

        /// <summary>
        /// Stops and finalizes the current loop. 
        /// </summary>
        public void StopLoop()
        {
            if (!loopingActive)
                return;

            //Verifies that loopSteps only contains one step type
            var mainLoopStepType = mainLoopStep.GetType();
            bool hasMultipleStepTypes = loopSteps.Any(item => item.GetType() != mainLoopStepType);

            string mainLoopStepName = mainLoopStep.Name;
            if (loopSteps.Count > 0) //Just summary step
            {
                if (report.api.TestMode == TestModeType.Active)
                {
                    mainLoopStep.stepRow.Loop.num = (short)loopSteps.Count;
                    mainLoopStep.stepRow.Loop.numSpecified = true;
                    mainLoopStep.stepRow.Loop.passed = 0;
                    mainLoopStep.stepRow.Loop.passedSpecified = true;
                    mainLoopStep.stepRow.Loop.failed = 0;
                    mainLoopStep.stepRow.Loop.failedSpecified = true;
                    mainLoopStep.stepRow.Loop.ending_index = (short)loopSteps.Count;
                    mainLoopStep.stepRow.Loop.ending_indexSpecified = true;

                    for (int i = 0; i < loopSteps.Count; i++)
                    {
                        loopSteps[i].Name = mainLoopStepName;
                        loopSteps[i].stepRow.Loop.index = (short)i;
                        loopSteps[i].stepRow.Loop.indexSpecified = true;

                        if (loopSteps[i].Status == StepStatusType.Passed)
                            mainLoopStep.stepRow.Loop.passed++;
                        else if (loopSteps[i].Status == StepStatusType.Failed)
                            mainLoopStep.stepRow.Loop.failed++;
                    }
                }
            }

            loopingActive = false;
            loopSteps = null;
            mainLoopStep = null;

            //Move to next step index after ending the loop
            GetNextStepIndex();

            //Verify this last so that TestStand Save can catch and ignore this error.
            if (hasMultipleStepTypes)
                throw new ArgumentException($"Loop {mainLoopStepName} contains more than one step type.");
        }

        /// <summary>
        /// *Only for loop* Adds a new sequencecall.
        /// </summary>
        /// <param name="stepName">Name of sequence</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns>new sequencecall, use this to add sub-steps</returns>
        public SequenceCall AddSequenceCall(string stepName, short index)
        {
            return AddSequenceCall(stepName, report.SequenceName, report.SequenceVersion, index);
        }

        /// <summary>
        /// *Only for loop* Adds a new sequence call
        /// </summary>
        /// <param name="stepName">Name of sequence step</param>
        /// <param name="sequenceName">Alternate name of sequence</param>
        /// <param name="sequenceVersion">Alternate sequence version</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public SequenceCall AddSequenceCall(string stepName, string sequenceName, string sequenceVersion, short index)
        {
            SequenceCall seqCall = AddSequenceCall(stepName, sequenceName, sequenceVersion);

            seqCall.stepRow.Loop.index = index;
            seqCall.stepRow.Loop.indexSpecified = true;

            return seqCall;
        }

        /// <summary>
        /// *Only for loop* Add a Numeric limit test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public NumericLimitStep AddNumericLimitStep(string stepName, short index)
        {
            NumericLimitStep step = AddNumericLimitStep(stepName);
            step.stepRow.Loop.index = index;
            step.stepRow.Loop.indexSpecified = true;

            return step;
        }

        /// <summary>
        /// *Only for loop* Add a String value test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public StringValueStep AddStringValueStep(string stepName, short index)
        {
            StringValueStep step = AddStringValueStep(stepName);
            step.stepRow.Loop.index = index;
            step.stepRow.Loop.indexSpecified = true;

            return step;
        }

        /// <summary>
        /// *Only for loop* Add a Pass/Fail (boolean) test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public PassFailStep AddPassFailStep(string stepName, short index)
        {
            PassFailStep step = AddPassFailStep(stepName);
            step.stepRow.Loop.index = index;
            step.stepRow.Loop.indexSpecified = true;

            return step;
        }

        /// <summary>
        /// *Only for loops* Adds a call to external program with exitCode
        /// </summary>
        /// <param name="stepName"></param>
        /// <param name="exitCode"></param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public CallExeStep AddCallExeStep(string stepName, double exitCode, short index)
        {
            CallExeStep step = AddCallExeStep(stepName, exitCode);

            step.stepRow.Loop.index = index;
            step.stepRow.Loop.indexSpecified = true;

            return step;
        }

        /// <summary>
        /// *Only for loops* Adds a generic step, see GenericStepTypes 
        /// </summary>
        /// <param name="stepType"></param>
        /// <param name="stepName"></param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public GenericStep AddGenericStep(GenericStepTypes stepType, string stepName, short index)
        {
            GenericStep step = AddGenericStep(stepType, stepName);

            step.stepRow.Loop.index = index;
            step.stepRow.Loop.indexSpecified = true;

            return step;
        }

        /// <summary>
        /// *Only for loops* Adds the result of a message popop.
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="buttonPressed">The button (numeric value) that was pressed</param>
        /// <param name="response">Response from the popup</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public MessagePopupStep AddMessagePopupStep(string stepName, short buttonPressed, string response, short index)
        {
            MessagePopupStep step = AddMessagePopupStep(stepName, buttonPressed, response);

            step.stepRow.Loop.index = index;
            step.stepRow.Loop.indexSpecified = true;

            return step;
        }

        #endregion

        protected internal override void RemoveStepData()
        {
            base.RemoveStepData();

            //Find all children recursivley, remove all their items, then remove the children.
            RemoveItems(stepRow);

            //Reset loop stuff
            stepRow.Loop = null;
            mainLoopStep = null;
            loopSteps = null;
            loopingActive = false;
            
            void RemoveItems(Step_type step)
            {
                var subSteps = reportRow.Items.OfType<Step_type>().Where(n => n.ParentStepIDSpecified && n.ParentStepID == step.StepID).ToList();
                foreach (var subStep in subSteps)
                {
                    RemoveItems(subStep);
                    reportRow.Items.Remove(subStep);
                }

                //Removes all non-step items belonging to this step
                reportRow.Items.RemoveAll(o => {
                    if (o is Step_type)
                        return false;

                    var property = o.GetType().GetProperty("StepID");                   
                    return property != null && (int)property.GetValue(o) == step.StepID;                    
                });
            }
        }
    }
}
