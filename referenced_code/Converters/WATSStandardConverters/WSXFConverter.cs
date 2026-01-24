using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WSXF;
using Virinco.WATS.Schemas.WRML;
using Virinco.WATS.Interface;
using System.Collections.ObjectModel;
using System.IO;
using System.Text.RegularExpressions;
using System.Xml.Serialization;
using System.Xml;
using System.Xml.Linq;
using System.Xml.Schema;
using System.Globalization;

namespace Virinco.WATS.Integration
{
    public class WSXFConverter
    {
        private readonly List<Schemas.WRML.WATSReport> reports = new List<Schemas.WRML.WATSReport>();
        private static readonly System.DateTime dt1970 = new System.DateTime(1970, 1, 1);

        public ReadOnlyCollection<Schemas.WRML.WATSReport> Reports { get { return reports.AsReadOnly(); } }

        private Counter stepIdCounter;
        private StackableCounter stepIndexCounter;
        private Counter measureIndexCounter;
        private Counter measureOrderNumberCounter;

        public Schemas.WRML.WATSReport ConvertReport(Schemas.WSXF.WATSReport wsxfReport)
        {
            stepIdCounter = new Counter();
            stepIndexCounter = new StackableCounter();
            measureIndexCounter = new Counter();
            measureOrderNumberCounter = new Counter();

            Schemas.WRML.WATSReport wrmlReport = new Schemas.WRML.WATSReport();

            if (!string.IsNullOrEmpty(wsxfReport.PN))
                wrmlReport.PN = wsxfReport.PN.Trim();
            else
                throw new InvalidOperationException("Attribute PN for Report is null or empty");

            if (!string.IsNullOrEmpty(wsxfReport.SN))
                wrmlReport.SN = wsxfReport.SN.Trim();
            else
                throw new InvalidOperationException("Attribute SN for Report is null or empty");

            if (wsxfReport.Process != null)
                wrmlReport.Process = GetProcess(wsxfReport.Process);
            else
                throw new InvalidOperationException("Element Process is missing from Report");

            //Start = 0001-01-01T00:00:00 in local time might fail because utc year is less than 0001 (same for 10000)
            wrmlReport.Start_offset = wsxfReport.Start_offset;
            if (wsxfReport.Start_utcSpecified)
            {
                wrmlReport.Start_utc = wsxfReport.Start_utc;
                wrmlReport.Start_utcSpecified = wsxfReport.Start_utcSpecified;
            }
            //else 
            //    throw new InvalidOperationException("Attributes Start and Start_utc are null");

            wrmlReport.Rev = wsxfReport.Rev?.Trim() ?? "";
            wrmlReport.ID = wsxfReport.ID ?? Guid.NewGuid().ToString();
            wrmlReport.MachineName = !string.IsNullOrEmpty(wsxfReport.MachineName) ? wsxfReport.MachineName.Trim() : Env.StationName;

            wrmlReport.type = (Schemas.WRML.ReportType)Enum.Parse(typeof(Schemas.WRML.ReportType), wsxfReport.type.ToString());
            wrmlReport.Result = (Schemas.WRML.ReportResultType)Enum.Parse(typeof(Schemas.WRML.ReportResultType), wsxfReport.Result.ToString());
            wrmlReport.ResultSpecified = true;

            wrmlReport.Location = wsxfReport.Location?.Trim();
            wrmlReport.Purpose = wsxfReport.Purpose?.Trim();
            wrmlReport.origin = wsxfReport.origin;

            if (wsxfReport.type == Schemas.WSXF.ReportType.UUT)
            {
                if (wsxfReport.Item != null && wsxfReport.Item is Schemas.WSXF.UUT_type)
                    wrmlReport.Item = GetUUT(wsxfReport.Item as Schemas.WSXF.UUT_type);
                else
                    throw new InvalidOperationException("Element UUT is missing from Report");

                wrmlReport.Items.AddRange(GetUUTMiscInfos(wsxfReport.Items.OfType<Schemas.WSXF.MiscInfo_type>()));
                wrmlReport.Items.AddRange(GetUUTSubUnits(wsxfReport.Items.OfType<Schemas.WSXF.ReportUnitHierarchy_type>()));
                wrmlReport.Assets = wsxfReport.Assets.Select(a => GetAsset(a)).ToList();
                wrmlReport.AdditionalData = wsxfReport.AdditionalData.Select(ad => GetAdditionalData(ad)).ToList();

                Schemas.WSXF.Step_type[] rootSteps = wsxfReport.Items.OfType<Schemas.WSXF.Step_type>().ToArray();
                if (rootSteps.Length == 1)
                    wrmlReport.Items.AddRange(GetSteps(rootSteps[0], -1));
                else if (rootSteps.Length == 0)
                    Env.Trace.TraceData(System.Diagnostics.TraceEventType.Information, 0, "Report has no steps, only header");
                else
                    throw new InvalidOperationException($"Report has {rootSteps.Length} root steps");
            }
            else if (wsxfReport.type == Schemas.WSXF.ReportType.UUR)
            {
                if (wsxfReport.Item != null && wsxfReport.Item is Schemas.WSXF.UUR_type)
                    wrmlReport.Item = GetUUR(wsxfReport.Item as Schemas.WSXF.UUR_type);
                else
                    throw new InvalidOperationException("Element UUR is missing from Report");

                wrmlReport.Items.AddRange(GetUURMiscInfos(wsxfReport.Items.OfType<Schemas.WSXF.MiscInfo_type>()));
                wrmlReport.Items.AddRange(GetUURSubUnits(wsxfReport.Items.OfType<Schemas.WSXF.ReportUnitHierarchy_type>()));
                wrmlReport.Items.AddRange(GetFailures(wsxfReport.Items.OfType<Schemas.WSXF.Failures_type>()));
                wrmlReport.Items.AddRange(GetBinaries(wsxfReport.Items.OfType<Schemas.WSXF.Binary_type>()));
            }

            reports.Add(wrmlReport);
            return wrmlReport;
        }

