using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Net.Mime;
using System.Net.NetworkInformation;
using System.Runtime.Serialization.Formatters.Binary;
using System.Runtime.Versioning;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Xml.Linq;
using System.Xml.Serialization;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Virinco.WATS.Configuration;
using Virinco.WATS.Interface;

namespace Virinco.WATS.REST
{

    /// <summary>
    /// Used to call REST services in WATS from WATS Client
    /// </summary>
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    public class ServiceProxy
    {

        private HttpClient client = null;

        /// <summary>
        /// Create and set HttpClient parameters.
        /// </summary>
        internal HttpClient CreateClient()
        {
            HttpClientHandler handler = new HttpClientHandler();

            if (webProxy != null)
            {
                handler.Proxy = webProxy;
                handler.UseProxy = true;
            }
            else if (UseSystemProxy)
            {
                handler.UseProxy = true;
            }
            else
            {
                handler.UseProxy = false; 
                //You want to set this to false so HTMLClient doesn't use resources and time looking up the system proxy. 
            }

            handler.UseCookies = false;
            var httpClient = new HttpClient(handler);
            return httpClient;
        }
        
        /// <summary>
        /// Settings file loaded from settings.json
        /// </summary>
        protected internal Configuration.ClientSettings _settings;

        /// <summary>
        /// Base URL or WATS Services
        /// </summary>
        public string TargetURL { get { return _settings.TargetURL; } set { _settings.TargetURL = value; } }
        /// <summary>
        /// Client state
        /// </summary>
        public ClientStateType ClientState { get { return _settings.ClientState; } set { _settings.ClientState = value; } }
        /// <summary>
        /// Maximum size of an attachment to WATS in bytes
        /// </summary>
        public long MaxAttachmentFileSize { get { return _settings.MaxAttachmentFileSize; } set { _settings.MaxAttachmentFileSize = value; } }

        public long MaxChartSeries { get => _settings.MaxChartSeries; set => _settings.MaxChartSeries = value; }

        public int DownloadClientUpdateTimeout => _settings.DownloadClientUpdateTimeout;

        /// <summary>
        /// Milliseconds delay between submitting reports from TDM.SubmitPendingReports()
        /// </summary>
        public int SubmitPendingDelay => _settings.SubmitPendingDelay;

        public LoggingSettings LoggingSettings => _settings.LoggingSettings;

        /// <summary>
        /// Proxy settings (web proxy) from settings.json
        /// </summary>
        public Configuration.ProxySettings ProxySettings
        {
            get { return _settings.ProxySettings; }
            set
            {
                _settings.ProxySettings = value;
                ConfigureProxy();
                SaveSettings();

                //Ensure client is always valid
                var oldClient = client;
                client = CreateClient();
                oldClient.Dispose();
            }
        }

        /// <summary>
        /// Loads client settings from local config file
        /// </summary>
#if NET8_0_OR_GREATER
        [SupportedOSPlatform("windows")]
#endif
        public void LoadSettings()
        {
            // Load settings.json:
            _settings = Configuration.ClientSettings.Load(Env.GetConfigFilePath(Env.SettingsFileName));

            ConfigureProxy();

            if (client == null)
                client = CreateClient();

            if (_settings.EncryptedClientPasscode == null && _settings.ClientPasscode != null)
            {
                if (_settings.ClientPasscode == string.Empty)
                {
                    _settings.EncryptedClientPasscode = null;
                    _settings.ClientPasscode = null;
                }
                else
                {
                    _settings.EncryptedClientPasscode = Convert.ToBase64String(ProtectedData.Protect(Encoding.UTF8.GetBytes(_settings.ClientPasscode), Encoding.UTF8.GetBytes(GetMACAddress() ?? " "), DataProtectionScope.LocalMachine));
                    _settings.ClientPasscode = null;
                }

                SaveSettings();
            }

            // verify TargetURL
            string url = "";
            if (!Uri.TryCreate(_settings.TargetURL, UriKind.Absolute, out Uri targetUri))
                _settings.ClientState = ClientStateType.NotConfigured;
            else
            {
                // Validate TargetURL as an wellformed web uri
                if (targetUri.Scheme != "http" && targetUri.Scheme != "https") throw new ArgumentException("Invalid service target url. Url must be wellformed and using either http or https protocol");

                // Ensure TargetURL ends with forward slash
                url = targetUri.ToString();
                url += (url.EndsWith("/") ? "" : "/");
            }

            // write back if different.. (TBD:Save?)
            if (url != _settings.TargetURL) _settings.TargetURL = url;

            // Check client state
            if (!Enum.IsDefined(typeof(ClientStateType), _settings.ClientState)) _settings.ClientState = ClientStateType.NotConfigured;
        }
        private WebProxy webProxy { get; set; }

        private bool UseSystemProxy;
        private void ConfigureProxy()
        {
            try
            {
                if (!object.ReferenceEquals(null, this._settings.ProxySettings) && this._settings.ProxySettings.Method == Configuration.ProxyMethodEnum.Custom)
                {
                    var pxy = new WebProxy(this._settings.ProxySettings.Address);
                    if (!string.IsNullOrEmpty(this._settings.ProxySettings.Username))
                    {
                        pxy.Credentials = new NetworkCredential(this._settings.ProxySettings.Username, this._settings.ProxySettings.Password);
                    }
                    this.webProxy = pxy;
                    UseSystemProxy = false;
                }
                else if (!object.ReferenceEquals(null, this._settings.ProxySettings) && this._settings.ProxySettings.Method == Configuration.ProxyMethodEnum.Default)
                {
                    this.webProxy = null;
                    UseSystemProxy = true;
                }
                else
                {
                    this.webProxy = null;// WebProxy.GetDefaultProxy();
                    UseSystemProxy = false;
                }
            }
            catch (Exception ex)
            {
                var e = ex;
            }
        }


        /// <summary>
        /// Saves current settings to local json file
        /// </summary>
        public void SaveSettings()
        {
            _settings.Save(Env.GetConfigFilePath(Env.SettingsFileName));
        }

        protected string GetClientToken()
        {
            if (_settings.EncryptedClientPasscode == null)
                throw new CryptographicException("Passcode is null.");

            string mac = GetMACAddress();

            if (mac == null)
                throw new CryptographicException("Registered mac address is null.");
            try
            {


                string pc = Encoding.UTF8.GetString(ProtectedData.Unprotect(Convert.FromBase64String(_settings.EncryptedClientPasscode), Encoding.UTF8.GetBytes(mac), DataProtectionScope.LocalMachine));
                return string.IsNullOrEmpty(pc) ? null : GetB64String("{0}:{1}", mac, pc.Trim('\"'));
            }
            catch (CryptographicException ce)
            {
                Env.LogException(ce, "Could not decrypt client passcode");
                return GetB64String("{0}:{1}", mac, ""); //Return invalid token, but with valid username
            }
        }

        /// <summary>
        /// REST Post request to WATS Server
        /// </summary>
        /// <typeparam name="responseType"></typeparam>
        /// <param name="query"></param>
        /// <param name="obj"></param>
        /// <param name="authorization"></param>
        /// <returns></returns>
        public responseType PostJson<responseType>(string query, object obj, string authorization = null)
        {
            return SendJson<responseType>(query, obj, "POST", authorization);
        }

        /// <summary>
        /// REST Put request to WATS Server
        /// </summary>
        /// <typeparam name="responseType"></typeparam>
        /// <param name="query"></param>
        /// <param name="obj"></param>
        /// <param name="authorization"></param>
        /// <returns></returns>
        public responseType PutJson<responseType>(string query, object obj, string authorization = null)
        {
            return SendJson<responseType>(query, obj, "PUT", authorization);
        }

        /// <summary>
        /// REST Delete request to WATS Server
        /// </summary>
        /// <typeparam name="responseType"></typeparam>
        /// <param name="query"></param>
        /// <param name="obj"></param>
        /// <param name="authorization"></param>
        /// <returns></returns>
        public responseType DeleteJson<responseType>(string query, object obj, string authorization = null)
        {
            return SendJson<responseType>(query, obj, "DELETE", authorization);
        }

        //private responseType SendJson<responseType>(string query, object obj, string method, string authorization = null)
        //{
        //    //httpclient
        //    HttpWebRequest rq = CreateHttpWebRequest(method, query, Authorization: authorization);
        //    string ser = JsonConvert.SerializeObject(obj);
        //    UTF8Encoding encoder = new UTF8Encoding();
        //    byte[] data = encoder.GetBytes(ser);
        //    rq.ContentLength = data.Length;
        //    using (Stream rqStream = rq.GetRequestStream())
        //    {
        //        rqStream.Write(data, 0, data.Length);
        //        rqStream.Flush();
        //        rqStream.Close();
        //    }
        //    var wr = rq.GetResponse();
        //    using (var rs = wr.GetResponseStream())
        //    using (var rd = new StreamReader(rs))
        //    {
        //        JsonReader jReader = new JsonTextReader(rd);
        //        var conv = JsonSerializer.Create();
        //        var res = conv.Deserialize<responseType>(jReader);
        //        jReader.Close();
        //        rd.Close();
        //        wr.Close();
        //        return res;
        //    }
        //}


        private responseType SendJson<responseType>(string query, object obj, string method,  string authorization = null)
        {
            //Set to Post since it doesn't take null.
            HttpRequestMessage request = new HttpRequestMessage();
            HttpResponseMessage response;
            
            string ser = JsonConvert.SerializeObject(obj);
            var ba = new StringContent(ser, Encoding.UTF8, "application/json");
            request.RequestUri = new Uri(TargetURL + query);
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", authorization ?? GetClientToken());
            request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));
            request.Content = ba;

