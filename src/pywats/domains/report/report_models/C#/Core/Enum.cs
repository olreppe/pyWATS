using System;

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
    public enum Modules { Database = 1, TransferAgent = 2, Datacenter = 3, Controlpanel = 4, Clientmonitor = 5, ServerConfigurator = 6, TestStation = 7, Core = 8, MESDatabase=9 }

    public enum FailureType { Default = 0, ManualProcess = 6, AutomaticProcess = 1, Scrapped = 2, NoFailureFound = 3, Component = 4, Design = 5, Replaced=7 }

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

        S_RolledThroughputYield  = 21,

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