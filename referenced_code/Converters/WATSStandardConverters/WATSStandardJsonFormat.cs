using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using Virinco.WATS.Interface;
using Newtonsoft.Json;
using System.Linq;

namespace Virinco.WATS.Integration.JsonConverter
{

    public class WATSStandardJsonConverter : IReportConverter_v2
    {
        //We use these later on for enum checking. 
        private const string measureStatus = "P SF";
        private const string stepStatus = "P SFET";
        private const string stepGroups = "SMC";
        private const string reportStatus = "PFET";

        //Set a variable with an InvariantCulture, which helps with removing any cultural differences with decimal formatting.
        private readonly CultureInfo culture = CultureInfo.InvariantCulture;

        private TestModeType testMode;

        //Various ways we set parameters, including standard arguments that the user can change in the WATS client. 
        public Dictionary<string, string> args = new Dictionary<string, string>()
        {
            { "operator", "oper" },
            { "processCode", "10" },
            { "repairProcessCode", "500" },
            { "sequenceName", "sequenceName" },
            { "sequenceVersion", "1.0" },
            { "partnumber", "pn" },
            { "revision", "rev" },
            { "serialnumber", "sn" },
            { "testMode", "Import" }
        };

        public Dictionary<string, string> ConverterParameters => args;

        public WATSStandardJsonConverter() { }

        public WATSStandardJsonConverter(Dictionary<string, string> arguments)
        {
            args = arguments;
        }

        public void CleanUp() 
        { 

        }

