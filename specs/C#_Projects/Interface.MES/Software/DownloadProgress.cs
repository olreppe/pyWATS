using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using Virinco.WATS.Service.MES.Contract;
using System.IO;
using System.Text.RegularExpressions;
using System.Net;
using System.Xml.Linq;

namespace Virinco.WATS.Interface.MES.Software
{
    internal partial class DownloadProgress : Form
    {
        Software software;
        List<Package> packages;
        bool DisplayProgress = false;
        bool Finished = false;
        bool Showing = false;
        BackgroundWorker backgroundWorker;

        public List<FileInfo> ExecuteFiles { get; internal set; }
        public List<FileInfo> TopLevelSequences { get; internal set; }
        //public Dictionary<FileInfo, int> OverwriteOnNewVersionFiles { get; internal set; }

        private DownloadProgress()
        {
            InitializeComponent();
            progressBar1.Value = 0;
            progressBar1.Maximum = 100;
            backgroundWorker = new BackgroundWorker();
            backgroundWorker.WorkerReportsProgress = false;
            backgroundWorker.DoWork += new DoWorkEventHandler(bgWorker_DoWork);
            backgroundWorker.RunWorkerCompleted += new RunWorkerCompletedEventHandler(bgWorker_RunWorkerCompleted);
        }

        public DownloadProgress(Software software, List<Package> packages, bool DisplayProgress)
            : this()
        {
            this.software = software;

            this.packages = packages;
            this.DisplayProgress = DisplayProgress;

            this.Text = "WATS - " + software.TranslateString("Getting Packages", null);

        }

        void bgWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            Finished = true;
            this.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.Close();
        }


        void ReportProgress()
        {
            if (InvokeRequired)
            {
                IAsyncResult tag = BeginInvoke((MethodInvoker)ReportProgress);
                EndInvoke(tag);
            }
            else
            {
                if (Showing && DisplayProgress && WindowState == FormWindowState.Minimized)
                {
                    WindowState = FormWindowState.Normal; Opacity = 1;
                }

                labelTotal.Text = string.Format("Overall: {0} of {1}", FormatBytes(ProgressTotal), FormatBytes(MaxTotal));
                if (PercentTotal >= 0 && PercentTotal <= 100)
                    progressBarTotal.Value = PercentTotal;

                if (PercentCurrentFile >= 0 && PercentCurrentFile <= 100)
                    progressBar1.Value = PercentCurrentFile;

                labelPackage.Text = PackageText;
                labelprogressfile.Text = Ellipsis.Compact(ProgressText + "                      ", labelprogressfile, EllipsisFormat.Path);
                labelProgress.Text = string.Format("{0} of {1}", FormatBytes(ProgressCurrentFile), FormatBytes(MaxCurrentFile)/*, software.TranslateString("copied", null)*/);

                this.Update();
            }
        }


        void bgWorker_DoWork(object sender, DoWorkEventArgs e)
        {
            BackgroundWorker worker = sender as BackgroundWorker;
            InstallPackages(worker);
        }

        public string FormatBytes(double bytes)
        {
            const int scale = 1024;
            string[] orders = new string[] { "GB", "MB", "KB", "Bytes" };
            long max = (long)Math.Pow(scale, orders.Length - 1);

            foreach (string order in orders)
            {
                if (bytes > max)
                    return string.Format("{0:#.0} {1}", bytes / max, order);

                max /= scale;
            }
            return "0 Bytes";
        }

        public string ProgressText { get; set; }
        public string PackageText { get; set; }
        public double MaxCurrentFile { get; set; }
        public double ProgressCurrentFile { get; set; }
        public int PercentCurrentFile { get; set; }

        public double MaxTotal { get; set; }
        public double ProgressTotal { get; set; }
        public int PercentTotal { get; set; }

