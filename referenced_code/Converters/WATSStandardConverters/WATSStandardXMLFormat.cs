using Virinco.WATS.Interface;
using System.IO;
using Virinco.WATS.Schemas.WRML;
using System;
using System.Linq;
using System.Xml.Serialization;
using System.Xml;
using System.Collections.Generic;

namespace Virinco.WATS.Integration.XMLConverter
{
    public class WATSStandardXMLFormat : IReportConverter_v2
    {
        protected Dictionary<string, string> converterArguments;

        public Dictionary<string, string> ConverterParameters => converterArguments;

        public WATSStandardXMLFormat(Dictionary<string, string> args)
        {
            //Setup default from Converter.xml arguments
            converterArguments = args;
        }

        public WATSStandardXMLFormat()
        {
            converterArguments = new Dictionary<string, string>() { { "operationTypeCode", "500" } };
        }

        public void CleanUp()
        {

        }

        public Report ImportReport(TDM api, Stream file)
        {
            WSXFConverter wsxfCnv = new WSXFConverter();
            XmlSerializer serializer = new XmlSerializer(typeof(Schemas.WSXF.Reports));
            Schemas.WSXF.Reports wsxfReports = (Schemas.WSXF.Reports)serializer.Deserialize(file);
            foreach (var wsxfReport in wsxfReports.Report)
            {
                Schemas.WRML.WATSReport wrmlReport = wsxfCnv.ConvertReport(wsxfReport);
                if (wrmlReport.type == ReportType.UUR)
                {
                    ValidateRepairProcess(api, wrmlReport);
                    ValidateProcess(api, (wrmlReport.Item as UUR_type).Process);
                }
                else //UUT
                    ValidateProcess(api, wrmlReport.Process);
                api.Submit(Report.Load(api, wrmlReport));
            }
            return null;
        }

        private void ValidateProcess(TDM api, Process_type process)
        {
            OperationType opType = null;
            if (process.CodeSpecified)
            {
                opType = api.GetOperationTypes().Where(op => short.Parse(op.Code) == process.Code).SingleOrDefault();
                if (opType == null)
                    throw new ArgumentException($"Process with code {process.Code} does not exist");
            }
            else if (!string.IsNullOrEmpty(process.Name))
            {
                opType = api.GetOperationTypes().Where(op => op.Name == process.Name).SingleOrDefault();
                if (opType == null)
                    throw new ArgumentException($"Process with name {process.Name} does not exist");

                process.Code = short.Parse(opType.Code);
                process.CodeSpecified = true;
            }
            else
                throw new ArgumentException("Neither process code nor process name is defined in report");
        }

        public Report ImportReport3(TDM api, Stream file)
        {
            Schemas.WSXF.Reports wsxfReports = null;

            try
            {
                wsxfReports = DeserializeReport<Schemas.WSXF.Reports>(file, @"http://wats.virinco.com/schemas/WATS/Report/wsxf", @"C:\Users\anders.kristiansen\Documents\Repos\Virinco\WATS\Main\Schemas\WATS WSXF Report.xsd");//@"C:\Program Files\Virinco\WATS\Schemas\WATS WSXF Report.xsd");
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error reading file", ex);
            }

            WSXFConverter conv = new WSXFConverter();

            if (wsxfReports != null)
            {
                foreach (Schemas.WSXF.WATSReport wsxfReport in wsxfReports.Report)
                {
                    Schemas.WRML.WATSReport wrmlReport = conv.ConvertReport(wsxfReport);

                    if (wrmlReport.type == ReportType.UUR)
                        ValidateRepairProcess(api, wrmlReport);

                    ValidateReport(wrmlReport);
                }
            }

            Report lastReport = null;
            for (int i = 0; i < conv.Reports.Count; i++)
            {
                Report report = Report.Load(api, conv.Reports[i]);

                if (i < conv.Reports.Count - 1)
                    api.Submit(SubmitMethod.Offline, report);
                else
                    lastReport = report;
            }

            return lastReport;
        }

