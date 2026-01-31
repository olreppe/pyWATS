using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using Microsoft.Win32;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// An attachment (file) to a UUR report or failure
    /// </summary>
    public class UURAttachment
    {
        private Binary_type row;

        internal UURAttachment(UURReport uur, WATSReport reportRow, Failures_type failure, string fileName, bool deleteAfterAttachment)
        {
            if (!File.Exists(fileName))
            {
                throw new ApplicationException("Error in Attachment. The specified file " + fileName + " does not exist");
            }

            var maxFileSize = uur.api.proxy.MaxAttachmentFileSize;
            var fileInfo = new FileInfo(fileName);
            if (fileInfo.Length > maxFileSize)
            {
                throw new ApplicationException($"Error in Attachment. The specified file {fileName} is too large ({fileInfo.Length} bytes). Maximum is {maxFileSize} bytes");
            }

            row = new Binary_type()
            {
                Data = new Binary_typeData
                {
                    Value = new byte[(int)fileInfo.Length],
                    ContentType = GetMimeType(fileInfo),
                    FileName = fileInfo.Name,
                    size = (int)fileInfo.Length,
                    sizeSpecified = true,
                    BinaryDataGUID = Guid.NewGuid().ToString()
                },
                FailIdx = failure?.Idx ?? 0,
                FailIdxSpecified = failure != null
            };

            FileStream stream = null;
            try
            {
                stream = fileInfo.OpenRead();
                stream.Read(row.Data.Value, 0, (int)fileInfo.Length);
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error reading attachment " + fileName + ".", ex);
            }
            finally
            {
                if (stream != null) 
                    stream.Close();
            }

            reportRow.Items.Add(row);

            if (deleteAfterAttachment)
            {
                try
                {
                    fileInfo.Delete();
                }
                catch (Exception ex)
                {
                    throw new ApplicationException("Error deleting attachment " + fileName + ".", ex);
                }
            }
        }

        internal UURAttachment(UURReport uur, WATSReport reportRow, Failures_type failure, string label, byte[] attachment, string mimeType)
        {
            if (mimeType.Length == 0)
                mimeType = "application/octet-stream";

            row = new Binary_type()
            {
                Data = new Binary_typeData
                {
                    Value = attachment,
                    ContentType = mimeType,
                    FileName = label,
                    size = attachment.Length,
                    sizeSpecified = true,
                    BinaryDataGUID = Guid.NewGuid().ToString()
                },
                FailIdx = failure?.Idx ?? 0,
                FailIdxSpecified = failure != null
            };

            reportRow.Items.Add(row);
        }

        internal UURAttachment(UURReport report, WATSReport reportRow, Binary_type row)
        {
            this.row = row;
        }

        /// <summary>
        /// Original filename (if set)
        /// </summary>
        public string FileName => row.Data.FileName;

        /// <summary>
        /// Returns attachment data as byte array
        /// </summary>
        public byte[] Data => row.Data.Value;

        /// <summary>
        /// MIME type of the attachment
        /// </summary>
        public string MimeType
        {
            get => row.Data.ContentType;
            set => row.Data.ContentType = value;            
        }

        private string GetMimeType(FileInfo fileInfo)
        {
            string mimeType = "application/octet-stream";

            RegistryKey regKey = Microsoft.Win32.Registry.ClassesRoot.OpenSubKey(
                fileInfo.Extension.ToLower()
                );

            if (regKey != null)
            {
                object contentType = regKey.GetValue("Content Type");

                if (contentType != null)
                    mimeType = contentType.ToString();
            }

            return mimeType;
        }        
    }
}
