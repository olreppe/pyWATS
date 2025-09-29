using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;

namespace Virinco.WATS
{
    internal class WATSDatabaseTraceListener : System.Diagnostics.TraceListener //System.Diagnostics.TextWriterTraceListener
    {
        private string cnstring;
        private const int ConnectTimeout = 2;
        internal WATSDatabaseTraceListener(string DatabaseConnectionString)
            : base()
        {
            SqlConnectionStringBuilder sbuilder = new SqlConnectionStringBuilder(DatabaseConnectionString) { ConnectTimeout = WATSDatabaseTraceListener.ConnectTimeout };
            cnstring = sbuilder.ToString();
        }
        internal static WATSDatabaseTraceListener Create()
        {
            // Lookup WATS connection string in applicationconfiguration
            return (!object.ReferenceEquals(ConfigurationManager.ConnectionStrings["WATS"], null)) ?
                new WATSDatabaseTraceListener(ConfigurationManager.ConnectionStrings["WATS"].ConnectionString) :
                null;
        }
        internal static WATSDatabaseTraceListener Create(EventTypeFilter eventTypeFilter)
        {
            // Lookup WATS connection string in applicationconfiguration
            return (!object.ReferenceEquals(ConfigurationManager.ConnectionStrings["WATS"], null)) ?
                new WATSDatabaseTraceListener(ConfigurationManager.ConnectionStrings["WATS"].ConnectionString) { Filter = eventTypeFilter } :
                null;
        }

        public override void TraceData(TraceEventCache eventCache, string source, TraceEventType eventType, int id, object data)
        {
            WATSLogMessage msg;
            if (data is WATSLogItem) msg = ((WATSLogItem)data).GetLogMessage();
            else if (data is WATSLogMessage) msg = (WATSLogMessage)data;
            else
                msg = new WATSLogMessage(Logging.LogSeverity.INFORMATION, Logging.LogCategory.Unknown, "") { description = String.Format("{0}", data) };
            //if (!string.IsNullOrEmpty(category)) msg.group=category;
            using (SqlConnection cn = new SqlConnection(cnstring))
                AppendLog(cn, msg);
        }

        public override void Write(object o, string category)
        {
            WATSLogMessage msg;
            if (o is WATSLogItem) msg = ((WATSLogItem)o).GetLogMessage();
            else if (o is WATSLogMessage) msg = (WATSLogMessage)o;
            else
                msg = new WATSLogMessage(Logging.LogSeverity.INFORMATION, Logging.LogCategory.Unknown, "") { description = String.Format("{0}", o) };
            if (!string.IsNullOrEmpty(category)) msg.group = category;
            using (SqlConnection cn = new SqlConnection(cnstring))
                AppendLog(cn, msg);
        }


        public override void Write(string message, string category)
        {
            using (SqlConnection cn = new SqlConnection(cnstring))
                AppendLog(cn, new WATSLogMessage(Logging.LogSeverity.INFORMATION, Logging.LogCategory.Unknown, category) { description = message });
        }
        public override void Write(object o)
        {
            this.Write(o, string.Empty);
        }
        public override void Write(string message)
        {
            this.Write(message, string.Empty);
        }
        public override void WriteLine(object o)
        {
            this.Write(o, string.Empty);
        }
        public override void WriteLine(object o, string category)
        {
            this.Write(o, category);
        }
        public override void WriteLine(string message)
        {
            this.Write(message, string.Empty);
        }
        public override void WriteLine(string message, string category)
        {
            this.Write(message, category);
        }

        private static void AppendLog(SqlConnection cn, Virinco.WATS.WATSLogMessage message)
        {
            bool dblogged = false;
            try
            {
                if (cn != null)
                {
                    if (cn.State == ConnectionState.Broken) cn.Close();
                    if (cn.State == ConnectionState.Closed) cn.Open();
                    using (SqlCommand cmd = new SqlCommand("wats.AddLog", cn))
                    {
                        cmd.CommandType = CommandType.StoredProcedure;
                        cmd.Parameters.AddWithValue("@category", message.category);
                        cmd.Parameters.AddWithValue("@severity", message.severity);
                        cmd.Parameters.AddWithValue("@group", message.group);
                        cmd.Parameters.AddWithValue("@item_type", message.item_type);
                        cmd.Parameters.AddWithValue("@item_guid", message.item_guid);
                        cmd.Parameters.AddWithValue("@item_lcid", message.item_lcid);
                        cmd.Parameters.AddWithValue("@total_time", message.total_time_sec);
                        cmd.Parameters.AddWithValue("@module_time", message.module_time_sec);
                        cmd.Parameters.AddWithValue("@external_time", message.external_time_sec);
                        cmd.Parameters.AddWithValue("@Source", message.source);
                        cmd.Parameters.AddWithValue("@Destination", message.destination);
                        cmd.Parameters.AddWithValue("@description", message.description);
                        cmd.Parameters.AddWithValue("@exception_details", message.GetExceptionDetails());
                        cmd.Parameters.AddWithValue("@comment", message.comment);
                        cmd.ExecuteNonQuery();
                    }
                    dblogged = true;
                }
            }
            catch
            {
                dblogged = false;
            }
            if (!dblogged || message.severity < Virinco.WATS.Logging.LogSeverity.ALERT) WriteToEventLog(message);
        }
        private static void WriteToEventLog(Virinco.WATS.WATSLogMessage message)
        {
            System.Text.StringBuilder sb = new System.Text.StringBuilder();
            using (System.IO.StringWriter swr = new System.IO.StringWriter(sb))
            {
                message.WriteToTextStream(swr);
                swr.Close();
            }
            System.Diagnostics.EventLog.WriteEntry("WATS", sb.ToString(), System.Diagnostics.EventLogEntryType.Error, (int)message.category);
        }
    }
}
