using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Interface
{
    static class Common
    {

        internal static DateTime parseDateTime(string date, bool useTime)
        {
            //012345678901234
            //20081210_123047
            int year = int.Parse(date.Substring(0, 4));
            int month = int.Parse(date.Substring(4, 2));
            int day = int.Parse(date.Substring(6, 2));
            int hour = 0;
            int min = 0;
            int sec = 0;
            if (useTime)
            {
                hour = int.Parse(date.Substring(9, 2));
                min = int.Parse(date.Substring(11, 2));
                sec = int.Parse(date.Substring(13, 2));
            }
            return new DateTime(year, month, day, hour, min, sec, 0, DateTimeKind.Unspecified);
        }

        internal static bool EnumTryParse<T>(string strType, out T result)
        {
            if (string.IsNullOrEmpty(strType)) { result = default(T); return false; }
            string strTypeFixed = strType.Replace(' ', '_');
            if (Enum.IsDefined(typeof(T), strTypeFixed))
            {
                result = (T)Enum.Parse(typeof(T), strTypeFixed, true);
                return true;
            }
            else
            {
                foreach (string value in Enum.GetNames(typeof(T)))
                {
                    if (value.Equals(strTypeFixed, StringComparison.OrdinalIgnoreCase))
                    {
                        result = (T)Enum.Parse(typeof(T), value);
                        return true;
                    }
                }
                result = default(T);
                return false;
            }
        }

    }
}
