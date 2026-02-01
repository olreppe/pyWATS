using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Interface
{

    /// <summary>
    /// Status of API
    /// </summary>
    public enum APIStatusType : short
    {
        /// <summary>
        /// Un-initialized, call initialize to set
        /// </summary>
        Unknown = 0,
        /// <summary>
        /// Online contact with WATS server ok
        /// </summary>
        Online = 1,
        /// <summary>
        /// Currently offline from WATS
        /// </summary>
        Offline = 2,
        /// <summary>
        /// The API is not setup properly, run the installer
        /// </summary>
        NotInstalled = 3,
        /// <summary>
        /// There is an error condition, see the application eventlog for details.
        /// </summary>
        Error = 4,
        /// <summary>
        /// The API is disposing - stop any processing immediately.
        /// </summary>
        Disposing = 5,
        /// <summary>
        /// The client is not registered with any server.
        /// </summary>
        NotRegistered = 6,
        /// <summary>
        /// The client is not activated for use with configured server
        /// </summary>
        NotActivated = 7
    }

    /// <summary>
    /// Sets or gets API test mode
    /// </summary>
    public enum TestModeType
    {
        /// <summary>
        /// API is recording test times, checking limits, fail steps etc. while recording test results
        /// </summary>
        Active,
        /// <summary>
        /// API just logs data, used for import of already compiled data
        /// </summary>
        Import,
        /// <summary>
        /// API logs data, allows inserting steps with "custom" StepOrderNumber, StepIndex and StatusText. No limit checking or other validation will occur in the API
        /// </summary>
        TestStand
    }

    /// <summary>
    /// Defines how the API will respond to errors.
    /// Main cases are:
    /// - Property length Violations
    /// - Invalid xml characters
    /// - Missing properties
    /// Invalid XML Characters are defined with this regular expression:
    /// [<![CDATA[(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]|[\uD800-\uDBFF](?![\uDC00-\uDFFF])|[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F\uFEFF\uFFFE\uFFFF]]]>
    /// </summary>
    public enum ValidationModeType
    {
        /// <summary>
        /// Will throw and exeption immediately when a property is set that 
        /// violates a length restriction or property contains invalid characters
        /// Missing fields will generate an exception on Submit
        /// </summary>
        ThrowExceptions,
        /// <summary>
        /// Will truncate properties and invalid characters will be removed or replaced
        /// Missing fields will still generate an exception on Submit
        /// Use this option with care as data loss can occur.
        /// </summary>
        AutoTruncate
    }

    /// <summary>
    /// Method for delivering reports.
    /// </summary>
    public enum SubmitMethod : short
    {
        /// <summary>
        /// Submit online (syncronous) if possible (API is connected), otherwise save report to queue.
        /// </summary>
        Automatic = 1,
        /// <summary>
        /// Always submit online (syncronous), throws exception if API is not connected
        /// </summary>
        Online=2,
        /// <summary>
        /// Save report to queue. Client Service will process the reports asyncronuosly.
        /// If used in LightWeight mode (sandboxed), the apllication must call <see cref="M:Virinco.WATS.Interface.TDM.SubmitPendingReports"/> to process the reports.
        /// </summary>
        Offline=3
    }

    /// <summary>
    /// Step / Measure status
    /// </summary>
    public enum StepStatusType : short
    {
        /// <summary>
        /// Successful operation
        /// </summary>
        Passed = 0, 
        /// <summary>
        /// Step done without any result
        /// </summary>
        Done = 1, 
        /// <summary>
        /// Step skipped
        /// </summary>
        Skipped = 2,
        /// <summary>
        /// Step Failed
        /// </summary>
        Failed = 3, 
        /// <summary>
        /// There was an error in the step
        /// </summary>
        Error = 4,
        /// <summary>
        /// Step terminated
        /// </summary>
        Terminated = 5
    }

    /// <summary>
    /// UUT status
    /// </summary>
    public enum UUTStatusType : short
    {
        /// <summary>
        /// Successful operation
        /// </summary>
        Passed = 0,
        /// <summary>
        /// Test Failed
        /// </summary>
        Failed = 1,
        /// <summary>
        /// There was an error in the test
        /// </summary>
        Error = 2,
        /// <summary>
        /// Test terminated
        /// </summary>
        Terminated = 3
    }


    /// <summary>
    /// Step Groups
    /// </summary>
    public enum StepGroupEnum : short
    {
        /// <summary>
        /// Setup phase of test
        /// </summary>
        Setup = 0, 

        /// <summary>
        /// Main phase of test
        /// </summary>
        Main = 1, 
        /// <summary>
        /// Cleanup phase of test
        /// </summary>
        Cleanup = 2
    }

    //public enum SQL2005FloatState : byte { Normal = 0x00, DeNormal = 0x01, PositiveInfinity = 0x02, NegativeInfinity = 0x03, NaN = 0x04 }


    /// <summary>
    /// Comparition operator
    /// </summary>
    public enum CompOperatorType : short
    {
        ///<summary>EQ (==)</summary>
        EQ=0,
        ///<summary>NE (!=)</summary>
        NE=1,
        ///<summary>GT (>)</summary>
        GT=2,
        ///<summary>LT (&lt;)</summary>
        LT=3,
        ///<summary>GE (>=)</summary>
        GE=4,
        ///<summary>LE (&lt;=)</summary>
        LE=5,
        ///<summary>GTLT (> AND &lt;)</summary>
        GTLT=6,
        ///<summary>GELE (>= AND &lt;=)</summary>
        GELE=7,
        ///<summary>GELT(>= AND &lt;)</summary>
        GELT=8,
        ///<summary>GTLE (> AND &lt;=)</summary>
        GTLE=9,
        ///<summary>LTGT (&lt; OR >)</summary>
        LTGT=10,
        ///<summary>LEGE (&lt;= OR >=)</summary>
        LEGE=11,
        ///<summary>LEGT(&lt;= OR >)</summary>
        LEGT=12,
        ///<summary>LTGE (&lt; OR >=)</summary>
        LTGE=13,
        ///<summary>No Comparison</summary>
        LOG=14,
        ///<summary>Case Sensitive</summary>
        CASESENSIT=15,
        ///<summary>Ignore Case</summary>
        IGNORECASE=16
    }

    /// <summary>
    /// Failure type used in WATS reporting
    /// </summary>
    public enum FailureTypeEnum
    {
        /// <summary>
        /// Common failure
        /// </summary>
        Default = 0,
        /// <summary>
        /// Process failure
        /// </summary>
        Process = 1,
        /// <summary>
        /// Unit scrapped
        /// </summary>
        Scrapped = 2,
        /// <summary>
        /// No failure found
        /// </summary>
        NoFailureFound = 3,
        /// <summary>
        /// Component failure
        /// </summary>
        Component = 4
    }


    /// <summary>
    /// Generic step types (without testdata) will generate icons 
    /// </summary>
    public enum GenericStepTypes : short
    {
        ///<summary>Inserts a label with StepName</summary>
        Label=0,                                        ///<summary>Generic icon</summary>
        Action = 1,                                     ///<summary>Generic icon</summary>
        Goto = 2,                                       ///<summary>Generic icon</summary>
        FTPFiles = 3,                                   ///<summary>Generic icon</summary>
        If = 4,                                         ///<summary>Generic icon</summary>
        ElseIf = 5,                                     ///<summary>Generic icon</summary>
        Else = 6,                                       ///<summary>Generic icon</summary>
        End = 7,                                        ///<summary>Generic icon</summary>
        For = 8,                                        ///<summary>Generic icon</summary>
        ForEach = 9,                                    ///<summary>Generic icon</summary>
        Break = 10,                                     ///<summary>Generic icon</summary>
        Continue = 11,                                  ///<summary>Generic icon</summary>
        DoWhile = 12,                                   ///<summary>Generic icon</summary>
        While = 13,                                     ///<summary>Generic icon</summary>
        Select = 14,                                    ///<summary>Generic icon</summary>
        Case = 15,                                      ///<summary>Generic icon</summary>
        Lock = 16,                                      ///<summary>Generic icon</summary>
        Rendezvous = 17,                                ///<summary>Generic icon</summary>
        Queue = 18,                                     ///<summary>Generic icon</summary>
        Notification = 19,                              ///<summary>Generic icon</summary>
        Wait = 20,                                      ///<summary>Generic icon</summary>
        BatchSyncronization = 21,                       ///<summary>Generic icon</summary>
        AutoSchedule = 22,                              ///<summary>Generic icon</summary>
        UseAutoScheduledResource = 23,                  ///<summary>Generic icon</summary>
        ThreadPriority = 24,                            ///<summary>Generic icon</summary>
        Semaphore = 25,                                 ///<summary>Generic icon</summary>
        BatchSpecification = 26,                        ///<summary>Generic icon</summary>
        OpenDatabase = 27,                              ///<summary>Generic icon</summary>
        OpenSQLStatement = 28,                          ///<summary>Generic icon</summary>
        CloseSQLStatement = 29,                         ///<summary>Generic icon</summary>
        CloseDatabase = 30,                             ///<summary>Generic icon</summary>
        DataOperation = 31,                             ///<summary>Generic icon</summary>
        IVIDmm = 32,                                    ///<summary>Generic icon</summary>
        IVIScope = 33,                                  ///<summary>Generic icon</summary>
        IVIFgen = 34,                                   ///<summary>Generic icon</summary>
        IVIPowerSupply = 35,                            ///<summary>Generic icon</summary>
        Switch = 36,                                    ///<summary>Generic icon</summary>
        IVITools = 37,                                  ///<summary>Generic icon</summary>
        CheckRemoteSystemStatus = 38,                   ///<summary>Generic icon</summary>
        RunVIAsynchronously = 39                        
    }                                           

    internal enum iconNames
    {
        Label = 0,
        Action = 1,
        Goto = 2,
        NI_FTPFiles = 3,
        NI_Flow_If = 4,
        NI_Flow_ElseIf = 5,
        NI_Flow_Else = 6,
        NI_Flow_End = 7,
        NI_Flow_For = 8,
        NI_Flow_ForEach = 9,
        NI_Flow_Break = 10,
        NI_Flow_Continue = 11,
        NI_Flow_DoWhile = 12,
        NI_Flow_While = 13,
        NI_Flow_Select = 14,
        NI_Flow_Case = 15,
        NI_Lock = 16,
        NI_Rendezvous = 17,
        NI_Queue = 18,
        NI_Notification = 19,
        NI_Wait = 20,
        NI_Batch_Sync = 21,
        NI_AutoSchedule = 22,
        NI_UseResource = 23,
        NI_ThreadPriority = 24,
        NI_Semaphore = 25,
        NI_BatchSpec = 26,
        NI_OpenDatabase = 27,
        NI_OpenSQLStatement = 28,
        NI_CloseSQLStatement = 29,
        NI_CloseDatabase = 30,
        NI_DataOperation = 31,
        NI_IVIDmm = 32,
        NI_IVIScope = 33,
        NI_IVIFgen = 34,
        NI_IVIPowerSupply = 35,
        NI_Switch = 36,
        NI_IVITools = 37,
        NI_LV_CheckSystemStatus = 38,
        NI_LV_RunVIAsynchronously = 39
    }
}


