using System;
using System.Collections.Generic;
using Virinco.WATS.Interface;
using System.Linq;
using System.Text;
using System.Globalization;

namespace Virinco.WATS.Integration.TextConverter
{

    public class WATSStandardTextFormat : TextConverterBase
    {
        //Global chart values
        private Chart currentChart;
        private int currentChartSeriesCount;
        private bool stepHasMoreThanOneChart;

        protected override bool ProcessNonMatchLine(string line, ref TextConverterBase.ReportReadState readState)
        {
            try
            {
                if (readState == ReportReadState.InHeader) //Treat this as misc info
                {
                    //TODO: More strict parsing?
                    string[] keyValue = line.Split(new char[] { '\t' });
                    if (keyValue.Length >= 2)
                        currentUUT.AddMiscUUTInfo(keyValue[0], keyValue[1]);
                }
                else if (readState == ReportReadState.InTest)
                {
                    string firstElement = line.Split(new char[] { '\t' }).FirstOrDefault();
                    if (!(firstElement == "StepType") && !(firstElement == "--Step-Data-End--")) //special definition cases //StepDataEnd should be added to a different ReportReadState?
                        throw new TextFormatException("First element in line is not recognized as a valid type."); //catch step/lines with wrong/non-existent types
                }
            }
            catch (TextFormatException ex)
            {
                ParseError(ex.Message, line);
            }
            return true;
        }