        private Schemas.WRML.UUT_type GetUUT(Schemas.WSXF.UUT_type wsxfUUT)
        {
            Schemas.WRML.UUT_type wrmlUUT = new Schemas.WRML.UUT_type();

            wrmlUUT.BatchFailCount = wsxfUUT.BatchFailCount;
            wrmlUUT.BatchFailCountSpecified = wsxfUUT.BatchFailCountSpecified;
            wrmlUUT.BatchFailCountFormat = wsxfUUT.BatchFailCountFormat;
            wrmlUUT.BatchLoopIndex = wsxfUUT.BatchLoopIndex;
            wrmlUUT.BatchLoopIndexSpecified = wsxfUUT.BatchLoopIndexSpecified;
            wrmlUUT.BatchLoopIndexFormat = wsxfUUT.BatchLoopIndexFormat;
            wrmlUUT.BatchSN = wsxfUUT.BatchSN?.Trim();
            wrmlUUT.Comment = wsxfUUT.Comment;
            wrmlUUT.ErrorCode = wsxfUUT.ErrorCode;
            wrmlUUT.ErrorCodeSpecified = wsxfUUT.ErrorCodeSpecified;
            wrmlUUT.ErrorCodeFormat = wsxfUUT.ErrorCodeFormat;
            wrmlUUT.ErrorMessage = wsxfUUT.ErrorMessage;
            wrmlUUT.ExecutionTime = wsxfUUT.ExecutionTime;
            wrmlUUT.ExecutionTimeSpecified = wsxfUUT.ExecutionTimeSpecified;
            wrmlUUT.ExecutionTimeFormat = wsxfUUT.ExecutionTimeFormat;
            wrmlUUT.FixtureId = wsxfUUT.FixtureId?.Trim();
            wrmlUUT.ParameterBaseVersion = wsxfUUT.ParameterBaseVersion;
            wrmlUUT.TestSocketIndex = wsxfUUT.TestSocketIndex;
            wrmlUUT.TestSocketIndexSpecified = wsxfUUT.TestSocketIndexSpecified;
            wrmlUUT.TestSocketIndexFormat = wsxfUUT.TestSocketIndexFormat;
            wrmlUUT.UserLoginName = wsxfUUT.UserLoginName?.Trim();

            return wrmlUUT;
        }

        private Schemas.WRML.UUR_type GetUUR(Schemas.WSXF.UUR_type wsxfUUR)
        {
            Schemas.WRML.UUR_type wrmlUUR = new Schemas.WRML.UUR_type();

            wrmlUUR.Active = wsxfUUR.Active;
            wrmlUUR.ActiveSpecified = wsxfUUR.ActiveSpecified;
            wrmlUUR.Comment = wsxfUUR.Comment;
            wrmlUUR.ConfirmDate = wsxfUUR.ConfirmDate;
            wrmlUUR.ConfirmDateSpecified = wsxfUUR.ConfirmDateSpecified;
            wrmlUUR.ExecutionTime = wsxfUUR.ExecutionTime;
            wrmlUUR.ExecutionTimeSpecified = wsxfUUR.ExecutionTimeSpecified;
            wrmlUUR.FinalizeDate = wsxfUUR.FinalizeDate;
            wrmlUUR.FinalizeDateSpecified = wsxfUUR.FinalizeDateSpecified;
            wrmlUUR.Parent = wsxfUUR.Parent;

            wrmlUUR.UserLoginName = wsxfUUR.UserLoginName?.Trim() ?? "";

            if (!string.IsNullOrEmpty(wsxfUUR.ReferencedUUT))
            {
                if (Guid.TryParse(wsxfUUR.ReferencedUUT, out Guid _))
                    wrmlUUR.ReferencedUUT = wsxfUUR.ReferencedUUT;
                else
                    throw new InvalidOperationException("ReferencedUUT in UUR must be a report ID (GUID)");
            }

            if (wsxfUUR.Process != null)
                wrmlUUR.Process = GetProcess(wsxfUUR.Process);
            else
                throw new InvalidOperationException("Element Process is missing from UUR");

            return wrmlUUR;
        }

        private Schemas.WRML.Process_type GetProcess(Schemas.WSXF.Process_type wsxfProcess)
        {
            Schemas.WRML.Process_type wrmlProcess = new Schemas.WRML.Process_type();

            if (wsxfProcess.CodeSpecified || !string.IsNullOrEmpty(wsxfProcess.Name))
            {
                wrmlProcess.Code = wsxfProcess.Code;
                wrmlProcess.CodeSpecified = wsxfProcess.CodeSpecified;
                wrmlProcess.CodeFormat = wsxfProcess.CodeFormat;
                wrmlProcess.Name = wsxfProcess.Name;
            }
            else
                throw new InvalidOperationException("Attributes Code and Name for Process are empty or null");

            return wrmlProcess;
        }


        private IEnumerable<object> GetUUTMiscInfos(IEnumerable<Schemas.WSXF.MiscInfo_type> wsxfMiscInfos)
        {
            List<object> wrmlMiscInfos = new List<object>();

            foreach (Schemas.WSXF.MiscInfo_type wsxfMiscInfo in wsxfMiscInfos)
            {
                Schemas.WRML.MiscInfo_type wrmlMiscInfo = new Schemas.WRML.MiscInfo_type();

                wrmlMiscInfo.Typedef = wsxfMiscInfo.Typedef ?? "";

                wrmlMiscInfo.Description = wsxfMiscInfo.Description?.Trim();
                wrmlMiscInfo.Numeric = wsxfMiscInfo.Numeric;
                wrmlMiscInfo.NumericSpecified = wsxfMiscInfo.NumericSpecified;
                wrmlMiscInfo.NumericFormat = wsxfMiscInfo.NumericFormat;
                wrmlMiscInfo.Value = wsxfMiscInfo.Value;

                wrmlMiscInfo.idx = wsxfMiscInfo.idx;
                wrmlMiscInfo.idxSpecified = wsxfMiscInfo.idxSpecified;
                wrmlMiscInfo.order_no = wsxfMiscInfo.order_no;
                wrmlMiscInfo.order_noSpecified = wsxfMiscInfo.order_noSpecified;

                wrmlMiscInfos.Add(wrmlMiscInfo);
            }

            return wrmlMiscInfos;
        }

