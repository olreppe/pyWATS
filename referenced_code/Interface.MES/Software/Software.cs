extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using napict = newclientapi::Virinco.WATS.Service.MES.Contract;
using System.Collections.Generic;
using Virinco.WATS.Service.MES.Contract;
using System.Linq;
using System.IO;

namespace Virinco.WATS.Interface.MES.Software
{
    /// <summary>
    /// Class to handle software distribution
    /// </summary>
    public class Software : MesBase
    {
        private napi.Software.Software _instance;

        internal Software(napi.Software.Software software)
        {
            this._instance = software;
        }

        public new bool isConnected() => _instance.isConnected();

        /// <summary>
        /// Returns an array of revoked packages matching the tags. All package versions are included
        /// </summary>
        /// <param name="tagNames">Array of tags</param>
        /// <param name="tagValues">Array of tag values matching index of the tagnames array</param>   
        /// <param name="SelectedPackage">The selected package (from GUI)</param>
        /// <param name="Continue">True if a package is selected (from Gui)</param>
        /// <param name="ExecuteFiles">Array of executable files in selected package</param>
        /// <param name="TopLevelSequences">Array of toplevelsequencefiles in selected package</param>
        /// <returns>Matching Packages</returns>  
        public Package[] GetRevokedPackages(string[] tagNames, string[] tagValues, out Package SelectedPackage, out bool Continue, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences)
        {
            napict.Package selectedPackage;
            var res = _instance.GetRevokedPackages(tagNames, tagValues, out selectedPackage, out Continue, out ExecuteFiles, out TopLevelSequences);
            SelectedPackage = new Package(selectedPackage);
            return res.Select(i => new Package(i)).ToArray();
        }

