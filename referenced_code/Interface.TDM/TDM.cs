extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;
using System.Xml.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Library toolkit to create test in WATS
    /// </summary>
    public class TDM : IDisposable
    {
        internal readonly newclientapi::Virinco.WATS.Interface.TDM _instance = new newclientapi::Virinco.WATS.Interface.TDM();

        #region Internal helpers and data handling
        /// <summary>
        /// Get result from rest call to server 
        /// </summary>
        /// <param name="query"></param>
        /// <returns></returns>
        public responseType GetFromServer<responseType>(string query)
            => _instance.GetFromServer<responseType>(query);

        /// <summary>
        /// Target WATS Service URL
        /// Points to WATS Root address, REST Api can be found under /api, datacenter under /wats-dc, wats web application on root
        /// </summary>
        public string TargetURL
        {
            get => _instance.TargetURL;
        }

        /// <summary>
        /// Specifies if API should raise Exceptions after logging to EventLog
        /// </summary>
        public bool RethrowException // r/w
        {
            get => _instance.RethrowException;
            set => _instance.RethrowException = value;
        }

        /// <summary>
        /// Property to set if any Exception should be written to eventlog
        /// </summary>
        public bool LogExceptions // r/w
        {
            get => _instance.LogExceptions;
            set => _instance.LogExceptions = value;
        }

        /// <summary>
        /// Guid identifying Station
        /// </summary>
        /// <remarks>Automatically generated and saved on workstation on first time connection</remarks>
        [Obsolete("MemberId should not be depended on. Starting from WATS Version 5.0 the client is identified by primary network adapter's MAC Address.", false)]
        public Guid MemberId // r/o
        {
            get => _instance.MemberId;
        }

        /// <summary>
        /// Disk location for storage of pending reports
        /// </summary>
        public string DataDir // r/o
        {
            get => _instance.DataDir;
        }

        /// <summary>
        /// Name of test machine
        /// </summary>
        public string StationName
        {
            get => _instance.StationName;
            set => _instance.StationName = value;
        }

        /// <summary>
        /// Returns list of defined processes (locally buffered)
        /// </summary>
        /// <returns></returns>
        public static List<Models.Process> GetProcesses()
            => napi.TDM.GetProcesses().Select(p => new Models.Process(p)).ToList();

        /// <summary>
        /// Purpose of test machine
        /// </summary>
        public string Purpose // r/o
        {
            get => _instance.Purpose;
            //set => _instance.Purpose = value;
        }

        /// <summary>
        /// Test station location
        /// </summary>
        public string Location // r/o
        {
            get => _instance.Location;
            //set => _instance.Location = value;
        }

        /// <summary>
        /// Change setup information (default values)
        /// To configure the api with permanent values use (string,string,string,true)
        /// </summary>
        /// <param name="dataDir">Temp location for reports</param>
        /// <param name="location">Test station location</param>
        /// <param name="purpose">Test station purpose</param>
        /// <param name="Persist">Set to true to overwrite values in registry - use with caution.</param>
        public void SetupAPI(string dataDir, string location, string purpose, bool Persist)
            => _instance.SetupAPI(dataDir, location, purpose, Persist);

        /// <summary>
        /// Change setup information (default values), This overload is obsolete and should not be used. It will be removed in a future release.
        /// Starting from v5.0 WCF has been replaced with REST based service.
        /// use void SetupAPI(string dataDir, string location, string purpose, bool Persist) instead.
        /// </summary>
        /// <param name="dataDir">Temp location for reports</param>
        /// <param name="location">Test station location</param>
        /// <param name="purpose">Test station purpose</param>
        /// <param name="wcfConfigFile">Full path to a WCF configuration file</param>
        /// <param name="tdmEndpoint">Name of TDM endpoint</param>
        /// <param name="mesEndpoint">Name of MES endpoint</param>
        /// <param name="Persist">Set to true to overwrite values in registry - use with caution.</param>
        [Obsolete("This overload of SetupAPI is no longer supported in this version of the API", false)]
        public void SetupAPI(string dataDir, string location, string purpose, string wcfConfigFile, string tdmEndpoint, string mesEndpoint, bool Persist)
            => _instance.SetupAPI(dataDir, location, purpose, wcfConfigFile, tdmEndpoint, mesEndpoint, Persist);

        /// <summary>
        /// Change setup information (default values), This overload is obsolete and should not be used. It will be removed in a future release.
        /// Starting from v5.0 WCF has been replaced with REST based service.
        /// use void SetupAPI(string dataDir, string location, string purpose, bool Persist) instead.
        /// </summary>
        /// <param name="dataDir">Temp location for reports</param>
        /// <param name="location">Test station location</param>
        /// <param name="purpose">Test station purpose</param>
        /// <param name="wcfConfigFile">Full path to a WCF configuration file</param>
        /// <param name="tdmEndpoint">Name of TDM endpoint</param>
        /// <param name="mesEndpoint">Name of MES endpoint</param>
        [Obsolete("This overload of SetupAPI is no longer supported in this version of the API", true)]
        public void SetupAPI(string dataDir, string location, string purpose, string wcfConfigFile, string tdmEndpoint, string mesEndpoint)
            => _instance.SetupAPI(dataDir, location, purpose, wcfConfigFile, tdmEndpoint, mesEndpoint);

        /// <summary>
        /// Returns number of reports waiting to be sent to server, including senderror
        /// </summary>
        /// <returns></returns>
        public int GetPendingReportCount()
            => _instance.GetPendingReportCount();

        /// <summary>
        /// Returns number of reports waiting to be sent to server, including SendError.
        /// </summary>
        /// <param name="LoadError">Returns number of reports that failed during load from disk. These reports will not be retransmitted.</param>
        /// <param name="SendError">Returns number of reports that failed during send to server. These reports will be retried every 2 hours.</param>
        /// <returns></returns>
        public int GetPendingReportCount(ref int LoadError, ref int SendError)
            => _instance.GetPendingReportCount(ref LoadError, ref SendError);

        /// <summary>
        /// Directory for queued reports, create if neccessary
        /// </summary>
        public string ReportsDirectory // r/o
        {
            get => _instance.ReportsDirectory;
        }

        /// <summary>
        /// Returnes the last exception from transfer service
        /// </summary>
        public Exception LastServiceException // r/o (is r/w in previous api, should be r/o)
        {
            get => _instance.LastServiceException;
        }

        /// <summary>
        /// Submits a report to server. 
        /// If server is online, report is transmitted directly, else report is saved.
        /// </summary>
        /// <param name="method">SubmitMethod, use Online to force syncronous transfer, or Offline to force enqueing</param>
        /// <param name="report">The report to tranfer</param>
        /// <returns>Returns true if report is queued or transmitted, false if report validation failed</returns>
        /// <exception cref="System.ArgumentException">Thrown if an invalid SubmitMethod is </exception>
        /// <exception cref="Virinco.WATS.WATSException">The API is in a state that prohibites sending. Most common reason for this behavior is when the API is not registered with a server.</exception>
        public virtual bool Submit(SubmitMethod method, Report report)
            => _instance.Submit(method.CastTo<napi.SubmitMethod>(), report._baseinstance);

        /// <summary>
        /// Submits a report to server, syncrounus if online.
        /// </summary>
        /// <remarks>This method is deprecated, use Submit(SubmitMethod,Report) instead! This method will be removed in a future release.</remarks>
        /// <param name="report">The report to tranfer</param>
        /// <returns>True on successful transfer</returns>
        [Obsolete("Use the method Submit(SubmitMethod,Report) instead. This overload is provided for backwards compatibility, and will be removed in a future release.")]
        public bool SubmitOnline(Report report)
            => _instance.Submit(napi.SubmitMethod.Online, report._baseinstance);

        /// <summary>
        /// Submits a report to server. If server is online, report is transmitted directly, else report is saved.
        /// </summary>
        /// <param name="report">The report to tranfer</param>
        /// <returns>Returns true if report is queued or transmitted, false if report validation failed</returns>
        /// <exception cref="Virinco.WATS.WATSException">The API is in a state that prohibites sending. Most common reason for this behavior is when the API is not registered with a server.</exception>
        public bool Submit(Report report)
            => _instance.Submit(napi.SubmitMethod.Automatic, report._baseinstance);

        /// <summary>
        /// <para>Submits pending reports to server, syncrounously. If offline, reports are requeued.</para>
        /// <para>
        /// This method does not need to be called when the WATS Client is installed normally. The WATS Client Service calls it periodically.
        /// When the WATS Client Service is not installed this method needs to be called for pending reports to be submitted to WATS.
        /// </para>
        /// </summary>
        /// <returns>Number of reports submitted</returns>
        public int SubmitPendingReports()
            => _instance.SubmitPendingReports();

        #endregion Internal helpers and data handling

        #region Web Service helper functions

        /// <summary>
        /// Initialization mode
        /// </summary>
        public enum InitializationMode
        {
            /// <summary>Do not connect</summary>
            NoConnect,
            /// <summary>Connect syncronous</summary>
            Syncronous,
            /// <summary>Connect asyncronous</summary>
            Asyncronous,
            /// <summary>Use existing state</summary>
            UseExistingStatus
        }

        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="tryConnectToServer">If True, the API will try to go online otherwise API will be initialized in offline mode</param>
        public void InitializeAPI(bool tryConnectToServer)
            => _instance.InitializeAPI(tryConnectToServer);

        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="InitMode">Specifies how initialization should be performed</param>
        /// <param name="RegisterClient">Register client on the server</param>
        /// <param name="GetCodes">Request codes from connected server</param>
        [Obsolete("This overload is obsolete starting from version 5.0, Client must be registered using RegisterClient")]
        public void InitializeAPI(InitializationMode InitMode, bool RegisterClient, bool GetCodes)
            => _instance.InitializeAPI((napi.TDM.InitializationMode)(int)InitMode, GetCodes);

        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="InitMode">Specifies how initialization should be performed</param>
        public void InitializeAPI(InitializationMode InitMode)
            => _instance.InitializeAPI((napi.TDM.InitializationMode)(int)InitMode, true);

        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="InitMode">Specifies how initialization should be performed</param>
        /// <param name="DownloadMetadata">Download metadata from server</param>
        public void InitializeAPI(InitializationMode InitMode, bool DownloadMetadata)
            => _instance.InitializeAPI((napi.TDM.InitializationMode)(int)InitMode, DownloadMetadata);

        /// <summary>
        /// Register client using username/password with RegisterClient permission
        /// To use registration-token, set username to String.Empty and the token in password parameter
        /// Base url: for instance https://example.skywats.com/
        /// </summary>
        /// <param name="BaseUrl">WATS Server base url</param>
        /// <param name="Username">User with RegisterClient permission</param>
        /// <param name="Password">Password or registration token</param>
        /// <returns></returns>
        public void RegisterClient(string BaseUrl, string Username, string Password)
            => _instance.RegisterClient(BaseUrl, Username, Password);

        public bool HasRegisterClientConflict(string baseUrl, string username, string password)
            => _instance.HasRegisterClientConflict(baseUrl, username, password);

        /// <summary>
        /// Register and activate client using existing Target-token
        /// Base url should include /wats, for instance https://example.skywats.com/wats
        /// BaseUrl will be saved to registry if existing token allows querying Client/ServerInfo
        /// </summary>
        /// <param name="BaseUrl">WATS Server base url</param>
        public void RegisterClient(string BaseUrl)
            => _instance.RegisterClient(BaseUrl);

        /// <summary>
        /// Clear server URL and client token. Disconnects client from server.
        /// 
        /// NB! Serial number reservations from Serial Number Handler will not be canceled. 
        /// Use Virinco.WATS.Interface.MES.Production.SerialNumberHandler.CancelAllReservations() to ensure unused reserved serial numbers are freed.
        /// </summary>
        public void UnRegisterClient()
            => _instance.UnRegisterClient();

        public Version ServerVersion // r/o
        {
            get => _instance.ServerVersion;
        }

        /// <summary>
        /// Connect to configured server 
        /// </summary>
        /// <param name="UpdateMetadata">Download metadata (Processes and codes) from configured server</param>
        /// <param name="Timeout">Server connect timeout in seconds </param>
        /// <returns>Returns false if configured server could not be reached</returns>
        public bool ConnectServer(bool UpdateMetadata, TimeSpan Timeout)
            => _instance.ConnectServer(UpdateMetadata, Timeout);
        #endregion Web Service helper functions

        #region Properties
        /// <summary>
        /// Name of main sequence (root step)
        /// </summary>
        public string RootStepName // r/w
        {
            get => _instance.RootStepName;
            set => _instance.RootStepName = value;
        }


        // REMOVED Status change event from Interface-proxy -- MUST Convert to NEW WATS Client Api to use this functionality
        //public delegate void StatusChangedEventHandler(object sender, StatusChangedEventArgs e);

        //public class StatusChangedEventArgs : EventArgs
        //{
        //    public StatusChangedEventArgs(APIStatusType oldStatus, APIStatusType newStatus)
        //    {
        //        this.oldStatus = oldStatus;
        //        this.newStatus = newStatus;
        //    }
        //    public APIStatusType oldStatus;
        //    public APIStatusType newStatus;
        //}
        //public event StatusChangedEventHandler StatusChanged;


        /// <summary>
        /// Returns current API status 
        /// </summary>
        public APIStatusType Status // r/o
        {
            get => (APIStatusType)(int)_instance.Status;
        }

        /// <summary>
        /// Returns current ClientState. API must be initialized before reading this value.
        /// </summary>
        public ClientStateType ClientState // r/o
        {
            get => (ClientStateType)(int)_instance.ClientState;
        }

        // REMOVED Client State change and Config change event from Interface-proxy -- MUST Convert to NEW WATS Client Api to use this functionality
        //public delegate void ClientStateChangedEventHandler(object sender, ClientStateChangedEventArgs e);
        //public class ClientStateChangedEventArgs : EventArgs
        //{
        //    public ClientStateType oldClientState { get; set; }
        //    public ClientStateType newClientState { get; set; }
        //}
        //public event ClientStateChangedEventHandler ClientStateChanged;

        //public delegate void ConfigChangedEventHandler(object sender, ConfigChangedEventArgs e);
        //public class ConfigChangedEventArgs : EventArgs
        //{
        //}
        //public event ConfigChangedEventHandler ConfigChanged;
        #endregion Properties

        #region Exposed API

        /// <summary>
        /// Initializes API in Active Testmode
        /// </summary>
        public TDM()
        {
        }

        /// <summary>
        /// Validation mode will decide how the API will react to errors.
        /// Default value is <see cref="ValidationModeType.ThrowExceptions"/> 
        /// </summary>
        public ValidationModeType ValidationMode // r/w
        {
            get { return (ValidationModeType)(int)_instance.ValidationMode; }
            set { _instance.ValidationMode = (napi.ValidationModeType)(int)value; }
        }

        /// <summary>
        /// Sets API recording mode: Active (Default) or Import
        /// Determines if API is used to record live test data (Active) or historical processed data (Import).
        /// Checking of results and time recording are disable if mode is set to Import
        /// </summary>
        public TestModeType TestMode // r/w
        {
            get { return (TestModeType)(int)_instance.TestMode; }
            set { _instance.TestMode = (napi.TestModeType)(int)value; }
        }

        /// <summary>
        /// Creates a UUT with most common information
        /// </summary>
        /// <param name="operatorName">ATE Operator name</param>
        /// <param name="partNumber">Product part number</param>
        /// <param name="revision">Product revision number</param>
        /// <param name="serialNumber">Serial number, unique within a part number</param>
        /// <param name="operationType">Type of test</param>
        /// <param name="sequenceFileName">Name of sequence file (test program)</param>
        /// <param name="sequenceFileVersion">Version of sequence file (test program)</param>
        /// <returns>new UUT report</returns>
        public UUTReport CreateUUTReport(string operatorName, string partNumber, string revision, string serialNumber, OperationType operationType, string sequenceFileName, string sequenceFileVersion)
            => new UUTReport(_instance.CreateUUTReport(operatorName, partNumber, revision, serialNumber, operationType._instance, sequenceFileName, sequenceFileVersion));

        /// <summary>
        /// Creates a new UUT report given operation type as code
        /// </summary>
        /// <param name="operatorName"></param>
        /// <param name="partNumber"></param>
        /// <param name="revision"></param>
        /// <param name="serialNumber"></param>
        /// <param name="operationType"></param>
        /// <param name="sequenceFileName"></param>
        /// <param name="sequenceFileVersion"></param>
        /// <returns></returns>
        public UUTReport CreateUUTReport(string operatorName, string partNumber, string revision, string serialNumber, string operationType, string sequenceFileName, string sequenceFileVersion)
            => new UUTReport(_instance.CreateUUTReport(operatorName, partNumber, revision, serialNumber, operationType, sequenceFileName, sequenceFileVersion));

        /// <summary>
        /// Creates a new UUT report given operation type as a guid
        /// </summary>
        /// <param name="operatorName">Name of operator</param>
        /// <param name="partNumber">Part number</param>
        /// <param name="revision">Revision</param>
        /// <param name="serialNumber">Serial number</param>
        /// <param name="operationType">Id of operation type (Guid)</param>
        /// <param name="sequenceFileName">Sequence name</param>
        /// <param name="sequenceFileVersion">
        /// Version of Sequence 
        /// (e.g.1.0.0.1)
        /// </param>
        /// <returns></returns>
        public UUTReport CreateUUTReport(string operatorName, string partNumber, string revision, string serialNumber, Guid operationType, string sequenceFileName, string sequenceFileVersion)
            => new UUTReport(_instance.CreateUUTReport(operatorName, partNumber, revision, serialNumber, operationType, sequenceFileName, sequenceFileVersion));

        /// <summary>
        /// Creates a new Repair report 
        /// </summary>
        /// <param name="operatorName"></param>
        /// <param name="repairType"></param>
        /// <param name="uutReport"></param>
        /// <returns></returns>
        public UURReport CreateUURReport(string operatorName, RepairType repairType, UUTReport uutReport)
            => new UURReport(_instance.CreateUURReport(operatorName, repairType._instance, uutReport._instance));

        /// <summary>
        /// Creates a UUR without UUT
        /// </summary>
        /// <param name="operatorName">Name of operator</param>
        /// <param name="repairType">Use one of the repair types</param>
        /// <param name="optype"></param>
        /// <param name="serialNumber"></param>
        /// <param name="partNumber"></param>
        /// <param name="revisionNumber"></param>
        /// <returns></returns>
        public UURReport CreateUURReport(string operatorName, RepairType repairType, OperationType optype, string serialNumber, string partNumber, string revisionNumber)
            => new UURReport(_instance.CreateUURReport(operatorName, repairType._instance, optype._instance, serialNumber, partNumber, revisionNumber));

        /// <summary>
        /// Get the <see cref="YieldMonitor"/>, and use it to get test yield statistics for this client.
        /// </summary>
        public napi.Statistics.YieldMonitor GetYieldMonitorStatistics()
            => _instance.GetYieldMonitorStatistics();
        #endregion Exposed API

        /// <summary>
        /// reference to the sourcefile and conversion parameters for the current conversion operation. This property is only valid when the api is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public napi.ConversionSource ConversionSource // r/o
        {
            get => _instance.ConversionSource;
        }

        /// <summary>
        /// Called from WATS Client Service to identify the file the api is working on
        /// </summary>
        /// <param name="ConversionSourceFile">The file being in processed</param>
        /// <param name="SourceParameters">Converter's source parameters</param>
        /// <param name="DestinationParameters">Converter's destination parameters</param>
        public void SetConversionSource(FileInfo ConversionSourceFile, Dictionary<string, string> SourceParameters, Dictionary<string, string> DestinationParameters)
            => _instance.SetConversionSource(ConversionSourceFile, SourceParameters, DestinationParameters);

        /// <summary>
        /// Called from WATS Client Service when a file has been processed to clear the reference to the sourcefile and the converter.
        /// </summary>
        public void ClearConversionSource()
            => _instance.ClearConversionSource();

        /// <summary>
        /// Gets Operation types for the current connection
        /// </summary>
        /// <returns>An array of operation types</returns>
        public OperationType[] GetOperationTypes()
            => _instance.GetOperationTypes().Select(ot => new OperationType(ot)).ToArray();

        /// <summary>
        /// Get operation type given the GUID 
        /// </summary>
        /// <param name="operationTypeId"></param>
        /// <returns></returns>
        public OperationType GetOperationType(Guid operationTypeId)
            => new OperationType(_instance.GetOperationType(operationTypeId));

        /// <summary>
        /// Get operation type given the Code or Name
        /// </summary>
        /// <param name="code">Test operation code (string parsable as int) or the operation type Name </param>
        /// <returns></returns>
        public OperationType GetOperationType(string code)
            => new OperationType(_instance.GetOperationType(code));

        /// <summary>
        /// Get operation type given the Code
        /// </summary>
        /// <param name="code">Test operation code as Int16</param>
        /// <returns></returns>
        public OperationType GetOperationType(short code)
            => new OperationType(_instance.GetOperationType(code));

        /// <summary>
        /// Get repair types
        /// </summary>
        /// <returns></returns>
        public RepairType[] GetRepairTypes()
            => _instance.GetRepairTypes().Select(rt => new RepairType(rt)).ToArray();

        /// <summary>
        /// Get repair type given the GUID
        /// </summary>
        /// <param name="repairTypeId">Repair operation identifier (GUID)</param>
        /// <returns>A RepairType object</returns>
        public RepairType GetRepairType(Guid repairTypeId)
            => new RepairType(_instance.GetRepairType(repairTypeId));

        /// <summary>
        /// Returns a list of defined main failcodes in wats
        /// </summary>
        /// <param name="RepairType"></param>
        /// <returns></returns>
        public FailCode[] GetRootFailCodes(RepairType RepairType)
            => _instance.GetRootFailCodes(RepairType._instance).Select(fc => new FailCode(fc)).ToArray();

        /// <summary>
        /// Returns a list of child failcodes given a root failcode
        /// </summary>
        /// <param name="FailCode"></param>
        /// <returns></returns>
        public FailCode[] GetChildFailCodes(FailCode FailCode)
            => _instance.GetChildFailCodes(FailCode._instance).Select(fc => new FailCode(fc)).ToArray();

        /// <summary>
        /// Generates C# constants to use for operation types, failcodes given repair type
        /// </summary>
        /// <param name="repairType"></param>
        /// <returns></returns>
        public string GetCodeDeclaration(RepairType repairType)
            => _instance.GetCodeDeclaration(repairType._instance);

        /// <summary>
        /// Finds WATS reports given filter, for doc, see watsserver/swagger
        /// </summary>
        /// <param name="filter">see watsserver/swagger Report/Query</param>
        /// <param name="top">If > 0, return top first</param>
        /// <param name="orderby">Field to sort on, default is Start_UTC desc</param>
        /// <returns>Array of report headers <see cref="WatsReportHeader"/></returns>
        [Obsolete("Deprecated, use FindReportHeaders instead.")]
        public newclientapi::Virinco.WATS.Web.Api.Models.WatsReportHeader[] FindReports(string filter, int top, string orderby = "Start_UTC desc")
            => _instance.FindReports(filter, top, orderby);

        /// <summary>
        /// <para>Find WATS reports by filter, see rest API documentation on WATS server for more information (Report -> Query/Header).</para>
        /// </summary>
        /// <param name="filter">OData filter, returns reports that matches the filter.</param>
        /// <param name="top">Amount of results to return, from the top based on orderby.</param>
        /// <param name="skip">Skips results from the top, use to create paging.</param>
        /// <param name="orderby">Specifiy order of results, including ascending or descending. Use comma to order by more than one property (first order by property1, then order reports with same property1 value by property2).</param>
        /// <param name="select">Comma separated list of properties to return, the rest will be default values (null, Datetime.MinValue, Guid.Empty, 0, etc.).</param>
        /// <param name="expand">Which sub items to include, like misc info or sub units. NB! Only works for WATS 2022.2.</param>
        /// <returns></returns>
        public napi.Models.ReportHeader[] FindReportHeaders(string filter, int top, int skip = 0, string orderby = "start desc", string select = "", string expand = "")
            => _instance.FindReportHeaders(filter, top, skip, orderby, select, expand);

        /// <summary>
        /// Retrieve a spesific report from WATS Server (recursive search in server hierarchy)
        /// </summary>
        /// <param name="ReportId">Report unique identifier (GUID as string)</param>
        /// <returns>A Report object containing the requested report, or null if report was not found</returns>
        /// <exception cref="System.Exception">Service related exception may be thrown</exception>
        public Report LoadReport(string ReportId)
        {
            var napiReport = _instance.LoadReport(ReportId);
            if (napiReport is napi.UUTReport napiUUTReport)
                return new UUTReport(napiUUTReport);
            else if (napiReport is napi.UURReport napiUURReport)
                return new UURReport(napiUURReport);
            else
                return new Report(_instance.LoadReport(ReportId));
        }

        /// <summary>
        /// Statistics object containing client test statistics
        /// </summary>
        public napi.Statistics.StatisticsReader Statistics
        {
            get => _instance.Statistics;
        }

        /// <summary>
        /// Update Client info to remote server
        /// </summary>
        public void UpdateClientInfo()
            => _instance.UpdateClientInfo();

        public static XElement GetMemberMiscInfo()
            => napi.TDM.GetMemberMiscInfo();

        public void Dispose()
            => _instance.Dispose();
    }

    /*
    // ConversionSource class is not proxied in Interface.TDM - returning new-api class instead
    
    /// <summary>
    /// A class holding reference to the sourcefile and converter parameters for the current conversion operation.
    /// </summary>
    public class ConversionSource : IDisposable
    {
        public enum PostProcessAction { Move, Archive, Delete }

        public const string CompletedFolder = "Done";
        public const string ErrorFolder = "Error";

        private const string logfileextension = ".log";
        private const string errorlogfileextension = ".error";
        private const string sourceparamKeyName_EnableConversionLog = "EnableConversionLog";

        private Dictionary<string, string> _sourceparams;
        private Dictionary<string, string> _destinationparams;

        private Stream _errorlog;
        private Stream _conversionlog;

        internal ConversionSource(FileInfo ConversionSourceFile, Dictionary<string, string> SourceParameters, Dictionary<string, string> DestinationParameters, TDM apiReference)
        {
            this.SourceFile = ConversionSourceFile;
            this._destinationparams = DestinationParameters;
            this._sourceparams = SourceParameters;
        }

        /// <summary>
        /// Reference to the source file for the current conversion operation. This property is only valid when the API is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public FileInfo SourceFile { get; private set; }

        /// <summary>
        /// Uri to the source "root" folder for the current conversion operation. This property is only valid when the API is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public Uri ConversionSourceRoot {
          get => new Uri(_sourceparams["Path"]);
          set => new Uri(_sourceparams["Path"]) = value;
        }

        /// <summary>
        /// Relative uri to the source "root" folder for the current conversion operation. This property is only valid when the API is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public Uri ConversionSourceRelativePath {
          get => ConversionSourceRoot.MakeRelativeUri(new Uri(SourceFile.FullName));
          set => ConversionSourceRoot.MakeRelativeUri(new Uri(SourceFile.FullName)) = value;
        }

        /// <summary>
        /// Filter to match files to in the <see cref="ConversionSourceRoot"/> folder. The <see cref="SourceFile"/> matches this filter. This property is only valid when the API is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public string SourceFilter {
          get => _sourceparams["Filter"];
          set => _sourceparams["Filter"] = value;
        }

        /// <summary>
        /// Action for what will be done with the <see cref="SourceFile"/> after successful conversion.
        /// </summary>
        public PostProcessAction SourcePostProcessAction {
          get => (PostProcessAction)Enum.Parse(typeof(PostProcessAction), _sourceparams["PostProcessAction"]);
          set => (PostProcessAction)Enum.Parse(typeof(PostProcessAction), _sourceparams["PostProcessAction"]) = value;
        }

        public void LogException(Exception e, string message)
        {
            Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = message });
        }

        public void LogErrorMessage(string ErrorMessage)
        {
            Env.Trace.TraceData(TraceEventType.Error, 0, ErrorMessage);
        }

        /// <summary>
        /// A stream used for reporting errors during conversion operation.
        /// </summary>
        public Stream ErrorLog
        {
            get
            {
                if (object.ReferenceEquals(_errorlog, null))
                {
                    string errorlogpath = Path.Combine(SourceFile.DirectoryName, CompletedFolder + "\\" + Path.GetFileNameWithoutExtension(SourceFile.FullName) + errorlogfileextension);
                    string directorypath = Path.GetDirectoryName(errorlogpath);

                    if (!Directory.Exists(directorypath))
                        Directory.CreateDirectory(directorypath);

                    _errorlog = new FileStream(errorlogpath, FileMode.Append, FileAccess.Write, FileShare.ReadWrite);
                }

                return _errorlog;
            }
        }

        /// <summary>
        /// A stream used for reporting conversion information and progress.
        /// </summary>
        public Stream ConversionLog
        {
            get
            {
                if (object.ReferenceEquals(SourceFile, null))
                    throw new InvalidOperationException("ConversionLog is only valid during conversion initiated by WATS Client Service");

                if (_sourceparams == null || !_sourceparams.ContainsKey(sourceparamKeyName_EnableConversionLog) || string.Compare(_sourceparams[sourceparamKeyName_EnableConversionLog], "true", true) != 0)
                    return new MemoryStream();

                if (object.ReferenceEquals(_conversionlog, null))
                {
                    string conversionlogpath = Path.Combine(SourceFile.DirectoryName, CompletedFolder + "\\" + Path.GetFileNameWithoutExtension(SourceFile.FullName) + logfileextension);
                    string directorypath = Path.GetDirectoryName(conversionlogpath);

                    if (!Directory.Exists(directorypath))
                        Directory.CreateDirectory(directorypath);

                    _conversionlog = new FileStream(conversionlogpath, FileMode.Append, FileAccess.Write, FileShare.ReadWrite);
                }

                return _conversionlog;
            }
        }

        public void Dispose()
        {
            _conversionlog?.Close();
            _errorlog?.Close();
        }
    }
    */
}