        private IEnumerable<object> GetUUTSubUnits(IEnumerable<Schemas.WSXF.ReportUnitHierarchy_type> wsxfSubUnits)
        {
            List<object> wrmlSubUnits = new List<object>();

            foreach (Schemas.WSXF.ReportUnitHierarchy_type wsxfSubUnit in wsxfSubUnits)
            {
                Schemas.WRML.ReportUnitHierarchy_type wrmlSubUnit = new Schemas.WRML.ReportUnitHierarchy_type();

                wrmlSubUnit.Rev = wsxfSubUnit.Rev?.Trim() ?? "";

                wrmlSubUnit.PN = wsxfSubUnit.PN?.Trim();
                wrmlSubUnit.SN = wsxfSubUnit.SN?.Trim();
                wrmlSubUnit.PartType = wsxfSubUnit.PartType?.Trim();

                wrmlSubUnit.Idx = wsxfSubUnit.Idx;
                wrmlSubUnit.IdxSpecified = wsxfSubUnit.IdxSpecified;
                wrmlSubUnit.ParentIDX = wsxfSubUnit.ParentIDX;
                wrmlSubUnit.ParentIDXSpecified = wsxfSubUnit.ParentIDXSpecified;
                wrmlSubUnit.Position = wsxfSubUnit.Position;
                wrmlSubUnit.PositionSpecified = wsxfSubUnit.PositionSpecified;
                wrmlSubUnit.ReplacedIDX = wsxfSubUnit.ReplacedIDX;
                wrmlSubUnit.ReplacedIDXSpecified = wsxfSubUnit.ReplacedIDXSpecified;

                wrmlSubUnits.Add(wrmlSubUnit);
            }

            return wrmlSubUnits;
        }

        private Schemas.WRML.Asset_type GetAsset(Schemas.WSXF.Asset_type wsxfAsset)
        {
            return new Schemas.WRML.Asset_type
            {
                AssetSN = wsxfAsset.AssetSN,
                UsageCount = wsxfAsset.UsageCount,
                UsageCountFormat = wsxfAsset.UsageCountFormat
            };
        }

        private IEnumerable<object> GetUURMiscInfos(IEnumerable<Schemas.WSXF.MiscInfo_type> wsxfMiscInfos)
        {
            List<object> wrmlMiscInfos = new List<object>();

            foreach (Schemas.WSXF.MiscInfo_type wsxfMiscInfo in wsxfMiscInfos)
            {
                Schemas.WRML.MiscInfo_type wrmlMiscInfo = new Schemas.WRML.MiscInfo_type();

                wrmlMiscInfo.Typedef = wsxfMiscInfo.Typedef ?? "";

                wrmlMiscInfo.Description = wsxfMiscInfo.Description?.Trim();
                wrmlMiscInfo.Numeric = wsxfMiscInfo.Numeric;
                wrmlMiscInfo.NumericSpecified = wsxfMiscInfo.NumericSpecified;
                wrmlMiscInfo.NumericFormat = wsxfMiscInfo.NumericFormat;
                wrmlMiscInfo.Value = wsxfMiscInfo.Value;

                wrmlMiscInfo.Id = wsxfMiscInfo.Id;
                wrmlMiscInfo.idx = wsxfMiscInfo.idx;
                wrmlMiscInfo.idxSpecified = wsxfMiscInfo.idxSpecified;
                wrmlMiscInfo.order_no = wsxfMiscInfo.order_no;
                wrmlMiscInfo.order_noSpecified = wsxfMiscInfo.order_noSpecified;

                wrmlMiscInfos.Add(wrmlMiscInfo);
            }

            return wrmlMiscInfos;
        }

        private IEnumerable<object> GetUURSubUnits(IEnumerable<Schemas.WSXF.ReportUnitHierarchy_type> wsxfSubUnits)
        {
            List<object> wrmlSubUnits = new List<object>();

            //Validate that the first one is this unit?
            foreach (Schemas.WSXF.ReportUnitHierarchy_type wsxfSubUnit in wsxfSubUnits)
            {
                Schemas.WRML.ReportUnitHierarchy_type wrmlSubUnit = new Schemas.WRML.ReportUnitHierarchy_type();

                wrmlSubUnit.Rev = wsxfSubUnit.Rev?.Trim() ?? "";

                wrmlSubUnit.PN = wsxfSubUnit.PN?.Trim();
                wrmlSubUnit.SN = wsxfSubUnit.SN?.Trim();
                wrmlSubUnit.PartType = wsxfSubUnit.PartType?.Trim();

                wrmlSubUnit.Idx = wsxfSubUnit.Idx;
                wrmlSubUnit.IdxSpecified = wsxfSubUnit.IdxSpecified;
                wrmlSubUnit.ParentIDX = wsxfSubUnit.ParentIDX;
                wrmlSubUnit.ParentIDXSpecified = wsxfSubUnit.ParentIDXSpecified;

                wrmlSubUnit.Position = wsxfSubUnit.Position;
                wrmlSubUnit.PositionSpecified = wsxfSubUnit.PositionSpecified;
                wrmlSubUnit.ReplacedIDX = wsxfSubUnit.ReplacedIDX;
                wrmlSubUnit.ReplacedIDXSpecified = wsxfSubUnit.ReplacedIDXSpecified;

                wrmlSubUnits.Add(wrmlSubUnit);
            }

            return wrmlSubUnits;
        }

