using System;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;
using System.IO;
using System.Xml.Linq;
using Virinco.WATS.Schemas.WRML;
using Virinco.WATS.Interface.Models;
using System.Net;
using Newtonsoft.Json;
using System.Xml.Serialization;
using Virinco.WATS.Web.Api.Models;
using Virinco.WATS.REST;
using Virinco.WATS.Interface.Statistics;
using System.Xml;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Library toolkit to create test in WATS
    /// </summary>
    public class TDM : IDisposable
    {

        #region Internal helpers and data handling
        //
        protected internal REST.ServiceProxy proxy = new REST.ServiceProxy();
        /// <summary>
        /// Holds codes for Operation Types, Repair types etc.
        /// </summary>
        internal Processes _processes { get; set; }

        /// <summary>
        /// Local cached memberinfo (update clientinfo result)
        /// </summary>
        private ClientInfoHandler _clientinfo { get; set; }

        // Filenames for locally cached metadata

        internal const string clientUpdatesFolder = @"PublicFiles/WatsClient/";

        /// <summary>
        /// Get result from rest call to server 
        /// </summary>
        /// <param name="query"></param>
        /// <returns></returns>
        public responseType GetFromServer<responseType>(string query)
        {
            return proxy.GetXml<responseType>(query);
        }

        internal Client GetClientInfo(bool forceReload)
        {
            if (_clientinfo == null || forceReload)
            {
                //TODO: Get clientinfo from server(?)
            }
            return _clientinfo.local;
        }

        /// <summary>
        /// Target WATS Service URL
        /// Points to WATS Root address, REST Api can be found under /api, datacenter under /wats-dc, wats web application on root
        /// </summary>
        public string TargetURL
        {
            get { return proxy.TargetURL; }
        }
        /*
        private string ClientPasscode { get; set; }
        */


        //Code files and statistics files are kept on the DataDir directory
        //internal const string codesFileName = "Codes_{0}.xml";                  //Codes file name {0} = endpoint name
        //internal const string statusFileName = "Status_{0}.xml";                //Status for endpoint
        //Report files are kept on the DataDir\TDMEndpoint\Reports directory
        internal const string reportsDirectoyName = "Reports";
        const string eventSource = "WATS_API";

        private const int ReportExceptionTimeout = 60000; // Maximum milliseconst to retry ReportException (to remote server)
        internal static readonly DateTime dt1900 = new DateTime(1900, 1, 1);
        internal static readonly DateTime dt1900utc = new DateTime(1900, 1, 1, 0, 0, 0, DateTimeKind.Utc);

        /// <summary>
        /// Specifies if API should raise Exceptions after logging to EventLog
        /// </summary>
        public bool RethrowException
        {
            get { return Env.RethrowException; }
            set { Env.RethrowException = value; }
        }

        internal string SetPropertyValidated<Type>(string propertyName, string newValue, string displayName = "")
        {            
            if (displayName == "") displayName = propertyName;
            if (newValue == null)
                throw new ArgumentNullException(displayName);
            newValue = newValue.Trim();
            int maxLen = Utilities.GetMaxLengthFromAttribute<Type>(propertyName);
            if (maxLen > 0 && newValue.Length > maxLen)
            {
                if (ValidationMode == ValidationModeType.ThrowExceptions)
                    throw new ArgumentException(String.Format("Error setting property {0}\r\n Max length is {1}. Attempted length {2}", displayName, maxLen, newValue.Length), displayName);
                else
                    newValue = newValue.Substring(0, maxLen);
            }
            string cleanValue = Utilities.ReplaceInvalidXmlCharacters(newValue, "");
            if (cleanValue != newValue)
            {
                if (ValidationMode == ValidationModeType.ThrowExceptions)
                    throw new ArgumentException(String.Format("Error setting property {0}.\r\nNew value contains invalid characters", displayName), displayName);
                else
                    newValue = cleanValue;
            }
            return newValue;
        }

        /// <summary>
        /// Property to set if any Exception should be written to eventlog
        /// </summary>
        public bool LogExceptions
        {
            get { return Env.LogExceptions; }
            set { Env.LogExceptions = value; }
        }

        /// <summary>
        /// Guid identifying Station
        /// </summary>
        /// <remarks>Automatically generated and saved on workstation on first time connection</remarks>
        [Obsolete("MemberId should not be depended on. Starting from WATS Version 5.0 the client is identified by primary network adapter's MAC Address.", false)]
        public Guid MemberId
        {
            get { return Env.MemberId; }
        }

        /// <summary>
        /// Disk location for storage of pending reports
        /// </summary>
        public string DataDir
        {
            get { return Env.DataDir; }
        }


        private string stationName;
        /// <summary>
        /// Name of test machine
        /// </summary>
        public string StationName
        {
            get
            {
                if (stationName == null || stationName.Length == 0)
                    return Env.StationName;
                else
                    return stationName;
            }
            set { stationName = value; }
        }

        /// <summary>
        /// Returns list of defined processes (locally buffered)
        /// </summary>
        /// <returns></returns>
        public static List<Models.Process> GetProcesses()
        {
            var psFilepath = Path.Combine(Env.DataDir, Processes.processesFilename);
            if (!File.Exists(psFilepath)) throw new ApplicationException("No test-operation processes are defined. Connect the WATS Client to a valid server to download defined processes");
            using (var txtreader = new StreamReader(psFilepath))
            {
                var reader = new Newtonsoft.Json.JsonTextReader(txtreader);
                var serializer = new Newtonsoft.Json.JsonSerializer();
                //serializer.Converters.Add(new ProcessPropertiesConverter());
                return serializer.Deserialize<List<Models.Process>>(reader);
            }
        }

        /// <summary>
        /// Purpose of test machine
        /// </summary>
        public string Purpose
        {
            get { return Env.Purpose; }
        }

        /// <summary>
        /// Test station location
        /// </summary>
        public string Location
        {
            get { return Env.Location; }
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
        {
            //Set persist first!
            Env.PersistValues = Persist;

            Env.Location = location;
            Env.Purpose = purpose;
            Env.DataDir = !string.IsNullOrEmpty(dataDir) ? dataDir : Env.DataDir; //Will set default datadir value
        }

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
        {
            SetupAPI(dataDir, location, purpose, Persist);
        }
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
        {
            SetupAPI(dataDir, location, purpose, false);
        }

        /// <summary>
        /// Returns number of reports waiting to be sent to server, including senderror
        /// </summary>
        /// <returns></returns>
        public int GetPendingReportCount()
        {
            DirectoryInfo d = new DirectoryInfo(ReportsDirectory);
            if (d.Exists)
                return d.GetFiles().Length;
            else
                return 0;
        }

        /// <summary>
        /// Returns number of reports waiting to be sent to server, including SendError.
        /// </summary>
        /// <param name="LoadError">Returns number of reports that failed during load from disk. These reports will not be retransmitted.</param>
        /// <param name="SendError">Returns number of reports that failed during send to server. These reports will be retried every 2 hours.</param>
        /// <returns></returns>
        public int GetPendingReportCount(ref int LoadError, ref int SendError)
        {
            DirectoryInfo d = new DirectoryInfo(ReportsDirectory + @"\Error");
            LoadError = d.Exists ? d.GetFiles().Length : 0;
            d = new DirectoryInfo(ReportsDirectory);
            SendError = d.GetFiles("*.error").Length;
            return d.GetFiles().Length;
        }

        /// <summary>
        /// Directory for queued reports, create if neccessary
        /// </summary>
        public string ReportsDirectory
        {
            get
            {
                string dir = Path.Combine(DataDir, reportsDirectoyName);
                if (!Directory.Exists(dir))
                    Directory.CreateDirectory(dir);
                return dir;
            }
        }

        internal string GetReportFileName(Guid reportId, Report.ReportTransferStatusEnum status)
        {
            return Report.GetReportFileName(this, status, reportId);
        }

        /// <summary>
        /// Returnes the last exception from transfer service
        /// </summary>
        public Exception LastServiceException
        {
            get;
            set;
        }

        /// <summary>
        /// Submits a report to server, syncrounus if online
        /// </summary>
        /// <remarks>Transfer </remarks>
        /// <param name="report"></param>
        /// <returns>True on successful transfer</returns>
        private bool SubmitReport(Report report)
        {
            if (object.ReferenceEquals(report, null)) 
                return false;

            WATSReport r = report.reportRow;
            try
            {
                Env.StartLogicalTraceOperation();
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "SubmitOnline() started, ReportId:{0}", report.ReportId);
                if (report.ReportTransferStatus == Report.ReportTransferStatusEnum.InMemory)
                {
                    report.ReportTransferStatus = Report.ReportTransferStatusEnum.Queued;
                }
                Guid ReportId = new Guid(r.ID);

                var reps = new Reports();
                reps.Report.Add(r);
                var result = SubmitReports(reps).Single();
                if (result.ID != ReportId) throw new InvalidDataException("An invalid dataresponse was returned from the service, Request and Response IDs does not match.");
                report.EnsureStatisticsUpdated();
                report.DeleteFile();
                return true;  //Report transmitted
            }
            finally { Env.StopLogicalTraceOperation(); }
        }

        protected internal bool SubmitFromFile(SubmitMethod submitMethod, FileInfo file)
        {
            var reports = LoadWrml(file);
            var report = LoadReportFromWRML(reports.Report[0]);
            return Submit(submitMethod, report);
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
        {
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Submit.Validate() , Method:{0} ReportId:{1}", method.ToString(), report.ReportId.ToString());
            report.ValidateForSubmit();
            report.ValidateReport();
            report.reportRow.origin = ServiceProxy.GetMACAddress();
            bool sent = false;
            if (object.ReferenceEquals(report, null)) return false;
            switch (method)
            {
                case SubmitMethod.Offline: // Save to queue...
                    report.SaveToFile();
                    return true;
                case SubmitMethod.Online: // Required online delivery, throws exception if submit failes.
                    return SubmitReport(report);
                case SubmitMethod.Automatic: // Let API Status decide delivery method
                    // "trysend" online if api-status==Online.
                    switch (Status)
                    {
                        case APIStatusType.Online:        // "try-sbumit", save if unsuccessful...
                            try { sent = SubmitReport(report); }
                            catch (Exception ex)
                            {
                                //AbortConnection();
                                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Error submitting report to WATS" });
                                LastServiceException = ex;
                                SetStatus(APIStatusType.Offline);
                                sent = false;
                            }
                            break;
                        case APIStatusType.Offline:       // Just save it...
                        case APIStatusType.NotActivated:  // Allow saving even if the client is not activated (?) 
                        case APIStatusType.NotRegistered: // Server address is not configured, but processes.json is added manually, allow save offline
                        case APIStatusType.Error:         // API has failed, save for async delivery.
                            sent = false;
                            break;
                        case APIStatusType.Disposing:     // API not valid, throw exception!
                        case APIStatusType.NotInstalled:  // Some configuration failure has been detected, throw exception
                        case APIStatusType.Unknown:       // API not valid, throw exception!
                        default:                          // API status is not valid, throw exception!
                            throw new WATSException(new WATSLogMessage(Logging.LogSeverity.ERROR, Logging.LogCategory.Transfer, "API") { item_guid = report.ReportId, description = String.Format("Submit report is not allowed while API Status is {0}", Status) });
                    }
                    if (!sent)
                    {
                        Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Submit.SaveToFile() , Status:{0} ReportId:{1}", Status.ToString(), report.ReportId.ToString());
                        report.SaveToFile();
                    }
                    return true;
                default:
                    throw new ArgumentException("Invalid SubmitMethod", "method");
            }
        }
        /// <summary>
        /// Submits a report to server, syncrounus if online.
        /// </summary>
        /// <remarks>This method is deprecated, use Submit(SubmitMethod,Report) instead! This method will be removed in a future release.</remarks>
        /// <param name="report">The report to tranfer</param>
        /// <returns>True on successful transfer</returns>
        [Obsolete("Use the method Submit(SubmitMethod,Report) instead. This overload is provided for backwards compatibility, and will be removed in a future release.")]
        public bool SubmitOnline(Report report)
        {
            try { return Submit(SubmitMethod.Online, report); }
            catch (Exception ex)
            {
                //AbortConnection();
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Error submitting report to WATS" });
                LastServiceException = ex;
                SetStatus(APIStatusType.Offline);
                return false;
            }
        }
        /// <summary>
        /// Submits a report to server. If server is online, report is transmitted directly, else report is saved.
        /// </summary>
        /// <param name="report">The report to tranfer</param>
        /// <returns>Returns true if report is queued or transmitted, false if report validation failed</returns>
        /// <exception cref="Virinco.WATS.WATSException">The API is in a state that prohibites sending. Most common reason for this behavior is when the API is not registered with a server.</exception>
        public bool Submit(Report report)
        {
            return Submit(SubmitMethod.Automatic, report);
        }

        /// <summary>
        /// <para>Submits pending reports to server, syncrounously. If offline, reports are requeued.</para>
        /// <para>
        /// This method does not need to be called when the WATS Client is installed normally. The WATS Client Service calls it periodically.
        /// When the WATS Client Service is not installed this method needs to be called for pending reports to be submitted to WATS.
        /// </para>
        /// </summary>
        /// <returns>Number of reports submitted</returns>
        public int SubmitPendingReports()
        {
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "SubmitPendingReports() started");
            if (Status != APIStatusType.Online)
                return 0;

            int transfered = 0;
            DirectoryInfo d = new DirectoryInfo(ReportsDirectory);
            for (; ; )
            {
                var files = d.EnumerateFiles("*." + Report.ReportTransferStatusEnum.Queued.ToString()).OrderBy(file => file.CreationTime).Take(10000);
                if (Status == APIStatusType.Offline || files.Count() == 0)
                    break;

                foreach (FileInfo file in files)
                {
                    if (Status == APIStatusType.Offline)
                        break; //Stop further processing if status has changed to offline

                    Report.ReportTransferStatusEnum reportTransferStatus = Report.ReportTransferStatusEnum.Error;
                    try
                    {
                        Reports wrml;
                        try
                        {
                            wrml = this.LoadWrml(file);
                            reportTransferStatus = Report.ReportTransferStatusEnum.Transfering;
                        }
                        catch (InvalidOperationException ioe) when (
                            ioe.InnerException is XmlException ||
                            ioe.InnerException is FormatException ||
                            ioe.InnerException is InvalidCastException ||
                            ioe.InnerException is InvalidOperationException)
                        {
                            reportTransferStatus = Report.ReportTransferStatusEnum.InvalidReport;
                            throw;
                        }

                        File.SetLastAccessTime(file.FullName, DateTime.Now);
                        SetReportStatus(file, reportTransferStatus);
                       
                        bool submitok = false;
                        try
                        {
                            //foreach (var row in wrml.Report) Report.ValidateReportRow(row);
                            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "SubmitFromPending() started, ReportId:{0}", wrml.Report[0].ID);
                            var res = SubmitReports(wrml);
                            submitok = res.Count() > 0 && string.Equals(res.Single().ID.ToString(), wrml.Report[0].ID, StringComparison.OrdinalIgnoreCase);
                            if (!submitok) reportTransferStatus = Report.ReportTransferStatusEnum.Error; //Not exception but not transferred => error
                            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, $"SubmitFromPending() completed, ReportId:{wrml.Report[0].ID}, result={submitok}");
                        }
                        catch (WebException ex)
                        {
                            Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("Error submitting report [{0}] to WATS", file.Name) });
                            LastServiceException = ex;                            
                            if (ex.Response != null && ((HttpWebResponse)ex.Response).StatusCode == HttpStatusCode.BadRequest)
                                reportTransferStatus = Report.ReportTransferStatusEnum.InvalidReport;
                            else
                            {
                                if (ex.Response != null && ((HttpWebResponse)ex.Response).StatusCode == (HttpStatusCode)429) // Too many requests
                                    SetStatus(APIStatusType.Offline); //SubmitPending will exit if status is offline and try again in a bit (if run from WATS Client service)
                                else
                                    SetStatus(APIStatusType.Error);

                                reportTransferStatus = Report.ReportTransferStatusEnum.Error;
                            }
                        }
                        catch (Exception ex)
                        {
                            Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("Error submitting report [{0}] to WATS", file.Name) });
                            LastServiceException = ex;
                            reportTransferStatus = Report.ReportTransferStatusEnum.Error;
                            SetStatus(APIStatusType.Error);
                        }
                        if (submitok)
                        {
                            transfered++;
                            file.Delete();
                        }
                        else // Report validation failed, what to do ???
                        {
                            // Set as error, retransmit will retry every 5 min
                            SetReportStatus(file, reportTransferStatus);
                        }
                    }
                    catch (Exception ex)
                    {
                        SetReportStatus(file, reportTransferStatus);
                        Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("Unexpected error occured during file transfer {0}.", file.Name) });
                    }
                    
                    System.Threading.Thread.Sleep(proxy.SubmitPendingDelay);
                }
            }
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "SubmitPendingReports() completed sending {0} reports", transfered);
            return transfered;
        }

        private void SetReportStatus(FileInfo file, Report.ReportTransferStatusEnum status)
        {
            string newName = Path.Combine(file.DirectoryName, Path.GetFileNameWithoutExtension(file.Name) + "." + status.ToString());
            if (file.Exists && file.FullName != newName)
            {
                if (File.Exists(newName)) File.Delete(newName);
                file.MoveTo(newName);
            }
        }

        internal IEnumerable<Virinco.WATS.Web.Dashboard.Models.procs.ReportsWrmlUpsertResult> SubmitReports(Reports reports)
        {
            var gzipIt = Env.CompressionEnabled;
            var qry = gzipIt ? "api/Report/gzip" : "api/Report";
            HttpWebRequest rq = proxy.CreateHttpWebRequest("POST", qry, ContentType: "text/xml", Accept: "application/json", Timeout: 100000);
            using (Stream rqStream = rq.GetRequestStream())
            {
                System.Xml.Serialization.XmlSerializer ser = new System.Xml.Serialization.XmlSerializer(typeof(Reports));
                if (gzipIt)
                {
                    using (System.IO.Compression.GZipStream gs = new System.IO.Compression.GZipStream(rqStream, System.IO.Compression.CompressionMode.Compress))
                        ser.Serialize(gs, reports);
                }
                else
                {
                    ser.Serialize(rqStream, reports);
                }

            }
            using (var rs = rq.GetResponse().GetResponseStream())
            using (var tReader = new StreamReader(rs))
            {
                JsonReader jReader = new JsonTextReader(tReader);
                var conv = JsonSerializer.Create();
                var res = conv.Deserialize<Virinco.WATS.Web.Dashboard.Models.procs.ReportsWrmlUpsertResult[]>(jReader);
                jReader.Close();
                return res;
            }
        }

        /// <summary>
        /// Check connection status to server
        /// </summary>
        /// <param name="PingServer"></param>
        /// <returns></returns>
        protected bool IsConnectedToServer(bool PingServer)
        {
            try
            {
                if (PingServer)
                {
                    return Ping();
                }
                else
                {
                    var res = proxy.GetJson<ModuleVersion[]>("api/internal/Client/Version");
                    if (res.Length > 0)
                    {
                        SetStatus(APIStatusType.Online);
                        return true;
                    }
                    else return false;
                }
            }
            catch (Exception ex)
            {
                //if (LogException)
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "IsConnected failed" });
                LastServiceException = ex;
                return false;
            }

        }
        /// <summary>
        /// Save the report to transfer queue
        /// </summary>
        /// <param name="report">The report to save</param>
        internal void SaveReport(Report report)
        {
            try
            {
                report.SaveToFile();
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "SaveReport(id={0}) Success", report.ReportId);
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("Error writing Report to disk. FileName:{0}", report.ReportFileName) });
            }
        }
        #endregion Internal helpers and data handling

        #region Web Service helper functions

        private bool CheckConfiguration()
        {
            bool result = true;

            //TODO: Validate RESTApi Target location as a valid url

            if (!Directory.Exists(ReportsDirectory))
                Directory.CreateDirectory(ReportsDirectory);

            return result;
        }

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
        private struct InitializationMethod { internal InitializationMode mode; internal bool DownloadMetadata; }

        private const string settings_keyname_TargetURL = "TargetURL";
        private const string settings_keyname_ClientPasscode = "ClientPasscode";
        private const string settings_keyname_ClientState = "ClientState";

        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="tryConnectToServer">If True, the API will try to go online otherwise API will be initialized in offline mode</param>
        public void InitializeAPI(bool tryConnectToServer)
        {
            InitializeAPI(tryConnectToServer ? InitializationMode.Syncronous : InitializationMode.NoConnect, true);
        }

        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="InitMode">Specifies how initialization should be performed</param>
        /// <param name="RegisterClient">Register client on the server</param>
        /// <param name="GetCodes">Request codes from connected server</param>
        [Obsolete("This overload is obsolete starting from version 5.0, Client must be registered using RegisterClient")]
        public void InitializeAPI(InitializationMode InitMode, bool RegisterClient, bool GetCodes)
        {
            InitializeAPI(InitMode, GetCodes);
        }
        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="InitMode">Specifies how initialization should be performed</param>
        public void InitializeAPI(InitializationMode InitMode)
        {
            InitializeAPI(InitMode, true);
        }
        /// <summary>
        /// Makes the API ready for use. Check the Status property to see if API is connected to server.
        /// </summary>
        /// <param name="InitMode">Specifies how initialization should be performed</param>
        /// <param name="DownloadMetadata">Download metadata from server</param>
        public void InitializeAPI(InitializationMode InitMode, bool DownloadMetadata)
        {
            // Load settings.json file
            proxy.LoadSettings();
            try
            {
                // Verify configuration (currently just checks/creates reports folder)
                CheckConfiguration();
                // Synchronize ClientState and ClientStatus (notConfigured=>notRegistered)
                if (ClientState == ClientStateType.NotConfigured)
                {
                    SetStatus(APIStatusType.NotRegistered);

                    //If the file exists, load it so converters will work.
                    if(_processes.CanLoad())
                        _processes.Load();
                    if(_clientinfo.CanLoad())
                        _clientinfo.Load();
                }                
                else if (InitMode == InitializationMode.NoConnect || InitMode == InitializationMode.UseExistingStatus)
                {
                    if (InitMode == InitializationMode.NoConnect) SetStatus(APIStatusType.Offline); //Forced offline, will not try to connect unless ConnectServer is called explicitly.
                    // Load Codes, Processes and Memberinfo from offline cache
                    _processes.Load();
                    _clientinfo.Load();
                    if (_processes == null || _processes.processes.Count == 0)
                    {
                        ApplicationException ex = new ApplicationException("The API must be initialized online once before it can be used offline");
                        Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "InitializeAPI Error" });
                        SetStatus(APIStatusType.NotRegistered);
                        throw ex;
                    }
                }
                else // Normal (sync or async) connection
                {
                    InitializationMethod init;
                    init.mode = InitMode;
                    init.DownloadMetadata = DownloadMetadata;
                    //todo: check else if
                    if (InitMode == InitializationMode.Syncronous) ConnectServer(init);
                    else if (InitMode == InitializationMode.Asyncronous) System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(ConnectServer), init);
                }
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "Initialize API error" });
                //throw ex;
            }
        }

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
        {
            try
            {
                // Ensure minimum version - throw exception if server version is too low
                var info = proxy.GetServerInfo(BaseUrl, Username, Password);
                var serverVersion = new Version(info["Version"]);
                var minVersion = new Version(2021, 2);
                if (serverVersion < minVersion)
                    throw new WATSException($"Server version too low, minimum required version is {minVersion}, server version is {serverVersion}. Server must be upgraded to use this client version.", null);

                proxy.RegisterClient(BaseUrl, Username, Password);

                if (ClientState == ClientStateType.NotConfigured || ClientState == ClientStateType.Unknown)
                    ClientState = ClientStateType.Active;

                proxy.SaveSettings();
            }
            catch
            {
                proxy.ClearTarget();
                throw;
            }
        }

        public bool HasRegisterClientConflict(string baseUrl, string username, string password)
        {
            var selfSites = proxy.GetJsonWhenNotRegistered<Client[]>(baseUrl, username, password, "api/internal/Client/GetClients?$filter=Client_ID eq 0");
            if (selfSites.Length > 0)
            {
                string name = Env.StationName;
                string siteCode = selfSites[0].SiteCode;
                var clients = proxy.GetJsonWhenNotRegistered<Client[]>(baseUrl, username, password, $"api/internal/Client/GetClients?$filter=Name eq '{name.Replace("'", "''")}' and SiteCode eq '{siteCode.Replace("'", "''")}' and ClientType eq '{ClientType.TestStation}'");
                if (clients.Length > 0)
                {
                    var mac = ServiceProxy.GetMACAddress(false);
                    return !string.Equals(clients[0].MachineAccountId, mac, StringComparison.OrdinalIgnoreCase);
                }
            }

            return false;
        }

        internal Client GetClient(int id)
        {
            var mbrs = proxy.GetJson<Client[]>($"api/internal/Client/GetClients?$filter=Client_ID eq {id}");
            return mbrs.Length > 0 ? mbrs[0] : null;
        }

        internal Client GetClient(string name)
        {
            // return client where having same site id as self (0)
            var srv = GetClient(0);
            return GetClient(srv.SiteCode, name);
        }

        internal Client GetClient(string site, string name)
        {
            var mbrs = proxy.GetJson<Client[]>($"api/internal/Client/GetClients?$filter=Name eq '{name.Replace("'", "''")}' and SiteCode eq '{site.Replace("'", "''")}'");
            return mbrs.Length > 0 ? mbrs[0] : null;
        }

        /// <summary>
        /// Register and activate client using existing Target-token
        /// Base url should include /wats, for instance https://example.skywats.com/wats
        /// BaseUrl will be saved to registry if existing token allows querying Client/ServerInfo
        /// </summary>
        /// <param name="BaseUrl">WATS Server base url</param>
        public void RegisterClient(string BaseUrl)
        {
            var versions = proxy.RegisterClient(BaseUrl);
            // If everything works ok so far, we can rest assured existing target token is ok, and just save the specified BaseUrl to registry.
            //var key = Registry.LocalMachine.OpenSubKey(registry_keypath);
            proxy.TargetURL = BaseUrl;
            if (ClientState == ClientStateType.NotConfigured || ClientState == ClientStateType.Unknown)            
                ClientState = ClientStateType.Active;
            
            proxy.SaveSettings();
        }

        /// <summary>
        /// Clear server URL and client token. Disconnects client from server.
        /// 
        /// NB! Serial number reservations from Serial Number Handler will not be canceled. 
        /// Use Virinco.WATS.Interface.MES.Production.SerialNumberHandler.CancelAllReservations() to ensure unused reserved serial numbers are freed.
        /// </summary>
        public void UnRegisterClient()
        {
            //TODO: Send "unregister" message to server (async, short timeout to avoid re-register
            proxy.ClearTarget();
        }


        public Version ServerVersion { get; private set; }

        /// <summary>
        /// Connect to configured server 
        /// </summary>
        /// <param name="UpdateMetadata">Download metadata (Processes and codes) from configured server</param>
        /// <param name="Timeout">Server connect timeout in seconds </param>
        /// <returns>Returns false if configured server could not be reached</returns>
        public bool ConnectServer(bool UpdateMetadata, TimeSpan Timeout)
        {
            try
            {
                var res = proxy.GetJson<Dictionary<string, string>>("api/internal/Client/ServerInfo", (int)Timeout.TotalMilliseconds);
                if (res != null)
                {
                    ServerVersion = new Version(res["Version"]);
                    if (UpdateMetadata)
                    {
                        // Get Processes from server
                        _processes.Get(save: true);
                        _clientinfo.Get(save: true);
                    }
                    else
                    {
                        // Load Codes, Processes and Memberinfo from offline cache
                        _processes.Load();
                        _clientinfo.Load();
                    }
                    return true;
                }
                else
                {
                    //Support for loading default-processes offline
                    _processes.Load();
                    _clientinfo.Load();
                }
                return false;
            }
            catch (Exception ex)
            {
                //Support for loading default-processes offline
                _processes.Load();
                _clientinfo.Load();

                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "ConnectServer failed" });
                return false;
            }
        }

        /*
        /// <summary>
        /// Timeout for all server connection, defaults to 10 seconds. 
        /// </summary>
        public int ServerConnectionTimeout { get; set; } = 10;
        */
        private void ConnectServer(object sender)
        {
            try
            {
                InitializationMethod init = (InitializationMethod)sender;
                // Check if server can be reached.
                if (ConnectServer(init.DownloadMetadata, TimeSpan.FromSeconds(5)))
                    SetStatus(APIStatusType.Online);
                else
                    SetStatus(APIStatusType.Offline);
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "ConnectServer failed" });
            }

        }
        #endregion Web Service helper functions

        #region Properties


        private string mainSequenceName;
        /// <summary>
        /// Name of main sequence (root step)
        /// </summary>
        public string RootStepName
        {
            get
            {
                if (mainSequenceName == null || mainSequenceName.Length == 0)
                    return "MainSequence Callback";
                else
                    return mainSequenceName;
            }
            set
            {
                mainSequenceName = value;
            }
        }

        public delegate void StatusChangedEventHandler(object sender, StatusChangedEventArgs e);

        public class StatusChangedEventArgs : EventArgs
        {
            public StatusChangedEventArgs(APIStatusType oldStatus, APIStatusType newStatus)
            {
                this.oldStatus = oldStatus;
                this.newStatus = newStatus;
            }
            public APIStatusType oldStatus;
            public APIStatusType newStatus;
        }
        public event StatusChangedEventHandler StatusChanged;


        private static APIStatusType _status;
        /// <summary>
        /// Returns current API status 
        /// </summary>
        public APIStatusType Status
        {
            get { return _status; }
            private set { _status = value; }
        }
        private void SetStatus(APIStatusType newStatus)
        {
            if (newStatus != Status && StatusChanged != null)
            {
                var args = new StatusChangedEventArgs(Status, newStatus);
                StatusChanged(this, args);
            }
            Status = newStatus;
        }
        /// <summary>
        /// Returns current ClientState. API must be initialized before reading this value.
        /// </summary>
        public ClientStateType ClientState
        {
            get { return proxy.ClientState; }
            private set { proxy.ClientState = value; }
        }

        public delegate void ClientStateChangedEventHandler(object sender, ClientStateChangedEventArgs e);
        public class ClientStateChangedEventArgs : EventArgs
        {
            public ClientStateType oldClientState { get; set; }
            public ClientStateType newClientState { get; set; }
        }
        public event ClientStateChangedEventHandler ClientStateChanged;

        public delegate void ConfigChangedEventHandler(object sender, ConfigChangedEventArgs e);
        public class ConfigChangedEventArgs : EventArgs
        {
        }
        public event ConfigChangedEventHandler ConfigChanged;
        #endregion Properties

        #region Exposed API

        /// <summary>
        /// Initializes API in Active Testmode
        /// </summary>
        public TDM()
        {
            TestMode = TestModeType.Active;
            ValidationMode = ValidationModeType.ThrowExceptions; //Default
            _processes = new Processes(this);
            _clientinfo = new ClientInfoHandler(this);
        }

        /// <summary>
        /// Validation mode will decide how the API will react to errors.
        /// Default value is <see cref="ValidationModeType.ThrowExceptions"/> 
        /// </summary>
        public ValidationModeType ValidationMode { get; set; }


        private TestModeType testMode;
        /// <summary>
        /// Sets API recording mode: Active (Default) or Import
        /// Determines if API is used to record live test data (Active) or historical processed data (Import).
        /// Checking of results and time recording are disable if mode is set to Import
        /// </summary>
        public TestModeType TestMode
        {
            get { return testMode; }
            set { testMode = value; /*Env.PersistInfo=(testMode==TestModeType.)*/}
        }

        //public void TestLabView(CompOperatorType op)
        //{
        //    //Trace.WriteLine("TestLabView");
        //}


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
        {
            try
            {
                operatorName = operatorName ?? string.Empty;
                partNumber = partNumber ?? string.Empty;
                revision = revision ?? string.Empty;
                serialNumber = serialNumber ?? string.Empty;
                sequenceFileName = sequenceFileName ?? string.Empty;
                sequenceFileVersion = sequenceFileVersion ?? string.Empty;

                return new UUTReport(this, operatorName, sequenceFileName, sequenceFileVersion)
                {
                    PartNumber = partNumber,
                    PartRevisionNumber = revision,
                    SerialNumber = serialNumber,
                    OperationType = operationType,
                    // Set Date to "invalid". Validatereport will correct date/time with regard to current zone if only one of the date/times is set. Submit time will be used if both are invalid at submit time.
                    // Any date prior to 1970-01-01 is considered invalid.
                    StartDateTime = dt1900,
                    StartDateTimeUTC = dt1900utc
                };
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "CreateUUTReport failed." });
                throw;
            }
        }

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
        {
            //Trace.WriteLine("CreateUUTReport with operationType as string");
            return CreateUUTReport(operatorName, partNumber, revision, serialNumber, GetOperationType(operationType), sequenceFileName, sequenceFileVersion);
        }

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
        {
            //Trace.WriteLine("CreateUUTReport with operationType as Guid");
            return CreateUUTReport(operatorName, partNumber, revision, serialNumber, GetOperationType(operationType), sequenceFileName, sequenceFileVersion);
        }


        /// <summary>
        /// Creates a new Repair report 
        /// </summary>
        /// <param name="operatorName"></param>
        /// <param name="repairType"></param>
        /// <param name="uutReport"></param>
        /// <returns></returns>
        public UURReport CreateUURReport(string operatorName, RepairType repairType, UUTReport uutReport)
        {
            //Trace.WriteLine("CreateUURReport");
            if (uutReport == null)
            {
                if (repairType.UUTRequired)
                {
                    Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = new ApplicationException("This repairtype requires an UUT"), Message = "CreateUURReport" });
                }
            }
            UURReport r = new UURReport(this, repairType, uutReport, uutReport.OperationType, operatorName);
            r.SerialNumber = uutReport.SerialNumber;
            r.PartNumber = uutReport.PartNumber;
            r.PartRevisionNumber = uutReport.PartRevisionNumber;
            r.UUTGuid = uutReport.ReportId;
            r.PartInfo[0].SerialNumber = uutReport.SerialNumber;
            r.PartInfo[0].PartNumber = uutReport.PartNumber;
            r.PartInfo[0].PartRevisionNumber = uutReport.PartRevisionNumber;
            return r;
        }

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
        {
            //Trace.WriteLine("CreateUURReport");
            if (repairType.UUTRequired)
            {
                Env.Trace.TraceData(TraceEventType.Error, 0, new WATSLogItem() { ex = new ApplicationException("This repairtype requires an UUT"), Message = "CreateUURReport" });
            }
            UURReport r = new UURReport(this, repairType, null, optype, operatorName);
            r.SerialNumber = serialNumber;
            r.PartNumber = partNumber;
            r.PartRevisionNumber = revisionNumber;
            r.PartInfo[0].SerialNumber = serialNumber;
            r.PartInfo[0].PartNumber = partNumber;
            r.PartInfo[0].PartRevisionNumber = revisionNumber;
            return r;
        }

        //public UURReport CreateUURReport(string operatorName, RepairType repairType, Guid uutReportId)
        //{

        //}

        private YieldMonitor yieldMonitor;

        /// <summary>
        /// Get the <see cref="YieldMonitor"/>, and use it to get test yield statistics for this client.
        /// </summary>
        public YieldMonitor GetYieldMonitorStatistics()
        {
            if(yieldMonitor == null)
                yieldMonitor = new YieldMonitor(this);

            return yieldMonitor;
        }


        #endregion Exposed API

        /// <summary>
        /// reference to the sourcefile and conversion parameters for the current conversion operation. This property is only valid when the api is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public ConversionSource ConversionSource { get; private set; }
        /// <summary>
        /// Called from WATS Client Service to identify the file the api is working on
        /// </summary>
        /// <param name="ConversionSourceFile">The file being in processed</param>
        /// <param name="SourceParameters">Converter's source parameters</param>
        /// <param name="DestinationParameters">Converter's destination parameters</param>
        public void SetConversionSource(FileInfo ConversionSourceFile, Dictionary<string, string> SourceParameters, Dictionary<string, string> DestinationParameters)
        {
            Env.Reset(); // Resets any "volatile" values set by SetupAPI in other conversions.
            this.TestMode = TestModeType.Active; // Unless specified otherwise, use Active TestModeType
            this.ConversionSource = new ConversionSource(ConversionSourceFile, SourceParameters, DestinationParameters, this);
        }
        /// <summary>
        /// Called from WATS Client Service when a file has been processed to clear the reference to the sourcefile and the converter.
        /// </summary>
        public void ClearConversionSource()
        {
            if (!object.ReferenceEquals(this.ConversionSource, null)) this.ConversionSource.Dispose();
            this.ConversionSource = null;
        }

        /// <summary>
        /// Gets Operation types for the current connection
        /// </summary>
        /// <returns>An array of operation types</returns>
        public OperationType[] GetOperationTypes()
        {
            if (_processes == null || _processes.processes == null)
                WATSLogMessage.LogException(new ApplicationException("Processes not found, check client setup"), Logging.LogSeverity.ERROR, Logging.LogCategory.TDMInterface);
            return _processes.processes.Values.Where(p => p.IsTestOperation).Select(p => new OperationType(p)).ToArray();
        }

        /// <summary>
        /// Get operation type given the GUID 
        /// </summary>
        /// <param name="operationTypeId"></param>
        /// <returns></returns>
        public OperationType GetOperationType(Guid operationTypeId)
        {
            if (_processes == null || _processes.processes == null)
                WATSLogMessage.LogException(new ApplicationException("Processes not found, check client setup"), Logging.LogSeverity.ERROR, Logging.LogCategory.TDMInterface);
            Virinco.WATS.Interface.Models.Process process = _processes.processes.Values.FirstOrDefault(p => p.ProcessID == operationTypeId);
            if (process == null)
            {
                //Operation type not found, throw error
                ApplicationException ex = new ApplicationException(String.Format("Operation type id {0} not found", operationTypeId));
                WATSLogMessage.LogException(ex, Logging.LogSeverity.ERROR, Logging.LogCategory.TDMInterface);
                throw ex;
            }
            return new OperationType(process);// { Code = process.Code.ToString(), Description = process.Description, Name = process.Name, Id = process.GUID };
        }


        /// <summary>
        /// Get operation type given the Code or Name
        /// </summary>
        /// <param name="code">Test operation code (string parsable as int) or the operation type Name </param>
        /// <returns></returns>
        public OperationType GetOperationType(string code)
        {
            short otCode;
            if (short.TryParse(code, out otCode))
                return GetOperationType(otCode);
            else
            {
                //By name
                var process = _processes.processes.Where(p => p.Value.Name == code).SingleOrDefault().Value;
                if (process == null)
                {
                    ApplicationException ex = new ApplicationException(String.Format("Specified operation type code ({0}) is not an Int16 or name.", code));
                    WATSLogMessage.LogException(ex, Logging.LogSeverity.ERROR, Logging.LogCategory.TDMInterface);
                    throw ex;
                }
                return new OperationType(process);
            }
        }
        /// <summary>
        /// Get operation type given the Code
        /// </summary>
        /// <param name="code">Test operation code as Int16</param>
        /// <returns></returns>
        public OperationType GetOperationType(short code)
        {
            //Trace.WriteLine("Get operation type by code: " + code);
            Virinco.WATS.Interface.Models.Process process = _processes.processes.ContainsKey(code) ? _processes.processes[code] : null;
            if (process == null)
            {
                //Operation type not found, throw error
                ApplicationException ex = new ApplicationException(String.Format("Operation type code {0} not found", code));
                WATSLogMessage.LogException(ex, Logging.LogSeverity.ERROR, Logging.LogCategory.TDMInterface);
                throw ex;
            }
            return new OperationType(process);// { Code = process.Code.ToString(), Description = process.Description, Name = process.Name, Id = process.GUID };

        }

        /// <summary>
        /// Get repair types
        /// </summary>
        /// <returns></returns>
        public RepairType[] GetRepairTypes()
        {
            return _processes.processes.Values.Where(p => p.IsRepairOperation && p.State == ProcessRecordState.Active).Select(p => new RepairType(p)).ToArray();
        }

        /// <summary>
        /// Get repair type given the GUID
        /// </summary>
        /// <param name="repairTypeId">Repair operation identifier (GUID)</param>
        /// <returns>A RepairType object</returns>
        public RepairType GetRepairType(Guid repairTypeId)
        {
            //Trace.WriteLine("Get repair type: " + repairTypeId.ToString());
            foreach (RepairType r in GetRepairTypes())
            {
                if (r.Id == repairTypeId)
                    return r;
            }
            //Operation type not found, throw error
            ApplicationException ex = new ApplicationException("Error in GetRepairType");
            WATSLogMessage.LogException(ex, Logging.LogSeverity.ERROR, Logging.LogCategory.TDMInterface);
            throw ex;
        }

        /// <summary>
        /// Returns a list of defined main failcodes in wats
        /// </summary>
        /// <param name="RepairType"></param>
        /// <returns></returns>
        public FailCode[] GetRootFailCodes(RepairType RepairType)
        {
            Models.RepairType rt = _processes.processes.Values.First(p => p.ProcessID == RepairType.Id).Properties as Models.RepairType;
            return rt == null
                ? new FailCode[0]
                : rt.Categories.Select(fc => new FailCode(fc)).ToArray();
        }

        /// <summary>
        /// Returns a list of child failcodes given a root failcode
        /// </summary>
        /// <param name="FailCode"></param>
        /// <returns></returns>
        public FailCode[] GetChildFailCodes(FailCode FailCode)
        {
            //Models.RepairType rt = GetCodes(false).processes.First(p => p.GUID == RepairType.Id).Properties as Models.RepairType;
            foreach (var p in _processes.processes.Values.Where(p => p.IsRepairOperation))
            {
                Models.RepairType rt = p.Properties as Models.RepairType;
                if (rt != null)
                {
                    var cat = rt.Categories.SingleOrDefault(c => c.GUID == FailCode.Id);
                    if (cat != null) // Found, return childcodes
                    {
                        return cat.Failcodes.Select(fc => new FailCode(fc)).ToArray();
                    }
                }
            }
            // Not found, return empty array
            return new FailCode[0];
        }

        /// <summary>
        /// Generates C# constants to use for operation types, failcodes given repair type
        /// </summary>
        /// <param name="repairType"></param>
        /// <returns></returns>
        public string GetCodeDeclaration(RepairType repairType)
        {
            string declaration = "//Operation types:\r\n";
            declaration += _processes.processes.Values.Where(p => p.IsTestOperation).Select(p => String.Format(String.Format("public const string operationType_{0}=\"{1}\";\r\n", p.Name.Replace(" ", "_").Replace("-", "_"), p.Code)));
            //foreach (OperationType o in operationTypes)
            //{
            //    declaration += String.Format("public const string operationType_{0}=\"{1}\";\r\n", o.Name.Replace(" ", "_").Replace("-", "_"), o.Code);
            //}
            declaration += "\r\n//Repair type:\r\n";
            declaration += "public readonly static Guid repairType_" + repairType.Description + "=new Guid(\"{" + repairType.Id.ToString() + "}\");\r\n\r\n";
            declaration += "\r\n//Fail codes:\r\n";
            foreach (var p in _processes.processes.Values.Where(p => p.IsRepairOperation))
            {
                Models.RepairType rt = p.Properties as Models.RepairType;
                if (rt != null)
                {
                    var fcodes = rt.Categories.SelectMany(cat => cat.Failcodes.Select(fc => new { Id = fc.GUID, Category = cat.Description, Description = fc.Description }));
                    declaration += fcodes.Select(fcs => String.Format("public readonly static Guid failCode_{0}_{1}=new Guid({2});\r\n", fcs.Category.Replace(" ", "_").Replace("-", "_"), fcs.Description.Replace(" ", "_").Replace("-", "_"), "\"{" + fcs.Id.ToString() + "}\""));
                    //foreach(var cat in rt.Categories)
                    //    foreach(var fc in cat.Failcodes)
                    //        declaration += String.Format("public readonly static Guid failCode_{0}_{1}=new Guid({2});\r\n", cat.Description.Replace(" ", "_").Replace("-", "_"), fc.Description.Replace(" ", "_").Replace("-", "_"), "\"{" + fc.GUID.ToString() + "}\"");
                }

            }
            //FailCode[] rootfc = GetRootFailCodes(repairType);
            //foreach (FailCode fcparent in rootfc)
            //{
            //    FailCode[] childfc = GetChildFailCodes(fcparent);
            //    foreach (FailCode fc in childfc)
            //    {
            //        declaration +=
            //            String.Format("public readonly static Guid failCode_{0}_{1}=new Guid({2});\r\n", fcparent.Description.Replace(" ", "_").Replace("-", "_"), fc.Description.Replace(" ", "_").Replace("-", "_"), "\"{" + fc.Id.ToString() + "}\"");
            //    }
            //}
            return declaration;
        }


        /// <summary>
        /// Finds WATS reports given filter, for doc, see watsserver/swagger
        /// </summary>
        /// <param name="filter">see watsserver/swagger Report/Query</param>
        /// <param name="top">If > 0, return top first</param>
        /// <param name="orderby">Field to sort on, default is Start_UTC desc</param>
        /// <returns>Array of report headers <see cref="WatsReportHeader"/></returns>
        [Obsolete("Deprecated, use FindReportHeaders instead.")]
        public WatsReportHeader[] FindReports(string filter, int top, string orderby = "Start_UTC desc")
        {
            string query = String.Format("api/Report/Query?$orderby={0}", orderby) +
                (String.IsNullOrEmpty(filter) ? "" : String.Format("&$filter={0}", filter)) + (top <= 0 ? "" : String.Format("&$top={0}", top));
            return proxy.GetJson<WatsReportHeader[]>(query);
        }

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
        public ReportHeader[] FindReportHeaders(string filter, int top, int skip = 0, string orderby = "start desc", string select = "", string expand = "")
        {
            var @params = new List<string> { $"$top={top}" };
            if (skip > 0)
                @params.Add($"$skip={skip}");

            if (!string.IsNullOrWhiteSpace(filter))
                @params.Add($"$filter={filter}");

            if (!string.IsNullOrWhiteSpace(orderby))
                @params.Add($"$orderby={orderby}");

            if (!string.IsNullOrWhiteSpace(select))
                @params.Add($"$select={select}");

            if (!string.IsNullOrWhiteSpace(expand))
                @params.Add($"$expand={expand}");

            string query = $"api/Report/Query/Header?{string.Join("&", @params)}";
            return proxy.GetJson<ReportHeader[]>(query);
        }

        /// <summary>
        /// Retrieve a spesific report from WATS Server (recursive search in server hierarchy)
        /// </summary>
        /// <param name="ReportId">Report unique identifier (GUID as string)</param>
        /// <returns>A Report object containing the requested report, or null if report was not found</returns>
        /// <exception cref="System.Exception">Service related exception may be thrown</exception>
        public Report LoadReport(string ReportId)
        {
            var result = proxy.GetXml<Reports>(String.Format("api/Internal/Report/WRML/{0}", ReportId));
            var report = result.Report.Single();
            return LoadReportFromWRML(report);
        }

        protected internal WATSReport GetAsWRML(Report report)
        {
            return report.reportRow;
        }

        protected internal Report LoadReportFromWRML(WATSReport report)
        {
            if (report.type == ReportType.UUT)
                return new UUTReport(this, report);
            else
                return new UURReport(this, report);
        }


        /// <summary>
        /// Load a WRML Report from filesystem
        /// </summary>
        /// <param name="file">FileInfo object to WRML File</param>
        /// <returns>A Report object containing the requested report, or null if report was not found</returns>
        /// <exception cref="System.Exception">Service related exception may be thrown</exception>
        private Reports LoadWrml(FileInfo file)
        {
            var xmlReader = new XmlSerializer(typeof(Reports));
            using (var f = file.OpenRead())
            {
                return (Reports)xmlReader.Deserialize(f);
            }
        }

        private static Statistics.StatisticsReader _statistics;

        /// <summary>
        /// Statistics object containing client test statistics
        /// </summary>
        public Statistics.StatisticsReader Statistics
        {
            get { if (_statistics == null) _statistics = new Interface.Statistics.StatisticsReader(this); return _statistics; }
        }

        /// <summary>
        /// Send a lifesign signal to remote server
        /// </summary>
        /// <returns>Returns true if server response is ok</returns>
        protected bool Ping()
        {
            try
            {
                var res = proxy.GetJson<PingBack>("api/internal/Client/Ping");
                if (!string.IsNullOrEmpty(res.ServerName))
                {
                    if (res.ServerTime.HasValue && (DateTimeOffset.Now > res.ServerTime.Value.AddMinutes(5) || DateTimeOffset.Now < res.ServerTime.Value.AddMinutes(-5)))
                        Env.Trace.TraceEvent(TraceEventType.Warning, 0, "Client and server clocks are out of sync. Client time: {0}, Server time: {1}", DateTimeOffset.Now, res.ServerTime);

                    SetStatus(APIStatusType.Online);
                    return true;
                }
                else return false;
            }
            catch (Exception ex)
            {
                SetStatus(APIStatusType.Offline);
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Ping Failed, connection aborted." });
                return false;
            }
        }

        protected void PostClientLog()
        {
            try
            {
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Uploading client log.");
                string logFilePath = Env.GetConfigFilePath(Env.WatsLogFileName);
                if (File.Exists(logFilePath))
                {
                    var request = proxy.CreateHttpWebRequest("POST", $"api/internal/Blob/clientlog/{ServiceProxy.GetMACAddress()}", ContentType: "text/plain");
                    using (var fileStream = new FileStream(logFilePath, FileMode.Open, FileAccess.Read))
                    using (var requestStream = request.GetRequestStream())
                    {
                        fileStream.CopyTo(requestStream);
                        using (var response = (HttpWebResponse)request.GetResponse())
                        {
                            if (response.StatusCode == HttpStatusCode.OK)
                                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Client log successfully uploaded.");
                        }
                    }
                }
            }
            catch (Exception e)
            {
                Env.LogException(e, "Uploading client log failed.");
            }
        }

        /// <summary>
        /// Update Client info to remote server
        /// </summary>
        public void UpdateClientInfo()
        {
            try
            {
                Env.Trace.TraceEvent(TraceEventType.Verbose, 0, "Update memberinfo: start");
                var miscinfo = GetClientMiscInfo().ToString();
                _clientinfo.Put(miscinfo: miscinfo);
            }
            catch (Exception e)
            {
                Env.Trace.TraceData(TraceEventType.Warning, 0, WATSLogMessage.Create(e, Logging.LogSeverity.WARNING, Logging.LogCategory.TDMInterface, "Update memberinfo: Failed.", "tdmif"));
            }

        }

        private XElement GetClientMiscInfo()
        {
            XElement e = GetMemberMiscInfo(); //XElement.Parse(GetMemberMiscInfo().OuterXml);
            if (!InsertServiceStatus(e))
            {
                XElement pnd = e.Element("pending");
                if (pnd == null)
                {
                    pnd = new XElement("pending");
                    e.Add(pnd);
                }
                int pending = GetPendingReportCount();
                pnd.SetAttributeValue("total", pending);
                pnd.SetAttributeValue("current", pending);
                pnd.SetAttributeValue("future", 0);
                pnd.SetAttributeValue("unprocessed", 0);
            }

            XElement modules = e.Element("Modules");
            if (modules == null)
            {
                modules = new XElement("Modules");
                e.Add(modules);
            }

            SetVersion(modules, Modules.TestStation, "Test Station", System.Reflection.Assembly.GetExecutingAssembly().GetName().Version);
            SetVersion(modules, Modules.Core, "Core Module", System.Reflection.Assembly.GetAssembly(typeof(WATSReport)).GetName().Version);

            XElement computer = e.Element("computer");
            if (computer == null)
            {
                computer = new XElement("computer");
                e.Add(computer);
            }

            try
            {
                System.Management.ObjectQuery wmios = new System.Management.WqlObjectQuery("SELECT * FROM Win32_OperatingSystem");
                System.Management.ManagementObjectSearcher oss = new System.Management.ManagementObjectSearcher(wmios);

                foreach (System.Management.ManagementObject os in oss.Get())
                {

                    computer.SetElementValue("OSVersion", os["caption"]);
                    computer.SetElementValue("CSName", os["CSName"]);
                    computer.SetElementValue("CSDVersion", os["CSDVersion"]);
                    computer.SetElementValue("CountryCode", os["CountryCode"]);
                    computer.SetElementValue("OSArchitecture", os["OSArchitecture"]);
                    computer.SetElementValue("OSLanguage", os["OSLanguage"]);
                    computer.SetElementValue("Version", os["Version"]);
                    computer.SetElementValue("OSStatus", os["Status"]);
                    break;
                }
                wmios = new System.Management.WqlObjectQuery("SELECT * FROM Win32_ComputerSystem");
                oss = new System.Management.ManagementObjectSearcher(wmios);
                foreach (System.Management.ManagementObject cs in oss.Get())
                {
                    computer.SetElementValue("Caption", cs["Caption"]);
                    computer.SetElementValue("PCSystemType", cs["PCSystemType"]);
                    computer.SetElementValue("Domain", cs["Domain"]);
                    computer.SetElementValue("Manufacturer", cs["Manufacturer"]);
                    computer.SetElementValue("Model", cs["Model"]);
                    computer.SetElementValue("Name", cs["Name"]);
                    computer.SetElementValue("TotalPhysicalMemory", cs["TotalPhysicalMemory"]);
                    break;
                }
            }
            catch
            {
                Env.Trace.TraceEvent(TraceEventType.Warning, 0, "Update memberinfo: Failed to read OS and Computer info.");
                computer.SetElementValue("OSVersion", Environment.OSVersion.VersionString);
            }

            try
            {
                XElement wats = e.Element("wats");
                if (wats == null)
                {
                    wats = new XElement("wats");
                    e.Add(wats);
                }

                wats.SetAttributeValue("clientFunction", Env.ClientFunction);
                wats.SetAttributeValue("ClientLicense", Env.ClientLicense);

                XElement packages = new XElement("Packages");
                string installedPackagesXml = Env.GetConfigFilePath(Env.InstalledPackagesFileName);
                if (File.Exists(installedPackagesXml))
                {
                    XDocument doc = XDocument.Load(installedPackagesXml);
                    packages = doc.Root;
                }

                wats.Add(
                    new XElement("mes",
                        new XElement("fileDistribution",
                            new XAttribute("rootFolder", Env.MESSoftwareDistributionRoot),
                            new XAttribute("fileTransferChunkSize", Env.FileTransferChunkSize),
                            packages
                        )
                    )
                );                
            }
            catch
            {
                Env.Trace.TraceEvent(TraceEventType.Warning, 0, "Update memberinfo: Failed to read WATS info.");
            }

            try
            {
                XElement deploy = e.Element("deployment");
                if (deploy == null)
                {
                    deploy = new XElement("deployment");
                    e.Add(deploy);
                }

                XNamespace xmlns = "http://schemas.virinco.com/WATS/Wats-Client/Deployment.xsd";
                XDocument doc = XDocument.Load(Env.GetConfigFilePath(Env.DeployConfigFileName));

                var products = doc.Root.Elements(xmlns + "Product");
                foreach (var product in products)
                    AddDeploymentInfo(deploy, product, "TestStand");

                var labViews = doc.Root.Elements(xmlns + "LabView");
                foreach (var labView in labViews)
                    AddDeploymentInfo(deploy, labView, "LabView");

                void AddDeploymentInfo(XElement target, XElement source, string typeName)
                {
                    var destination = target.Elements("Product").SingleOrDefault(dp => dp.Attribute("Id") == source.Attribute("Id"));
                    if (destination != null)
                    {
                        destination.SetAttributeValue("Name", source.Attribute("Name"));
                        destination.SetAttributeValue("State", source.Attribute("State"));
                        destination.SetAttributeValue("Type", typeName);
                    }
                    else
                    {
                        target.Add(
                            new XElement("Product",
                                new XAttribute("Id", source.Attribute("Id").Value),
                                new XAttribute("Type", typeName),
                                new XAttribute("Name", source.Attribute("Name").Value),
                                new XAttribute("State", source.Attribute("State").Value)));
                    }
                }
            }
            catch (Exception ex)
            {
                Env.LogException(ex, "Update memberinfo: Failed to read integration-status.");
            }

            try
            {
                string convertersPath = Env.GetConfigFilePath(Env.ConvertersFileName);
                if (File.Exists(convertersPath))
                {
                    converters converters;
                    using (var convertersStream = File.OpenRead(convertersPath))
                        converters = (converters)new XmlSerializer(typeof(converters)).Deserialize(convertersStream);

                    var sources = e.Element("pending").Elements("converter");
                    foreach (var converter in converters.converter) 
                    {
                        var source = sources.FirstOrDefault(s => s.Attribute("name")?.Value == converter.name);
                        if(source == null)
                        {
                            source = new XElement("converter",
                                new XAttribute("name", converter.name)
                            );

                            e.Element("pending").Add(source);
                        }

                        if (source.Attribute("state") == null)
                            source.Add(new XAttribute("state", "Failed"));

                        if (converter.Source?.Parameter != null)
                            source.Add(converter.Source.Parameter.Select(p => new XAttribute(p.name, p.Value)));

                        if (converter.Destination?.Parameter != null)
                        {
                            source.Add(converter.Destination.Parameter.Select(p =>
                                new XElement("parameter",
                                    new XAttribute("name", p.name),
                                    new XAttribute("value", p.Value)
                                )
                            ));
                        }                        

                        source.Add(
                            new XAttribute("assembly", converter.assembly),
                            new XAttribute("class", converter.@class)
                        );
                    }
                }
            }
            catch(Exception ex)
            {
                Env.LogException(ex, "Update memberinfo: Failed to read converter parameters.");
            }

            return e;
        }
        public static XElement GetMemberMiscInfo()
        {
            return new XElement("miscinfo",
                new XElement("appSettings",
                    !string.IsNullOrEmpty(Env.GPSPosition) ?
                    new XElement("setting",
                        new XAttribute("key", "gpscoord"),
                        new XAttribute("value", Env.GPSPosition?.ToString())
                        ) : null
                    ),
                new XElement("Modules"),
                new XElement("computer",
                    new XElement("OSVersion", Environment.OSVersion.VersionString),
                    new XElement("CLRVersion", Environment.Version.ToString()),
                    System.IO.DriveInfo.GetDrives().Where(d => d.IsReady).Select(d => GetDriveInfoElement(d))
                    )
                );
        }

        private static XElement GetDriveInfoElement(DriveInfo drv)
        {
            string sysdrvname = null;
            try
            {
                sysdrvname = new System.IO.DirectoryInfo(System.Environment.SystemDirectory).Root.Name;
            }
            catch (Exception e)
            {
                Env.LogException(e, "Update memberinfo: Failed to find systemdrive.");
            }

            XElement el = new XElement("disk",
                new XAttribute("Name", drv.Name),
                new XAttribute("DriveType", drv.DriveType),
                new XAttribute("systemdrive", (drv.Name == sysdrvname).ToString())
                );
            try
            {
                el.Add(
                        new XAttribute("VolumeLabel", drv.VolumeLabel),
                        new XAttribute("TotalSize", drv.TotalSize.ToString()),
                        new XAttribute("AvailableFreeSpace", drv.AvailableFreeSpace.ToString()),
                        new XAttribute("TotalFreeSpace", drv.TotalFreeSpace.ToString()),
                        new XAttribute("DriveFormat", drv.DriveFormat)
                    );
            }
            catch (Exception ex)
            {
                el.Add(new XAttribute("ErrorMessage", ex.Message));
            }
            return el;
        }

        private bool InsertServiceStatus(XElement e)
        {
            //Update the install status
            GetClientUpdateUri(5000);

            string fileName = Path.Combine(DataDir, "ServiceStatus.xml");
            if (File.Exists(fileName))
            {
                try
                {
                    var status = XDocument.Load(fileName);
                    if (status.Root != null)
                    {
                        foreach (XElement el in status.Root.Elements())
                            e.Add(el);

                        return true;
                    }
                }
                catch { }
            }
            Env.Trace.TraceEvent(TraceEventType.Warning, 0, "Update memberinfo: Failed to read service status.");
            return false;
        }

        private void SetVersion(XElement modules, Modules module, Version version)
        {
            SetVersion(modules, module, module.ToString(), version);
        }

        private void SetVersion(XElement modules, Modules module, string ModuleName, Version version)
        {
            string modstring = ((int)module).ToString();
            XElement mod = modules.Elements("version").FirstOrDefault(v => v.Attribute("ModuleID")?.Value == modstring);
            if (mod == null)
            {
                mod = new XElement("version");
                mod.SetAttributeValue("ModuleID", modstring);
                modules.Add(mod);
            }
            mod.SetAttributeValue("ModuleName", ModuleName);
            mod.SetAttributeValue("Version", version);
        }

        /// <summary>
        /// This metod is obsolete in this version of the api
        /// </summary>
        /// <param name="address"></param>
        /// <returns></returns>
        [Obsolete("This metod is obsolete in this version of the api", true)]
        public static string GetEndpointIdentity(string address)
        {
            throw new NotImplementedException();
        }
        /// <summary>
        /// 
        /// </summary>
        /// <param name="timeout">Channel's OperationTimeout in milliseconds</param>
        /// <returns></returns>
        protected Uri GetClientUpdateUri(int timeout)
        {
            try
            {
                var version = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version;
                string platform = Utilities.ProcessType == Utilities.ProcessTypeEnum.w32on32 ? "x86" : "x64";
                string updateUri = proxy.GetJson<string>($"api/internal/clientupdates/link?version={version}&platform={platform}", timeout);

                if (!string.IsNullOrEmpty(updateUri))
                {
                    var oldUpdateUri = Interface.Statistics.ServiceStatus.GetInstallerUri();  
                    if (updateUri == oldUpdateUri)
                    {
                        //if update uri in different from last time, overwrite install error or download error anyway.
                        //need to store old uri somehow
                        var installStatus = Interface.Statistics.ServiceStatus.GetInstallStatus();
                        if (installStatus != Interface.Statistics.ServiceStatus.InstallStatus.InstallError && installStatus != Interface.Statistics.ServiceStatus.InstallStatus.DownloadError)
                            Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.Pending);
                    }
                    else
                    {
                        Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.Pending, updateUri);
                    }                   

                    return new Uri(updateUri);
                }
                else                
                    Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.Upgraded);                
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = "Check for updates failed." });
                Interface.Statistics.ServiceStatus.SetInstallStatus(Interface.Statistics.ServiceStatus.InstallStatus.CheckError);                
            }

            return null;
        }

        internal StatusType ReportResultToStatus(Schemas.WRML.ReportResultType result)
        {
            switch (result)
            {
                case Schemas.WRML.ReportResultType.Passed: return StatusType.Passed;
                case Schemas.WRML.ReportResultType.Failed: return StatusType.Failed;
                case Schemas.WRML.ReportResultType.Error: return StatusType.Error;
                case Schemas.WRML.ReportResultType.Terminated: return StatusType.Terminated;
                default: return StatusType.Unknown;
            }
        }

        internal OperationType GetOperationType(Process_type process_type)
        {
            return new OperationType(_processes.processes[process_type.Code]);
        }

        internal Process_type GetProcess(OperationType value)
        {
            return new Process_type()
            {
                Code = short.Parse(value.Code),
                CodeSpecified = true,
                Name = value.Name,
                Guid = value.Id.ToString()
            };
        }

        internal Models.MiscInfo GetUURMiscInfo(short ProcessCode, string MiscInfoTypeId)
        {
            int pcode = ProcessCode;
            Guid mi_guid = new Guid(MiscInfoTypeId);
            var process = _processes.processes[ProcessCode];
            var rt = process.Properties as Models.RepairType;
            return rt.MiscInfos.First(mi => mi.GUID == mi_guid);
        }

        /// <summary>
        /// Cleanup
        /// </summary>
        public void Dispose()
        {

        }
    }

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
        public Uri ConversionSourceRoot => new Uri(_sourceparams["Path"]);

        /// <summary>
        /// Relative uri to the source "root" folder for the current conversion operation. This property is only valid when the API is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public Uri ConversionSourceRelativePath => ConversionSourceRoot.MakeRelativeUri(new Uri(SourceFile.FullName));

        /// <summary>
        /// Filter to match files to in the <see cref="ConversionSourceRoot"/> folder. The <see cref="SourceFile"/> matches this filter. This property is only valid when the API is accessed in a converter activated from WATS Client Service.
        /// </summary>
        public string SourceFilter => _sourceparams["Filter"];

        /// <summary>
        /// Action for what will be done with the <see cref="SourceFile"/> after successful conversion.
        /// </summary>
        public PostProcessAction SourcePostProcessAction => (PostProcessAction)Enum.Parse(typeof(PostProcessAction), _sourceparams["PostProcessAction"]);

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
}