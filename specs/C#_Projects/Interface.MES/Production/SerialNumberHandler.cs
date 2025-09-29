using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml.Serialization;

namespace Virinco.WATS.Interface.MES.Production
{
    /// <summary>
    /// Interface to handle serialnumbers from WATS MES. 
    /// Written by Ragnar Engnes, Virinco as - 2016
    /// </summary>
    /// <remarks>
    /// Some methods need a special access token to use, called token (not to be confused with
    /// tokenID, which is WATS token). That access token is '1C3CFC7C-1386-4219-94F4-06D2B7FD8E18'.
    /// </remarks>
    public class SerialNumberHandler
    {
        private readonly string serialTypeName;

        private readonly MesServiceProxy serviceProxy;

        private Guid setupToken = new Guid("{1C3CFC7C-1386-4219-94F4-06D2B7FD8E18}");

        /// <summary>
        /// Serialnumber type status
        /// </summary>
        public enum Status
        {
            /// <summary>
            /// Local store ready for retrieval
            /// </summary>
            Ready,
            /// <summary>
            /// Not ready for retrieval, run Setup <see cref="Initialize(string, string, RequestType, bool, int, int, string, string, Guid)"/> first>
            /// </summary>
            NotInitialized
        }

        /// <summary>
        /// Describes how the client retrieves serial numbers from server
        /// </summary>
        public enum RequestType
        {
            /// <summary>
            /// Work in offline mode, local pool of serial numbers. Pool is reserved at server
            /// </summary>
            Reserve,
            /// <summary>
            /// Work in online mode, serialnumbers retrieved are Taken at once
            /// </summary>
            Take
        }

        /// <summary>
        /// Constructor, creates an object reference
        /// </summary>
        /// <param name="serialNumberTypeName">Type of serial number, e.g. MACAddress</param>
        public SerialNumberHandler(string serialNumberTypeName)
        {
            serialTypeName = serialNumberTypeName;

            serviceProxy = new MesServiceProxy();
            serviceProxy.LoadSettings();
        }

        public static IEnumerable<SerialNumberType> GetSerialNumberTypes()
        {
            try
            {
                var proxy = new MesServiceProxy();
                proxy.LoadSettings();

                return proxy.GetJson<IEnumerable<SerialNumberType>>("api/Production/SerialNumbers/Types");
            }
            catch(Exception e)
            {
                Env.LogException(e, "Getting serial number types failed.");
                throw;
            }
        }

        public IEnumerable<SerialNumbersSN> GetLocalSerialNumbers()
        {
            try
            {
                return ReadFile().SN.AsEnumerable();
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Getting local serial numbers from {serialTypeName} failed.");
                throw;
            }            
        }

        private static string GetFileDir()
        {
            return Env.GetConfigFilePath("AddressStore");
        }

        private string GetFileName()
        {
            return Path.Combine(GetFileDir(), $"{serialTypeName}.xml");
        }

        private string GetUncommittedFilePath()
        {
            return Path.Combine(GetFileDir(), $"{serialTypeName}.{Path.GetRandomFileName()}.uncommitted");
        }

        /// <summary>
        /// Converts from Int to MAC string
        /// </summary>
        /// <param name="i"></param>
        /// <param name="separator"></param>
        /// <returns></returns>
        public string FormatAsMAC(Int64 i, char separator)
        {
            string hex = String.Format("{0:X12}", i);
            var regex = "(.{2})(.{2})(.{2})(.{2})(.{2})(.{2})";
            var replace = "$1-$2-$3-$4-$5-$6";
            var newformat = Regex.Replace(hex, regex, replace);
            if (separator != '-') replace = replace.Replace('-', separator);
            return newformat;
        }


        private SerialNumbers GetNextSerialnumberBatch(SerialNumbers sn)
        {
            var dict = new Dictionary<string, object>();
            dict.Add("sn", sn);

            var result = serviceProxy.PostJson<Dictionary<string, string>>(sn.url, "GetAndReserveNewSerialNumbers", sn.tokenId, dict);

            var xmlSerializer = new XmlSerializer(typeof(SerialNumbers), "http://schemas.microsoft.com/2003/10/Serialization/");
            using (var reader = new StringReader(result["sn"]))
            {
                return (SerialNumbers)xmlSerializer.Deserialize(reader);
            }
        }

