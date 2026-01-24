//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.ServiceModel;
//using Virinco.WATS.Service.MES.Contract;
//using System.IO;
//using System.Collections;
//using System.Reflection;
//using System.Xml;
//using System.Xml.Linq;
//using System.Windows.Forms;
//using System.Xml.XPath;

//namespace Virinco.WATS.Interface.MES.Software
//{
//    /// <summary>
//    /// Class to handle software distribution
//    /// </summary>
//    public class Software : MesBase
//    {
//        private string installedPackagesPath = Env.GetConfigFilePath(Env.InstalledPackagesFileName);

//        /// <summary>
//        /// True if connected to server
//        /// </summary>
//        /// <returns></returns>
//        public new bool isConnected()
//        {
//            return base.isConnected();
//        }

//        /// <summary>
//        /// Returns an array of revoked packages matching the tags. All package versions are included
//        /// </summary>
//        /// <param name="tagNames">Array of tags</param>
//        /// <param name="tagValues">Array of tag values matching index of the tagnames array</param>   
//        /// <param name="SelectedPackage">The selected package (from GUI)</param>
//        /// <param name="Continue">True if a package is selected (from Gui)</param>
//        /// <param name="ExecuteFiles">Array of executable files in selected package</param>
//        /// <param name="TopLevelSequences">Array of toplevelsequencefiles in selected package</param>
//        /// <returns>Matching Packages</returns>  
//        public Package[] GetRevokedPackages(string[] tagNames, string[] tagValues, out Package SelectedPackage, out bool Continue, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences)
//        {
//            string XPath = "//*";
//            for (int i = 0; i < tagNames.Length; i++)
//            {
//                string tag = tagNames[i];
//                string value = tagValues[i];

//                if (!string.IsNullOrEmpty(tag) && value != null)
//                {
//                    if (tag == "StationName")
//                        XPath += string.Format("[{0}[.=\"{1}\" or .=\"Any\"]] ", tag, value);
//                    else
//                        XPath += string.Format("[{0}[.=\"{1}\"]] ", tag, value);
//                }
//            }

//            List<Package> packages = serviceProxy.GetJson<Package[]>($"api/internal/Software/GetPackageHistory?tags={XPath}&status={StatusEnum.Revoked}&allVersions=true").OrderBy(p => p.Name).ThenBy(p => p.Version).ToList();
//            if (packages != null && packages.Count() > 0)
//                validatePackages(packages);

//            SelectedPackage = null;
//            Continue = true;
//            TopLevelSequences = null;
//            ExecuteFiles = null;

//            using (PackageHistory ph = new PackageHistory(this, packages))
//            {
//                ph.ShowDialog();
//                SelectedPackage = ph.SelectedPackage;
//                Continue = ph.Continue;

//                if (SelectedPackage != null)
//                {
//                    InstallPackage(SelectedPackage, true, true, out ExecuteFiles, out TopLevelSequences);
//                }
//            }

//            return packages.ToArray();
//        }

//        private string getXpath(string PartNumber = null, string Process = null, string StationType = null, string Revision = null, string StationName = null, string Misc = null)
//        {
//            string XPath = "//*";
//            if (PartNumber != null)
//                XPath += string.Format("[PartNumber[.=\"{0}\"]] ", System.Security.SecurityElement.Escape(PartNumber));

//            if (Process != null)
//                XPath += string.Format("[Process[.=\"{0}\"]] ", System.Security.SecurityElement.Escape(Process));

//            if (StationType != null)
//                XPath += string.Format("[StationType[.=\"{0}\"]] ", System.Security.SecurityElement.Escape(StationType));

//            if (Revision != null)
//                XPath += string.Format("[Revision[.=\"{0}\"]] ", System.Security.SecurityElement.Escape(Revision));

//            if (StationName != null)
//                XPath += string.Format("[StationName[.=\"{0}\" or .=\"Any\"]] ", System.Security.SecurityElement.Escape(StationName));

//            if (Misc != null)
//                XPath += string.Format("[Misc[.=\"{0}\"]] ", System.Security.SecurityElement.Escape(Misc));

//            return XPath;
//        }


