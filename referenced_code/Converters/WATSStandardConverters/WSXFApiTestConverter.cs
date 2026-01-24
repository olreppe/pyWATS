using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml;
using System.Xml.Linq;
using Virinco.WATS.Interface;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Integration
{
    public class WSXFApiTestConverter : IReportConverter
    {

        private IDictionary<string, string> arguments;

        public WSXFApiTestConverter(IDictionary<string, string> args)
        {
            arguments = args;
        }

        /// <summary>
        /// IReportConverter inheritance dependancy
        /// </summary>
        public void CleanUp()
        {
        }

        /// <summary>
        /// "Main" function, which also parses out Virinco namespace.
        /// </summary>
        /// <param name="api">TDM Api</param>
        /// <param name="file">XML file</param>
        /// <returns>UUT report</returns>
        public Report ImportReport(TDM api, Stream file)
        {
            UUTReport uut = null;
            UURReport uur = null;

            using (XmlReader reader = XmlReader.Create(file))
            {

                XDocument xdoc = XDocument.Load(reader);
                string response = xdoc.ToString();
                string regexFilter = @" xmlns=""\S+""";
         
                response = Regex.Replace(response, regexFilter, "");
                xdoc = XDocument.Parse(response);

                ReportType reportType = GetReportType(xdoc);

                if (reportType == ReportType.UUT)
                {
                    uut = CreateUUTReport(api, xdoc);
                    return uut;
                }
                else if(reportType == ReportType.UUR)
                {
                    uur = CreateUURReport(api, xdoc);
                    return uur;
                }
                else
                {
                    throw new ArgumentException(@"ImportReport parameter 'ReportType' is invalid. Can only contain 'UUR' or 'UUT'");
                }
            }
        }

        /// <summary>
        /// Inserting XML data to the WATS UUT report
        /// </summary>
        /// <param name="api">TDM Api</param>
        /// <param name="xdoc">XDocument (XML file)</param>
        /// <returns>UUT report</returns>
        public UUTReport CreateUUTReport(TDM api, XDocument xdoc)
        {
            //Root element
            XElement report = xdoc.Element("Reports").Element("Report");

            //Creates variables to handle null exceptions for non-required UUT-header values
            string sequenceName = report.Element("Step").Element("SequenceCall").Attribute("Name")?.Value ?? "";
            string sequenceVersion = report.Element("Step").Element("SequenceCall").Attribute("Version")?.Value ?? "";
            string userLoginName = report.Element("UUT")?.Attribute("UserLoginName")?.Value ?? "";
            string revision = report.Attribute("Rev")?.Value ?? "";

            UUTReport uut = api.CreateUUTReport(
                report.Attribute("PN").Value,
                userLoginName,
                revision,
                report.Attribute("SN").Value,
                report.Element("Process").Attribute("Code").Value,
                sequenceName,
                sequenceVersion);

            if (report.Element("UUT").Attribute("FixtureId") != null) uut.FixtureId = GetElementAttributeOrDefault(report.Element("UUT"), "FixtureId");
            if (report.Element("UUT").Attribute("BatchSN") != null) uut.BatchSerialNumber = GetElementAttributeOrDefault(report.Element("UUT"), "BatchSN");
            if (report.Element("UUT").Attribute("ExecutionTime") != null) uut.ExecutionTime = double.Parse(GetElementAttributeOrDefault(report.Element("UUT"), "ExecutionTime").ToString());
            if (report.Element("UUT").Attribute("ErrorCode") != null) uut.ErrorCode = int.Parse(GetElementAttributeOrDefault(report.Element("UUT"), "ErrorCode"));
            if (report.Element("UUT").Attribute("ErrorMessage") != null) uut.ErrorMessage = GetElementAttributeOrDefault(report.Element("UUT"), "ErrorMessage");
            if (report.Element("UUT").Attribute("TestSocketIndex") != null) uut.TestSocketIndex = short.Parse(GetElementAttributeOrDefault(report.Element("UUT"), "TestSocketIndex"));
            if (report.Element("UUT").Attribute("Comment") != null) uut.Comment = GetElementAttributeOrDefault(report.Element("UUT"), "Comment");
            if (report.Attribute("Result") != null && report.Attribute("Result").Value != null) uut.Status = report.Attribute("Result").Value == "Passed" ? UUTStatusType.Passed : UUTStatusType.Failed;
            if (report.Attribute("Location") != null && report.Attribute("Location").Value != null) uut.Location = report.Attribute("Location").Value;
            if (DateTime.Parse(report.Attribute("Start").Value) != null)
            {
                uut.StartDateTime = DateTime.Parse(report.Attribute("Start").Value, null, DateTimeStyles.RoundtripKind);
            }
            else
            {
                throw new ArgumentNullException("'Start' datetime must be specified. Cannot find attribute 'Start' in <Report> element");
            }
            if (uut.StartDateTime.ToUniversalTime() != null) uut.StartDateTimeUTC = uut.StartDateTime.ToUniversalTime();

            //Fetches all miscInfo xElements and adds them to the UUTReport as MiscUUTInfo
            List<XElement> miscInfoElements = report.Elements().Where(e => e.Name.LocalName.Contains("MiscInfo")).ToList();
            foreach (XElement miscElement in miscInfoElements)
            {
                try
                {
                    if (miscElement.Value != null && miscElement.Attribute("Numeric") != null)
                    {
                        uut.AddMiscUUTInfo(
                            miscElement.Attribute("Description").Value,
                            miscElement.Value,
                            short.Parse(GetElementAttributeOrDefault(miscElement, "Numeric")));
                    }
                    else if (miscElement.Value == null && miscElement.Attribute("Numeric") != null)
                    {
                        uut.AddMiscUUTInfo(
                            miscElement.Attribute("Description").Value,
                            short.Parse(GetElementAttributeOrDefault(miscElement, "Numeric")));
                    }
                    else if (miscElement.Value != null && miscElement.Attribute("Numeric") == null)
                    {
                        uut.AddMiscUUTInfo(
                            miscElement.Attribute("Description").Value,
                            miscElement.Value);
                    }
                    else uut.AddMiscUUTInfo(miscElement.Attribute("Description").Value);
                }
                catch
                {
                    throw new ArgumentNullException("MiscElement must have a description");
                }
            }

            // Fetches all Sub units xElements and adds them into the UUTReport as ReportUnitHierarchy
            List<XElement> subUnitElements = report.Elements().Where(e => e.Name.LocalName.Contains("ReportUnitHierarchy")).ToList();
            foreach (XElement subElement in subUnitElements)
            {
                try
                {
                    if ((subElement.Attribute("PartType").Value != null) && (subElement.Attribute("SN").Value != null))
                    {
                        uut.AddUUTPartInfo(
                            subElement.Attribute("PartType").Value,
                            GetElementAttributeOrDefault(subElement, "PN"),
                            subElement.Attribute("SN").Value,
                            GetElementAttributeOrDefault(subElement, "Rev"));
                    }
                }
                catch (ArgumentNullException)
                {
                    throw new ArgumentNullException("ReportUnitHierarchy must minimun have a PartType and a Serial Number");
                }
            }

            //Defines the root step for the 'body' part of the XML file
            XElement rootStep = report.Element("Step");

            //Reads all data from root element to document end. 
            ReadUUTSteps(api, rootStep, uut.GetRootSequenceCall());
            return uut;
        }

        /// <summary>
        /// Creates a UUR report
        /// </summary>
        /// <param name="api">TDM api</param>
        /// <param name="xdoc">xml document</param>
        /// <param name="uutReportID">Referenced UUT Id/GUID</param>
        /// <returns></returns>
        public UURReport CreateUURReport(TDM api, XDocument xdoc)
        {
            UURReport uurReport = null;
            XElement report = xdoc.Element("Reports").Element("Report");
            string operatorName = report.Element("UUR").Attribute("UserLoginName").Value;
            string uutReportID = report.Element("UUR").Attribute("ReferencedUUT")?.Value ?? "";
            RepairType repairType = GetRepairType(api, xdoc);
            OperationType operationType = GetOperationType(api, xdoc);


            if (string.IsNullOrEmpty(uutReportID))
            {
                try
                {
                    UURReport uur = api.CreateUURReport(operatorName, GetRepairType(api, xdoc), GetReferencedUUTReport(api, uutReportID));
                    uurReport = uur;
                }
                catch
                {
                    throw new ArgumentException($"Could not find UUT report with ID {uutReportID}.");
                }
            }
            else
            {
                try
                {
                    UURReport uur = api.CreateUURReport(operatorName, repairType, operationType, report.Attribute("SN").Value, report.Attribute("PN").Value, report.Attribute("Rev").Value);
                    uurReport = uur;
                }
                catch
                {
                    throw new ArgumentException($"Error related to CreateUURReport");
                }
            }

            if (IsDefined(report, "Purpose")) uurReport.Purpose = (report.Attribute("Purpose").Value);
            if (IsDefined(report, "Location")) uurReport.Location = (report.Attribute("Location").Value);
            if (IsDefined(report, "MachineName")) uurReport.StationName = (report.Attribute("MachineName").Value);

            if (IsDefined(report, "Start")) uurReport.StartDateTime = DateTime.ParseExact(report.Attribute("Start").Value.Substring(0, 23), "yyyy-MM-ddTHH:mm:ss.fff", CultureInfo.InvariantCulture);
            if (IsDefined(report, "Start_utc")) uurReport.StartDateTimeUTC = uurReport.StartDateTime.ToUniversalTime();
            else
            {
                throw new Exception("Start_utc must be set, but can be null");
            }

            if (report.Element("UUR").Element("Comment") != null) uurReport.Comment = report.Element("UUR").Element("Comment").Value;
            if (IsDefined(report.Element("UUR"), "ExecutionTime")) uurReport.ExecutionTime = double.Parse(report.Element("UUR").Attribute("ExecutionTime").Value);
            if (IsDefined(report.Element("UUR"), "ConfirmDate")) uurReport.Confirmed = DateTime.ParseExact(report.Element("UUR").Attribute("ConfirmDate").Value.Substring(0, 23), "yyyy-MM-ddTHH:mm:ss.fff", CultureInfo.InvariantCulture);
            if (IsDefined(report.Element("UUR"), "FinalizeDate")) uurReport.Finalized = DateTime.ParseExact(report.Element("UUR").Attribute("FinalizeDate").Value.Substring(0, 23), "yyyy-MM-ddTHH:mm:ss.fff", CultureInfo.InvariantCulture);

            List<XElement> miscInfoElements = report.Elements().Where(e => e.Name.LocalName.Contains("MiscInfo")).ToList();
            foreach (XElement miscElement in miscInfoElements)
            {
                try
                {
                    uurReport.MiscInfo[miscElement.Attribute("Description").Value] = miscElement.Value;
                }
                catch
                {
                    throw new ArgumentNullException($"MiscInfo description {miscElement.Attribute("Description").Value} is not defined in repair type  {repairType.Code} {repairType.Description}");
                }
            }

            List<XElement> partInfoElements = report.Elements().Where(e => e.Name.LocalName.Contains("ReportUnitHierarchy")).ToList();
            foreach (XElement partinfo in partInfoElements)
            {
                try
                {
                    uurReport.AddUURPartInfo(partinfo.Attribute("PN").Value, partinfo.Attribute("SN").Value, partinfo.Attribute("Rev").Value);
                }
                catch
                {
                    throw new ArgumentException($"PartInfo could not be added because one or more of the required attributes is null. PN:{partinfo.Attribute("PN").Value}, SN:{partinfo.Attribute("SN").Value}, Revision:{partinfo.Attribute("Rev").Value}");
                }
            }

            List<XElement> failureElements = report.Elements().Where(e => e.Name.LocalName.Contains("Failures")).ToList();

            //Fetches all RootFailCodes from the given RepairType
            FailCode[] repairCategories = api.GetRootFailCodes(repairType);

            foreach (XElement failure in failureElements)
            {
                FailCode category;

                if(string.IsNullOrEmpty(failure.Attribute("Category").Value))
                {
                    //Require atleast one repair category for a repair type.
                    if(repairCategories.Length < 1)
                        throw new ArgumentException($"No repair category was found in process {repairType.Name}");
                    else if (repairCategories.Length > 1)
                        throw new ArgumentException($"Cannot identify repair code without specifying repair category because {repairType.Name} contains more than one category");
                    else
                    {
                        category = repairCategories.Single();
                    }
                }

                else
                {
                    category = repairCategories.Where(c => c.Description == failure.Attribute("Category").Value).SingleOrDefault();
                    if(category == null)
                    {
                        throw new ArgumentException($"Repair category {failure.Attribute("Category").Value} was not found in process {repairType.Name}");
                    }
                }

                FailCode code = api.GetChildFailCodes(category).Where(c => c.Description == failure.Attribute("Code").Value).SingleOrDefault();
                if(code==null)
                {
                    throw new ArgumentException($"Repair code {failure.Attribute("Code").Value} in category {failure.Attribute("Category").Value} was not found in process {repairType.Name}");
                }

                Failure uurFailure = uurReport.AddFailure(code, failure.Attribute("CompRef").Value, failure.Element("Comment").Value, int.Parse(failure.Attribute("StepID").Value));

                if (IsDefined(failure, "FunctionBlock")) uurFailure.ComprefFunctionBlock = failure.Attribute("FunctionBlock").Value;
                if (IsDefined(failure, "ArticleNumber")) uurFailure.ComprefArticleNumber = failure.Attribute("ArticleNumber").Value;
                if (IsDefined(failure, "ArticleRevision")) uurFailure.ComprefArticleRevision = failure.Attribute("ArticleRevision").Value;
                if (IsDefined(failure, "ArticleVendor")) uurFailure.ComprefArticleVendor = failure.Attribute("ArticleVendor").Value;

                int failureIndex = int.Parse(failure.Attribute("PartIdx").Value);

                List<XElement> attachments = report.Elements().Where(e => e.Name.LocalName.Contains("Binary")).ToList();
                foreach (XElement attachment in attachments)
                {
                    if(int.Parse(attachment.Attribute("FailIdx").Value) == failureIndex)
                    {
                        string byteValues;
                        if (attachment.Element("Data").Value != null)
                        {
                            byteValues = attachment.Element("Data").Value;
                            byte[] content = Encoding.Unicode.GetBytes(byteValues);
                            string fileName = attachment.Element("Data").Attribute("FileName").Value;
                            string contentType = attachment.Element("Data").Attribute("ContentType").Value;

                            uurFailure.AddAttachment(content, fileName, contentType);
                        }
                    }
                }
            }
            return uurReport;
        }


        /// <summary>
        /// Reads all data from root-element to XML-document end.
        /// </summary>
        /// <param name="api">TDM api</param>
        /// <param name="rootStep">Root element</param>
        /// <param name="rootSequence">Root sequence</param>
        private void ReadUUTSteps(TDM api, XElement rootStep, SequenceCall rootSequence)
        {
            foreach (XElement subStep in rootStep.Elements().Where(e => e.Name.LocalName.Contains("Step")))
            {
                string name = "";
                if (subStep.Attribute("Name") != null) name = subStep.Attribute("Name").Value;

                //Adds sequence calls if they exist, then calls "ReadSteps" with the new sequenceCall if one exist. 
                XElement seqCall = subStep.Descendants().Where(e => e.Name.LocalName.Contains("SequenceCall")).FirstOrDefault();
                if (seqCall != null && seqCall.Attribute("Name").Value != rootSequence.Name)
                {
                    SequenceCall newSeq = rootSequence.AddSequenceCall(name,
                        seqCall.Attribute("Name")?.Value ?? "",
                        seqCall.Attribute("Version")?.Value ?? "");

                    ReadUUTSteps(api, subStep, newSeq);
                }
                else
                {
                    //Used to add attachments such as Chart and Files to a given step.
                    Step step = null;

                    List<XElement> NumericSteps = subStep.Elements("NumericLimit").ToList();
                    List<XElement> StringValueSteps = subStep.Elements("StringValue").ToList();
                    List<XElement> PassFailSteps = subStep.Elements("PassFail").ToList();
                    List<XElement> AttachmentSteps = subStep.Elements("Attachment").ToList();
                    List<XElement> ChartSteps = subStep.Elements("Chart").ToList();
                    List<XElement> AdditionalResultSteps = subStep.Elements("AdditionalResult").ToList();
                    List<XElement> ExecutableSteps = subStep.Elements("Callexe").ToList();
                    List<XElement> MessagePopUpSteps = subStep.Elements("MessagePopup").ToList();

                    //CHECKS IF ANY OF THE LISTS CONTAINS A COUNT > 1
                    if(NumericSteps.Count != 0  ||       StringValueSteps.Count != 0 ||    PassFailSteps.Count != 0 ||  AttachmentSteps.Count != 0 || 
                       ChartSteps.Count != 0    ||  AdditionalResultSteps.Count != 0 ||  ExecutableSteps.Count != 0 || MessagePopUpSteps.Count != 0)
                    {
                        //NUMERICVALUE
                        if (NumericSteps.Count > 0)
                        {
                            if (NumericSteps.Count > 1)
                            {
                                try
                                {
                                    step = AddMultipleNumericTest(rootSequence, NumericSteps, name);
                                }
                                catch
                                {
                                    throw new ArgumentNullException("MultipleNumeric steps must have a name for each step.");
                                }
                            }
                            else
                            {
                                step = AddSingleNumericTest(rootSequence, NumericSteps, name);
                            }
                        }

                        //STRINGVALUE
                        else if (StringValueSteps.Count > 0)
                        {
                            if (StringValueSteps.Count > 1)
                            {
                                try
                                {
                                    step = AddMultipleStringValueTest(rootSequence, StringValueSteps, name);
                                }
                                catch
                                {
                                    throw new ArgumentNullException("MultipleStringValue steps must have a name for each step.");
                                }
                            }
                            else
                            {
                                step = AddSingleStringValueTest(rootSequence, StringValueSteps, name);
                            }
                        }

                        //PASSFAIL
                        else if (PassFailSteps.Count > 0)
                        {
                            if (PassFailSteps.Count > 1)
                            {
                                try
                                {
                                    step = AddMultiplePassFailTest(rootSequence, PassFailSteps, name);
                                }
                                catch
                                {
                                    throw new ArgumentNullException("MultiplePassFail steps must have a name for each step.");
                                }
                            }
                            else
                            {
                                step = AddSinglePassFailTest(rootSequence, PassFailSteps, name);
                            }
                        }

                        //CALLEXECUTABLE 
                        else if (ExecutableSteps.Count > 0)
                        {
                            step = AddExecutableStep(rootSequence, ExecutableSteps, name);
                        }

                        else if (MessagePopUpSteps.Count > 0)
                        {
                            step = AddMessagePopUpStep(rootSequence, MessagePopUpSteps, name);
                        }

                        //ADDITIONALRESULT
                        else if (AdditionalResultSteps.Count > 0)
                        {
                            AddAdditionalResult(rootSequence, AdditionalResultSteps, name);
                        }

                        //CHARTDATA
                        if (ChartSteps.Count > 0)
                        {
                            if (ChartSteps.Count == 1) AddGraphToStep(step, ChartSteps);
                            else throw new ArgumentException("There can only be one chart-type for each step.");
                        }

                        //ATTACHMENT
                        if (AttachmentSteps.Count > 0)
                        {
                            if (step != null)
                            {
                                AddAttachmentToStep(step, AttachmentSteps);
                            }
                            else
                            {
                                GenericStep gStep = rootSequence.AddGenericStep(GenericStepTypes.Action, name);
                                step = gStep;
                                AddAttachmentToStep(step, AttachmentSteps);
                            }
                        }

                        if (step == null) step = rootSequence.AddSequenceCall(rootSequence.Name);
                        CreateUUTStepHeader(step, subStep);
                    }
                    
                    //ADDS A GENERICSTEP IF NONE OF THE ABOVE WAS FOUND.
                    else
                    {
                        AddGenericSteps(rootSequence, name, subStep);
                    }      
                }
            }
        }

        /// <summary>
        /// Creates a step header to each step
        /// </summary>
        /// <param name="step">Steptype such as numericLimit, StringValue etc</param>
        /// <param name="ex">Test Xelement</param>
        private void CreateUUTStepHeader(Step step, XElement ex)
        {
            if (ex.Attribute("Name") != null) step.Name = ex.Attribute("Name").Value;
            if (ex.Attribute("StepType") != null) step.StepType = GetElementAttributeOrDefault(ex, "StepType");
            if (ex.Attribute("total_time") != null) step.StepTime = double.Parse(GetElementAttributeOrDefault(ex, "total_time"));
            if (ex.Attribute("Group") != null && ex.Attribute("Group").Value != null) step.StepGroup = (Interface.StepGroupEnum)Enum.Parse(typeof(Virinco.WATS.Interface.StepGroupEnum), ex.Attribute("Group").Value);
            if (ex.Attribute("Status") != null && ex.Attribute("Status").Value != null) step.Status = (StepStatusType)Enum.Parse(typeof(StepStatusType), ex.Attribute("Status").Value);
        }

        /// <summary>
        /// Adds a multiple-numeric test to the UUT report
        /// </summary>
        /// <param name="parentsequence">SequenceCall</param>
        /// <param name="multipleNumTests">List of multiple numericlimitsteps</param>
        /// <param name="name">Name of step</param>
        /// <returns></returns>
        private NumericLimitStep AddMultipleNumericTest(SequenceCall parentsequence, List<XElement> multipleNumTests, string name)
        {
            //DET MÅ DA FINNES EN MÅTE Å GJØRE DETTE BEDRE PÅ? 
            NumericLimitStep nls = parentsequence.AddNumericLimitStep(name);

            foreach (XElement numstep in multipleNumTests)
            {
                CompOperatorType op;
                StepStatusType status;

                //Value, CompOperator, Lowlimit, Highlimit, Units, Name and Status
                if (numstep.Attribute("LowLimit") != null && numstep.Attribute("HighLimit") != null && numstep.Attribute("CompOperator") != null && numstep.Attribute("Status") != null)
                {
                    op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numstep.Attribute("CompOperator").Value);
                    status = (StepStatusType)Enum.Parse(typeof(StepStatusType), numstep.Attribute("Status").Value);

                    nls.AddMultipleTest(XElementAttributeValue(numstep, "NumericValue", 0),
                                        op,
                                        XElementAttributeValue(numstep, "LowLimit", 0),
                                        XElementAttributeValue(numstep, "HighLimit", 0),
                                        XElementAttributeValue(numstep, "Units", ""),
                                        XElementAttributeValue(numstep, "Name", ""),
                                        status);
                }
                //Value, CompOperator, Lowlimit, Highlimit, Units and Name
                else if (numstep.Attribute("LowLimit") != null && numstep.Attribute("HighLimit") != null && numstep.Attribute("CompOperator") != null)
                {
                    op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numstep.Attribute("CompOperator").Value);

                    //nls.AddTest(XElementAttributeValue(numstep, "NumericValue", 0),
                    //                    op,
                    //                    XElementAttributeValue(numstep, "LowLimit", 0),
                    //                    XElementAttributeValue(numstep, "HighLimit", 0),
                    //                    XElementAttributeValue(numstep, "Units", ""),
                    //                    XElementAttributeValue(numstep, "Name", ""));
                }
                //Value, CompOperator, Highlimit, Units and Name
                else if (numstep.Attribute("LowLimit") == null && numstep.Attribute("HighLimit") != null && numstep.Attribute("CompOperator") != null)
                {
                    op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numstep.Attribute("CompOperator").Value);
                    nls.AddMultipleTest(XElementAttributeValue(numstep, "NumericValue", 0),
                                        op,
                                        XElementAttributeValue(numstep, "HighLimit", 0),
                                        XElementAttributeValue(numstep, "Units", ""),
                                        XElementAttributeValue(numstep, "Name", ""));
                }
                //Value, CompOperator, LowLimit, Units and Name
                else if (numstep.Attribute("HighLimit") == null && numstep.Attribute("LowLimit") != null && numstep.Attribute("CompOperator") != null)
                {
                    op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numstep.Attribute("CompOperator").Value);
                    nls.AddMultipleTest(XElementAttributeValue(numstep, "NumericValue", 0),
                                        op,
                                        XElementAttributeValue(numstep, "LowLimit", 0),
                                        XElementAttributeValue(numstep, "Units", ""),
                                        XElementAttributeValue(numstep, "Name", ""));
                }
                //Value, units and name.
                else
                {
                    nls.AddMultipleTest(XElementAttributeValue(numstep, "NumericValue", 0),
                                        XElementAttributeValue(numstep, "Units", ""),
                                        XElementAttributeValue(numstep, "Name", ""));
                }
            }
            return nls;
        }

        /// <summary>
        /// Adds a single-numeric test to the UUT report
        /// </summary>
        /// <param name="parentsequence">SequenceCall</param>
        /// <param name="multipleNumTests">List of single numericlimitsteps (as single)</param>
        /// <param name="name">Name of step</param>
        /// <returns></returns>>
        private NumericLimitStep AddSingleNumericTest(SequenceCall parentsequence, List<XElement> NumTest, string name)
        {
            //DET MÅ DA FINNES EN MÅTE Å GJØRE DETTE BEDRE PÅ? 
            NumericLimitStep nls = parentsequence.AddNumericLimitStep(name);
            XElement numElement = NumTest.Single();

            CompOperatorType op;
            StepStatusType status;

            //Value, CompOperator, Lowlimit, Highlimit, Units, Name and Status
            if (numElement.Attribute("LowLimit") != null && numElement.Attribute("HighLimit") != null && numElement.Attribute("CompOperator") != null && numElement.Attribute("Status") != null)
            {
                op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numElement.Attribute("CompOperator").Value);
                status = (StepStatusType)Enum.Parse(typeof(StepStatusType), numElement.Attribute("Status").Value);

                nls.AddTest(XElementAttributeValue(numElement, "NumericValue", 0),
                                    op,
                                    XElementAttributeValue(numElement, "LowLimit", 0),
                                    XElementAttributeValue(numElement, "HighLimit", 0),
                                    XElementAttributeValue(numElement, "Units", ""),
                                    status);
            }

            //Value, CompOperator, Lowlimit, Highlimit, Units and Name
            else if (numElement.Attribute("LowLimit") != null && numElement.Attribute("HighLimit") != null && numElement.Attribute("CompOperator") != null)
            {
                op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numElement.Attribute("CompOperator").Value);

                nls.AddTest(XElementAttributeValue(numElement, "NumericValue", 0),
                                    op,
                                    XElementAttributeValue(numElement, "LowLimit", 0),
                                    XElementAttributeValue(numElement, "HighLimit", 0),
                                    XElementAttributeValue(numElement, "Units", ""));
            }
            //Value, CompOperator, Highlimit, Units and Name
            else if (numElement.Attribute("LowLimit") == null && numElement.Attribute("HighLimit") != null && numElement.Attribute("CompOperator") != null)
            {
                op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numElement.Attribute("CompOperator").Value);

                nls.AddTest(XElementAttributeValue(numElement, "NumericValue", 0),
                                    op,
                                    XElementAttributeValue(numElement, "HighLimit", 0),
                                    XElementAttributeValue(numElement, "Units", ""));
            }
            //Value, CompOperator, LowLimit, Units and Name
            else if (numElement.Attribute("HighLimit") == null && numElement.Attribute("LowLimit") != null && numElement.Attribute("CompOperator") != null)
            {
                op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), numElement.Attribute("CompOperator").Value);

                nls.AddTest(XElementAttributeValue(numElement, "NumericValue", 0),
                                    op,
                                    XElementAttributeValue(numElement, "LowLimit", 0),
                                    XElementAttributeValue(numElement, "Units", ""));
            }
            else if (numElement.Attribute("HighLimit") == null && numElement.Attribute("LowLimit") != null && numElement.Attribute("CompOperator") != null)
            {
                status = (StepStatusType)Enum.Parse(typeof(StepStatusType), numElement.Attribute("Status").Value);

                nls.AddTest( XElementAttributeValue(numElement, "NumericValue", 0),
                                    XElementAttributeValue(numElement, "Units", ""),
                                    status);
            }
            //Value, units and name.
            else
            {
                nls.AddTest(XElementAttributeValue(numElement, "NumericValue", 0),
                                    XElementAttributeValue(numElement, "Units", ""));
            }
            return nls;
        }

        /// <summary>
        /// Adds a multiple-StringValue-test to the UUT report
        /// </summary>
        /// <param name="parentsequence">SequenceCall</param>
        /// <param name="multipleNumTests">List of multiple StringValues</param>
        /// <param name="name">Name of step</param>
        /// <returns></returns>>
        private StringValueStep AddMultipleStringValueTest(SequenceCall parentsequence, List<XElement> StringTest, string name)
        {
            StringValueStep svs = parentsequence.AddStringValueStep(name);
            CompOperatorType op;
            StepStatusType stepResult;

            foreach (XElement s in StringTest)
            {
                //CompOperator, value, Limit, name, result
                if (s.Attribute("Status") != null && s.Attribute("CompOperator") != null)
                {
                    op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), s.Attribute("CompOperator").Value);
                    stepResult = (StepStatusType)Enum.Parse(typeof(StepStatusType), s.Attribute("Status").Value);

                    svs.AddMultipleTest(op,
                        XElementAttributeValue(s, "StringValue", ""),
                        XElementAttributeValue(s, "StringLimit", ""),
                        XElementAttributeValue(s, "Name", ""),
                        stepResult);

                }
                //CompOperator, value and limit, name
                else if (s.Attribute("CompOperator") != null)
                {
                    op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), s.Attribute("CompOperator").Value);

                    svs.AddMultipleTest(op,
                        XElementAttributeValue(s, "StringValue", ""),
                        XElementAttributeValue(s, "StringLimit", ""),
                        XElementAttributeValue(s, "Name", ""));
                }
                //Value and Name
                else
                {
                    svs.AddMultipleTest(XElementAttributeValue(s, "StringValue", ""), XElementAttributeValue(s, "Name", ""));
                }
            }

            return svs;
        }

        /// <summary>
        /// Adds a single StringValue-test to the UUT report
        /// </summary>
        /// <param name="parentsequence">SequenceCall</param>
        /// <param name="multipleNumTests">List of StringValues (as single) </param>
        /// <param name="name">Name of step</param>
        /// <returns></returns>>
        private StringValueStep AddSingleStringValueTest(SequenceCall parentsequence, List<XElement> StringTest, string name)
        {
            //DET MÅ DA FINNES EN MÅTE Å GJØRE DETTE BEDRE PÅ? 
            StringValueStep svs = parentsequence.AddStringValueStep(name);
            XElement stringElement = StringTest.Single();
            CompOperatorType op;
            StepStatusType stepResult;

            //CompOperator, value, Limit, result
            if (stringElement.Attribute("Status") != null && stringElement.Attribute("CompOperator") != null)
            {
                op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), stringElement.Attribute("CompOperator").Value);
                stepResult = (StepStatusType)Enum.Parse(typeof(StepStatusType), stringElement.Attribute("Status").Value);

                svs.AddTest(op, 
                    XElementAttributeValue(stringElement, "StringValue", ""), 
                    XElementAttributeValue(stringElement, "StringLimit", ""), 
                    stepResult);
                
            }
            //CompOperator, value and limit
            else if (stringElement.Attribute("CompOperator") != null)
            {
                op = (CompOperatorType)Enum.Parse(typeof(CompOperatorType), stringElement.Attribute("CompOperator").Value);

                svs.AddTest(op, 
                    XElementAttributeValue(stringElement, "StringValue", ""), 
                    XElementAttributeValue(stringElement, "StringLimit", ""));
            }
            //Value and status
            else if (stringElement.Attribute("Status") != null)
            {
                stepResult = (StepStatusType)Enum.Parse(typeof(StepStatusType), stringElement.Attribute("Status").Value);

                svs.AddTest(XElementAttributeValue(stringElement, "StringValue", ""), stepResult);
            }
            //Value
            else
            {
                svs.AddTest(XElementAttributeValue(stringElement, "StringValue", ""));

            }
            return svs;
        }

        /// <summary>
        /// Adds a multiple-PassFail-test to the UUT report
        /// </summary>
        /// <param name="parentsequence">SequenceCall</param>
        /// <param name="multipleNumTests">List of multiple PassFailTests</param>
        /// <param name="name">Name of step</param>
        /// <returns></returns>>
        private PassFailStep AddMultiplePassFailTest(SequenceCall parentsequence, List<XElement> PassFailTest, string name)
        {
            PassFailStep pfs = parentsequence.AddPassFailStep(name);
            StepStatusType status;

            foreach (XElement t in PassFailTest)
            {
                status = (StepStatusType)Enum.Parse(typeof(StepStatusType), t.Attribute("Status").Value);
                
                if(t.Attribute("Status").Value == "Passed")
                {
                    pfs.AddMultipleTest(
                    true,
                    t.Attribute("Name").Value,
                    status);
                }
                else
                {
                    pfs.AddMultipleTest(
                    false,
                    t.Attribute("Name").Value,
                    status);
                }
            }
            return pfs;
        }

        /// <summary>
        /// Adds a Single-PassFail-test to the UUT report
        /// </summary>
        /// <param name="parentsequence">SequenceCall</param>
        /// <param name="multipleNumTests">List of single PassFailTests (as single)</param>
        /// <param name="name">Name of step</param>
        /// <returns></returns>>
        private PassFailStep AddSinglePassFailTest(SequenceCall parentsequence, List<XElement> PassFailTest, string name)
        {
            PassFailStep pfs = parentsequence.AddPassFailStep(name);
            XElement passFailStep = PassFailTest.Single();
            StepStatusType status;

            if (passFailStep.Attribute("Status").Value == "Passed")
            {
                status = (StepStatusType)Enum.Parse(typeof(StepStatusType), passFailStep.Attribute("Status").Value);
                pfs.AddTest(true, status);
            }
            else
            {
                status = (StepStatusType)Enum.Parse(typeof(StepStatusType), passFailStep.Attribute("Status").Value);
                pfs.AddTest(false, status);
            }
            return pfs;
        }

        /// <summary>
        /// Adds a Message-Popup-step to the UUT report.
        /// </summary>
        /// <param name="parentSequence"></param>
        /// <param name="messagePopUpResult"></param>
        /// <param name="name"></param>
        /// <returns></returns>
        private MessagePopupStep AddMessagePopUpStep(SequenceCall parentSequence, List<XElement> messagePopUpResult, string name)
        {
            XElement mPopUpStep = messagePopUpResult.Single();
            MessagePopupStep popUp = parentSequence.AddMessagePopupStep(name, short.Parse(mPopUpStep.Attribute("Button").Value), mPopUpStep.Attribute("Response").Value);
            return popUp;
        }

        /// <summary>
        /// Reads the report header and checks for keywords "UUT" or "UUR" to dertermine report type.
        /// </summary>
        /// <param name="xdoc">xml file</param>
        /// <returns></returns>
        private ReportType GetReportType(XDocument xdoc)
        {
            ReportType reportType;
            string reportTypeValue = xdoc.Element("Reports").Element("Report").Attribute("type").Value.ToLower();
            if(reportTypeValue != null && reportTypeValue == "uut" || reportTypeValue == "uur")
            {
                reportType = xdoc.Element("Reports").Element("Report").Attribute("type").Value == "UUT" ? ReportType.UUT : ReportType.UUR;
            }
            else
            {
                throw new ArgumentException($"Report element must have a valid type (UUT or UUR)");
            }
            return reportType;
        }

        /// <summary>
        /// Adds a Executable step
        /// </summary>
        /// <param name="parentSequence">SequenceCall</param>
        /// <param name="ExeSteps">List of Executable steps</param>
        /// <param name="name">Name of parent step</param>
        /// <returns></returns>
        private CallExeStep AddExecutableStep(SequenceCall parentSequence, List<XElement> ExeSteps, string name)
        {
            XElement callExe = ExeSteps.Single();
            double exitCode = double.Parse(callExe.Attribute("ExitCode").Value);
            CallExeStep executable = parentSequence.AddCallExeStep(name, exitCode);
            return executable;
        }
        /// <summary>
        /// Adds a Generic step to the UUT report
        /// </summary>
        /// <param name="parentSequence">SequenceCall</param>
        /// <param name="name">List of Executable steps</param>
        /// <param name="step">Name of parent step</param>
        /// <returns></returns>
        private GenericStep AddGenericSteps(SequenceCall parentSequence, string name, XElement step)
        {
            if(step.Attribute("StepType") != null && step.Attribute("StepType").Value != null)
            {
                GenericStep genericStep; 

                try
                {
                    GenericStepTypes stepType = (GenericStepTypes)Enum.Parse(typeof(GenericStepTypes), step.Attribute("StepType").Value);
                    genericStep = parentSequence.AddGenericStep(stepType, name);
                }
                catch
                {
                    throw new ArgumentException($" {step.Attribute("StepType").Value} is not a valid GenericStepType.");
                }
                return genericStep;
            }
            else
            {
                throw new Exception($"{step.Name} does not contain attribute 'StepType' which is required for GenericSteps.");
            }

        }

        /// <summary>
        /// Adds a AdditionalResult to the UUT report
        /// </summary>
        /// <param name="parentSequence">SequenceCall</param>
        /// <param name="additionalResults">List of additional results</param>
        /// <param name="name">Name of step</param>
        /// <returns></returns>
        private void AddAdditionalResult(SequenceCall parentSequence, List<XElement> additionalResults, string name)
        {
            XElement additionalResult = additionalResults.Single();
            AdditionalResult result = parentSequence.AddAdditionalResult(name, additionalResult);
        }

        /// <summary>
        /// Adds a Chart/Graph to a given step.
        /// "Step" type is used to be able to add chart to all step types (numeric, stringValue, pass/fail etc).
        /// </summary>
        /// <param name="parentStep">Step which contains an attached Chart</param>
        /// <param name="Charts">List of Charts (as single)</param>
        private void AddGraphToStep(Step parentStep, List<XElement> Charts)
        {
            XElement listStep = Charts.Single();

            Chart chart = parentStep.AddChart(
                             (ChartType)Enum.Parse(typeof(ChartType), listStep.Attribute("ChartType").Value),
                             GetElementAttributeOrDefault(listStep, "Label"),
                             GetElementAttributeOrDefault(listStep, "XLabel"),
                             GetElementAttributeOrDefault(listStep, "XUnit"),
                             GetElementAttributeOrDefault(listStep, "YLabel"),
                             GetElementAttributeOrDefault(listStep, "YUnit"));

            List<XElement> graphSeries = listStep.Descendants().Where(e => e.Name.LocalName.Contains("Series")).ToList();

            foreach (XElement series in graphSeries)
            {
                double[] xVals = GetDoubleFromString(series.Element("xdata").Value);
                double[] yVals = GetDoubleFromString(series.Element("ydata").Value);

                //Series DataType is sat by the Addseries function.
                chart.AddSeries(series.Name.ToString(), xVals, yVals);
            }
        }

        /// <summary>
        /// Adds a attachment (file) to a step
        /// </summary>
        /// <param name="parentStep">Step which contains an attached file</param>
        /// <param name="Attachments">List of attachments</param>
        private void AddAttachmentToStep(Step parentStep, List<XElement> Attachments)
        {
            foreach (XElement attachment in Attachments)
            {
                string byteValues = attachment.Value;
                parentStep.AttachByteArray(GetElementAttributeOrDefault(attachment, "Name"), Encoding.Unicode.GetBytes(byteValues), GetElementAttributeOrDefault(attachment, "ContentType"));
            }
            //XElement attachmentStep = Attachments.Single();
            //seqCall.AttachFile(GetElementAttrib uteOrDefault(xe, "Name"), false);
        }

        /// <summary>
        /// Checks if an element has a given attribute, and that the attribute contains a value 
        /// </summary>
        /// <param name="element"></param>
        /// <param name="attribute"></param>
        /// <returns></returns>
        public bool IsDefined(XElement element, string attribute)
        {
            bool status;

            if (element.Attribute(attribute) != null)
            {
                if (element.Attribute(attribute).Value != null && element.Attribute(attribute).Value != "")
                    status = true;
                else
                    status = false;
            }
            else
                status = false;
            return status;
        }

        /// <summary>
        /// Fetches the repait type in the process element and verfy that it exists.
        /// </summary>
        /// <param name="api"></param>
        /// <param name="xdoc"></param>
        /// <returns></returns
        public RepairType GetRepairType(TDM api, XDocument xdoc)
        {
            XAttribute processCode = xdoc.Element("Reports").Element("Report").Element("Process").Attribute("Code");
            RepairType repairType;

            try
            {
                repairType = api.GetRepairTypes().Where(r => r.Code == short.Parse(processCode.Value)).Single();
            }
            catch
            {
                throw new ArgumentException($"Process with code {processCode.Value} does not exist");
            }
            return repairType;
        }

        /// <summary>
        /// Fetches the operation type in the UUR element and verfy that it exists.
        /// </summary>
        /// <param name="api"></param>
        /// <param name="xdoc"></param>
        /// <returns></returns>
        public OperationType GetOperationType(TDM api, XDocument xdoc)
        {
            XAttribute processCode = xdoc.Element("Reports").Element("Report").Element("UUR").Element("Process").Attribute("Code");
            OperationType operationType;

            try
            {
                operationType = api.GetOperationTypes().Where(r => r.Code == processCode.Value).Single();
            }
            catch
            {
                throw new ArgumentException($"Process with code {processCode.Value} does not exist");
            }
            return operationType;
        }

        /// <summary>
        /// Loads a UUT report based on reportID
        /// </summary>
        /// <param name="api"></param>
        /// <param name="reportID"></param>
        /// <returns></returns>
        public UUTReport GetReferencedUUTReport(TDM api, string reportID)
        {
            Report report = api.LoadReport(reportID);
            return report as UUTReport;
        }

        /// <summary>
        /// Takes a string and splits it based on ";" then insert the values as doubles in a array
        /// </summary>
        /// <param name="data">String which contains chart data</param>
        /// <returns></returns>
        private double[] GetDoubleFromString(string data)
        {
            string[] strValues = data.Split(new char[] { ';' });
            double[] d = new double[strValues.Length];
            for (int i = 0; i < strValues.Length; i++)
            {
                d[i] = Double.Parse(strValues[i], CultureInfo.InvariantCulture);
            }
            return d;
        }

        /// <summary>
        /// Help-method to extract Attribute-value from a Xelement
        /// </summary>
        /// <param name="el">Xelement</param>
        /// <param name="attribute">Attribute name</param>
        /// <returns></returns>
        private string GetElementAttributeOrDefault(XElement el, string attribute)
        {
            if (el.Attribute(attribute) == null) return null;
            if (el.Attribute(attribute).Value != null) return el.Attribute(attribute).Value.ToString();
            else return "";
        }

        /// <summary>
        /// Help-method to extract Attribute-value from a Xelement
        /// </summary>
        /// <param name="element">step element</param>
        /// <param name="name">attribute name</param>
        /// <param name="defaultValue">default value (double) if value field is empty</param>
        /// <returns></returns>
        private double XElementAttributeValue(XElement element, string name, double defaultValue = 0)
        {
            string s = XElementAttributeValue(element, name, defaultValue.ToString());
            double d = defaultValue;
            CultureInfo provider = CultureInfo.InvariantCulture;
            double.TryParse(s, NumberStyles.Number, provider, out d);
            return d;
        }

        /// <summary>
        /// Help-method to extract Attribute-value from a Xelement
        /// </summary>
        /// <param name="element"></param>
        /// <param name="name">attribute name</param>
        /// <param name="defaultValue">default value (string) if value field is empty</param>
        /// <returns></returns>
        private string XElementAttributeValue(XElement element, string name, string defaultValue = "")
        {
            if (element.HasAttributes && element.Attribute(name) != null)
                return element.Attribute(name).Value;
            else
                return defaultValue;
        }

        /// <summary>
        ///  Help-method for parsing Enums
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="strType"></param>
        /// <param name="result"></param>
        /// <returns></returns>
    }
}