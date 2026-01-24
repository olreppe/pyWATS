extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Linq;
using System.Collections.Generic;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A unit under repair report (UUR)
    /// </summary>
    public class UURReport : Report
    {
        internal napi.UURReport _instance;
        internal UURReport(napi.UURReport instance) : base(instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Comment on repair
        /// </summary>
        public string Comment
        {
            get => _instance.Comment;
            set => _instance.Comment = value;
        }

        /// <summary>
        /// Referenced UUT Guid
        /// </summary>
        public Guid UUTGuid
        {
            get => _instance.UUTGuid;
            set => _instance.UUTGuid = value;
        }

        /// <summary>
        /// The test report operation type, e.g. PCBA test, Calibration, Final Function etc.
        /// </summary>
        public OperationType OperationType
        {
            get { return new OperationType(_instance.OperationType); }
            set { _instance.OperationType = value._instance; }
        }

        /// <summary>
        /// Repair type
        /// </summary>
        public RepairType RepairTypeSelected
        {
            get { return new RepairType(_instance.RepairTypeSelected); }
            //internal set { _instance.RepairTypeSelected = value._instance; }
        }

        /// <summary>
        /// Name of the operator that performed the repair
        /// </summary>
        public string Operator
        {
            get => _instance.Operator;
            set => _instance.Operator = value;
        }

        /// <summary>
        /// Returns array of registered sub-parts
        /// </summary>
        public UURPartInfo[] PartInfo // r/o
        {
            get => _instance.PartInfo.Select(pi => new UURPartInfo(pi)).ToArray();
            //set => _instance.PartInfo = value.Select(pi => pi._instance).ToArray();
        }

        /// <summary>
        /// UUR was finalize date time (UTC)
        /// Is not currently displayed in the UUR report.
        /// </summary>
        public DateTime Confirmed
        {
            get => _instance.Confirmed;
            set => _instance.Confirmed = value;
        }

        /// <summary>
        /// UUR was finalize date time (UTC)
        /// </summary>
        public DateTime Finalized
        {
            get => _instance.Finalized;
            set => _instance.Finalized = value;
        }

        /// <summary>
        /// Time spent on UUR report (seconds)
        /// </summary>
        public double ExecutionTime
        {
            get => _instance.ExecutionTime;
            set => _instance.ExecutionTime = value;
        }

        /// <summary>
        /// Get the root list of failcodes for this repairtype
        /// </summary>
        /// <returns></returns>
        public FailCode[] GetRootFailcodes()
            => _instance.GetRootFailcodes().Select(fc => new FailCode(fc)).ToArray();

        /// <summary>
        /// Get the list of failcodes that belongs to a failcode
        /// </summary>
        /// <param name="failCode"></param>
        /// <returns></returns>
        public FailCode[] GetChildFailCodes(FailCode failCode)
            => _instance.GetChildFailCodes(failCode._instance).Select(fc => new FailCode(fc)).ToArray();

        /// <summary>
        /// Get a Failcode given its id
        /// </summary>
        /// <param name="failCodeId"></param>
        /// <returns></returns>
        public FailCode GetFailCode(Guid failCodeId)
            => new FailCode(_instance.GetFailCode(failCodeId));

        /// <summary>
        /// Adds an UUR sub-unit
        /// </summary>
        /// <param name="partNumber"></param>
        /// <param name="partSerialNumber"></param>
        /// <param name="partRevisionNumber"></param>
        /// <returns></returns>
        public UURPartInfo AddUURPartInfo(string partNumber, string partSerialNumber, string partRevisionNumber)
            => new UURPartInfo(_instance.AddUURPartInfo(partNumber, partSerialNumber, PartRevisionNumber));

        /// <summary>
        /// Adds a failure to the repaired unit
        /// </summary>
        /// <param name="failCode"></param>
        /// <param name="componentReference"></param>
        /// <param name="comment"></param>
        /// <param name="stepOrderNumber"></param>
        public Failure AddFailure(FailCode failCode, string componentReference, string comment, int stepOrderNumber)
            => new Failure(_instance.AddFailure(failCode._instance, componentReference, comment, stepOrderNumber));

        /// <summary>
        /// Returns array of failures belonging to main unit
        /// </summary>
        public Failure[] Failures // r/o
        {
            get => _instance.Failures.Select(f => new Failure(f)).ToArray();
            //set => _instance.Failures = value.Select(i => i._instance).ToArray();
        }

        /// <summary>
        /// Colletion of valid MiscInfo fields for the selected repair type
        /// </summary>
        public IEnumerable<MiscUURInfo> MiscInfo // r/o
        {
            get => _instance.MiscInfo.Select(mi => new MiscUURInfo(mi));
            //set => _instance.MiscInfo = value._instance.Select(mi => mi._instance);
        }

        /// <summary>
        /// Misc repair information
        /// </summary>

        public MiscUURInfo[] MiscUURInfo // r/o
        {
            get => _instance.MiscUURInfo.Select(mi => new MiscUURInfo(mi)).ToArray();
            //set => _instance.MiscUURInfo = value.Select(mi => mi._instance).ToArray();
        }

        /// <summary>
        /// Adds attachment (image) to this UUR
        /// </summary>
        /// <param name="image"></param>
        /// <param name="fileName"></param>
        /// <param name="contentType">Mime type</param>
        [Obsolete("Use AttachByteArray instead.")]
        public void AddAttachment(byte[] image, string fileName, string contentType)
            => _instance.AddAttachment(image, fileName, contentType);

        /// <summary>
        /// Attaches a file to the repair report.
        /// </summary>
        /// <param name="fileName">Full path and name of file</param>
        /// <param name="deleteAfterAttach">If true, the file is deleted after being attached</param>
        /// <returns></returns>
        public UURAttachment AttachFile(string fileName, bool deleteAfterAttach)
            => new UURAttachment(_instance.AttachFile(fileName, deleteAfterAttach));

        /// <summary>
        /// Attaches a byte array to the repair report.
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