        public Report ImportReport(TDM api, Stream file)
        {
            string testmode = args["testMode"].ToLower();

            //Import is default mode, so we check for active or default to import
            if (testmode == "active")
                api.TestMode = TestModeType.Active;
            else
                api.TestMode = TestModeType.Import;

            testMode = api.TestMode;

            using (var reader = new StreamReader(file))
            {
                string json = reader.ReadToEnd();
                var jReport = JsonConvert.DeserializeObject<Schemas.WSJF.Report>(json, new JsonSerializerSettings { Culture = culture });

                string @operator;
                string processCode;
                string sequenceName;
                string sequenceVersion;
                string partnumber;
                string revision;
                string serialnumber;
                
                if (jReport.ReportType == 'T')
                {
                    if (jReport.UUTHeader?.UserName != null)
                        @operator = jReport.UUTHeader.UserName;
                    else
                        @operator = args["operator"];

                    if (jReport.ProcessCode.HasValue)
                        processCode = jReport.ProcessCode.Value.ToString();
                    else if (jReport.ProcessName != null)
                        processCode = jReport.ProcessName;
                    else
                        processCode = args["processCode"];

                    if (jReport.RootStep?.SequenceCall?.Name != null)
                        sequenceName = jReport.RootStep.SequenceCall.Name;
                    else
                        sequenceName = args["sequenceName"];

                    if (jReport.RootStep?.SequenceCall?.Version != null)
                        sequenceVersion = jReport.RootStep.SequenceCall.Version;
                    else
                        sequenceVersion = args["sequenceVersion"];

                    if (jReport.PartNumber != null)
                        partnumber = jReport.PartNumber;
                    else
                        partnumber = args["partnumber"];

                    if (jReport.Revision != null)
                        revision = jReport.Revision;
                    else
                        revision = args["revision"];

                    if (jReport.SerialNumber != null)
                        serialnumber = jReport.SerialNumber;
                    else
                        serialnumber = args["serialnumber"];

                    var uut = api.CreateUUTReport(@operator, partnumber, revision, serialnumber, processCode, sequenceName, sequenceVersion);

                    if (jReport.ReportId != Guid.Empty)
                        uut.ReportId = jReport.ReportId;

                    if (api.TestMode == TestModeType.Import)
                        uut.Status = (UUTStatusType)reportStatus.IndexOf(jReport.Result);

                    uut.StartDateTimeOffset = jReport.Start;
                    if (jReport.StartUTC != default)
                        uut.StartDateTimeUTC = jReport.StartUTC;

                    if (!string.IsNullOrEmpty(jReport.MachineName))
                        uut.StationName = jReport.MachineName;

                    if (!string.IsNullOrEmpty(jReport.Location))
                        uut.Location = jReport.Location;

                    if (!string.IsNullOrEmpty(jReport.Purpose))
                        uut.Purpose = jReport.Purpose;

                    if (jReport.UUTHeader != null)
                    {
                        var jUut = jReport.UUTHeader;
                        if (jUut.BatchFailCount.HasValue)
                        {
                            uut.BatchFailCount = jUut.BatchFailCount.Value;

                            if (!string.IsNullOrEmpty(jUut.BatchFailCountFormat))
                                uut.BatchFailCountFormat = jUut.BatchFailCountFormat;
                        }

                        if (jUut.BatchLoopIndex.HasValue)
                        {
                            uut.BatchLoopIndex = jUut.BatchLoopIndex.Value;

                            if (!string.IsNullOrEmpty(jUut.BatchLoopIndexFormat))
                                uut.BatchLoopIndexFormat = jUut.BatchLoopIndexFormat;
                        }

                        if (jUut.ErrorCode.HasValue)
                        {
                            uut.ErrorCode = jUut.ErrorCode.Value;

                            if (!string.IsNullOrEmpty(jUut.ErrorCodeFormat))
                                uut.ErrorCodeFormat = jUut.ErrorCodeFormat;
                        }

                        if (jUut.ExecutionTime.HasValue)
                        {
                            uut.ExecutionTime = jUut.ExecutionTime.Value;

                            if (!string.IsNullOrEmpty(jUut.ExecutionTimeFormat))
                                uut.ExecutionTimeFormat = jUut.ExecutionTimeFormat;
                        }

                        if (jUut.TestSocketIndex.HasValue)
                        {
                            uut.TestSocketIndex = jUut.TestSocketIndex.Value;

                            if (!string.IsNullOrEmpty(jUut.TestSocketIndexFormat))
                                uut.TestSocketIndexFormat = jUut.TestSocketIndexFormat;
                        }

                        if (!string.IsNullOrEmpty(jUut.BatchSN))
                            uut.BatchSerialNumber = jUut.BatchSN;

                        if (!string.IsNullOrEmpty(jUut.Comment))
                            uut.Comment = jUut.Comment;

                        if (!string.IsNullOrEmpty(jUut.ErrorMessage))
                            uut.ErrorMessage = jUut.ErrorMessage;

                        if (!string.IsNullOrEmpty(jUut.FixtureId))
                            uut.FixtureId = jUut.FixtureId;
                    }

                    if (jReport.MiscInfos != null)
                    {
                        foreach (var jMisc in jReport.MiscInfos)
                        {
                            if (!string.IsNullOrEmpty(jMisc.TextValue) && jMisc.NumericValue.HasValue)
                            {
                                var miscInfo = uut.AddMiscUUTInfo(jMisc.Description, jMisc.TextValue, jMisc.NumericValue.Value);
                                if (string.IsNullOrEmpty(jMisc.NumericValueFormat))
                                    miscInfo.DataNumericFormat = jMisc.NumericValueFormat;
                            }
                            else if (!string.IsNullOrEmpty(jMisc.TextValue))
                            {
                                uut.AddMiscUUTInfo(jMisc.Description, jMisc.TextValue);
                            }
                            else if (jMisc.NumericValue.HasValue)
                            {
                                var miscInfo = uut.AddMiscUUTInfo(jMisc.Description, jMisc.NumericValue.Value);
                                if (string.IsNullOrEmpty(jMisc.NumericValueFormat))
                                    miscInfo.DataNumericFormat = jMisc.NumericValueFormat;
                            }
                            else
                                uut.AddMiscUUTInfo(jMisc.Description);
                        }
                    }

                    if (jReport.SubUnits != null)
                    {
                        foreach (var jSubunit in jReport.SubUnits)
                            uut.AddUUTPartInfo(jSubunit.PartType, jSubunit.PartNumber, jSubunit.SerialNumber, jSubunit.Revision);                        
                    }

                    if (jReport.Assets != null)
                    {
                        foreach (var jAsset in jReport.Assets)
                        {
                            var asset = uut.AddAsset(jAsset.AssetSN, jAsset.UsageCount);
                            if (string.IsNullOrEmpty(jAsset.UsageCountFormat))
                                asset.UsageCountFormat = jAsset.UsageCountFormat;
                        }
                    }

                    if (jReport.RootStep != null)
                    {
                        if (jReport.RootStep.SequenceCall != null)
                        {
                            if (jReport.RootStep.Steps != null)
                            {
                                var root = uut.GetRootSequenceCall();
                                SetExtraStepData(root, jReport.RootStep);

                                if (testMode == TestModeType.Import)
                                    root.Status = GetStepStatus(jReport.RootStep.Status);

                                bool hasLoop = false;
                                foreach (var jStep in jReport.RootStep.Steps)
                                    AddStep(jStep, root, ref hasLoop);
                            }
                        }
                        else
                            throw new InvalidOperationException("Root step must have sequence call.");
                    }
                    else
                        throw new InvalidOperationException("UUT report must have root step.");

                    return uut;
                }
                else if (jReport.ReportType == 'R')
                {
                    if (jReport.UURHeader?.UserName != null)
                        @operator = jReport.UURHeader.UserName;
                    else
                        @operator = args["operator"];

                    if (jReport.PartNumber != null)
                        partnumber = jReport.PartNumber;
                    else
                        partnumber = args["partnumber"];

                    if (jReport.Revision != null)
                        revision = jReport.Revision;
                    else
                        revision = args["revision"];

                    if (jReport.SerialNumber != null)
                        serialnumber = jReport.SerialNumber;
                    else
                        serialnumber = args["serialnumber"];

                    RepairType repairType;
                    if (jReport.ProcessCode.HasValue)
                    {
                        repairType = api.GetRepairTypes().SingleOrDefault(rt => rt.Code == jReport.ProcessCode.Value);
                        if (repairType == null)
                            throw new InvalidOperationException($"Repair type with code {jReport.ProcessCode} does not exist.");
                    }
                    else if (jReport.ProcessName != null)
                    {
                        repairType = api.GetRepairTypes().SingleOrDefault(rt => rt.Name == jReport.ProcessName);
                        if (repairType == null)
                            throw new InvalidOperationException($"Repair type with name {jReport.ProcessName} does not exist.");
                    }
                    else
                    {
                        var code = short.Parse(args["repairProcessCode"], culture);
                        repairType = api.GetRepairTypes().SingleOrDefault(rt => rt.Code == code);
                        if (repairType == null)
                            throw new InvalidOperationException($"Repair type with code {code} does not exist.");
                    }

                    OperationType operationType;
                    if (jReport.UURHeader?.ProcessCode != null)
                        operationType = api.GetOperationType(jReport.UURHeader.ProcessCode);
                    else if (jReport.UURHeader?.ProcessName != null)
                        operationType = api.GetOperationType(jReport.UURHeader.ProcessName);
                    else
                        operationType = api.GetOperationType(args["processCode"]);


                    var uur = api.CreateUURReport(@operator, repairType, operationType, serialnumber, partnumber, revision);

                    if (jReport.ReportId != Guid.Empty)
                        uur.ReportId = jReport.ReportId;

                    if (!string.IsNullOrEmpty(jReport.MachineName))
                        uur.StationName = jReport.MachineName;

                    if (!string.IsNullOrEmpty(jReport.Location))
                        uur.Location = jReport.Location;

                    if (!string.IsNullOrEmpty(jReport.Purpose))
                        uur.Purpose = jReport.Purpose;

                    uur.StartDateTimeOffset = jReport.Start;
                    if (jReport.StartUTC != default)
                        uur.StartDateTimeUTC = jReport.StartUTC;

                    if (jReport.UURHeader != null)
                    {
                        var jUur = jReport.UURHeader;

                        if (!string.IsNullOrEmpty(jUur.Comment))
                            uur.Comment = jUur.Comment;

                        if (jUur.ConfirmDate.HasValue)
                            uur.Confirmed = jUur.ConfirmDate.Value;

                        if (jUur.ExecutionTime.HasValue)
                            uur.ExecutionTime = jUur.ExecutionTime.Value;

                        if (jUur.FinalizeDate.HasValue)
                            uur.Finalized = jUur.FinalizeDate.Value;

                        if (jUur.ReferencedUUT.HasValue)
                            uur.UUTGuid = jUur.ReferencedUUT.Value;
                    }

                    if (jReport.MiscInfos != null)
                    {
                        foreach (var jMisc in jReport.MiscInfos)
                        {
                            var misc = uur.MiscUURInfo.SingleOrDefault(m => string.Equals(m.Description, jMisc.Description, StringComparison.OrdinalIgnoreCase));
                            if (misc != null)
                                misc.DataString = jMisc.TextValue;
                        }
                    }

                    if (jReport.BinaryData != null)
                    {
                        foreach (var jAttachment in jReport.BinaryData)
                        {
                            var data = Convert.FromBase64String(jAttachment.Data);
                            uur.AttachByteArray(jAttachment.Name, data, jAttachment.ContentType);
                        }
                    }

                    if (jReport.SubUnits != null && jReport.SubUnits.Any())
                    {
                        var indexes = new Dictionary<int, int>();

                        if (!jReport.SubUnits.All(su => su.Idx.HasValue))
                            throw new InvalidOperationException("All subunits must have unique idx.");

                        var jMainUnits = jReport.SubUnits.Where(su => su.Idx == 0);
                        if (!jMainUnits.Any())
                            throw new InvalidOperationException("One subunit must have idx 0.");
                        else if (jMainUnits.Count() > 1)
                            throw new InvalidOperationException("Subunit idx must be unique.");

                        var jMainUnit = jMainUnits.First();
                        indexes.Add(0, 0);

                        foreach (var jSubunit in jReport.SubUnits.Where(su => su.Idx > 0))
                        {
                            var part = uur.AddUURPartInfo(jSubunit.PartNumber, jSubunit.SerialNumber, jSubunit.Revision);
                            part.PartType = jSubunit.PartType;

                            if (indexes.ContainsKey(jSubunit.Idx.Value))
                                throw new InvalidOperationException("Subunit idx must be unique.");

                            indexes.Add(jSubunit.Idx.Value, part.PartIndex);

                            if (jSubunit.Failures != null)
                                AddFailures(part, jSubunit.Failures);
                        }

                        var partInfo = uur.PartInfo;
                        var mainUnit = partInfo.Single(pi => pi.PartIndex == 0);
                        mainUnit.SerialNumber = jMainUnit.SerialNumber;
                        mainUnit.PartNumber = jMainUnit.PartNumber;
                        mainUnit.PartRevisionNumber = jMainUnit.Revision;

                        if (jMainUnit.Failures != null)
                            AddFailures(mainUnit, jMainUnit.Failures);

                        //Translate idx
                        foreach (var jSubunit in jReport.SubUnits)
                        {
                            var partIdx = indexes[jSubunit.Idx.Value];
                            var part = partInfo.Single(pi => pi.PartIndex == partIdx);

                            if (jSubunit.ReplacedIDX.HasValue)
                            {
                                if (indexes.TryGetValue(jSubunit.ReplacedIDX.Value, out int idx))
                                    part.ReplacedIDX = idx;
                                else
                                    throw new InvalidOperationException("replacedIdx must reference an existing idx.");
                            }

                            if (jSubunit.ParentIDX.HasValue)
                            {
                                if (indexes.TryGetValue(jSubunit.ParentIDX.Value, out int idx))
                                    part.ParentIDX = idx;
                                else
                                    throw new InvalidOperationException("parentIdx must reference an existing idx.");
                            }
                        }

                        void AddFailures(UURPartInfo part, IEnumerable<Schemas.WSJF.Failure> jFailures)
                        {
                            foreach (var jFailure in jFailures)
                            {
                                var category = api.GetRootFailCodes(repairType).SingleOrDefault(f => f.Description == jFailure.Category);
                                if (category != null)
                                {
                                    var code = api.GetChildFailCodes(category).SingleOrDefault(f => f.Description == jFailure.Code);
                                    if (code != null)
                                    {
                                        var compRef = jFailure.CompRef ?? "";
                                        var comment = jFailure.Comment ?? "";

                                        var failure = part.AddFailure(code, compRef, comment, jFailure.ReferencedStepId);

                                        if (!string.IsNullOrEmpty(jFailure.ArticleDescription))
                                            failure.ComprefArticleDescription = jFailure.ArticleDescription;

                                        if (!string.IsNullOrEmpty(jFailure.ArticleVendor))
                                            failure.ComprefArticleVendor = jFailure.ArticleVendor;

                                        if (!string.IsNullOrEmpty(jFailure.ArticleNumber))
                                            failure.ComprefArticleNumber = jFailure.ArticleNumber;

                                        if (!string.IsNullOrEmpty(jFailure.ArticleRevision))
                                            failure.ComprefArticleRevision = jFailure.ArticleRevision;

                                        if (!string.IsNullOrEmpty(jFailure.FunctionBlock))
                                            failure.ComprefFunctionBlock = jFailure.FunctionBlock;

                                        if (jFailure.BinaryData != null)
                                        {
                                            foreach (var jAttachment in jFailure.BinaryData)
                                            {
                                                var data = Convert.FromBase64String(jAttachment.Data);
                                                failure.AttachByteArray(jAttachment.Name, data, jAttachment.ContentType);
                                            }
                                        }
                                    }
                                    else
                                        throw new InvalidOperationException($"Failure code {jFailure.Code} does not exist in category {jFailure.Category}.");
                                }
                                else
                                    throw new InvalidOperationException($"Failure category {jFailure.Category} does not exist.");
                            }
                        }
                    }

                    return uur;
                }
                else
                    throw new InvalidOperationException("Type must be T or R."); 
            }
        }