        /// <summary>
        /// Two modes: Import vs Active. Header-keyword: ConverterMode can be set to either of these. If not set in txt-file, Active is default. 
        /// NB! Import is not implemented for more than NumericLimitTest (not PassFailTest or StringValueTest). 
        /// Suggest to look into seperate this method into several parts, due to its length. 
        /// </summary>
        /// <param name="match"></param>
        /// <param name="readState"></param>
        /// <returns></returns>
        protected override bool ProcessMatchedLine(TextConverterBase.SearchFields.SearchMatch match, ref TextConverterBase.ReportReadState readState)
        {
            try
            {
                if (match == null) //End of file
                {
                    if (currentUUT != null)
                    {
                        SubmitUUT(); //If EndTest was missing, send report anyway, but throw exception
                        throw new TextFormatException("Did not find at end of test '--UUT-End--', report submitted anyway");
                    }
                    return true;
                }

                if (currentUUT == null && match.matchField.fieldName != "StartTest")
                    throw new ApplicationException("Missing --Header-Start--");

                string stepName = "";
                string measureName = "";
                if (readState == ReportReadState.InTest && match.ExistSubField("StepName"))
                {
                    stepName = (string)match.GetSubField("StepName");
                    measureName = (string)match.GetSubField("MeasureName");
                }

                switch (match.matchField.fieldName)
                {
                    case "StartTest":
                        if (currentUUT == null) CreateDefaultUUT();
                        break;
                    case "EndTest":
                        SubmitUUT();
                        currentUUT = null;
                        break;
                    case "SequenceCall":
                        currentSequence = currentSequence.AddSequenceCall(stepName);
                        currentStep = currentSequence;

                        if (match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //apiRef.TestMode == TestModeType.Import &&  //removed this due to status working for active too
                        {
                            currentSequence.Status = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);
                        }
                        AddGeneralStepInformation(currentSequence, match);
                        break;
                    case "EndSequenceCall":
                        if (stepName == "" || currentSequence.Name == stepName) //endsequencecall for current sequence call//override , StepTime, StepReportText, StepErrorCode and StepErrorMessage 
                        {
                            if (match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //apiRef.TestMode == TestModeType.Import &&  //removed this due to status working for active too
                            {
                                currentSequence.Status = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);
                            }
                            AddGeneralStepInformation(currentSequence, match);
                            currentSequence = currentSequence.Parent; //set the current sequence call to level above
                            currentStep = currentSequence;
                        }
                        else
                        {
                            throw new TextFormatException("EndSequenceCall with name that does not correspond to the current sequence call: " + stepName);
                        }

                        break;
                    case "NumericLimitTest":
                        if (!(currentStep is NumericLimitStep) || (!String.IsNullOrEmpty(stepName) && currentStep != null && stepName != currentStep.Name))
                        {
                            currentStep = currentSequence.AddNumericLimitStep(stepName);
                            if (apiRef.TestMode == TestModeType.Active && match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //set startup status for simple syntax multiple step //only for Active
                            {
                                currentStep.Status = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);
                            }
                        }

                        double measure = (double)match.GetSubField("Value");
                        double lowlim = (double)match.GetSubField("LowLimit");
                        double highlim = (double)match.GetSubField("HighLimit");
                        CompOperatorType compOp = (CompOperatorType)match.GetSubField("CompOperator");
                        string unit = (string)match.GetSubField("Unit");

                        if (apiRef.TestMode == TestModeType.Active) //Active mode => validation and ripple effect (current status quo)
                        {
                            if (match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //if status & active mode
                            {
                                StepStatusType currentStatus = StepStatusType.Passed; //default value
                                currentStatus = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);

                                if (String.IsNullOrEmpty(measureName)) //single step //with status                                
                                    AddNumericLimitTest((NumericLimitStep)currentStep, measure, compOp, lowlim, highlim, unit, currentStatus);
                                else
                                    AddNumericLimitMultipleTest((NumericLimitStep)currentStep, measure, compOp, lowlim, highlim, unit, measureName, currentStatus);
                            }
                            else //no status in active mode => PURE active mode
                            {
                                if (String.IsNullOrEmpty(measureName)) //single step //with status                                
                                    AddNumericLimitTest((NumericLimitStep)currentStep, measure, compOp, lowlim, highlim, unit);
                                else
                                    AddNumericLimitMultipleTest((NumericLimitStep)currentStep, measure, compOp, lowlim, highlim, unit, measureName);
                            }
                        }
                        else if (apiRef.TestMode == TestModeType.Import) //Import mode => Status needs to be present everywhere!
                        {
                            StepStatusType currentStatus = StepStatusType.Passed; //default value
                            if (match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //status present -> no validation                            
                                currentStatus = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);

                            if (String.IsNullOrEmpty(measureName)) //single step //with status                                
                                AddNumericLimitTest((NumericLimitStep)currentStep, measure, compOp, lowlim, highlim, unit, currentStatus);
                            else
                                AddNumericLimitMultipleTest((NumericLimitStep)currentStep, measure, compOp, lowlim, highlim, unit, measureName, currentStatus);
                        }
                        AddGeneralStepInformation(currentStep, match);
                        break;
                    case "PassFailTest":
                        if (!(currentStep is PassFailStep) || (!String.IsNullOrEmpty(stepName) && currentStep != null && stepName != currentStep.Name))
                        {
                            currentStep = currentSequence.AddPassFailStep(stepName);
                            if (apiRef.TestMode == TestModeType.Active && match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //set startup status for simple syntax multiple step //only for Active
                            {
                                currentStep.Status = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);
                            }
                        }
                        bool boolMeasure = (bool)match.GetSubField("Value");

                        if (apiRef.TestMode == TestModeType.Active) //Active mode => validation and ripple effect (current status quo)
                        {
                            if (match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //status present -> no validation
                            {
                                var status = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);
                                if (status == StepStatusType.Failed && boolMeasure == true)
                                    boolMeasure = false;

                                if (String.IsNullOrEmpty(measureName))                                
                                    ((PassFailStep)currentStep).AddTest(boolMeasure, status);                                
                                else                                
                                    ((PassFailStep)currentStep).AddMultipleTest(boolMeasure, measureName, status);                                
                            }
                            else //status not present -> with validation
                            {
                                if (String.IsNullOrEmpty(measureName))                                
                                    ((PassFailStep)currentStep).AddTest(boolMeasure);                                
                                else                                
                                    ((PassFailStep)currentStep).AddMultipleTest(boolMeasure, measureName);                                
                            }
                        }
                        // NB! Needs to implement Import-mode too. 
                        //else if (apiRef.TestMode == TestModeType.Import) //Import mode => Status needs to be present everywhere!
                        AddGeneralStepInformation(currentStep, match);
                        break;

                    case "StringValueTest":
                        if (!(currentStep is StringValueStep) || (!String.IsNullOrEmpty(stepName) && currentStep != null && stepName != currentStep.Name))
                        {
                            currentStep = currentSequence.AddStringValueStep(stepName);
                            if (apiRef.TestMode == TestModeType.Active && match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //set startup status for simple syntax multiple step //only for Active
                            {
                                currentStep.Status = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);
                            }
                        }

                        string stringMeasure = (string)match.GetSubField("Value");
                        string stringLimit = (string)match.GetSubField("StringLimit");
                        compOp = (CompOperatorType)match.GetSubField("CompOperator");

                        if (apiRef.TestMode == TestModeType.Active) //Active mode => validation and ripple effect (current status quo)
                        {
                            if (match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "") //status present -> no validation
                            {
                                if (String.IsNullOrEmpty(measureName))
                                    ((StringValueStep)currentStep).AddTest(compOp, stringMeasure, stringLimit, (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null));
                                else                                
                                    ((StringValueStep)currentStep).AddMultipleTest(compOp, stringMeasure, stringLimit, measureName, (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null));
                            }
                            else //status not present -> with validation
                            {
                                if (String.IsNullOrEmpty(measureName))
                                    ((StringValueStep)currentStep).AddTest(compOp, stringMeasure, stringLimit);
                                else
                                    ((StringValueStep)currentStep).AddMultipleTest(compOp, stringMeasure, stringLimit, measureName);
                            }
                        }
                        //NB! needs to implement import mode too
                        //else if (apiRef.TestMode == TestModeType.Import) //Import mode => Status needs to be present everywhere!
                        AddGeneralStepInformation(currentStep, match);
                        break;
                    case "ActionStep":
                        currentStep = currentSequence.AddGenericStep(GenericStepTypes.Action, stepName);
                        //Status (only for the steps that does not do it in the API code)
                        if (match.ExistSubField("Status") && ((string)match.GetSubField("Status")) != "")
                            currentStep.Status = (StepStatusType)ConvertStringToAny((string)match.GetSubField("Status"), typeof(StepStatusType), null, null);
                        AddGeneralStepInformation(currentStep, match);
                        break;
                    case "Subunit":
                        currentUUT.AddUUTPartInfo(
                            (string)match.GetSubField("Description"),
                            (string)match.GetSubField("PartNumber"),
                            (string)match.GetSubField("SerialNumber"),  //NB: Error in documentation
                            (string)match.GetSubField("Revision"));
                        break;
                    case "Chart":
                        CheckCurrentChart();
                        ChartType chartType = ChartType.Line;
                        if (!EnumTryParse<ChartType>(stepName, out chartType))
                        {
                            //ParseError("The chart type is not recognized. \"Line\" should be used as default.", match.completeLine);
                            throw new Exception("The chart type is not recognized. \"Line\" should be used as default.");
                        }
                        string stringLabel = measureName;
                        string stringChartxLabel = (string)match.GetSubField("XLabel");
                        string stringChartxUnit = (string)match.GetSubField("XUnit");
                        string stringChartyLabel = (string)match.GetSubField("YLabel");
                        string stringChartyUnit = (string)match.GetSubField("YUnit");

                        currentChart = currentStep.AddChart(
                           chartType, stringLabel, stringChartxLabel, stringChartxUnit, stringChartyLabel, stringChartyUnit);

                        break;
                    case "Series":
                        if (currentChart == null)
                        {
                            throw new TextFormatException("No current chart. Check text-file.");
                        }
                        if (stepHasMoreThanOneChart)
                        {
                            throw new TextFormatException("The chart has more than one Chart for one Step.");
                        }
                        if (currentChartSeriesCount > 10)
                        {
                            throw new TextFormatException("The chart already has the maximum number of 10 series.");
                        }

                        string stringPlotname = stepName;

                        //Check if data is filled in DataType, YData and XData
                        string stringDataType;
                        string stringYData;
                        string stringXData;

                        stringDataType = CheckAndGetField(match, "MeasureName", true);

                        if (stringDataType == "XYG") //Need to check this (even though it is not currently any other options)
                        {
                            stringYData = CheckAndGetField(match, "YData", true);
                            stringXData = CheckAndGetField(match, "XData", false);

                            double[] yData = SplitAndParseSeriesData(stringYData);
                            double[] xData = null;

                            if (!string.IsNullOrEmpty(stringXData))
                            {
                                xData = SplitAndParseSeriesData(stringXData);
                            }

                            if (!string.IsNullOrEmpty(stringXData) && (yData.Count() != xData.Count())) //Only check if count is the same after cutoff at max
                            {
                                throw new TextFormatException("The two plotdimensions have different lengths.");
                            }

                            if (!string.IsNullOrEmpty(stringXData))
                            {
                                currentChart.AddSeries(stringPlotname, xData, yData);
                            }
                            else
                            {
                                currentChart.AddSeries(stringPlotname, yData);
                            }
                            currentChartSeriesCount++;
                        }
                        else //Unknown type
                        {
                            throw new TextFormatException("Series DataType not recognized: " + stringDataType);
                        }
                        break;
                    default:
                        break;
                }
            }
            catch (TextFormatException ex)
            {
                throw new Exception(ex.Message);
            }

            return true;
        }

