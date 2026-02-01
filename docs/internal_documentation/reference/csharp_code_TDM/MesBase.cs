using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Runtime.Versioning;
using System.Xml.Linq;
using Virinco.WATS.Configuration;
using Virinco.WATS.REST;
using Virinco.WATS.Service.MES.Contract;

namespace Virinco.WATS.Interface.MES
{
    internal class MesServiceProxy : REST.ServiceProxy
    {
        public new string GetClientToken()
        {
            return base.GetClientToken();
        }

        public string GetTargetURL()
        {
            return base.TargetURL;
        }

        public new T PostJson<T>(string baseUrl, string query, string authorization, object content)
        {
            return base.PostJson<T>(baseUrl, query, authorization, content);
        }

    }


    /// <summary>
    /// Base class for use in Production, Product, Software, Equipment and Asset...
    /// </summary>
    public class MesBase
    {
        //IMesService svc_mes;
        //IProductionService svc_production;
        //IProductService svc_product;
        //ISoftwareService svc_sw, svc_sw_stream;
        //IEquipmentService svc_equipment;
        //IWorkflowService svc_workflow;
        internal Dictionary<int, string> Translations = new Dictionary<int, string>();

        /// <summary>
        /// Base constructor
        /// </summary>
        public MesBase() { this.CultureCode = "en"; loadSettings(); }

        /// <summary>
        /// Constructor with culture
        /// </summary>
        /// <param name="CultureCode"></param>
        public MesBase(string CultureCode) { this.CultureCode = CultureCode; loadSettings(); }

        #region Services


        internal ServiceProxy serviceProxy = new ServiceProxy();
        protected string adminToken = null;
#if NET8_0_OR_GREATER
        [SupportedOSPlatform("windows")]
#endif
        private void loadSettings()
        {
            try
            {
                serviceProxy.LoadSettings();
            }
            catch (Exception ex) { Env.LogException(ex, "Unable to load MES server settings"); }
        }

        /// <summary>
        /// Allow to use alternative credentials when calling "admistrative functions"
        /// </summary>
        /// <param name="userName"></param>
        /// <param name="password"></param>
        public void SetAdminCredentials(string userName, string password)
        {
            adminToken= serviceProxy.GetB64String("{0}:{1}", userName, password);            
        }


        /// <summary>
        /// Perform WATS REST GET call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTGetJson<responseType>(string query, bool useAdminCredentials=false)
        {
            try
            {
                if (useAdminCredentials && string.IsNullOrEmpty(adminToken))
                    throw new ApplicationException("Admin credentials not set, use SetAdminCredentials prior to call");
                return serviceProxy.GetJson<responseType>(query,Authorization:useAdminCredentials ? adminToken : null);
            }
            catch (Exception ex) { Env.LogException(ex, "Error calling RESTGetJson"); }
            return default(responseType);
        }

        /// <summary>
        /// Perform WATS REST GET call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="obj">See swagger doc</param>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTPostJson<responseType>(string query, object obj, bool useAdminCredentials=false)
        {
            try
            {
                if (useAdminCredentials && string.IsNullOrEmpty(adminToken))
                    throw new ApplicationException("Admin credentials not set, use SetAdminCredentials prior to call");
                return serviceProxy.PostJson<responseType>(query, obj, useAdminCredentials ? adminToken : null);
            }
            catch (Exception ex) { Env.LogException(ex, "Error calling RESTPostJson"); throw; }
        }

        /// <summary>
        /// Perform WATS REST GET call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="obj">See swagger doc</param>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTPutJson<responseType>(string query, object obj=null, bool useAdminCredentials=false)
        {
            try
            {
                if (useAdminCredentials && string.IsNullOrEmpty(adminToken))
                    throw new ApplicationException("Admin credentials not set, use SetAdminCredentials prior to call");
                return serviceProxy.PutJson<responseType>(query, obj, useAdminCredentials ? adminToken : null);
            }
            catch (Exception ex) { Env.LogException(ex, "Error calling RESTPutJson"); throw; }
        }

        /// <summary>
        /// Perform WATS REST DELETE call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="obj">See swagger doc</param>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTDeleteJson<responseType>(string query, object obj = null, bool useAdminCredentials = false)
        {
            try
            {
                if (useAdminCredentials && string.IsNullOrEmpty(adminToken))
                    throw new ApplicationException("Admin credentials not set, use SetAdminCredentials prior to call");
                return serviceProxy.DeleteJson<responseType>(query, obj, useAdminCredentials ? adminToken : null);
            }
            catch (Exception ex) { Env.LogException(ex, "Error calling RESTDeleteJson"); throw; }
        }

