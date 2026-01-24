using System;
using System.Collections.Generic;
using System.Runtime.Serialization;
using System.Globalization;

namespace Virinco.WATS.Service.MES.Contract
{
    ///// <summary>
    ///// WATS Built in activity types
    ///// </summary>
    //public enum ActivityType : short
    //{
    //    Initialize,
    //    WIPPoint,
    //    Test,
    //    Repair,
    //    UserInput,
    //    UnitContent
    //}

    ///// <summary>
    ///// Possible Activity methods
    ///// </summary>
    //public enum ActivityMethod : short
    //{
    //    Initialize,
    //    Validate,
    //    StartTest,
    //    EndTest,
    //    CheckIn,
    //    CheckOut,
    //    StartRepair,
    //    EndRepair,
    //    Scrap,
    //    UserInput,
    //    AddUnit,
    //    RemoveUnit,
    //    CheckUnit
    //}

    /////// <summary>
    /////// Used to link an activity to a process 
    /////// </summary>
    ////public class ActivityProcess
    ////{
    ////    public string Name { get; set; }
    ////    public string Code { get; set; }
    ////}

    ///// <summary>
    ///// Test result
    ///// </summary>
    //public enum ActivityTestResult : short
    //{
    //    Unknown,
    //    Passed,
    //    Failed,
    //    Error
    //}

    ///// <summary>
    ///// User input alternatives
    ///// </summary>
    //public enum UserInputType : short
    //{
    //    Text,
    //    YesNo,
    //    Message
    //}

    //public enum UnitContentAction : short
    //{
    //    AddUnit,
    //    RemoveChildUnit,
    //    RemoveAllChildUnits,
    //    CheckUnit
    //}


    ///// <summary>
    ///// Possible unit phases
    ///// </summary>
    //[Flags()]
    //public enum Unit_Phase : short
    //{
    //    Unknown = 1,                    //Initial state
    //    Under_Production = 2,           //Unit is under production
    //    Repair_Production = 4,          //Unit is under production repair
    //    Repair_Service = 8,             //Unit is under service repair (RMA)
    //    Finalized = 16,                 //Unit is finished
    //    Scrapped = 32,                  //Unit is scrapped
    //    Extended_Test = 64,             //Unit is under an extended test
    //    Customization = 128,            //Unit is under customization
    //    Repaired = 256,                 //Unit has been repaired
    //    Missing = 512,                  //Unit is missing (in production/repair too long, for example)
    //    In_Storage = 1024,              //Unit is in storage/warehouse
    //    Shipped = 2048,                 //Unit is shipped (out of factory)
    //    Queued = 4096,                  //Combination flag, common combination is Under_Production and Repair*
	   // Under_Production_Q= 4096+2,     //Unit is under production in a queue'),
	   // Repair_Production_Q= 4096+4,    //Production Repair, Queued','Unit is waiting for production repair'),
	   // Repair_Service_Q=4096+8         //Service repair, Queued','Unit is waiting for service repair(RMA)')
    //}

    ///// <summary>
    ///// Information about the workflow instance. Called to either validate or execute a workflow,
    ///// see stored procedure GetWorkflowInstance for more information. Also passed as a result in WorkflowResponse.
    ///// WorkflowInstanceStatus is a part of <see cref="WorkflowResponse"/>. OK will be true except cases 1 and 2
    ///// </summary>
    //public enum WorkflowInstanceStatus : short
    //{
    //    ///<summary>Not OK, Workflow software error, Network error etc</summary>
    //    SystemError = 1,
    //    ///<summary>Not OK, Attempted action / process is not according to instance current process</summary>
    //    ValidationError=2,
    //    ///<summary>An active workflow exist, this is the normal situation</summary>
    //    ActiveWorkflowExist = 3,
    //    ///<summary>A workflow is defined, but it is not initialized</summary>
    //    WorkflowNotInitialized = 4,
    //    ///<summary>A workflow is defined, but it is completed previously</summary>
    //    WorkflowCompleted = 5,
    //    ///<summary>There is no workflow assigned to this unit</summary>
    //    WorkflowNotDefined = 6,
    //    ///<summary>There is an active workflow instance, but is has been suspended</summary>
    //    WorkflowSuspended = 7,
    //    ///<summary>The previous workflow has been cancelled</summary>
    //    WorkflowCancelled = 8
    //}

    [DataContract(Namespace = "​​http://wats.virinco.local/mes/")]
    public class ValidateWorkflowRequest
    {
        [DataMember]
        public Guid WorkflowInstanceId { get; set; }
        [DataMember]
        public ActivityMethod Method { get; set; }
        [DataMember]
        public string Name { get; set; }
        [DataMember]
        public Dictionary<string, object> InputValues;
        [DataMember]
        public string CultureCode { get; set; }
    }

    [DataContract(Namespace="​​http://wats.virinco.local/mes/")]
    [KnownType(typeof(UserInputType))]
    [KnownType(typeof(ActivityTestResult))]
    public class WorkflowResponse
    {
        public WorkflowResponse()
        {
            AllowedMethods = new List<ActivityMethod>();
            ok = true;
            _instanceStatus = WorkflowInstanceStatus.ActiveWorkflowExist;
        }

        public void SetError(string errorMessage, string description)
        {
            ok = false;
            ErrorMessage = errorMessage;
            if (description!=null) Description = description;
        }

        private string _errorMessage="";
        private WorkflowInstanceStatus _instanceStatus;

        [DataMember]
        public bool ok { get; set; }
        [DataMember]
        public WorkflowInstanceStatus InstanceStatus
        {
            get { return _instanceStatus; }
            set 
            {
                switch (value)
                {
                    case WorkflowInstanceStatus.SystemError:
                    case WorkflowInstanceStatus.ValidationError:
                        ok = false;
                        _instanceStatus = value;
                        break;
                    default:
                        _instanceStatus = value;
                        break;
                }
            }
        }
        [DataMember]
        public ActivityType CurrentActivity { get; set; }
        [DataMember]
        public ICollection<ActivityMethod> AllowedMethods { get; set; }
        [DataMember]
        public string CurrentActivityName { get; set; }
        [DataMember]
        public string ErrorMessage
        {
            get { return _errorMessage; }
            set 
            {  
                _errorMessage = value; 
                ok = string.IsNullOrEmpty(_errorMessage);
            }
        }
        [DataMember]
        public string Description { get; set; }

        [DataMember]
        public byte [] Image { get; set; }

        [DataMember]
        public Dictionary<string, object> ReturnValues;
    }
    
}