        /// <summary>
        /// Add information general to all steps. 
        /// Also initialize chart-parameters for the step.
        /// Step Status can not be put in here, since it is also used for the different steps with multiple tests, this will lead to a bug. 
        /// </summary>
        /// <param name="match"></param>
        private void AddGeneralStepInformation(Step currentStep, SearchFields.SearchMatch match)
        {
            InitChart();

            //process general fields if they exist    
            if (match.ExistSubField("StepExecutionTime") && (double)match.GetSubField("StepExecutionTime") > 0)
                currentStep.StepTime = (double)match.GetSubField("StepExecutionTime");
            if (match.ExistSubField("StepReportText") && ((string)match.GetSubField("StepReportText")) != "")
                currentStep.ReportText = (string)match.GetSubField("StepReportText");
            if (match.ExistSubField("StepErrorCode"))
                currentStep.StepErrorCode = (int)match.GetSubField("StepErrorCode");
            if (match.ExistSubField("StepErrorMessage") && ((string)match.GetSubField("StepErrorMessage")) != "")
                currentStep.StepErrorMessage = (string)match.GetSubField("StepErrorMessage");
            if (match.ExistSubField("CausedSequenceFailure") && ((string)match.GetSubField("CausedSequenceFailure") != ""))
                currentStep.CausedSequenceFailure = (bool)ConvertStringToAny((string)match.GetSubField("CausedSequenceFailure"), typeof(bool), null, null);
        }