//        /// <summary>
//        /// Get Package by default tags. Default value (null) will skip tag.
//        /// </summary>
//        /// <param name="PartNumber">Tagged with a given PartNumber</param>
//        /// <param name="Process">Tagged with a given Process</param>
//        /// <param name="StationType">Tagged with a given StationType</param>
//        /// <param name="Revision">Tagged with a given Revision</param>
//        /// <param name="StationName">Tagged with a given Staion Name</param>
//        /// <param name="Misc">Tagged with a given Misc value</param>        
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package[] GetPackages(string PartNumber = null, string Process = null, string StationType = null, string Revision = null/*, string Site = null*/, string StationName = null, string Misc = null, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
//        {
//            string XPath = getXpath(PartNumber, Process, StationType, Revision, StationName, Misc);
//            return GetPackagesByTag(XPath, Install, DisplayProgress, WaitForExecution, PackageStatus);
//        }

//        /// <summary>
//        /// Get an array of Packages.
//        /// </summary>
//        /// <param name="XPath">Return Packages with a Tag matching the XPath</param>
//        /// <param name="ExecuteFiles">List of files beeing executed</param>
//        /// <param name="TopLevelSequences">List of toplevel sequences</param>
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package[] GetPackagesByTag(string XPath, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
//        {
//            ExecuteFiles = null;
//            TopLevelSequences = null;

//            if (isConnected())
//            {
//                try
//                {
//                    List<Package> packages = serviceProxy.GetJson<List<Package>>($"api/internal/Software/GetPackagesByTag?tags={XPath}&status={PackageStatus}");

//                    if (packages != null && packages.Count > 0)
//                    {

//                        if (Install)
//                            InstallPackage(packages.ToArray(), DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences);
//                        else
//                            validatePackages(packages);

//                        return packages.OrderBy(p => p.Name).ToArray();
//                    }
//                }
//                catch (Exception ex) { Env.LogException(ex, "Error in GetPackagesByTag"); }
//            }
//            else if (File.Exists(installedPackagesPath))
//            {
//                //Replace //* (any element anywhere, not just as children of current element) with ./* (any child element of current element), because here all tags are in the same document
//                var offlineXPath = "./*" + XPath.Substring(3); 

//                var xDoc = XDocument.Load(installedPackagesPath);
//                var xPackages = xDoc.Root.Elements("Package").Where(e => e.Element("Tags").XPathSelectElements(offlineXPath).Any() && e.Attribute("Status").Value == ((int)PackageStatus).ToString());

//                return GetPackagesOffline(xPackages, WaitForExecution, out ExecuteFiles, out TopLevelSequences, Install);
//            }
//            return new Package[0];
//        }

//        /// <summary>
//        /// Get an array of Packages.
//        /// </summary>
//        /// <param name="XPath">Return Packages with a Tag matching the XPath</param>
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package[] GetPackagesByTag(string XPath, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
//        {

//            List<FileInfo> ExecuteFiles = null;
//            List<FileInfo> TopLevelSequences = null;
//            return GetPackagesByTag(XPath, out ExecuteFiles, out TopLevelSequences, Install, DisplayProgress, WaitForExecution, PackageStatus);
//        }


//        /// <summary>
//        /// Returns Packages matching a dictionary of Tag/Values.
//        /// </summary>
//        /// <param name="TagValue"></param>
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package[] GetPackagesByTag(Dictionary<string, string> TagValue, bool Install, bool DisplayProgress, bool WaitForExecution, StatusEnum PackageStatus = StatusEnum.Released)
//        {
//            List<FileInfo> fi = null;
//            return GetPackagesByTag(TagValue, Install, DisplayProgress, WaitForExecution, out fi, out fi, PackageStatus);
//        }

//        /// <summary>
//        /// Returns Packages matching array of Tag/Values.
//        /// </summary>
//        /// <param name="tagNames">Array of tags to match (the tag value should be located on identical index in the tagValues array)</param>
//        /// <param name="tagValues">Array of tagvalues to match (the tag name should be placed on the identical index in the tagNames array)</param>
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="ExecuteFiles">List of files beeing executed</param>
//        /// <param name="TopLevelSequences">List of toplevel sequences</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package[] GetPackagesByTag(string[] tagNames, string[] tagValues, bool Install, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, StatusEnum PackageStatus = StatusEnum.Released)
//        {
//            ExecuteFiles = null;
//            TopLevelSequences = null;
//            try
//            {
//                string XPath = "//*";
//                for (int i = 0; i < tagNames.Length; i++)
//                {
//                    string tag = tagNames[i];
//                    string value = tagValues.Length > i ? tagValues[i] : "";


//                    if (!string.IsNullOrEmpty(tag) && value != null)
//                    {
//                        if (tag == "StationName")
//                            XPath += string.Format("[{0}[.=\"{1}\" or .=\"Any\"]] ", tag, value);
//                        else
//                            XPath += string.Format("[{0}[.=\"{1}\"]] ", tag, value);
//                    }
//                }

//                return GetPackagesByTag(XPath, out ExecuteFiles, out TopLevelSequences, Install, DisplayProgress, WaitForExecution, PackageStatus);

//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in GetPackagesByTag"); }
//            return new Package[0];
//        }

//        /// <summary>
//        /// Returns Packages matching a dictionary of Tag/Values.
//        /// </summary>
//        /// <param name="TagValue"></param>
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="ExecuteFiles">List of files beeing executed</param>
//        /// <param name="TopLevelSequences">List of toplevel sequences</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package[] GetPackagesByTag(Dictionary<string, string> TagValue, bool Install, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, StatusEnum PackageStatus = StatusEnum.Released)
//        {
//            string[] tagNames = TagValue.Keys.ToArray();
//            string[] tagValues = new string[tagNames.Length];

//            for (int i = 0; i < tagNames.Length; i++)
//            {
//                tagValues[i] = TagValue[tagNames[i]];
//            }
//            return GetPackagesByTag(tagNames, tagValues, Install, DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences, PackageStatus);
//        }

//        /// <summary>
//        /// Get Packages with a given name.
//        /// </summary>
//        /// <param name="PackageName">Name of Package</param>
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="ExecuteFiles">List of files beeing executed</param>
//        /// <param name="TopLevelSequences">List of toplevel sequences</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package GetPackageByName(string PackageName, bool Install, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, StatusEnum PackageStatus = StatusEnum.Released)
//        {
//            ExecuteFiles = null;
//            TopLevelSequences = null;

//            if (isConnected())
//            {
//                try
//                {
//                    var package = serviceProxy.GetJson<Package>($"api/internal/Software/GetPackageByName?packageName={PackageName}&status={PackageStatus}");

//                    if (package != null)
//                    {
//                        if (Install)
//                            InstallPackage(package, DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences);
//                        else
//                            validatePackages(new List<Package>(new[] { package }));

//                        return package;
//                    }
//                }
//                catch (Exception ex) { Env.LogException(ex, "Error in GetPackageByName"); }
//            }
//            else if (File.Exists(installedPackagesPath))
//            {
//                var xDoc = XDocument.Load(installedPackagesPath);
//                var xPackages = xDoc.Root.Elements("Package").Where(e => e.Attribute("Name").Value == PackageName && e.Attribute("Status").Value == ((int)PackageStatus).ToString());
                
//                return GetPackagesOffline(xPackages, WaitForExecution, out ExecuteFiles, out TopLevelSequences, Install).FirstOrDefault();
//            }
//            return null;
//        }

//        /// <summary>
//        /// Get Packages with a given name
//        /// </summary>
//        /// <param name="PackageName">Name of Package</param>
//        /// <param name="Install">Install Package?</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="PackageStatus">Status of package to get</param>
//        /// <returns></returns>
//        public Package GetPackageByName(string PackageName, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
//        {
//            return GetPackageByName(PackageName, Install, DisplayProgress, WaitForExecution, out _, out _, PackageStatus);
//        }


//        /// <summary>
//        /// Install an array of Packages. Getting files to filesystem and executing files being marked for execution
//        /// </summary>
//        /// <param name="packages">Packages to install</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finish</param>
//        /// <param name="ExecuteFiles">List of files being tagged for execution</param>
//        /// <param name="TopLevelSequences">List of files being tagged as top level sequence</param>
//        public void InstallPackage(Package[] packages, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences)
//        {
//            ExecuteFiles = null;
//            TopLevelSequences = null;
//            try
//            {
//                //Priority less than 0 is from offline storage, 0 or more is from server
//                var download = packages.Where(p => p.Priority >= 0).ToList();
                
//                if (download.Any())
//                {
//                    using (DownloadProgress dp = new DownloadProgress(this, download, DisplayProgress))
//                    {
//                        dp.Opacity = 0; dp.WindowState = FormWindowState.Minimized;
//                        if (dp.ShowDialog() == DialogResult.OK)
//                        {
//                            foreach (FileInfo fi in dp.ExecuteFiles)
//                                ExecuteFile(fi, WaitForExecution);

//                            ExecuteFiles = dp.ExecuteFiles;
//                            TopLevelSequences = dp.TopLevelSequences;
//                        }
//                    }
//                }

//                var ids = packages.Where(p => p.Priority < 0).Select(p => p.PackageId).ToList();
//                if (ids.Any()) 
//                {                    
//                    var xDoc = XDocument.Load(installedPackagesPath);
//                    var xPackages = xDoc.Root.Descendants("Package").Where(e => ids.Contains(Guid.Parse(e.Attribute("PackageId").Value)));

//                    _ = GetPackagesOffline(xPackages, WaitForExecution, out ExecuteFiles, out TopLevelSequences,  true);
//                }

//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in InstallPackage"); }
//        }



//        /// <summary>
//        /// Install an array of Packages. Getting files to filesystem and executing files being marked for execution
//        /// </summary>
//        /// <param name="packages">Packages to install</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        public void InstallPackage(Package[] packages, bool DisplayProgress, bool WaitForExecution)
//        {
//            List<FileInfo> fi = null;
//            InstallPackage(packages, DisplayProgress, WaitForExecution, out fi, out fi);
//        }

//        /// <summary>
//        /// Install a given package (overwriting modified files). Getting files to filesystem and executing files being marked for execution
//        /// </summary>
//        /// <param name="package">Package to install</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        /// <param name="ExecuteFiles">List of files beeing tagged for execution</param>
//        /// <param name="TopLevelSequences">List of files being tagged as top level sequence</param>
//        public void InstallPackage(Package package, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences)
//        {
//            Package[] packages = new Package[] { package };
//            InstallPackage(packages, DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences);
//        }


//        /// <summary>
//        /// Install a given package (overwriting modified files). 
//        /// </summary>
//        /// <param name="package">Package to install</param>
//        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
//        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
//        public void InstallPackage(Package package, bool DisplayProgress, bool WaitForExecution)
//        {
//            InstallPackage(package, DisplayProgress, WaitForExecution, out _, out _);
//        }

//        /// <summary>
//        /// Set path to local software root folder, where packages will be installed.
//        /// </summary>
//        /// <param name="rootFolderPath">
//        /// <para>Path to the new folder packages will be installed into. Must be an absolute path, and should be an empty folder.</para>
//        /// <para>NB! Existing files in the folder may be overwritten by packages.</para></param>
//        /// <param name="moveExistingPackages">
//        /// <para>
//        /// Choose to move packages files to the new folder. 
//        /// May fail if folder or file with same name as a package already exists in the new folder.
//        /// If files are not moved, installed packages will stop working until they are reinstalled.
//        /// </para>
//        /// <para>NB! If the current root folder does not only contain packages, those files will also be moved.</para>
//        /// </param>
//        public static void SetRootFolderPath(string rootFolderPath, bool moveExistingPackages = true)
//        {
//            string root = Path.GetPathRoot(rootFolderPath);
//            if (!root.StartsWith(@"\\") && !root.EndsWith(@"\"))
//                throw new ArgumentException($"Must be an absolute path.", nameof(rootFolderPath));

//            //Change setting before move because it is easier to fix if move fails.
//            string currentRootFolderPath = Env.MESSoftwareDistributionRoot;
//            Env.MESSoftwareDistributionRoot = rootFolderPath;

//            if (moveExistingPackages)
//            {
//                var currentDirectory = new DirectoryInfo(currentRootFolderPath);
//                foreach (var item in currentDirectory.EnumerateDirectories())
//                    item.MoveTo(Path.Combine(rootFolderPath, item.Name));

//                foreach (var item in currentDirectory.EnumerateFiles())
//                    item.MoveTo(Path.Combine(rootFolderPath, item.Name));
//            }
//        }

//        /// <summary>
//        /// Returns the local Root Folder path where software packages are installed
//        /// </summary>
//        /// <returns></returns>
//        public static string GetRootFolderPath()
//        {
//            return Env.MESSoftwareDistributionRoot;
//        }

//        /// <summary>
//        /// Populate package download size and return number of bytes needed to download all packages
//        /// </summary>
//        /// <param name="packages"></param>
//        /// <returns></returns>
//        internal long validatePackages(List<Package> packages)
//        {
//            //XDocument doc = System.IO.File.Exists(installedPackagesXml) ? XDocument.Load(installedPackagesXml) :null;
//            //installed = doc.Descendants("Package").Any(p => new Guid(p.Attribute("PackageId").Value) == package.PackageId);
//            long total = 0;
//            for (int i = 0; i < packages.Count(); i++)
//            {
//                Package package = packages[i];
//                var installPackage = getPackageById(package.PackageId);

//                packages[i] = installPackage;

//                installPackage.DownloadSize = 0;
//                DirectoryInfo root = null;
//                string path = Path.Combine(Env.MESSoftwareDistributionRoot, package.PackageFolder ? package.Name : "");
//                if (Directory.Exists(path))
//                    root = new DirectoryInfo(path);

//                var folders = from pf in installPackage.PackageFolders where pf.Parent == null select pf;
//                installPackage.DownloadSize += validateFiles(folders, root);
//                total += installPackage.DownloadSize.Value;

//                storePackageInfo(installPackage, false);
//                //var xmlPackage = doc.Descendants("Package").FirstOrDefault(p => p.Attribute("PackageId")?.Value == installPackage.PackageId.ToString());
//                //if(xmlPackage != null)
//                //    xmlPackage.SetAttributeValue("DownloadSize",installPackage.DownloadSize.Value.ToString());


//                //xmlPackage = doc.Descendants("Package").FirstOrDefault(p => 
//                //                    p.Attribute("Name")?.Value == package.Name &&
//                //                    Utilities.ParseInt32(p.Attribute("Version")?.Value, 0) < package.Version  
//                //                    //&& new Guid(p.Attribute("PackageId")?.Value) != package.PackageId
//                //                    );

//                //if (xmlPackage != null)
//                //    xmlPackage.SetAttributeValue("AvailableVersion", installPackage.Version);


//            }
//            // doc.Save(installedPackagesXml);

//            return total;
//        }

//        private long validateFiles(IEnumerable<PackageFolder> packageFolders, DirectoryInfo parentFolder)
//        {
//            long total = 0;
//            foreach (PackageFolder packageFolder in packageFolders)
//            {
//                string folderPath = null;
//                DirectoryInfo folderInfo = null;

//                if (parentFolder != null)
//                {
//                    folderPath = Path.Combine(parentFolder.FullName, packageFolder.Name);
//                    if (Directory.Exists(folderPath))
//                        folderInfo = new DirectoryInfo(folderPath);
//                }

//                foreach (PackageFolderFile pfile in packageFolder.PackageFolderFiles)
//                {
//                    if (folderInfo == null)// && pfile.RepositoryFolderFile.FileSize.HasValue)
//                    {
//                        if (pfile.RepositoryFolderFile.FileSize.HasValue)
//                            total += pfile.RepositoryFolderFile.FileSize.Value;
//                    }
//                    else
//                    {
//                        string filePath = Path.Combine(folderInfo.FullName, pfile.RepositoryFolderFile.Name);
//                        FileInfo fileInfo = new FileInfo(filePath);
//                        if (!fileInfo.Exists || (fileInfo.Exists && fileInfo.LastWriteTimeUtc != pfile.RepositoryFolderFile.FileModifiedDate))
//                        {
//                            if (pfile.RepositoryFolderFile.FileSize.HasValue)
//                                total += pfile.RepositoryFolderFile.FileSize.Value;
//                        }
//                    }
//                }
//                total += validateFiles(packageFolder.PackageFolders.AsEnumerable(), folderInfo);
//            }
//            return total;
//        }



//        /// <summary>
//        /// Method to clean file distribution root folder
//        /// </summary>
//        /// <param name="PromptOperator">Display a OK/Cancel dialog</param>
//        public void DeleteAllPackages(bool PromptOperator = true)
//        {
//            if (!PromptOperator || (PromptOperator && System.Windows.Forms.MessageBox.Show(string.Format("{0} '{1}'", TranslateString("Delete all Packages in", null), Env.MESSoftwareDistributionRoot), TranslateString("Confirm", null), System.Windows.Forms.MessageBoxButtons.OKCancel) == System.Windows.Forms.DialogResult.OK))
//            {
//                try
//                {
//                    Directory.Delete(Env.MESSoftwareDistributionRoot, true);
//                }
//                catch (Exception ex) { Env.LogException(ex, "Error in DeleteAllPackages"); }
//            }
//        }



//        /// <summary>
//        /// Delete all files and empty folders
//        /// </summary>
//        /// <param name="package"></param>
//        internal void deleteAllFiles(Package package)
//        {
//            try
//            {
//                if (package == null)
//                    return;  
                
//                string path = GetRootPath(package);
//                var directoryInfo = new DirectoryInfo(path);

//                var rootFolders = package.PackageFolders.Where(pf => pf.ParentFolderId == null).ToList();

//                deleteAllFiles(directoryInfo, rootFolders);
//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in deleteAllFiles(package)"); }
//        }

//        /// <summary>
//        /// Delete all files and empty folders
//        /// </summary>
//        /// <param name="directoryInfo"></param>
//        /// <param name="folders">package root folders</param>
//        internal void deleteAllFiles(DirectoryInfo directoryInfo, List<PackageFolder> folders)
//        {
//            try
//            {
//                foreach (var folder in folders)
//                {
//                    DirectoryInfo di = new DirectoryInfo(Path.Combine(directoryInfo.FullName, folder.Name));

//                    foreach (var file in folder.PackageFolderFiles)
//                    {
//                        DeleteFile(di, file);
//                    }

//                    deleteAllFiles(di, folder.PackageFolders.ToList());

//                    if (di.Exists && di.GetFiles().Length == 0)
//                        di.Delete(true);
//                }
//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in deleteAllFiles"); }
//        }



//        /// <summary>
//        /// Delete revoked packages. 
//        /// Only revoked packages without a released version are deleted (packages without a new released verison)
//        /// </summary>
//        /// <param name="PromptOperator">Display a OK/Cancel dialog</param>
//        public void DeleteRevokedPackages(bool PromptOperator = true)
//        {
//            if (!PromptOperator || (PromptOperator && System.Windows.Forms.MessageBox.Show(string.Format("{0} '{1}'", TranslateString("Delete revoked Packages in", null), Env.MESSoftwareDistributionRoot), TranslateString("Confirm", null), System.Windows.Forms.MessageBoxButtons.OKCancel) == System.Windows.Forms.DialogResult.OK))
//            {
//                try
//                {
//                    if (File.Exists(installedPackagesPath))
//                    {
//                        var doc = XDocument.Load(installedPackagesPath);
//                        List<Guid> installedGuids = (from g in doc.Descendants("Package")
//                                                     select new Guid(g.Attribute("PackageId").Value)).ToList();

//                        //IDs of installed packages which are deleted or revoked on server
//                        List<Guid> deleteGuids = serviceProxy.GetJson<List<Guid>>($"api/internal/Software/GetRevokedPackages?includeRevokedOnly=true&installedPackages={string.Join(",", installedGuids.Select(g => g.ToString()).ToArray())}");

//                        var removePackages = (from p in doc.Descendants("Package")
//                                              join d in deleteGuids on new Guid(p.Attribute("PackageId").Value) equals d
//                                              select p).ToList();

//                        foreach (var e in removePackages)
//                        {
//                            bool packageNameIsFolderName = true;
//                            Boolean.TryParse(e.Attribute("PackageFolder").Value, out packageNameIsFolderName);

//                            if (packageNameIsFolderName)
//                            {
//                                string packagePath = Path.Combine(Env.MESSoftwareDistributionRoot, e.Attribute("Name").Value);
//                                if (Directory.Exists(packagePath))
//                                    Directory.Delete(packagePath, true);
//                            }
//                            else
//                            {
//                                //get package by id and run delete files 
//                                string guid = e?.Attribute("PackageId")?.Value;
//                                if (!string.IsNullOrEmpty(guid))
//                                {                                    
//                                    var p = getPackageById(new Guid(guid));
//                                    deleteAllFiles(p);
//                                }
                                
//                                /* var folders = (from f in e.Descendants("Folder")
//                                               select f.Attribute("Name").Value).ToList();

//                                foreach (string foldername in folders)
//                                {
//                                    string packagePath = Path.Combine(Env.MESSoftwareDistributionRoot, foldername);
//                                    if (System.IO.Directory.Exists(packagePath))
//                                        System.IO.Directory.Delete(packagePath, true);
//                                }*/
//                            }
//                            e.Remove();
//                        }
//                        doc.Save(installedPackagesPath);
//                    }
//                }
//                catch (Exception ex) { Env.LogException(ex, "Error in DeleteRevokedPackages"); }
//            }
//        }

//        /// <summary>
//        /// Store information about a package
//        /// </summary>
//        /// <param name="package"></param>
//        /// <param name="markAsInstalled">Mark package as installed or available</param>
//        internal void storePackageInfo(Package package, bool markAsInstalled = false)// Guid PackageGuid, string PackageName, string FolderName)
//        {
//            try
//            {
//                if (!File.Exists(installedPackagesPath))
//                { 
//                    var xml = new XElement("Packages");
//                    xml.Save(installedPackagesPath);
//                }

//                XDocument doc = XDocument.Load(installedPackagesPath);

//                var xPackage = doc.Descendants("Package").Where(p => p.Attribute("PackageId").Value == package.PackageId.ToString()).SingleOrDefault();
//                if (xPackage == null) //new package
//                {
//                    xPackage = new XElement("Package",
//                        new XAttribute("PackageId", package.PackageId),
//                        new XAttribute("Name", package.Name),
//                        new XAttribute("Version", package.Version),
//                        new XAttribute("PackageFolder", package.PackageFolder),
//                        new XAttribute("RootDirectory", package.RootDirectory ?? ""),
//                        new XAttribute("DownloadSize", package.DownloadSize.Value),
//                        new XAttribute("Description", package.Description),
//                        new XAttribute("Status", package.Status),
//                        new XAttribute("Installed", markAsInstalled),
//                        new XElement("RootFolders", package.PackageFolders.Where(pf => !package.PackageFolder && pf.Parent == null).Select(pf =>
//                            new XElement("Folder", new XAttribute("Name", pf.Name))
//                        )),
//                        (!string.IsNullOrEmpty(package.Tags) ? new XElement("Tags", XElement.Parse(package.Tags)) : new XElement("Tags"))
//                    );

//                    doc.Element("Packages").Add(xPackage);
//                }
//                else
//                {
//                    if (markAsInstalled)
//                    {//only set installed, never clear flag
//                        xPackage.SetAttributeValue("Installed", markAsInstalled);
//                        xPackage.SetAttributeValue("InstalledDate", DateTime.UtcNow.ToString("s"));
//                    }
//                    xPackage.SetAttributeValue("DownloadSize", markAsInstalled ? 0 : package.DownloadSize.Value);
//                    xPackage.SetAttributeValue("Status", package.Status);
//                }

//                //When installing, save file info
//                if (markAsInstalled)
//                {
//                    var xFiles = new XElement("Files");
//                    foreach (var folder in package.PackageFolders)
//                        GetXFiles(xFiles, folder, "");

//                    xPackage.Element("Files")?.Remove();
//                    xPackage.Add(xFiles);

//                    void GetXFiles(XElement root, PackageFolder packageFolder, string path)
//                    {
//                        path = Path.Combine(path, packageFolder.Name);
//                        foreach (var file in packageFolder.PackageFolderFiles)
//                        {
//                            string filePath = Path.Combine(path, file.RepositoryFolderFile.Name);
//                            root.Add(new XElement("File", new XAttribute("Id", file.PackageFolderFileId), new XAttribute("Attributes", file.Attributes), new XAttribute("Path", filePath)));
//                        }

//                        foreach (var folder in packageFolder.PackageFolders)
//                            GetXFiles(root, folder, path);
//                    }
//                }

//                var old = doc.Descendants("Package").Where(p => p.Attribute("Name").Value == package.Name && p.Attribute("PackageId").Value != package.PackageId.ToString()).ToList();
//                if (old != null && old.Count() > 0)
//                {
//                    for (int i = 0; i < old.Count(); i++)
//                    {
//                        var o = old[i];

//                        // if (Utilities.ParseInt32(o.Attribute("Version")?.Value, 0) < package.Version)
//                        // if(package.DownloadSize.Value > 0)
//                        o.SetAttributeValue("AvailableVersion", package.Version);

//                        if (markAsInstalled)//remove old version
//                            o.Remove();
//                    }


//                }

//                doc.Save(installedPackagesPath);
//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in storePackageInfo"); }
//        }

//        internal void DeleteFile(DirectoryInfo folder, PackageFolderFile file)
//        {
//            var fi = new FileInfo(Path.Combine(folder.FullName, file.RepositoryFolderFile.Name));
//            if (fi.Exists)
//                fi.Delete();

//            if (File.Exists(installedPackagesPath)) 
//            { 
//                var doc = XDocument.Load(installedPackagesPath);
//                var xFiles = doc.Descendants("File").Where(f => f.Attribute("Id").Value == file.PackageFolderFileId.ToString());
//                foreach(var xFile in xFiles)                
//                    xFile.Remove();

//                doc.Save(installedPackagesPath);
//            }
//        }




//        /// <summary>
//        /// return the previous installed package or null.
//        /// 
//        /// </summary>
//        /// <param name="package">new package to compare with</param>
//        /// <returns></returns>
//        internal Package getPreviousInstalledPackage(Package package)
//        {
//            try
//            {
//                if (File.Exists(installedPackagesPath))
//                {
//                    var doc = XDocument.Load(installedPackagesPath);
//                    var tmp = doc.Descendants("Package").Where(p => p.Attribute("Name").Value == package.Name && p.Attribute("Installed")?.Value?.ToLower() == Boolean.TrueString.ToLower() && p.Attribute("PackageId").Value != package.PackageId.ToString()).FirstOrDefault();

//                    string guid = tmp?.Attribute("PackageId")?.Value;
//                    if (!string.IsNullOrEmpty(guid))
//                    {
//                        Guid packageId = new Guid(guid);
//                        return getPackageById(packageId);
//                    }
//                }
//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in getPreviousInstalledPackage"); }
//            return null;
//        }


//        /// <summary>
//        /// Get a package with a given id
//        /// </summary>
//        /// <param name="packageId"></param>
//        /// <returns></returns>
//        internal Package getPackageById(Guid packageId)
//        {
//            try
//            {
//                return serviceProxy.GetJson<Package>($"api/internal/Software/GetPackage?packageId={packageId}");
//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in getPackageById"); }
//            return null;
//        }


//        /// <summary>
//        /// Check server for new version of installed packages
//        /// </summary>
//        /// <param name="PackagesAvailable">boolean value if new packages exists</param>
//        /// <returns>Array of available packages</returns>
//        public Package[] GetAvailablePackages(out bool PackagesAvailable)
//        {
//            PackagesAvailable = false;
//            List<Package> ret = new List<Package>();
//            try
//            {
//                if (File.Exists(installedPackagesPath))
//                {
//                    var doc = XDocument.Load(installedPackagesPath);
//                    List<Guid> installedGuids = (from g in doc.Descendants("Package")
//                                                 select new Guid(g.Attribute("PackageId").Value)).ToList();

//                    ret = serviceProxy.GetJson<List<Package>>($"api/internal/Software/GetAvailablePackages?installedPackages={string.Join(",", installedGuids.Select(g => g.ToString()).ToArray())}");

//                    if (ret != null && ret.Count > 0)
//                        validatePackages(ret);

//                    PackagesAvailable = ret.Count > 0;
//                }
//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in GetAvailablePackages"); }
//            return ret.ToArray();
//        }

//        /// <summary>
//        /// Log information about a package beeing downloaded
//        /// </summary>
//        internal void LogPackageDownloaded(Package p)
//        {
//            if (isConnected())
//            {
//                try
//                {
//                    serviceProxy.GetJson<List<Package>>($"api/internal/Software/Log?packageId={p.PackageId}&downloadSize={p.DownloadSize}");
//                }
//                catch (Exception ex) { Env.LogException(ex, "Error in LogPackageDownloaded"); }
//            }
//        }

//        internal string GetRootPath(Package package)
//        {
//            string rootPath = !string.IsNullOrEmpty(package.RootDirectory) ? package.RootDirectory : Env.MESSoftwareDistributionRoot;
//            return Path.Combine(rootPath, package.PackageFolder ? package.Name : "");
//        }

//        private Package[] GetPackagesOffline(IEnumerable<XElement> xPackages, bool waitForExecution, out List<FileInfo> executeFiles, out List<FileInfo> topLevelSequences, bool withFiles)
//        {
//            xPackages = xPackages.Where(e => bool.Parse(e.Attribute("Installed").Value)).ToList();
//            var packages = xPackages.Select(e => new Package
//            {
//                PackageId = Guid.Parse(e.Attribute("PackageId").Value),
//                Name = e.Attribute("Name").Value,
//                Version = int.Parse(e.Attribute("Version").Value),
//                PackageFolder = bool.Parse(e.Attribute("PackageFolder").Value),
//                RootDirectory = e.Attribute("RootDirectory").Value,
//                DownloadSize = long.Parse(e.Attribute("DownloadSize").Value),
//                Description = e.Attribute("Description").Value,
//                Status = int.Parse(e.Attribute("Status").Value),
//                Tags = e.Element("Tags").Value,
//                Priority = -1
//            }).OrderBy(p => p.Name).ToArray();

//            if (withFiles)
//            {
//                var xFiles = xPackages.SelectMany(e =>
//                {
//                    string rootPath = GetRootPath(packages.Single(p => p.PackageId == Guid.Parse(e.Attribute("PackageId").Value)));
//                    return e.Descendants("File").Select(f => new { xFile = f, rootPath = rootPath });
//                }).ToList();

//                executeFiles = xFiles.Where(e => HasFileAttribute(e.xFile, FileAttribute.ExecuteAlways)).Select(e => new FileInfo(Path.Combine(e.rootPath, e.xFile.Attribute("Path").Value))).ToList();
//                topLevelSequences = xFiles.Where(e => HasFileAttribute(e.xFile, FileAttribute.TopLevelFile)).Select(e => new FileInfo(Path.Combine(e.rootPath, e.xFile.Attribute("Path").Value))).ToList();

//                foreach (var file in executeFiles)
//                    ExecuteFile(file, waitForExecution);
//            }
//            else
//            {
//                executeFiles = null;
//                topLevelSequences = null;
//            }

//            return packages;

//            bool HasFileAttribute(XElement e, FileAttribute fileAttribute)
//            {
//                return ((FileAttribute)Enum.Parse(typeof(FileAttribute), e.Attribute("Attributes").Value)).HasFlag(fileAttribute);
//            }
//        }

//        private void ExecuteFile(FileInfo file, bool waitForExecution)
//        {
//            try
//            {
//                file.Refresh();
//                if (file.Exists)
//                {
//                    using (System.Diagnostics.Process p = System.Diagnostics.Process.Start(file.FullName))
//                    {
//                        if (waitForExecution && p != null)
//                            p.WaitForExit();
//                    }
//                }            
//            }
//            catch (Exception ex) { Env.LogException(ex, "Error in Execute file"); }
//        }
//    }
//}
