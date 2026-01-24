using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Sub part information
    /// </summary>
    public class UUTPartInfo
    {
        ReportUnitHierarchy_type partRow;
        UUTReport report;

        internal UUTPartInfo(ReportUnitHierarchy_type pr, UUTReport uut)
        {
            partRow = pr;
            report = uut;
        }

        internal UUTPartInfo(PartInfo_type pt, UUTReport uut)
        {
            partRow = new ReportUnitHierarchy_type
            {
                Idx = pt.idx,
                IdxSpecified = pt.idxSpecified,
                PartType = pt.PartType,
                PN = pt.PN,
                SN = pt.SN,
                Rev = pt.Rev
            };

            //Add the new ruh instead so that edits are saved
            uut.reportRow.Items.Remove(pt);
            uut.reportRow.Items.Add(partRow);

            report = uut;
        }

        /// <summary>
        /// Type of subpart
        /// </summary>
        public string PartType
        {
            get { return partRow.PartType; }
            set { partRow.PartType = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("PartType", value); }
        }

        /// <summary>
        /// Part number of subpart
        /// </summary>
        public string PartNumber
        {
            get { return partRow.PN; }
            set { partRow.PN = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("PN", value,"PartNumber"); }
        }

        /// <summary>
        /// Sub parts serial number
        /// </summary>
        public string SerialNumber
        {
            get { return partRow.SN; }
            set { partRow.SN = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("SN", value,"SerialNumber"); }
        }

        /// <summary>
        /// Sub part revision number
        /// </summary>
        public string PartRevisionNumber
        {
            get { return partRow.Rev; }
            set { partRow.Rev = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("Rev", value,"PartRevisionNumber"); }
        }
    }

}