        /// <summary>
        /// Returns true if connection to server is ok. TODO: Also check database on server
        /// </summary>
        /// <returns></returns>
        public bool isConnected()
        {
            try
            {
                if (this is Production.Production)
                    return serviceProxy.GetJson<bool>($"api/internal/Production/isConnected");
                else if (this is Product.Product)
                    return serviceProxy.GetJson<bool>($"api/internal/Product/isConnected");
                else if (this is Software.Software)
                    return serviceProxy.GetJson<bool>($"api/internal/software/isConnected");
                else if (this is Asset.AssetHandler)
                    return serviceProxy.GetJson<bool>($"api/internal/mes/isConnected");
                else if (this is Workflow.Workflow)
                    return serviceProxy.GetJson<bool>($"api/internal/workflow/isConnected");
                else if (this is MesBase)
                    return serviceProxy.GetJson<bool>($"api/internal/mes/isConnected");
                return false;
            }
            catch (Exception e)
            {
                Env.LogException(e, "Unable to connect to service");
            }
            return false;
        }
        #endregion


        /// <summary>
        /// Language code
        /// </summary>
        public string CultureCode { get; set; }

        /// <summary>
        /// Translates english to language given by Culture
        /// </summary>
        /// <param name="Culture"></param>
        /// <param name="EnglishText"></param>
        /// <param name="arguments"></param>
        /// <returns></returns>
        public string TranslateString(string Culture, string EnglishText, object[] arguments)
        {
            try
            {
                string translatedText;
                if (arguments != null)
                    //Cannot cache texts with arguments, can be fixed by applying server logic in client
                    translatedText = serviceProxy.PostJson<string>($"api/internal/mes/Translate?cultureCode=" + Culture + "&englishText=" + EnglishText, arguments);
                else
                {
                    int key = (Culture + EnglishText).GetHashCode();
                    if (!Translations.ContainsKey(key)) {
                        translatedText = serviceProxy.PostJson<string>($"api/internal/mes/Translate?cultureCode=" + Culture + "&englishText=" + EnglishText, arguments);
                        Translations.Add(key, translatedText);
                    }
                    translatedText = Translations[key];
                }
                return translatedText;
            }
            catch (Exception e)
            {
                Env.LogException(e, "Failed to translate text");
                return EnglishText;
            }
        }

        /// <summary>
        /// Define language in CultureCode property 
        /// </summary>
        /// <param name="EnglishText"></param>
        /// <param name="arguments"></param>
        /// <returns></returns>
        public string TranslateString(string EnglishText, object[] arguments)
        {
            return TranslateString(CultureCode, EnglishText, arguments);
        }

        /// <summary>
        /// Define language in CultureCode property
        /// </summary>
        /// <param name="englishText"></param>
        /// <returns></returns>
        public string[] TranslateArray(string[] englishText)
        {
            return TranslateArray(CultureCode, englishText);
        }

        /// <summary>
        /// Translates an array of english texts
        /// </summary>
        /// <param name="CultureCode"></param>
        /// <param name="englishText"></param>
        /// <returns></returns>
        public string[] TranslateArray(string CultureCode, string[] englishText)
        {
            if (CultureCode == "en")
                return englishText;

            try
            {
                string[] ret = new string[englishText.Length];
                for (int i = 0; i < ret.Length; i++)
                {
                    int key = (CultureCode + englishText[i]).GetHashCode();
                    if (Translations.ContainsKey(key))
                        ret[i] = Translations[key];
                    else
                    { ret = null; break; }
                }

                if (ret == null)
                {
                    string[] t = serviceProxy.PostJson<string[]>($"api/internal/mes/TranslateArray?cultureCode=" + CultureCode, englishText);
                    for (int i = 0; i < englishText.Length; i++)
                    {
                        int key = (CultureCode + englishText[i]).GetHashCode();
                        if (!Translations.ContainsKey(key))
                            Translations.Add(key, t[i]);
                    }
                    return t;
                }
                else
                    return ret;
            }
            catch (Exception e)
            {
                Env.LogException(e, "Failed to translate text");
                return englishText;
            }
        }


        Process[] _processes;
        /// <summary>
        /// Get Processes. By default will only test operations be returned
        /// </summary>
        /// <param name="IsTestOperation">return processes marked as test operation</param>
        /// <param name="IsRepairOperation">return processes marked as repair operation</param>
        /// <param name="IsWIPOperation">return processes marked as WIP operation</param>
        /// <returns></returns>
        public Process[] GetProcesses(bool IsTestOperation = true, bool IsRepairOperation = false, bool IsWIPOperation = false)
        {
            if (_processes == null) {
                _processes = serviceProxy.GetJson<IEnumerable<Process>>($"api/internal/process/GetProcesses").Where(p => p.State == 1).ToArray();                                             
            }                
            return _processes.Where(p => (p.IsTestOperation && IsTestOperation) || (p.IsRepairOperation && IsRepairOperation) || (p.IsWIPOperation && IsWIPOperation)).OrderBy(p=>p.Name).ToArray();
        }


