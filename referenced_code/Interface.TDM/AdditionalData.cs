extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

using System.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// An additional data can represent any kind of data, formatted as xml node.
    /// </summary>
    public class AdditionalData
    {
        internal napi.AdditionalData _baseinstance;
        internal AdditionalData(napi.AdditionalData instance) { _baseinstance = instance; }

        /// <summary>
        /// Element Name
        /// </summary>
        public string Name
        {
            get => _baseinstance.Name;
            set => _baseinstance.Name = value;
        }

        /// <summary>
        /// Contents
        /// </summary>
        public System.Xml.Linq.XElement Contents
        {
            get => _baseinstance.Contents;
            set => _baseinstance.Contents = value;
        }
    }
}