        /// <summary>
        /// Generates and uploads serialnumbers to server.<see cref="MACToInt(string)"/> can be used to convert a MAC string
        /// </summary>
        /// <param name="tokenID"></param>
        /// <param name="serviceUrl"></param>
        /// <param name="fromSN"></param>
        /// <param name="toSN"></param>
        /// <param name="separator">Use to format mac string</param>
        /// <param name="uploaded">Successfully uploaded</param>
        /// <param name="rejected">Already exists</param>
        /// <param name="token">Secret token from support@virinco.com</param>
        /// <returns>A list of serialnumbers that already existed</returns>
        public List<string> GenerateAndUploadSerialNumbers(string tokenID, string serviceUrl, Int64 fromSN, Int64 toSN, char separator, out int uploaded, out int rejected, Guid token)
        {
            uploaded = 0;
            rejected = 0;

            if (token != setupToken)
                return null;

            var sn = new SerialNumbers
            {
                serialNumberType = serialTypeName
            };

            try
            {
                var lsn = new List<SerialNumbersSN>();
                for (long i = fromSN; i <= toSN; i++)
                {
                    var s = new SerialNumbersSN();
                    s.id = FormatAsMAC(i, separator);
                    lsn.Add(s);
                }
                sn.SN = lsn.ToArray();

                var dict = new Dictionary<string, object>();
                dict.Add("sn", sn);

                var alreadyExist = serviceProxy.PostJson<List<string>>(serviceUrl, tokenID, "UploadSerialNumbers", dict);
                uploaded = sn.SN.Length - alreadyExist.Count;
                rejected = alreadyExist.Count;

                return alreadyExist;
            }
            catch(Exception e)
            {
                Env.LogException(e, $"Uploading new serial numbers to {serialTypeName} failed");
                throw;
            }
        }

        /// <summary>
        /// Uploads a text file with serialnumbers to the server, one sn per line - separated by CR/LF
        /// </summary>
        /// <param name="tokenID"></param>
        /// <param name="serviceUrl"></param>
        /// <param name="fileName"></param>
        /// <param name="uploaded"></param>
        /// <param name="rejected"></param>
        /// <param name="token"></param>
        /// <returns></returns>
        public List<string> UploadSerialNumbersFromFile(string tokenID, string serviceUrl, string fileName, out int uploaded, out int rejected, Guid token)
        {
            uploaded = 0; 
            rejected = 0;

            if (token != setupToken)
                return null;

            var sn = new SerialNumbers
            {
                serialNumberType = serialTypeName
            };

            try
            {
                var lsn = new List<SerialNumbersSN>();
                using (var reader = new StreamReader(fileName))
                {
                    while (!reader.EndOfStream)
                    {
                        string serial = reader.ReadLine();
                        if (!string.IsNullOrEmpty(serial))
                            lsn.Add(new SerialNumbersSN() { id = serial });
                    }
                }
                sn.SN = lsn.ToArray();

                var dict = new Dictionary<string, object>();
                dict.Add("sn", sn);

                var alreadyExist = serviceProxy.PostJson<List<string>>(serviceUrl, tokenID, "UploadSerialNumbers", dict);
                uploaded = sn.SN.Length - alreadyExist.Count;
                rejected = alreadyExist.Count;

                return alreadyExist;
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Uploading new serial numbers from {fileName} to {serialTypeName} failed.");
                throw;
            }
        }