namespace Virinco.WATS
{
    public enum ProfileProperty
    {
        WatsFilters,
        CommonSettings,
        StartupDashboard
        //FullName,
        //CultureCode,
        //DOB
    }

    [Flags()]
    public enum ClientFunctions
    {
        None = 0x00,
        TDM = 0x01,
        MES = 0x02,
        All = 0xFF
    }

    public enum ClientLicenseTypes
    {
        Development = 0x01,
        Production = 0x02
    }

    public enum ClientIdentifierType
    {
        MacAddress = 0,
        Custom = 1
    }

    [Flags()]
    public enum MemberStatus
    {
        Unknown = 1,
        Offline = 2,
        Online = 4,
        Inactive = 8,
        Exception = 16,
        Freespace = 32,
        Pending = 64,
        Versions = 128
    }

    public enum StatusType
    {
        Passed = 0x01, Done = 0x02, Skipped = 0x08,
        Terminated = 0x20, Failed = 0x40, Error = 0x80,
        Unknown = 0x4000
    }

    public enum RecordState
    {
        Inactive = 0x00, Active = 0x01, Deleted = 0x02
    }

    public enum PeriodEnum
    {
        Hour, Day, Week, Month, Quarter, Year
    }

    public enum StepTypeEnum
    {
        SequenceCall = 0x0000,
        NumericLimitTest = 0x0010, ET_NLT = 0x0011, ET_MNLT = 0x0012,
        PassFailTest = 0x0020, ET_PFT = 0x0021, ET_MPFT = 0x0022,
        StringValueTest = 0x0030, ET_SVT = 0x0031, ET_MSVT = 0x0032,
        Action = 0x0040, ET_A = 0x0041,
        Label = 0x0050,
        CallExecutable = 0x0060,
        MessagePopup = 0x0070,
        NI_VariableAndPropertyLoader = 0x0080,
        NI_Wait = 0x0090,
        NI_Flow = 0x100,
        NI_Other = 0x200,
        Unknown = 0x4000
    }

