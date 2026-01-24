using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS.Client.PackageManager.Converters
{
    public static class Extensions
    {
        public static string FormatBytes(this long bytes)
        {
            const int scale = 1024;
            string[] orders = new string[] { "GB", "MB", "KB", "B " };
            long max = (long)Math.Pow(scale, orders.Length - 1);

            foreach (string order in orders)
            {
                if (bytes > max)
                    return string.Format("{0:#.0} {1}", bytes / max, order);

                max /= scale;
            }
            return "0.0 B ";
        }
    }
}
