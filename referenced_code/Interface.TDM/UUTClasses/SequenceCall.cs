extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Management;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// 
    /// </summary>
    public class SequenceCall : Step
    {
        internal napi.SequenceCall _instance;
        internal SequenceCall(napi.SequenceCall instance) : base(instance) { _instance = instance; }

        /// <summary>
        /// Sequence name - name of test program
        /// </summary>
        public string SequenceName
        {
            get => _instance.SequenceName;
            set => _instance.SequenceName = value;
        }

        /// <summary>
        /// Version of sequence
        /// </summary>
        public string SequenceVersion
        {
            get => _instance.SequenceVersion;
            set => _instance.SequenceVersion = value;
        }

        /// <summary>
        /// Adds a new sequencecall.
        /// </summary>
        /// <param name="stepName">Name of sequence</param>
        /// <returns>new sequencecall, use this to add sub-steps</returns>
        public SequenceCall AddSequenceCall(string stepName)
            => new SequenceCall(_instance.AddSequenceCall(stepName));

        /// <summary>
        /// Adds a new sequence call
        /// </summary>
        /// <param name="stepName">Name of sequence step</param>
        /// <param name="sequenceName">Alternate name of sequence</param>
        /// <param name="sequenceVersion">Alternate sequence version</param>
        /// <returns></returns>
        public SequenceCall AddSequenceCall(string stepName, string sequenceName, string sequenceVersion)
            => new SequenceCall(_instance.AddSequenceCall(stepName, sequenceName, sequenceVersion));

        /// <summary>
        /// Add a Numeric limit test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Name of step</param>
        /// <returns></returns>
        public NumericLimitStep AddNumericLimitStep(string stepName)
            => new NumericLimitStep(_instance.AddNumericLimitStep(stepName));

        /// <summary>
        /// Adds a Pass/Fail (boolean) step, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        public PassFailStep AddPassFailStep(string stepName)
            => new PassFailStep(_instance.AddPassFailStep(stepName));

        /// <summary>
        /// Adds a string value step, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName"></param>
        /// <returns></returns>
        public StringValueStep AddStringValueStep(string stepName)
            => new StringValueStep(_instance.AddStringValueStep(stepName));

        /// <summary>
        /// Adds a call to external program with exitCode
        /// </summary>
        /// <param name="stepName"></param>
        /// <param name="exitCode"></param>
        /// <returns></returns>
        public CallExeStep AddCallExeStep(string stepName, double exitCode)
            => new CallExeStep(_instance.AddCallExeStep(stepName, exitCode));

        /// <summary>
        /// Adds a generic step, see GenericStepTypes 
        /// </summary>
        /// <param name="stepType"></param>
        /// <param name="stepName"></param>
        /// <returns></returns>
        public GenericStep AddGenericStep(GenericStepTypes stepType, string stepName)
            => new GenericStep(_instance.AddGenericStep((napi.GenericStepTypes)(int)stepType, stepName));

        /// <summary>
        /// Adds the result of a message popop.
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="buttonPressed">The button (numeric value) that was pressed</param>
        /// <param name="response">Response from the popup</param>
        /// <returns></returns>
        public MessagePopupStep AddMessagePopupStep(string stepName, short buttonPressed, string response)
            => new MessagePopupStep(_instance.AddMessagePopupStep(stepName, buttonPressed, response));

        /// <summary>
        /// Adds a Teststand Description loader step
        /// </summary>
        /// <param name="stepName"></param>
        /// <param name="numPropApplied"></param>
        /// <param name="numPropRead"></param>
        /// <returns></returns>
        public PropertyLoaderStep AddPropertyLoaderStep(string stepName, short numPropApplied, short numPropRead)
            => new PropertyLoaderStep(_instance.AddPropertyLoaderStep(stepName, numPropApplied, numPropRead));

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
            => new SequenceCall(napi.SequenceCall.Create(ParentStep._baseinstance, stepIndex, stepGroup, stepType,
                stepName, sequenceName, sequenceFile, sequenceFileVersion, stepStatusText, startDateTime, errorCode, errorMessage, stepTime, moduleTime));

        #region Looping
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
            throw new NotImplementedException("Looping is not longer supported in the legacy WATS Client Api, switch to the new WATS Client Api for looping support");
            //var itm = _instance.StartLoop<T>(stepName, iterations, passed, failed, endingIndex);

            //if (_instance.loopingActive)
            //    return null;

            //loopSteps = new List<Step>();
            //loopingActive = true;

            //T step;
            //if (typeof(T) == typeof(SequenceCall))
            //    step = new SequenceCall(report, reportRow, this, stepName, "", "") as T;
            //else if (typeof(T) == typeof(NumericLimitStep))
            //    step = new NumericLimitStep(report, reportRow, this, stepName) as T;
            //else if (typeof(T) == typeof(StringValueStep))
            //    step = new StringValueStep(report, reportRow, this, stepName) as T;
            //else if (typeof(T) == typeof(PassFailStep))
            //    step = new PassFailStep(report, reportRow, this, stepName) as T;
            //else if (typeof(T) == typeof(GenericStep))
            //    step = new GenericStep(report, reportRow, this, stepName, GenericStepTypes.Action.ToString()) as T;
            //else if (typeof(T) == typeof(CallExeStep))
            //    step = new CallExeStep(report, reportRow, this, stepName, 0) as T;
            //else if (typeof(T) == typeof(MessagePopupStep))
            //    step = new MessagePopupStep(report, reportRow, this, stepName, 0, "") as T;
            //else
            //    throw new ArgumentException($"{typeof(T)} is not a valid loop step type.");

            //step.stepRow.Loop = new Step_typeLoop()
            //{
            //    num = iterations ?? 0,
            //    numSpecified = iterations != null ? true : false,
            //    passed = passed ?? 0,
            //    passedSpecified = passed != null ? true : false,
            //    failed = failed ?? 0,
            //    failedSpecified = failed != null ? true : false,
            //    ending_index = endingIndex ?? 0,
            //    ending_indexSpecified = endingIndex != null ? true : false,
            //};

            //mainLoopStep = step;

            //return step;
        }

        /// <summary>
        /// Stops and finalizes the current loop. 
        /// </summary>
        public void StopLoop()
        {
            throw new NotImplementedException("Looping is not longer supported in the legacy WATS Client Api, switch to the new WATS Client Api for looping support");
            //if (!loopingActive)
            //    return;

            ////Verifies that loopSteps only contains one step type
            //var mainLoopStepType = mainLoopStep.GetType();
            //bool hasMultipleStepTypes = loopSteps.Any(item => item.GetType() != mainLoopStepType);

            //string mainLoopStepName = mainLoopStep.Name;
            //if (loopSteps.Count > 0) //Just summary step
            //{
            //    if (report.api.TestMode == TestModeType.Active)
            //    {
            //        mainLoopStep.stepRow.Loop.num = (short)loopSteps.Count;
            //        mainLoopStep.stepRow.Loop.numSpecified = true;
            //        mainLoopStep.stepRow.Loop.passed = 0;
            //        mainLoopStep.stepRow.Loop.passedSpecified = true;
            //        mainLoopStep.stepRow.Loop.failed = 0;
            //        mainLoopStep.stepRow.Loop.failedSpecified = true;
            //        mainLoopStep.stepRow.Loop.ending_index = (short)loopSteps.Count;
            //        mainLoopStep.stepRow.Loop.ending_indexSpecified = true;

            //        for (int i = 0; i < loopSteps.Count; i++)
            //        {
            //            loopSteps[i].Name = mainLoopStepName;
            //            loopSteps[i].stepRow.Loop.index = (short)i;
            //            loopSteps[i].stepRow.Loop.indexSpecified = true;

            //            if (loopSteps[i].Status == StepStatusType.Passed)
            //                mainLoopStep.stepRow.Loop.passed++;
            //            else if (loopSteps[i].Status == StepStatusType.Failed)
            //                mainLoopStep.stepRow.Loop.failed++;
            //        }
            //    }
            //}

            //loopingActive = false;
            //loopSteps = null;
            //mainLoopStep = null;

            ////Move to next step index after ending the loop
            //GetNextStepIndex();

            ////Verify this last so that TestStand Save can catch and ignore this error.
            //if (hasMultipleStepTypes)
            //    throw new ArgumentException($"Loop {mainLoopStepName} contains more than one step type.");
        }

        /// <summary>
        /// *Only for loop* Adds a new sequencecall.
        /// </summary>
        /// <param name="stepName">Name of sequence</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns>new sequencecall, use this to add sub-steps</returns>
        public SequenceCall AddSequenceCall(string stepName, short index)
            => new SequenceCall(_instance.AddSequenceCall(stepName, index));

        /// <summary>
        /// *Only for loop* Adds a new sequence call
        /// </summary>
        /// <param name="stepName">Name of sequence step</param>
        /// <param name="sequenceName">Alternate name of sequence</param>
        /// <param name="sequenceVersion">Alternate sequence version</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public SequenceCall AddSequenceCall(string stepName, string sequenceName, string sequenceVersion, short index)
            => new SequenceCall(_instance.AddSequenceCall(stepName, sequenceName, sequenceVersion, index));

        /// <summary>
        /// *Only for loop* Add a Numeric limit test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public NumericLimitStep AddNumericLimitStep(string stepName, short index)
            => new NumericLimitStep(_instance.AddNumericLimitStep(stepName, index));

        /// <summary>
        /// *Only for loop* Add a String value test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public StringValueStep AddStringValueStep(string stepName, short index)
            => new StringValueStep(_instance.AddStringValueStep(stepName, index));

        /// <summary>
        /// *Only for loop* Add a Pass/Fail (boolean) test, can contain a single test or multiple (named) tests
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public PassFailStep AddPassFailStep(string stepName, short index)
            => new PassFailStep(_instance.AddPassFailStep(stepName, index));

        /// <summary>
        /// *Only for loops* Adds a call to external program with exitCode
        /// </summary>
        /// <param name="stepName"></param>
        /// <param name="exitCode"></param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public CallExeStep AddCallExeStep(string stepName, double exitCode, short index)
            => new CallExeStep(_instance.AddCallExeStep(stepName, exitCode, index));

        /// <summary>
        /// *Only for loops* Adds a generic step, see GenericStepTypes 
        /// </summary>
        /// <param name="stepType"></param>
        /// <param name="stepName"></param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public GenericStep AddGenericStep(GenericStepTypes stepType, string stepName, short index)
            => new GenericStep(_instance.AddGenericStep((napi.GenericStepTypes)(int)stepType, stepName, index));

        /// <summary>
        /// *Only for loops* Adds the result of a message popop.
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="buttonPressed">The button (numeric value) that was pressed</param>
        /// <param name="response">Response from the popup</param>
        /// <param name="index">Iteration index of the loop</param>
        /// <returns></returns>
        public MessagePopupStep AddMessagePopupStep(string stepName, short buttonPressed, string response, short index)
            => new MessagePopupStep(_instance.AddMessagePopupStep(stepName, buttonPressed, response, index));

        #endregion
    }
}