        /// <summary>
        /// Initialize a client and make it ready for serial number retrieval.
        /// </summary>
        /// <param name="tokenID">Authentication token generated on the WATS server according to this procedure:<para/>
        /// https://virinco.zendesk.com/hc/en-us/articles/207424253-Authentication
        /// /// </param>
        /// <param name="serviceUrl">The service address, e.g.:<para/>
        /// http://localhost/SerialnumberAdmin/api/SerialNumber/
        /// </param>
        /// <param name="requestType">Legal Values <seealso cref="RequestType"/> :<para/>
        /// Take:    Client must be online and requested number of serialnumbers will be marked as Taken in the SN database<para/>
        /// Reserve: Client downloads a <paramref name="batchSize"/> number of serialnumbers and makes a reservation in the SN database.<para/>
        ///          The downloaded serial numbers are stored and maintained in an XML file on the client (C:\ProgramData\Virinco\WATS\AddressStore)<para/>
        ///          When there are <paramref name="fetchWhenLessThan"/> serialnumbers left in the local store, new serialnumbers are downloaded from server<para/>
        /// </param>
        /// <param name="onlyInSequence">If set to true, requested serialnumbers will be contiguous (NB: Only MAC addresses)</param>
        /// <param name="batchSize">How many serialnumbers that are reserved on the server (When requestType=Resvere)</param>
        /// <param name="fetchWhenLessThan">Number of remaining offline serialnumbers before server is polled for a new batch</param>
        /// <param name="startFromSerialNumber">If specified, will restrict serial numbers retrieved to be greater or equal this value</param>
        /// <param name="siteName">Deprecated. Used to be that serial numbers would be registered to the site with this name.</param>
        /// <param name="token">Deprecated. Used to be a special Guid needed to perform this function.</param>
        public void Initialize(string tokenID, string serviceUrl, RequestType requestType, bool onlyInSequence, int batchSize, int fetchWhenLessThan, string startFromSerialNumber, string siteName, Guid token = new Guid())
        {
            try
            {
                //if (token != setupToken)
                //    return;
                if (string.IsNullOrEmpty(tokenID) || string.IsNullOrEmpty(serviceUrl))
                {
                    var proxy = new MesServiceProxy();
                    proxy.LoadSettings();
                    tokenID = proxy.GetClientToken();
                    //http://localhost/wats/api/Internal/Production/
                    serviceUrl = proxy.GetTargetURL() + "api/Internal/Production/";
                }

                //Move file to .uncommitted, status will be NotInitialized
                if (GetStatus() == Status.Ready)
                {
                    var filename = GetFileName();
                    var newFilename = GetUncommittedFilePath();
                    File.Move(filename, newFilename);
                }

                var sn = new SerialNumbers
                {
                    serialNumberType = this.serialTypeName,
                    tokenId = tokenID,
                    url = serviceUrl,
                    //siteName = siteName,
                    batchSize = batchSize,
                    stationName = Environment.MachineName,
                    fetchWhenLessThan = fetchWhenLessThan,
                    fetchWhenLessThanSpecified = true,
                    fromSerialNumber = startFromSerialNumber,
                    requestType = requestType.ToString(),
                    onlyInSequence = onlyInSequence,
                    onlyInSequenceSpecified = true
                };

                //Ensure settings get saved, status is Ready
                SaveFile(sn);

                //Cancel reservations on the server
                var uncommittedSnFilePaths = Directory.EnumerateFiles(GetFileDir(), $"{serialTypeName}.*.uncommitted");
                if (uncommittedSnFilePaths.Any())
                {
                    foreach(var filePath in uncommittedSnFilePaths)
                    {
                        try
                        {
                            var uncommittedSn = ReadFile(filePath);
                            if (uncommittedSn.requestType.ToLower() == "reserve")
                            {
                                try
                                {
                                    uncommittedSn.batchSize = 0; //This signals that all resevations are cancelled and no new serialnumbers are returned
                                    GetFromServer(uncommittedSn); //Call server to update status
                                }
                                catch (Virinco.WATS.REST.HttpRequestException hre)
                                    when (hre.HttpStatusCode == System.Net.HttpStatusCode.Unauthorized)
                                {
                                    //Client might have been disconnected and reconnected, which means it has a new passcode.
                                    uncommittedSn.tokenId = tokenID;
                                    GetFromServer(uncommittedSn);
                                }
                            }

                            File.Delete(filePath);
                        }
                        catch (Exception e)
                        {
                            Env.LogException(e, $"Failed to cancel serial number reservation {Path.GetFileName(filePath)}");
                        }
                    }
                }

                //Get first batch of reserved serial numbers
                if (requestType == RequestType.Reserve)
                {
                    sn = GetFromServer(sn);
                    SaveFile(sn);
                }
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Initialize serial number handler for {serialTypeName} failed.");
                throw;
            }
        }


