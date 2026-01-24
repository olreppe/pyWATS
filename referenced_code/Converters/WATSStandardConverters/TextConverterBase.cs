using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Interface;
using System.IO;
using System.Globalization;
using System.Text.RegularExpressions;

namespace Virinco.WATS.Integration.TextConverter
{
    public abstract class TextConverterBase : IReportConverter_v2
    {

        protected abstract bool ProcessMatchedLine(SearchFields.SearchMatch match, ref ReportReadState readState);
        protected virtual bool ProcessNonMatchLine(string line, ref ReportReadState readState) { return true; }
        protected virtual string PreProcessLine(string line) { return line; }

        const NumberStyles numberStylesAllowed = NumberStyles.AllowThousands | NumberStyles.AllowDecimalPoint | NumberStyles.AllowExponent | NumberStyles.AllowLeadingSign | NumberStyles.AllowLeadingWhite | NumberStyles.AllowParentheses | NumberStyles.AllowTrailingWhite;

        public enum UUTField
        {
            UserDefined,
            UseSubFields,
            OperationTypeCode,
            OperationTypeName,
            SerialNumber,
            PartNumber,
            PartRevisionNumber,
            StartDateTime,
            StartDatetimeUTC,
            BatchSerialNumber,
            SequenceName,
            SequenceVersion,
            Status,
            ErrorCode,
            ErrorMessage,
            ExecutionTime,
            StationName,
            FixtureId,
            TestSocketIndex,
            Operator,
            Comment,
            MiscUUTInfo, 
            ConverterMode
        }

        public enum ReportReadState
        {
            Unknown,
            InHeader,
            InTest,
            InFooter,
            EndOfFile
        }

        public class SearchFields
        {
            public CultureInfo culture;
            public SearchFields(CultureInfo cultureInfo)
            {
                culture = cultureInfo;
            }

            public class SubField
            {
                public string name;
                public Type type;
                public string formatString;
                public UUTField uutField;
            }

            List<SearchField> searchFields = new List<SearchField>();
            public class SearchField
            {
                public CultureInfo culture;
                public UUTField uutField { get; set; }
                public List<SubField> subFields { get; set; }
                public string fieldName { get; set; }
                public ReportReadState readState { get; set; }
                public ReportReadState nextReadState { get; set; }
                public Type fieldType { get; set; }
                public string formatString { get; set; }
                public int startPosition { get; set; }
                public int length { get; set; }
                public virtual SearchMatch FindMatch(string line) { return null; }
                public void AddSubField(string subfieldName, Type type, string formatString = null, UUTField uutField = UUTField.UserDefined)
                {
                    if (subFields == null) subFields = new List<SubField>();
                    subFields.Add(new SubField() { name = subfieldName, type = type, formatString = formatString, uutField = uutField });
                }
            }


            public class ExactSearchField : SearchField
            {
                public string searchFor { get; set; }
                public bool searchFromStartOnly { get; set; }
                public char[] delimiters { get; set; }
                public bool ignoreCase { get; set; }

                public override SearchMatch FindMatch(string line)
                {
                    SearchMatch match = null;
                    if ((startPosition != -1 || length != -1) && line.Length >= startPosition + length)
                        line = line.Substring(startPosition, length); //Truncate before search
                    if (ignoreCase)
                    {
                        line = line.ToLower();
                        searchFor = searchFor.ToLower();
                    }
                    int matchIndex = line.IndexOf(searchFor);
                    if (searchFromStartOnly && matchIndex == 0 || !searchFromStartOnly && matchIndex >= 0)
                        match = new SearchMatch() { matchField = this, completeLine = line };
                    else
                        return null;
                    if (subFields != null && delimiters == null)
                        throw new ApplicationException("Subfields for ExactSearchFields requires delimiters");
                    if (delimiters != null)
                        match.splittedLine = line.Split(delimiters);
                    List<object> results = new List<object>();
                    if (subFields != null) //Process sub-fields
                    {
                        for (int i = 0; i < subFields.Count && i < match.splittedLine.Length; i++)
                            results.Add(ConvertStringToAny(match.splittedLine[i].Trim(), subFields[i].type, subFields[i].formatString, culture));
                    }
                    else //Single value
                        results.Add(ConvertStringToAny(line.Substring(matchIndex + searchFor.Length).Trim(), fieldType, formatString, culture));
                    match.results = results.ToArray();
                    return match;
                }
            }

