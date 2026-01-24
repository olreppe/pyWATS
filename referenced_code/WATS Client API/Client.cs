using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.Versioning;

namespace Virinco.WATS.Interface
{
    internal class ClientInfo
    {
        internal Models.Client server { get; set; }
        internal Models.Client local { get; set; }
    }
    internal class ClientInfoHandler
    {
        private TDM _api;
        private ClientInfo _ci = new Interface.ClientInfo();

        private const string clientInfoFilename = "ClientInfo.json";

        internal ClientInfoHandler(TDM api)
        {
            _api = api;
        }

        public Models.Client server
        {
            get
            {
                return _ci.server;
            }
        }
        public Models.Client local
        {
            get
            {
                return _ci.local;
            }
        }

        /// <summary>
        /// Load from local cache
        /// </summary>
        internal void Load()
        {
            using (var txtreader = new StreamReader(Path.Combine(_api.DataDir, clientInfoFilename)))
            {
                var reader = new Newtonsoft.Json.JsonTextReader(txtreader);
                var serializer = new Newtonsoft.Json.JsonSerializer();
                _ci = serializer.Deserialize<ClientInfo>(reader);
            }
        }

        internal bool CanLoad()
        {
            return File.Exists(Path.Combine(_api.DataDir, clientInfoFilename));
        }

        /// <summary>
        /// Save to local cache
        /// </summary>
        internal void Save()
        {
            using (var txtwriter = new StreamWriter(Path.Combine(_api.DataDir, clientInfoFilename)))
            {
                var writer = new Newtonsoft.Json.JsonTextWriter(txtwriter);
                var serializer = new Newtonsoft.Json.JsonSerializer();
                serializer.Serialize(writer, _ci);
            }
        }

#if NET8_0_OR_GREATER
        [SupportedOSPlatform("windows")]
#endif
        /// <summary>
        /// Load from server
        /// </summary>
        internal void Get(bool save = true)
        {
            _ci.server = _api.GetClient(0);
            _ci.local = _api.GetClient(_ci.server.SiteCode, Env.StationName);

            Env.Location = _ci.local.Location ?? "";
            Env.Purpose = _ci.local.Purpose ?? "";

            if (save) Save();
            // Write codes to local cache
        }

        /// <summary>
        /// Push to server !!?
        /// </summary>
#if NET8_0_OR_GREATER
        [SupportedOSPlatform("windows")]
#endif
        internal void Put(string miscinfo = null)
        {
            var dict = new Dictionary<string, string>();
            dict.Add("name", Env.StationName);
            //dict.Add("location", _api.Location); //Dont update location, it can only be set from server
            //dict.Add("purpose", _api.Purpose); //Dont update location, it can only be set from server
            dict.Add("utcoffset", DateTimeOffset.Now.Offset.ToString());
            if (!string.IsNullOrEmpty(miscinfo)) dict.Add("miscinfo", miscinfo);
            _ci.local = _api.proxy.PostJson<Models.Client>("api/internal/Client/update", dict);
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Update memberinfo: finished");
        }        
    }
}
