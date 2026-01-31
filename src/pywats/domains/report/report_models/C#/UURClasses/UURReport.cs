using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;
using System.IO;
//using Virinco.WATS.Schemas.WSXF;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A unit under repair report (UUR)
    /// </summary>
    public class UURReport : Report
    {

        internal UUR_type uurHeader;
        //private FailCodes failCodes;

        internal UURReport(TDM apiRef, RepairType repairType, UUTReport uutReport, OperationType operationType, string operatorName) : base(apiRef, true)
        {
            //Trace.WriteLine("UURReport Constructor");
            //reportRow.Item_type = (short)Transfer.TransferItemType.RepairReport;
            //reportRow.Operation = repairType.Id;// operationType.Id;
            //api = apiRef;

            reportRow.type = ReportType.UUR;
            reportRow.Process = new Process_type() { Code = repairType.Code, CodeSpecified = true };
            RepairTypeSelected = repairType;
            uurHeader = new UUR_type()
            {
                Process = new Process_type() { Code = short.Parse(operationType.Code), CodeSpecified = true },
                UserLoginName = api.SetPropertyValidated<UUR_type>("UserLoginName", operatorName, "OperatorName"),
                Active = true,
                ActiveSpecified = true
            };
            reportRow.Item = uurHeader;
            //Prepare miscUURInfo objects from MiscInfo definition (meta)
            MiscInfo = new MiscUURInfoColletion(repairType.repairtype.MiscInfos.Select(mi => new MiscUURInfo(mi, null, this)));
            //Main unit should always have a PartInfo with index 0 which should be the same as the UUTReport attributes
            var MainPi = new ReportUnitHierarchy_type()
            {
                    PN = this.PartNumber,
                    SN = this.SerialNumber,
                    Rev = this.PartRevisionNumber,
                    Idx = 0,
                    IdxSpecified = true
            };
            reportRow.Items.Add(MainPi);
        }

        internal UURReport(TDM apiRef, WATSReport wr) 
            : base(apiRef, wr)
        {
            RepairType repairType;

            if(wr.Process.CodeSpecified)
            {
                repairType = apiRef.GetRepairTypes().Where(rt => rt.Code == wr.Process.Code).Single();
            }
            else if (wr.Process.Name != null)
            {
                repairType = apiRef.GetRepairTypes().Where(rt => rt.Name == wr.Process.Name).Single();
            }
            else
            {
                throw new ArgumentException("Neither process code nor process name is defined in report");
            }

            RepairTypeSelected = repairType;

            var existingMiscInfos = wr.Items.OfType<Schemas.WRML.MiscInfo_type>();
            MiscInfo = new MiscUURInfoColletion(repairType.repairtype.MiscInfos.Select(mi => new MiscUURInfo(mi, existingMiscInfos.SingleOrDefault(m => Guid.Parse(m.Id) == mi.GUID), this)));

            failures = wr.Items.OfType<Failures_type>().Select(f => new Failure(this, f)).ToList();

            uurHeader = (UUR_type)wr.Item;
        }

        /// <summary>
        /// Comment on repair
        /// </summary>
        public string Comment
        {
            get { return uurHeader.Comment; }
            set { uurHeader.Comment = api.SetPropertyValidated<UUR_type>("Comment", value); }
        }

        /// <summary>
        /// Referenced UUT Guid
        /// </summary>
        public Guid UUTGuid
        {
            get
            {
                Guid guid;
                return Utilities.GuidTryParse(uurHeader.ReferencedUUT, out guid) ? guid : Guid.Empty;
            }
            set { uurHeader.ReferencedUUT = value.ToString(); }
        }

        /// <summary>
        /// The test report operation type, e.g. PCBA test, Calibration, Final Function etc.
        /// </summary>
        public OperationType OperationType
        {
            get { return api.GetOperationType(uurHeader.Process); }
            set
            {
                uurHeader.Process = new Process_type() { Code = value.process.Code, CodeSpecified = true, Guid = value.Id.ToString(), Name = value.Name };
            }
        }

        /// <summary>
        /// Repair type
        /// </summary>
        public RepairType RepairTypeSelected
        {
            get;
            internal set;
        }

        /// <summary>
        /// Name of the operator that performed the repair
        /// </summary>
        public string Operator
        {
            get { return uurHeader.UserLoginName; }
            set { uurHeader.UserLoginName = api.SetPropertyValidated<UUR_type>("UserLoginName", value, "Operator"); }
        }

        /// <summary>
        /// Returns array of registered sub-parts
        /// </summary>
        public UURPartInfo[] PartInfo
        {
            get { return reportRow.Items.OfType<ReportUnitHierarchy_type>().Select(pi => new UURPartInfo(this, pi)).ToArray(); }
        }

        /// <summary>
        /// UUR was finalize date time (UTC)
        /// Is not currently displayed in the UUR report.
        /// </summary>
        public DateTime Confirmed
        {
            get { return uurHeader.ConfirmDate; }
            set { uurHeader.ConfirmDate = value; uurHeader.ConfirmDateSpecified = true; }
        }

        /// <summary>
        /// UUR was finalize date time (UTC)
        /// </summary>
        public DateTime Finalized
        {
            get { return uurHeader.FinalizeDate; }
            set { uurHeader.FinalizeDate = value; uurHeader.FinalizeDateSpecified = true; }
        }

        /// <summary>
        /// Time spent on UUR report (seconds)
        /// </summary>
        public double ExecutionTime
        {
            get { return uurHeader.ExecutionTimeSpecified ? uurHeader.ExecutionTime : 0; }
            set { uurHeader.ExecutionTime = value; uurHeader.ExecutionTimeSpecified = true; }
        }

        /// <summary>
        /// Get the root list of failcodes for this repairtype
        /// </summary>
        /// <returns></returns>
        public FailCode[] GetRootFailcodes()
        {
            return RepairTypeSelected.repairtype.Categories.Select(fc => new FailCode(fc)).ToArray();
            //return failCodes.GetRootFailCodes(RepairTypeSelected);
        }

        /// <summary>
        /// Get the list of failcodes that belongs to a failcode
        /// </summary>
        /// <param name="failCode"></param>
        /// <returns></returns>
        public FailCode[] GetChildFailCodes(FailCode failCode)
        {
            return failCode.fc.Failcodes.Select(fc => new FailCode(fc)).ToArray();
        }

        /// <summary>
        /// Get a Failcode given its id
        /// </summary>
        /// <param name="failCodeId"></param>
        /// <returns></returns>
        public FailCode GetFailCode(Guid failCodeId)
        {
            var rt = RepairTypeSelected.repairtype;
            // Lookup Id as Category
            var fc = rt.Categories.SingleOrDefault(c => c.GUID == failCodeId);
            // Lookup Id as FailCode 
            if (fc == null)
                fc = rt.Categories.SelectMany(cat => cat.Failcodes).SingleOrDefault(cod => cod.GUID == failCodeId);
            return new FailCode(fc);
        }

        //private List<UURPartInfo> partInfo = new List<UURPartInfo>();
        /// <summary>
        /// Adds an UUR sub-unit
        /// </summary>
        /// <param name="partNumber"></param>
        /// <param name="partSerialNumber"></param>
        /// <param name="partRevisionNumber"></param>
        /// <returns></returns>
        public UURPartInfo AddUURPartInfo(string partNumber, string partSerialNumber, string partRevisionNumber)
        {
            var pi = new ReportUnitHierarchy_type()
            {
                PN = api.SetPropertyValidated<ReportUnitHierarchy_type>("PN", partNumber, "PartNumber"),
                SN = api.SetPropertyValidated<ReportUnitHierarchy_type>("SN", partSerialNumber, "SerialNumber"),
                Rev = api.SetPropertyValidated<ReportUnitHierarchy_type>("Rev", partRevisionNumber, "PartRevisionNumber"),
                Idx = this.PartInfo.Length,
                IdxSpecified = true,
                ParentIDX = 0,
                ParentIDXSpecified = true
            };
            this.reportRow.Items.Add(pi);
            return new UURPartInfo(this, pi);
        }



        int failureIndex = 0;
        /// <summary>
        /// Creates a failure on the repaired unit
        /// </summary>
        /// <param name="failCode"></param>
        /// <param name="componentReference">Reference to component</param>
        /// <param name="partIndex">Index of sub part this failure belongs to, 0 to uur</param>
        /// <exception cref="ArgumentException"></exception>
        /// <returns></returns>
        internal Failure AddFailure(FailCode failCode, string componentReference, int partIndex)
        {
            // Find FailCode's parent Category
            var category = RepairTypeSelected.repairtype.Categories.Where(cat => cat.Failcodes.Any(fc => fc.GUID == failCode.Id)).SingleOrDefault();
            if (category == null) //Check if failcode is found
                throw new ArgumentException("There was an error with the failcode. The provided failcode is not valid: " + failCode.Id);
            var fail = new Failures_type()
            {
                Failcode = failCode.Id.ToString(),
                PartIdx = partIndex,
                CompRef = api.SetPropertyValidated<Failures_type>("CompRef", componentReference, "ComponentReference"),
                Code = failCode.Description,
                Category = category.Description,
                Idx = failureIndex,
            };
            failureIndex++;
            this.reportRow.Items.Add(fail);
            return new Failure(this, fail);
        }


        private List<Failure> failures = new List<Failure>();
        /// <summary>
        /// Adds a failure to the repaired unit
        /// </summary>
        /// <param name="failCode"></param>
        /// <param name="componentReference"></param>
        /// <param name="comment"></param>
        /// <param name="stepOrderNumber"></param>
        public Failure AddFailure(FailCode failCode, string componentReference, string comment, int stepOrderNumber)
        {
            Failure f = AddFailure(failCode, componentReference, 0);
            f.ComponentReference = componentReference;
            f.Comment = comment;
            f.FailedStepOrderNumber = stepOrderNumber;
            failures.Add(f);
            return f;
        }


        /// <summary>
        /// Returns array of failures belonging to main unit
        /// </summary>
        public Failure[] Failures
        {
            get { return failures.ToArray<Failure>(); }
        }

        /// <summary>
        /// Colletion of valid MiscInfo fields for the selected repair type
        /// </summary>
        public MiscUURInfoColletion MiscInfo { get; private set; }
        /// <summary>
        /// Misc repair information
        /// </summary>

        public MiscUURInfo[] MiscUURInfo
        {
            get
            {
                return MiscInfo.ToArray();
            }
            internal set
            {
                MiscInfo = new MiscUURInfoColletion(value);
            }

        }

        internal Models.MiscInfo GetMiscInfoType(string MiscInfoTypeId)
        {
            return api.GetUURMiscInfo(this.reportRow.Process.Code, MiscInfoTypeId);
        }

        /// <summary>
        /// Adds attachment (image) to this UUR
        /// </summary>
        /// <param name="image"></param>
        /// <param name="fileName"></param>
        /// <param name="contentType">Mime type</param>
        [Obsolete("Use AttachByteArray instead.")]
        public void AddAttachment(byte[] image, string fileName, string contentType)
        {
            Binary_type attachment = new Binary_type();
            attachment.Data = new Binary_typeData()
            {
                Value = image,
                ContentType = api.SetPropertyValidated<Binary_typeData>("ContentType", contentType),
                FileName = fileName,
                size = image.Length,
                sizeSpecified = true,
                BinaryDataGUID = Guid.NewGuid().ToString()
            };
            reportRow.Items.Add(attachment);
        }

        /// <summary>
        /// Attaches a file to the repair report.
        /// </summary>
        /// <param name="fileName">Full path and name of file</param>
        /// <param name="deleteAfterAttach">If true, the file is deleted after being attached</param>
        /// <returns></returns>
        public UURAttachment AttachFile(string fileName, bool deleteAfterAttach)
        {
            var attachment = new UURAttachment(this, reportRow, null, fileName, deleteAfterAttach);
            return attachment;
        }

        /// <summary>
        /// Attaches a byte array to the repair report.
        /// </summary>
        /// <param name="label">Will be showed in WATS as a label to the attachment</param>
        /// <param name="content">Byte array (binary data) to be attached</param>
        /// <param name="mimeType">Will decide how the browser opens the attachement. see: http://en.wikipedia.org/wiki/Internet_media_type for details
        /// <para>If blank, mimeType application/octet-stream will be used</para></param>
        /// <returns></returns>
        public UURAttachment AttachByteArray(string label, byte[] content, string mimeType)
        {
            var attachment = new UURAttachment(this, reportRow, null, label, content, mimeType);
            return attachment;
        }

        /// <summary>
        /// Get files attached to this failure.
        /// </summary>
        public UURAttachment[] Attachments
        {
            get => reportRow.Items.OfType<Binary_type>()
                .Where(b => !b.FailIdxSpecified)
                .Select(b => new UURAttachment(this, reportRow, b))
                .ToArray();
        }
    }
}
