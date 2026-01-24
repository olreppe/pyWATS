extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// An attachment (file) to any step type can be added
    /// </summary>
    public class Attachment
    {
        internal napi.Attachment _instance;
        internal Attachment(napi.Attachment instance) { _instance = instance; }

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
        /// Save attachment as file
        /// </summary>
        /// <param name="fileName"></param>
        public void SaveDataToFile(string fileName)
            => _instance.SaveDataToFile(fileName);

        /// <summary>
        /// MIME type of the attachment
        /// </summary>
        public string MimeType // r/w
        {
            get => _instance.MimeType;
            set => _instance.MimeType = value;
        }
    }
}
