using System.Collections.Generic;
using System.IO;
using System.Runtime.Versioning;
using Newtonsoft.Json;

namespace Virinco.WATS.Interface.Configuration
{
    /// <summary>
    /// Loads saves converter settings
    /// </summary>
    public class ConverterSettings
    {
        Dictionary<string, string> _settings;
        string _fileName="";

#if NET8_0_OR_GREATER
        [SupportedOSPlatform("windows")]
#endif
        /// <summary>
        /// Loads / Saves converter specific settings
        /// </summary>
        /// <param name="converterName"></param>
        public ConverterSettings(string converterName)
        {
            _fileName = Path.Combine(Env.DataDir, converterName) + "_settings.json";
            if (File.Exists(_fileName))
            {
                JsonSerializer ser = new JsonSerializer();
                using (StreamReader str = File.OpenText(_fileName))
                    _settings = (Dictionary<string, string>)ser.Deserialize(str, typeof(Dictionary<string,string>));
            }
            else
            {
                _settings = new Dictionary<string, string>();
            }
        }

        /// <summary>
        /// Get / Set converter setting
        /// </summary>
        /// <param name="key"></param>
        /// <returns></returns>
        public string this [string key]
        {
            get
            {
                if (!_settings.ContainsKey(key))
                    _settings.Add(key,"");
                return _settings[key];
            }
            set
            {
                if (!_settings.ContainsKey(key))
                    _settings.Add(key, value);
                else
                    _settings[key]=value;
            }
        }

        /// <summary>
        /// Saves converter settings
        /// </summary>
        public void Save()
        {
            JsonSerializer ser = new JsonSerializer();
            using (StreamWriter str = new StreamWriter(_fileName))
                ser.Serialize(str, _settings);
        }
    }
}
