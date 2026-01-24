using System;

namespace Virinco.WATS.Configuration
{
    public class CommonUserSettings
    {
        public string FullName { get; set; }
        public string CultureCode { get; set; }

        /// <summary>
        /// This is only a getter. MemberShipUser stores the value
        /// </summary>
        public string Email { get; set; }

        /// <summary>
        /// This is only a getter. RoleProvider stores the value
        /// </summary>
        public string[] Roles { get; set; }

        public TimeSpan DefaultFromDate { get; set; }

        public long DefaultFromDateTicks
        {
            get { return DefaultFromDate.Ticks; }
            set { DefaultFromDate = new TimeSpan(value); }
        }



        /// <summary>
        /// 0=Hierarchical,1=Flat
        /// </summary>
        public int SNH_DefaultReportStyle { get; set; }


        public string[] Levels { get; set; }

        public string[] ProductGroups { get; set; }
    }

}