        private void ValidateReport(Schemas.WRML.WATSReport wrmlReport)
        {
            string tempFilePath = $"{Path.GetTempFileName()}.xml";

            Schemas.WRML.Reports wrmlReports = new Schemas.WRML.Reports();
            wrmlReports.Report.Add(wrmlReport);
            try
            {
                using (FileStream targetFile = new FileStream(tempFilePath, FileMode.Create, FileAccess.Write))
                    SerializeReport<Schemas.WRML.Reports>(targetFile, wrmlReports);

                using (FileStream sourceFile = new FileStream(tempFilePath, FileMode.Open, FileAccess.Read))
                    DeserializeReport<Schemas.WRML.Reports>(sourceFile, @"http://wats.virinco.com/schemas/WATS/Report", @"C:\Program Files\Virinco\WATS\Schemas\WATS Report.xsd");
            }
            catch (Exception ex)
            {
                throw new ApplicationException("Error validating file", ex);
            }

            try
            {
                File.Delete(tempFilePath);
            }
            catch (Exception)
            {
                //if delete file fails, log it and continue. Its in %temp% anyway
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Warning, 1, $"Error deleting temporary file {tempFilePath}");
            }
        }

        private T DeserializeReport<T>(Stream sourceFile, string schemaNamespace, string schemaUri)
        {
            XmlReaderSettings settings = new XmlReaderSettings();
            settings.ValidationType = ValidationType.Schema;
            settings.ValidationFlags = System.Xml.Schema.XmlSchemaValidationFlags.ReportValidationWarnings;
            settings.Schemas.Add(schemaNamespace, schemaUri);

            using (XmlReader reader = XmlReader.Create(sourceFile, settings))
            {
                XmlSerializer serializer = new XmlSerializer(typeof(T));
                return (T)serializer.Deserialize(reader);
            }
        }

        private void SerializeReport<T>(Stream targetFile, object source)
        {
            XmlSerializer serializer = new XmlSerializer(typeof(T));
            serializer.Serialize(targetFile, source);
        }

        private void ValidateRepairProcess(TDM api, WATSReport wrmlReport)
        {
            //If only code, search all categories and choose first found or make sure there is only one

            RepairType repairtype;
            short repairProcessCode = 0;
            if (wrmlReport.Process.CodeSpecified)
                repairProcessCode = wrmlReport.Process.Code;
            if (repairProcessCode == 0 && converterArguments.ContainsKey("operationTypeCode"))
                repairProcessCode = short.Parse(converterArguments["operationTypeCode"]);
            if (repairProcessCode>0)
            {
                repairtype = api.GetRepairTypes().Where(r => r.Code == repairProcessCode).SingleOrDefault();
                if (repairtype == null)
                    throw new ArgumentException($"Process with code {repairProcessCode} does not exist");
            }
            else if (!string.IsNullOrEmpty(wrmlReport.Process.Name))
            {
                repairtype = api.GetRepairTypes().Where(r => r.Name == wrmlReport.Process.Name).SingleOrDefault();                
                if (repairtype == null)
                    throw new ArgumentException($"Process with name {wrmlReport.Process.Name} does not exist");

                wrmlReport.Process.Code = repairtype.Code;
                wrmlReport.Process.CodeSpecified = true;
            }
            else
                throw new ArgumentException("Neither process code nor process name is defined in report");

            FailCode[] repairCategories = api.GetRootFailCodes(repairtype);

            foreach (Failures_type fail in wrmlReport.Items.OfType<Failures_type>())
            {
                FailCode category;
                if (string.IsNullOrEmpty(fail.Category))
                {
                    if (repairCategories.Length < 1)
                        throw new ArgumentException($"No repair category was found in process {repairtype.Name}");
                    else if (repairCategories.Length > 1)
                        throw new ArgumentException($"Cannot identify repair code without specifying repair category because {repairtype.Name} contains more than one category");
                    else
                    {
                        category = repairCategories.Single();
                        fail.Category = category.Description;
                    }
                }
                else
                {
                    category = repairCategories.Where(c => c.Description == fail.Category).SingleOrDefault();
                    if (category == null)
                        throw new ArgumentException($"Repair category {fail.Category} was not found in process {repairtype.Name}");
                }

                FailCode code = api.GetChildFailCodes(category).Where(c => c.Description == fail.Code).SingleOrDefault();
                if (code == null)
                    throw new ArgumentException($"Repair code {fail.Code} in category {fail.Category} was not found in process {repairtype.Name}");
            }
        }
    }
}