            public class RegExpSearchField : SearchField
            {
                public string regExp { get; set; }

                public override SearchMatch FindMatch(string line)
                {
                    SearchMatch match = null;
                    if ((startPosition != -1 || length != -1) && line.Length >= startPosition + length)
                        line = line.Substring(startPosition, length); //Truncate before search
                    Regex regex = new Regex(regExp);
                    Match regMatch = regex.Match(line);
                    if (regMatch.Success)
                    {
                        match = new SearchMatch() { matchField = this, completeLine = line, regExpMatch = regMatch };
                        List<object> results = new List<object>();
                        if (subFields != null)
                            for (int i = 0; i < subFields.Count; i++)
                            {
                                results.Add(ConvertStringToAny(regMatch.Groups[subFields[i].name].Value, subFields[i].type, subFields[i].formatString, culture));
                            }
                        else
                            results.Add(ConvertStringToAny(regMatch.Groups[1].Value, fieldType, formatString, culture));
                        match.results = results.ToArray();
                    }
                    return match;
                }
            }

            public class SearchMatch
            {
                public SearchField matchField { get; set; }
                public string completeLine { get; set; }
                public string[] splittedLine { get; set; }
                public Match regExpMatch { get; set; }
                public object[] results { get; set; }
                public object GetSubField(string subFieldName)
                {
                    if (matchField.subFields == null)
                        throw new ArgumentException("Searchfield has no defined subfields: " + matchField.uutField.ToString() + " " + matchField.fieldName);
                    SubField subField = matchField.subFields.Where(s => s.name == subFieldName).FirstOrDefault();
                    if (subField == null)
                        throw new ArgumentException("Subfield not found: " + " " + subFieldName);
                    int index = matchField.subFields.IndexOf(subField);
                    if (index > results.Length)
                        throw new ArgumentException("Subfield not found in values: " + " " + subFieldName);
                    return results[index];
                }
                public bool ExistSubField(string subFieldName)
                {
                    if (matchField.subFields == null) return false;
                    SubField subField = matchField.subFields.Where(s => s.name == subFieldName).FirstOrDefault();
                    if (subField == null) return false;
                    int index = matchField.subFields.IndexOf(subField);
                    if (index >= results.Length) return false;
                    return true;
                }
            }

            //Add UUT field
            public ExactSearchField AddExactField(UUTField uutField, ReportReadState readState, string searchFor, string formatString, Type fieldType, bool searchFromStartOnly = true, ReportReadState nextReadState = ReportReadState.Unknown, int lookAtStartPos = -1, int lookAtLength = -1, bool ignoreCase = false)
            {
                ExactSearchField sf = new ExactSearchField() { uutField = uutField, readState = readState, searchFor = searchFor, formatString = formatString, fieldType = fieldType, searchFromStartOnly = searchFromStartOnly, nextReadState = nextReadState, culture = culture, startPosition = lookAtStartPos, length = lookAtLength, ignoreCase = ignoreCase };
                searchFields.Add(sf);
                return sf;
            }

            //Add user defined field
            public ExactSearchField AddExactField(string fieldName, ReportReadState readState, string searchFor, string formatString, Type fieldType, bool searchFromStartOnly = true, ReportReadState nextReadState = ReportReadState.Unknown, int lookAtStartPos = -1, int lookAtLength = -1, bool ignoreCase = false)
            {
                ExactSearchField sf = new ExactSearchField() { uutField = UUTField.UserDefined, readState = readState, fieldName = fieldName, searchFor = searchFor, formatString = formatString, fieldType = fieldType, searchFromStartOnly = searchFromStartOnly, nextReadState = nextReadState, startPosition = lookAtStartPos, length = lookAtLength, ignoreCase = ignoreCase, culture = culture };
                searchFields.Add(sf);
                return sf;
            }

            public RegExpSearchField AddRegExpField(UUTField uutField, ReportReadState readState, string regExp, string formatString, Type fieldType, ReportReadState nextReadState = ReportReadState.Unknown, int lookAtStartPos = -1, int lookAtLength = -1)
            {
                RegExpSearchField sf = new RegExpSearchField() { uutField = uutField, readState = readState, regExp = regExp, formatString = formatString, fieldType = fieldType, nextReadState = nextReadState, culture = culture, startPosition = lookAtStartPos, length = lookAtLength };
                searchFields.Add(sf);
                return sf;
            }

