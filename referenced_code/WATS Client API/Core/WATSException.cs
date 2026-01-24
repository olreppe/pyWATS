using System;
using System.Xml;
using System.IO;
using System.Runtime.Versioning;

namespace Virinco.WATS
{
    /// <summary>
    /// Summary description for WATSException.
    /// </summary>
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    public class WATSException : Exception
    {
        public WATSException(string Message, Exception InnerException)
            : base(Message, InnerException)
        {
            _itemguid = Guid.Empty;
            _itemtype = 0; // Unknown
            _message = null;
        }
        public WATSException(string Message, Guid ItemGuid, Exception InnerException)
            : base(Message, InnerException)
        {
            _itemguid = ItemGuid;
            _itemtype = 0; // Unknown
            _message = null;
        }
        public WATSException(string Message, int ItemType, Guid ItemGuid, Exception InnerException)
            : base(Message, InnerException)
        {
            _itemguid = ItemGuid;
            _itemtype = ItemType;
            _message = null;
        }
        public WATSException(WATSLogMessage message)
            : base(message.description, message.exception)
        {
            _itemguid = message.item_guid.HasValue ? message.item_guid.Value : Guid.Empty;
            _itemtype = message.item_type.HasValue ? message.item_type.Value : 0;
            _message = message;
        }
        private Guid _itemguid;
        public Guid ItemGuid { get { return _itemguid; } }
        private int _itemtype;
        public int ItemType { get { return _itemtype; } }
        private WATSLogMessage _message;
        public WATSLogMessage LogMessage { get { return _message; } }

        public static void ExceptionWriteText(Exception ex, System.IO.TextWriter writer, string indent="")
        {
            var cnv = new Newtonsoft.Json.JsonSerializer();
            cnv.Serialize(writer, ex);
        }
    }
    public class WATSLogMessage
    {
        public WATSLogMessage(Virinco.WATS.Logging.LogSeverity severity, Virinco.WATS.Logging.LogCategory category, string group)
        {
            this.severity = severity;
            this.category = category;
            this.group = group;
        }
        public int? log_id;

        public WATSException exception;
        public string exception_string;

        public Logging.LogCategory category;
        public Logging.LogSeverity severity;
        //public DateTime? log_date;
        public string group;

        /* Reporting-item identification */
        public int? item_type;
        public Guid? item_guid;
        public int? item_lcid;

        /* Reporting-item timespan */
        public TimeSpan? total_time;
        public TimeSpan? module_time;
        public TimeSpan? external_time;
        public Single? total_time_sec
        {
            get { if (total_time.HasValue) return System.Convert.ToSingle(total_time.Value.TotalSeconds); else return null; }
        }
        public Single? module_time_sec
        {
            get { if (module_time.HasValue) return System.Convert.ToSingle(module_time.Value.TotalSeconds); else return null; }
        }
        public Single? external_time_sec
        {
            get { if (external_time.HasValue) return System.Convert.ToSingle(external_time.Value.TotalSeconds); else return null; }
        }

        /* Source & Destination */
        public Guid? source;
        public Guid? destination;

        /* Description and details */
        public string description;
        public string GetExceptionDetails()
        {
            if (exception_string!=null && exception_string != String.Empty) return exception_string;
            if (exception == null) return null;
            else
            {
                System.IO.StringWriter sw = new System.IO.StringWriter();
                WATSException.ExceptionWriteText(exception, sw);
                return sw.ToString();
            }
        }
        public string comment;
        public void WriteToTextStream(System.IO.TextWriter writer)
        {
            string nl="\r\n\t";
            writer.WriteLine("ErrorLog {{{0}Category=\"{1}\";{0}Group=\"{2}\";{0}Severity=\"{3}\";{0}Description=\"{4}\";\r\n",
                nl, this.category, this.group, this.severity, this.description);

            if (this.item_type.HasValue) writer.WriteLine("\tItemType=\"{0}\";", this.item_type.Value);
            if (this.item_guid.HasValue) writer.WriteLine("\tItemId=\"{0}\";", this.item_guid.Value);
            if (this.item_lcid.HasValue) writer.WriteLine("\tItemLcid=\"{0}\";", this.item_lcid.Value);

            if (this.total_time.HasValue) writer.WriteLine("\tTotaltime=\"{0}\";", this.total_time.Value);
            if (this.module_time.HasValue) writer.WriteLine("\tModuletime=\"{0}\";", this.module_time.Value);
            if (this.external_time.HasValue) writer.WriteLine("\tExternaltime=\"{0}\";", this.external_time.Value);

            if (this.source.HasValue) writer.WriteLine("\tSourceId=\"{0}\";", this.source.Value);
            if (this.destination.HasValue) writer.WriteLine("\tDestinationId=\"{0}\";", this.destination.Value);
            if (this.comment != null) writer.WriteLine("\tComment=\"{0}\";", this.comment);
            if (this.exception != null) WATSException.ExceptionWriteText(this.exception, writer);
        }
        public static WATSLogMessage Create(Exception ex, Logging.LogSeverity severity, Logging.LogCategory category, string description = "", string group = "", string comment = "")
        {
            return new WATSLogMessage(severity, category, group)
            {
                comment = comment,
                description = description,
                exception = (ex is WATSException) ? (WATSException)ex : new WATSException(description, ex)
            };
        }

        public static WATSLogMessage LogException(Exception ex, Virinco.WATS.Logging.LogSeverity severity, Virinco.WATS.Logging.LogCategory category, string description = "", string group = "", string comment = "")
        {
            if (string.IsNullOrEmpty(description) && ex!=null) description = ex.Message;
            WATSLogMessage err = Create(ex, severity, category, description, group, comment);
            Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, err);
            //Virinco.WATS.Data.Common.AppendLog(err);
            return err;
        }
        public override string ToString()
        {
            StringWriter sw = new StringWriter();
            WriteToTextStream(sw);
            return sw.ToString();
        }

    }
    /// <summary>
    /// This struct is deprecated, use WATSLogMessage directly instead. support for this struct will be removed in a future release!
    /// All WATS trace listeners must provide support for WATSLogMessage.
    /// </summary>
    public struct WATSLogItem
    {
        //public System.Diagnostics.TraceEventType eventType;
        public string Message;
        public WATSLogMessage logMessage;
        public Exception ex;

        internal void WriteToStream(TextWriter sw)
        {
            if (!string.IsNullOrEmpty(Message)) sw.WriteLine("Message=\"{0}\";", Message);
            if (!object.ReferenceEquals(logMessage, null)) logMessage.WriteToTextStream(sw);
            if (!object.ReferenceEquals(ex, null)) {
                var cnv = new Newtonsoft.Json.JsonSerializer();
                cnv.Serialize(sw, ex);
            }
        }
        public override string ToString()
        {
            StringWriter sw = new StringWriter();
            WriteToStream(sw);
            return sw.ToString();
        }

        public WATSLogMessage GetLogMessage()
        {
            if (logMessage != null) return logMessage;
            else
                return new WATSLogMessage(Logging.LogSeverity.INFORMATION, Logging.LogCategory.Unknown, "") { description = Message, exception = GetWATSException() };
        }

        private WATSException GetWATSException()
        {
            if (ex is WATSException) return (WATSException)ex;
            else return new WATSException(Message, ex);
        }
    }
}