        /// <summary>
        /// Initializes the chart for a new step. 
        /// This is necessary to reset the currentChart object and series-count to add a new chart to the correct step. 
        /// </summary>
        private void InitChart()
        {
            currentChart = null;
            stepHasMoreThanOneChart = false; //used to discard Series-lines if more than one chart
            currentChartSeriesCount = 0;  //reset series count to 0 after new chart
        }

        /// <summary>
        /// Checks if a current chart exists and throws an exception if it does. 
        /// </summary>
        private void CheckCurrentChart()
        {
            if (currentChart != null)
            {
                stepHasMoreThanOneChart = true;
                throw new TextFormatException("The step can not have more than one chart.");
            }
            else
            {
                stepHasMoreThanOneChart = false;
            }
        }

        /// <summary>
        /// Checks if a field in the text file exist and is not empty.
        /// </summary>
        /// <param name="match">The matched line.</param>
        /// <param name="fieldName">The name of the field.</param>
        /// <returns>Bool if the field exists or not.</returns>
        private string CheckAndGetField(TextConverterBase.SearchFields.SearchMatch match, string fieldName, bool required)
        {
            if (match.ExistSubField(fieldName) && ((string)match.GetSubField(fieldName)) != "")
            {
                return (string)match.GetSubField(fieldName);
            }
            else
            {
                if (required)
                {
                    throw new TextFormatException("The " + fieldName + " field does not exixt or is empty.");
                }
                else
                {
                    return null;
                }
            }
        }

        /// <summary>
        /// Splits the input of a Series up in an array.
        /// Changes , to . before split
        /// Converts the strings into double.
        /// Throws a TextFormatException if the count of the elements is more than 10000.
        /// </summary>
        /// <param name="stringData">Input string.</param>
        /// <returns>Array of the Series in double format.</returns>
        private double[] SplitAndParseSeriesData(string stringData)
        {
            char[] delimiterChars = { ';' };
            int maxXYCount = 10000;

            if (stringData.Contains(','))
            {
                //ParseError("Series contains comma instead of dot in line, will be replaced", "Series with stringData: " + stringData);
                stringData = stringData.Replace(',', '.'); //replace comma with dot
            }

            string[] tempData = stringData.Split(delimiterChars, StringSplitOptions.None);

            if (tempData.Count() > maxXYCount)
            {
                throw new TextFormatException("Too many elements in one of the data fields.");
            }

            return tempData.Select(s => ParseChartDouble(s)).Take(maxXYCount).ToArray();
        }

        /// <summary>
        /// Parses a string into a double. 
        /// Throws TextFormatException if the conversion fails.
        /// </summary>
        /// <param name="s">input field</param>
        /// <returns>double value of input field.</returns>
        private double ParseChartDouble(string s)
        {
            double d;

            bool result = Double.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out d);