            public RegExpSearchField AddRegExpField(string fieldName, ReportReadState readState, string regExp, string formatString, Type fieldType, ReportReadState nextReadState = ReportReadState.Unknown, int lookAtStartPos = -1, int lookAtLength = -1)
            {
                RegExpSearchField sf = new RegExpSearchField() { fieldName = fieldName, readState = readState, regExp = regExp, formatString = formatString, fieldType = fieldType, nextReadState = nextReadState, culture = culture, startPosition = lookAtStartPos, length = lookAtLength };
                searchFields.Add(sf);
                return sf;
            }

            public SearchMatch[] FindMatches(string line, ReportReadState reportState, bool returnJustFirstMatch = true)
            {
                List<SearchMatch> matches = new List<SearchMatch>();
                foreach (SearchField f in searchFields)
                {
                    if (f.readState == ReportReadState.Unknown || reportState == f.readState)
                    {
                        SearchMatch match = f.FindMatch(line);
                        if (match != null)
                        {
                            matches.Add(match);
                            if (returnJustFirstMatch)
                                break;
                        }
                    }
                }
                return matches.ToArray();
            }
        }

        //Helper variables
        protected SearchFields searchFields;
        protected CultureInfo currentCulture;
        protected TestModeType testModeType = TestModeType.Active;
        protected StreamWriter logStream = null;
        protected StreamWriter errorStream = null;
        StreamReader reader = null;
        protected TDM apiRef;
        protected int lineCount = 0;
        protected IDictionary<string, string> converterArguments;

        protected UUTReport currentUUT;
        protected bool firstTestInFile;
        protected SequenceCall currentSequence;
        protected Step currentStep;
        protected NumericLimitTest currentNumLimTest;
        protected PassFailTest currentPassFailTest;
        protected StringValueTest currentStringValueTest;
        protected ReportReadState currentReportState = ReportReadState.InHeader;
        TimeZone zone = TimeZone.CurrentTimeZone;

        public Dictionary<string, string> ConverterParameters =>(Dictionary<string, string>)converterArguments;

        public Dictionary<string,string> GetDefaultArguments()
        {
            return new Dictionary<string, string>()
            {
                { "operationTypeCode", "10" },
                { "testModeType", "Active" },
                { "operator", "sysoper" },
                { "stationName", Env.StationName },
                { "sequenceName", "SeqName" },
                { "sequenceVersion", "0.0.0" },
                { "cultureCode", "en-US" },
                { "fileEncoding", "1252" },
                { "validationMode", ValidationModeType.ThrowExceptions.ToString() }
            };
        }

        public TextConverterBase() {
            converterArguments = GetDefaultArguments();
            currentCulture = new CultureInfo(converterArguments["cultureCode"]);
            searchFields = new SearchFields(currentCulture);
        }

        public TextConverterBase(IDictionary<string, string> args)
        {
            //Setup default from Converter.xml arguments
            converterArguments = args;
            Dictionary<string, string> defaultArgs = GetDefaultArguments();
            //Merge default arguments to support upgrade from 5.x clients
            foreach (KeyValuePair<string,string> keyValuePair in defaultArgs)
            {
                if (!converterArguments.ContainsKey(keyValuePair.Key))
                {
                    converterArguments.Add(keyValuePair);
                }
            }
            currentCulture = new CultureInfo(converterArguments["cultureCode"]);
            searchFields = new SearchFields(currentCulture);
        }

        public void CleanUp()
        {
            return;
        }

        protected void CreateDefaultUUT()
        {
            try
            {
                //Create UUT with defaults
                currentUUT = apiRef.CreateUUTReport(converterArguments["operator"], "", "", "", converterArguments["operationTypeCode"], "", "");
                currentUUT.StationName = converterArguments["stationName"]; 
                currentUUT.StartDateTimeUTC = DateTime.UtcNow;
                currentUUT.StartDateTime = zone.ToLocalTime(currentUUT.StartDateTimeUTC);
                currentSequence = currentUUT.GetRootSequenceCall();
                currentStep = currentSequence;
                currentUUT.SequenceName = converterArguments["sequenceName"];
                currentUUT.SequenceVersion = converterArguments["sequenceVersion"];
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error in CreateDefaultUUT", ex);
            }
        }

