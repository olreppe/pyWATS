extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Reserved for use with TestStand. Does not show up in analysis.
    /// An additional result can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
    /// </summary>
    public class AdditionalResult
    {
        internal napi.AdditionalResult _instance;
        internal AdditionalResult(napi.AdditionalResult instance) { _instance = instance; }

        /// <summary>
        /// Element Name
        /// </summary>
        public string Name
        {
            get => _instance.Name;
            set => _instance.Name = value;
        }

        /// <summary>
        /// Contents
        /// </summary>
        public System.Xml.Linq.XElement Contents
        {
            get => _instance.Contents;
            set => _instance.Contents = value;
        }
    }
}
