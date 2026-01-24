using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Xml.Linq;
using Virinco.WATS;

namespace Virinco.WATS.Client.PackageManager
{
    class Utils
    {

        public static int CheckInterval
        {
            get
            {
                try
                {
                    return Int32.Parse(ConfigFile?.Root?.Attribute("Interval")?.Value);
                }
                catch { }
                return 86400;
            }
            set
            {
                try
                {
                    XDocument cfg = ConfigFile;
                    cfg.Root.Attribute("Interval").Value = value.ToString();
                    cfg.Save(packageTagsXml);
                }
                catch { }
            }
        }

        public static bool AllowConfiguration
        {
            get
            {
                try
                {
                    return Boolean.Parse(ConfigFile?.Root?.Attribute("AllowConfiguration")?.Value);
                }
                catch { }
                return false;
            }
        }

        public static bool BringToFront
        {
            get
            {
                try
                {
                    return Boolean.Parse(ConfigFile?.Root?.Attribute("BringToFront")?.Value);
                }
                catch { }
                return true;
            }
            set
            {
                try
                {
                    XDocument cfg = ConfigFile;

                    if (cfg?.Root?.Attribute("BringToFront") == null)
                        cfg.Root.Add(new XAttribute("BringToFront", value));
                    else
                        cfg.Root.Attribute("BringToFront").Value = value.ToString();

                    cfg.Save(packageTagsXml);
                }
                catch { }
            }
        }

        public static int PackageStatus
        {
            get
            {
                try
                {
                    return Int32.Parse(ConfigFile?.Root?.Attribute("PackageStatus")?.Value);
                }
                catch { }
                return 2;
            }
            set
            {
                try
                {
                    XDocument cfg = ConfigFile;
                    cfg.Root.Attribute("PackageStatus").Value = value.ToString();
                    cfg.Save(packageTagsXml);
                }
                catch { }
            }
        }

        public static bool DeleteRevokedPackages
        {
            get
            {
                try
                {
                    return Boolean.Parse(ConfigFile?.Root?.Attribute("DeleteRevokedPackages")?.Value);
                }
                catch { }
                return true;
            }
        }

        public static string getFilter(/*out List<string> tagNames, out List<string> tagValues*/)
        {
            //tagNames = new List<string>();
            //tagValues = new List<string>();
            string filter = "";
            try
            {
                string packageTagsXml = System.IO.Path.Combine(Env.MESSoftwareDistributionRoot, "DownloadManager.xml");

                string tmp = ConfigFile.Descendants("Filter")?.First()?.Value;
                if (!string.IsNullOrEmpty(tmp))
                    filter = tmp;


                //var res = from t in ConfigFile.Descendants("Tag")
                //          select new
                //          {
                //              name = t.Attribute("Name").Value,
                //              value = t.Attribute("Value").Value
                //          };

                //foreach (var o in res)
                //{
                //    tagNames.Add(o.name.Trim());
                //    tagValues.Add(o.value.Trim());
                //}

            }
            catch (Exception ex) { Env.LogException(ex, "Error in getFilter"); }
            return filter;

        }



        /*
         
         PartNumber=123|234|456 OR Misc=12|34
         StationName=ST1|ST2 OR StationName=Any
         OR
         PartNumber=223|224|226 OR Misc=22|33
         
where Tags.exist( '//*[ PartNumber[.="5555000055"] or PartNumber[.="5555000066"]]  [StationName[.="main-source.wats.no" or .="Any"]]' ) = 0x1

where Tags.exist( '//*[ StationName[.="main-source.wats.nso" or .="LDCT2-P1C"] or Misc[.="misc" or .="misc2"] ] ' ) = 0x1

         */