        /// <summary>
        /// Get Package by default tags. Default value (null) will skip tag.
        /// </summary>
        /// <param name="PartNumber">Tagged with a given PartNumber</param>
        /// <param name="Process">Tagged with a given Process</param>
        /// <param name="StationType">Tagged with a given StationType</param>
        /// <param name="Revision">Tagged with a given Revision</param>
        /// <param name="StationName">Tagged with a given Staion Name</param>
        /// <param name="Misc">Tagged with a given Misc value</param>        
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package[] GetPackages(string PartNumber = null, string Process = null, string StationType = null, string Revision = null/*, string Site = null*/, string StationName = null, string Misc = null, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
            => _instance.GetPackages(PartNumber, Process, StationType, Revision, StationName, Misc, Install, DisplayProgress, WaitForExecution, (napict.StatusEnum)(int)PackageStatus)
                .Select(i => new Package(i)).ToArray();

        /// <summary>
        /// Get an array of Packages.
        /// </summary>
        /// <param name="XPath">Return Packages with a Tag matching the XPath</param>
        /// <param name="ExecuteFiles">List of files beeing executed</param>
        /// <param name="TopLevelSequences">List of toplevel sequences</param>
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package[] GetPackagesByTag(string XPath, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
            => _instance.GetPackagesByTag(XPath, out ExecuteFiles, out TopLevelSequences, Install, DisplayProgress, WaitForExecution, (napict.StatusEnum)(int)PackageStatus)
                .Select(i => new Package(i)).ToArray();

        /// <summary>
        /// Get an array of Packages.
        /// </summary>
        /// <param name="XPath">Return Packages with a Tag matching the XPath</param>
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package[] GetPackagesByTag(string XPath, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
            => _instance.GetPackagesByTag(XPath, Install, DisplayProgress, WaitForExecution, (napict.StatusEnum)(int)PackageStatus)
                .Select(i => new Package(i)).ToArray();

        /// <summary>
        /// Returns Packages matching a dictionary of Tag/Values.
        /// </summary>
        /// <param name="TagValue"></param>
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package[] GetPackagesByTag(Dictionary<string, string> TagValue, bool Install, bool DisplayProgress, bool WaitForExecution, StatusEnum PackageStatus = StatusEnum.Released)
            => _instance.GetPackagesByTag(TagValue, Install, DisplayProgress, WaitForExecution, (napict.StatusEnum)(int)PackageStatus)
                .Select(i => new Package(i)).ToArray();

        /// <summary>
        /// Returns Packages matching array of Tag/Values.
        /// </summary>
        /// <param name="tagNames">Array of tags to match (the tag value should be located on identical index in the tagValues array)</param>
        /// <param name="tagValues">Array of tagvalues to match (the tag name should be placed on the identical index in the tagNames array)</param>
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="ExecuteFiles">List of files beeing executed</param>
        /// <param name="TopLevelSequences">List of toplevel sequences</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package[] GetPackagesByTag(string[] tagNames, string[] tagValues, bool Install, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, StatusEnum PackageStatus = StatusEnum.Released)
            => _instance.GetPackagesByTag(tagNames, tagValues, Install, DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences, (napict.StatusEnum)(int)PackageStatus)
                .Select(i => new Package(i)).ToArray();

        /// <summary>
        /// Returns Packages matching a dictionary of Tag/Values.
        /// </summary>
        /// <param name="TagValue"></param>
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="ExecuteFiles">List of files beeing executed</param>
        /// <param name="TopLevelSequences">List of toplevel sequences</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package[] GetPackagesByTag(Dictionary<string, string> TagValue, bool Install, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, StatusEnum PackageStatus = StatusEnum.Released)
            => _instance.GetPackagesByTag(TagValue, Install, DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences, (napict.StatusEnum)(int)PackageStatus)
                .Select(i => new Package(i)).ToArray();

        /// <summary>
        /// Get Packages with a given name.
        /// </summary>
        /// <param name="PackageName">Name of Package</param>
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="ExecuteFiles">List of files beeing executed</param>
        /// <param name="TopLevelSequences">List of toplevel sequences</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package GetPackageByName(string PackageName, bool Install, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences, StatusEnum PackageStatus = StatusEnum.Released)
            => new Package(_instance.GetPackageByName(PackageName, Install, DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences, (napict.StatusEnum)(int)PackageStatus));

        /// <summary>
        /// Get Packages with a given name
        /// </summary>
        /// <param name="PackageName">Name of Package</param>
        /// <param name="Install">Install Package?</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="PackageStatus">Status of package to get</param>
        /// <returns></returns>
        public Package GetPackageByName(string PackageName, bool Install = true, bool DisplayProgress = true, bool WaitForExecution = true, StatusEnum PackageStatus = StatusEnum.Released)
            => new Package(_instance.GetPackageByName(PackageName, Install, DisplayProgress, WaitForExecution, (napict.StatusEnum)(int)PackageStatus));

        /// <summary>
        /// Install an array of Packages. Getting files to filesystem and executing files being marked for execution
        /// </summary>
        /// <param name="packages">Packages to install</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finish</param>
        /// <param name="ExecuteFiles">List of files being tagged for execution</param>
        /// <param name="TopLevelSequences">List of files being tagged as top level sequence</param>
        public void InstallPackage(Package[] packages, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences)
            => _instance.InstallPackage(packages.Select(p => p._instance).ToArray(), DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences);

        /// <summary>
        /// Install an array of Packages. Getting files to filesystem and executing files being marked for execution
        /// </summary>
        /// <param name="packages">Packages to install</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        public void InstallPackage(Package[] packages, bool DisplayProgress, bool WaitForExecution)
            => _instance.InstallPackage(packages.Select(p => p._instance).ToArray(), DisplayProgress, WaitForExecution);

        /// <summary>
        /// Install a given package (overwriting modified files). Getting files to filesystem and executing files being marked for execution
        /// </summary>
        /// <param name="package">Package to install</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        /// <param name="ExecuteFiles">List of files beeing tagged for execution</param>
        /// <param name="TopLevelSequences">List of files being tagged as top level sequence</param>
        public void InstallPackage(Package package, bool DisplayProgress, bool WaitForExecution, out List<FileInfo> ExecuteFiles, out List<FileInfo> TopLevelSequences)
            => _instance.InstallPackage(package._instance, DisplayProgress, WaitForExecution, out ExecuteFiles, out TopLevelSequences);

        /// <summary>
        /// Install a given package (overwriting modified files). 
        /// </summary>
        /// <param name="package">Package to install</param>
        /// <param name="DisplayProgress">Display a progressbar when files are downloaded</param>
        /// <param name="WaitForExecution">Wait for for executed files to finsish</param>
        public void InstallPackage(Package package, bool DisplayProgress, bool WaitForExecution)
            => _instance.InstallPackage(package._instance, DisplayProgress, WaitForExecution);

        /// <summary>
        /// Set path to local software root folder, where packages will be installed.
        /// </summary>
        /// <param name="rootFolderPath">
        /// <para>Path to the new folder packages will be installed into. Must be an absolute path, and should be an empty folder.</para>
        /// <para>NB! Existing files in the folder may be overwritten by packages.</para></param>
        /// <param name="moveExistingPackages">
        /// <para>
        /// Choose to move packages files to the new folder. 
        /// May fail if folder or file with same name as a package already exists in the new folder.
        /// If files are not moved, installed packages will stop working until they are reinstalled.
        /// </para>
        /// <para>NB! If the current root folder does not only contain packages, those files will also be moved.</para>
        /// </param>
        public static void SetRootFolderPath(string rootFolderPath, bool moveExistingPackages = true)
            => napi.Software.Software.SetRootFolderPath(rootFolderPath, moveExistingPackages);

        /// <summary>
        /// Returns the local Root Folder path where software packages are installed
        /// </summary>
        /// <returns></returns>
        public static string GetRootFolderPath()
            => napi.Software.Software.GetRootFolderPath();

        /// <summary>
        /// Method to clean file distribution root folder
        /// </summary>
        /// <param name="PromptOperator">Display a OK/Cancel dialog</param>
        public void DeleteAllPackages(bool PromptOperator = true)
            => _instance.DeleteAllPackages(PromptOperator);

        /// <summary>
        /// Delete revoked packages. 
        /// Only revoked packages without a released version are deleted (packages without a new released verison)
        /// </summary>
        /// <param name="PromptOperator">Display a OK/Cancel dialog</param>
        public void DeleteRevokedPackages(bool PromptOperator = true)
            => _instance?.DeleteRevokedPackages(PromptOperator);

        /// <summary>
        /// Check server for new version of installed packages
        /// </summary>
        /// <param name="PackagesAvailable">boolean value if new packages exists</param>
        /// <returns>Array of available packages</returns>
        public Package[] GetAvailablePackages(out bool PackagesAvailable)
            => _instance.GetAvailablePackages(out PackagesAvailable).Select(p => new Package(p)).ToArray();

    }
}