        protected void CreateNumLimStep(string stepName, double measure = 0, string unit = "")
        {
            currentStep = currentSequence.AddNumericLimitStep(stepName);
            currentNumLimTest = ((NumericLimitStep)currentStep).AddTest(measure, unit);
        }

        protected void MakeFileCopy(string catalog)
        {
            string directoryTo = Path.Combine(apiRef.ConversionSource.SourceFile.DirectoryName, catalog);
            if (!Directory.Exists(directoryTo))
                Directory.CreateDirectory(directoryTo);
            reader.BaseStream.Seek(0, SeekOrigin.Begin);
            StreamWriter writer = new StreamWriter(Path.Combine(directoryTo, apiRef.ConversionSource.SourceFile.Name));
            string buffer = reader.ReadToEnd();
            writer.Write(buffer);
            writer.Close();
        }

        protected void SubmitUUT()
        {
            //Check before sending
            if (String.IsNullOrEmpty(currentUUT.SerialNumber)) throw new ApplicationException("Serial number is missing");
            if (String.IsNullOrEmpty(currentUUT.PartNumber)) throw new ApplicationException("Part number is missing");
            logStream.WriteLine("{0}\t{1}\tCalling submit thread {2}", DateTime.Now.ToString("yyyy.MM.dd HH:mm:ss"), currentUUT.SerialNumber, System.Threading.Thread.CurrentThread.ManagedThreadId.ToString());
            apiRef.Submit(SubmitMethod.Offline, currentUUT);
            logStream.WriteLine("{0}\t{1}\tQueued ok", DateTime.Now.ToString("yyyy.MM.dd HH:mm:ss"), currentUUT.SerialNumber);
        }

        public virtual Report ImportReport(TDM api, System.IO.Stream file)
        {
            #if NET8_0_OR_GREATER
                Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            #endif

            if(Utilities.EnumTryParse(converterArguments["validationMode"], out ValidationModeType validationModeType))
                api.ValidationMode = validationModeType;

            lineCount = 0; //Global line count
            try
            {
                currentReportState = ReportReadState.InHeader;
                firstTestInFile = true;
                apiRef = api;
                CreateDefaultUUT();
                if (apiRef.ConversionSource.SourceFile.Extension.ToLower() == ".pdf")
                    //Overload of virtual must handle pdf parsing
                    reader = new StreamReader(file);
                else if (apiRef.ConversionSource.SourceFile.Extension.ToLower() == ".rtf")
                    reader = new RTFStream(file);
                else
                    reader = new StreamReader(file, Encoding.GetEncoding(int.Parse(converterArguments["fileEncoding"])));
                api.TestMode = testModeType;
                logStream = new StreamWriter(api.ConversionSource.ConversionLog);
                logStream.WriteLine("{0}\tStarting convert on thread {1} - {2}", DateTime.Now.ToString("yyyy.MM.dd HH:mm:ss"), System.Threading.Thread.CurrentThread.ManagedThreadId, apiRef.ConversionSource.SourceFile.Name);
                ReadFile(reader, api);
                logStream.WriteLine("{0}\tFinished convertion", DateTime.Now.ToString("yyyy.MM.dd HH:mm:ss"));
            }
            catch (Exception ex)
            {
                ParseError("ImportReport: " + ex.Message + (ex.InnerException == null ? "" : "\r\n" + ex.InnerException.Message), lineCount.ToString());
                throw;
            }
            finally
            {
                logStream.Flush();
                if (errorStream != null)
                {
                    errorStream.Flush();
                    errorStream = null;
                }
            }
            return null;
        }