    public enum StepDataTypeEnum
    {
        SequenceCall = 0x0000,
        NumericLimitTest = 0x0010,
        PassFailTest = 0x0020,
        StringValueTest = 0x0030,
        //Action = 0x0040,
        //Label = 0x0050,
        CallExecutable = 0x0060,
        MessagePopup = 0x0070,
        VariableAndPropertyLoader = 0x0080,
        //NI_Wait=0x0090,
        IVI_Singlepoint = 0x00A0,
        IVI_Wave = 0x00B0,
        IVI_Wavepair = 0x00C0,
        ChartData = 0x0800,
        Unknown = 0x4000
    }

    public enum StepGroupEnum
    {
        Setup = 0, Main = 1, Cleanup = 2, Unknown = 0x4000
    }

    [Flags]
    public enum StepGrouping
    {
        StepName = 1,
        DesignIndex = 2,
        StepID = 4,
        Group = 8,
    }

    public enum SQL2005FloatState : byte { Normal = 0x00, DeNormal = 0x01, PositiveInfinity = 0x02, NegativeInfinity = 0x03, NaN = 0x04 }

    /// <summary>
    /// Virinco.WATS.Modules is the Module identifier used in wats.Version.
    /// This enum replaces the old Virinco.WATS.DBC.Common.WATSModules (.\Base\Common_enum.cs)
    /// </summary>
    public enum Modules { Database = 1, TransferAgent = 2, Datacenter = 3, Controlpanel = 4, Clientmonitor = 5, ServerConfigurator = 6, TestStation = 7, Core = 8, MESDatabase = 9 }