        private void DownloadProgress_Shown(object sender, EventArgs e)
        {
            Finished = false;
            ExecuteFiles = new List<FileInfo>();
            TopLevelSequences = new List<FileInfo>();
            //OverwriteOnNewVersionFiles = new Dictionary<FileInfo, int>();
            backgroundWorker.RunWorkerAsync();
        }

        private void DownloadProgress_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!Finished && MessageBox.Show(
                software.TranslateString("Download in progress, sure you want to cancel?", null),
                software.TranslateString("Download in progress", null),
                MessageBoxButtons.OKCancel) == System.Windows.Forms.DialogResult.Cancel)
                e.Cancel = true;
        }

        private void linkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            try { System.Diagnostics.Process.Start(((LinkLabel)sender).Tag.ToString()); }
            catch { } /* Dont care if default browser does not exist... */
        }



        internal void removeObsoleteFiles(DirectoryInfo root, Package newPackage)
        {
            try
            {
                //delete obsolete files/folders
                var oldPackage = software.getPreviousInstalledPackage(newPackage);

                if (oldPackage != null)
                {
                    var existingRootFolders = oldPackage.PackageFolders.Where(pf => pf.ParentFolderId == null).ToList();
                    var newRootFolders = newPackage.PackageFolders.Where(pf => pf.ParentFolderId == null).ToList();

                    compareFolders(root, existingRootFolders, newRootFolders);
                }
            }
            catch (Exception ex)
            {
                Env.LogException(ex, "Error occured in removeObsoleteFiles");
            }
        }


        private void compareFolders(DirectoryInfo directoryInfo, List<PackageFolder> existingFolders, List<PackageFolder> newFolders)
        {
            var toBeDeleted = existingFolders.Where(ef => !newFolders.Exists(nf => nf.Name == ef.Name)).ToList();
            var existingFoldersWithMatch = existingFolders.Where(ef => newFolders.Exists(nf => nf.Name == ef.Name)).ToList();

            foreach (PackageFolder existingFolder in existingFoldersWithMatch)
            {
                PackageFolder newFolder = newFolders.Where(nf => nf.Name == existingFolder.Name).FirstOrDefault();
                DirectoryInfo di = new DirectoryInfo(Path.Combine(directoryInfo.FullName, existingFolder.Name));

                List<PackageFolderFile> toBeDeletedFiles = existingFolder.PackageFolderFiles.Where(eff => !newFolder.PackageFolderFiles.Any(nff => nff.RepositoryFolderFile.Name == eff.RepositoryFolderFile.Name)).ToList();

                foreach (var file in toBeDeletedFiles)
                {
                    software.DeleteFile(di, file);
                }

                compareFolders(di, existingFolder.PackageFolders.ToList(), newFolder.PackageFolders.ToList());
            }

            if(toBeDeleted.Count > 0)
                software.deleteAllFiles(directoryInfo, toBeDeleted);
        }
                

        /// <summary>
        /// Install packages (overwriting modified files). 
        /// </summary>
        /// <param name="worker">Thread to run on</param>
        void InstallPackages(BackgroundWorker worker)
        {
            try
            {
                MaxTotal = software.validatePackages(this.packages);

                foreach (Package package in this.packages.OrderBy(p => p.Priority))
                {
                    PackageText = string.Format("{0}: {1} v{2}", software.TranslateString("Package", null), package.Name, package.Version);
                    ReportProgress();

                    Package installPackage = package;// software.UseSoftwareRestApi ? software.GetJson<Package>($"api/internal/Software/GetPackage?packageId={package.PackageId}") :
                                                     //                      ServicePool.GetSWService(Env.WCFConfigFile).GetPackage(package.PackageId);

                    string path = software.GetRootPath(installPackage);
                    var root = new DirectoryInfo(path);
                    if (!root.Exists)
                        root.Create();
                    
                    var r = from p in installPackage.PackageFolders where p.Parent == null select p;

                    removeObsoleteFiles(root, installPackage);

                    string installedPackagesPath = Env.GetConfigFilePath(Env.InstalledPackagesFileName);
                    var installedPackages = XDocument.Load(installedPackagesPath);

                    var installed = installedPackages?.Element("Packages")?.Elements()?.Where(p => p.Attribute("Name")?.Value == installPackage.Name).FirstOrDefault();
                    bool newPackageVer = false;

                    if (installed != null && installed.Attribute("Version").Value.ToInt32() < installPackage.Version)
                        newPackageVer = true;

                    downloadFiles(r, root, worker, newPackageVer);

                    software.storePackageInfo(installPackage, true);
                    software.LogPackageDownloaded(installPackage);
                }
            }
            catch (Exception ex)
            {
                if (this.DialogResult != DialogResult.Cancel)
                {
                    MessageBox.Show(this,
                        software.TranslateString("An error occurred trying to install the package", null),
                        software.TranslateString("Error Occurred", null),
                        MessageBoxButtons.OK, MessageBoxIcon.Error);
                    Env.LogException(ex, "Error in InstallPackage");
                    Finished = true;
                    this.DialogResult = System.Windows.Forms.DialogResult.Abort;
                    this.Close();
                }
            }

        }


        private void downloadFiles(IEnumerable<PackageFolder> packageFolders, DirectoryInfo parentFolder, BackgroundWorker worker, bool newPackageVer)
        {
            foreach (PackageFolder packageFolder in packageFolders)
            {
                DirectoryInfo folder = parentFolder.CreateSubdirectory(packageFolder.Name);
                foreach (PackageFolderFile pfile in packageFolder.PackageFolderFiles)
                {
                    
                    string fullname = Path.Combine(folder.FullName, pfile.RepositoryFolderFile.Name);
                    FileInfo currentFile = new FileInfo(fullname);
                    bool executeFile = false;
                    if (!currentFile.Exists || (currentFile.Exists && currentFile.LastWriteTimeUtc != pfile.RepositoryFolderFile.FileModifiedDate))
                    {
                        if ((FileAttribute)pfile.Attributes == FileAttribute.OverwriteNever && currentFile.Exists)
                            continue;
                        if ((FileAttribute)pfile.Attributes == FileAttribute.OverwriteOnNewPackageVersion && currentFile.Exists && !newPackageVer)
                            continue;

                        Showing = true;
                        ProgressText = fullname;
                        MaxCurrentFile = pfile.RepositoryFolderFile?.FileSize ?? 0; ProgressCurrentFile = 0; PercentCurrentFile = 0;
                        ReportProgress();


                        //prevent disposing objects before copy is completed?
                        int retry = 3;
                        while (retry-- > 0)
                        {
                            Stream FileByteStream = null;
                            WebResponse response = null;
                            //FileRequest req = null;
                            try
                            {
                                var request = software.serviceProxy.CreateHttpWebRequest("GET", $"api/internal/Software/DownloadFile?repositoryFolderFileId={pfile.RepositoryFolderFile.RepositoryFolderFileId}", 300000/*,"",""*/);
                                response = request.GetResponse();
                                FileByteStream = response.GetResponseStream();

                                if (MaxCurrentFile == 0 && (FileByteStream?.CanSeek ?? false))
                                    MaxCurrentFile = FileByteStream?.Length ?? 0;

                                using (FileStream writer = new FileStream(fullname, FileMode.Create, FileAccess.Write))
                                    copyStream(FileByteStream, writer, worker);
                                File.SetLastWriteTimeUtc(fullname, pfile.RepositoryFolderFile.FileModifiedDate);

                                if (((FileAttribute)pfile.Attributes & FileAttribute.ExecuteOnce) == FileAttribute.ExecuteOnce)
                                    ExecuteFiles.Add(currentFile);
                                //Already know file didn't exist, so can set executeFile = true if attribute fits
                                else if (((FileAttribute)pfile.Attributes & FileAttribute.ExecuteOncePerVersion) == FileAttribute.ExecuteOncePerVersion)
                                    executeFile = true;

                                break;
                            }
                            catch (Exception ex)
                            {
                                if (response != null)
                                    response.Close();

                                ProgressTotal -= ProgressCurrentFile;
                                if (retry == 0)
                                    throw ex;
                            }

                            if (response != null)
                                response.Close();
                        }

                        

                    }

                    //if execute once per package version?
                    //software.isPackageInstalled? -> check xml
                    // bool i = software.isPackageInstalled(Package);
                    //if (((FileAttribute)pfile.Attributes & FileAttribute.ExecuteOncePerVersion) == FileAttribute.ExecuteOncePerVersion)
                    //    ExecuteFiles.Add(currentFile);

                    //Add a new list or dictionary that contains any files to be skipped and when they should be overwritten.
                    //if (!OverwriteOnNewVersionFiles.ContainsKey(currentFile) && ((FileAttribute)pfile.Attributes & FileAttribute.OverwriteNever) == FileAttribute.OverwriteNever)
                    //    OverwriteOnNewVersionFiles.Add(currentFile, pfile.RepositoryFolderFile.Version);

                    if ((((FileAttribute)pfile.Attributes & FileAttribute.ExecuteAlways) == FileAttribute.ExecuteAlways) && !ExecuteFiles.Contains(currentFile))
                        ExecuteFiles.Add(currentFile);

                    if (((FileAttribute)pfile.Attributes & FileAttribute.TopLevelFile) == FileAttribute.TopLevelFile)
                        TopLevelSequences.Add(currentFile);

                    //If file is new or new package version
                    if ((executeFile || newPackageVer) && ((FileAttribute)pfile.Attributes & FileAttribute.ExecuteOncePerVersion) == FileAttribute.ExecuteOncePerVersion)
                        ExecuteFiles.Add(currentFile);

                }
                downloadFiles(packageFolder.PackageFolders.AsEnumerable(), folder, worker, newPackageVer);
            }
        }

        int oldP = 0;
        private void copyStream(Stream source, FileStream destination, BackgroundWorker worker)
        {
            int chunkSize = int.Parse(Env.FileTransferChunkSize);

            byte[] buffer = new byte[chunkSize];
            do
            {
                int bytesRead = source.Read(buffer, 0, chunkSize);
                if (bytesRead == 0) break;
                destination.Write(buffer, 0, bytesRead);

                ProgressCurrentFile = destination.Position;

                if (MaxCurrentFile > 0)
                    PercentCurrentFile = (int)((destination.Position / MaxCurrentFile) * 100);

                ProgressTotal += bytesRead;
                if (MaxTotal > 0)
                    PercentTotal = (int)((ProgressTotal / MaxTotal) * 100);


                if (oldP != PercentCurrentFile)
                {
                    oldP = PercentCurrentFile;
                    ReportProgress();
                }


            } while (true);
            destination.Close();
            source.Close();
        }

    }







    /// <summary>
    /// Specifies ellipsis format and alignment.
    /// </summary>
    [Flags]
    internal enum EllipsisFormat
    {
        /// <summary>
        /// Text is not modified.
        /// </summary>
        None = 0,
        /// <summary>
        /// Text is trimmed at the end of the string. An ellipsis (...) is drawn in place of remaining text.
        /// </summary>
        End = 1,
        /// <summary>
        /// Text is trimmed at the begining of the string. An ellipsis (...) is drawn in place of remaining text. 
        /// </summary>
        Start = 2,
        /// <summary>
        /// Text is trimmed in the middle of the string. An ellipsis (...) is drawn in place of remaining text.
        /// </summary>
        Middle = 3,
        /// <summary>
        /// Preserve as much as possible of the drive and filename information. Must be combined with alignment information.
        /// </summary>
        Path = 4,
        /// <summary>
        /// Text is trimmed at a word boundary. Must be combined with alignment information.
        /// </summary>
        Word = 8
    }


    internal class Ellipsis
    {
        /// <summary>
        /// String used as a place holder for trimmed text.
        /// </summary>
        public static readonly string EllipsisChars = "...";

        private static Regex prevWord = new Regex(@"\W*\w*$");
        private static Regex nextWord = new Regex(@"\w*\W*");

        /// <summary>
        /// Truncates a text string to fit within a given control width by replacing trimmed text with ellipses. 
        /// </summary>
        /// <param name="text">String to be trimmed.</param>
        /// <param name="ctrl">text must fit within ctrl width.
        ///	The ctrl's Font is used to measure the text string.</param>
        /// <param name="options">Format and alignment of ellipsis.</param>
        /// <returns>This function returns text trimmed to the specified witdh.</returns>
        public static string Compact(string text, Control ctrl, EllipsisFormat options)
        {
            if (string.IsNullOrEmpty(text.Trim()))
                return text;

            // no aligment information
            if (options == EllipsisFormat.None)
                return text;

            if (ctrl == null)
                throw new ArgumentNullException("ctrl");

            using (Graphics dc = ctrl.CreateGraphics())
            {
                Size s = TextRenderer.MeasureText(dc, text, ctrl.Font);

                // control is large enough to display the whole text
                if (s.Width <= ctrl.Width)
                    return text;

                string pre = "";
                string mid = text;
                string post = "";

                bool isPath = (EllipsisFormat.Path & options) != 0;

                // split path string into <drive><directory><filename>
                if (isPath)
                {
                    pre = Path.GetPathRoot(text);
                    mid = Path.GetDirectoryName(text).Substring(pre.Length);
                    post = Path.GetFileName(text);
                }

                int len = 0;
                int seg = mid.Length;
                string fit = "";

                // find the longest string that fits into 
                // the control boundaries using bisection method
                while (seg > 1)
                {
                    seg -= seg / 2;

                    int left = len + seg;
                    int right = mid.Length;

                    if (left > right)
                        continue;

                    if ((EllipsisFormat.Middle & options) == EllipsisFormat.Middle)
                    {
                        right -= left / 2;
                        left -= left / 2;
                    }
                    else if ((EllipsisFormat.Start & options) != 0)
                    {
                        right -= left;
                        left = 0;
                    }

                    // trim at a word boundary using regular expressions
                    if ((EllipsisFormat.Word & options) != 0)
                    {
                        if ((EllipsisFormat.End & options) != 0)
                        {
                            left -= prevWord.Match(mid, 0, left).Length;
                        }
                        if ((EllipsisFormat.Start & options) != 0)
                        {
                            right += nextWord.Match(mid, right).Length;
                        }
                    }

                    // build and measure a candidate string with ellipsis
                    string tst = mid.Substring(0, left) + EllipsisChars + mid.Substring(right);

                    // restore path with <drive> and <filename>
                    if (isPath)
                    {
                        tst = Path.Combine(Path.Combine(pre, tst), post);
                    }
                    s = TextRenderer.MeasureText(dc, tst, ctrl.Font);

                    // candidate string fits into control boundaries, try a longer string
                    // stop when seg <= 1
                    if (s.Width <= ctrl.Width)
                    {
                        len += seg;
                        fit = tst;
                    }
                }

                if (len == 0) // string can't fit into control
                {
                    // "path" mode is off, just return ellipsis characters
                    if (!isPath)
                        return EllipsisChars;

                    // <drive> and <directory> are empty, return <filename>
                    if (pre.Length == 0 && mid.Length == 0)
                        return post;

                    // measure "C:\...\filename.ext"
                    fit = Path.Combine(Path.Combine(pre, EllipsisChars), post);

                    s = TextRenderer.MeasureText(dc, fit, ctrl.Font);

                    // if still not fit then return "...\filename.ext"
                    if (s.Width > ctrl.Width)
                        fit = Path.Combine(EllipsisChars, post);
                }
                return fit;
            }
        }
    }
}