        void ReadFile(StreamReader r, TDM api)
        {
            string line = "";
            try
            {
                line = GetNextNonBlankLine(r);
                while (line != null)
                {
                    line = PreProcessLine(line); //Makes it possible to alter input line before processing
                    SearchFields.SearchMatch[] matches = searchFields.FindMatches(line, currentReportState); //TODO: Handle more than one match.. Makes sense?
                    if (matches.Length > 0)
                    {
                        SearchFields.SearchMatch match = matches[0]; //Just use first match
                        if (match.matchField.uutField != UUTField.UserDefined)
                        {
                            if (match.matchField.uutField == UUTField.UseSubFields)
                            {
                                for (int i = 0; i < match.matchField.subFields.Count; i++)
                                {
                                    ProcessUUTField(match.matchField.subFields[i].uutField, match.results[i], match, match.matchField.subFields[i].name);
                                }
                            }
                            else
                            {
                                 if (match.matchField is SearchFields.ExactSearchField) //Use Search criterion as description
                                    ProcessUUTField(match.matchField.uutField, match.results[0], match,((SearchFields.ExactSearchField)match.matchField).searchFor);
                                 else
                                    ProcessUUTField(match.matchField.uutField, match.results[0], match, match.matchField.fieldName);
                            }
                        }
                        //Call User code
                        if (!ProcessMatchedLine(match, ref currentReportState))
                            return; //Stop the import
                                    //Handle NextReadState if set
                        if (match.matchField.nextReadState != ReportReadState.Unknown && match.matchField.nextReadState != currentReportState)
                            currentReportState = match.matchField.nextReadState;
                    }
                    else
                        if (!ProcessNonMatchLine(line, ref currentReportState))
                        return; //Stop the import                       

                    line = GetNextNonBlankLine(r);
                }
                currentReportState = ReportReadState.EndOfFile;
                ProcessMatchedLine(null, ref currentReportState);
                ProcessNonMatchLine("", ref currentReportState);
            }
            catch (Exception ex)
            {
                ParseError(String.Format("ReadFile {0}", ex.Message + (ex.InnerException == null ? "" : "\r\nInner: " + ex.InnerException.Message)), line);
                throw; //Rethrow exeption
            }
        }

        private void ProcessUUTField(UUTField uutField, object value, SearchFields.SearchMatch match, string description="")
        {
            switch (uutField)
            {
                case UUTField.UserDefined:
                    break;
                case UUTField.MiscUUTInfo:
                    if (string.IsNullOrEmpty(description))
                        description = "Info";
                    if (!string.IsNullOrEmpty((string)value)) //Do not record blanks
                        currentUUT.AddMiscUUTInfo(description,(string)value);
                    break;
                case UUTField.OperationTypeCode:
                    currentUUT.OperationType = apiRef.GetOperationType((string)value);
                    break;
                case UUTField.OperationTypeName:
                    currentUUT.OperationType = GetOperationTypeByName((string)value);
                    break;
                case UUTField.SerialNumber:
                    currentUUT.SerialNumber = (string)value;
                    break;
                case UUTField.PartNumber:
                    currentUUT.PartNumber = (string)value;
                    break;
                case UUTField.PartRevisionNumber:
                    currentUUT.PartRevisionNumber = (string)value;
                    break;
                case UUTField.StartDateTime:
                    currentUUT.StartDateTime = (DateTime)value;                  
                    currentUUT.StartDateTimeUTC = zone.ToUniversalTime(currentUUT.StartDateTime);
                    break;
                case UUTField.StartDatetimeUTC:
                    currentUUT.StartDateTimeUTC = (DateTime)value;
                    currentUUT.StartDateTime = zone.ToLocalTime(currentUUT.StartDateTimeUTC);
                    break;
                case UUTField.BatchSerialNumber:
                    currentUUT.BatchSerialNumber = (string)value;
                    break;
                case UUTField.SequenceName:
                    currentUUT.SequenceName = (string)value;
                    break;
                case UUTField.SequenceVersion:
                    currentUUT.SequenceVersion = (string)value;
                    break;
                case UUTField.Status:
                    currentUUT.Status = (UUTStatusType)value;
                    break;
                case UUTField.ErrorCode:
                    currentUUT.ErrorCode = (int)value;
                    break;
                case UUTField.ErrorMessage:
                    currentUUT.ErrorMessage = (string)value;
                    break;
                case UUTField.ExecutionTime:
                    if (value is TimeSpan)
                        currentUUT.ExecutionTime = ((TimeSpan)value).TotalMilliseconds / 1000.0;
                    else
                        currentUUT.ExecutionTime = (double)value;
                    break;
                case UUTField.StationName:
                    currentUUT.StationName = (string)value;
                    break;
                case UUTField.FixtureId:
                    currentUUT.FixtureId = (string)value;
                    break;
                case UUTField.TestSocketIndex:
                    currentUUT.TestSocketIndex = (short)value;
                    break;
                case UUTField.Operator:
                    currentUUT.Operator = (string)value;
                    break;
                case UUTField.Comment:
                    currentUUT.Comment = (string)value;
                    break;
                case UUTField.ConverterMode:
                    if ((string)value == "Import")
                    {
                        apiRef.TestMode = TestModeType.Import;
                    }
                    //otherwise ignore
                    break;
                default:
                    break;
            }

        }

