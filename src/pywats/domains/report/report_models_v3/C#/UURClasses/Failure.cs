using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// This class represent a failure found and can be connected to an UUR report or a UURPartInfo (subpart)
    /// </summary>
    public class Failure
    {
        private Failures_type failRow;
        private UURReport uur;
        internal Failure(UURReport uurReport, Failures_type f)
        {
            uur = uurReport;
            failRow = f;
        }

        /// <summary>
        /// Reference to failed component; e.g. R12
        /// </summary>
        public string ComponentReference
        {
            get {return failRow.CompRef;}
            set {failRow.CompRef = uur.api.SetPropertyValidated<Failures_type>("CompRef",value,"ComponentReference");}
        }


        /// <summary>
        /// Comment to the failure
        /// </summary>
        public string Comment
        {
            // Comment incorrectly defined as list of strings (max=unbounded...)
            // TBD: Change WRML Definition, or keep this workaround ???
            get { return failRow.Comment.Aggregate((ag, c) => ag + "\n" + c); }
            set { failRow.Comment.Clear(); failRow.Comment.Add(uur.api.SetPropertyValidated<Failures_type>("Comment", value));}
        }

        /// <summary>
        /// A valid fail code
        /// </summary>
        public FailCode FailCode
        {
            get { return uur.GetFailCode(new Guid(failRow.Failcode)); }
            set { failRow.Failcode = value.Id.ToString(); }
        }

        /// <summary>
        /// It is possible to link the failure to the UUT test step. Put UUT step order in here.
        /// </summary>
        public int FailedStepOrderNumber
        {
            get { return failRow.StepID; }
            set { failRow.StepID = value; }
        }

        internal int PartIndex
        {
            get { return failRow.PartIdx; }
            set { failRow.PartIdx = value; }
        }


        /// <summary>
        /// Article number of a component
        /// </summary>
        public string ComprefArticleNumber
        {
            get { return failRow.ArticleNumber; }
            set { failRow.ArticleNumber= uur.api.SetPropertyValidated<Failures_type>("ArticleNumber", value, "ComprefArticleNumber"); }
        }

        /// <summary>
        /// Article revision of a component
        /// </summary>
        public string ComprefArticleRevision
        {
            get { return failRow.ArticleRevision; }
            set { failRow.ArticleRevision = uur.api.SetPropertyValidated<Failures_type>("ArticleRevision", value, "ComprefArticleRevision"); }
        }

        /// <summary>
        /// Component reference article description
        /// </summary>
        public string ComprefArticleDescription
        {
            get { return failRow.ArticleDescription; }
            set { failRow.ArticleDescription = uur.api.SetPropertyValidated<Failures_type>(nameof(Failures_type.ArticleDescription), value, nameof(ComprefArticleDescription)); }
        }


        /// <summary>
        /// Component vendor
        /// </summary>
        public string ComprefArticleVendor
        {
            get { return failRow.ArticleVendor; }
            set { failRow.ArticleVendor = uur.api.SetPropertyValidated<Failures_type>("ArticleVendor", value, "ComprefArticleVendor"); }
        }

        /// <summary>
        /// Component functional block (area)
        /// </summary>
        public string ComprefFunctionBlock
        {
            get { return failRow.FunctionBlock;}
            set { failRow.FunctionBlock = uur.api.SetPropertyValidated<Failures_type>("FunctionBlock", value, "ComprefFunctionBlock"); }
        }


        /// <summary>
        /// Adds a picture to a failure
        /// </summary>
        /// <param name="image">Byte array with pickture</param>
        /// <param name="contentType">Mime type of attached picture</param>
        /// <param name="fileName">Filename of picture</param>
        [Obsolete("Use AttachByteArray instead.")]
        public void AddAttachment(byte[] image, string fileName, string contentType)
        {
            Binary_type attachment = new Binary_type()
            {
                FailIdx = this.failRow.Idx, FailIdxSpecified = true
            };

            attachment.Data = new Binary_typeData()
            {
                Value = image,
                ContentType = contentType,
                FileName = fileName,
                size = image.Length,
                sizeSpecified = true,
                BinaryDataGUID = Guid.NewGuid().ToString()
            };

            uur.reportRow.Items.Add(attachment);
        }

        /// <summary>
        /// Attaches a file to the failure.
        /// </summary>
        /// <param name="fileName">Full path and name of file</param>
        /// <param name="deleteAfterAttach">If true, the file is deleted after being attached</param>
        /// <returns></returns>
        public UURAttachment AttachFile(string fileName, bool deleteAfterAttach)
        {
            var attachment = new UURAttachment(uur, uur.reportRow, failRow, fileName, deleteAfterAttach);
            return attachment;
        }

        /// <summary>
        /// Attaches a byte array to the failure.
        /// </summary>
        /// <param name="label">Will be showed in WATS as a label to the attachment</param>
        /// <param name="content">Byte array (binary data) to be attached</param>
        /// <param name="mimeType">Will decide how the browser opens the attachement. see: http://en.wikipedia.org/wiki/Internet_media_type for details
        /// <para>If blank, mimeType application/octet-stream will be used</para></param>
        /// <returns></returns>
        public UURAttachment AttachByteArray(string label, byte[] content, string mimeType)
        {
            var attachment = new UURAttachment(uur, uur.reportRow, failRow, label, content, mimeType);
            return attachment;
        }

        /// <summary>
        /// Get files attached to this failure.
        /// </summary>
        public UURAttachment[] Attachments
        {
            get => uur.reportRow.Items.OfType<Binary_type>()
                .Where(b => b.FailIdxSpecified && b.FailIdx == failRow.Idx)
                .Select(b => new UURAttachment(uur, uur.reportRow, b))
                .ToArray();
        }
    }
}
