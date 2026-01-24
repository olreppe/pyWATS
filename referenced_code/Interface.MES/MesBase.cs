extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using Virinco.WATS.Service.MES.Contract;
using System;
using System.Linq;

namespace Virinco.WATS.Interface.MES
{
    /// <summary>
    /// Base class for use in Production, Product, Software, Equipment and Asset...
    /// </summary>
    public class MesBase
    {
        internal napi.MesBase _baseinstance;

        internal MesBase(napi.MesBase mesbase)
        {
            this._baseinstance = mesbase;
        }

        /// <summary>
        /// Base constructor
        /// </summary>
        public MesBase()
        {
            _baseinstance = new napi.MesBase();
        }

        /// <summary>
        /// Constructor with culture
        /// </summary>
        /// <param name="CultureCode"></param>
        public MesBase(string CultureCode)
        {
            _baseinstance = new napi.MesBase(CultureCode);
        }

        #region Services

        /// <summary>
        /// Allow to use alternative credentials when calling "admistrative functions"
        /// </summary>
        /// <param name="userName"></param>
        /// <param name="password"></param>
        public void SetAdminCredentials(string userName, string password)
            => _baseinstance.SetAdminCredentials(userName, password);

        /// <summary>
        /// Perform WATS REST GET call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTGetJson<responseType>(string query, bool useAdminCredentials = false)
            => _baseinstance.RESTGetJson<responseType>(query, useAdminCredentials);

        /// <summary>
        /// Perform WATS REST GET call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="obj">See swagger doc</param>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTPostJson<responseType>(string query, object obj, bool useAdminCredentials = false)
            => _baseinstance.RESTPostJson<responseType>(query, obj, useAdminCredentials);

        /// <summary>
        /// Perform WATS REST GET call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="obj">See swagger doc</param>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTPutJson<responseType>(string query, object obj = null, bool useAdminCredentials = false)
            => _baseinstance.RESTPutJson<responseType>(query, obj, useAdminCredentials);

        /// <summary>
        /// Perform WATS REST DELETE call to WATS
        /// </summary>
        /// <typeparam name="responseType">See swagger doc</typeparam>
        /// <param name="obj">See swagger doc</param>
        /// <param name="query">See swagger doc</param>
        /// <param name="useAdminCredentials">Uses administrative credentials set by <see cref="SetAdminCredentials"/></param>
        /// <returns></returns>
        public responseType RESTDeleteJson<responseType>(string query, object obj = null, bool useAdminCredentials = false)
            => _baseinstance.RESTDeleteJson<responseType>(query, obj, useAdminCredentials);

        /// <summary>
        /// Returns true if connection to server is ok. TODO: Also check database on server
        /// </summary>
        /// <returns></returns>
        public bool isConnected()
            => _baseinstance.isConnected();
        #endregion

        /// <summary>
        /// Language code
        /// </summary>
        public string CultureCode
        {
            get => _baseinstance.CultureCode;
            set => _baseinstance.CultureCode = value;
        }

        /// <summary>
        /// Translates english to language given by Culture
        /// </summary>
        /// <param name="Culture"></param>
        /// <param name="EnglishText"></param>
        /// <param name="arguments"></param>
        /// <returns></returns>
        public string TranslateString(string Culture, string EnglishText, object[] arguments)
            => _baseinstance.TranslateString(Culture, EnglishText, arguments);

        /// <summary>
        /// Define language in CultureCode property 
        /// </summary>
        /// <param name="EnglishText"></param>
        /// <param name="arguments"></param>
        /// <returns></returns>
        public string TranslateString(string EnglishText, object[] arguments)
            => _baseinstance.TranslateString(EnglishText, arguments);

        /// <summary>
        /// Define language in CultureCode property
        /// </summary>
        /// <param name="englishText"></param>
        /// <returns></returns>
        public string[] TranslateArray(string[] englishText)
            => _baseinstance.TranslateArray(englishText);

        /// <summary>
        /// Translates an array of english texts
        /// </summary>
        /// <param name="CultureCode"></param>
        /// <param name="englishText"></param>
        /// <returns></returns>
        public string[] TranslateArray(string CultureCode, string[] englishText)
            => _baseinstance.TranslateArray(CultureCode, englishText);

