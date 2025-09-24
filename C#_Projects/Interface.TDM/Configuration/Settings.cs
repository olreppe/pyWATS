using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Virinco.Virinco.Newtonsoft.Json;
using Virinco.Virinco.Newtonsoft.Json.Converters;

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
            this.ClientState = ClientStateType.Unknown;
        }

        internal static ClientSettings Load(string FullPath)
        {
            ClientSettings s;
            if (File.Exists(FullPath))
            {
                // Load existing file
                JsonSerializer ser = new JsonSerializer();
                using (StreamReader str = File.OpenText(FullPath))
                    s = (ClientSettings)ser.Deserialize(str, typeof(ClientSettings));
            }
            else
            {
                // Create new file
                s = new ClientSettings();
                s.Save(FullPath);
            }
            return s;
        }

        internal void Save(string FullPath)
        {
            JsonSerializer ser = new JsonSerializer();
            using (StreamWriter str = new StreamWriter(FullPath))
                ser.Serialize(str, this);
        }

        [JsonProperty("ClientPasscode")]
        internal string ClientPasscode { get; set; }

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
        public ClientStateType ClientState { get; set; }

        /// <summary>
        /// Get maximum allowed file attachment size in bytes (default is 2MB)
        /// </summary>
        [JsonProperty("MaxAttachmentFileSize")]
        public long MaxAttachmentFileSize { get; internal set; }
    }
}