        /// <summary>
        /// Change the behaviour of the serialnumber handler to re-use serialnumbers if referencedSN and referencedPN and number requested has been requested earlier (in the same call) 
        /// </summary>
        /// <param name="on">Turns on this functionality (default is off)</param>
        public void SetReuseOnDuplicateRequest(bool on)
        {
            try
            {
                var sn = ReadFile();
                if (sn.reuseOnDuplicateRequestSpecified && sn.reuseOnDuplicateRequest == on)
                    return; //No change, exit
                sn.reuseOnDuplicateRequest = on;
                sn.reuseOnDuplicateRequestSpecified = true;
                SaveFile(sn);
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Set reuse serial number result on duplicate request for {serialTypeName} failed.");
                throw;
            }
        }

        public bool GetResuseOnDuplicateRequest()
        {
            SerialNumbers sn = ReadFile();
            return sn.reuseOnDuplicateRequestSpecified && sn.reuseOnDuplicateRequest;
        }

        /// <summary>
        /// Cancels any reservations that is not taken from the local store on the server.
        /// </summary>
        /// <param name="token">Deprecated. Used to be a special Guid needed to perform this function</param>
        public void CancelReservations(Guid token = new Guid())
        {
            //if (token != setupToken)
            //    return;
            if (GetStatus() == Status.NotInitialized)
                throw new ApplicationException("SerialnumberType is not initialized");

            try
            {
                SerialNumbers sn = ReadFile();
                if (sn.requestType.ToLower() == "reserve" && sn.SN != null && sn.SN.Length > 0)
                {
                    var uncommittedSnFilePath = GetUncommittedFilePath();

                    //Move file to .uncommitted, status is NotInitialized
                    File.Move(GetFileName(), uncommittedSnFilePath);

                    //Clear SNs and save, status is Ready and next GetSerialNumber will reserve new from server
                    sn.SN = new SerialNumbersSN[0];
                    SaveFile(sn);

                    //Cancel reservations on server
                    var uncommittedSn = ReadFile(uncommittedSnFilePath);
                    uncommittedSn.batchSize = 0; //This signals that all resevations are cancelled and no new serialnumbers are returned
                    GetFromServer(uncommittedSn); //Call server to update status

                    //If successful, delete uncommitted file. If failed, will try again on Initialize
                    File.Delete(uncommittedSnFilePath);
                }
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Cancel serial number reservation for {serialTypeName} failed.");
                throw;
            }
        }

        /// <summary>
        /// Returns the status of a SerialnumberType
        /// </summary>
        /// <returns>Ready/NotInitialized</returns>
        public Status GetStatus()
        {
            try
            {
                if (!Directory.Exists(GetFileDir()))
                {
                    Directory.CreateDirectory(GetFileDir());
                    return Status.NotInitialized;
                }
                if (!File.Exists(GetFileName()))
                    return Status.NotInitialized;
                return Status.Ready;
            }
            catch (Exception e)
            {
                throw new ApplicationException("Error in GetStatus", e);
            }
        }

        /// <summary>
        /// Returns the number of local serial numbers that are not taken.
        /// </summary>
        /// <returns>Free local serialnumbers</returns>
        public int GetFreeLocalSerialNumbers()
        {
            SerialNumbers sn = ReadFile();
            return sn.SN.Count(s => !s.takenSpecified);
        }

        /// <summary>
        /// Returns information about the current pool when type is Reserve
        /// </summary>
        /// <param name="onlyInSequence"></param>
        /// <param name="batchSize"></param>
        /// <param name="fetchWhenLessThan"></param>
        /// <param name="startFromSerialNumber"></param>
        /// <param name="siteName"></param>
        public void GetPoolInfo(out bool onlyInSequence, out int batchSize, out int fetchWhenLessThan, out string startFromSerialNumber, out string siteName)
        {
            SerialNumbers sn = ReadFile();
            onlyInSequence = sn.onlyInSequence;
            batchSize = sn.batchSize;
            fetchWhenLessThan = sn.fetchWhenLessThan;
            startFromSerialNumber = sn.fromSerialNumber;
            siteName = sn.siteName;
        }