        private void AddStep(Schemas.WSJF.Step jStep, SequenceCall seq, ref bool isInLoop)
        {
            var measurements = new object[] { jStep.SequenceCall, jStep.MessagePopup, jStep.CallExe }.AsEnumerable();
            if (jStep.NumericMeasurements != null)
                measurements = measurements.Concat(jStep.NumericMeasurements);
            if (jStep.StringMeasurements != null)
                measurements = measurements.Concat(jStep.StringMeasurements);
            if (jStep.BooleanMeasurements != null)
                measurements = measurements.Concat(jStep.BooleanMeasurements);
            measurements = measurements.Where(o => o != null);
            if (measurements.Any())
            {
                var firstMeasurementType = measurements.First().GetType();
                var measurementTypeGroups = measurements.GroupBy(o => o.GetType());
                if (measurementTypeGroups.Count() > 1)
                {
                    var firstTypeName = GetStepTypeName(measurementTypeGroups.First().Key);
                    var unsupportedMeasurementTypeGroup = measurementTypeGroups.First(g => g.Key != firstMeasurementType);

                    throw new InvalidOperationException($"Cannot have {GetStepTypeName(unsupportedMeasurementTypeGroup.Key)} in step with {firstTypeName}.");                       
                }
            }

            if (jStep.SequenceCall == null && jStep.Steps != null && jStep.Steps.Any())
                throw new InvalidOperationException("A seqCall is required for a step to have substeps.");

            if (jStep.ChartData != null && jStep.Attachment != null)
                throw new InvalidOperationException("Cannot have chart in step with attachment.");


            if (isInLoop && (jStep.Loop == null || !jStep.Loop.Index.HasValue))
            {
                seq.StopLoop();
                isInLoop = false;
            }

            //Loop may be followed immediately by another loop
            if (!isInLoop && jStep.Loop != null)
                isInLoop = true;

            Step step;
            if (jStep.SequenceCall != null)
            {
                SequenceCall seqStep;
                if (jStep.Loop != null)
                {
                    if (!jStep.Loop.Index.HasValue)
                    {
                        seqStep = seq.StartLoop<SequenceCall>(jStep.Name, jStep.Loop.Num, jStep.Loop.NumPassed, jStep.Loop.NumFailed, jStep.Loop.EndingIndex);
                        seqStep.SequenceVersion = jStep.SequenceCall.Version;
                    }
                    else
                        seqStep = seq.AddSequenceCall(jStep.Name, jStep.SequenceCall.Name, jStep.SequenceCall.Version, jStep.Loop.Index.Value);
                }
                else
                {
                    seqStep = seq.AddSequenceCall(jStep.Name, jStep.SequenceCall.Name, jStep.SequenceCall.Version);
                }
                
                //SequenceName sets sequence FilePath...
                seqStep.SequenceName = jStep.SequenceCall.Filepath;
                seqStep.Status = GetStepStatus(jStep.Status);

                bool hasLoop = false;
                if (jStep.Steps != null)
                {
                    foreach (var jSubstep in jStep.Steps)
                        AddStep(jSubstep, seqStep, ref hasLoop);
                }

                step = seqStep;
            }
            else if (jStep.NumericMeasurements != null)
            {
                NumericLimitStep numStep;
                if (jStep.Loop != null)
                {
                    if (!jStep.Loop.Index.HasValue)
                        numStep = seq.StartLoop<NumericLimitStep>(jStep.Name, jStep.Loop.Num, jStep.Loop.NumPassed, jStep.Loop.NumFailed, jStep.Loop.EndingIndex);
                    else
                        numStep = seq.AddNumericLimitStep(jStep.Name, jStep.Loop.Index.Value);
                }
                else
                {
                    numStep = seq.AddNumericLimitStep(jStep.Name);
                }                

                if (jStep.NumericMeasurements.Count() == 1)
                {
                    var jMeas = jStep.NumericMeasurements.Single();

                    var compOp = GetCompOp(jMeas.CompOperator);
                    var status = GetStepStatus(jStep.Status);
                    if (jMeas.HighLimit.HasValue && jMeas.LowLimit.HasValue)
                    {
                        NumericLimitTest test;
                        if (testMode == TestModeType.Import)
                            test = numStep.AddTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.HighLimit.Value, jMeas.Unit, status);
                        else
                            test = numStep.AddTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.HighLimit.Value, jMeas.Unit);

                        if (!string.IsNullOrEmpty(jMeas.HighLimitFormat))
                            test.HighLimitFormat = jMeas.HighLimitFormat;

                        if (!string.IsNullOrEmpty(jMeas.LowLimitFormat))
                            test.LowLimitFormat = jMeas.LowLimitFormat;
                    }
                    else if (jMeas.HighLimit.HasValue)
                    {
                        NumericLimitTest test;
                        if (testMode == TestModeType.Import)
                            test = numStep.AddTest(jMeas.Value, compOp, jMeas.HighLimit.Value, jMeas.Unit, status);
                        else
                            test = numStep.AddTest(jMeas.Value, compOp, jMeas.HighLimit.Value, jMeas.Unit);

                        //Yes, low limit format... it is technically "limit 1"
                        if (!string.IsNullOrEmpty(jMeas.LowLimitFormat))
                            test.LowLimitFormat = jMeas.LowLimitFormat;
                    }
                    else if (jMeas.LowLimit.HasValue)
                    {
                        NumericLimitTest test;
                        if (testMode == TestModeType.Import)
                            test = numStep.AddTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.Unit, status);
                        else
                            test = numStep.AddTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.Unit);

