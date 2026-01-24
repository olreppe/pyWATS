using System;

namespace Virinco.WATS.Service.MES.Contract
{
    public enum StatusEnum
    {
        Draft = 0,
        Pending = 1,
        Released = 2,
        Revoked = 3
    }

    public enum VirtualFolderType
    {
        Workflow = 0,
        Package = 1,
        TestSequence = 2,
        RestrictedPackage = 3,
        InternalSystemFolder = 99 //default WF
    }

    public enum RepositoryType
    {
        Default = 0,
        ManualInspection = 1,
        VirincoInternal = 2, //default WF
        Restricted = 3, //available only for users with restricted access permission
        Labels = 4
    }

    [Flags()]
    public enum TagTypeEnum
    {
        None = 0,
        ReadOnly = 1,
        Internal = 2,
        Misc = 4,
        SoftwareManager = 8,
        ProductManager = 16,
        WorkflowManager = 32

    }


    [Flags()]
    public enum FileAttribute
    {
        None = 0,
        ExecuteOnce = 1,
        ExecuteAlways = 2,
        TopLevelFile = 4,
        OverwriteNever = 8,
        OverwriteOnNewPackageVersion = 16,
        ExecuteOncePerVersion = 32
    }


    public enum CompOperatorType : short
    {
        ///<summary>EQ (==)</summary>
        EQ = 0,
        ///<summary>NE (!=)</summary>
        NE = 1,
        ///<summary>GT (>)</summary>
        GT = 2,
        ///<summary>LT (&lt;)</summary>
        LT = 3,
        ///<summary>GE (>=)</summary>
        GE = 4,
        ///<summary>LE (&lt;=)</summary>
        LE = 5,
        ///<summary>GTLT (> AND &lt;)</summary>
        GTLT = 6,
        ///<summary>GELE (>= AND &lt;=)</summary>
        GELE = 7,
        ///<summary>GELT(>= AND &lt;)</summary>
        GELT = 8,
        ///<summary>GTLE (> AND &lt;=)</summary>
        GTLE = 9,
        ///<summary>LTGT (&lt; OR >)</summary>
        LTGT = 10,
        ///<summary>LEGE (&lt;= OR >=)</summary>
        LEGE = 11,
        ///<summary>LEGT(&lt;= OR >)</summary>
        LEGT = 12,
        ///<summary>LTGE (&lt; OR >=)</summary>
        LTGE = 13,
        ///<summary>No Comparison</summary>
        LOG = 14,
        ///<summary>Case Sensitive</summary>
        CASESENSIT = 15,
        ///<summary>Ignore Case</summary>
        IGNORECASE = 16,
        ///<summary>Regular Expression</summary>
        REGEX = 17
    }


    public enum StepResult : short
    {
        Unknown = 0,
        Passed = 1,
        Failed = 2,
        Error = 3
    }

    /// <summary>
    /// WATS Built in activity types
    /// </summary>
    public enum ActivityType : short
    {
        Initialize,
        WIPPoint,
        Test,
        Repair,
        UserInput,
        UnitContent
    }

    /// <summary>
    /// Possible Activity methods
    /// </summary>
    public enum ActivityMethod : short
    {
        Initialize,
        Validate,
        StartTest,
        EndTest,
        CheckIn,
        CheckOut,
        StartRepair,
        EndRepair,
        Scrap,
        UserInput,
        AddUnit,
        RemoveUnit,
        CheckUnit
    }

    /// <summary>
    /// Test result
    /// </summary>
    public enum ActivityTestResult : short
    {
        Unknown,
        Passed,
        Failed,
        Error
    }

    /// <summary>
    /// User input alternatives
    /// </summary>
    public enum UserInputType : short
    {
        Text,
        YesNo,
        Message
    }

    public enum UnitContentAction : short
    {
        AddUnit,
        RemoveChildUnit,
        RemoveAllChildUnits,
        CheckUnit
    }


    /// <summary>
    /// Possible unit phases
    /// </summary>
    [Flags()]
    public enum Unit_Phase : short
    {
        Unknown = 1,                    //Initial state
        Under_Production = 2,           //Unit is under production
        Repair_Production = 4,          //Unit is under production repair
        Repair_Service = 8,             //Unit is under service repair (RMA)
        Finalized = 16,                 //Unit is finished
        Scrapped = 32,                  //Unit is scrapped
        Extended_Test = 64,             //Unit is under an extended test
        Customization = 128,            //Unit is under customization
        Repaired = 256,                 //Unit has been repaired
        Missing = 512,                  //Unit is missing (in production/repair too long, for example)
        In_Storage = 1024,              //Unit is in storage/warehouse
        Shipped = 2048,                 //Unit is shipped (out of factory)
        Queued = 4096,                  //Combination flag, common combination is Under_Production and Repair*
        Under_Production_Q = 4096 + 2,     //Unit is under production in a queue'),
        Repair_Production_Q = 4096 + 4,    //Production Repair, Queued','Unit is waiting for production repair'),
        Repair_Service_Q = 4096 + 8         //Service repair, Queued','Unit is waiting for service repair(RMA)')
    }

    /// <summary>
    /// Information about the workflow instance. Called to either validate or execute a workflow,
    /// see stored procedure GetWorkflowInstance for more information. Also passed as a result in WorkflowResponse.
    /// WorkflowInstanceStatus is a part of <see cref="WorkflowResponse"/>. OK will be true except cases 1 and 2
    /// </summary>
    public enum WorkflowInstanceStatus : short
    {
        ///<summary>Not OK, Workflow software error, Network error etc</summary>
        SystemError = 1,
        ///<summary>Not OK, Attempted action / process is not according to instance current process</summary>
        ValidationError = 2,
        ///<summary>An active workflow exist, this is the normal situation</summary>
        ActiveWorkflowExist = 3,
        ///<summary>A workflow is defined, but it is not initialized</summary>
        WorkflowNotInitialized = 4,
        ///<summary>A workflow is defined, but it is completed previously</summary>
        WorkflowCompleted = 5,
        ///<summary>There is no workflow assigned to this unit</summary>
        WorkflowNotDefined = 6,
        ///<summary>There is an active workflow instance, but is has been suspended</summary>
        WorkflowSuspended = 7,
        ///<summary>The previous workflow has been cancelled</summary>
        WorkflowCancelled = 8
    }
}