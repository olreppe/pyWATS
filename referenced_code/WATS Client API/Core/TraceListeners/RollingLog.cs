using System;
using System.Collections.Generic;
using System.Text;
using System.Diagnostics;
using System.IO;
using System.Runtime.Versioning;
//using Virinco.WATS.ServerConfig.Helpers;

namespace Virinco.WATS
{
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    internal class RollingTextWriterTraceListener : System.Diagnostics.TraceListener //System.Diagnostics.TextWriterTraceListener
    {
        private TextLogWriter logFile;
        /// <summary>
        /// 512KB
        /// </summary>
        internal int maxSize = 524288; /* if logfile size > maxSize --> truncate to minSize */
        /// <summary>
        /// 384KB
        /// </summary>
        internal int minSize = 393216;
        internal object truncateLocker = new object();
        internal RollingTextWriterTraceListener(string FileName)
            : base()
        {
            logFile = new TextLogWriter(new FileInfo(FileName), maxSize, minSize);
            logFile.Initialize();
            System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(Truncate));
        }

        public override void Write(object o)
        {
            this.Write(o, string.Empty);
        }
        public override void Write(object o, string category)
        {
            lock (logFile)
            {
                using (StreamWriter sw = logFile.getStream())
                {
                    if (sw != null)
                    {
                        if (o is Exception)
                        {
                            sw.WriteLine($"{DateTime.Now:o};{category}");
                            sw.WriteLine(Newtonsoft.Json.JsonConvert.SerializeObject(o, Newtonsoft.Json.Formatting.Indented));
                        }
                        else if (o is WATSLogItem) ((WATSLogItem)o).WriteToStream(sw);
                        else if (o is WATSLogMessage) ((WATSLogMessage)o).WriteToTextStream(sw);
                        else sw.Write("{0:o};{1};{2}", DateTime.Now, category, o);
                    }
                }
            }
            //this.WriteLine(o, category);
        }
        public override void Write(string message)
        {
            this.Write(message, string.Empty);
        }
        public override void Write(string message, string category)
        {
            lock (logFile)
                using (StreamWriter sw = logFile.getStream())                
                    sw?.Write("{0:o};{1};{2}", DateTime.Now, category, message);                
        }
        public override void WriteLine(object o)
        {
            this.WriteLine(o, string.Empty);
        }
        public override void WriteLine(object o, string category)
        {
            //WATSLogMessage lm = o as WATSLogMessage;
            lock (logFile)
            {
                using (StreamWriter sw = logFile.getStream())
                {
                    if(sw != null)
                    {
                        if (o is WATSLogItem) ((WATSLogItem)o).WriteToStream(sw);
                        else if (o is WATSLogMessage) ((WATSLogMessage)o).WriteToTextStream(sw);
                        else sw.WriteLine("{0:o};{1};{2}", DateTime.Now, category, o);
                    }
                }
            }
            System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(Truncate));
        }
        public override void WriteLine(string message)
        {
            this.WriteLine(message, string.Empty);
        }
        public override void WriteLine(string message, string category)
        {
            lock (logFile)
            {
                using (StreamWriter sw = logFile.getStream())
                {
                    if (sw != null)
                        sw.WriteLine("{0:o};{1};{2}", DateTime.Now, category, message);
                }
            }
            System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(Truncate));
        }
        private void Truncate(object sender)
        {
            if (!System.Threading.Monitor.TryEnter(truncateLocker)) return;
            try { logFile.Truncate(); }
            finally { System.Threading.Monitor.Exit(truncateLocker); }
        }
    }

