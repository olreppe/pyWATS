using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml.Linq;
using System.Xml.XPath;

namespace Virinco.WATS.Interface
{

    /// <summary>
    /// A repair type is a set of fail-codes. e.g. Module Repair has a different set of failcodes than System Repair
    /// </summary>
    public class RepairType
    {
        internal Models.Process process;
        internal Models.RepairType repairtype;
        internal RepairType(Models.Process process)
        {
            this.process = process;
            this.repairtype=process.Properties as Models.RepairType;
        }

        /// <remarks>Code of repair type</remarks>
        public Int16 Code
        {
            get { return process.Code; }
        }
        /// <remarks>Name of repair type</remarks>
        public string Name
        {
            get { return process.Name; }
        }
        /// <remarks>Description of repair type</remarks>
        public string Description
        {
            get { return process.Description; }
        }

        /// <summary>
        /// Repair type identifier
        /// </summary>
        public Guid Id
        {
            get { return process.ProcessID; }
        }

        /// <summary>
        /// True if repair type requires an UUT Id
        /// </summary>
        public bool UUTRequired
        {
            get
            {
                return repairtype!=null?repairtype.UUTRequired == 0:false;
            }
        }
        /// <summary>
        /// A regular expression that validates a  valid component reference
        /// </summary>
        public string ComponentReferenceMask
        {
            get
            {
                return repairtype != null ? repairtype.CompRefMask : string.Empty;
            }
        }

        /// <summary>
        /// Description of a ComponentReferenceMask
        /// </summary>
        public string ComponentReferenceMaskDescription
        {
            get
            {
                return repairtype != null ? repairtype.CompRefMaskDescription : string.Empty;
            }
        }
    }

    //internal class RepairTypes
    //{
    //    private Models.Process process;

    //    private Codes.RepairtypeDataTable repairTypesTable;
    //    private Codes.ProcessDataTable processTable;
    //    private RepairType[] repairTypesArray = null;
    //    internal RepairTypes(Codes codes)
    //    {
    //        repairTypesTable = codes.Repairtype;
    //        processTable = codes.Process;
    //    }

    //    internal RepairType[] GetRepairTypes()
    //    {
    //        if (repairTypesArray != null)
    //            return repairTypesArray;
    //        //Construct array from table
    //        if (repairTypesTable.Count > 0)
    //        {
    //            List<RepairType> r = new List<RepairType>();
    //            foreach (Codes.ProcessRow p in processTable.Rows)
    //            {
    //                if (!p.IsRepairOperation) continue; // skip non-repair processes
    //                if (p.State != 1) continue; // skip inactive and deleted
    //                Int16 pCode;
    //                if (!Int16.TryParse(p.Code, out pCode)) continue; // Skip repairprocesses with invalid codes.
    //                XElement props = p.IsPropertiesNull()?null:System.Xml.Linq.XDocument.Parse(p.Properties).Root;
    //                Codes.RepairtypeRow rtr = repairTypesTable.Where(s => s.GUID == p.GUID).SingleOrDefault();
    //                RepairType rt = new RepairType()
    //                {
    //                    Id = p.GUID,
    //                    LcId = rtr == null ? 0 : rtr.RT_LCID,
    //                    Code = pCode,
    //                    Name = p.Name,
    //                    Description = p.Description,
    //                    Properties = props
    //                };
    //                r.Add(rt);
                    
    //            }
    //            /*
    //            var r = from rt in repairTypesTable
    //                    where rt.Status != 2
    //                    select new RepairType() { Id = rt.GUID, LcId = rt.RT_LCID, Description = rt.Description, UUTRequired = rt.UUTRequired == 0 ? false : true, ComponentReferenceMask = rt.CompRefMask, ComponentReferenceMaskDescription = rt.CompRefMaskDescription };
    //            */
    //            repairTypesArray = r.ToArray();
    //            return repairTypesArray;
    //        }
    //        else
    //            return null;
    //    }
    //    internal static bool TryParseElementBool(XElement element, XName elementname, out bool value)
    //    {
    //        XElement el = element.Element(elementname);
    //        if (el != null)
    //            return Boolean.TryParse(el.Value, out value);
    //        else { value = false; return false; }
    //    }
    //    internal static bool TryParseElementString(XElement element, XName elementname, out string value)
    //    {
    //        XElement el = element.Element(elementname);
    //        if (el != null) { value = el.Value; return true; }
    //        else { value = null; return false; }
    //    }
    //}
}
