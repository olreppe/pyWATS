extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Sub part information
    /// </summary>
    public class UURPartInfo
    {
        internal napi.UURPartInfo _instance;
        internal UURPartInfo(napi.UURPartInfo instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Part type of subpart
        /// </summary>
        public string PartType
        {
            get => _instance.PartType;
            set => _instance.PartType = value;
        }

        /// <summary>
        /// Part number of subpart
        /// </summary>
        public string PartNumber
        {
            get => _instance.PartNumber;
            set => _instance.PartNumber = value;
        }

        /// <summary>
        /// Sub parts serial number
        /// </summary>
        public string SerialNumber
        {
            get => _instance.SerialNumber;
            set => _instance.SerialNumber = value;
        }

        /// <summary>
        /// Sub part revision number
        /// </summary>
        public string PartRevisionNumber
        {
            get => _instance.PartRevisionNumber;
            set => _instance.PartRevisionNumber = value;
        }

        /// <summary>
        /// Index of subpart, Index 0 has to have SN/PN as main main unit
        /// </summary>
        public int PartIndex // r/o
        {
            get => _instance.PartIndex;
        }

        /// <summary>
        /// Parent index of subpart
        /// </summary>
        public int ParentIDX
        {
            get => _instance.ParentIDX;
            set => _instance.ParentIDX = value;
        }


        /// <summary>
        /// If given, this subpart replaces the part with this index
        /// </summary>
        public int ReplacedIDX
        {
            get => _instance.ReplacedIDX;
            set => _instance.ReplacedIDX = value;
        }

        private List<Failure> failures = new List<Failure>();
        /// <summary>
        /// Adds a failure the repaired unit
        /// </summary>
        /// <param name="failCode"></param>
        /// <param name="componentReference"></param>
        /// <param name="comment"></param>
        /// <param name="stepOrderNumber"></param>
        public Failure AddFailure(FailCode failCode, string componentReference, string comment, int stepOrderNumber)
            => new Failure(_instance.AddFailure(failCode._instance, componentReference, comment, stepOrderNumber));

        /// <summary>
        /// Returns an array of failures to a part
        /// </summary>
        public Failure[] Failures // r/o
        {
            get => _instance.Failures.Select(f => new Failure(f)).ToArray();
        }
    }
}