        private IEnumerable<object> GetSteps(Schemas.WSXF.Step_type wsxfStep, int parentStepId)
        {
            List<object> wrmlSteps = new List<object>();

            measureIndexCounter.ResetCounter();

            Type[] exemptTypes = new Type[] { typeof(Schemas.WSXF.Chart_type), typeof(Schemas.WSXF.Step_typeLoop), typeof(Schemas.WSXF.Attachment_type), typeof(Schemas.WSXF.AdditionalResults_type) };
            IGrouping<Type, object>[] typeGroups = wsxfStep.Items.Where(item => !exemptTypes.Any(type => type == item.GetType())).GroupBy(item => item.GetType()).ToArray();
            if (typeGroups.Length > 1)
            {
                string[] typeNames = typeGroups.Select(g => g.Key.Name).Select(s => s.Substring(0, s.Length - "_type".Length)).ToArray();
                throw new InvalidOperationException($"Step contains {string.Join(", ", typeNames, 0, typeNames.Length - 1)} and {typeNames.Last()}");
            }

            Schemas.WRML.Step_type wrmlStep = GetStep(wsxfStep, parentStepId);
            wrmlSteps.Add(wrmlStep);

            Schemas.WSXF.SequenceCall_type[] wsxfSequenceCalls = wsxfStep.Items.OfType<Schemas.WSXF.SequenceCall_type>().ToArray();
            Schemas.WSXF.NumericLimit_type[] wsxfNumericLimits = wsxfStep.Items.OfType<Schemas.WSXF.NumericLimit_type>().ToArray();
            Schemas.WSXF.StringValue_type[] wsxfStringValues = wsxfStep.Items.OfType<Schemas.WSXF.StringValue_type>().ToArray();
            Schemas.WSXF.PassFail_type[] wsxfPassFails = wsxfStep.Items.OfType<Schemas.WSXF.PassFail_type>().ToArray().ToArray();
            Schemas.WSXF.MessagePopup_type[] wsxfMessagePopups = wsxfStep.Items.OfType<Schemas.WSXF.MessagePopup_type>().ToArray();
            Schemas.WSXF.Callexe_type[] wsxfCallExes = wsxfStep.Items.OfType<Schemas.WSXF.Callexe_type>().ToArray();

            Schemas.WSXF.Step_typeLoop wsxfLoop = wsxfStep.Loop;
            Schemas.WSXF.Chart_type[] wsxfCharts = wsxfStep.Items.OfType<Schemas.WSXF.Chart_type>().ToArray();
            Schemas.WSXF.Attachment_type[] wsxfAttachments = wsxfStep.Items.OfType<Attachment_type>().ToArray();
            Schemas.WSXF.AdditionalResults_type[] wsxfAdditionalResults = wsxfStep.Items.OfType<Schemas.WSXF.AdditionalResults_type>().ToArray();

            if (parentStepId == -1)
            {
                if (wsxfSequenceCalls.Length != 1)
                    throw new InvalidOperationException($"Root step contains {wsxfSequenceCalls.Length} SequenceCalls");
            }

            if (wsxfSequenceCalls.Length > 0)
            {
                if (wsxfSequenceCalls.Length > 1)
                    throw new InvalidOperationException($"Step contains {wsxfSequenceCalls.Length} SequenceCalls");

                wrmlStep.StepType = "SequenceCall";
                wrmlSteps.Add(GetSequenceCall(wsxfSequenceCalls.Single(), wrmlStep.StepID));

                stepIndexCounter.NewCounter();
                foreach (Schemas.WSXF.Step_type wsxfSubStep in wsxfStep.Step)
                {
                    wrmlSteps.AddRange(GetSteps(wsxfSubStep, wrmlStep.StepID));
                }
                stepIndexCounter.PreviousCounter();
            }
            else if (wsxfNumericLimits.Length > 0)
            {
                if (wsxfNumericLimits.Length > 1)
                    wrmlStep.StepType = "ET_MNLT";
                else
                    wrmlStep.StepType = string.IsNullOrEmpty(wsxfNumericLimits[0].Name) ? "ET_NLT" : "ET_MNLT";

                var numericLimits = GetNumericLimits(wsxfNumericLimits, wrmlStep.StepID);
                wrmlSteps.AddRange(numericLimits);

                //Measurement only has Passed, Failed, and Skipped. Only change if step is Passed.
                if (wrmlStep.Status == Schemas.WRML.StepResultType.Passed && numericLimits.Any(nl => ((Schemas.WRML.NumericLimit_type)nl).Status == Schemas.WRML.MeasurementResultType.Failed))
                    wrmlStep.Status = Schemas.WRML.StepResultType.Failed;
            }
            else if (wsxfStringValues.Length > 0)
            {
                if (wsxfNumericLimits.Length > 1)
                    wrmlStep.StepType = "ET_MSVT";
                else
                    wrmlStep.StepType = "ET_SVT";

                var stringValues = GetStringValues(wsxfStringValues, wrmlStep.StepID);
                wrmlSteps.AddRange(stringValues);

                if (wrmlStep.Status == Schemas.WRML.StepResultType.Passed && stringValues.Any(sv => ((Schemas.WRML.StringValue_type)sv).Status == Schemas.WRML.MeasurementResultType.Failed))
                    wrmlStep.Status = Schemas.WRML.StepResultType.Failed;
            }
            else if (wsxfPassFails.Length > 0)
            {
                if (wsxfPassFails.Length > 1)
                    wrmlStep.StepType = "ET_MPFT";
                else
                    wrmlStep.StepType = "ET_PFT";

                var passFails = GetPassFails(wsxfPassFails, wrmlStep.StepID);
                wrmlSteps.AddRange(passFails);

                if (wrmlStep.Status == Schemas.WRML.StepResultType.Passed && passFails.Any(pf => ((Schemas.WRML.PassFail_type)pf).Status == Schemas.WRML.MeasurementResultType.Failed))
                    wrmlStep.Status = Schemas.WRML.StepResultType.Failed;
            }
            else if (wsxfMessagePopups.Length > 0)
            {
                if (wsxfMessagePopups.Length > 1)
                    throw new InvalidOperationException($"Step contains {wsxfMessagePopups.Length} MessagePopups");

                wrmlStep.StepType = "MessagePopup";
                wrmlSteps.Add(GetMessagePopup(wsxfMessagePopups.Single(), wrmlStep.StepID));
            }
            else if (wsxfCallExes.Length > 0)
            {
                if (wsxfCallExes.Length > 1)
                    throw new InvalidOperationException($"Step contains {wsxfCallExes.Length} CallExes");

                wrmlStep.StepType = "CallExecutable";
                wrmlSteps.Add(GetCallExe(wsxfCallExes.Single(), wrmlStep.StepID));
            }
            else
            {
                GenericStepTypes genericStepType;
                if (Utilities.EnumTryParse(wsxfStep.StepType, out genericStepType))
                    wrmlStep.StepType = wsxfStep.StepType;
                else
                {
                    wrmlStep.StepType = GenericStepTypes.Action.ToString();
                    Env.Trace.TraceData(System.Diagnostics.TraceEventType.Information, 0, "Step has invalid StepType. StepType set to Action as default");
                }
            }

            if (wsxfCharts.Length > 0)
            {
                if (wsxfCharts.Length > 1)
                    throw new InvalidOperationException($"Step contains {wsxfCharts.Length} Charts");

                wrmlStep.StepType = "WATS_XYGMNLT";
                wrmlSteps.AddRange(GetChart(wsxfCharts.Single(), wrmlStep.StepID));
            }
            if (wsxfAttachments.Length > 0)
            {
                if (wsxfAttachments.Length > 1)
                    throw new InvalidOperationException($"Step contains {wsxfAttachments.Length} Attachments");

                wrmlStep.StepType = "WATS_AttachFile";
                wrmlSteps.AddRange(GetAttachment(wsxfAttachments.Single(), wrmlStep.StepID));
            }
            if (wsxfAdditionalResults.Length > 0)
            {
                //Supported for export/import, not documented how to create additional results
                wrmlSteps.AddRange(wsxfAdditionalResults.Select(ar => GetAdditionalResult(ar, wrmlStep.StepID)));
            }
            if (wsxfLoop!=null)
            {
                wrmlStep.Loop = GetLoopSummary(wsxfLoop);
            }

            return wrmlSteps;
        }

