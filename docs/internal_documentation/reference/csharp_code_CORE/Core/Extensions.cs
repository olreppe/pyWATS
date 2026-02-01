using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;

namespace Virinco.WATS
{
    public static class Extensions
    {
        public static Int32? ToInt32(this string source)
        {
            Int32 value;
            if (Int32.TryParse(source, out value)) return value;
            else return null;
        }
        public static Int32 ToInt32(this string source, Int32 defaultValue)
        {
            Int32.TryParse(source, out defaultValue);
            return defaultValue;
        }


        public static Int16? ToInt16(this string source)
        {
            Int16 value;
            if (Int16.TryParse(source, out value)) return value;
            else return null;
        }
        public static Int16 ToInt16(this string source, Int16 defaultValue)
        {
            Int16.TryParse(source, out defaultValue);
            return defaultValue;
        }
        public static Double? ToDouble(this string source)
        {
            Double value;
            if (Double.TryParse(source, out value)) return value;
            else return null;
        }
        public static Double ToDouble(this string source, Double defaultValue)
        {
            Double.TryParse(source, out defaultValue);
            return defaultValue;
        }

        public static bool? ToBool(this string source)
        {
            bool value;
            int iValue;
            if (bool.TryParse(source, out value)) return value;
            else if (int.TryParse(source, out iValue)) return iValue != 0;
            else return null;
        }
        public static bool ToBool(this string source, bool defaultValue)
        {
            bool? value=source.ToBool();
            return value.HasValue ? value.Value : defaultValue;
        }


        public static DateTime? ToDateTime(this string source)
        {
            DateTime value;
            if (DateTime.TryParse(source, out value)) return value;
            else return null;
        }
        public static DateTime ToDateTime(this string source, DateTime defaultValue)
        {
            DateTime.TryParse(source, out defaultValue);
            return defaultValue;
        }

        public static string Truncate(this string source, int length)
        {
            if (source?.Length > length)
                source = source.Substring(0, length);
            return source;
        }

        public static WebResponse GetResponseWithoutException(this WebRequest request)
        {
            if (request == null)
            {
                throw new ArgumentNullException("request");
            }

            try
            {
                return request.GetResponse();
            }
            catch (WebException e)
            {
                if (e.Response == null)
                {
                    throw;
                }

                return e.Response;
            }
        }

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

        /*
        public static string GetErrors(this System.Data.DataSet ds, int MaxLines)
        {
            System.Text.StringBuilder sb = new System.Text.StringBuilder();
            if (ds == null) return null;
            foreach (System.Data.DataTable tbl in ds.Tables)
            {
                if (tbl.HasErrors)
                {
                    int rowno = 0;
                    foreach (System.Data.DataRow row in tbl.Rows)
                    {
                        if (!string.IsNullOrEmpty(row.RowError))
                        {
                            sb.AppendFormat("T[{0}]R[{1}]:{2}\n", tbl.TableName, rowno, row.RowError);
                            MaxLines--;
                        }
                        if (MaxLines == 0) break;
                        foreach (System.Data.DataColumn col in row.GetColumnsInError())
                        {
                            sb.AppendFormat("T[{0}]R[{1}]C[{2}]:{3}\n", tbl.TableName, rowno, col.ColumnName, row.GetColumnError(col));
                            MaxLines--;
                            if (MaxLines == 0) break;
                        }
                        if (MaxLines == 0) break;
                        rowno++;
                    }
                    if (MaxLines == 0) break;
                }
            }
            return sb.ToString();
        }
        */
    }
}