        /// <summary>
        /// Returns information about the current pool when type is Reserve
        /// </summary>
        /// <param name="onlyInSequence"></param>
        /// <param name="batchSize"></param>
        /// <param name="fetchWhenLessThan"></param>
        /// <param name="startFromSerialNumber"></param>
        /// <param name="siteName"></param>
        public void GetPoolInfo(out bool onlyInSequence, out int batchSize, out int fetchWhenLessThan, out string startFromSerialNumber, out string siteName, out RequestType requestType)
        {
            SerialNumbers sn = ReadFile();
            onlyInSequence = sn.onlyInSequence;
            batchSize = sn.batchSize;
            fetchWhenLessThan = sn.fetchWhenLessThan;
            startFromSerialNumber = sn.fromSerialNumber;
            siteName = sn.siteName;
            requestType = (RequestType)Enum.Parse(typeof(RequestType), sn.requestType, true);
        }


        /// <summary>
        /// Retrieves serialnumber from local store or server
        /// </summary>
        /// <param name="numToGet">Number of serialnumbers wanted</param>
        /// <param name="serialnumberRef">Reference to a serial number</param>
        /// <param name="partnumberRef">Reference to a part number</param>
        /// <returns>String array with serial numbers</returns>
        public string[] GetSerialNumbers(int numToGet, string serialnumberRef, string partnumberRef)
        {
            if (GetStatus() != Status.Ready)
                throw new ApplicationException(string.Format("{0} is not initialized, please setup", serialTypeName));

            SerialNumbers sn = ReadFile(); //Read the local store
            if (sn.requestType.ToLower() == "take")
                return GetSerialNumbersOnline(sn, numToGet, sn.onlyInSequenceSpecified && sn.onlyInSequence, serialnumberRef, partnumberRef);
            //Type=Reserve
            if (numToGet > sn.batchSize)
                throw new ApplicationException("numToGet cannot be greater than batchsize");

            return GetSerialNumbersLocal(sn, numToGet, serialnumberRef, partnumberRef);
        }

        /// <summary>
        /// Returns one serial number, see also <see cref="GetSerialNumbers(int, string, string)"/>
        /// </summary>
        /// <param name="serialnumberRef">Associate this serial number to this serialnumber</param>
        /// <param name="partnumberRef">Associate this serial number to this partnumber</param>
        /// <returns>Serial number as string</returns>
        public string GetSerialNumber(string serialnumberRef, string partnumberRef)
        {
            string[] sn = GetSerialNumbers(1, serialnumberRef, partnumberRef);
            return sn[0];
        }

        /// <summary>
        /// Returns serial numbers already taken.
        /// </summary>
        /// <param name="serialnumberRef">Search for serial numbers associated with this serial number, or null to only search by reference part number.</param>
        /// <param name="partnumberRef">Search for part numbers associated with this serial number, or null to only search by reference serial number.</param>
        /// <returns>Serial numbers as array of strings</returns>
        public string[] GetTakenSerialNumbers(string serialnumberRef, string partnumberRef)
        {
            var parameters = new List<string>();
            parameters.Add($"serialNumberType={serialTypeName}");
            if (serialnumberRef != null)
                parameters.Add($"refSn={serialnumberRef}");
            if (partnumberRef != null)
                parameters.Add($"refPn={partnumberRef}");

            SerialNumbers sn = ReadFile(); //Read the local store
            var res = serviceProxy.GetJson<List<Dictionary<string, string>>>($"api/Production/SerialNumbers/ByReference?{string.Join("&", parameters)}", Authorization: sn.tokenId, baseAddress: sn.url.Substring(0, sn.url.Length - 24));

            return res.Select(r => r["serialNumber"]).ToArray();
        }