        private Schemas.WRML.Step_type GetStep(Schemas.WSXF.Step_type wsxfStep, int parentStepId)
        {
            Schemas.WRML.Step_type wrmlStep = new Schemas.WRML.Step_type();

            wrmlStep.Group = (Schemas.WRML.StepGroup_type)Enum.Parse(typeof(Schemas.WRML.StepGroup_type), wsxfStep.Group.ToString());
            wrmlStep.Status = (Schemas.WRML.StepResultType)Enum.Parse(typeof(Schemas.WRML.StepResultType), wsxfStep.Status.ToString());

            wrmlStep.Name = wsxfStep.Name?.Trim();
            wrmlStep.ReportText = wsxfStep.ReportText;
            wrmlStep.module_time = wsxfStep.module_time;
            wrmlStep.module_timeSpecified = wsxfStep.module_timeSpecified;
            wrmlStep.module_timeFormat = wsxfStep.module_timeFormat;
            wrmlStep.Start = wsxfStep.Start;
            wrmlStep.StartSpecified = wsxfStep.StartSpecified;
            wrmlStep.StepCausedSequenceFailure = wsxfStep.StepCausedSequenceFailure;
            wrmlStep.StepCausedSequenceFailureSpecified = wsxfStep.StepCausedSequenceFailureSpecified;
            wrmlStep.StepErrorCode = wsxfStep.StepErrorCode;
            wrmlStep.StepErrorCodeSpecified = wsxfStep.StepErrorCodeSpecified;
            wrmlStep.StepErrorMessage = wsxfStep.StepErrorMessage;
            wrmlStep.StepErrorCodeFormat = wsxfStep.StepErrorCodeFormat;
            wrmlStep.total_time = wsxfStep.total_time;
            wrmlStep.total_timeSpecified = wsxfStep.total_timeSpecified;
            wrmlStep.total_timeFormat = wsxfStep.total_timeFormat;
            wrmlStep.TSGuid = wsxfStep.TSGuid;

            int stepId = stepIdCounter.Increment();
            int stepIndex = stepIndexCounter.Increment();

            wrmlStep.Idx = wsxfStep.Idx;
            wrmlStep.IdxSpecified = wsxfStep.IdxSpecified;
            wrmlStep.InteractiveExeNum = wsxfStep.InteractiveExeNum;
            wrmlStep.InteractiveExeNumSpecified = wsxfStep.InteractiveExeNumSpecified;
            wrmlStep.InteractiveExeNumFormat = wsxfStep.InteractiveExeNumFormat;
            wrmlStep.StepIndex = wsxfStep.StepIndexSpecified ? wsxfStep.StepIndex : stepIndex;
            wrmlStep.StepIndexSpecified = true;

            wrmlStep.StepID = stepId;

            wrmlStep.ParentStepID = parentStepId;
            wrmlStep.ParentStepIDSpecified = parentStepId == -1 ? false : true;

            return wrmlStep;
        }

        private Schemas.WRML.SequenceCall_type GetSequenceCall(Schemas.WSXF.SequenceCall_type wsxfSeqCall, int stepId)
        {
            Schemas.WRML.SequenceCall_type wrmlSeqCall = new Schemas.WRML.SequenceCall_type();

            wrmlSeqCall.Filename = wsxfSeqCall.Filename ?? "";
            wrmlSeqCall.Filepath = wsxfSeqCall.Filepath ?? "";
            wrmlSeqCall.Version = wsxfSeqCall.Version ?? "";
            wrmlSeqCall.Name = wsxfSeqCall.Name ?? "";
            wrmlSeqCall.StepID = stepId;

            int measureIndex = measureIndexCounter.Increment();
            wrmlSeqCall.MeasIndex = measureIndex;

            return wrmlSeqCall;
        }

