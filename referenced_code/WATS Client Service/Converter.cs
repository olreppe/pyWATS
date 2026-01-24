using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.IO;
using System.Threading;
using ICSharpCode.SharpZipLib.Zip;

namespace Virinco.WATS.ClientService
{
    class Converter : IDisposable
    {
        private convertersConverter conv;
        private FileSystemWatcher fsw;
        private System.Type converterClass;
        private Dictionary<string, string> sourceparams;
        private Dictionary<string, string> destinationparams;

        private string watchPath;
        private string watchFilter;

        internal List<ConversionItem> pendingitems;

        //private TDMAPIPool apipool = new TDMAPIPool(Interface.TestModeType.TestStand, Interface.TDM.InitializationMode.Syncronous, false, false);
        private Conversion conversion;

        internal ConverterStateEnum ConverterState { private set; get; }
        internal string ConverterStateReason { private set; get; }
        internal Exception LastStateChangeException { private set; get; }

        public enum PostProcessActionEnum { Move, Archive, Error, Delete }
        internal PostProcessActionEnum DefaultPostProcessAction = PostProcessActionEnum.Delete;

        public Converter(convertersConverter conv, Conversion conversion)
        {
            // TODO: Complete member initialization
            this.conv = conv;
            this.conversion = conversion;
            sourceparams = GetParameters(conv.Source);
            destinationparams = GetParameters(conv.Destination);

            // Parse "postprocessaction"
            if (this.sourceparams.ContainsKey("PostProcessAction"))
            {
                if (!Utilities.EnumTryParse<PostProcessActionEnum>(this.sourceparams["PostProcessAction"], out DefaultPostProcessAction))
                {
                    // Process "aliases"
                    switch (this.sourceparams["PostProcessAction"].ToLower())
                    {
                        case "zip": DefaultPostProcessAction = PostProcessActionEnum.Archive; break;
                        case "": DefaultPostProcessAction = PostProcessActionEnum.Delete; break;
                        default:
                            throw new ArgumentException("Invalid PostProcessAction: " + this.sourceparams["PostProcessAction"], "PostProcessAction");
                    }
                }
            }
            else
                DefaultPostProcessAction = PostProcessActionEnum.Delete;

            ConverterState = ConverterStateEnum.Created;
            // Locate specified Convertertype, and ensure that it can cast to IWATSReport
            converterClass = System.Type.GetType(conv.@class, false);
            if (converterClass == null)
            {
                string exeDir = Path.GetDirectoryName(System.Environment.ProcessPath);
                string assemblyPath = Path.Combine(exeDir, conv.assembly) + ".dll";
                System.Reflection.Assembly asm = System.Reflection.Assembly.LoadFrom(assemblyPath);
                if (asm == null) throw new ApplicationException("Specified assembly could not be found: " + conv.assembly);
                else
                {
                    converterClass = asm.GetType(conv.@class, true, true);
                    version = asm.GetName().Version;
                }
            }
            if (!typeof(Interface.IReportConverter).IsAssignableFrom(converterClass)) throw new ApplicationException("Specified assembly does not implement Interface.IReportConverter: " + conv.assembly + ", " + conv.@class);
            // Read config, setup watcher, and queue import-thread (threadpool)
            watchPath = sourceparams["Path"]; // conv.Source.Parameter.First(p => p.name == "Path").Value;
            watchFilter = sourceparams["Filter"]; // conv.Source.Parameter.First(p => p.name == "Filter").Value;
            pendingitems = new List<ConversionItem>();
        }