        protected string GetNextLine()
        {
            return GetNextNonBlankLine(reader);
        }

        string GetNextNonBlankLine(StreamReader r)
        {
            string line = "";
            try
            {
                //Read next non-blank line
                //if (r is PDFStream)
                //{
                //    PDFStream s = (PDFStream)r;
                //    if (s.EndOfStream) //Due to lack of virtual for EndOfStream
                //        return null;
                //    do { line = s.ReadLine(); lineCount++; } while (!s.EndOfStream && line.Trim().Length == 0);
                //}
                //else 
                if (r is RTFStream)
                {
                    RTFStream s = (RTFStream)r;
                    if (s.EndOfStream) //Due to lack of virtual for EndOfStream
                        return null;
                    do { line = s.ReadLine(); lineCount++; } while (!s.EndOfStream && line.Trim().Length == 0);
                }
                else if (r is StreamReader)
                {
                    if (r.EndOfStream)
                        return null;
                    do { line = r.ReadLine(); lineCount++; } while (!r.EndOfStream && line.Trim().Length == 0);
                }
            }
            catch (Exception ex)
            {
                ParseError("GetNextNonBlankLine: " + ex.Message, line);
                throw ex;
            }
            return CleanInvalidXmlChars(line); //Removes invalid xml chars..
        }

        protected void ParseError(string err, string line)
        {
            if (errorStream == null)
            {
                errorStream = new StreamWriter(apiRef.ConversionSource.ErrorLog);
                errorStream.WriteLine("\n");
                errorStream.WriteLine("\n\rStart parsing: {0}", DateTime.Now);
            }
            errorStream.WriteLine("Parse error in line {0}: {1}", lineCount, err);

            if (!String.IsNullOrEmpty(line))
            {
                errorStream.WriteLine("Line: {0}", line);
            }
        }

        //protected bool CheckToken(TextLine token, LineType expected, string expectedArg0)
        //{
        //    if (token.lineType != expected || (expectedArg0.Length > 0 && (!((string)token.arguments[0]).StartsWith(expectedArg0))))
        //    {
        //        ParseError("Expected lineType: " + expected, token.originalLine);
        //        return false;
        //    }
        //    return true;
        //}

        protected OperationType GetOperationTypeByName(string optypeName)
        {
            OperationType[] optypes = apiRef.GetOperationTypes();
            OperationType optype = optypes.Where(p => p.Name == optypeName).SingleOrDefault();
            return optype;
        }

        #region String utils

