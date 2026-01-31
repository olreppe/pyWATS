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
    /// An attachment (file) to any step type can be added
    /// </summary>
    public class Attachment
    {

        //The attachment uses the chart table to transfer content
        //private WATSReport.ChartDataTable chartTable;
        private short measureIndex = 0;
        Step parent;
        UUTReport uutReport;
        WATSReport reportRow;
        

        internal Attachment(UUTReport uut, WATSReport reportRow, Step parentStep, string fileName, bool deleteAfterAttachment)
        {
            if (!File.Exists(fileName))
            {
                throw new ApplicationException("Error in Attachment. The specified file " + fileName + " does not exist");
            }

            var maxFileSize = uut.api.proxy.MaxAttachmentFileSize;
            FileInfo fileInfo = new FileInfo(fileName);
            if (fileInfo.Length > maxFileSize)
            {
                throw new ApplicationException($"Error in Attachment. The specified file {fileName} is too large ({fileInfo.Length} bytes). Maximum is {maxFileSize} bytes");
            }

            //TODO: Check if step already has attachments
            uutReport = uut;
            parent = parentStep;

            //chartTable = reportDS.Chart;
            Chart_type row1 = newChartRow();
            row1.Label = fileInfo.Name;
            row1.ChartType = "ATTACHMENT";

            Chart_type row2 = newChartRow();
            row2.PlotName = GetMimeType(fileInfo);
            row2.DataType = "ATTACHMENT";

            FileStream stream = null;
            try
            {
                stream = fileInfo.OpenRead();
                row2.Data = new byte[(int)fileInfo.Length];
                stream.Read(row2.Data, 0, (int)fileInfo.Length);
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

            reportRow.Items.Add(row1);
            reportRow.Items.Add(row2);

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

            this.reportRow = reportRow;
        }

        internal Attachment(UUTReport uut, WATSReport reportRow, Step parentStep, string label, byte[] attachment, string mimeType)
        {
            if (mimeType.Length == 0)
                mimeType = "application/octet-stream";

            uutReport = uut;
            parent = parentStep;

            Chart_type row1 = newChartRow();
            row1.Label = label;
            row1.ChartType = "ATTACHMENT";

            Chart_type row2 = newChartRow();
            row2.PlotName = mimeType;
            row2.Data = attachment;

            reportRow.Items.Add(row1);
            reportRow.Items.Add(row2);

            this.reportRow = reportRow;
        }

        internal Attachment(UUTReport report, WATSReport reportRow, Step step)
        {
            this.uutReport = report;
            this.parent = step;
            this.reportRow = reportRow;
        }

        /// <summary>
        /// Original filename (if set)
        /// </summary>
        public string FileName
        {
            get
            {
                Chart_type row1 = reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == parent.StepOrderNumber && c.idx==0).FirstOrDefault();
                if (row1 == null) return null;
                return row1.Label;
            }
        }
       

        /// <summary>
        /// Returns attachment data as byte array
        /// </summary>
        public byte[] Data
        {
            get
            {
                Chart_type row2 = reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == parent.StepOrderNumber && c.idx == 1).FirstOrDefault();
                return row2.Data;
            }
        }


        /// <summary>
        /// Save attachment as file
        /// </summary>
        /// <param name="fileName"></param>
        public void SaveDataToFile(string fileName)
        {
            File.WriteAllBytes(fileName, Data);
        }


        internal Chart_type newChartRow()
        {
            Chart_type r = new Chart_type() { StepID = parent.StepOrderNumber };
            r.idx = measureIndex;
            measureIndex++;
            r.idxSpecified = true;
            return r;
        }

        string GetMimeType(FileInfo fileInfo)
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

        /// <summary>
        /// MIME type of the attachment
        /// </summary>
        public string MimeType
        {
            get
            {
                Chart_type row2 = reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == parent.StepOrderNumber && c.idx == 1).FirstOrDefault();
                return row2.PlotName;
            }
            set
            {
                Chart_type row2 = reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == parent.StepOrderNumber && c.idx == 1).FirstOrDefault();
                row2.PlotName = value;
            }
        }
    }
}
