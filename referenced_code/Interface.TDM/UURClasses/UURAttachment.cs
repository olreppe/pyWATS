extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// An attachment (file) to a UUR report or failure
    /// </summary>
    public class UURAttachment
    {
        internal napi.UURAttachment _instance;
        internal UURAttachment(napi.UURAttachment instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Original filename (if set)
        /// </summary>
        public string FileName // r/o
        {
            get => _instance.FileName;
            //set => _instance.FileName = value;
        }

        /// <summary>
        /// Returns attachment data as byte array
        /// </summary>
        public byte[] Data // r/o
        {
            get => _instance.Data;
            //set => _instance.Data = value;
        }

        /// <summary>
        /// MIME type of the attachment
        /// </summary>
        public string MimeType
        {
            get => _instance.MimeType;
            set => _instance.MimeType = value;
        }
    }
}