        private T[] getArr<T>(string[] keys)
        {
            T[] ret = new T[keys == null ? 0 : keys.Length];
            if (keys != null)
            {
                string q = "";
                keys.ToList().ForEach(k => q += $"key eq '{k}' or ");
                q = q.Remove(q.Length - 4, 4);
                object res = serviceProxy.GetJson<object>($"api/internal/Mes/GetSettings?$filter={q}");

                if (res != null)
                {
                    Newtonsoft.Json.Linq.JArray a = Newtonsoft.Json.Linq.JArray.Parse(res.ToString());

                    foreach (Newtonsoft.Json.Linq.JObject o in a.Children<Newtonsoft.Json.Linq.JObject>())
                    {
                        string key = (string)o.GetValue("key").ToString();
                        string val = (string)o.GetValue("value");

                        int keyIndex = Array.FindIndex(keys, w => w == key);
                        if (typeof(T) == typeof(bool))    //1 == true, 0 == false                
                            ret[keyIndex] = (T)Convert.ChangeType(Utilities.ParseBool(val, false), typeof(T));
                        else
                            ret[keyIndex] = val == null ? default(T) : (T)Convert.ChangeType(val, typeof(T));
                    }
                }
            }
            return ret;
        }

        /// <summary>
        /// Gets MES Server settings
        /// </summary>
        /// <param name="stringValues"></param>
        /// <param name="boolValues"></param>
        /// <param name="numberValues"></param>
        /// <param name="stringKeys"></param>
        /// <param name="boolKeys"></param>
        /// <param name="numberKeys"></param>
        public void GetMesServerSettings(out string[] stringValues, out bool[] boolValues, out int[] numberValues, string[] stringKeys = null, string[] boolKeys = null, string[] numberKeys = null)
        {
            stringValues = new string[stringKeys == null ? 0 : stringKeys.Length];
            boolValues = new bool[boolKeys == null ? 0 : boolKeys.Length];
            numberValues = new int[numberKeys == null ? 0 : numberKeys.Length];
            try
            {
                boolValues = getArr<bool>(boolKeys);
                stringValues = getArr<string>(stringKeys);
                numberValues = getArr<int>(numberKeys);
            }
            catch (Exception ex) { Env.LogException(ex, "Unable to get MES server settings from API"); }
        }

        /// <summary>
        /// Gets user settings
        /// </summary>
        /// <param name="UserName"></param>
        /// <returns></returns>
        public CommonUserSettings GetCommonUserSettings(string UserName)
        {
            try
            {
                return serviceProxy.GetJson<CommonUserSettings>($"api/internal/mes/GetCommonUserSettings?userName=" + UserName);
            }
            catch (Exception ex) { Env.LogException(ex, "GetCommonUserSettings"); }
            return null;
        }

        Dictionary<string, string> _generalOptions = null;
        Dictionary<string, string> generalOptions
        {
            get
            {
                if (_generalOptions == null) ReadGeneralOptions();
                return _generalOptions;
            }
        }
        private void ReadGeneralOptions()
        {
            _generalOptions = new Dictionary<string, string>();
            string path = Virinco.WATS.Env.GetConfigFilePath(Virinco.WATS.Env.GeneralSettingsFileName);
            ExeConfigurationFileMap configFileMap = new ExeConfigurationFileMap();
            configFileMap.ExeConfigFilename = path;
            System.Configuration.Configuration cfg = ConfigurationManager.OpenMappedExeConfiguration(configFileMap, ConfigurationUserLevel.None);
            foreach (KeyValueConfigurationElement element in cfg.AppSettings.Settings)
            {
                _generalOptions.Add(element.Key, element.Value);
            }
        }

        /// <summary>
        /// General string option
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public string GetGeneralOptionString(string key)
        {
            if (generalOptions.ContainsKey(key))
                return generalOptions[key];
            else
                return "";
        }

        /// <summary>
        /// General bool option
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public bool GetGeneralOptionBool(string key)
        {
            if (generalOptions.ContainsKey(key))
            {
                bool value;
                int iValue;
                if (bool.TryParse(generalOptions[key], out value)) return value;
                else if (int.TryParse(generalOptions[key], out iValue)) return iValue != 0;
                else return false;
            }
            else
                return false;
        }

        public int GetGeneralOptionInt(string key)
        {
            int iValue;
            if (generalOptions.ContainsKey(key))
                return int.TryParse(generalOptions[key], out iValue) ? iValue : -1;
            else
                return -1;
        }

        /// <summary>
        /// GUI for simple MES connectivity testing
        /// </summary>
        public void DisplayMesTestGUI()
        {
            MesTestGUI tg = new MesTestGUI();
            tg.ShowDialog();
        }