        private IEnumerable<object> GetNumericLimits(Schemas.WSXF.NumericLimit_type[] wsxfNumericLimits, int stepID)
        {
            List<object> wrmlNumericLimits = new List<object>();

            foreach (Schemas.WSXF.NumericLimit_type wsxfNumericLimit in wsxfNumericLimits)
            {
                Schemas.WRML.NumericLimit_type wrmlNumericLimit = new Schemas.WRML.NumericLimit_type();

                if (wsxfNumericLimits.Length > 1)
                {
                    if (wsxfNumericLimit.Name == null)
                        throw new InvalidOperationException("Attribute Name in Multiple NumericLimit Test is null");
                }

                if (!string.IsNullOrEmpty(wsxfNumericLimit.CompOperator))
                    wrmlNumericLimit.CompOperator = wsxfNumericLimit.CompOperator;
                else
                    wrmlNumericLimit.CompOperator = "Log";

                wrmlNumericLimit.Status = (Schemas.WRML.MeasurementResultType)Enum.Parse(typeof(Schemas.WRML.MeasurementResultType), wsxfNumericLimit.Status.ToString());

                wrmlNumericLimit.NumericValue = wsxfNumericLimit.NumericValue;
                wrmlNumericLimit.NumericValueFormat = wsxfNumericLimit.NumericValueFormat;
                wrmlNumericLimit.HighLimit = wsxfNumericLimit.HighLimit;
                wrmlNumericLimit.HighLimitSpecified = wsxfNumericLimit.HighLimitSpecified;
                wrmlNumericLimit.HighLimitFormat = wsxfNumericLimit.HighLimitFormat;
                wrmlNumericLimit.LowLimit = wsxfNumericLimit.LowLimit;
                wrmlNumericLimit.LowLimitSpecified = wsxfNumericLimit.LowLimitSpecified;
                wrmlNumericLimit.LowLimitFormat = wsxfNumericLimit.LowLimitFormat;
                wrmlNumericLimit.Name = wsxfNumericLimit.Name?.Trim();
                wrmlNumericLimit.Units = wsxfNumericLimit.Units;
                wrmlNumericLimit.StepID = stepID;

                int measureIndex = measureIndexCounter.Increment();
                wrmlNumericLimit.MeasIndex = wsxfNumericLimit.MeasIndexSpecified ? wsxfNumericLimit.MeasIndex : measureIndex;
                wrmlNumericLimit.MeasIndexSpecified = true;

                int measureOrderNumber = measureOrderNumberCounter.Increment();
                wrmlNumericLimit.MeasOrderNumber = wsxfNumericLimit.MeasIndexSpecified ? wsxfNumericLimit.MeasOrderNumber : measureOrderNumber;
                wrmlNumericLimit.MeasOrderNumberSpecified = true;

                wrmlNumericLimits.Add(wrmlNumericLimit);
            }

            return wrmlNumericLimits;
        }

        private IEnumerable<object> GetStringValues(Schemas.WSXF.StringValue_type[] wsxfStringValues, int stepID)
        {
            List<object> wrmlStringValues = new List<object>();

            foreach (Schemas.WSXF.StringValue_type wsxfStringValue in wsxfStringValues)
            {
                Schemas.WRML.StringValue_type wrmlStringValue = new Schemas.WRML.StringValue_type();

                if (wsxfStringValues.Length > 1)
                {
                    if (wsxfStringValue.Name == null)
                        throw new InvalidOperationException("Attribute Name in Multiple StringValue Test is null");
                }

                if (!string.IsNullOrEmpty(wsxfStringValue.CompOperator))
                    wrmlStringValue.CompOperator = wsxfStringValue.CompOperator;
                else
                    wrmlStringValue.CompOperator = "Log";

                wrmlStringValue.Status = (Schemas.WRML.MeasurementResultType)Enum.Parse(typeof(Schemas.WRML.MeasurementResultType), wsxfStringValue.Status.ToString());

                wrmlStringValue.StringValue = wsxfStringValue.StringValue;
                wrmlStringValue.StringLimit = wsxfStringValue.StringLimit;
                wrmlStringValue.Name = wsxfStringValue.Name?.Trim();
                wrmlStringValue.StepID = stepID;

                int measureIndex = measureIndexCounter.Increment();
                wrmlStringValue.MeasIndex = wsxfStringValue.MeasIndexSpecified ? wsxfStringValue.MeasIndex : measureIndex;
                wrmlStringValue.MeasIndexSpecified = true;

                int measureOrderNumber = measureOrderNumberCounter.Increment();
                wrmlStringValue.MeasOrderNumber = wsxfStringValue.MeasIndexSpecified ? wsxfStringValue.MeasOrderNumber : measureOrderNumber;
                wrmlStringValue.MeasOrderNumberSpecified = true;

                wrmlStringValues.Add(wrmlStringValue);
            }

            return wrmlStringValues;
        }

        private IEnumerable<object> GetPassFails(Schemas.WSXF.PassFail_type[] wsxfPassFails, int stepID)
        {
            List<object> wrmlPassFails = new List<object>();

            foreach (Schemas.WSXF.PassFail_type wsxfPassFail in wsxfPassFails)
            {
                Schemas.WRML.PassFail_type wrmlPassFail = new Schemas.WRML.PassFail_type();

                if (wsxfPassFails.Length > 1)
                {
                    if (wsxfPassFail.Name == null)
                        throw new InvalidOperationException("Attribute Name in Multiple PassFail Test is null");
                }

                wrmlPassFail.Status = (Schemas.WRML.MeasurementResultType)Enum.Parse(typeof(Schemas.WRML.MeasurementResultType), wsxfPassFail.Status.ToString());

                wrmlPassFail.Name = wsxfPassFail.Name?.Trim();
                wrmlPassFail.StepID = stepID;

                int measureIndex = measureIndexCounter.Increment();
                wrmlPassFail.MeasIndex = wsxfPassFail.MeasIndexSpecified ? wsxfPassFail.MeasIndex : measureIndex;
                wrmlPassFail.MeasIndexSpecified = true;

                int measureOrderNumber = measureOrderNumberCounter.Increment();
                wrmlPassFail.MeasOrderNumber = wsxfPassFail.MeasIndexSpecified ? wsxfPassFail.MeasOrderNumber : measureOrderNumber;
                wrmlPassFail.MeasOrderNumberSpecified = true;

                wrmlPassFails.Add(wrmlPassFail);
            }

            return wrmlPassFails;
        }

