extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// This class represent a failure found and can be connected to an UUR report or a UURPartInfo (subpart)
    /// </summary>
    public class Failure
    {
        internal napi.Failure _instance;
        internal Failure(napi.Failure instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Reference to failed component; e.g. R12
        /// </summary>
        public string ComponentReference
        {
            get => _instance.ComponentReference;
            set => _instance.ComponentReference = value;
        }


        /// <summary>
        /// Comment to the failure
        /// </summary>
        public string Comment
        {
            get => _instance.Comment;
            set => _instance.Comment = value;
        }

        /// <summary>
        /// A valid fail code
        /// </summary>
        public FailCode FailCode
        {
            get => new FailCode(_instance.FailCode);
            set => _instance.FailCode = value._instance;
        }

        /// <summary>
        /// It is possible to link the failure to the UUT test step. Put UUT step order in here.
        /// </summary>
        public int FailedStepOrderNumber
        {
            get => _instance.FailedStepOrderNumber;
            set => _instance.FailedStepOrderNumber = value;
        }

        internal int PartIndex
        {
            get => _instance.FailedStepOrderNumber;
            set => _instance.FailedStepOrderNumber = value;
        }


        /// <summary>
        /// Article number of a component
        /// </summary>
        public string ComprefArticleNumber
        {
            get => _instance.ComprefArticleNumber;
            set => _instance.ComprefArticleNumber = value;
        }

        /// <summary>
        /// Article revision of a component
        /// </summary>
        public string ComprefArticleRevision
        {
            get => _instance.ComponentReference;
            set => _instance.ComponentReference = value;
        }

        /// <summary>
        /// Component reference article description
        /// </summary>
        public string ComprefArticleDescription
        {
            get => _instance.ComprefArticleDescription;
            set => _instance.ComprefArticleDescription = value;
        }


        /// <summary>
        /// Component vendor
        /// </summary>
        public string ComprefArticleVendor
        {
            get => _instance.ComprefArticleVendor;
            set => _instance.ComprefArticleVendor = value;
        }

        /// <summary>
        /// Component functional block (area)
        /// </summary>
        public string ComprefFunctionBlock
        {
            get => _instance.ComprefFunctionBlock;
            set => _instance.ComprefFunctionBlock = value;
        }


        /// <summary>
        /// Adds a picture to a failure
        /// </summary>
        /// <param name="image">Byte array with pickture</param>
        /// <param name="contentType">Mime type of attached picture</param>
        /// <param name="fileName">Filename of picture</param>
        [Obsolete("Use AttachByteArray instead.")]
        public void AddAttachment(byte[] image, string fileName, string contentType)
            => _instance.AddAttachment(image, fileName, contentType);

        /// <summary>
        /// Attaches a file to the failure.
        /// </summary>
        /// <param name="fileName">Full path and name of file</param>
        /// <param name="deleteAfterAttach">If true, the file is deleted after being attached</param>
        /// <returns></returns>
        public UURAttachment AttachFile(string fileName, bool deleteAfterAttach)
            => new UURAttachment(_instance.AttachFile(fileName, deleteAfterAttach));

        /// <summary>
        /// Attaches a byte array to the failure.
        /// </summary>
        /// <param name="label">Will be showed in WATS as a label to the attachment</param>
        /// <param name="content">Byte array (binary data) to be attached</param>
        /// <param name="mimeType">Will decide how the browser opens the attachement. see: http://en.wikipedia.org/wiki/Internet_media_type for details
        /// <para>If blank, mimeType application/octet-stream will be used</para></param>
        /// <returns></returns>
        public UURAttachment AttachByteArray(string label, byte[] content, string mimeType)
            => new UURAttachment(_instance.AttachByteArray(label, content, mimeType));

        /// <summary>
        /// Get files attached to this failure.
        /// </summary>
        public UURAttachment[] Attachments // r/o
        {
            get => _instance.Attachments.Select(a => new UURAttachment(a)).ToArray();
            //set => _instance.Attachments = value.Select(a => a._instance).ToArray();
        }
    }
}
