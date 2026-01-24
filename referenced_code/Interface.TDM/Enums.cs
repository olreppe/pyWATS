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

    public static class EnumExtensions
    {
        public static TTarget CastTo<TTarget>(this Enum source) where TTarget : Enum
        {
            return (TTarget)Enum.ToObject(typeof(TTarget), Convert.ToInt32(source));
        }
    }
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

