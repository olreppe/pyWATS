extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Virinco.WATS.Interface.MES.Production
{

    public class UnitHistory
    {
        private napi.Production.UnitHistory _instance;

        internal UnitHistory(napi.Production.UnitHistory instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Unit serial number.
        /// </summary>
        public string SN
        {
            get => _instance.SN;
            set => _instance.SN = value;
        }

        /// <summary>
        /// Unit part number.
        /// </summary>
        public string PN
        {
            get => _instance.PN;
            set => _instance.PN = value;
        }

        /// <summary>
        /// Unit revision.
        /// </summary>
        public string Revision
        {
            get => _instance.Revision;
            set => _instance.Revision = value;
        }

        /// <summary>
        /// Unit type, Unit or Subunit.
        /// </summary>
        public string Level
        {
            get => _instance.Level;
            set => _instance.Level = value;
        }

        /// <summary>
        /// The process the unit was in.
        /// </summary>
        public string Process
        {
            get => _instance.Process;
            set => _instance.Process = value;
        }

        /// <summary>
        /// The status the unit had.
        /// </summary>
        public string Status
        {
            get => _instance.Status;
            set => _instance.Status = value;
        }


        /// <summary>
        /// <c>true</c> if this change was forced by a user.
        /// </summary>
        public bool Forced
        {
            get => _instance.Forced;
            set => _instance.Forced = value;
        }

        /// <summary>
        /// Id to a report, if the change was because of test or repair.
        /// </summary>
        public Guid? ReportId
        {
            get => _instance.ReportId;
            set => _instance.ReportId = value;
        }

        /// <summary>
        /// If unit has report, this is the station name in the report.
        /// </summary>
        public string StationName
        {
            get => _instance.StationName;
            set => _instance.StationName = value;
        }

        /// <summary>
        /// If unit has report, this is the location in the report.
        /// </summary>
        public string Location
        {
            get => _instance.Location;
            set => _instance.Location = value;
        }

        /// <summary>
        /// If unit has report, this is the purpose in the report.
        /// </summary>
        public string Purpose
        {
            get => _instance.Purpose;
            set => _instance.Purpose = value;
        }

        /// <summary>
        /// If unit has report, this is the operator in the report.
        /// </summary>
        public string Operator
        {
            get => _instance.Operator;
            set => _instance.Operator = value;
        }

        /// <summary>
        /// Date and time of when the change happened.
        /// </summary>
        public DateTime StartUtc
        {
            get => _instance.StartUtc;
            set => _instance.StartUtc = value;
        }

        /// <summary>
        /// If unit has report, this is when the test or repair ended.
        /// </summary>
        public DateTime? EndUtc
        {
            get => _instance.EndUtc;
            set => _instance.EndUtc = value;
        }

        /// <summary>
        /// If details is <c>true</c>, a list of info and error messages.
        /// </summary>
        public IEnumerable<UnitReportHistoryDetails> Details
        {
            get => _instance.Details.Select(i => new UnitReportHistoryDetails(i));
            set => _instance.Details = value.Select(i => i._instance).ToList();
        }
    }

    public class UnitReportHistoryDetails
    {
        internal napi.Production.UnitReportHistoryDetails _instance;

        internal UnitReportHistoryDetails(napi.Production.UnitReportHistoryDetails instance)
        {
            _instance = instance;
        }

        public string Info
        {
            get => _instance.Info;
            set => _instance.Info = value;
        }

        public string Error
        {
            get => _instance.Error;
            set => _instance.Error = value;
        }

    }

}