        private SerialNumbers GetFromServer(SerialNumbers sn)
        {
            sn = GetNextSerialnumberBatch(sn);
            if (sn.SN != null && sn.SN.Length > 0 && sn.requestType.ToLower() == "reserve" && sn.onlyInSequenceSpecified && sn.onlyInSequence)
                AddSequenceCount(sn);
            return sn;
        }

        private void AddSequenceCount(SerialNumbers sn)
        {
            if (sn.SN == null) return;
            Int64 prevSequence = 0;
            Int64 thisSequence = 0;
            int sequenceCount = 1;
            for (int i = sn.SN.Length - 1; i >= 0; i--)
            {
                thisSequence = MACToInt(sn.SN[i].id);
                if (prevSequence - thisSequence == 1)
                    sequenceCount++;
                else
                    sequenceCount = 1;
                sn.SN[i].seq = sequenceCount; sn.SN[i].seqSpecified = true;
                prevSequence = thisSequence;
            }
        }

        private string[] GetSerialNumbersOnline(SerialNumbers sn, int numberToGet, bool onlyInSequence, string connectToSerial, string connectToPartNumber)
        {
            try
            {
                sn.batchSize = numberToGet;
                sn.requestType = RequestType.Take.ToString();
                sn.refSN = connectToSerial;
                sn.refPN = connectToPartNumber;
                sn = GetFromServer(sn);

                List<string> lsn = new List<string>();
                foreach (var s in sn.SN)                
                    lsn.Add(s.id);
                
                return lsn.ToArray();
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Take serial numbers for {serialTypeName} failed.");
                throw new ApplicationException("Error in GetSerialNumbersOnline", e);
            }
        }

        /// <summary>
        /// Converts MAC string to int
        /// </summary>
        /// <param name="mac">MAC String, supported separators are -,:,blank</param>
        /// <returns>Int64</returns>
        public Int64 MACToInt(string mac)
        {
            string hexStr = mac.Replace("-", "").Replace(" ", "").Replace(":", "");
            return Convert.ToInt64(hexStr, 16);
        }

        private bool IsInSequence(SerialNumbersSN[] serials)
        {
            long first = MACToInt(serials[0].id);
            for (int i = 1; i < serials.Length; i++)
            {
                if (MACToInt(serials[i].id) - i != 1)
                    return false;
            }
            return true;
        }

