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
    public class UURPartInfo
    {
        UURReport report;
        ReportUnitHierarchy_type partRow;

        internal UURPartInfo(UURReport uurReport, ReportUnitHierarchy_type pr)
        {
            this.partRow = pr;
            this.report = uurReport;
        }

        /// <summary>
        /// Part type of subpart
        /// </summary>
        public string PartType
        {
            get { return partRow.PartType; }
            set { partRow.PartType = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("PartType", value, "PartType"); }
        }

        /// <summary>
        /// Part number of subpart
        /// </summary>
        public string PartNumber
        {
            get { return partRow.PN; }
            set { partRow.PN = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("PN",value,"PartNumber"); }
        }

        /// <summary>
        /// Sub parts serial number
        /// </summary>
        public string SerialNumber
        {
            get { return partRow.SN; }
            set { partRow.SN = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("SN", value, "SerialNumber"); }
        }

        /// <summary>
        /// Sub part revision number
        /// </summary>
        public string PartRevisionNumber
        {
            get { return partRow.Rev; }
            set { partRow.Rev = report.api.SetPropertyValidated<ReportUnitHierarchy_type>("Rev", value, "PartRevisionNumber"); }
        }

        /// <summary>
        /// Index of subpart, Index 0 has to have SN/PN as main main unit
        /// </summary>
        public int PartIndex
        {
            get { return partRow.Idx; }
        }

        /// <summary>
        /// Parent index of subpart
        /// </summary>
        public int ParentIDX
        {
            get { return partRow.ParentIDX; }
            set { partRow.ParentIDX = value; }
        }


        /// <summary>
        /// If given, this subpart replaces the part with this index
        /// </summary>
        public int ReplacedIDX
        {
            get { return partRow.ReplacedIDX; }
            set { partRow.ReplacedIDX = value; }
        }

        private List<Failure> failures=new List<Failure>();
        /// <summary>
        /// Adds a failure the repaired unit
        /// </summary>
        /// <param name="failCode"></param>
        /// <param name="componentReference"></param>
        /// <param name="comment"></param>
        /// <param name="stepOrderNumber"></param>
        public Failure AddFailure(FailCode failCode, string componentReference, string comment, int stepOrderNumber)
        {
            Failure f = report.AddFailure(failCode, componentReference,partRow.Idx);
            f.ComponentReference = componentReference;
            f.Comment = comment;
            f.FailedStepOrderNumber = stepOrderNumber;
            f.PartIndex = partRow.Idx;
            failures.Add(f);
            return f;
        }

        /// <summary>
        /// Returns an array of failures to a part
        /// </summary>
        public Failure[] Failures
        {
            get
            {
                return failures.ToArray<Failure>();
            }
        }

    }
}