            if (!result)
            {
                throw new TextFormatException("Conversion error for a value in the Series data, field: " + s);
            }

            return d;
        }

        private void AddNumericLimitTest(NumericLimitStep step, double measure, CompOperatorType compOp, double lowLimit, double highLimit, string unit, StepStatusType? status = null)
        {
            switch (compOp)
            {
                case CompOperatorType.LOG:
                    if(status.HasValue)
                        step.AddTest(measure, unit, status.Value);
                    else
                        step.AddTest(measure, unit);
                    break;
                case CompOperatorType.EQ:
                case CompOperatorType.NE:
                case CompOperatorType.GE:
                case CompOperatorType.GT:
                case CompOperatorType.LE:
                case CompOperatorType.LT:
                    if (status.HasValue)
                        step.AddTest(measure, compOp, lowLimit, unit, status.Value);
                    else
                        step.AddTest(measure, compOp, lowLimit, unit);
                    break;
                case CompOperatorType.GELE:
                case CompOperatorType.GELT:
                case CompOperatorType.GTLE:
                case CompOperatorType.GTLT:
                case CompOperatorType.LEGE:
                case CompOperatorType.LEGT:
                case CompOperatorType.LTGE:
                case CompOperatorType.LTGT:
                    if (status.HasValue)
                        step.AddTest(measure, compOp, lowLimit, highLimit, unit, status.Value);
                    else
                        step.AddTest(measure, compOp, lowLimit, highLimit, unit);
                    break;
            }
        }       

        private void AddNumericLimitMultipleTest(NumericLimitStep step, double measure, CompOperatorType compOp, double lowLimit, double highLimit, string unit, string measureName, StepStatusType? status = null)
        {
            switch (compOp)
            {
                case CompOperatorType.LOG:
                    if (status.HasValue)
                        step.AddMultipleTest(measure, unit, measureName, status.Value);
                    else
                        step.AddMultipleTest(measure, unit, measureName);
                    break;
                case CompOperatorType.EQ:
                case CompOperatorType.NE:
                case CompOperatorType.GE:
                case CompOperatorType.GT:
                case CompOperatorType.LE:
                case CompOperatorType.LT:
                    if (status.HasValue)
                        step.AddMultipleTest(measure, compOp, lowLimit, unit, measureName, status.Value);
                    else
                        step.AddMultipleTest(measure, compOp, lowLimit, unit, measureName);
                    break;
                case CompOperatorType.GELE:
                case CompOperatorType.GELT:
                case CompOperatorType.GTLE:
                case CompOperatorType.GTLT:
                case CompOperatorType.LEGE:
                case CompOperatorType.LEGT:
                case CompOperatorType.LTGE:
                case CompOperatorType.LTGT:
                    if (status.HasValue)
                        step.AddMultipleTest(measure, compOp, lowLimit, highLimit, unit, measureName, status.Value);
                    else
                        step.AddMultipleTest(measure, compOp, lowLimit, highLimit, unit, measureName);
                    break;
            }              
        }

        // Only for configurator to get default arguments
        public WATSStandardTextFormat() : base() { }

