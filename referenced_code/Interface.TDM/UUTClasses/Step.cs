extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;

namespace Virinco.WATS.Interface
{
    /// <summary> 
    /// Steps are the content of a UUT report. WATS support 
    /// </summary>
    public class Step
    {
        internal napi.Step _baseinstance;
        internal Step(napi.Step instance) { _baseinstance = instance; }

        /// <summary>
        /// Set/Get unique identifier of a step (Teststand TSGuid, optional)
        /// </summary>
        public string StepGuid
        {
            get => _baseinstance.StepGuid;
            set => _baseinstance.StepGuid = value;
        }

        /// <summary>
        /// Parent Step
        /// </summary>
        public SequenceCall Parent // r/o
        {
            get => new SequenceCall(_baseinstance.Parent);
            //set => _baseinstance.Parent = value;
        }

        /// <summary>
        /// Returns full path of a step. The path is built from names of all parent steps separated by /. Main Sequence Callback is omitted
        /// </summary>
        public string StepPath // r/o
        {
            get => _baseinstance.StepPath;
            //set => _baseinstance.StepPath = value;
        }

        /// <summary>
        /// Returns step type
        /// </summary>
        public string StepType
        {
            get => _baseinstance.StepType;
            set => _baseinstance.StepType = value;
        }

        /// <summary>
        /// Global step order number
        /// </summary>
        public int StepOrderNumber // r/o
        {
            get => _baseinstance.StepOrderNumber;
            //set => _baseinstance.StepOrderNumber = value;
        }

        /// <summary>
        /// Step position within a sequence
        /// </summary>
        public short StepIndex
        {
            get => _baseinstance.StepIndex;
            set => _baseinstance.StepIndex = value;
        }

        /// <summary>
        /// Name of step
        /// </summary>
        public string Name
        {
            get => _baseinstance.Name;
            set => _baseinstance.Name = value;
        }

        /// <summary>
        /// Normally, a failed step will propagate up to parent step. To prevent this, set this property to false
        /// </summary>
        public bool FailParentOnFail
        {
            get => _baseinstance.FailParentOnFail;
            set => _baseinstance.FailParentOnFail = value;
        }

        /// <summary>
        /// Indicates that this step caused the sequence to fail.
        /// </summary>
        public bool CausedSequenceFailure
        {
            get => _baseinstance.CausedSequenceFailure;
            set => _baseinstance.CausedSequenceFailure = value;
        }

        /// <summary>
        /// Step status
        /// </summary>
        public virtual StepStatusType Status

        {
            get { return (StepStatusType)(int)_baseinstance.Status; }
            set { _baseinstance.Status = (napi.StepStatusType)(int)value; }
        }

        /// <summary>
        /// Step status
        /// </summary>
        public string StatusText // r/o
        {
            get => _baseinstance.StatusText;
            //set => _baseinstance.StatusText = value;
        }

        /// <summary>
        /// Report text
        /// </summary>
        public string ReportText
        {
            get => _baseinstance.ReportText;
            set => _baseinstance.ReportText = value;
        }

        /// <summary>
        /// Step execution time (in seconds)
        /// </summary>
        public double StepTime
        {
            get => _baseinstance.StepTime;
            set => _baseinstance.StepTime = value;
        }

        /// <summary>
        /// The number format for the step execution time. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string StepTimeFormat
        {
            get => _baseinstance.StepTimeFormat;
            set => _baseinstance.StepTimeFormat = value;
        }

        /// <summary>
        /// Step module-execution time (in seconds)
        /// </summary>
        public double ModuleTime
        {
            get => _baseinstance.ModuleTime;
            set => _baseinstance.ModuleTime = value;
        }

        /// <summary>
        /// The number format for the step module-execution time. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ModuleTimeFormat
        {
            get => _baseinstance.ModuleTimeFormat;
            set => _baseinstance.ModuleTimeFormat = value;
        }

        /// <summary>
        /// Step’s start date/time
        /// </summary>
        public DateTime StartDateTime
        {
            get => _baseinstance.StartDateTime;
            set => _baseinstance.StartDateTime = value;
        }

