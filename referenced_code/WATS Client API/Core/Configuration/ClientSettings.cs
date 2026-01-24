using System;
using System.Collections.Generic;
using System.Configuration;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace Virinco.WATS.Configuration
{
    /// <summary>
    /// Class reflecting contents of WATS' settings.json file
    /// </summary>
    public class ClientSettings
    {
        internal ClientSettings()
        {
            // Apply default values:
            this.MaxAttachmentFileSize = 1024 * 2000;
            this.MaxChartSeries = 50;
            this.ClientState = Interface.ClientStateType.Unknown;
            this.LoggingSettings = new LoggingSettings();
            this.DownloadClientUpdateTimeout = 600000;
            this.SubmitPendingDelay = 1000;
        }

        public static ClientSettings Load(string FullPath)
        {
            ClientSettings s;
            if (File.Exists(FullPath))
            {
                // Load existing file
                JsonSerializer ser = new JsonSerializer();
                using (var fs = File.Open(FullPath, FileMode.Open, FileAccess.Read, FileShare.Read))
                using (var sr = new StreamReader(fs))
                    s = (ClientSettings)ser.Deserialize(sr, typeof(ClientSettings));

                if (s != null)
                {
                    if (s.LoggingSettings != null)
                    {
                        if (s.LoggingSettings.Overridden && (!s.LoggingSettings.OverrideExpiresDate.HasValue || DateTimeOffset.UtcNow > s.LoggingSettings.OverrideExpiresDate))
                        {
                            s.LoggingSettings.Overridden = false;
                            s.LoggingSettings.OverrideExpiresDate = null;

                            if (s.LoggingSettings.OverriddenLoggingLevel.HasValue)
                            {
                                s.LoggingSettings.LoggingLevel = s.LoggingSettings.OverriddenLoggingLevel.Value;
                                s.LoggingSettings.OverriddenLoggingLevel = null;
                            }
                        }
                    }
                    else
                        s.LoggingSettings = new LoggingSettings();

                    return s;
                }
            }
            
            // Create new
            s = new ClientSettings();
            return s;
        }

        internal void Save(string FullPath)
        {
            JsonSerializer ser = new JsonSerializer();
            using (StreamWriter str = new StreamWriter(FullPath))
                ser.Serialize(str, this);
        }

        [Obsolete]
        [JsonProperty("ClientPasscode", DefaultValueHandling = DefaultValueHandling.Ignore)]
        internal string ClientPasscode { get; set; }


        [JsonProperty("Passcode")]
        internal string EncryptedClientPasscode { get; set; }

        /// <summary>
        /// Currently configured server url (base url) 
        /// </summary>
        [JsonProperty("TargetURL")]
        public string TargetURL { get; set; }

        /// <summary>
        /// Client's last known state
        /// Used to signal external applications of client registration
        /// </summary>
        [JsonProperty("ClientState")]
        [JsonConverter(typeof(StringEnumConverter))]
        public Interface.ClientStateType ClientState { get; set; }

        /// <summary>
        /// Get maximum allowed file attachment size in bytes (default is 2MB)
        /// </summary>
        [JsonProperty("MaxAttachmentFileSize")]
        public long MaxAttachmentFileSize { get; internal set; }

        /// <summary>
        /// Get maximum allowed number of series in a chart (default is 50)
        /// </summary>
        [JsonProperty("MaxChartSeries")]
        public long MaxChartSeries { get; internal set; }

        [JsonProperty("LoggingSettings")]
        public LoggingSettings LoggingSettings { get; set; }

        public ProxySettings ProxySettings { get; set; }

        [JsonProperty("DownloadClientUpdateTimeout")]
        public int DownloadClientUpdateTimeout { get; set; }

        [JsonProperty("SubmitPendingDelay")]
        public int SubmitPendingDelay { get; set; }
    }

    public class LoggingSettings
    {
        public SourceLevels LoggingLevel { get; set; } = SourceLevels.Critical | SourceLevels.Error | SourceLevels.Warning | SourceLevels.Information;

        public bool Overridden { get; set; } = false;

        public SourceLevels? OverriddenLoggingLevel { get; set; } = null;

        public DateTimeOffset? OverrideExpiresDate { get; set; } = null;
    }

    /// <summary>
    /// Proxy server authentication methods: None, Default or Custom
    /// </summary>
    public enum ProxyMethodEnum { None, Default, Custom }
    public class ProxySettings
    {
        private Security.SimpleAes enc = new Security.SimpleAes();

        /// <summary>
        /// Proxy method: None, Default or Custom
        /// </summary>
        [JsonConverter(typeof(StringEnumConverter))]
        public ProxyMethodEnum Method { get; set; }
        /// <summary>
        /// Proxy server address (for custom method)
        /// </summary>
        public string Address { get; set; }
        /// <summary>
        /// Proxy server user name (for custom method)
        /// </summary>
        public string Username { get; set; }
        /// <summary>
        /// Proxy server user-domain (for custom method)
        /// </summary>
        public string Domain { get; set; }

        [JsonProperty("Password")]
        public string EncryptedPassword { get { return string.IsNullOrEmpty(this.Password) ? null : enc.Encrypt(this.Password); } set { try { this.Password = string.IsNullOrEmpty(value) ? null : enc.Decrypt(value); } catch { this.Password = ""; } } }
        /// <summary>
        /// Proxy server password (for custom method)
        /// </summary>
        [JsonIgnore]
        public string Password { get; set; }

        public ProxySettings Clone()
        {
            return new ProxySettings() { Method = this.Method, Address = this.Address, Username = this.Username, Domain = this.Domain, Password = this.Password };
        }

        public override bool Equals(object obj)
        {
            return base.Equals(obj);
        }

        public override int GetHashCode()
        {
            return base.GetHashCode();
        }

        public static bool operator ==(ProxySettings a, ProxySettings b)
        {
            if (object.ReferenceEquals(null, a))
                return object.ReferenceEquals(null, b);
            else if (object.ReferenceEquals(null, b))
                return false;
            else
                return (a.Method == b.Method && a.Address == b.Address && a.Username == b.Username && a.Domain == b.Domain && a.Password == b.Password);
        }

        public static bool operator !=(ProxySettings a, ProxySettings b) { return !(a == b); }
    }
}