        private void AttachWatcher(bool LogAsWarning)
        {
            try { fsw = new FileSystemWatcher(watchPath, watchFilter); }
            catch (ArgumentException ex)
            {
                if (LogAsWarning)
                    Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = ex, Message = String.Format("Error attaching file watcher for converter: {0} on path '{1}'\nThe folder will be checked periodically", conv.name, watchPath) });
                else
                    Env.Trace.TraceData(System.Diagnostics.TraceEventType.Information, 0, new WATSLogItem() { ex = ex, Message = String.Format("unable to attach file watcher for converter: {0} on path '{1}'", conv.name, watchPath) });
            }
            if (fsw != null)
            {
                fsw.Changed += new FileSystemEventHandler(fsw_Changed);
                fsw.Renamed += new RenamedEventHandler(fsw_Renamed);
                fsw.EnableRaisingEvents = true;
            }
        }

        internal string Name { get { return conv.name; } }

        public Version version { get; internal set; }

        internal int PendingCount()
        {
            System.IO.DirectoryInfo di = new System.IO.DirectoryInfo(watchPath);
            return di.Exists ? di.GetFiles(watchFilter).Count() : 0;
        }
        internal int ErrorCount()
        {
            System.IO.DirectoryInfo di = new System.IO.DirectoryInfo(watchPath + @"\Error");
            return di.Exists ? di.GetFiles().Count() : 0;
        }

        private Dictionary<string, string> GetParameters(ParametersCollection parametersCollection)
        {
            var dic = new Dictionary<string, string>();
            if (parametersCollection?.Parameter != null)
            {
                foreach (var p in parametersCollection.Parameter)
                    dic.Add(p.name, p.Value);
            }

            return dic;
        }

        void fsw_Renamed(object sender, System.IO.RenamedEventArgs e)
        {
            CheckFolderSingleThread(null);
        }

        void fsw_Changed(object sender, System.IO.FileSystemEventArgs e)
        {
            CheckFolderSingleThread(null);
        }

        public void Start()
        {
            if (ConverterState == ConverterStateEnum.Disposing)
                return;

            try
            {
                var testFilePath = Path.Combine(watchPath, Path.GetRandomFileName());
                File.WriteAllText(testFilePath, "test file");
                File.ReadAllText(testFilePath);
                File.Delete(testFilePath);

                var errorFolderPath = Path.Combine(watchPath, Interface.ConversionSource.ErrorFolder);
                Directory.CreateDirectory(errorFolderPath);

                ConverterState = ConverterStateEnum.Running;
                CheckFolder(); // Runs once, "syncronous" during startup...

                if (fsw == null)
                    AttachWatcher(true);

                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Start(), Converter started", System.Threading.Thread.CurrentThread.ManagedThreadId, this.converterClass.ToString());
            }
            catch
            {
                ConverterState = ConverterStateEnum.FailedToStart;
                throw;
            }
        }

        internal void Stop()
        {
            if (fsw != null) fsw.EnableRaisingEvents = false;
        }


        private object _checkfolderLocker = new object();
        private DateTime _lastCheckRequest;
        /// <summary>
        /// Run "continously" to check for new files. Mutex (Monitor) ensuring only one thread will run CheckFolder.
        /// Pauses 5 seconds between each CheckFolder to avoid unneccessary workload.
        /// This method should be called in a separate thread, to avoid blocking.
        /// </summary>
        public void CheckFolderSingleThread(object sender)
        {
            if (!Monitor.TryEnter(_checkfolderLocker))
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Skipping CheckFolder (already running).");
                return;
            }

            try
            {
                if (ConverterState == ConverterStateEnum.FailedToStart)
                    Start(); //Start also runs CheckFolder
                else
                    CheckFolder();

                Thread.Sleep(5000); // wait 5sec betweeen CheckFolders to avvoid unneccessary workload.
            }
            catch (Exception ex)
            {
                Env.LogException(ex, $"An unhandled exception occurred during CheckFolder for converter {Name}.");
            }
            finally
            {
                Monitor.Exit(_checkfolderLocker); // release locker.
            }
        }

        public void CheckFolder()
        {
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Check(),Checking source folder for new files, ConverterState={2}", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, ConverterState);
            if (ConverterState == ConverterStateEnum.Disposing)
                return;

            // Check for "orphaned" Conversion items (may occur if same filename is beeing written while 
            lock (pendingitems)
            {
                List<ConversionItem> orphanedItems = new List<ConversionItem>();
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Check(),Checking PendingItems, Count={2}", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, pendingitems.Count);
                foreach (ConversionItem ci in pendingitems) if (this.conversion == null || !this.conversion.IsPending(ci)) orphanedItems.Add(ci);
                foreach (ConversionItem ci in orphanedItems)
                {
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Check['{2}'],Removing orphaned Conversion item ", ci.threadId, this.Name, ci.file.Name);
                    pendingitems.Remove(ci);
                }
            }
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Check(),Checking PendingItems 2, Count={2}", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, pendingitems.Count);

            int pendingcount_start = pendingitems.Count;
            if (pendingcount_start >= 10)
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Check(), {2} Files are already registered as pending items, skipping CheckFolder.", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, pendingcount_start);
                return; // Avoid unneccessary filesystem querying (at least 10 items are already registered)
            }

            // Checking folder
            System.IO.DirectoryInfo di = null;
            try
            {
                di = new System.IO.DirectoryInfo(watchPath);
            }
            catch (Exception ex)
            {
                throw new Exception($"Unable to access path '{watchPath}' for converter {Name}. See inner exception.", ex);
            }

            if (di == null || !di.Exists) // Directory does not exist.                
                throw new Exception($"Th[0x{Thread.CurrentThread.ManagedThreadId:X2}],Cnv[{Name}],Check[],Checkfolder failed: Path '{watchPath}' was not accessible.");

            IEnumerable<FileInfo> files;
            try
            {
                files = di.EnumerateFiles(watchFilter);
            }
            catch (Exception ex)
            {
                throw new Exception($"Error trying to enumerate files in the folder '{watchPath}' for converter {Name}", ex);
            }

            IEnumerable<FileInfo> sortedFiles = files.OrderBy(file => file.CreationTime).Take(10000);
            foreach (System.IO.FileInfo fi in sortedFiles)
            {
                if (ConverterState == ConverterStateEnum.Disposing == true) break;  // Stop processing because service is stopping...
                ConversionItem item = conversion.AddFile(fi, this); // Add or get ConversionItem from conversion (all converters combined)
                lock (pendingitems)
                {
                    if (!this.pendingitems.Contains(item)) // Add new ConversionItems to pendingitems collection
                    {
                        this.pendingitems.Add(item);
                    }
                }
            }

            int pendingcount_end = pendingitems.Count;
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Check[],Checkfolder result: pending count: {2}, new files: {3}", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, pendingcount_end, pendingcount_end - pendingcount_start);
        }

        public Interface.IReportConverter GetConverter()
        {
            ConstructorInfo ci = converterClass.GetConstructor(new Type[] { typeof(IDictionary<string, string>) });
            if (ci == null)
                ci = converterClass.GetConstructor(new Type[] { typeof(Dictionary<string, string>) });
            if (ci != null)
                return (Interface.IReportConverter)ci.Invoke(BindingFlags.DeclaredOnly | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.CreateInstance, null, new Object[] { destinationparams }, null);
            else
                return (Interface.IReportConverter)converterClass.InvokeMember(null, BindingFlags.DeclaredOnly | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.CreateInstance, null, null, new Object[] { });
        }
        internal enum InitMode { NoConnect, SyncConnect, AsyncConnect }

        internal void ConvertFile(ConversionItem ci, Virinco.WATS.Interface.TDM api)
        {
            if (ConverterState == ConverterStateEnum.Disposing) return;
            if (ConverterState == ConverterStateEnum.Failed) // Converter is failed, remove from queue.
            {
                lock (pendingitems)
                {
                    conversion.RemoveFile(ci.file.FullName);
                }
                return;
            }
            ci.processstart = DateTime.Now;
            ci.threadId = System.Threading.Thread.CurrentThread.ManagedThreadId;
            lock (pendingitems)
            {
                if (pendingitems.Contains(ci)) pendingitems.Remove(ci);
            }
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Convert['{2}'],Conversion started", ci.threadId, this.Name, ci.file.Name);
            //"Th[0x{0:X2}],Cnv[{1}],ARC|MOV|DEL,'{2}', description", ci.threadId, this.Name, ci.file.Name

            using (System.IO.FileStream fs = GetFileExclusiveLock(ci, TimeSpan.FromSeconds(30)))
            {
                if (fs != null)
                {
                    Interface.IReportConverter conv = GetConverter();
                    //Virinco.WATS.Interface.TDM api = apipool.GetAPI();
                    //string PostProcessAction = this.sourceparams.ContainsKey("PostProcessAction") ? this.sourceparams["PostProcessAction"] : "Delete";
                    PostProcessActionEnum PostProcessAction = this.DefaultPostProcessAction;
                    try
                    {
                        api.SetConversionSource(ci.file, this.sourceparams, this.destinationparams);
                        ci.state = ConversionItemState.Processing;
                        Interface.Report report = conv.ImportReport(api, fs);
                        ci.state = ConversionItemState.PostProcessing;
                        if (!object.ReferenceEquals(report, null)) api.Submit(Interface.SubmitMethod.Automatic, report);
                    }
                    catch (Exception ex)
                    {
                        PostProcessAction = PostProcessActionEnum.Error; // Move to error !
                        Env.LogException(ex, "An error occured during file conversion, see inner exception for details");
                    }
                    api.ClearConversionSource();
                    conv.CleanUp();
                    switch (PostProcessAction)
                    { //move, archive, error, delete
                        case PostProcessActionEnum.Move:
                            try { FileMove(ci.file); conversion.RemoveFile(ci.sourcePath); }
                            catch { System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(MoveFile), ci); }
                            break;
                        case PostProcessActionEnum.Archive:
                            conversion.RemoveFile(ci.sourcePath);
                            System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(ZipAndDeleteFile), ci);
                            break;
                        case PostProcessActionEnum.Error:
                            try { FileError(ci.file); conversion.RemoveFile(ci.sourcePath); }
                            catch { System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(ErrorFile), ci); }
                            break;
                        case PostProcessActionEnum.Delete:
                        default:
                            try { ci.file.Delete(); conversion.RemoveFile(ci.sourcePath); }
                            // Access denied: no need to schedule async delete. The converter will go into failed state.
                            catch (UnauthorizedAccessException uaex) { SetConverterState(ConverterStateEnum.Failed, "Filedeletion failed with UnauthorizedAccessException, entering Failed state.", uaex); }
                            // Any other exception, schedule async deletion...
                            catch { System.Threading.ThreadPool.QueueUserWorkItem(new System.Threading.WaitCallback(DeleteFile), ci); }
                            break;
                    }
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Convert['{2}'],Removed from queue with postprocessaction {3}", ci.threadId, this.Name, ci.file.Name, PostProcessAction);
                }
                else
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Warning, 0, "Th[0x{0:X2}],Cnv[{1}],Convert['{2}'],Unable to get exclusive lock on file , conversion failed.", ci.threadId, this.Name, ci.file.Name);
            }
            // Ok... return (with success)
            // Report success ??
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Convert['{2}'],Conversion complete", ci.threadId, this.Name, ci.file.Name);
            return;
            // try-catch for "unhandled" exceptions removed from ConvertFile - handled in WorkerClass instead!
        }

        private void DeleteFile(object sender)
        {
            Exception lastException = null;
            ConversionItem ci = sender as ConversionItem;
            double msRemaining = 30000;
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Delete['{2}'],Failed to delete sourcefile, trying to delete asyncronously", ci.threadId, this.Name, ci.file.Name);
            while (ci.file != null && ci.file.Exists)
            {
                try { ci.file.Delete(); }
                catch (UnauthorizedAccessException uaex) // No need to retry the delete, access denied. The converter will go into failed state.
                {
                    SetConverterState(ConverterStateEnum.Failed, "Filedeletion failed with UnauthorizedAccessException, entering Failed state.", uaex);
                    break;
                }
                catch (Exception ex)
                {
                    lastException = ex;
                    msRemaining -= 250;
                    if (msRemaining <= 0) break;
                    Thread.Sleep(250);
                }
                ci.file.Refresh();
            }
            if (ci.file != null && !ci.file.Exists) Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Delete['{2}'],Sourcefile deleted after {3}ms", ci.threadId, this.Name, ci.file.Name, 30000 - msRemaining);
            else if (ci.file != null) Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Information, 0, "Th[0x{0:X2}],Cnv[{1}],Delete['{2}'],Failed to delete sourcefile", ci.threadId, this.Name, ci.file.Name);
            else Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Delete['{2}'],Failed to delete file, invalid sourcefile reference", ci.threadId, this.Name, ci.sourcePath);
            if (lastException != null) Env.Trace.TraceData(System.Diagnostics.TraceEventType.Warning, 0, new WATSLogItem() { ex = lastException, Message = String.Format("Th[0x{0:X2}],Cnv[{1}],Delete['{2}'],One or more exceptions was thrown during deletefile", ci.threadId, this.Name, ci.file.Name) });
            try { conversion.RemoveFile(ci.sourcePath); }
            catch { } //WTF?
        }

        private void SetConverterState(ConverterStateEnum newConverterState, string StateChangeReason, Exception e)
        {
            this.ConverterStateReason = StateChangeReason;
            this.LastStateChangeException = e;
            Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = e, Message = String.Format("Th[0x{0:X2}],Cnv[{1}],StateChange, State changed from {2} to {3}. Reason:'{4}' ", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, this.ConverterState, newConverterState, StateChangeReason) });
            this.ConverterState = newConverterState;

        }
        private void MoveFile(object sender)
        {
            ConversionItem ci = sender as ConversionItem;
            double msRemaining = 30000;
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Move['{2}'],Failed to move sourcefile, trying to delete asyncronously", ci.threadId, this.Name, ci.file.Name);
            while (ci.file != null && ci.file.Exists)
            {
                try
                {
                    FileMove(ci.file);
                }
                catch
                {
                    msRemaining -= 250;
                    if (msRemaining <= 0) break;
                    Thread.Sleep(250);
                }
                ci.file.Refresh();
            }
            if (ci.file != null && !ci.file.Exists) Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Move['{2}'],Sourcefile moved after {3}ms", ci.threadId, this.Name, ci.file.Name, 30000 - msRemaining);
            else if (ci.file != null) Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Information, 0, "Th[0x{0:X2}],Cnv[{1}],Move['{2}'],Failed to move sourcefile", ci.threadId, this.Name, ci.file.Name);
            else Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Move['{2}'],Failed to move sourcefile, invalid sourcefile reference", ci.threadId, this.Name, ci.sourcePath);
            try { conversion.RemoveFile(ci.sourcePath); }
            catch { } //WTF?
        }
        private void FileMove(FileInfo source)
        {
            FileInfo destination = new FileInfo(
                Path.Combine(source.DirectoryName,
                String.Format(@"{0}\{1}{2}",
                    Virinco.WATS.Interface.ConversionSource.CompletedFolder,
                    Path.GetFileNameWithoutExtension(source.Name),
                    source.Extension
                )));
            if (destination.Exists)
                destination = new FileInfo(
                Path.Combine(source.DirectoryName,
                String.Format(@"{0}\{1}.{2}{3}",
                    Virinco.WATS.Interface.ConversionSource.CompletedFolder,
                    Path.GetFileNameWithoutExtension(source.Name),
                    Path.GetRandomFileName().Substring(0, 8),
                    source.Extension
                )));
            if (!destination.Directory.Exists) destination.Directory.Create();
            source.MoveTo(destination.FullName);
        }

        private Queue<ConversionItem> archive_queue = new Queue<ConversionItem>();
        private void ZipAndDeleteFile(object sender)
        {
            ConversionItem ci = sender as ConversionItem;
            FileMove(ci.file); // "temporarily" move into Done-folder
            archive_queue.Enqueue(ci); // Add to arhive-item-queue... Archiving will trigger when the last WP is going idle...

            if (archive_queue.Count > 50) ProcessArchiveQueue(null);
        }

        private static Object zipfilemutex = new object();
        public void ProcessArchiveQueue(object sender)
        {
            if (archive_queue.Count == 0)
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}], Nothing to archive; exiting", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name);
                return;
            }
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Starting process archive queue", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name);
            // Create or open archive
            if (Monitor.TryEnter(zipfilemutex))
            {
                string archiveFilePath = Path.Combine(this.watchPath,
                   string.Format(@"{0}\{1:yyyyMM}.zip",
                   Virinco.WATS.Interface.ConversionSource.CompletedFolder,
                   DateTime.Now
                   ));
                if (!Directory.Exists(Path.GetDirectoryName(archiveFilePath))) Directory.CreateDirectory(Path.GetDirectoryName(archiveFilePath));
                try
                {
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Archive locked", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name);
                    ZipFile zf =
                        System.IO.File.Exists(archiveFilePath) ?
                        new ZipFile(archiveFilePath) :
                        ZipFile.Create(archiveFilePath);
                    int files_archived = 0;

                    //Make entrynames use unicode (OEMCodePage is invalid in some cultures)
                    ((ZipEntryFactory)zf.EntryFactory).IsUnicodeText = true;

                    int maxFilesPerCommit = 10;

                    while (archive_queue.Count > 0)
                    {
                        // Get maxFilesPerCommit items from archive-queue:
                        try
                        {
                            var items = new List<ConversionItem>();
                            while (items.Count < maxFilesPerCommit && archive_queue.Count > 0)
                            {
                                var item = archive_queue.Dequeue();
                                if (item.file.Exists) // skip item if file does not exist
                                    items.Add(item);
                            }
                            //ConversionItem ci = archive_queue.Dequeue();
                            zf.BeginUpdate();
                            zf.SetComment(null); //Set comment to null will skip encoding it to bytes (default is string.Empty). The default code page (OEMCodePage) is invalid in some cultures.
                            foreach (var ci in items)
                            {
                                string fileNameInArchive = ci.file.Name;
                                if (zf.FindEntry(fileNameInArchive, true) >= 0)
                                {
                                    // File already exists in archive, append random filename
                                    fileNameInArchive = String.Format(@"{0}.{1}{2}",
                                       Path.GetFileNameWithoutExtension(ci.file.Name),
                                       Path.GetRandomFileName().Substring(0, 8),
                                       ci.file.Extension);
                                }
                                // Append File and Update...
                                zf.Add(ci.file.FullName, fileNameInArchive);
                                files_archived++;
                                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Archive['{2}'],File['{3}'], File added to archive", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, Path.GetFileName(archiveFilePath), ci.file.Name);
                            }
                            zf.CommitUpdate();
                            try
                            {
                                foreach (var ci in items) ci.file.Delete();
                            }
                            catch { } // Don't care if delete fails???

                        }
                        catch (Exception ex)
                        {
                            Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("Th[0x{0:X2}],Cnv[{1}],Archive['{2}'], FAILED to update archive", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, Path.GetFileName(archiveFilePath)) });
                            // ZipFile not updated, reschedule ???
                        }
                        //conversion.RemoveFile(ci.sourcePath);
                    }
                    zf.Close();
                    Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Archive['{2}'], Archived {3} files", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, Path.GetFileName(archiveFilePath), files_archived);
                }
                catch (Exception ex)
                {
                    Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = String.Format("Th[0x{0:X2}],Cnv[{1}],Archive['{2}'], FAILED to add file to archive", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name, Path.GetFileName(archiveFilePath)) });
                }
                finally { Monitor.Exit(zipfilemutex); }
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Archive mutex released", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name);
            }
            else // timeout waiting for mutex
            {
                Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Archive queue is already being processed by another workerthread", System.Threading.Thread.CurrentThread.ManagedThreadId, this.Name);
            }
        }

        private void ErrorFile(object sender)
        {
            ConversionItem ci = sender as ConversionItem;
            //string sourceFullName = fileInfo.FullName;
            double msRemaining = 30000;
            Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Error['{2}'],Failed to move faulty sourcefile, trying to move asyncronously", ci.threadId, this.Name, ci.file.Name);
            Exception lastException = null;
            int ExceptionCount = 0;
            while (ci.file != null && ci.file.Exists)
            {
                try
                {
                    FileError(ci.file);
                }
                catch (Exception ex)
                {
                    lastException = ex;
                    ExceptionCount++;
                    msRemaining -= 250;
                    if (msRemaining <= 0) break;
                    Thread.Sleep(250);
                }
                ci.file.Refresh();
            }

            if (ci.file != null && !ci.file.Exists)
            {
                if (lastException != null) Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Warning, 0, "Th[0x{0:X2}],Cnv[{1}],Error['{2}'], {3} Exceptions was captured before sourcefile was succesfully moved to Error folder. The last exception was '{4}'", ci.threadId, this.Name, ci.file.Name, ExceptionCount, lastException.Message);
                else Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Error['{2}'],Faulty Sourcefile moved to Error folder", ci.threadId, this.Name, ci.file.Name, 30000 - msRemaining);
            }
            else if (ci.file != null) Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Information, 0, "Th[0x{0:X2}],Cnv[{1}],Error['{2}'],Failed to move faulty sourcefile", ci.threadId, this.Name, ci.file.Name);
            else Env.Trace.TraceEvent(System.Diagnostics.TraceEventType.Verbose, 0, "Th[0x{0:X2}],Cnv[{1}],Error['{2}']: Failed to move faulty sourcefile, invalid sourcefile reference", ci.threadId, this.Name, ci.sourcePath);
            try { conversion.RemoveFile(ci.sourcePath); }
            catch { } //WTF?
            if (lastException != null) Env.LogException(lastException, "Exception caught during archiving conversion sourcefile");
        }
        private void FileError(FileInfo source)
        {
            FileInfo destination = new FileInfo(
                Path.Combine(source.DirectoryName,
                String.Format(@"{0}\{1}{2}",
                    Virinco.WATS.Interface.ConversionSource.ErrorFolder,
                    Path.GetFileNameWithoutExtension(source.Name),
                    source.Extension
                )));
            if (destination.Exists)
                destination = new FileInfo(
                Path.Combine(source.DirectoryName,
                String.Format(@"{0}\{1}.{2}{3}",
                    Virinco.WATS.Interface.ConversionSource.ErrorFolder,
                    Path.GetFileNameWithoutExtension(source.Name),
                    Path.GetRandomFileName().Substring(0, 8),
                    source.Extension
                )));
            if (!destination.Directory.Exists) destination.Directory.Create();
            source.MoveTo(destination.FullName);
        }


        private FileStream GetFileExclusiveLock(ConversionItem ci, TimeSpan timeout)
        {
            double msRemaining = timeout.TotalMilliseconds;
            FileStream fs = null;
            while (fs == null)
            {
                ci.lockiteration++;
                if (ConverterState == ConverterStateEnum.Disposing) break;
                try { fs = new FileStream(ci.file.FullName, FileMode.Open, FileAccess.Read, FileShare.Delete | FileShare.Read); }
                catch
                {
                    msRemaining -= 250;
                    if (msRemaining <= 0) break;
                    Thread.Sleep(250);
                }
            }
            return fs;
        }

        internal void CheckState(object state)
        {
            if (ConverterState == ConverterStateEnum.Disposing)
                return;

            //Retry "attach" filesystem watcher on folder...
            if (fsw == null)
                AttachWatcher(false);

            CheckFolderSingleThread(null);
        }

        public void Dispose()
        {
            ConverterState = ConverterStateEnum.Disposing;
            if (fsw != null)
            {
                fsw.EnableRaisingEvents = false;
                fsw.Dispose();
                fsw = null;
            }
        }
    }
}