        public static string getXpath()
        {
            return getXpath(getFilter());
        }
        public static string getXpath(string filter)
        {
            if (string.IsNullOrEmpty(filter))
                return "//*";

            string machineName = Environment.MachineName;
            filter = Regex.Replace(filter, "<StationName>", machineName, RegexOptions.IgnoreCase);


            string XPath = "//*[";
            
            
            //for (int i = 0; i < tagNames.Length; i++)
            //{
            //    string tag = tagNames[i];
            //    string value = tagValues.Length > i ? tagValues[i] : "";


            //    if (!string.IsNullOrEmpty(tag) && value != null)
            //    {
            //        if (tag == "StationName")
            //            XPath += string.Format("[{0}[.=\"{1}\" or .=\"Any\"]] ", tag, value);
            //        else
            //            XPath += string.Format("[{0}[.=\"{1}\"]] ", tag, value);
            //    }
            //}


            //string[] groups = filter.Split(new string[] { $"{Environment.NewLine}OR" }, StringSplitOptions.RemoveEmptyEntries);

            string[] groups = Regex.Split(filter, @";\s*OR\s*;");//,RegexOptions. filter.Split(new string[] { $"{Environment.NewLine}OR" }, StringSplitOptions.RemoveEmptyEntries);

            int groupIdx = 0;
            foreach (string group in groups)
            {
                XPath += "(";

                string[] lines = group.Split(new string[] { ";" }, StringSplitOptions.RemoveEmptyEntries);
                foreach (string line in lines)
                {                    
                        XPath += "(";    
                string[] tags = Regex.Split(line, @"\s+OR\s+",RegexOptions.IgnoreCase);  //line.Split(new string[] { " OR " }, StringSplitOptions.RemoveEmptyEntries);


                    foreach (string tag in tags)
                    {

                        string[] tmp = tag.Split(new string[] { "=" }, StringSplitOptions.RemoveEmptyEntries);

                        string name = tmp.Length > 0 ? tmp[0].Trim() : "";
                        string value = tmp.Length > 1 ? tmp[1].Trim() : "";

                        if (!(string.IsNullOrEmpty(name) || string.IsNullOrEmpty(value)))
                        {

                            XPath += $"{name}[";
                           tmp = value.Split(new string[] { "|" }, StringSplitOptions.RemoveEmptyEntries);

                            foreach (string v in tmp)
                            {

                                XPath += $".=\"{v}\" or ";
                                //names.Add(name);
                                //values.Add(v);
                            }
                            //remoce last or
                            XPath = XPath.Remove(XPath.Length - 4);

                            if (name == "StationName")
                                XPath += string.Format(" or .=\"Any\"", tag, value);

                            XPath += "] or ";
                        }
                    }
                    //remoce last or
                    XPath = XPath.Remove(XPath.Length - 4);

                    XPath += ") and ";

                }
                //remove last and
                XPath = XPath.Remove(XPath.Length - 5);


                groupIdx++;

                XPath += ") or ";
            }
            
            //remove last or
            XPath = XPath.Remove(XPath.Length - 4);
            XPath += "]";

            return XPath;
        }
        public static void saveFilter(string filter)
        {
            try
            {

                ////*[ PartNumber[.="5555000055"] or PartNumber[.="5555000066"]]  [StationName[.="main-source.wats.no" or .="Any"]]

                XDocument cfg = ConfigFile;
                XElement xFilter = cfg.Descendants("Filter").FirstOrDefault();
                if (xFilter == null)
                {
                    xFilter = new XElement("Filter");
                    cfg.Root.Add(xFilter);
                }
                xFilter.RemoveAll();

                xFilter.Value = filter;

                //XElement tags = cfg.Descendants("Tags").FirstOrDefault();
                //if (tags == null)
                //{
                //    tags = new XElement("Tags");
                //    cfg.Root.Add(tags);
                //}
                //tags.RemoveAll();
                //for (int i = 0; i < tagNames.Count; i++)
                //{
                //    string tag = tagNames[i];
                //    string value = tagValues.Count > i ? tagValues[i] : "";
                //    if (!string.IsNullOrEmpty(tag) && value != null)
                //    {
                //        tags.Add(new XElement("Tag",
                //                    new XAttribute("Name", tag.Trim()),
                //                    new XAttribute("Value", value.Trim())
                //                ));
                //    }
                //}
                cfg.Save(packageTagsXml);

            }
            catch (Exception ex) { Env.LogException(ex, "Error in saveFilter"); }
        }

        static string packageTagsXml = Env.GetConfigFilePath(Env.DownloadManagerFileName);
        public static XDocument ConfigFile
        {
            get
            {
                if (!System.IO.File.Exists(packageTagsXml))
                {
                    XElement xml = new XElement("DownloadManager", 
                        new XAttribute("Interval", 86400), 
                        new XAttribute("PackageStatus", 2),
                        new XAttribute("AllowConfiguration", true), 
                        new XAttribute("DeleteRevokedPackages", true), 
                        new XAttribute("BringToFront", true),
                        new XElement("Filter", "StationName=<StationName>;")
                    );

                    if (!Directory.Exists(Path.GetDirectoryName(packageTagsXml)))
                        Directory.CreateDirectory(Path.GetDirectoryName(packageTagsXml));
                    xml.Save(packageTagsXml);
                }
                return XDocument.Load(packageTagsXml);
            }
        }

       
    }
}