        /// <summary>
        /// Main step group (Setup, Main, Cleanup)
        /// </summary>
        public StepGroupEnum StepGroup
        {
            get { return (StepGroupEnum)(int)_baseinstance.StepGroup; }
            set { _baseinstance.StepGroup = (napi.StepGroupEnum)(int)value; }
        }

        /// <summary>
        /// Error message connected to step
        /// </summary>
        public string StepErrorMessage
        {
            get => _baseinstance.StepErrorMessage;
            set => _baseinstance.StepErrorMessage = value;
        }

        /// <summary>
        /// Error code connected to step
        /// </summary>
        public int StepErrorCode
        {
            get => _baseinstance.StepErrorCode;
            set => _baseinstance.StepErrorCode = value;
        }

        /// <summary>
        /// The number format for the step error code. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string StepErrorCodeFormat
        {
            get => _baseinstance.StepErrorCodeFormat;
            set => _baseinstance.StepErrorCodeFormat = value;
        }

        /// <summary>
        /// Adds a chart to a step
        /// </summary>
        /// <param name="chartType">Linear or logaritmic can be selected</param>
        /// <param name="chartLabel">Chart label</param>
        /// <param name="xLabel">X-Label</param>
        /// <param name="xUnit">X-Unit</param>
        /// <param name="yLabel">Y-Label</param>
        /// <param name="yUnit">Y-Unit</param>
        /// <returns></returns>
        public Chart AddChart(ChartType chartType, string chartLabel, string xLabel, string xUnit, string yLabel, string yUnit)
            => new Chart(_baseinstance.AddChart((napi.ChartType)(int)chartType, chartLabel, xLabel, xUnit, yLabel, yUnit));

        /// <summary>
        /// Get chart if present
        /// </summary>
        public Chart Chart // r/o
        {
            get => new Chart(_baseinstance.Chart);
            //set => _baseinstance.Chart = value._instance;
        }

        /// <summary>
        /// Attaches a file to a step.
        /// </summary>
        /// <remarks>File size is limited to 100KB</remarks>
        /// <param name="fileName">Full path and name of file</param>
        /// <param name="deleteAfterAttach">If true, the file is deleted after being attached</param>
        /// <returns></returns>
        public Attachment AttachFile(string fileName, bool deleteAfterAttach)
            => new Attachment(_baseinstance.AttachFile(fileName, deleteAfterAttach));

        /// <summary>
        /// Gets an attachment
        /// </summary>
        public Attachment Attachment
        {
            get => new Attachment(_baseinstance.Attachment);
            //set => _baseinstance.Attachment = value;
        }

        /// <summary>
        /// Reserved for use with TestStand. Does not show up in analysis.
        /// An additional result can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
        /// </summary>
        /// <param name="Name"></param>
        /// <param name="contents"></param>
        /// <returns></returns>
        public AdditionalResult AddAdditionalResult(string Name, System.Xml.Linq.XElement contents)
            => new AdditionalResult(_baseinstance.AddAdditionalResult(Name, contents));

        public AdditionalResult AdditionalResult // r/o
        {
            get => new AdditionalResult(_baseinstance.AdditionalResult);
            //set => _baseinstance.AdditionalResult = value._instance;
        }

        /// <summary>
        /// Attaches a byte array to a step
        /// </summary>
        /// <remarks>File size is limited to 100KB</remarks>
        /// <param name="label">Will be showed in WATS as a label to the attachment</param>
        /// <param name="content">Byte array (binary data) to be attached</param>
        /// <param name="mimeType">Will decide how the browser opens the attachement. see: http://en.wikipedia.org/wiki/Internet_media_type for details
        /// <para>If blank, mimeType application/octet-stream will be used</para></param>
        /// <returns></returns>
        public Attachment AttachByteArray(string label, byte[] content, string mimeType)
            => new Attachment(_baseinstance.AttachByteArray(label, content, mimeType));

        /// <summary>
        /// Get/Set loop index of the step
        /// </summary>
        public short LoopIndex
        {
            get => _baseinstance.LoopIndex;
            set => _baseinstance.LoopIndex = value;
        }
    }
}