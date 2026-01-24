extern alias newclientapi;

using System;

namespace Virinco.WATS.Configuration
{
    public class CommonUserSettings
    {
        internal newclientapi::Virinco.WATS.Configuration.CommonUserSettings _instance;
        internal CommonUserSettings(newclientapi::Virinco.WATS.Configuration.CommonUserSettings settings)
        {
            this._instance = settings;
        }

        public string FullName
        {
            get => _instance.FullName;
            set => _instance.FullName = value;
        }
        public string CultureCode
        {
            get => _instance.CultureCode;
            set => _instance.CultureCode = value;
        }

        /// <summary>
        /// This is only a getter. MemberShipUser stores the value
        /// </summary>
        public string Email
        {
            get => _instance.Email;
            set => _instance.Email = value;
        }

        /// <summary>
        /// This is only a getter. RoleProvider stores the value
        /// </summary>
        public string[] Roles
        {
            get => _instance.Roles;
            set => _instance.Roles = value;
        }

        public TimeSpan DefaultFromDate
        {
            get => _instance.DefaultFromDate;
            set => _instance.DefaultFromDate = value;
        }

        public long DefaultFromDateTicks
        {
            get => _instance.DefaultFromDateTicks;
            set => _instance.DefaultFromDateTicks = value;
        }


        /// <summary>
        /// 0=Hierarchical,1=Flat
        /// </summary>
        public int SNH_DefaultReportStyle
        {
            get => _instance.SNH_DefaultReportStyle;
            set => _instance.SNH_DefaultReportStyle = value;
        }


        public string[] Levels
        {
            get => _instance.Levels;
            set => _instance.Levels = value;
        }

        public string[] ProductGroups
        {
            get => _instance.ProductGroups;
            set => _instance.ProductGroups = value;
        }
    }

}