            request.Headers.Add("operatorName", Env.Operator);
            request.Headers.Add("stationName", Env.StationName);

            switch (method)
            {
                case "POST":
                    request.Method = HttpMethod.Post;
                    response = client.SendAsync(request).Result;
                    break;
                case "PUT":
                    request.Method = HttpMethod.Put;
                    response = client.SendAsync(request).Result;
                    break;
                case "DELETE":
                    request.Method = HttpMethod.Delete;
                    response = client.SendAsync(request).Result;
                    break;
                default:
                    response = null;
                    break;
            }

            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException($"{(int)response.StatusCode} {response.ReasonPhrase}", response.StatusCode, response.Content);

            return JsonConvert.DeserializeObject<responseType>(response.Content.ReadAsStringAsync().Result);
        }

        public responseType GetJson<responseType>(string query, int Timeout = 10000, string Authorization = null, string baseAddress = null)
        {
            if (!string.IsNullOrEmpty(baseAddress))
                baseAddress += baseAddress.EndsWith("/") ? "" : "/";
            else
                baseAddress = TargetURL + (TargetURL.EndsWith("/") ? "" : "/");

            HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Get, baseAddress + query);
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", Authorization ?? GetClientToken());
            request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));

            request.Headers.Add("operatorName", Env.Operator);
            request.Headers.Add("stationName", Env.StationName);

            var response = client.SendAsync(request).Result;

            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException($"{(int)response.StatusCode} {response.ReasonPhrase}", response.StatusCode, response.Content);

            return JsonConvert.DeserializeObject<responseType>(response.Content.ReadAsStringAsync().Result);

        }

        protected T PostJson<T>(string baseUrl, string query, string authorization, object content)
        {
            var request = new HttpRequestMessage(HttpMethod.Post, baseUrl + query);
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", authorization);
            request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));
            request.Content = new StringContent(JsonConvert.SerializeObject(content), Encoding.UTF8, "application/json"); ;

            request.Headers.Add("operatorName", Env.Operator);
            request.Headers.Add("stationName", Env.StationName);

            var response = client.SendAsync(request).Result;

            if (!response.IsSuccessStatusCode)
                throw new Virinco.WATS.REST.HttpRequestException($"{(int)response.StatusCode} {response.ReasonPhrase}", response.StatusCode, response.Content);

            return JsonConvert.DeserializeObject<T>(response.Content.ReadAsStringAsync().Result);
        }

        //public responseType GetJson<responseType>(string query, int Timeout = 10000, string Authorization = null, string baseAddress = null)
        //{
        //    if (string.IsNullOrEmpty(Authorization))
        //    {
        //        var ct = GetClientToken();
        //        if (ct == null) return default(responseType);
        //        Authorization = String.Format("Basic {0}", ct);
        //    }
        //    using (System.Net.WebClient c = new WebClient() { BaseAddress = baseAddress ?? this.TargetURL, Encoding = Encoding.UTF8 })
        //    {
        //        if (WebProxy != null) c.Proxy = WebProxy;
        //        c.Headers[HttpRequestHeader.Accept] = "application/json";
        //        c.Headers[HttpRequestHeader.ContentType] = "application/json";
        //        c.Headers[HttpRequestHeader.Authorization] = Authorization;
        //        c.Headers[HttpRequestHeader.Referer] = c.BaseAddress;
        //        var tmp = c.DownloadString(query);
        //        var res = Newtonsoft.Json.JsonConvert.DeserializeObject<responseType>(tmp);
        //        return res;
        //    }
        //}

        //public Stream GetJsonStream(string query, int Timeout = 10000, string Authorization = null)
        //{
        //    return CreateHttpWebRequest("GET", query, Timeout, Authorization).GetResponse().GetResponseStream();
        //}

        public Stream GetJsonStream(string query, int Timeout = 10000, string Authorization = null)
        {
            return JsonStream(query, Timeout, Authorization);
        }

        public Stream JsonStream(string query, int Timeout = 10000, string ContentType = "application/json", string Accept = "application/json", long ContentLength = -1, string Authorization = null)
        {
            string baseAddress = TargetURL + (TargetURL.EndsWith("/") ? "" : "/");

            var request = new HttpRequestMessage(HttpMethod.Get, baseAddress + query);
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", Authorization ?? GetClientToken());
            request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue(Accept));

            request.Headers.Add("operatorName", Env.Operator);
            request.Headers.Add("stationName", Env.StationName);

            var response = client.SendAsync(request).Result;

            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException($"{(int)response.StatusCode} {response.ReasonPhrase}", response.StatusCode, response.Content);

            return response.Content.ReadAsStreamAsync().Result;
        }

        public HttpWebRequest CreateHttpWebRequest(string Method, string query, int Timeout = 10000, string ContentType = "application/json", string Accept = "application/json", long ContentLength = -1, string Authorization = null)
        {
            string fullurl = this.TargetURL + (this.TargetURL.EndsWith("/") ? "" : "/") + query;
            HttpWebRequest rq = (HttpWebRequest)WebRequest.Create(fullurl);

            rq.Method = Method;
            rq.ContentType = ContentType;
            rq.Accept = Accept;
            rq.Headers["Authorization"] = String.Format("Basic {0}", Authorization ?? GetClientToken());
            rq.Timeout = Timeout;

            if (webProxy != null) 
                rq.Proxy = webProxy;

            if (ContentLength > -1)
                rq.ContentLength = ContentLength;


            rq.Headers.Add("operatorName", Env.Operator);
            rq.Headers.Add("stationName", Env.StationName);

            return rq;
        }


        static private string _mac;

        /// <summary>
        /// Return PhysicalAddress (MAC Address) of first physical network interface
        /// If validateOnly is true (default), this function verifies that the registered mac address is valid on this machine.
        /// If validateOnly is false this function will search for a valid address (registered or unregistered)
        /// </summary>
        /// <param name="validateOnly">Validate registered address only</param>
        /// <returns></returns>
        static public string GetMACAddress(bool validateOnly = true, bool rememberResult = true)
        {
            string mac = validateOnly ? _mac : null;
            if (mac == null || !rememberResult)
            {
                var identifierType = Env.IdentifierType;
                if (identifierType == ClientIdentifierType.MacAddress)
                {
                    string lastUsedMAC = Env.MACAddressRegistered;
                    var iface = NetworkInterface.GetAllNetworkInterfaces().Where(nic => nic.GetPhysicalAddress().ToString() == lastUsedMAC).FirstOrDefault();
                    if (iface == null)
                        lastUsedMAC = null;
                    else
                        mac = iface.GetPhysicalAddress().ToString();

                    if (String.IsNullOrEmpty(lastUsedMAC) && !validateOnly) //First time asking for MAC, search for one
                    {
                        // Get first (by IPv4's index) wireless interface with mac address and gateway address (exclude Loopback & Tunnels) 
                        iface = NetworkInterface.GetAllNetworkInterfaces()
                        .Where(nic => nic.NetworkInterfaceType == NetworkInterfaceType.Wireless80211 &&
                                nic.GetPhysicalAddress() != null && nic.GetIPProperties() != null &&
                                (nic.GetIPProperties().GatewayAddresses.Count > 0 && nic.GetIPProperties().GatewayAddresses.First()?.Address?.ToString() != "0.0.0.0"))
                        .OrderBy(nic => nic.GetIPProperties().GetIPv4Properties().Index).FirstOrDefault();

                        if (iface == null)
                        {
                            // Get first (by IPv4's index) ethernet interface with mac address and gateway address (exclude Loopback & Tunnels) 
                            iface = NetworkInterface.GetAllNetworkInterfaces()
                            .Where(nic => nic.NetworkInterfaceType == NetworkInterfaceType.Ethernet &&
                                    nic.OperationalStatus == OperationalStatus.Up &&
                                    nic.GetPhysicalAddress() != null && nic.GetIPProperties() != null &&
                                    (nic.GetIPProperties().GatewayAddresses.Count > 0 && nic.GetIPProperties().GatewayAddresses.First()?.Address?.ToString() != "0.0.0.0"))
                            .OrderBy(nic => nic.GetIPProperties().GetIPv4Properties().Index).FirstOrDefault();
                        }

                        // Get first (by IPv4's index) interface with mac address and gateway address (exclude Loopback & Tunnels) 
                        if (iface == null)
                        {
                            // No interface found with gateway address, expand search to include non-gw interfaces (might return virtual host interfaces - VMWare etc)
                            iface = NetworkInterface.GetAllNetworkInterfaces()
                                .Where(nic => nic.NetworkInterfaceType != NetworkInterfaceType.Tunnel &&
                                nic.NetworkInterfaceType != NetworkInterfaceType.Loopback &&
                                nic.GetPhysicalAddress() != null && nic.GetIPProperties() != null)
                                .OrderBy(nic => nic.GetIPProperties().GetIPv4Properties().Index).First();
                        }

                        if (iface == null)
                            throw new ApplicationException("No MAC address found");

                        mac = iface.GetPhysicalAddress().ToString();
                    }
                }
                else
                {
                    mac = Env.MACAddressRegistered;
                }

                if (rememberResult)
                    _mac = mac;
            }

            return mac;
        }

        public static string GetCurrentMACAddress()
        {
            try
            {
                var mac = GetMACAddress(false, false);
                if (Env.IdentifierType == ClientIdentifierType.MacAddress)
                    return string.Join(":", Enumerable.Range(0, 6).Select(i => mac.Substring(i * 2, 2)));
                else
                    return mac;
            }
            catch
            {
                return null;
            }
        }

        public string GetB64String(string Format, params object[] args)
        {
            string sUserPass = String.Format(Format, args);
            byte[] bUserPass = ASCIIEncoding.ASCII.GetBytes(sUserPass);
            string sToken = Convert.ToBase64String(bUserPass);
            return sToken;
        }

        public void RegisterClient(string BaseUrl, string Username, string Password)
        {
            if (client == null)
                client = CreateClient();

            BaseUrl += BaseUrl.EndsWith("/") ? "" : "/"; // Ensure ending slash exists

            var mac = GetMACAddress(false);
            if (string.IsNullOrWhiteSpace(mac))
            {
                string message;
                switch (Env.IdentifierType)
                {
                    default:
                    case ClientIdentifierType.MacAddress:
                        message = "No network card found. The client needs to bind to a network card with a fixed mac address.";
                        break;
                    case ClientIdentifierType.Custom:
                        message = "No custom identifier specified. The client needs a unique identifier, for example a randomly generated UUID.";
                        break;
                }

                throw new Exception(message);
            }

            string fullurl = $"{BaseUrl}api/internal/Client/Register?mac={mac}&name={Env.StationName}&location={Env.Location}&purpose={Env.Purpose}&utcOffset={new decimal(DateTimeOffset.Now.Offset.TotalHours)}&version={System.Reflection.Assembly.GetExecutingAssembly().GetName().Version}";

            // Use password as token if UserName is blank or whitespace
            string tmpToken = string.IsNullOrWhiteSpace(Username) ? Password : GetB64String("{0}:{1}", Username, Password);

            HttpRequestMessage request = new HttpRequestMessage();
            //var request = (HttpWebRequest)WebRequest.Create(fullurl);
            //if (webProxy != null)
            //    request.Proxy = webProxy;
            
            request.Method = HttpMethod.Post;
            request.RequestUri = new Uri(fullurl);
            //request.ContentType = "application/json";
            request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("application/json"));
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", tmpToken ?? GetClientToken());
            //request.ContentLength = 0;

            string newPasscode;
            var response = client.SendAsync(request).Result;

            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException($"{(int)response.StatusCode} {response.ReasonPhrase}", response.StatusCode, response.Content);

            var responseStream = response.Content.ReadAsStreamAsync().Result;
            using (var responseReader = new StreamReader(responseStream))
                newPasscode = responseReader.ReadToEnd().Trim('\"');

            // test connection with newPassCode
            GetServerInfo(BaseUrl, mac, newPasscode);

            // Save Target BaseURL and Passcode to settings.json
            if (_settings == null)
                _settings = new Configuration.ClientSettings();
            _settings.TargetURL = BaseUrl;

            _settings.EncryptedClientPasscode = Convert.ToBase64String(ProtectedData.Protect(Encoding.UTF8.GetBytes(newPasscode), Encoding.UTF8.GetBytes(mac), DataProtectionScope.LocalMachine));
            _settings.ClientPasscode = null;

            Env.MACAddressRegistered = mac;
        }

        //public Dictionary<string, string> RegisterClient(string BaseUrl)
        //{
        //    string fullurl = BaseUrl + (BaseUrl.EndsWith("/") ? "" : "/") + "api/internal/Client/ServerInfo";
        //    var rq = CreateHttpWebRequest("GET", "api/internal/Client/ServerInfo", Timeout: 2000);
        //    using (var rs = rq.GetResponse().GetResponseStream())
        //    {
        //        var tReader = new StreamReader(rs);
        //        JsonReader jReader = new JsonTextReader(tReader);
        //        var ser = JsonSerializer.Create();
        //        var res = ser.Deserialize<Dictionary<string, string>>(jReader);
        //        jReader.Close();
        //        return res;
        //    }
        //}

        public Dictionary<string, string> RegisterClient(string BaseUrl)
        {
            using (var s = GetJsonStream("api/internal/Client/ServerInfo"))
            {
                var tReader = new StreamReader(s);
                JsonReader jReader = new JsonTextReader(tReader);
                var ser = JsonSerializer.Create();
                var res = ser.Deserialize<Dictionary<string, string>>(jReader);
                jReader.Close();
                return res;
            }
        }

        public Dictionary<string, string> GetServerInfo(string baseUrl, string username, string password)
        {
            return GetJsonWhenNotRegistered<Dictionary<string, string>>(baseUrl, username, password, "api/internal/Client/ServerInfo");            
        }

        public T GetJsonWhenNotRegistered<T>(string baseUrl, string username, string password, string query)
        {
            if (client == null)
                client = CreateClient();

            string token = string.IsNullOrWhiteSpace(username) ? password : GetB64String("{0}:{1}", username, password);
            return GetJson<T>(query, baseAddress: baseUrl, Authorization: token);
        }

        public responseType PostXML<responseType>(string query, string xmlData, int Timeout = 10000, string Authorization = null, bool rethrowException = false)
        {
            
            string fullurl = TargetURL + (TargetURL.EndsWith("/") ? "" : "/");
            HttpRequestMessage request = new HttpRequestMessage();
            HttpResponseMessage response;
            
            StringContent content = new StringContent(xmlData, Encoding.UTF8, "text/xml");

            request.Headers.Clear();
            request.Method = HttpMethod.Post;
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", Authorization ?? GetClientToken());
            request.RequestUri = new Uri(fullurl + query);
            //request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("text/xml"));
            request.Content = content;
            
            response = client.SendAsync(request).Result;

            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException($"{(int)response.StatusCode} {response.ReasonPhrase}", response.StatusCode, response.Content);

            return JsonConvert.DeserializeObject<responseType>(response.Content.ReadAsStringAsync().Result);
        }

        //public responseType PostXML<responseType>(string query, string xmlData, int Timeout = 10000, string Authorization = null, bool rethrowException = false)
        //{
        //    var rq = CreateHttpWebRequest("POST", query, ContentType: "text/xml", Accept: "application/json", Timeout: Timeout, Authorization: Authorization);
        //    byte[] data = Encoding.ASCII.GetBytes(xmlData);
        //    rq.ContentLength = data.Length;
        //    using (Stream rqStream = rq.GetRequestStream())
        //    {
        //        rqStream.Write(data, 0, data.Length);
        //        rqStream.Flush();
        //        rqStream.Close();
        //    }
        //    WebResponse wr;
        //    try
        //    {
        //        wr = rq.GetResponse();
        //    }
        //    catch (WebException wex)
        //    {
        //        wr = wex.Response;
        //        if (rethrowException) throw;
        //    }
        //    using (var rs = wr.GetResponseStream())
        //    using (var rd = new StreamReader(rs))
        //    {
        //        JsonReader jReader = new JsonTextReader(rd);
        //        var conv = JsonSerializer.Create();
        //        var res = conv.Deserialize<responseType>(jReader);
        //        jReader.Close();
        //        rd.Close();
        //        wr.Close();
        //        return res;
        //    }
        //}

        public responseType GetXml<responseType>(string query, int Timeout = 10000, string Authorization = null)
        {
            string baseAddress = TargetURL + (TargetURL.EndsWith("/") ? "" : "/");

            
            HttpRequestMessage request = new HttpRequestMessage();
            request.Method = HttpMethod.Get;
            request.Headers.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", Authorization ?? GetClientToken());
            request.RequestUri = new Uri(baseAddress + query);
            request.Headers.Accept.Add(new System.Net.Http.Headers.MediaTypeWithQualityHeaderValue("text/xml"));
            var response = client.SendAsync(request).Result;

            if (!response.IsSuccessStatusCode)
                throw new HttpRequestException($"{(int)response.StatusCode} {response.ReasonPhrase}", response.StatusCode, response.Content);            

            using (var stream = response.Content.ReadAsStreamAsync().Result)
            {
                XmlSerializer serializer = new XmlSerializer(typeof(responseType));
                return (responseType)serializer.Deserialize(stream);
            }
        }

        //public responseType GetXml<responseType>(string query, int Timeout = 10000, string Authorization = null)
        //{
        //    var rq = CreateHttpWebRequest("GET", query, ContentType: "text/xml", Accept: "text/xml", Timeout: Timeout, Authorization: Authorization);
        //    //using (var rs = rq.GetResponse().GetResponseStream())
        //    //{
        //    //    var rd = System.Xml.XmlReader.Create(rs);
        //    //    var ser = new XmlSerializer(typeof(responseType));
        //    //    var res = (responseType)ser.Deserialize(rd);
        //    //    rd.Close();
        //    //    return res;
        //    //}
        //    using (var rs = rq.GetResponse().GetResponseStream())
        //    using (StreamReader streamReader = new StreamReader(rs))
        //    {
        //        string xmlText = streamReader.ReadToEnd();
        //        using (StringReader stringReader = new StringReader(xmlText))
        //        {
        //            XmlSerializer serializer = new XmlSerializer(typeof(responseType));
        //            return (responseType)serializer.Deserialize(stringReader);
        //        }
        //    }
        //}

        public void ClearTarget()
        {
            if (_settings != null)
            {
                _settings.TargetURL = "";
                _settings.ClientPasscode = null;
                _settings.EncryptedClientPasscode = "IA==";
                _settings.ClientState = ClientStateType.NotConfigured;
                this.SaveSettings();
            }
        }
    }

    public class HttpRequestException : System.Net.Http.HttpRequestException
    {
        public HttpStatusCode HttpStatusCode { get; }

        public HttpContent HttpContent { get; }

        public HttpRequestException(string message, HttpStatusCode httpStatusCode, HttpContent httpContent) : base(message)
        {
            HttpStatusCode = httpStatusCode;
            HttpContent = httpContent;
        }

    }

    public class PublicWatsFilter
    {       
        public string filterName { get; set; }        
        public byte? filterOrder { get; set; }
        public string serialNumber { get; set; }
        public string partNumber { get; set; }
        public string revision { get; set; }
        public string batchNumber { get; set; }       
        public string componentNumber { get; set; }
        public string stationName { get; set; }
        public string testOperation { get; set; }        
        public string repairOperation { get; set; }
        public string status { get; set; }
        public int? yield { get; set; }
        public string miscDescription { get; set; }
        public string miscValue { get; set; }
        public string productGroup { get; set; }
        public string level { get; set; }       
        public string phase { get; set; }
        public string swFilename { get; set; }
        public string swVersion { get; set; }
        public string socket { get; set; }       
        public string repairedUnits { get; set; }
        public DateTime? dateFrom { get; set; }
        public DateTime? dateTo { get; set; }       
        public bool? dateIsLocal { get; set; }
        public PeriodEnum? dateGrouping { get; set; }        
        public DateTimeTypeEnum dateTimeType { get; set; }
        public int? periodCount { get; set; } = 0;
        public bool? includeCurrentPeriod { get; set; }       
        public string appraiserType { get; set; }        
        public string appraiserValue { get; set; }
        public int? maxCount { get; set; }
        public int? minCount { get; set; }
        public int? topCount { get; set; }
        public string dimensions { get; set; }
        public bool includeMissingPeriods { get; set; }



    }
    public class DateTimeTypeEnum
    {

    }
    }
