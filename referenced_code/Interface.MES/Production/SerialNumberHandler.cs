extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System;
using System.Collections.Generic;
using System.Linq;

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
        private napi.Production.SerialNumberHandler _instance;

        internal SerialNumberHandler(napi.Production.SerialNumberHandler instance)
        {
            _instance = instance;
        }

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
            _instance = new napi.Production.SerialNumberHandler(serialNumberTypeName);
        }

        public static IEnumerable<SerialNumberType> GetSerialNumberTypes()
            => napi.Production.SerialNumberHandler.GetSerialNumberTypes().Select(i => new SerialNumberType(i));

        public IEnumerable<SerialNumbersSN> GetLocalSerialNumbers()
            => _instance.GetLocalSerialNumbers().Select(i => new SerialNumbersSN(i));

        /// <summary>
        /// Converts from Int to MAC string
        /// </summary>
        /// <param name="i"></param>
        /// <param name="separator"></param>
        /// <returns></returns>
        public string FormatAsMAC(Int64 i, char separator)
            => _instance.FormatAsMAC(i, separator);

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
            => _instance.GenerateAndUploadSerialNumbers(tokenID, serviceUrl, fromSN, toSN, separator, out uploaded, out rejected, token);

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
            => _instance.UploadSerialNumbersFromFile(tokenID, serviceUrl, fileName, out uploaded, out rejected, token);

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
            => _instance.Initialize(tokenID, serviceUrl, (napi.Production.SerialNumberHandler.RequestType)(int)requestType, onlyInSequence, batchSize, fetchWhenLessThan, startFromSerialNumber, siteName, token);

        /// <summary>
        /// Change the behaviour of the serialnumber handler to re-use serialnumbers if referencedSN and referencedPN and number requested has been requested earlier (in the same call) 
        /// </summary>
        /// <param name="on">Turns on this functionality (default is off)</param>
        public void SetReuseOnDuplicateRequest(bool on)
            => _instance.SetReuseOnDuplicateRequest(on);

        public bool GetResuseOnDuplicateRequest()
            => _instance.GetResuseOnDuplicateRequest();

        /// <summary>
        /// Cancels any reservations that is not taken from the local store on the server.
        /// </summary>
        /// <param name="token">Deprecated. Used to be a special Guid needed to perform this function</param>
        public void CancelReservations(Guid token = new Guid())
            => _instance?.CancelReservations(token);

        /// <summary>
        /// Returns the status of a SerialnumberType
        /// </summary>
        /// <returns>Ready/NotInitialized</returns>
        public Status GetStatus()
            => (Status)(int)_instance.GetStatus();

        /// <summary>
        /// Returns the number of local serial numbers that are not taken.
        /// </summary>
        /// <returns>Free local serialnumbers</returns>
        public int GetFreeLocalSerialNumbers()
            => _instance.GetFreeLocalSerialNumbers();

        /// <summary>
        /// Returns information about the current pool when type is Reserve
        /// </summary>
        /// <param name="onlyInSequence"></param>
        /// <param name="batchSize"></param>
        /// <param name="fetchWhenLessThan"></param>
        /// <param name="startFromSerialNumber"></param>
        /// <param name="siteName"></param>
        public void GetPoolInfo(out bool onlyInSequence, out int batchSize, out int fetchWhenLessThan, out string startFromSerialNumber, out string siteName)
            => _instance.GetPoolInfo(out onlyInSequence, out batchSize, out fetchWhenLessThan, out startFromSerialNumber, out siteName);

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
            napi.Production.SerialNumberHandler.RequestType rtype;
            _instance.GetPoolInfo(out onlyInSequence, out batchSize, out fetchWhenLessThan, out startFromSerialNumber, out siteName, out rtype);
            requestType = (RequestType)(int)rtype;
        }

        /// <summary>
        /// Retrieves serialnumber from local store or server
        /// </summary>
        /// <param name="numToGet">Number of serialnumbers wanted</param>
        /// <param name="serialnumberRef">Reference to a serial number</param>
        /// <param name="partnumberRef">Reference to a part number</param>
        /// <returns>String array with serial numbers</returns>
        public string[] GetSerialNumbers(int numToGet, string serialnumberRef, string partnumberRef)
            => _instance.GetSerialNumbers(numToGet, serialnumberRef, partnumberRef);

        /// <summary>
        /// Returns one serial number, see also <see cref="GetSerialNumbers(int, string, string)"/>
        /// </summary>
        /// <param name="serialnumberRef">Associate this serial number to this serialnumber</param>
        /// <param name="partnumberRef">Associate this serial number to this partnumber</param>
        /// <returns>Serial number as string</returns>
        public string GetSerialNumber(string serialnumberRef, string partnumberRef)
            => _instance.GetSerialNumber(serialnumberRef, partnumberRef);

        /// <summary>
        /// Returns serial numbers already taken.
        /// </summary>
        /// <param name="serialnumberRef">Search for serial numbers associated with this serial number, or null to only search by reference part number.</param>
        /// <param name="partnumberRef">Search for part numbers associated with this serial number, or null to only search by reference serial number.</param>
        /// <returns>Serial numbers as array of strings</returns>
        public string[] GetTakenSerialNumbers(string serialnumberRef, string partnumberRef)
            => _instance.GetTakenSerialNumbers(serialnumberRef, partnumberRef);

        /// <summary>
        /// Converts MAC string to int
        /// </summary>
        /// <param name="mac">MAC String, supported separators are -,:,blank</param>
        /// <returns>Int64</returns>
        public Int64 MACToInt(string mac)
            => _instance.MACToInt(mac);

        /// <summary>
        /// Cancels all reservations for all types. Useful before disconnecting the client to ensure all unused reserved serial numbers are freed.
        /// </summary>
        public static void CancelAllReservations()
            => napi.Production.SerialNumberHandler.CancelAllReservations();
    }
}