        protected static object ConvertStringToAny(string input, Type type, string formatString, CultureInfo cultureInfo)
        {
            try
            {
                if (type == typeof(char))
                {
                    return input[0];
                }
                if (type == typeof(string))
                {
                    return input;
                }
                if (type == typeof(bool))
                {
                    if (input == "") return true;
                    if (input.ToLower() == "true" || input.ToLower() == "1") return true;
                    if (input.ToLower() == "false" || input.ToLower() == "0") return false;
                    throw new ApplicationException("Invalid boolean value: " + input);
                }
                if (type == typeof(byte))
                {
                    //Treat blank as zero //Only used for Error Code, no measurements
                    if (input == "") return (byte)0;
                    byte res = byte.Parse(input, NumberStyles.Any, cultureInfo.NumberFormat);
                    return res;
                }
                if (type == typeof(short))
                {
                    //Treat blank as zero //Only used for Error Code, no measurements
                    if (input == "") return (short)0;
                    short res = short.Parse(input, NumberStyles.Any, cultureInfo.NumberFormat);
                    return res;
                }
                if (type == typeof(int))
                {
                    //Treat blank as zero //Only used for Error Code, no measurements
                    if (input == "") return (int)0;
                    int res = int.Parse(input, NumberStyles.Any, cultureInfo.NumberFormat);
                    return res;
                }
                if (type == typeof(Double))
                {
                    if (input.Trim() == "") return Double.NaN;
                    Double res;
                    if (input.ToLower() == "inf" || input.ToLower() == "+inf")
                        res = double.PositiveInfinity;
                    else
                        if (input.ToLower() == "-inf")
                        res = double.NegativeInfinity;
                    else
                        res = Double.Parse(input, numberStylesAllowed, cultureInfo.NumberFormat);
                    return res;
                }
                if (type == typeof(DateTime))
                {
                    DateTime res = DateTime.ParseExact(input, formatString, cultureInfo);
                    return res;
                }
                if (type == typeof(TimeSpan))
                {
                    if (input == "") return new TimeSpan();
                    DateTime res = DateTime.ParseExact(input, formatString, cultureInfo);
                    if (res.Date == DateTime.Now.Date) //If no date component is given, current date is used
                    {

                        TimeSpan ts = new TimeSpan();
                        ts = res.Subtract(DateTime.Now.Date);
                        return ts;
                    }
                    return TimeSpan.FromTicks(res.Ticks);
                }
                if (type == typeof(UUTStatusType))
                {
                    UUTStatusType res =
                        input.ToLower() == "passed" ||
                        input.ToLower() == "pass" ? UUTStatusType.Passed :
                        input.ToLower() == "failed" ||
                        input.ToLower() == "fail" ? UUTStatusType.Failed :
                        input.ToLower() == "terminated" || input.ToLower() == "undetermined" ||
                        input.ToLower() == "aborted" ? UUTStatusType.Terminated :
                        input.ToLower() == "error" ? UUTStatusType.Error : UUTStatusType.Error;
                    if (res == UUTStatusType.Error && input.ToLower() != "error")
                        throw new ApplicationException("Invalid UUT status type: " + input);
                    return res;
                }
                if (type == typeof(StepStatusType))
                {
                    StepStatusType res =
                        input.ToLower() == "passed" ||
                        input.ToLower() == "pass" ? StepStatusType.Passed :
                        input.ToLower() == "failed" ||
                        input.ToLower() == "fail" ? StepStatusType.Failed :
                        input.ToLower() == "terminated" ? StepStatusType.Terminated :
                        input.ToLower() == "error" ? StepStatusType.Error :
                        input.ToLower() == "done" ? StepStatusType.Done :
                        input.ToLower() == "skipped" ? StepStatusType.Skipped : StepStatusType.Error;
                    if (res == StepStatusType.Error && input.ToLower() != "error")
                        throw new ApplicationException("Invalid step status type: " + input);
                    return res;
                }
                if (type == typeof(CompOperatorType))
                {
                    CompOperatorType res;
                    if (EnumTryParse<CompOperatorType>(input, out res))
                        return res;
                    else
                        throw new ApplicationException("Invalid compare operator: " + input);
                }
            }
            catch (Exception ex)
            {
                throw new ApplicationException($"Error in ConvertStringToAny: {input}->{type.Name} fmt:{formatString} culture:{cultureInfo.Name}");
            }
            return null;
        }

    protected static bool EnumTryParse<T>(string strType, out T result)
    {
        if (string.IsNullOrEmpty(strType)) { result = default(T); return false; }
        string strTypeFixed = strType.Replace(' ', '_');
        if (Enum.IsDefined(typeof(T), strTypeFixed))
        {
            result = (T)Enum.Parse(typeof(T), strTypeFixed, true);
            return true;
        }
        else
        {
            foreach (string value in Enum.GetNames(typeof(T)))
            {
                if (value.Equals(strTypeFixed, StringComparison.OrdinalIgnoreCase))
                {
                    result = (T)Enum.Parse(typeof(T), value);
                    return true;
                }
            }
            result = default(T);
            return false;
        }
    }

    protected static string CleanInvalidXmlChars(string text)
    {
        if (text == null)
            return null;
        // From xml spec valid chars: 
        // #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]     
        // any Unicode character, excluding the surrogate blocks, FFFE, and FFFF. 
        string re = @"[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD\u10000-u10FFFF]";
        return Regex.Replace(text, re, "");
    }

    protected static string GetStringFromDictionary(IDictionary<string, string> dict, string key, string defaultValue)
    {
        if (dict != null && dict.ContainsKey(key))
            return dict[key];
        else
            return defaultValue;
    }

    #endregion
}


}
