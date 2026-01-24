extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// A unit under test report (UUT) contains calls and datastructures to build up a test report you can submit to WATS
    /// use <see cref="TDM.CreateUUTReport(string, string, string, string, OperationType, string, string)"/> to create an instance.
    /// </summary>
    public class UUTReport : Report
    {
        internal napi.UUTReport _instance;
        internal UUTReport(napi.UUTReport instance) : base(instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Returns steps matching step name and / or step path.
        /// Note: StepPath will correspond to a SequenceCall name (nested levels allowed)
        /// </summary>
        /// <param name="stepName">Step name</param>
        /// <param name="stepPath">Step path</param>
        /// <returns></returns>
        public Step[] FindSteps(string stepName, string stepPath)
            => _instance.FindSteps(stepName, stepPath).Select(s => new Step(s)).ToArray();

        /// <summary>
        /// Gets a step given step order number
        /// </summary>
        /// <param name="stepOrderNumber"></param>
        /// <returns></returns>
        public Step GetStep(int stepOrderNumber)
            => new Step(_instance.GetStep(stepOrderNumber));

        #region Properties

        /// <summary>
        /// Returns an array of all steps
        /// </summary>
        public Step[] AllSteps // r/o
        {
            get => _instance.AllSteps.Select(s => new Step(s)).ToArray();
            //set => _instance.AllSteps = value.Select(s => s._baseinstance).ToArray();
        }

        /// <summary>
        /// Returns all steps with status is not Passed or Skipped.
        /// Includes Failed, Error and Terminated
        /// </summary>
        public Step[] FailedSteps // r/o
        {
            get => _instance.FailedSteps.Select(s => new Step(s)).ToArray();
            //set => _instance.FailedSteps = value.Select(s => s._baseinstance).ToArray();
        }

        /// <summary>
        /// Name of operator that performs the test
        /// </summary>
        public string Operator
        {
            get => _instance.Operator;
            set => _instance.Operator = value;
        }

        /// <summary>
        /// Batch fail count
        /// </summary>
        public int BatchFailCount
        {
            get => _instance.BatchFailCount;
            set => _instance.BatchFailCount = value;
        }

        /// <summary>
        /// The number format for the batch fail count. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string BatchFailCountFormat
        {
            get => _instance.BatchFailCountFormat;
            set => _instance.BatchFailCountFormat = value;
        }

        /// <summary>
        /// Index of loop
        /// </summary>
        public int BatchLoopIndex
        {
            get => _instance.BatchLoopIndex;
            set => _instance.BatchLoopIndex = value;
        }

        /// <summary>
        /// The number format for the batch loop index. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string BatchLoopIndexFormat
        {
            get => _instance.BatchLoopIndexFormat;
            set => _instance.BatchLoopIndexFormat = value;
        }

        /// <summary>
        /// Serial number of production batch
        /// </summary>
        public string BatchSerialNumber
        {
            get => _instance.BatchSerialNumber;
            set => _instance.BatchSerialNumber = value;
        }

        /// <summary>
        /// Test socket
        /// </summary>
        public short TestSocketIndex
        {
            get => _instance.TestSocketIndex;
            set => _instance.TestSocketIndex = value;
        }

        /// <summary>
        /// The number format for the test socket. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string TestSocketIndexFormat
        {
            get => _instance.TestSocketIndexFormat;
            set => _instance.TestSocketIndexFormat = value;
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
        /// The number format for the operation type code. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string OperationTypeCodeFormat
        {
            get => _instance.OperationTypeCodeFormat;
            set => _instance.OperationTypeCodeFormat = value;
        }

        /// <summary>
        /// Name of test program
        /// </summary>
        public string SequenceName
        {
            get => _instance.SequenceName;
            set => _instance.SequenceName = value;
        }

        /// <summary>
        /// Version of test program, 3 or 4 part dotted
        /// </summary>
        public string SequenceVersion
        {
            get => _instance.SequenceVersion;
            set => _instance.SequenceVersion = value;
        }

        /// <summary>
        /// UUT Result status. Must be one of the following 4 statuscodes: ‘Passed’, ‘Failed’, ‘Error’, ‘Terminated’
        /// </summary>
        public UUTStatusType Status
        {
            get { return _instance.Status.CastTo<UUTStatusType>(); }
            set { _instance.Status = value.CastTo<napi.UUTStatusType>(); }
        }

        /// <summary>
        /// Time (in seconds) for the entire execution.
        /// </summary>
        public double ExecutionTime
        {
            get => _instance.ExecutionTime;
            set => _instance.ExecutionTime = value;
        }

        /// <summary>
        /// The number format for the execution time. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ExecutionTimeFormat
        {
            get => _instance.ExecutionTimeFormat;
            set => _instance.ExecutionTimeFormat = value;
        }

        /// <summary>
        /// Test Comment
        /// </summary>
        public string Comment
        {
            get => _instance.Comment;
            set => _instance.Comment = value;
        }

        /// <summary>
        /// Identification of fixture
        /// </summary>
        public string FixtureId
        {
            get => _instance.FixtureId;
            set => _instance.FixtureId = value;
        }

        /// <summary>
        /// Custom error code.
        /// Use 0 for no error
        /// </summary>
        public int ErrorCode
        {
            get => _instance.ErrorCode;
            set => _instance.ErrorCode = value;
        }

        public string ErrorCodeFormat
        {
            get => _instance.ErrorCodeFormat;
            set => _instance.ErrorCodeFormat = value;
        }

        /// <summary>
        /// Textual error message
        /// </summary>
        public string ErrorMessage
        {
            get => _instance.ErrorMessage;
            set => _instance.ErrorMessage = value;
        }

        /// <summary>
        /// Array of sub-parts registered (can be changed)
        /// </summary>
        public UUTPartInfo[] PartInfo // r/o
        {
            get => _instance.PartInfo.Select(pi => new UUTPartInfo(pi)).ToArray();
            //set => _instance.PartInfo = value.Select(pi => pi._instance).ToArray();
        }

        /// <summary>
        /// List of Misc. UUT info objects 
        /// </summary>
        public MiscUUTInfo[] MiscInfo // r/o
        {
            get => _instance.MiscInfo.Select(mi => new MiscUUTInfo(mi)).ToArray();
            //set => _instance.MiscInfo = value.Select(mi => mi._instance).ToArray();
        }

        /// <summary>
        /// List of used Assets 
        /// </summary>
        public Asset[] Assets // r/o
        {
            get => _instance.Assets.Select(a => new Asset(a)).ToArray();
            //set => _instance.Assets = value.Select(a => a._instance).ToArray();
        }

        /// <summary>
        /// List of statistics for used Assets. Only available when getting the report from the server with <see cref="TDM.LoadReport"/>.
        /// </summary>
        public AssetStatistics[] AssetStatistics // r/o
        {
            get => _instance.AssetStatistics.Select(a => new AssetStatistics(a)).ToArray();
            //set => _instance.AssetStatistics = value.Select(a => a._instance).ToArray();
        }

        /// <summary>
        /// The root sequence of the test
        /// </summary>
        public SequenceCall GetRootSequenceCall() => new SequenceCall(_instance.GetRootSequenceCall());

        #endregion Properties

        /// <summary>
        /// Used to to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Misc description</param>
        /// <returns>Empty MiscUUTInfo object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description)
            => new MiscUUTInfo(_instance.AddMiscUUTInfo(description));

        /// <summary>
        /// Used to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Description of info (tag)</param>
        /// <param name="stringValue">A string value</param>
        /// <param name="numericValue">A numeric value</param>
        /// <returns>A misc info object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description, string stringValue, short numericValue)
            => new MiscUUTInfo(_instance.AddMiscUUTInfo(description, stringValue, numericValue));

        /// <summary>
        /// Used to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Description of info (tag)</param>
        /// <param name="numericValue">A numeric value</param>
        /// <returns>A misc info object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description, short numericValue)
            => new MiscUUTInfo(_instance.AddMiscUUTInfo(description, numericValue));

        /// <summary>
        /// Used to store seachable information attached to the UUT header
        /// </summary>
        /// <param name="description">Description of info (tag)</param>
        /// <param name="stringValue">A string value</param>
        /// <returns>A misc info object</returns>
        public MiscUUTInfo AddMiscUUTInfo(string description, string stringValue)
            => new MiscUUTInfo(_instance.AddMiscUUTInfo(description, stringValue));

        /// <summary>
        /// To add uut part info to the report.
        /// Example of uut part info is sub modules with part number, serial number and revision number
        /// </summary>
        /// <returns>Empty UUTPartInfo object</returns>
        public UUTPartInfo AddUUTPartInfo()
            => new UUTPartInfo(_instance.AddUUTPartInfo());

        /// <summary>
        /// To add uut part info to the report.
        /// Example of uut part info is sub modules with part number, serial number and revision number
        /// </summary>
        /// <param name="partType">Describes type of subpart</param>
        /// <param name="partNumber">Subpart’s part number</param>
        /// <param name="partSerialNumber">Subpart’s serial number</param>
        /// <param name="partRevisionNumber">Subpart’s part revision number</param>
        public UUTPartInfo AddUUTPartInfo(string partType, string partNumber, string partSerialNumber, string partRevisionNumber)
            => new UUTPartInfo(_instance.AddUUTPartInfo(partType, partNumber, partSerialNumber, partRevisionNumber));

        public Asset AddAsset(string assetSerialNumber, int usageCount)
            => new Asset(_instance.AddAsset(assetSerialNumber, usageCount));

        /// <summary>
        /// Returns an array of step order numbers that has failed, same index as <see cref="GetFailedStepNames()"/>
        /// </summary>
        /// <returns></returns>
        public int[] GetFailedStepOrderNumbers() => _instance.GetFailedStepOrderNumbers();

        /// <summary>
        /// Returns string array of failed steps name, same index as <see cref="GetFailedStepOrderNumbers()"/>
        /// </summary>
        /// <returns></returns>
        public string[] GetFailedStepNames() => _instance.GetFailedStepNames();

        public Step GetStepCausedUUTFail() => new Step(_instance.GetStepCausedUUTFail());
    }
}