    public enum FailureType { Default = 0, ManualProcess = 6, AutomaticProcess = 1, Scrapped = 2, NoFailureFound = 3, Component = 4, Design = 5, Replaced = 7 }

    public enum RequirementConstraint { Required = 0, Optional = 1, Never = 2 }

    public enum RootCauseStatus : short { New = 0, Open = 1, Solved = 2, Closed = 3, OnHold = 4 }

    public enum RootCausePriority : short { Low = 0, Normal = 1, High = 2 }
}

namespace Virinco.WATS.ClientService
{
    public enum WATSServiceCustomCommand
    {
        ReloadConfig = 0x80,
        CheckConnection = 0x81,
        SubmitConnectionTestReport = 0x82
    }

    public enum ConverterStateEnum
    {
        Created = 0,
        Running = 1,
        Failed = 2,
        Disposing = 3,
        FailedToStart = 4
    }
}

namespace Virinco.WATS.Security
{
    public enum RolePermissions
    {
        S_Survey = 0,

        S_TestAndRepairCategory = 1,
        S_UUTReport = 2,
        S_UUTExportWizard = 3,
        S_SerialNumberHistory = 4,
        S_UURReport = 5,
        S_RepairAnalysis = 6,
        S_RepairTime = 7,

        S_YieldCategory = 8,
        S_TestStepYieldAndAnalysis = 9,
        S_ProductAndTestYield = 10,
        S_ProductYield = 11,
        S_ProductByRevisionYield = 12,
        S_TotalProcessYield = 13,
        S_EmailBasedYieldMonitor = 14,

        S_StationCategory = 15,
        S_OEEAnalysis = 16,
        S_GRRAnalysis = 17,
        S_StationReport = 18,
        S_ProcessCapabilityAnalysis = 19,
        S_ConnectionExecutionTime = 20,

        S_RolledThroughputYield = 21,

        S_EmailCategory = 22,
        S_SummaryReport = 23,

        S_YieldReport = 24,



        MS_MESSurvey = 50,
        MS_UnitReport = 51,
        MS_WIPTracking = 52,

        SM_SystemManager = 100,
        SM_DeleteClients = 101,
        SM_DeleteClearEvents = 102,
        SM_ActivateClients = 103,
        SM_EditClientComments = 104,

        CV_CaptainsView = 150,//Not in use
        DA_Dashboard = 151,
        DA_EditPrivate = 152,//Not in use
        DA_EditGlobal = 153,
        DA_StationMap = 154,