        public WATSStandardTextFormat(IDictionary<string, string> args) : base(args)
        {
            if (!args.ContainsKey("cultureCode"))
            {
                this.currentCulture = CultureInfo.InvariantCulture;
                this.searchFields.culture = CultureInfo.InvariantCulture;
            }

            searchFields.AddExactField("StartTest", ReportReadState.Unknown, "--Header-Start--", null, typeof(string), true, ReportReadState.InHeader);
            searchFields.AddExactField(UUTField.SerialNumber, ReportReadState.InHeader, "SerialNumber", null, typeof(string));
            searchFields.AddExactField(UUTField.PartNumber, ReportReadState.InHeader, "PartNumber", null, typeof(string));
            searchFields.AddExactField(UUTField.PartRevisionNumber, ReportReadState.InHeader, "Revision", null, typeof(string));
            searchFields.AddExactField(UUTField.OperationTypeName, ReportReadState.InHeader, "OperationTypeName", null, typeof(string));
            searchFields.AddExactField(UUTField.OperationTypeCode, ReportReadState.InHeader, "OperationTypeCode", null, typeof(string));
            //Accept UUTStatus in both header and test, last wins
            searchFields.AddExactField(UUTField.Status, ReportReadState.InHeader, "UUTStatus", null, typeof(UUTStatusType));
            searchFields.AddExactField(UUTField.Status, ReportReadState.InTest, "UUTStatus", null, typeof(UUTStatusType)); //can remove after test
            searchFields.AddExactField(UUTField.ErrorCode, ReportReadState.InHeader, "ErrorCode", null, typeof(int));
            //searchFields.AddExactField(UUTField.ErrorCode, ReportReadState.InTest, "ErrorCode", null, typeof(int)); //can remove after test
            searchFields.AddExactField(UUTField.ErrorMessage, ReportReadState.InHeader, "ErrorMessage", null, typeof(string));
            searchFields.AddExactField(UUTField.StartDateTime, ReportReadState.InHeader, "StartDateTime", "yyyy-MM-ddTHH:mm:ss", typeof(DateTime));
            searchFields.AddExactField(UUTField.StartDatetimeUTC, ReportReadState.InHeader, "UTCStartDateTime", "yyyy-MM-ddTHH:mm:ss", typeof(DateTime));
            searchFields.AddExactField(UUTField.ExecutionTime, ReportReadState.InHeader, "ExecutionTime", null, typeof(double));
            searchFields.AddExactField(UUTField.StationName, ReportReadState.InHeader, "StationName", null, typeof(string));
            searchFields.AddExactField(UUTField.Operator, ReportReadState.InHeader, "OperatorName", null, typeof(string));
            searchFields.AddExactField(UUTField.TestSocketIndex, ReportReadState.InHeader, "TestSocketIndex", null, typeof(short));
            searchFields.AddExactField(UUTField.FixtureId, ReportReadState.InHeader, "FixtureId", null, typeof(string));
            searchFields.AddExactField(UUTField.SequenceName, ReportReadState.InHeader, "SoftwareName", null, typeof(string));
            searchFields.AddExactField(UUTField.SequenceVersion, ReportReadState.InHeader, "SoftwareVersion", null, typeof(string));
            searchFields.AddExactField(UUTField.BatchSerialNumber, ReportReadState.InHeader, "BatchSerialNumber", null, typeof(string));
            searchFields.AddExactField(UUTField.Comment, ReportReadState.InHeader, "Comment", null, typeof(string));
            searchFields.AddExactField(UUTField.ConverterMode, ReportReadState.InHeader, "ConverterMode", null, typeof(string));
            //Not in use, add as misc info..  searchFields.AddExactField("StardardFormatVersion", ReportReadState.InHeader, "uCSwVer", null, typeof(string));
            searchFields.AddExactField(UUTField.UserDefined, ReportReadState.InHeader, "--Step-Data-Start--", null, typeof(string), true, ReportReadState.InTest);

            SearchFields.ExactSearchField field;
            field = searchFields.AddExactField("Subunit", ReportReadState.InHeader, "Subunit", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("Subunit", typeof(string));
            field.AddSubField("Description", typeof(string));
            field.AddSubField("PartNumber", typeof(string));
            field.AddSubField("SerialNumber", typeof(string));
            field.AddSubField("Revision", typeof(string));

            field = searchFields.AddExactField("SequenceCall", ReportReadState.InTest, "SequenceCall", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(string));
            field.AddSubField("LowLimit", typeof(double));
            field.AddSubField("HighLimit", typeof(double));
            field.AddSubField("CompOperator", typeof(string));
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("EndSequenceCall", ReportReadState.InTest, "EndSequenceCall", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(string));
            field.AddSubField("LowLimit", typeof(double));
            field.AddSubField("HighLimit", typeof(double));
            field.AddSubField("CompOperator", typeof(string));
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("NumericLimitTest", ReportReadState.InTest, "NumericLimitTest", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(double));
            field.AddSubField("LowLimit", typeof(double));
            field.AddSubField("HighLimit", typeof(double));
            field.AddSubField("CompOperator", typeof(CompOperatorType));
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("MultipleNumericLimitTest", ReportReadState.InTest, "MultipleNumericLimitTest", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(double));
            field.AddSubField("LowLimit", typeof(double));
            field.AddSubField("HighLimit", typeof(double));
            field.AddSubField("CompOperator", typeof(string)); //NB! due to main line not having it
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("EndMultipleNumericLimitTest", ReportReadState.InTest, "EndMultipleNumericLimitTest", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(double));
            field.AddSubField("LowLimit", typeof(double));
            field.AddSubField("HighLimit", typeof(double));
            field.AddSubField("CompOperator", typeof(string)); //NB! due to main line not having it
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("PassFailTest", ReportReadState.InTest, "PassFailTest", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(bool));
            field.AddSubField("LowLimit", typeof(string));
            field.AddSubField("HighLimit", typeof(string));
            field.AddSubField("CompOperator", typeof(string));
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("StringValueTest", ReportReadState.InTest, "StringValueTest", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(string));
            field.AddSubField("StringLimit", typeof(string));
            field.AddSubField("HighLimit", typeof(string)); //Not used
            field.AddSubField("CompOperator", typeof(CompOperatorType));
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("MultipleStringValueTest", ReportReadState.InTest, "MultipleStringValueTest", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(string));
            field.AddSubField("StringLimit", typeof(string));
            field.AddSubField("HighLimit", typeof(string)); //Not used
            field.AddSubField("CompOperator", typeof(string)); //NB! due to main line not having it
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            field = searchFields.AddExactField("ActionStep", ReportReadState.InTest, "ActionStep", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string));
            field.AddSubField("StepName", typeof(string));
            field.AddSubField("MeasureName", typeof(string));
            field.AddSubField("Value", typeof(string));
            field.AddSubField("StringLimit", typeof(string));
            field.AddSubField("HighLimit", typeof(string)); //Not used
            field.AddSubField("CompOperator", typeof(string));
            field.AddSubField("Unit", typeof(string));
            field.AddSubField("Status", typeof(string));
            field.AddSubField("StepExecutionTime", typeof(double));
            field.AddSubField("StepReportText", typeof(string));
            field.AddSubField("StepErrorCode", typeof(int));
            field.AddSubField("StepErrorMessage", typeof(string));
            field.AddSubField("CausedSequenceFailure", typeof(string));

            //Chart
            field = searchFields.AddExactField("Chart", ReportReadState.InTest, "Chart", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string)); //Chart //Not used for attachments
            field.AddSubField("StepName", typeof(string)); //charttype //Code assumes that StepName and MeasureName exists with those names
            field.AddSubField("MeasureName", typeof(string)); //Label //Code assumes that StepName and MeasureName exists with those names
            field.AddSubField("YUnit", typeof(string)); //Y Unit 
            field.AddSubField("YLabel", typeof(string)); // Y Label
            field.AddSubField("XUnit", typeof(string)); //X Unit
            field.AddSubField("XLabel", typeof(string)); // X Label