        private Schemas.WRML.MessagePopup_type GetMessagePopup(Schemas.WSXF.MessagePopup_type wsxfMessagePopup, int stepID)
        {
            Schemas.WRML.MessagePopup_type wrmlMessagePopup = new Schemas.WRML.MessagePopup_type();

            wrmlMessagePopup.Button = wsxfMessagePopup.Button;
            wrmlMessagePopup.ButtonSpecified = wsxfMessagePopup.ButtonSpecified;
            wrmlMessagePopup.ButtonFormat = wsxfMessagePopup.ButtonFormat;
            wrmlMessagePopup.Response = wsxfMessagePopup.Response;
            wrmlMessagePopup.StepID = stepID;

            int measureIndex = measureIndexCounter.Increment();
            wrmlMessagePopup.MeasIndex = wsxfMessagePopup.MeasIndexSpecified ? wsxfMessagePopup.MeasIndex : measureIndex;
            wrmlMessagePopup.MeasIndexSpecified = true;

            return wrmlMessagePopup;
        }

        private Schemas.WRML.Callexe_type GetCallExe(Schemas.WSXF.Callexe_type wsxfCallExe, int stepID)
        {
            Schemas.WRML.Callexe_type wrmlCallExe = new Schemas.WRML.Callexe_type();

            wrmlCallExe.ExitCode = wsxfCallExe.ExitCode;
            wrmlCallExe.ExitCodeSpecified = wsxfCallExe.ExitCodeSpecified;
            wrmlCallExe.ExitCodeFormat = wsxfCallExe.ExitCodeFormat;
            wrmlCallExe.StepID = stepID;

            int measureIndex = measureIndexCounter.Increment();
            wrmlCallExe.MeasIndex = wsxfCallExe.MeasIndexSpecified ? wsxfCallExe.MeasIndex : measureIndex;
            wrmlCallExe.MeasIndexSpecified = true;

            return wrmlCallExe;
        }

        private IEnumerable<object> GetAttachment(Schemas.WSXF.Attachment_type wsxfAttachment, int stepID)
        {
            List<object> wrmlAttachment = new List<object>();

            Schemas.WRML.Chart_type row1 = new Schemas.WRML.Chart_type();
            Schemas.WRML.Chart_type row2 = new Schemas.WRML.Chart_type();
            row1.StepID = stepID;
            row1.ChartType = "ATTACHMENT";
            row1.idx = 0;
            row1.idxSpecified = true;
            row2.StepID = stepID;
            row2.DataType = "ATTACHMENT";
            row2.PlotName = wsxfAttachment.ContentType;
            row2.idx = 1;
            row2.idxSpecified = true;

            if (wsxfAttachment.Value.Length == 0) //If there is no data string, it should be a file
            {
                if (File.Exists(wsxfAttachment.Name))
                {
                    FileInfo fileInfo = new FileInfo(wsxfAttachment.Name);
                    row1.Label = fileInfo.Name;
                    try
                    {
                        using (FileStream file = new FileStream(fileInfo.FullName, FileMode.Open, FileAccess.Read))
                        {
                            byte[] data = new byte[file.Length];
                            file.Read(data, 0, data.Length);
                            row2.Data = data;
                        }
                    }
                    catch (Exception ex)
                    {
                        throw new ApplicationException($"An exception occured while reading file {wsxfAttachment.Name}", ex);
                    }
                }
                else
                    throw new FileNotFoundException($"Attachment file {wsxfAttachment.Name} does not exist");
            }
            else
            {
                row1.Label = wsxfAttachment.Name;
                row2.Data = wsxfAttachment.Value;
            }

            wrmlAttachment.Add(row1);
            wrmlAttachment.Add(row2);

            return wrmlAttachment;
        }

        private Schemas.WRML.Step_typeLoop GetLoopSummary(Schemas.WSXF.Step_typeLoop wsxfLoop)
        {
            Schemas.WRML.Step_typeLoop wrmlLoop = new Schemas.WRML.Step_typeLoop();

            wrmlLoop.ending_index = wsxfLoop.ending_index;
            wrmlLoop.ending_indexSpecified = wsxfLoop.ending_indexSpecified;
            wrmlLoop.failed = wsxfLoop.failed;
            wrmlLoop.failedSpecified = wsxfLoop.failedSpecified;
            wrmlLoop.num = wsxfLoop.num;
            wrmlLoop.numSpecified = wsxfLoop.numSpecified;
            wrmlLoop.passed = wsxfLoop.passed;
            wrmlLoop.passedSpecified = wsxfLoop.passedSpecified;
            wrmlLoop.index = wsxfLoop.index;
            wrmlLoop.indexSpecified = wsxfLoop.indexSpecified;

            return wrmlLoop;
        }

        private object GetAdditionalResult(Schemas.WSXF.AdditionalResults_type wsxfAdditionalResults, int stepID)
        {
            Schemas.WRML.AdditionalResults_type wrmlAdditionalResults = new Schemas.WRML.AdditionalResults_type();

            wrmlAdditionalResults.Any = wsxfAdditionalResults.Any;
            wrmlAdditionalResults.Name = wsxfAdditionalResults.Name;
            wrmlAdditionalResults.StepID = stepID;
            wrmlAdditionalResults.StepIDSpecified = true;

            wrmlAdditionalResults.Idx = wsxfAdditionalResults.Idx;
            wrmlAdditionalResults.IdxSpecified = wsxfAdditionalResults.IdxSpecified;

            return wrmlAdditionalResults;
        }

        private Schemas.WRML.AdditionalData_type GetAdditionalData(Schemas.WSXF.AdditionalData_type wsxfAdditionalData)
        {
            return new Schemas.WRML.AdditionalData_type
            {
                Any = wsxfAdditionalData.Any,
                Name = wsxfAdditionalData.Name,
                Idx = wsxfAdditionalData.Idx,
                IdxSpecified = wsxfAdditionalData.IdxSpecified
            };
        }