        /// <summary>
        /// Get Processes. By default will only test operations be returned
        /// </summary>
        /// <param name="IsTestOperation">return processes marked as test operation</param>
        /// <param name="IsRepairOperation">return processes marked as repair operation</param>
        /// <param name="IsWIPOperation">return processes marked as WIP operation</param>
        /// <returns></returns>
        public Process[] GetProcesses(bool IsTestOperation = true, bool IsRepairOperation = false, bool IsWIPOperation = false)
            => _baseinstance.GetProcesses(IsTestOperation, IsRepairOperation, IsWIPOperation).Select(p => new Process(p)).ToArray();

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
            => _baseinstance.GetMesServerSettings(out stringValues, out boolValues, out numberValues, stringKeys, boolKeys, numberKeys);

        /// <summary>
        /// Gets user settings
        /// </summary>
        /// <param name="UserName"></param>
        /// <returns></returns>
        public Configuration.CommonUserSettings GetCommonUserSettings(string UserName)
            => new Configuration.CommonUserSettings(_baseinstance.GetCommonUserSettings(UserName));

        /// <summary>
        /// General string option
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public string GetGeneralOptionString(string key)
            => _baseinstance.GetGeneralOptionString(key);

        /// <summary>
        /// General bool option
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public bool GetGeneralOptionBool(string key)
            => _baseinstance.GetGeneralOptionBool(key);

        /// <summary>
        /// General int option
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public int GetGeneralOptionInt(string key)
            => _baseinstance.GetGeneralOptionInt(key);

        /// <summary>
        /// GUI for simple MES connectivity testing
        /// </summary>
        public void DisplayMesTestGUI()
            => _baseinstance.DisplayMesTestGUI();

        #region Storage

        /// <summary>
        /// Get XML stored with a given key (KeyValue pair)
        /// </summary>
        /// <param name="key"></param>
        /// <returns>XML value stored with the Key</returns>
        public string GetStorageXml(string key)
            => _baseinstance.GetStorageXml(key);

        /// <summary>
        /// Get string value stored with a given key (KeyValue pair)
        /// </summary>
        /// <param name="key">KeyValue.KEY</param>
        /// <returns>string value stored with the Key</returns>
        public string GetStorageValue(string key)
            => _baseinstance.GetStorageValue(key);

        /// <summary>
        /// Add string and or XML data (xml datatype) to a given key
        /// </summary>
        /// <param name="key">KeyValue.KEY</param>
        /// <param name="value">KeyValue.stringvalue</param>
        /// <param name="xml">KeyValue.xmldata</param>
        /// <returns></returns>
        public bool PutStorageData(string key, string value, string xml)
            => _baseinstance.PutStorageData(key, value, xml);

        /// <summary>
        /// Remove KeyValue with a given Key
        /// </summary>
        /// <param name="key">KeyValue.KEY</param>
        /// <returns></returns>
        public bool RemoveStorageData(string key)
            => _baseinstance.RemoveStorageData(key);

        #endregion

        #region Env

        /// <summary>
        /// Property to set if any Exception should be thrown
        /// </summary>
        public bool RethrowException
        {
            get => _baseinstance.RethrowException;
            set => _baseinstance.RethrowException = value;
        }

        /// <summary>
        /// Property to retrive the last Exception thrown
        /// </summary>
        public Exception LastException // r/o
        {
            get => _baseinstance.LastException;
            //set => _baseinstance.LastException = value;
        }

        /// <summary>
        /// Property to set if any Exception should be written to eventlog
        /// </summary>
        public bool LogExceptions
        {
            get => _baseinstance.LogExceptions;
            set => _baseinstance.LogExceptions = value;
        }

        /// <summary>
        /// Property to set the operator for the session
        /// </summary>
        public string Operator
        {
            get => _baseinstance.Operator;
            set => _baseinstance.Operator = value;
        }

        /// <summary>
        /// Starts to collect trace information to eventlog (API debug purpose)
        /// </summary>
        public void StartTraceToEventLog()
            => _baseinstance.StartTraceToEventLog();

        /// <summary>
        /// Stop trace information to eventlog (stop API debug)
        /// </summary>
        public void StopTraceToEventLog()
            => _baseinstance.StopTraceToEventLog();

        #endregion
    }
}