            //Series/plot of chart
            field = searchFields.AddExactField("Series", ReportReadState.InTest, "Series", null, typeof(string));
            field.delimiters = new char[] { '\t' };
            field.AddSubField("StepType", typeof(string)); //Series 
            field.AddSubField("StepName", typeof(string)); //Plotname //Code assumes that StepName and MeasureName exists with those names
            field.AddSubField("MeasureName", typeof(string)); //Datatype //Code assumes that StepName and MeasureName exists with those names //always XYG
            field.AddSubField("YData", typeof(string)); //Y Data
            field.AddSubField("XData", typeof(string)); //X Data //not used for attachements

            searchFields.AddExactField(UUTField.UserDefined, ReportReadState.InTest, "--Step-Data-End--", null, typeof(string), true, ReportReadState.InFooter);

            searchFields.AddExactField(UUTField.Status, ReportReadState.InFooter, "UUTStatus", null, typeof(UUTStatusType));
            searchFields.AddExactField(UUTField.ErrorCode, ReportReadState.InFooter, "ErrorCode", null, typeof(int));
            searchFields.AddExactField(UUTField.ErrorMessage, ReportReadState.InFooter, "ErrorMessage", null, typeof(string));
            searchFields.AddExactField(UUTField.ExecutionTime, ReportReadState.InFooter, "ExecutionTime", null, typeof(double));

            searchFields.AddExactField("EndTest", ReportReadState.InFooter, "-- UUT-End--", null, typeof(string), true, ReportReadState.EndOfFile);
            searchFields.AddExactField("EndTest", ReportReadState.InFooter, "--UUT-End--", null, typeof(string), true, ReportReadState.EndOfFile);

        }

    }


    /// <summary>
    /// TextFormatException to be used for problems in the text file. 
    /// </summary>
    public class TextFormatException : System.Exception
    {
        public TextFormatException(string txt)
            : base(txt)
        {
        }
    }
}