        #region Storage

        /// <summary>
        /// Get XML stored with a given key (KeyValue pair)
        /// </summary>
        /// <param name="key"></param>
        /// <returns>XML value stored with the Key</returns>
        public string GetStorageXml(string key)
        {
            if (isConnected())
            {
                try
                {
                    KeyValue kv = serviceProxy.GetJson<KeyValue>($"api/internal/mes/GetKeyValue?key=" + key);
                    if (kv != null)
                        return kv.Xml;
                }
                catch (Exception ex) { Env.LogException(ex, "Error in GetStorageXml"); }
            }
            return null;
        }

        /// <summary>
        /// Get string value stored with a given key (KeyValue pair)
        /// </summary>
        /// <param name="key">KeyValue.KEY</param>
        /// <returns>string value stored with the Key</returns>
        public string GetStorageValue(string key)
        {
            if (isConnected())
            {
                try
                {
                    KeyValue kv = serviceProxy.GetJson<KeyValue>($"api/internal/mes/GetKeyValue?key=" + key);
                    if (kv != null)
                        return kv.Value;
                }
                catch (Exception ex) { Env.LogException(ex, "Error in GetStorageValue"); }
            }
            return null;
        }

        /// <summary>
        /// Add string and or XML data (xml datatype) to a given key
        /// </summary>
        /// <param name="key">KeyValue.KEY</param>
        /// <param name="value">KeyValue.stringvalue</param>
        /// <param name="xml">KeyValue.xmldata</param>
        /// <returns></returns>
        public bool PutStorageData(string key, string value, string xml)
        {
            if (isConnected())
            {
                try
                {
                    KeyValue kv = new KeyValue() { Key = key, Value = value, Xml = xml };
                    serviceProxy.PostJson<KeyValue>($"api/internal/mes/UpdateKeyValue", kv);
                    return true;
                }
                catch (Exception ex) { Env.LogException(ex, "Error in PutStorageData"); }
            }
            return false;
        }

        /// <summary>
        /// Remove KeyValue with a given Key
        /// </summary>
        /// <param name="key">KeyValue.KEY</param>
        /// <returns></returns>
        public bool RemoveStorageData(string key)
        {
            if (isConnected())
            {
                try
                {
                    KeyValue kv = new KeyValue() { Key = key };
                    kv.StartTracking();
                    kv.MarkAsDeleted();
                    serviceProxy.CreateHttpWebRequest("DELETE", $"api/internal/mes/DeleteKeyValue?key=" + key).GetResponse().Close();
                    return true;
                }
                catch (Exception ex) { Env.LogException(ex, "Error in RemoveStorageData"); }
            }
            return false;
        }


        #endregion

        #region Env

        /// <summary>
        /// Property to set if any Exception should be thrown
        /// </summary>
        public bool RethrowException
        {
            get { return Env.RethrowException; }
            set { Env.RethrowException = value; }
        }

        /// <summary>
        /// Property to retrive the last Exception thrown
        /// </summary>
        public Exception LastException
        {
            get { return Env.LastException; }
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
        /// Property to set the operator for the session
        /// </summary>
        public string Operator
        {
            get { return Env.Operator; }
            set { Env.Operator = value; }
        }

        /// <summary>
        /// Starts to collect trace information to eventlog (API debug purpose)
        /// </summary>
        public void StartTraceToEventLog()
        {
            Env.StartTraceToEventLog();
        }

        /// <summary>
        /// Stop trace information to eventlog (stop API debug)
        /// </summary>
        public void StopTraceToEventLog()
        {
            Env.StopTraceToEventLog();
        }

        #endregion


        private string GetEndpointIdentity(string address, string servicetype)
        {
            // Download & Parse WSDL for service (service url + "?wsdl)
            XDocument wsdl = XDocument.Load(address + "?wsdl");
            return wsdl.Root.Elements("{http://schemas.xmlsoap.org/wsdl/}service").Where(s => s.Attribute("name").Value == "MesService").First().Elements("{http://schemas.xmlsoap.org/wsdl/}port").Where(p => p.Attribute("name").Value == servicetype).First().Element("{http://www.w3.org/2005/08/addressing}EndpointReference").Element("{http://schemas.xmlsoap.org/ws/2006/02/addressingidentity}Identity").Element("{http://schemas.xmlsoap.org/ws/2006/02/addressingidentity}Dns").Value;
            /*
             * <{http://schemas.xmlsoap.org/wsdl/}service name="ReportCenter">
             *   <{http://www.w3.org/2005/08/addressing}EndpointReference>
             *     <Identity xmlns="http://schemas.xmlsoap.org/ws/2006/02/addressingidentity">
             *       <Dns>value</Dns> 
             *     </Identity
             *   </EndpointReference>
             * </service>
             */
        }

    }
}
