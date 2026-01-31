using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using Newtonsoft.Json;

namespace Virinco.WATS.Interface
{
    internal class Processes
    {
        private TDM _api;
        private Dictionary<short, Models.Process> _processes;

        internal const string processesFilename = "Processes.json";
        //internal const string processesLegacyXmlFilename = "Codes_TDM-Default.xml";
        private const string cApiGetProcesses = "api/internal/Process/GetProcesses";
        internal Processes(TDM api)
        {
            _api = api;
        }

        internal Dictionary<short, Models.Process> processes { get { return _processes; } }
        /// <summary>
        /// Load from local cache
        /// </summary>
        internal void Load()
        {
            using (var txtreader = new StreamReader(Path.Combine(_api.DataDir, processesFilename)))
            {
                var reader = new Newtonsoft.Json.JsonTextReader(txtreader);
                var serializer = new Newtonsoft.Json.JsonSerializer();
                _processes = serializer.Deserialize<Models.Process[]>(reader).ToDictionary(p => p.Code);
            }
        }

        internal bool CanLoad()
        {
            return File.Exists(Path.Combine(_api.DataDir, processesFilename));
        }

        /// <summary>
        /// Save to local cache
        /// </summary>
        internal void Save()
        {
            using (var txtwriter = new StreamWriter(Path.Combine(_api.DataDir, processesFilename)))
            {
                var writer = new Newtonsoft.Json.JsonTextWriter(txtwriter);
                var serializer = new Newtonsoft.Json.JsonSerializer();
                serializer.Serialize(writer, _processes.Values);
            }
            /*using (var txtwriter = new StreamWriter(Path.Combine(_api.DataDir, processesLegacyXmlFilename)))
            {
                string ns = "http://wats.virinco.local/Codes.xsd";
                var writer = System.Xml.XmlWriter.Create(txtwriter);
                writer.WriteStartElement("Codes", ns);
                foreach (var ot in _processes.Values.Where(p => p.IsTestOperation))
                {
                    writer.WriteStartElement("OPERATIONTYPES", ns);
                    writer.WriteElementString("GUID", ns, ot.ProcessID.ToString());
                    writer.WriteElementString("Category", ns, "0");
                    writer.WriteElementString("Code", ns, ot.Code.ToString());
                    writer.WriteElementString("Name", ns, ot.Name);
                    writer.WriteElementString("Description", ns, ot.Description);
                    writer.WriteElementString("State", ns, ot.State.ToString());
                    writer.WriteEndElement();
                }
                foreach (var p in _processes.Values)
                {
                    writer.WriteStartElement("Process", ns);
                    writer.WriteElementString("GUID", ns, p.ProcessID.ToString());
                    writer.WriteElementString("Code", ns, p.Code.ToString());
                    writer.WriteElementString("Name", ns, p.Name);
                    writer.WriteElementString("Description", ns, p.Description);
                    writer.WriteElementString("State", ns, p.State.ToString());
                    writer.WriteElementString("ProcessIndex", ns, p.ProcessIndex.ToString());
                    if (p.Properties != null)
                        writer.WriteElementString("IsTestOperation", ns, p.IsTestOperation.ToString());
                    writer.WriteElementString("IsWIPOperation", ns, p.IsWIPOperation.ToString());
                    writer.WriteElementString("IsRepairOperation", ns, p.IsRepairOperation.ToString());
                    writer.WriteEndElement();

                }
                writer.WriteEndElement();
            }*/

        }

        /// <summary>
        /// Load from server
        /// </summary>
        internal void Get(bool save = true)
        {
            using (var res = _api.proxy.GetJsonStream(cApiGetProcesses))
            using (var tReader = new StreamReader(res))
            {
                JsonReader jReader = new JsonTextReader(tReader);
                var conv = JsonSerializer.Create();
                var procs = conv.Deserialize(jReader) as Newtonsoft.Json.Linq.JArray;
                var filteredprocs =
                procs.Select(p => new { c16 = p.Value<Int16?>("Code"), p })
                    .Where(p => p.c16.HasValue);
                _processes = filteredprocs.Select(p => new Models.Process()
                {
                    Code = p.c16.Value,
                    ProcessID = new Guid(p.p.Value<string>("ProcessID")),
                    Name = p.p.Value<string>("Name"),
                    Description = p.p.Value<string>("Description"),
                    ProcessIndex = p.p.Value<int>("ProcessIndex"),
                    State = (Models.ProcessRecordState)p.p.Value<int>("State"),
                    IsRepairOperation = p.p.Value<bool>("IsRepairOperation"),
                    IsTestOperation = p.p.Value<bool>("IsTestOperation"),
                    IsWIPOperation = p.p.Value<bool>("IsWIPOperation"),
                    Properties = Models.RepairType.Parse(p.p.Value<string>("Properties")),
                }).Where(p => p.State==Models.ProcessRecordState.Active).ToDictionary(p => p.Code);
            }
            // persist to disk (unless explicitly set save to false)
            if (save) Save();
        }
    }
}