        private IEnumerable<object> GetChart(Schemas.WSXF.Chart_type wsxfChart, int stepID)
        {
            List<object> wrmlChartItems = new List<object>();

            short idx = 0;

            Schemas.WRML.Chart_type wrmlChart = new Schemas.WRML.Chart_type();

            wrmlChart.ChartType = wsxfChart.ChartType ?? "Line";
            wrmlChart.Label = wsxfChart.Label?.Trim() ?? "";
            wrmlChart.XLabel = wsxfChart.XLabel?.Trim() ?? "";
            wrmlChart.XUnit = wsxfChart.XUnit ?? "";
            wrmlChart.YLabel = wsxfChart.YLabel?.Trim() ?? "";
            wrmlChart.YUnit = wsxfChart.YUnit ?? "";
            wrmlChart.StepID = stepID;

            //Chart Idx must be 0, or else it wont be rendered in UUT view
            wrmlChart.idx = idx++;
            wrmlChart.idxSpecified = true;

            wrmlChartItems.Add(wrmlChart);

            foreach (Schemas.WSXF.ChartSeries_type wsxfSeries in wsxfChart.Series)
            {
                Schemas.WRML.Chart_type wrmlSeries = new Schemas.WRML.Chart_type();

                wrmlSeries.PlotName = wsxfSeries.Name;
                wrmlSeries.DataType = wsxfSeries.DataType.ToString();
                wrmlSeries.StepID = stepID;
                //wsxfSeries.DataTypeSpecified

                wrmlSeries.idx = idx++;
                wrmlSeries.idxSpecified = true;

                wrmlSeries.Data = GetChartSeriesData(wsxfSeries.xdata, wsxfSeries.ydata);

                wrmlChartItems.Add(wrmlSeries);
            }

            return wrmlChartItems;
        }

        private byte[] GetChartSeriesData(string xData, string yData)
        {
            if (string.IsNullOrEmpty(yData))
                throw new InvalidOperationException("yData of Series is empty");

            double[] yDataValues = GetDoubleArrayFromString(yData, ';');

            double[] xDataValues;
            if (string.IsNullOrEmpty(xData))
            {
                xDataValues = new double[yDataValues.Length];
                for (int i = 0; i < yDataValues.Length; i++)
                {
                    xDataValues[i] = i;
                }
            }
            else
                xDataValues = GetDoubleArrayFromString(xData, ';');

            if (xDataValues.Length != yDataValues.Length)
                throw new InvalidOperationException("Elements xData and yData do not have same number of points");

            byte[] data = new byte[xDataValues.Length * 16]; //length of xdata * 8 + ydata * 8 = xdata * 8 * 2 = xdata * 16
            for (int i = 0; i < xDataValues.Length; i++)
            {
                byte[] xBytes = BitConverter.GetBytes(xDataValues[i]);
                byte[] yBytes = BitConverter.GetBytes(yDataValues[i]);
                Array.Copy(xBytes, 0, data, i * 16, 8);
                Array.Copy(yBytes, 0, data, (i * 16) + 8, 8);
            }

            return data;
        }

        private double[] GetDoubleArrayFromString(string data, char separator)
        {
            string[] stringValues = data.Split(separator);
            double[] doubleValues = new double[stringValues.Length];

            for (int i = 0; i < stringValues.Length; i++)
            {
                double doubleValue;
                if (!double.TryParse(stringValues[i],NumberStyles.Any,CultureInfo.InvariantCulture, out doubleValue))
                    throw new InvalidCastException($"Series data {stringValues[i]} is not numeric");

                doubleValues[i] = doubleValue;
            }

            return doubleValues;
        }

        private IEnumerable<object> GetBinaries(IEnumerable<Schemas.WSXF.Binary_type> wsxfBinaries)
        {
            List<object> wrmlBinaries = new List<object>();

            foreach (Schemas.WSXF.Binary_type wsxfBinary in wsxfBinaries)
            {
                Schemas.WRML.Binary_type wrmlBinary = new Schemas.WRML.Binary_type();
                wrmlBinary.BinaryDataIndex = wsxfBinary.BinaryDataIndex;
                wrmlBinary.FailIdx = wsxfBinary.FailIdx;
                wrmlBinary.FailIdxSpecified = wsxfBinary.FailIdxSpecified;
                //a.StepID
                //a.StepIDSpecified

                wrmlBinary.Data = new Schemas.WRML.Binary_typeData();

                if (wsxfBinary.Data.BinaryDataGUID != null)
                    wrmlBinary.Data.BinaryDataGUID = wsxfBinary.Data.BinaryDataGUID;
                else
                    wrmlBinary.Data.BinaryDataGUID = Guid.NewGuid().ToString();

                wrmlBinary.Data.ContentType = wsxfBinary.Data.ContentType;
                wrmlBinary.Data.FileName = wsxfBinary.Data.FileName;
                wrmlBinary.Data.size = wsxfBinary.Data.size;
                wrmlBinary.Data.sizeSpecified = wsxfBinary.Data.sizeSpecified;
                wrmlBinary.Data.Value = wsxfBinary.Data.Value;

                wrmlBinaries.Add(wrmlBinary);
            }

            return wrmlBinaries;
        }

        private IEnumerable<object> GetFailures(IEnumerable<Schemas.WSXF.Failures_type> wsxfFailures)
        {
            List<object> wrmlFailures = new List<object>();

            foreach (Schemas.WSXF.Failures_type wsxfFailure in wsxfFailures)
            {
                Schemas.WRML.Failures_type wrmlFailure = new Schemas.WRML.Failures_type();
                //a.ArticleDescription
                wrmlFailure.ArticleNumber = wsxfFailure.ArticleNumber;
                wrmlFailure.ArticleRevision = wsxfFailure.ArticleRevision;
                wrmlFailure.ArticleVendor = wsxfFailure.ArticleVendor;
                wrmlFailure.Category = wsxfFailure.Category;
                wrmlFailure.Code = wsxfFailure.Code;
                wrmlFailure.Comment = wsxfFailure.Comment;
                wrmlFailure.CompRef = wsxfFailure.CompRef;
                wrmlFailure.Failcode = wsxfFailure.Failcode;
                wrmlFailure.FunctionBlock = wsxfFailure.FunctionBlock;
                wrmlFailure.Idx = wsxfFailure.Idx;
                wrmlFailure.PartIdx = wsxfFailure.PartIdx;
                wrmlFailure.StepID = wsxfFailure.StepID;

                wrmlFailures.Add(wrmlFailure);
            }

            return wrmlFailures;
        }
    }
}