        CS_ConfigureAndSettings = 200,
        CS_UserAndPermissions = 201,//only users
        CS_ProductRules = 202,
        CS_ProductGroups = 203,
        CS_EditProcess = 204,
        CS_EditWebClients = 205,
        CS_UpdateUUTReport = 206,
        CS_EditCPKValues = 207,   //Not in use
        CS_EditTranslation = 208,
        CS_EditArchive = 209,
        CS_PublishClientUpdates = 210,
        CS_EditLastOperations = 211,
        CS_EditGlobalProductGroups = 212,
        CS_EditKPITargets = 213,
        CS_RolesAndPermissions = 214,
        CS_ChangeLogo = 215,
        CS_UpdateUURReport = 216,
        CS_Account = 217,
        CS_RegisterClient = 218,
        CS_GetToken = 219,
        CS_SystemLanguageTranslation = 220,
        CS_DeleteReport = 221,
        CS_QuarantinedReports = 222,


        SW_SWDistribution = 250,
        SWP_PackageAdministrationCategory = 251,//Not in use
        SWP_CreatePackage = 252,
        SWP_MoveToPending = 253,
        SWP_ReleasePackage = 254,
        SWP_RevokePackage = 255,
        SWP_DeletePackage = 256,

        SWR_FileRepositoryCategory = 300,//not in use
        SWR_CreateRepository = 301, //Not in use
        SWR_AddFilesAndFolders = 302,
        SWR_DeleteFilesAndFolders = 303,
        SWR_RestrictedAccess = 304,
        SWR_PropertyEditor = 305,


        PM_ProductManager = 350,
        PM_CreateProductRevison = 351,
        PM_DeleteProductRevision = 352,
        PM_BoxBuilding = 353,
        PM_EditProductSettingsTags = 354,

        T_Tags = 400,//Not in use
        T_EditTags = 401,

        WF_WorkflowManager = 450,
        WF_EditWorkflow = 451,
        WF_MoveToPending = 452,
        WF_ReleaseWorkflow = 453,
        WF_RevokeWorkflow = 454,
        WF_DesignWorkflow = 455,
        WF_DeleteWorkflow = 456,

        OI_OperatorInterface = 500,
        OI_SkipTest = 501,
        OI_SkipRepair = 502,
        OI_SkipWIP = 503,
        OI_DisableUnitWorkflow = 504,
        OI_CreateUURreport = 505,
        OI_StationSettings = 506,
        OI_AdvancedSettings = 507,
        OI_SetUnitPhase = 508,
        OI_Test = 509,
        OI_Repair = 510,
        OI_WIP = 511,
        OI_UnitVerification = 512,
        OI_OverrideMESServerSettings = 513,
        OI_ScanUnitForActions = 514,

        AO_Addons = 550,
        AO_InterfaceTool = 551,
        AO_addon1 = 552,
        AO_addon2 = 553,
        AO_addon3 = 554,

        RC_RootCause = 600,
        RC_EditAllTickets = 601,
        RC_CreateTicket = 602,
        RC_AdminAllTickets = 603,

        MI_ManualInspectionManager = 650,
        MI_EditTestSequence = 651,
        MI_MoveToPending = 652,
        MI_ReleaseTestSequence = 653,
        MI_RevokeTestSequence = 654,
        MI_DesignTestSequence = 655,
        MI_DeleteTestSequence = 656,

        CUS_CustomReports = 700,
        CUS_BurninAnalysis = 701,
        CUS_NWA = 702,


        NS_NotificationSystem = 750,
        NS_Hardware = 751,
        NS_Statistics = 752,
        NS_SubSites = 753,
        NS_Maintenance = 754,
        NS_Information = 755,
        NS_Misc = 756,

        DSM_DataStreamManagement = 800,

        AM_AssetManager = 850,
        AM_CreateAssets = 851,
        AM_EditAssets = 852,
        AM_DeleteAssets = 853,

        PDM_ProductionManager = 900,

        Misc_BetaTester = 1000,

        API_RestApi = 1100,
        API_PostReport = 1101,

        //Mes Client Api actions
        API_SystemManager = 1102,
        API_MesProduction = 1103,
        API_MesProduct = 1104,
        API_MesSoftware = 1105,
        API_MesWorkflow = 1106,
        API_MesAsset = 1107,
        API_LocalServer = 1108,

