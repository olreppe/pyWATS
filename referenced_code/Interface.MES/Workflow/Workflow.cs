extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using napict = newclientapi::Virinco.WATS.Service.MES.Contract;
using Virinco.WATS.Service.MES.Contract;
using System.Collections.Generic;

namespace Virinco.WATS.Interface.MES.Workflow
{
    /// <summary>
    /// Class that represent a workflow
    /// </summary>
    public class Workflow : MesBase
    {
        private napi.Workflow.Workflow _instance;

        internal Workflow(napi.Workflow.Workflow workflow)
        {
            this._instance = workflow;
        }

        /// <summary>
        /// True if connected to server
        /// </summary>
        /// <returns></returns>
        new public bool isConnected() => _instance.isConnected();

        /// <summary>
        /// Start automated test
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse StartTest(string SerialNumber, string PartNumber, string Operation, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.StartTest(SerialNumber, PartNumber, Operation, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// End test with result
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="Result"></param>
        /// <param name="ForceExit"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse EndTest(string SerialNumber, string PartNumber, string Operation, ActivityTestResult Result, bool ForceExit, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.EndTest(SerialNumber, PartNumber, Operation, (napict.ActivityTestResult)(int)Result, ForceExit, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Validate workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Method"></param>
        /// <param name="Name"></param>
        /// <param name="inputValues"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <param name="generateImage"></param>
        /// <returns></returns>
        public WorkflowResponse Validate(string SerialNumber, string PartNumber, ActivityMethod Method, string Name, Dictionary<string, object> inputValues, StatusEnum workflowDefinitionStatus = StatusEnum.Released, bool generateImage = false)
            => new WorkflowResponse(_instance.Validate(SerialNumber, PartNumber, (napict.ActivityMethod)(int)Method, Name, inputValues, (napict.StatusEnum)(int)workflowDefinitionStatus, generateImage));

        /// <summary>
        /// Initialize a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Initialize(string SerialNumber, string PartNumber, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.Initialize(SerialNumber, PartNumber, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Performs a Check-In on a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse CheckIn(string SerialNumber, string PartNumber, string Operation, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.CheckIn(SerialNumber, PartNumber, Operation, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Performs a Check-Out on a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse CheckOut(string SerialNumber, string PartNumber, string Operation, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.CheckOut(SerialNumber, PartNumber, Operation, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Performs a UserInput on a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse UserInput(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.UserInput(SerialNumber, PartNumber, Operation, UserInput, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Start repair
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse StartRepair(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.StartRepair(SerialNumber, PartNumber, Operation, UserInput, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// End repair
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse EndRepair(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.EndRepair(SerialNumber, PartNumber, Operation, UserInput, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Scrap a unit under repair
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Scrap(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.Scrap(SerialNumber, PartNumber, Operation, UserInput, inputValues, promptOperator, AlwaysOnTop, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Suspends a workflow 
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Suspend(string SerialNumber, string PartNumber, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.Suspend(SerialNumber, PartNumber, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Resumes a suspended workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Resume(string SerialNumber, string PartNumber, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.Resume(SerialNumber, PartNumber, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Cancels an active workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Cancel(string SerialNumber, string PartNumber, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
            => new WorkflowResponse(_instance.Cancel(SerialNumber, PartNumber, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Adds unit in a boxbuild
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="ChildSerialNumber"></param>
        /// <param name="ChildPartNumber"></param>
        /// <param name="ActivityName"></param>
        /// <param name="inputValues"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse AddUnit(string SerialNumber, string PartNumber, string ChildSerialNumber, string ChildPartNumber, string ActivityName, Dictionary<string, object> inputValues, StatusEnum workflowDefinitionStatus)
            => new WorkflowResponse(_instance.AddUnit(SerialNumber, PartNumber, ChildSerialNumber, ChildPartNumber, ActivityName, inputValues, (napict.StatusEnum)(int)workflowDefinitionStatus));

        /// <summary>
        /// Removes a sub unit
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="ChildSerialNumber"></param>
        /// <param name="ChildPartNumber"></param>
        /// <param name="ActivityName"></param>
        /// <param name="inputValues"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse RemoveUnit(string SerialNumber, string PartNumber, string ChildSerialNumber, string ChildPartNumber, string ActivityName, Dictionary<string, object> inputValues, StatusEnum workflowDefinitionStatus)
            => new WorkflowResponse(_instance.RemoveUnit(SerialNumber, PartNumber, ChildSerialNumber, ChildPartNumber, ActivityName, inputValues, (napict.StatusEnum)(int)workflowDefinitionStatus));
    }
}
