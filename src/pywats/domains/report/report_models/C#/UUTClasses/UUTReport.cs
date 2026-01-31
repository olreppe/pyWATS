using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A unit under test report (UUT) contains calls and datastructures to build up a test report you can submit to WATS
    /// use <see cref="TDM.CreateUUTReport(string, string, string, string, OperationType, string, string)"/> to create an instance.
    /// </summary>
    public class UUTReport : Report
    {
        /// <summary>
        /// Internal data
        /// </summary>
        protected internal UUT_type uutHeaderRow;
        private SequenceCall rootSequenceCall;

        /// <summary>
        /// Internal data
        /// </summary>
        protected internal int currentStepOrder = 1;

        /// <summary>
        /// Internal data
        /// </summary>
        protected internal short currentMeasOrder = -1;


        /// <summary>
        /// Internal constructor, prepares the dataset
        /// </summary>
        /// <param name="apiRef"></param>
        /// <param name="operatorName"></param>
        /// <param name="sequenceName"></param>
        /// <param name="sequenceVersion"></param>
        internal UUTReport(TDM apiRef, string operatorName, string sequenceName, string sequenceVersion)
            : base(apiRef, true)
        {
            //Trace.WriteLine("UUTReport Constructor");
            InitializeUutHeader(operatorName, sequenceName, sequenceVersion, true);
        }


        /// <summary>
        /// Returns steps matching step name and / or step path.
        /// Note: StepPath will correspond to a SequenceCall name (nested levels allowed)
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="stepPath">Step path</param>
        /// <returns></returns>
        public Step[] FindSteps(string stepName, string stepPath)
        {
            var query = AllSteps.AsEnumerable();

            if (!string.IsNullOrEmpty(stepPath))
            {
                if (!stepPath.StartsWith("/"))
                    stepPath = "/" + stepPath;
                if (!stepPath.EndsWith("/"))
                    stepPath += "/";

                query = query.Where(s => string.Equals(s.StepPath, stepPath, StringComparison.OrdinalIgnoreCase));
            }
            
            if (!string.IsNullOrEmpty(stepName))
                query = query.Where(s => string.Equals(s.Name, stepName, StringComparison.OrdinalIgnoreCase));

            return query.ToArray();
        }

        /// <summary>
        /// Gets a step given step order number
        /// </summary>
        /// <param name="stepOrderNumber"></param>
        /// <returns></returns>
        public Step GetStep(int stepOrderNumber)
        {
            return AllSteps.Where(s => s.StepOrderNumber == stepOrderNumber).First();
        }

        /// <summary>
        /// Protected constructor, intended for TestStand integration purpose. Allows dataset access through protected properties.
        /// </summary>
        /// <param name="apiRef"></param>
        /// <param name="createHeader">True if a header should be created</param>
        protected UUTReport(TDM apiRef, bool createHeader)
            : base(apiRef, createHeader)
        {
            if (apiRef.TestMode != TestModeType.TestStand) throw new NotSupportedException("Unsupported TestMode for this operation");
        }

        /// <summary>
        /// Internal function
        /// </summary>
        /// <param name="operatorName"></param>
        /// <param name="sequenceName"></param>
        /// <param name="sequenceVersion"></param>
        /// <param name="initializeRootSequence"></param>
        protected internal void InitializeUutHeader(string operatorName, string sequenceName, string sequenceVersion, bool initializeRootSequence)
        {
            reportRow.type = ReportType.UUT;
            uutHeaderRow = new UUT_type()
            {
                UserLoginName = api.SetPropertyValidated<UUT_type>("UserLoginName",operatorName,"OperatorName"),
                ExecutionTime = 0,
                ExecutionTimeSpecified = true
            };
            reportRow.Item=uutHeaderRow;
            Status = UUTStatusType.Passed;
            //Create the root step
            if (initializeRootSequence)
                rootSequenceCall = new SequenceCall(this, reportRow, null, api.RootStepName, sequenceName, sequenceVersion);
        }

        internal UUTReport(TDM apiRef, WATSReport wr)
            : base(apiRef, wr)
        {
            uutHeaderRow = (UUT_type)wr.Item;
            var rootstep = wr.Items.OfType<Step_type>().Single(s => s.ParentStepIDSpecified == false);
            var rootstep_seq = wr.Items.OfType<SequenceCall_type>().Single(sq => sq.StepID == rootstep.StepID);
            currentStepOrder = wr.Items.OfType<Step_type>().Count()+1;
            rootSequenceCall = new SequenceCall(rootstep, rootstep_seq, wr, this);
            if (string.IsNullOrEmpty(wr.Process.Guid))
            {
                OperationType operation = apiRef.GetOperationTypes().Where(ot => ot.Code == wr.Process.Code.ToString()).FirstOrDefault();
                if (operation == null) operation= apiRef.GetOperationTypes().Where(ot => ot.Name == wr.Process.Name.ToString()).FirstOrDefault();
                if (operation == null) throw new ApplicationException("Operation type invalid");
                reportRow.Process.Guid = operation.Id.ToString();
            }
        }


        #region Properties

        /// <summary>
        /// Returns an array of all steps
        /// </summary>
        public Step[] AllSteps
        {
            get
            {
                return reportRow.Items.OfType<Step_type>().Select(s => Step.Create(s,reportRow,this)).ToArray();
            }
        }


        /// <summary>
        /// Returns all steps with status is not Passed or Skipped.
        /// Includes Failed, Error and Terminated
        /// </summary>
        public Step[] FailedSteps
        {
            get
            {
                return AllSteps.Where(s => s.Status >= StepStatusType.Failed).ToArray();
            }
        }

        /// <summary>
        /// Name of operator that performs the test
        /// </summary>
        public string Operator
        {
            get { return uutHeaderRow.UserLoginName; }
            set { uutHeaderRow.UserLoginName = api.SetPropertyValidated<UUT_type>("UserLoginName",value,"Operator");}
        }

        /// <summary>
        /// Batch fail count
        /// </summary>
        public int BatchFailCount
        {
            get { return uutHeaderRow.BatchFailCount; }
            set { uutHeaderRow.BatchFailCount = value; uutHeaderRow.BatchFailCountSpecified = true; }
        }

        /// <summary>
        /// The number format for the batch fail count. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string BatchFailCountFormat
        {
            get => uutHeaderRow.BatchFailCountFormat;
            set => uutHeaderRow.BatchFailCountFormat = value;
        }

        /// <summary>
        /// Index of loop
        /// </summary>
        public int BatchLoopIndex
        {
            get { return uutHeaderRow.BatchLoopIndex; }
            set { uutHeaderRow.BatchLoopIndex = value;  uutHeaderRow.BatchLoopIndexSpecified = true; }
        }

        /// <summary>
        /// The number format for the batch loop index. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string BatchLoopIndexFormat
        {
            get => uutHeaderRow.BatchLoopIndexFormat;
            set => uutHeaderRow.BatchLoopIndexFormat = value;
        }

        /// <summary>
        /// Serial number of production batch
        /// </summary>
        public string BatchSerialNumber
        {
            get { return uutHeaderRow.BatchSN; }
            set
            {
                uutHeaderRow.BatchSN = api.SetPropertyValidated<UUT_type>("BatchSN", value, "BatchSerialNumber");
            }
        }

        /// <summary>
        /// Test socket
        /// </summary>
        public short TestSocketIndex
        {
            get { return uutHeaderRow.TestSocketIndexSpecified ? uutHeaderRow.TestSocketIndex : (short)-1; }
            set { uutHeaderRow.TestSocketIndex = value; }
        }

        /// <summary>
        /// The number format for the test socket. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string TestSocketIndexFormat
        {
            get => uutHeaderRow.TestSocketIndexFormat;
            set => uutHeaderRow.TestSocketIndexFormat = value;
        }

        /// <summary>
        /// The test report operation type, e.g. PCBA test, Calibration, Final Function etc.
        /// </summary>
        public OperationType OperationType
        {
            get { return api.GetOperationType(reportRow.Process); }
            set { reportRow.Process = api.GetProcess(value); }
        }

        /// <summary>
        /// The number format for the operation type code. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string OperationTypeCodeFormat
        {
            get => reportRow.Process.CodeFormat;
            set => reportRow.Process.CodeFormat = value;
        }

        /// <summary>
        /// Name of test program
        /// </summary>
        public string SequenceName
        {
            get { return rootSequenceCall.SequenceName; }
            set { rootSequenceCall.SequenceName = value; }
        }

        /// <summary>
        /// Version of test program, 3 or 4 part dotted
        /// </summary>
        public string SequenceVersion
        {
            get { return rootSequenceCall.SequenceVersion; }
            set { rootSequenceCall.SequenceVersion = value; }
        }

        /// <summary>
        /// UUT Result status. Must be one of the following 4 statuscodes: ‘Passed’, ‘Failed’, ‘Error’, ‘Terminated’
        /// </summary>
        public UUTStatusType Status
        {
            get
            {
                switch (reportRow.Result)
                {
                    case ReportResultType.Passed: return UUTStatusType.Passed;
                    case ReportResultType.Failed: return UUTStatusType.Failed;
                    case ReportResultType.Error: return UUTStatusType.Error;
                    case ReportResultType.Terminated: return UUTStatusType.Terminated;
                    default: throw new ArgumentOutOfRangeException("Status", reportRow.Result, "Invalid UUT Status code");
                }
            }
            set
            {
                switch (value)
                {
                    case UUTStatusType.Passed: reportRow.Result = ReportResultType.Passed; break;
                    case UUTStatusType.Failed: reportRow.Result = ReportResultType.Failed; break;
                    case UUTStatusType.Error: reportRow.Result = ReportResultType.Error; break;
                    case UUTStatusType.Terminated: reportRow.Result = ReportResultType.Terminated; break;
                    default: throw new ArgumentOutOfRangeException("Status", reportRow.Result, "Invalid UUT Status code");
                }
            }
        }

        /// <summary>
        /// Time (in seconds) for the entire execution.
        /// </summary>
        public double ExecutionTime
        {
            get { return uutHeaderRow.ExecutionTimeSpecified ? uutHeaderRow.ExecutionTime : double.NaN; }
            set { uutHeaderRow.ExecutionTime = value; uutHeaderRow.ExecutionTimeSpecified = true; }
        }

        /// <summary>
        /// The number format for the execution time. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ExecutionTimeFormat
        {
            get => uutHeaderRow.ExecutionTimeFormat;
            set => uutHeaderRow.ExecutionTimeFormat = value;
        }

        /// <summary>
        /// Test Comment
        /// </summary>
        public string Comment
        {
            get { return uutHeaderRow.Comment; }
            set { uutHeaderRow.Comment = api.SetPropertyValidated<UUT_type>("Comment",value); }
        }

        /// <summary>
        /// Identification of fixture
        /// </summary>
        public string FixtureId
        {
            get { return uutHeaderRow.FixtureId; }
            set { uutHeaderRow.FixtureId = api.SetPropertyValidated<UUT_type>("FixtureId", value); }
        }

        /// <summary>
        /// Custom error code.
        /// Use 0 for no error
        /// </summary>
        public int ErrorCode
        {
            get { return uutHeaderRow.ErrorCodeSpecified ? uutHeaderRow.ErrorCode : 0; }
            set { uutHeaderRow.ErrorCode = value; uutHeaderRow.ErrorCodeSpecified = true; }
        }

        public string ErrorCodeFormat
        {
            get => uutHeaderRow.ErrorCodeFormat;
            set => uutHeaderRow.ErrorCodeFormat = value;
        }

        /// <summary>
        /// Textual error message
        /// </summary>
        public string ErrorMessage
        {
            get { return uutHeaderRow.ErrorMessage; }
            set { uutHeaderRow.ErrorMessage = api.SetPropertyValidated<UUT_type>("ErrorMessage", value); }
        }

        private List<UUTPartInfo> partInfo = new List<UUTPartInfo>();
        /// <summary>
        /// Array of sub-parts registered (can be changed)
        /// </summary>
        public UUTPartInfo[] PartInfo
        {
            get
            {
                //TODO: Discuss this
                var partInfos1= reportRow.Items.OfType<PartInfo_type>().Select(s => new UUTPartInfo(s, this));
                var partInfos2 = reportRow.Items.OfType<ReportUnitHierarchy_type>().Select(s => new UUTPartInfo(s, this));
                return partInfos1.Union(partInfos2).ToArray();
            }
        }

        /// <summary>
        /// List of Misc. UUT info objects 
        /// </summary>
        public MiscUUTInfo[] MiscInfo
        {
            get
            {
                return reportRow.Items.OfType<MiscInfo_type>().Select(s => new MiscUUTInfo(s,this)).ToArray();
            }
        }

        /// <summary>
        /// List of used Assets 
        /// </summary>
        public Asset[] Assets
        {
            get => reportRow.Assets.Select(s => new Asset(s, this)).ToArray();
        }

        /// <summary>
        /// List of statistics for used Assets. Only available when getting the report from the server with <see cref="TDM.LoadReport"/>.
        /// </summary>
        public AssetStatistics[] AssetStatistics
        {
            get => reportRow.AssetStats.Select(s => new AssetStatistics(s, this)).ToArray();
        }

        /// <summary>
        /// The root sequence of the test
        /// </summary>
        public SequenceCall GetRootSequenceCall()
        {
            return rootSequenceCall;
        }


        #endregion Properties

        /// <summary>
        /// Used to to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Misc description</param>
        /// <returns>Empty MiscUUTInfo object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description)
        {
            if (string.IsNullOrEmpty(description))
                throw new ApplicationException("MiscInfo description cannot be blank");
            
            int mi_count = MiscInfo.Count();
            MiscInfo_type miscRow = new MiscInfo_type()
            {
                order_no = (short)mi_count,
                order_noSpecified = true,
                idx = (short)mi_count,
                idxSpecified = true,
                Typedef = ""
            };
            reportRow.Items.Add(miscRow);

            MiscUUTInfo misc = new MiscUUTInfo(miscRow,this);
            misc.Description = description;

            return misc;
        }

        /// <summary>
        /// Used to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Description of info (tag)</param>
        /// <param name="stringValue">A string value</param>
        /// <param name="numericValue">A numeric value</param>
        /// <returns>A misc info object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description, string stringValue, short numericValue)
        {
            MiscUUTInfo misc = AddMiscUUTInfo(description);
            misc.DataString = stringValue;
            misc.DataNumeric = numericValue;
            return misc;
        }

        /// <summary>
        /// Used to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Description of info (tag)</param>
        /// <param name="numericValue">A numeric value</param>
        /// <returns>A misc info object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description, short numericValue)
        {
            MiscUUTInfo misc = AddMiscUUTInfo(description);
            misc.DataNumeric = numericValue;
            return misc;
        }

        /// <summary>
        /// Used to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Description of info (tag)</param>
        /// <param name="stringValue">A string value</param>
        /// <returns>A misc info object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description, string stringValue)
        {
            MiscUUTInfo misc = AddMiscUUTInfo(description);
            misc.DataString = stringValue;
            return misc;
        }


        /// <summary>
        /// To add uut part info to the report.
        /// Example of uut part info is sub modules with part number, serial number and revision number
        /// </summary>
        /// <returns>Empty UUTPartInfo object</returns>
        public UUTPartInfo AddUUTPartInfo()
        {
            int pi_count = reportRow.Items.OfType<PartInfo_type>().Count();
            ReportUnitHierarchy_type partRow = new ReportUnitHierarchy_type()
            {
                Position = (short)pi_count,
                PositionSpecified = true
            };
            reportRow.Items.Add(partRow);
            UUTPartInfo part = new UUTPartInfo(partRow,this);
            return part;
        }

        /// <summary>
        /// To add uut part info to the report.
        /// Example of uut part info is sub modules with part number, serial number and revision number
        /// </summary>
        /// <param name="partType">Describes type of subpart</param>
        /// <param name="partNumber">Subpart’s part number</param>
        /// <param name="partSerialNumber">Subpart’s serial number</param>
        /// <param name="partRevisionNumber">Subpart’s part revision number</param>
        public UUTPartInfo AddUUTPartInfo(string partType, string partNumber, string partSerialNumber, string partRevisionNumber)
        {
            UUTPartInfo partinf = AddUUTPartInfo();
            partinf.PartType = partType;
            partinf.PartNumber = partNumber;
            partinf.SerialNumber = partSerialNumber;
            partinf.PartRevisionNumber = partRevisionNumber;
            return partinf;
        }

        public Asset AddAsset(string assetSerialNumber, int usageCount)
        {
            var asset = new Asset(this, reportRow, assetSerialNumber, usageCount);
            return asset;
        }

        /// <summary>
        /// Returns an array of step order numbers that has failed, same index as <see cref="GetFailedStepNames()"/>
        /// </summary>
        /// <returns></returns>
        public int[] GetFailedStepOrderNumbers()
        {
            return reportRow.Items.OfType<Step_type>().Where(s => s.Status == StepResultType.Failed).OrderBy(s => s.StepID).Select(s => s.StepID).ToArray();
        }

        /// <summary>
        /// Returns string array of failed steps name, same index as <see cref="GetFailedStepOrderNumbers()"/>
        /// </summary>
        /// <returns></returns>
        public string[] GetFailedStepNames()
        {
            return reportRow.Items.OfType<Step_type>().Where(s => s.Status == StepResultType.Failed).OrderBy(s => s.StepID).Select(s => s.Name).ToArray(); 
        }

        public Step GetStepCausedUUTFail()
        {
            if(uutHeaderRow.StepIdCausedUUTFailureSpecified)
                return GetStep(uutHeaderRow.StepIdCausedUUTFailure);
            return null;
        }

        /// <summary>
        /// Internal function
        /// </summary>
        /// <returns></returns>
        protected internal int GetNextStepOrder()
        {
            return currentStepOrder++;
        }

        /// <summary>
        /// Internal function MeasOrder
        /// </summary>
        /// <returns></returns>
        protected internal short GetNextMeasOrder()
        {
            return currentMeasOrder++;
        }

    }
}