        TA_TriggerAndAutomation = 1200
    }
}
namespace Virinco.WATS.Logging
{
    public enum LoggingLevel { ExceptionsOnly, Standard, Detailed, Debug }
    public enum LoggingType { Unknown, TransferAgent, DataCenter, ControlPanel }
    /// <summary>
    /// LogSeverity is syslog inspired priority (0-7).
    /// LogSeverity is based on byte (underlying type)
    /// LogSeverity description:
    ///   Emergency(0): system is unusable (not used by WATS)
    ///   Alert(1): action must be taken immediately (eg. invalid configuration)
    ///   Critical(2): critical conditions (eg. sustained network failure)
    ///   Error(3): error conditions (eg. repeated report failure)
    ///   Warning(4): warning conditions (eg. first report failure)
    ///   Notice(5): normal but significant condition (eg. configuration changes etc.)
    ///   Information(6): informational messages (eg. successful transfer etc.)
    ///   Debug(7): debug-level messages (eg. detailed transfer information, timing etc.)
    ///   
    /// Emergency and Alert : reserved for unexpected errors rendering the system unstable - also logged to Windows eventlog
    /// Critical : 
    /// Error : report errors during transfers etc.
    /// </summary>
    public enum LogSeverity : byte
    {
        EMERGENCY = 0,
        ALERT = 1,
        CRITICAL = 2,
        ERROR = 3,
        WARNING = 4,
        NOTICE = 5,
        INFORMATION = 6,
        DEBUG = 7
    }
    public enum LogCategory : byte
    {
        General = 0,
        Transfer = 1,
        Recieve = 2,
        DashBoard = 3,
        DataCenter = 4,
        DW_Load = 5,
        CV_App = 6,
        ControlPanel = 7,
        OperatorInterface = 8,
        ServiceFacade = 9,
        MesService = 10,

        TDMInterface = 11,
        MESInterface = 12,

        SystemCheck = 13,

        RESTApi = 14,

        Debug = 15,

        Hangfire = 16,

        Unknown = 255
    }
}
namespace Virinco.WATS.Transfer
{
    public enum MemberType { TestStation, LocalServer, MasterServer, ReportingServer, EmbeddedClient, OnlineClient, WebClient, VirtualLevel }
    //public enum MemberAccessType { DCPing, LifeSign, TransferItem, TransferPackage, GetUpdates, GetReport, SubmitMemberInfo }

    public enum TransferItemType { Unknown = -1, UUT = 1, RepairReport = 2, TextDataDump = 3 }
}
namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Client State enumeration value
    /// </summary>
    public enum ClientStateType : short
    {
        /// <summary>
        /// Unknown ClientState. Indicates that API is not yet Initialized. ClientState has not been determined yet. Run InitializeAPI before attempting to read ClientState.
        /// </summary>
        Unknown = 0,
        /// <summary>
        /// Client is not configured, run RegisterClient to register with server and download configuration.
        /// </summary>
        NotConfigured = 1,
        /// <summary>
        /// Client is running normally
        /// </summary>
        Active = 2,
        /// <summary>
        /// A non-critical issue has been registered, run client configurator to investigate and clear the warning flag
        /// </summary>
        Warning = 3,
        /// <summary>
        /// A critical issue has been registered, run client configurator to investigate and clear the error flag
        /// </summary>
        Error = 4

    }
}

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

    //public enum TagTypeEnum
    //{
    //    Unknown = 0,
    //    OperationType = 1,
    //    StationType=2,
    //    PartNumber=3,
    //    Site=4,
    //    Revision=5,
    //    StationName=6,
    //    Misc=7
    //}

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

        //Online = 4,
        //Inactive = 8,
        //Exception = 16,
        //Freespace = 32,
        //Pending = 64,
        //Versions = 128
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

    ///// <summary>
    ///// Used to link an activity to a process 
    ///// </summary>
    //public class ActivityProcess
    //{
    //    public string Name { get; set; }
    //    public string Code { get; set; }
    //}

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
        Under_Production_Q = 4096+2,     //Unit is under production in a queue'),
        Repair_Production_Q = 4096+4,    //Production Repair, Queued','Unit is waiting for production repair'),
        Repair_Service_Q = 4096+8         //Service repair, Queued','Unit is waiting for service repair(RMA)')
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