                        if (!string.IsNullOrEmpty(jMeas.LowLimitFormat))
                            test.LowLimitFormat = jMeas.LowLimitFormat;
                    }
                    else
                    {
                        if (testMode == TestModeType.Import)
                            numStep.AddTest(jMeas.Value, jMeas.Unit, status);
                        else
                            numStep.AddTest(jMeas.Value, jMeas.Unit);
                    }
                }
                else
                {
                    foreach (var jMeas in jStep.NumericMeasurements)
                    {
                        var compOp = GetCompOp(jMeas.CompOperator);
                        var status = GetMeasureStatus(jMeas.Status);
                        if (jMeas.HighLimit.HasValue && jMeas.LowLimit.HasValue)
                        {
                            NumericLimitTest test;
                            if (testMode == TestModeType.Import)
                                test = numStep.AddMultipleTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.HighLimit.Value, jMeas.Unit, jMeas.Name, status);
                            else
                                test = numStep.AddMultipleTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.HighLimit.Value, jMeas.Unit, jMeas.Name);

                            if (!string.IsNullOrEmpty(jMeas.HighLimitFormat))
                                test.HighLimitFormat = jMeas.HighLimitFormat;

                            if (!string.IsNullOrEmpty(jMeas.LowLimitFormat))
                                test.LowLimitFormat = jMeas.LowLimitFormat;
                        }
                        else if (jMeas.HighLimit.HasValue)
                        {
                            NumericLimitTest test;
                            if (testMode == TestModeType.Import)
                                test = numStep.AddMultipleTest(jMeas.Value, compOp, jMeas.HighLimit.Value, jMeas.Unit, jMeas.Name, status);
                            else
                                test = numStep.AddMultipleTest(jMeas.Value, compOp, jMeas.HighLimit.Value, jMeas.Unit, jMeas.Name);

                            //Yes, low limit format... it is technically "limit 1"
                            if (!string.IsNullOrEmpty(jMeas.LowLimitFormat))
                                test.LowLimitFormat = jMeas.LowLimitFormat;
                        }
                        else if (jMeas.LowLimit.HasValue)
                        {
                            NumericLimitTest test;
                            if (testMode == TestModeType.Import)
                                test = numStep.AddMultipleTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.Unit, jMeas.Name, status);
                            else
                                test = numStep.AddMultipleTest(jMeas.Value, compOp, jMeas.LowLimit.Value, jMeas.Unit, jMeas.Name);

                            if (!string.IsNullOrEmpty(jMeas.LowLimitFormat))
                                test.LowLimitFormat = jMeas.LowLimitFormat;
                        }
                        else
                        {
                            if (testMode == TestModeType.Import)
                                numStep.AddMultipleTest(jMeas.Value, jMeas.Unit, jMeas.Name, status);
                            else
                                numStep.AddMultipleTest(jMeas.Value, jMeas.Unit, jMeas.Name);
                        }
                    }

                    if (testMode == TestModeType.Import)
                        numStep.Status = GetStepStatus(jStep.Status);
                }

                step = numStep;
            }
            else if (jStep.StringMeasurements != null)
            {
                StringValueStep strStep;
                if (jStep.Loop != null)
                {
                    if (!jStep.Loop.Index.HasValue)
                        strStep = seq.StartLoop<StringValueStep>(jStep.Name, jStep.Loop.Num, jStep.Loop.NumPassed, jStep.Loop.NumFailed, jStep.Loop.EndingIndex);
                    else
                        strStep = seq.AddStringValueStep(jStep.Name, jStep.Loop.Index.Value);
                }
                else
                {
                    strStep = seq.AddStringValueStep(jStep.Name);
                }

                if (jStep.StringMeasurements.Count() == 1)
                {
                    var jMeas = jStep.StringMeasurements.Single();

                    var compOp = GetCompOp(jMeas.CompOperator);
                    var status = GetStepStatus(jStep.Status);
                    if (jMeas.StringLimit != null)
                    {
                        if (testMode == TestModeType.Import)
                            strStep.AddTest(compOp, jMeas.Value, jMeas.StringLimit, status);
                        else
                            strStep.AddTest(compOp, jMeas.Value, jMeas.StringLimit);
                    }
                    else
                    {
                        if (testMode == TestModeType.Import)
                            strStep.AddTest(jMeas.Value, status);
                        else
                            strStep.AddTest(jMeas.Value);
                    }
                }
                else
                {
                    foreach (var jMeas in jStep.StringMeasurements)
                    {
                        var compOp = GetCompOp(jMeas.CompOperator);
                        var status = GetMeasureStatus(jMeas.Status);
                        if (jMeas.StringLimit != null)
                        {
                            if (testMode == TestModeType.Import)
                                strStep.AddMultipleTest(compOp, jMeas.Value, jMeas.StringLimit, jMeas.Name, status);
                            else
                                strStep.AddMultipleTest(compOp, jMeas.Value, jMeas.StringLimit, jMeas.Name);
                        }
                        else
                        {
                            if (testMode == TestModeType.Import)
                                strStep.AddMultipleTest(jMeas.Value, jMeas.Name, status);
                            else
                                strStep.AddMultipleTest(jMeas.Value, jMeas.Name);
                        }
                    }

                    if (testMode == TestModeType.Import)
                        strStep.Status = GetStepStatus(jStep.Status);
                }

                step = strStep;
            }
            else if (jStep.BooleanMeasurements != null)
            {
                PassFailStep pfStep;
                if (jStep.Loop != null)
                {
                    if (!jStep.Loop.Index.HasValue)
                        pfStep = seq.StartLoop<PassFailStep>(jStep.Name, jStep.Loop.Num, jStep.Loop.NumPassed, jStep.Loop.NumFailed, jStep.Loop.EndingIndex);
                    else
                        pfStep = seq.AddPassFailStep(jStep.Name, jStep.Loop.Index.Value);
                }
                else
                {
                    pfStep = seq.AddPassFailStep(jStep.Name);
                }

                if (jStep.BooleanMeasurements.Count() == 1)
                {
                    var jMeas = jStep.BooleanMeasurements.Single();

                    var status = GetStepStatus(jStep.Status);
                    if (testMode == TestModeType.Import)
                        pfStep.AddTest(jMeas.Status == 'P', status);
                    else
                        pfStep.AddTest(jMeas.Status == 'P');
                }
                else
                {
                    foreach (var jMeas in jStep.BooleanMeasurements)
                    {
                        var status = GetMeasureStatus(jMeas.Status);
                        if (testMode == TestModeType.Import)
                            pfStep.AddMultipleTest(jMeas.Status == 'P', jMeas.Name, status);
                        else
                            pfStep.AddMultipleTest(jMeas.Status == 'P', jMeas.Name);
                    }

                    if (testMode == TestModeType.Import)
                        pfStep.Status = GetStepStatus(jStep.Status);
                }

                step = pfStep;
            }
            else if (jStep.CallExe != null)
            {
                CallExeStep ceStep;
                if (jStep.Loop != null)
                {
                    if (!jStep.Loop.Index.HasValue)
                    {
                        ceStep = seq.StartLoop<CallExeStep>(jStep.Name, jStep.Loop.Num, jStep.Loop.NumPassed, jStep.Loop.NumFailed, jStep.Loop.EndingIndex);
                        ceStep.ExitCode = jStep.CallExe.ExitCode.Value;
                    }
                    else
                        ceStep = seq.AddCallExeStep(jStep.Name, jStep.CallExe.ExitCode.Value, jStep.Loop.Index.Value);
                }
                else
                {
                    ceStep = seq.AddCallExeStep(jStep.Name, jStep.CallExe.ExitCode.Value);
                }

                if (!string.IsNullOrEmpty(jStep.CallExe.ExitCodeFormat))
                    ceStep.ExitCodeFormat = jStep.CallExe.ExitCodeFormat;

                ceStep.Status = GetStepStatus(jStep.Status);
                step = ceStep;
            }
            else if (jStep.MessagePopup != null)
            {
                MessagePopupStep mpStep;
                if (jStep.Loop != null)
                {
                    if (!jStep.Loop.Index.HasValue)
                    {
                        mpStep = seq.StartLoop<MessagePopupStep>(jStep.Name, jStep.Loop.Num, jStep.Loop.NumPassed, jStep.Loop.NumFailed, jStep.Loop.EndingIndex);
                        mpStep.ButtonPressed = jStep.MessagePopup.Button.Value;
                        mpStep.Response = jStep.MessagePopup.Response;
                    }
                    else
                        mpStep = seq.AddMessagePopupStep(jStep.Name, jStep.MessagePopup.Button.Value, jStep.MessagePopup.Response, jStep.Loop.Index.Value);
                }
                else
                {
                    mpStep = seq.AddMessagePopupStep(jStep.Name, jStep.MessagePopup.Button.Value, jStep.MessagePopup.Response);
                }

                if (!string.IsNullOrEmpty(jStep.MessagePopup.ButtonFormat))
                    mpStep.ButtonFormat = jStep.MessagePopup.ButtonFormat;

                mpStep.Status = GetStepStatus(jStep.Status);
                step = mpStep;
            }
            else
            {
                if (!Enum.TryParse<GenericStepTypes>(jStep.StepType, true, out var stepType))
                    stepType = GenericStepTypes.Action;

                if (jStep.Loop != null)
                {
                    if (!jStep.Loop.Index.HasValue)
                        step = seq.StartLoop<GenericStep>(jStep.Name, jStep.Loop.Num, jStep.Loop.NumPassed, jStep.Loop.NumFailed, jStep.Loop.EndingIndex);                    
                    else
                        step = seq.AddGenericStep(stepType, jStep.Name, jStep.Loop.Index.Value);
                }
                else
                {
                    step = seq.AddGenericStep(stepType, jStep.Name);
                }

                step.Status = GetStepStatus(jStep.Status);
            }

            if (jStep.Attachment != null)
            {
                var data = Convert.FromBase64String(jStep.Attachment.Data);
                step.AttachByteArray(jStep.Attachment.Name, data, jStep.Attachment.ContentType);
            }
            else if (jStep.ChartData != null)
            {
                if (!Enum.TryParse<ChartType>(jStep.ChartData.ChartType, true, out var chartType))
                    throw new InvalidOperationException($"Invalid chart type {jStep.ChartData.ChartType}");

                var chart = step.AddChart(chartType, jStep.ChartData.Label ?? "", jStep.ChartData.XLabel ?? "", jStep.ChartData.XUnit ?? "", jStep.ChartData.YLabel ?? "", jStep.ChartData.YUnit ?? "");

                foreach (var jSeries in jStep.ChartData.Series)
                {
                    var yData = GetDoubleArrayFromString(jSeries.YData, jStep.Name, jSeries.Name, "yData");

                    double[] xData;
                    if (jSeries.XData == null)
                        xData = Enumerable.Range(0, yData.Length).Select(i => (double)i).ToArray();
                    else
                        xData = GetDoubleArrayFromString(jSeries.XData, jStep.Name, jSeries.Name, "xData");

                    chart.AddSeries(jSeries.Name, xData, yData);
                }
            }

            SetExtraStepData(step, jStep);
        }

        private void SetExtraStepData(Step step, Schemas.WSJF.Step jStep)
        {
            var stepGroup = stepGroups.IndexOf(jStep.Group);
            if (stepGroup != -1)
                step.StepGroup = (Interface.StepGroupEnum)stepGroup;

            if (!string.IsNullOrEmpty(jStep.ErrorMessage))
                step.StepErrorMessage = jStep.ErrorMessage;

            if (!string.IsNullOrEmpty(jStep.ReportText))
                step.ReportText = jStep.ReportText;

            if (jStep.Start.HasValue)
                step.StartDateTime = jStep.Start.Value.UtcDateTime;

            if (jStep.ErrorCode.HasValue)
            {
                step.StepErrorCode = jStep.ErrorCode.Value;

                if (!string.IsNullOrEmpty(jStep.ErrorCodeFormat))
                    step.StepErrorCodeFormat = jStep.ErrorCodeFormat;
            }

            if (jStep.TotalTime.HasValue)
            {
                step.StepTime = jStep.TotalTime.Value;

                if (!string.IsNullOrEmpty(jStep.TotalTimeFormat))
                    step.StepTimeFormat = jStep.TotalTimeFormat;
            }
        }

        private double[] GetDoubleArrayFromString(string data, string stepName, string seriesName, string dimension)
        {
            string[] stringValues = data.Split(new[] { ';' }, StringSplitOptions.RemoveEmptyEntries);
            double[] doubleValues = new double[stringValues.Length];
            for (int i = 0; i < stringValues.Length; i++)
            {
                if (!double.TryParse(stringValues[i], NumberStyles.Any, culture, out double doubleValue))
                    throw new InvalidOperationException($"Value {stringValues[i]} (#{i}) in {dimension} in series {seriesName} in step {stepName} is not a number.");

                doubleValues[i] = doubleValue;
            }

            return doubleValues;
        }

        private string GetStepTypeName(Type type)
        {
            if (type == typeof(Schemas.WSJF.SequenceCall))
                return "seqCall";
            if (type == typeof(Schemas.WSJF.NumericMeasurement))
                return "numericMeas";
            if (type == typeof(Schemas.WSJF.StringMeasurement))
                return "stringMeas";
            if (type == typeof(Schemas.WSJF.BooleanMeasurement))
                return "booleanMeas";
            if (type == typeof(Schemas.WSJF.MessagePopup))
                return "messagePopup";
            if (type == typeof(Schemas.WSJF.CallExe))
                return "callExe";
            return null;
        }

        private StepStatusType GetStepStatus(char status)
        {
            if (testMode == TestModeType.Import)
            {
                var index = stepStatus.IndexOf(status);
                if (index == -1)
                    throw new InvalidOperationException($"{status} is not a valid status.");
                return (StepStatusType)index;
            }

            return default;
        }

        private StepStatusType GetMeasureStatus(char status)
        {
            if (testMode == TestModeType.Import)
            {
                var index = measureStatus.IndexOf(status);
                if (index == -1)
                    throw new InvalidOperationException($"{status} is not a valid status.");
                return (StepStatusType)index;
            }

            return default;
        }

        private CompOperatorType GetCompOp(string comp)
        {
            if (comp != null && Enum.TryParse<CompOperatorType>(comp.ToUpper(), out var value))
                return value;

            return CompOperatorType.LOG;
        }

   
    }
}