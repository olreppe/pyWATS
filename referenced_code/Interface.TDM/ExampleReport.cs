using System;
using System.IO;
using System.Linq;
using System.Text;
using System.Xml.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Used to generates advanced example UUR and UUT objects.
    /// </summary>
    public class ExampleReport
    {
        /// <summary>
        /// Generates an advanced UUT report.
        /// </summary>
        /// <returns></returns>
        public UUTReport GenerateExampleUUT(TDM api)
        {
            UUTReport report = CreateFATUUT(api);
            return report;
        }

        /// <summary>
        /// Generates an advanced UUR report.
        /// *NOT YET IMPLEMENTED*
        /// </summary>
        /// <returns></returns>
        public UURReport GenerateExampleUUR()
        {
            throw new NotImplementedException();
        }

        private UUTReport CreateFATUUT(TDM api)
        {
            UUTReport uut = api.CreateUUTReport("FATOperator", "FATPartNo", "Rev1", String.Format("FATTest-{0}", new Random().Next(1000)), "10", "Seq1", "1.0.0");
            uut.AddMiscUUTInfo("MiscInfoNumeric", 100);
            uut.AddMiscUUTInfo("MiscInfoString", "Hello");
            uut.AddMiscUUTInfo("InvalidXML", "This is a test with < and >");
            uut.AddUUTPartInfo("PCBA", "SubPartNo1", "SubPartSN1", "Rev2");
            uut.AddUUTPartInfo("MODULE", "SubPartNo2", "SubPartSN2", "Rev3");
            uut.BatchSerialNumber = "BatchSN";
            uut.BatchFailCount = 10;
            uut.Comment = "FAT Comment - can be 500 long";
            uut.ErrorCode = 999;
            uut.ErrorMessage = "Error code 999";
            uut.ExecutionTime = 123.67;
            uut.FixtureId = "FAT FixtureId";
            uut.TestSocketIndex = 999;
            uut.StartDateTime = DateTime.Now;
            uut.StartDateTimeUTC = uut.StartDateTime.ToUniversalTime();
            SequenceCall numericTests = uut.GetRootSequenceCall().AddSequenceCall("Numeric tests");
            AddNumericTests(numericTests);
            SequenceCall passFailTests = uut.GetRootSequenceCall().AddSequenceCall("Pass/Fail tests");
            AddPassFailTests(passFailTests);
            SequenceCall stringValueTests = uut.GetRootSequenceCall().AddSequenceCall("StringValue tests");
            AddStringValueTests(stringValueTests);
            StringValueStep stringValueStep = uut.GetRootSequenceCall().AddStringValueStep("Step with ReportText/ErrorText");
            stringValueStep.AddTest("StringValueStep should have a ReportText and an Error Text");
            string s = "The quick brown fox jumps over the lazy dog\r\n";
            stringValueStep.ReportText = new StringBuilder(s.Length * 100).Insert(0, s, 100).ToString(); //45*100 = 4500 chars
            stringValueStep.StepErrorMessage = "Step error message (max 200 long)";
            stringValueStep.StepErrorCode = 9999;
            SequenceCall graphTest = uut.GetRootSequenceCall().AddSequenceCall("Graphs");
            AddGraph(graphTest);
            SequenceCall loopTest = uut.GetRootSequenceCall().AddSequenceCall("Loops");
            AddLoopTest(loopTest);
            SequenceCall miscFeatures = uut.GetRootSequenceCall().AddSequenceCall("Misc Features");
            //TODO: Make this work on Window 7
            //SequenceCall attachments = miscFeatures.AddSequenceCall("Attachments");
            //AddAttachments(attachments);
            SequenceCall genericSteps = miscFeatures.AddSequenceCall("Generic Steps");
            AddGenericSteps(genericSteps);
            SequenceCall misc = miscFeatures.AddSequenceCall("Misc");
            AddMessagePopup(misc);
            AddCallExe(misc);
            //AddAdditionalResults(misc); //Not supported (In WRML?)
            //TODO: Maintain and update if new types are added.
            return uut;
        }

        private UURReport CreateFATUUR(TDM tdm)
        {
            throw new NotImplementedException();
        }

        #region UUTHelpers

        private void AddNumericTests(SequenceCall numericTests)
        {
            numericTests.AddNumericLimitStep("SingleLog").AddTest(10, "A");
            //numericTests.AddNumericLimitStep("SingleLogDone").AddTest(15, "Log", StepStatusType.Done);
            numericTests.AddNumericLimitStep("SingleEQPass").AddTest(500, CompOperatorType.EQ, 500, "V");
            numericTests.AddNumericLimitStep("SingleEQFail").AddTest(500, CompOperatorType.EQ, 501, "V");
            numericTests.AddNumericLimitStep("SingleGEPass").AddTest(500, CompOperatorType.GE, 500, "V");
            numericTests.AddNumericLimitStep("SingleGEFail").AddTest(500, CompOperatorType.GE, 501, "V");
            numericTests.AddNumericLimitStep("SingleGELEPass").AddTest(500, CompOperatorType.GELE, 500, 500, "V");
            numericTests.AddNumericLimitStep("SingleGELEFail").AddTest(500, CompOperatorType.GELE, 501, 502, "V");
            numericTests.AddNumericLimitStep("SingleGELTPass").AddTest(500, CompOperatorType.GELT, 500, 501, "V");
            numericTests.AddNumericLimitStep("SingleGELTFail").AddTest(500, CompOperatorType.GELT, 499, 500, "V");
            numericTests.AddNumericLimitStep("SingleGTPass").AddTest(500, CompOperatorType.GT, 499, "V");
            numericTests.AddNumericLimitStep("SingleGTFail").AddTest(500, CompOperatorType.GT, 500, "V");
            numericTests.AddNumericLimitStep("SingleGTLEPass").AddTest(500, CompOperatorType.GTLE, 499, 500, "V");
            numericTests.AddNumericLimitStep("SingleGTLEFail").AddTest(500, CompOperatorType.GTLE, 500, 501, "V");
            numericTests.AddNumericLimitStep("SingleGTLTPass").AddTest(500, CompOperatorType.GTLT, 499, 501, "V");
            numericTests.AddNumericLimitStep("SingleGTLTFail").AddTest(500, CompOperatorType.GTLT, 499, 500, "V");
            numericTests.AddNumericLimitStep("SingleLEPass").AddTest(500, CompOperatorType.LE, 500, "V");
            numericTests.AddNumericLimitStep("SingleLEFail").AddTest(500, CompOperatorType.LE, 499, "V");
            numericTests.AddNumericLimitStep("SingleLEGEPass").AddTest(500, CompOperatorType.LEGE, 500, 500, "V");
            numericTests.AddNumericLimitStep("SingleLEGEFail").AddTest(500, CompOperatorType.LEGE, 499, 501, "V");
            numericTests.AddNumericLimitStep("SingleLEGTPass").AddTest(500, CompOperatorType.LEGT, 500, 500, "V");
            numericTests.AddNumericLimitStep("SingleLEGTFail").AddTest(500, CompOperatorType.LEGT, 499, 501, "V");
            numericTests.AddNumericLimitStep("SingleLTPass").AddTest(500, CompOperatorType.LT, 501, "V");
            numericTests.AddNumericLimitStep("SingleLTFail").AddTest(500, CompOperatorType.LT, 500, "V");
            numericTests.AddNumericLimitStep("SingleLTGEPass").AddTest(498, CompOperatorType.LTGE, 499, 501, "V");
            numericTests.AddNumericLimitStep("SingleLTGEFail").AddTest(500, CompOperatorType.LTGE, 500, 501, "V");
            numericTests.AddNumericLimitStep("SingleLTGTPass").AddTest(502, CompOperatorType.LTGT, 499, 501, "V");
            numericTests.AddNumericLimitStep("SingleLTGTFail").AddTest(500, CompOperatorType.LTGT, 500, 501, "V");
            numericTests.AddNumericLimitStep("SingleNEPass").AddTest(500, CompOperatorType.NE, 499, "V");
            numericTests.AddNumericLimitStep("SingleNEFail").AddTest(500, CompOperatorType.NE, 500, "V");

            NumericLimitStep ns = numericTests.AddNumericLimitStep("Multiple Numeric Step");
            ns.AddMultipleTest(10, "A", "MultiLog");
            ns.AddMultipleTest(500, CompOperatorType.EQ, 500, "V", "MultiEQPass");
            ns.AddMultipleTest(500, CompOperatorType.EQ, 501, "V", "MultiEQFail");
            ns.AddMultipleTest(500, CompOperatorType.GE, 500, "V", "MultiGEPass");
            ns.AddMultipleTest(500, CompOperatorType.GE, 501, "V", "MultiGEFail");
            ns.AddMultipleTest(500, CompOperatorType.GELE, 500, 500, "V", "MultiGELEPass");
            ns.AddMultipleTest(500, CompOperatorType.GELE, 501, 502, "V", "MultiGELEFail");
            ns.AddMultipleTest(500, CompOperatorType.GELT, 500, 501, "V", "MultiGELTPass");
            ns.AddMultipleTest(500, CompOperatorType.GELT, 499, 500, "V", "MultiGELTFail");
            ns.AddMultipleTest(500, CompOperatorType.GT, 499, "V", "MultiGTPass");
            ns.AddMultipleTest(500, CompOperatorType.GT, 500, "V", "MultiGTFail");
            ns.AddMultipleTest(500, CompOperatorType.GTLE, 499, 500, "V", "MultiGTLEPass");
            ns.AddMultipleTest(500, CompOperatorType.GTLE, 500, 501, "V", "MultiGTLEFail");
            ns.AddMultipleTest(500, CompOperatorType.GTLT, 499, 501, "V", "MultiGTLTPass");
            ns.AddMultipleTest(500, CompOperatorType.GTLT, 499, 500, "V", "MultiGTLTFail");
            ns.AddMultipleTest(500, CompOperatorType.LE, 500, "V", "MultiLEPass");
            ns.AddMultipleTest(500, CompOperatorType.LE, 499, "V", "MultiLEFail");
            ns.AddMultipleTest(500, CompOperatorType.LEGE, 500, 500, "V", "MultiLEGEPass");
            ns.AddMultipleTest(500, CompOperatorType.LEGE, 499, 501, "V", "MultiLEGEFail");
            ns.AddMultipleTest(500, CompOperatorType.LEGT, 500, 500, "V", "MultiLEGTPass");
            ns.AddMultipleTest(500, CompOperatorType.LEGT, 499, 501, "V", "MultiLEGTFail");
            ns.AddMultipleTest(500, CompOperatorType.LT, 501, "V", "MultiLTPass");
            ns.AddMultipleTest(500, CompOperatorType.LT, 500, "V", "MultiLTFail");
            ns.AddMultipleTest(498, CompOperatorType.LTGE, 499, 501, "V", "MultiLTGEPass");
            ns.AddMultipleTest(500, CompOperatorType.LTGE, 500, 501, "V", "MultiLTGEFail");
            ns.AddMultipleTest(502, CompOperatorType.LTGT, 499, 501, "V", "MultiLTGTPass");
            ns.AddMultipleTest(500, CompOperatorType.LTGT, 500, 501, "V", "MultiLTGTFail");
            ns.AddMultipleTest(500, CompOperatorType.NE, 499, "V", "MultiNEPass");
            ns.AddMultipleTest(500, CompOperatorType.NE, 500, "V", "MultiNEFail");
            ns.AddMultipleTest(500, "V", "MultiLOGPass");
        }

        private void AddStringValueTests(SequenceCall stringValueTests)
        {
            stringValueTests.AddStringValueStep("Single").AddTest("No compare");
            stringValueTests.AddStringValueStep("SingleCasePass").AddTest(CompOperatorType.CASESENSIT, "CaseSensitive", "CaseSensitive");
            stringValueTests.AddStringValueStep("SingleCaseFail").AddTest(CompOperatorType.CASESENSIT, "caseSensitive", "CaseSensitive");
            stringValueTests.AddStringValueStep("SingleInsiensPass").AddTest(CompOperatorType.IGNORECASE, "caseSensitive", "CaseSensitive");
            StringValueStep ns = stringValueTests.AddStringValueStep("Multiple tests");
            ns.AddMultipleTest("No compare", "Multi");
            ns.AddMultipleTest(CompOperatorType.CASESENSIT, "CaseSensitive", "CaseSensitive", "MultiCasePass");
            ns.AddMultipleTest(CompOperatorType.CASESENSIT, "caseSensitive", "CaseSensitive", "MultiCaseFail");
            ns.AddMultipleTest(CompOperatorType.IGNORECASE, "caseSensitive", "CaseSensitive", "MultiInsiensPass");
            ns.AddMultipleTest(CompOperatorType.IGNORECASE, "caseSensitive", "CaseSensitive2", "MultiInsiensFail");
        }

        private void AddPassFailTests(SequenceCall passFailTests)
        {
            passFailTests.AddPassFailStep("SinglePass").AddTest(true);
            passFailTests.AddPassFailStep("SingleFail").AddTest(false);
            passFailTests.AddPassFailStep("SinglePassDone").AddTest(true, StepStatusType.Done);
            PassFailStep ps = passFailTests.AddPassFailStep("Multiple tests");
            ps.AddMultipleTest(true, "Pass");
            ps.AddMultipleTest(false, "Fail");
            ps.AddMultipleTest(true, "PassSkipped", StepStatusType.Skipped);
        }

        private void AddLoopTest(SequenceCall seqCall)
        {
            //SequenceCall loop
            SequenceCall seqCallSequence = seqCall.AddSequenceCall("SequenceCallLoopSequence");
            SequenceCall sequenceCallSummary = seqCallSequence.StartLoop<SequenceCall>("SequenceCallLoop", 2, 1, 1, 2);
            sequenceCallSummary.AddNumericLimitStep("NumericStep1").AddTest(301, CompOperatorType.GE, 300, "");
            sequenceCallSummary.AddNumericLimitStep("NumericStep2").AddTest(301, CompOperatorType.LE, 300, "");
            sequenceCallSummary.AddNumericLimitStep("NumericStep3").AddTest(300, CompOperatorType.EQ, 300, "");
            sequenceCallSummary.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue", "testvalue", StepStatusType.Passed);
            sequenceCallSummary.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Passed);

            SequenceCall sequenceCallIteration1 = seqCallSequence.AddSequenceCall("SequenceCallLoop");
            sequenceCallIteration1.AddNumericLimitStep("NumericStep1").AddTest(301, CompOperatorType.GE, 300, "");
            sequenceCallIteration1.AddNumericLimitStep("NumericStep2").AddTest(301, CompOperatorType.LE, 300, "");
            sequenceCallIteration1.AddNumericLimitStep("NumericStep3").AddTest(300, CompOperatorType.EQ, 300, "");
            sequenceCallIteration1.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue", "testvalue", StepStatusType.Passed);
            sequenceCallIteration1.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Passed);

            SequenceCall sequenceCallIteration2 = seqCallSequence.AddSequenceCall("SequenceCallLoop");
            sequenceCallIteration2.AddNumericLimitStep("NumericStep1").AddTest(301, CompOperatorType.GE, 300, "");
            sequenceCallIteration2.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue", "testvalue", StepStatusType.Passed);
            sequenceCallIteration2.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Passed);

            SequenceCall sequenceCallIteration3 = seqCallSequence.AddSequenceCall("SequenceCallLoop");
            sequenceCallIteration3.AddNumericLimitStep("NumericStep2").AddTest(301, CompOperatorType.LE, 300, "");
            sequenceCallIteration3.AddNumericLimitStep("NumericStep3").AddTest(300, CompOperatorType.EQ, 300, "");
            sequenceCallIteration3.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue", "testvalue", StepStatusType.Passed);
            sequenceCallIteration3.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Passed);
            seqCallSequence.StopLoop();

            SequenceCall sequenceCall2Summary = seqCallSequence.StartLoop<SequenceCall>("SequenceCallLoop2", 2, 1, 1, 2);
            sequenceCall2Summary.AddNumericLimitStep("NumericStep1").AddTest(301, CompOperatorType.GE, 300, "");
            sequenceCall2Summary.AddNumericLimitStep("NumericStep2").AddTest(301, CompOperatorType.LE, 300, "");
            sequenceCall2Summary.AddNumericLimitStep("NumericStep3").AddTest(300, CompOperatorType.EQ, 300, "");
            sequenceCall2Summary.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue1", "testvalue1", StepStatusType.Passed);
            sequenceCall2Summary.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Passed);

            SequenceCall sequenceCall2Iteration1 = seqCallSequence.AddSequenceCall("SequenceCallLoop2");
            sequenceCall2Iteration1.AddNumericLimitStep("NumericStep1").AddTest(401, CompOperatorType.GE, 300, "");
            sequenceCall2Iteration1.AddNumericLimitStep("NumericStep2").AddTest(401, CompOperatorType.LE, 300, "");
            sequenceCall2Iteration1.AddNumericLimitStep("NumericStep3").AddTest(400, CompOperatorType.EQ, 300, "");
            sequenceCall2Iteration1.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue2", "testvalue2", StepStatusType.Passed);
            sequenceCall2Iteration1.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Passed);

            SequenceCall sequenceCall2Iteration2 = seqCallSequence.AddSequenceCall("SequenceCallLoop2");
            sequenceCall2Iteration2.AddNumericLimitStep("NumericStep1").AddTest(501, CompOperatorType.GE, 300, "");
            sequenceCall2Iteration2.AddNumericLimitStep("NumericStep2").AddTest(501, CompOperatorType.LE, 300, "");
            sequenceCall2Iteration2.AddNumericLimitStep("NumericStep3").AddTest(500, CompOperatorType.EQ, 300, "");
            sequenceCall2Iteration2.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue3", "testvalue3", StepStatusType.Passed);
            sequenceCall2Iteration2.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Failed);

            SequenceCall sequenceCall2Iteration3 = seqCallSequence.AddSequenceCall("SequenceCallLoop2");
            sequenceCall2Iteration3.AddNumericLimitStep("NumericStep1").AddTest(601, CompOperatorType.GE, 300, "");
            sequenceCall2Iteration3.AddNumericLimitStep("NumericStep2").AddTest(601, CompOperatorType.LE, 300, "");
            sequenceCall2Iteration3.AddNumericLimitStep("NumericStep3").AddTest(600, CompOperatorType.EQ, 300, "");
            sequenceCall2Iteration3.AddStringValueStep("StringStep").AddTest(CompOperatorType.IGNORECASE, "TestValue4", "testvalue4", StepStatusType.Passed);
            sequenceCall2Iteration3.AddPassFailStep("PassFailStep").AddTest(true, StepStatusType.Passed);
            seqCallSequence.StopLoop();

            //NumericLimit
            SequenceCall seqCallNumericLimit = seqCall.AddSequenceCall("NumericLimitLoopSequence");
            seqCallNumericLimit.StartLoop<NumericLimitStep>("NumericLimitStepLoop").AddTest(301, CompOperatorType.LE, 300, "");
            seqCallNumericLimit.AddNumericLimitStep("NumericLimitStepLoop").AddTest(298, CompOperatorType.LE, 300, "");
            seqCallNumericLimit.AddNumericLimitStep("NumericLimitStepLoop").AddTest(301, CompOperatorType.LE, 300, "");
            seqCallNumericLimit.StopLoop();

            //NumericLimit Multiple
            SequenceCall seqCallMulitNumericLimit = seqCall.AddSequenceCall("MultiNumericLimitLoopSequence");
            NumericLimitStep multiNumericLimitStepSummary = seqCallMulitNumericLimit.StartLoop<NumericLimitStep>("NumericLimitMultiStepLoop");
            multiNumericLimitStepSummary.AddMultipleTest(301, CompOperatorType.LE, 300, "", "NumTest1");
            multiNumericLimitStepSummary.AddMultipleTest(298, CompOperatorType.LE, 300, "", "NumTest2");

            NumericLimitStep multiNumericLimitStepIteration1 = seqCallMulitNumericLimit.AddNumericLimitStep("NumericLimitMultiStepLoop");
            multiNumericLimitStepIteration1.AddMultipleTest(301, CompOperatorType.LE, 300, "", "NumTest1");
            multiNumericLimitStepIteration1.AddMultipleTest(298, CompOperatorType.LE, 300, "", "NumTest2");

            NumericLimitStep multiNumericLimitStepIteration2 = seqCallMulitNumericLimit.AddNumericLimitStep("NumericLimitMultiStepLoop");
            multiNumericLimitStepIteration2.AddMultipleTest(302, CompOperatorType.LE, 300, "", "NumTest1");
            multiNumericLimitStepIteration2.AddMultipleTest(297, CompOperatorType.LE, 300, "", "NumTest2");
            seqCallMulitNumericLimit.StopLoop();

            //NumericLimit Mixed Single & Multiple
            SequenceCall seqCallMultiAndSingleNumericLimit = seqCall.AddSequenceCall("MultiAndSingleNumericLimitLoopSequence");
            NumericLimitStep numericLimit1 = seqCallMultiAndSingleNumericLimit.StartLoop<NumericLimitStep>("NumericLimitMultiAndSingleStepLoop1");
            seqCallMultiAndSingleNumericLimit.AddNumericLimitStep("NumericLimitMultiAndSingleStepLoop1").AddTest(302, CompOperatorType.LE, 300, "");
            NumericLimitStep numericStep1 = seqCallMultiAndSingleNumericLimit.AddNumericLimitStep("NumericLimitMultiAndSingleStepLoop1");
            numericStep1.AddMultipleTest(301, CompOperatorType.LE, 300, "", "NumTest");
            numericStep1.AddMultipleTest(298, CompOperatorType.LE, 300, "", "NumTest1");
            seqCallMultiAndSingleNumericLimit.AddNumericLimitStep("NumericLimitMultiAndSingleStepLoop1").AddTest(299, CompOperatorType.LE, 300, "");
            seqCallMultiAndSingleNumericLimit.StopLoop();

            NumericLimitStep numericLimit2 = seqCallMultiAndSingleNumericLimit.StartLoop<NumericLimitStep>("NumericLimitMultiAndSingleStepLoop2");
            NumericLimitStep numericStep2 = seqCallMultiAndSingleNumericLimit.AddNumericLimitStep("NumericLimitMultiAndSingleStepLoop2");
            numericStep2.AddMultipleTest(301, CompOperatorType.LE, 300, "", "NumTest");
            numericStep2.AddMultipleTest(298, CompOperatorType.LE, 300, "", "NumTest1");
            seqCallMultiAndSingleNumericLimit.AddNumericLimitStep("NumericLimitMultiAndSingleStepLoop2").AddTest(302, CompOperatorType.LE, 300, "");
            NumericLimitStep numericStep3 = seqCallMultiAndSingleNumericLimit.AddNumericLimitStep("NumericLimitMultiAndSingleStepLoop2");
            numericStep3.AddMultipleTest(303, CompOperatorType.LE, 300, "", "NumTest");
            numericStep3.AddMultipleTest(297, CompOperatorType.LE, 300, "", "NumTest1");
            seqCallMultiAndSingleNumericLimit.StopLoop();

            //StringValue
            SequenceCall seqCallStringValue = seqCall.AddSequenceCall("StringValueStepLoopSequence");
            seqCallStringValue.StartLoop<StringValueStep>("StringValueStepLoop").AddTest(CompOperatorType.IGNORECASE, "TestValue1", "testvalue1", StepStatusType.Passed);
            seqCallStringValue.AddStringValueStep("StringValueStepLoop").AddTest(CompOperatorType.IGNORECASE, "TestValue2", "testvalue2", StepStatusType.Passed);
            seqCallStringValue.AddStringValueStep("StringValueStepLoop").AddTest(CompOperatorType.CASESENSIT, "TestValue3", "testvalue3", StepStatusType.Failed);
            seqCallStringValue.StopLoop();

            //PassFail
            SequenceCall seqCallPassFail = seqCall.AddSequenceCall("PassFailStepLoopSequence");
            seqCallPassFail.StartLoop<PassFailStep>("PassFailLoop").AddTest(false, StepStatusType.Failed);
            seqCallPassFail.AddPassFailStep("PassFailLoop").AddTest(true, StepStatusType.Passed);
            seqCallPassFail.AddPassFailStep("PassFailLoop").AddTest(false, StepStatusType.Failed);
            seqCallPassFail.StopLoop();

            //Generic
            SequenceCall seqCallGeneric = seqCall.AddSequenceCall("GenericStepLoopSequence");
            seqCallGeneric.StartLoop<GenericStep>("GenericStepLoop").StepType = GenericStepTypes.DoWhile.ToString();
            seqCallGeneric.AddGenericStep(GenericStepTypes.Goto, "GenericStepLoop");
            seqCallGeneric.AddGenericStep(GenericStepTypes.IVIScope, "GenericStepLoop");
            seqCallGeneric.StopLoop();

            seqCallGeneric.StartLoop<GenericStep>("GenericStepLoop2").StepType = GenericStepTypes.Action.ToString();
            seqCallGeneric.AddGenericStep(GenericStepTypes.Action, "GenericStepLoop2").StepTime = 1;
            seqCallGeneric.AddGenericStep(GenericStepTypes.Action, "GenericStepLoop2").StepTime = 2;
            seqCallGeneric.StopLoop();

            //MessagePopup
            SequenceCall seqCallMessagePopup = seqCall.AddSequenceCall("MessagePopupStepLoopSequence");
            seqCallMessagePopup.StartLoop<MessagePopupStep>("MessagePopupStepLoop");
            seqCallMessagePopup.AddMessagePopupStep("MessagePopupStepLoop", 0, "Wrong Button :(");
            seqCallMessagePopup.AddMessagePopupStep("MessagePopupStepLoop", 1, "Good Job! ;)");
            seqCallMessagePopup.StopLoop();

            //CallExeStep
            SequenceCall seqCallCallExe = seqCall.AddSequenceCall("CallExeStepLoopSequence");
            seqCallCallExe.StartLoop<CallExeStep>("CallExeStepLoop");
            seqCallCallExe.AddCallExeStep("CallExeStepLoop", 1);
            seqCallCallExe.AddCallExeStep("CallExeStepLoop", 2);
            seqCallCallExe.StopLoop();

            //SequenceCallWithMultipleNumericLoops
            SequenceCall seqCallNumericLimitMultipleLoops = seqCall.AddSequenceCall("NumericLimitMultipleLoopsSequence");
            seqCallNumericLimitMultipleLoops.StartLoop<NumericLimitStep>("NumericLimitMultipleLoops1").AddTest(302, CompOperatorType.LE, 300, "");
            seqCallNumericLimitMultipleLoops.AddNumericLimitStep("NumericLimitMultipleLoops1").AddTest(301, CompOperatorType.LE, 300, "");
            seqCallNumericLimitMultipleLoops.AddNumericLimitStep("NumericLimitMultipleLoops1").AddTest(302, CompOperatorType.LE, 300, "");
            seqCallNumericLimitMultipleLoops.StopLoop();

            seqCallNumericLimitMultipleLoops.StartLoop<NumericLimitStep>("NumericLimitMultipleLoops2").AddTest(299, CompOperatorType.LE, 300, "");
            seqCallNumericLimitMultipleLoops.AddNumericLimitStep("NumericLimitMultipleLoops2").AddTest(298, CompOperatorType.LE, 300, "");
            seqCallNumericLimitMultipleLoops.AddNumericLimitStep("NumericLimitMultipleLoops2").AddTest(299, CompOperatorType.LE, 300, "");
            seqCallNumericLimitMultipleLoops.StopLoop();
        }

        private void AddGraph(SequenceCall sequence)
        {
            //Example 1: Fibonacci numbers with mean value
            //This will go into a graph series where x=0,1,2,3,4... and y is fibionacci(x)
            double[] yValuesFibonacci = new double[] { 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 };
            NumericLimitStep fibonacciStep = sequence.AddNumericLimitStep("Fibionacci");
            double meanFib = yValuesFibonacci.ToList().Average(); //Take the mean value
            fibonacciStep.AddTest(meanFib, "Number"); //Add a test with no limits on the mean value
            Chart fibChart = fibonacciStep.AddChart(ChartType.Line, "Fibonacci numbers", "X", "", "Y", "");
            fibChart.AddSeries("Fibionacci", yValuesFibonacci); //1 series
            fibChart.AddSeries("Mean", new double[,] { { 0, yValuesFibonacci.Length - 1 }, { meanFib, meanFib } }); //Also plot the mean value

            //Example 2: Some measured current values over time using a multiple numberic step
            //This will go into a graph series where x=Minutes from start and y=Current measured
            double[] xValuesCurrent = new double[] { 0, 17, 47, 76 }; //Minutes from start
            double[] yValuesCurrent = new double[] { 60.72, 61.886, 62.6, 0 }; //Ampere measured
            NumericLimitStep currentStep = sequence.AddNumericLimitStep("Current from burn-in test");
            currentStep.AddMultipleTest(yValuesCurrent.ToList().Min(), CompOperatorType.GE, 52, "A", "MinValue"); //The minimum should not be under 52 Amps
            currentStep.AddMultipleTest(yValuesCurrent.ToList().Max(), CompOperatorType.LE, 72, "A", "MaxValue"); //The minimum should not be over 72 Amps
            currentStep.AddMultipleTest(yValuesCurrent.ToList().Average(), "A", "Mean");
            Chart currentChart = currentStep.AddChart(ChartType.Line, "Current", "Minutes", "min", "Current", "A");
            currentChart.AddSeries("Current", yValuesCurrent);
            currentChart.AddSeries("Mean", new double[,] { { 0, yValuesCurrent.Length - 1 }, { yValuesCurrent.ToList().Average(), yValuesCurrent.ToList().Average() } });
            currentChart.AddSeries("LowLimit", new double[,] { { 0, yValuesCurrent.Length - 1 }, { 52, 52 } });
            currentChart.AddSeries("HighLimit", new double[,] { { 0, yValuesCurrent.Length - 1 }, { 72, 72 } });

            //Further notes:
            //ChartType also be logaritmic, use LineLogXY, LineLogX, LineLogY
            //A chart can be attached to any type of Step
            //If you have many values (lets say more 1000 in a series), please extract samples (e.g. use mean over time)
            //to reduce amount of data as this will degrade performance and consume space in the database.
        }

        private void AddAttachments(SequenceCall attachments)
        {
            GenericStep attachFile = attachments.AddGenericStep(GenericStepTypes.Action, "Attach file");
            Attachment attFile = attachFile.AttachFile(@"C:\Windows\winhlp32.exe", false); //false means do not delete it
            GenericStep attachByteArray = attachments.AddGenericStep(GenericStepTypes.Action, "Attach Byte array");
            FileStream f = new FileStream(@"c:\Windows\System32\SecurityAndMaintenance_Alert.png", FileMode.Open, FileAccess.Read);
            byte[] content = new byte[f.Length];
            f.Read(content, 0, (int)f.Length);
            attachByteArray.AttachByteArray("WiFiNotification", content, "image/png");
        }

        private void AddGenericSteps(SequenceCall genericSteps)
        {
            foreach (string stepType in Enum.GetNames(typeof(GenericStepTypes)))
            {
                genericSteps.AddGenericStep((GenericStepTypes)Enum.Parse(typeof(GenericStepTypes), stepType), $"{stepType} Step");
            }
        }

        private void AddCallExe(SequenceCall misc)
        {
            CallExeStep cStep = misc.AddCallExeStep("CallExe", 17232);
        }

        private void AddMessagePopup(SequenceCall misc)
        {
            misc.AddMessagePopupStep("MessagePopup", 1, "Response Message");
        }

        private void AddAdditionalResults(SequenceCall misc)
        {
            GenericStep additionalResult1 = misc.AddGenericStep(GenericStepTypes.Action, "AdditionalResults Example 1");
            XElement content =
                new XElement("Features",
                    new XElement("Feature", new XAttribute("Name", "Waterproof"), "No"),
                    new XElement("Feature", new XAttribute("Name", "Screws"), "16"));
            additionalResult1.AddAdditionalResult("Features", content);

            GenericStep additionalResult2 = misc.AddGenericStep(GenericStepTypes.Action, "AdditionalResults Example 2");
            content =
                new XElement("Team",
                    new XElement("Member", new XAttribute("Department", "Engineering"), new XAttribute("Role", "Head Engineer"), new XAttribute("Name", "Alex Smith")),
                    new XElement("Member", new XAttribute("Department", "Engineering"), new XAttribute("Role", "Torso Engineer"), new XAttribute("Name", "Felicia Jefferson")),
                    new XElement("Member", new XAttribute("Department", "Engineering"), new XAttribute("Role", "Left Arm Engineer"), new XAttribute("Name", "Jonah Tucker")),
                    new XElement("Member", new XAttribute("Department", "Administration"), new XAttribute("Role", "Project Manager"), new XAttribute("Name", "Paul Fisher")));
            additionalResult2.AddAdditionalResult("Teammembers", content);
        }

        #endregion UUTHelpers

        private void SendUUR_FAT()
        {
            TDM api = new TDM();       //Create api
            api.InitializeAPI(true);   //Initialize it
            UUTReport uut = CreateFATUUT(api);
            api.Submit(uut);
            RepairType repType = api.GetRepairTypes().Where(r => r.Code == 500).FirstOrDefault();
            UURReport uur = api.CreateUURReport("FAToper", repType, uut);
            uur.AddUURPartInfo(uut.PartInfo[0].PartNumber, uut.PartInfo[0].SerialNumber, uut.PartInfo[0].PartRevisionNumber);
            uur.AddUURPartInfo(uut.PartInfo[1].PartNumber, uut.PartInfo[1].SerialNumber, uut.PartInfo[1].PartRevisionNumber);
            uur.Comment = "FAT UUR Comment";
            FailCode[] fc = api.GetRootFailCodes(repType);
            FailCode cat = fc.Where(f => f.Description == "Assembly Process").FirstOrDefault();
            FailCode fail = api.GetChildFailCodes(cat).Where(f => f.Description == "Missing component").FirstOrDefault();
            uur.PartInfo[1].AddFailure(fail, "U16", "Failure on subunit", uut.GetFailedStepOrderNumbers()[0]);
            cat = fc.Where(f => f.Description == "Solder Process").FirstOrDefault();
            fail = api.GetChildFailCodes(cat).Where(f => f.Description == "Appearance").FirstOrDefault();
            uur.AddFailure(fail, "R55", "Failure on main unit", uut.GetFailedStepOrderNumbers()[1]);
            api.Submit(SubmitMethod.Automatic, uur);
        }
    }
}