        private string[] GetSerialNumbersLocal(SerialNumbers sn, int numberToGet, string connectToSerial, string connectToPartNumber)
        {
            try
            {
                int leftCount = 0;
                if (sn.SN != null)
                    leftCount = sn.SN.Count(s => !s.takenSpecified);
                if (sn.reuseOnDuplicateRequest)
                {
                    //Look if it is a duplicate request
                    SerialNumbersSN[] serialNumbersAlreadyThere = sn.SN.Where(s => s.refSN == connectToSerial && s.refPN == connectToPartNumber).ToArray();
                    if (serialNumbersAlreadyThere.Length > 0)
                    {
                        DateTime lastGenerated = serialNumbersAlreadyThere.OrderByDescending(s => s.taken).First().taken;
                        SerialNumbersSN[] serialNumbersLastGenerated = serialNumbersAlreadyThere.Where(s => Math.Abs((s.taken - lastGenerated).TotalSeconds) < 1).ToArray();
                        if (serialNumbersLastGenerated.Length == numberToGet) //If last generated (within a second) is same as requested, return same serialnumbers
                        {
                            List<string> reuseSN = new List<string>();
                            foreach (SerialNumbersSN serial in serialNumbersLastGenerated)
                            {
                                reuseSN.Add(serial.id);
                            }
                            return reuseSN.ToArray();
                        }
                    }
                }

                if (leftCount == 0) //Local store is exhausted
                {
                    sn = GetFromServer(sn); //Try to get more from server
                    leftCount = sn.SN == null ? 0 : sn.SN.Count(s => !s.takenSpecified); //Count again
                    if (leftCount == 0)
                        throw new ApplicationException("Error in GetNextSerial: No more serial numbers left");
                }
                //if (leftCount < sn.fetchWhenLessThan) ; //Give some warning?

                List<SerialNumbersSN> nextSerials;
                if (sn.onlyInSequenceSpecified && sn.onlyInSequence)
                {
                    SerialNumbersSN firstSN = sn.SN.Where(s => !s.takenSpecified && s.seq >= numberToGet).FirstOrDefault(); //Find first sn with capacity
                    if (firstSN == null)
                    {
                        //Not enough contiguous serialnumbers - get more from server
                        sn = GetFromServer(sn); //Try to get more from server
                        firstSN = sn.SN.Where(s => !s.takenSpecified && s.seq >= numberToGet).FirstOrDefault(); //Find first sn with capacity
                        if (firstSN == null)
                            throw new ApplicationException("Not enough contigous serial numbers available");
                    }
                    nextSerials = sn.SN.Where(s => string.Compare(s.id, firstSN.id) >= 0).OrderBy(s => s.id).Take(numberToGet).ToList(); //Find next available not taken
                }
                else
                {
                    nextSerials = sn.SN.Where(s => !s.takenSpecified).OrderBy(s => s.id).Take(numberToGet).ToList(); //Find next available not taken
                }

                List<string> serialList = new List<string>();
                foreach (SerialNumbersSN serial in nextSerials)
                {
                    serial.taken = DateTime.UtcNow;
                    serial.takenSpecified = true;
                    if (!string.IsNullOrEmpty(connectToSerial)) serial.refSN = connectToSerial;
                    if (!string.IsNullOrEmpty(connectToPartNumber)) serial.refPN = connectToPartNumber;
                    if (serial.seqSpecified) serial.seqSpecified = false;
                    serialList.Add(serial.id);
                }
                leftCount = sn.SN == null ? 0 : sn.SN.Count(s => !s.takenSpecified); //Count again
                if (leftCount <= sn.fetchWhenLessThan) //Limit has been reached, try get some more
                {
                    try
                    {
                        sn = GetFromServer(sn);
                    }
                    catch (Exception)
                    {
                        //Allow this to fail (client is offline), return sn until empty..
                    }
                }
                SaveFile(sn); //Save local store
                return serialList.ToArray();
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Get from reserved serial numbers for {serialTypeName} failed.");
                throw;
            }
        }



        private SerialNumbers ReadFile()
        {
            return ReadFile(GetFileName());
        }

        private SerialNumbers ReadFile(string filePath)
        {
            try
            {
                System.Xml.Serialization.XmlSerializer xs = new System.Xml.Serialization.XmlSerializer(typeof(SerialNumbers));
                using (System.Xml.XmlReader reader = System.Xml.XmlReader.Create(filePath))
                {
                    return (SerialNumbers)xs.Deserialize(reader);
                }
            }
            catch (Exception e)
            {
                throw new ApplicationException($"Error reading local serial numbers data file {filePath}", e);
            }
        }

        private void SaveFile(SerialNumbers sn)
        {
            try
            {
                System.Xml.Serialization.XmlSerializer xs = new System.Xml.Serialization.XmlSerializer(typeof(SerialNumbers));
                using (System.Xml.XmlWriter writer = System.Xml.XmlTextWriter.Create(GetFileName()))
                {
                    xs.Serialize(writer, sn);
                }
            }
            catch (Exception e)
            {
                throw new ApplicationException($"Error writing local serial numbers data file {GetFileName()}", e);
            }
        }

        /// <summary>
        /// Cancels all reservations for all types. Useful before disconnecting the client to ensure all unused reserved serial numbers are freed.
        /// </summary>
        public static void CancelAllReservations()
        {
            var dir = new DirectoryInfo(GetFileDir());
            if (dir.Exists)
            {
                var failed = new List<string>();
                foreach (var file in dir.GetFiles("*.xml"))
                {
                    try
                    {
                        var handler = new SerialNumberHandler(Path.GetFileNameWithoutExtension(file.FullName));
                        if (handler.GetStatus() == Status.Ready)
                            handler.CancelReservations();
                    }
                    catch
                    {
                        failed.Add(file.Name);
                    }
                }

                if (failed.Any())
                    throw new Exception($"Some reserved serial numbers were not canceled: {string.Join(", ", failed)}.");
            }
        }
    }
}