#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    internal class TextLogWriter
    {
        internal TextLogWriter(FileInfo logFile, int maxSize, int minSize) { this.logFile = logFile; this.originalLogFile = logFile; this.maxFileSize = maxSize; this.truncateToSize = minSize; }
        private FileInfo logFile;
        private FileInfo originalLogFile;
        private int maxFileSize;
        private int truncateToSize;

        internal void Initialize()
        {
            Truncate(true);
            using (StreamWriter sw = this.getStream())
            {
                sw?.WriteLine("{0:o};INFO;Tracelistener started for {1}", DateTime.Now, System.Reflection.Assembly.GetEntryAssembly()?.FullName);
            }
        }

        internal StreamWriter getStream()
        {
            return getStream(10, 20, 50);
        }
        /// <summary>
        /// Get logfile stream (exclusively locked).
        /// May wait up to retries * ( minWait+ (retries / 2 * waitLoopfactor) ) ms
        /// </summary>
        /// <param name="Retries"></param>
        /// <param name="minWait"></param>
        /// <param name="waitLoopFactor"></param>
        /// <returns>Exclusively locked logfile stream</returns>
        internal StreamWriter getStream(int Retries, int minWait, int waitLoopFactor)
        {
            var writeHeader = true;
            StreamWriter sw = null;
            for (int i = 0; ; i++)
            {
                try
                {
                    writeHeader = !File.Exists(logFile.FullName);
                    sw = new StreamWriter(logFile.Open(FileMode.Append, FileAccess.Write, FileShare.None));
                    break;
                }
                catch (Exception ex)
                {
                    if (i > Retries)
                    {
                        // DO NOT Create new logfile! Just log to eventlog and return null!
                        System.Diagnostics.EventLog.WriteEntry("WATS", String.Format("Error writing to WATS Log File: {0}", ex.Message), EventLogEntryType.Error);
                        return null;

                    }
                    System.Threading.Thread.Sleep(minWait + (i * waitLoopFactor));
                }
            }
            if (sw != null && writeHeader)
            {
                WriteHeader(sw, CreateHeader());
                sw.WriteLine("{0:o};INFO;WATS logfile Created", DateTime.Now);
            }
            return sw;

        }

        public bool FileExists { get { return File.Exists(logFile.FullName); } }

        internal void Truncate(bool justUpdateHeader=false)
        {
            for (int i = 0; ; i++)
            {
                try
                {
                    logFile.Refresh();
                    if (!logFile.Exists) return; // Incase of manual deletion
                    long beginPos = 0;
                    if (justUpdateHeader)
                        beginPos = logFile.Length;
                    else
                        if (logFile.Length < maxFileSize) return; // Not yet...
                    else
                        beginPos = logFile.Length - truncateToSize;
                    if (beginPos <= 0 || beginPos > logFile.Length) return; // something is wrong with the parameteres....
                    // Ok, lets do this.... truncate from beginning...
                    using (FileStream fs = logFile.Open(FileMode.Open, FileAccess.ReadWrite, FileShare.None))
                    {
                        // Load Header:
                        StreamReader srd = new StreamReader(fs);
                        if (justUpdateHeader)
                            beginPos=ReadToEndHeader(srd);
                        fs.Seek(beginPos, SeekOrigin.Begin);
                        srd.ReadLine(); // Just make sure we begin on a new line...
                        string newcontents = srd.ReadToEnd();
                        fs.Seek(0, SeekOrigin.Begin);
                        StreamWriter swr = new StreamWriter(fs);
                        WriteHeader(swr, CreateHeader());
                        swr.Write(newcontents);
                        swr.Flush();
                        fs.SetLength(fs.Position);
                        swr.Dispose();
                        srd.Dispose();
                    }
                    return;
                }
                catch
                {
                    if (i > 120) return;
                    System.Threading.Thread.Sleep(5000); /* Sleep 5sec, then try again... Max. 120x --> 600s(10min) */
                }
            }
        }


        private static Dictionary<string, string> CreateHeader()
        {
            var hdr = new Dictionary<string, string>();
            var asm = System.Reflection.Assembly.GetExecutingAssembly();
            var version = asm?.GetName()?.Version != null ? Utilities.GetMSIVersionString(asm.GetName().Version) : null;
            hdr["created"] = DateTimeOffset.Now.ToString();
            hdr["machinename"] = Env.StationName;
            hdr["watsversion"] = version;
            hdr["osver"] = Environment.OSVersion.ToString();
            hdr["lictype"] = Env.ClientLicense.ToString();
            hdr["identifier"] = REST.ServiceProxy.GetCurrentMACAddress();
            try
            {
                var pxy = new REST.ServiceProxy();
                pxy.LoadSettings();
                hdr["serverurl"] = pxy.TargetURL;
            }
            catch { }
            return hdr;
        }
        private static string hdrBegin = "%BeginHeader:WatsLogFile%";
        private static string hdrEnd = "%EndHeader:WatsLogFile%";
        private static void WriteHeader(StreamWriter sw, Dictionary<string, string> info)
        {
            sw.WriteLine(hdrBegin);
            sw.WriteLine(Newtonsoft.Json.JsonConvert.SerializeObject(info, Newtonsoft.Json.Formatting.Indented));
            sw.WriteLine(hdrEnd);
        }
        private long ReadToEndHeader(StreamReader srd)
        {
            while (!srd.EndOfStream)
            {
                var line = srd.ReadLine();
                if (line == hdrEnd)
                    return srd.BaseStream.Position;
            }
            return srd.BaseStream.Position;
        }
    }
}
