using System;
using System.Linq;
using System.Collections;
using System.Web;
using System.Text.RegularExpressions;
using System.IO;
using System.Xml.Serialization;
using System.Collections.Generic;
using System.IO.Compression;
using System.Text;
using System.Diagnostics;
using System.ComponentModel.DataAnnotations;
using System.Security.AccessControl;
using System.Security.Principal;
using System.Runtime.Versioning;

namespace Virinco.WATS
{
    public static class Utilities
    {
        /*
        public static string sqlCSVStatus(int StatusBitmap)
        {
            ArrayList al = new ArrayList();
            if ((StatusBitmap & (int)StatusType.Passed) != 0x00) al.Add("Passed");
            if ((StatusBitmap & (int)StatusType.Done) != 0x00) al.Add("Done");
            if ((StatusBitmap & (int)StatusType.Failed) != 0x00) al.Add("Failed");
            if ((StatusBitmap & (int)StatusType.Terminated) != 0x00) al.Add("Terminated");
            if ((StatusBitmap & (int)StatusType.Skipped) != 0x00) al.Add("Skipped");
            if ((StatusBitmap & (int)StatusType.Error) != 0x00) al.Add("Error");
            return string.Join(",", (string[])al.ToArray(typeof(string)));
        }

        public static string EnumValueToString(Type enumType, object value)
        {
            if (!enumType.IsEnum)
                return string.Empty;
            return Enum.GetName(enumType, value);
        }

        public static IEnumerable<T> EnumValuesAsIEnumerable<T>()
        {
            return typeof(T)
            .GetFields()
            .Where(x => x.IsLiteral)
            .Select(field => (T)field.GetValue(null));
        }
        
        /// <summary>
        /// Converts object to Int32, or returns defaultValue if conversion fails.
        /// Avoid using this implementation if possible (uses exception catch)
        /// </summary>
        /// <param name="obj">an object possibly containing an Int32 convertible...</param>
        /// <param name="defaultValue">Default value returned if conversion fails.</param>
        /// <returns>Converted value or default value.</returns>
        public static Int32 ParseInt32(object obj, Int32 defaultValue)
        {
            try { return System.Convert.ToInt32(obj); }
            catch { return defaultValue; }
        }
        */
        /// <summary>
        /// Converts object to Int32, or returns defaultValue if conversion is impossible.
        /// </summary>
        /// <param name="value">String containing integer value</param>
        /// <param name="defaultValue">Value returned if conversion is impossible</param>
        /// <returns>Converted value</returns>
        public static Int32 ParseInt32(object value, Int32 defaultValue)
        {
            if (value is int) return (int)value;
            if (value != null) return value.ToString().ToInt32(defaultValue);
            else return defaultValue;
        }
        /*
        public static Int32? ParseNInt32(string value)
        {
            Int32 ret;
            if (Int32.TryParse(value, out ret)) return ret;
            else return null;
        }

        public static Int64 ParseInt64(object obj, Int64 defaultValue)
        {
            try { return System.Convert.ToInt64(obj); }
            catch { return defaultValue; }
        }
        public static Int64 ParseInt64(string value, Int64 defaultValue)
        {
            Int64 ret;
            if (Int64.TryParse(value, out ret)) return ret;
            else return defaultValue;
        }
        public static Int64? ParseNInt64(string value)
        {
            Int64 ret;
            if (Int64.TryParse(value, out ret)) return ret;
            else return null;
        }
        */

        public static Double ParseDouble(object value, Double defaultValue)
        {
            if (value is Double) return (Double)value;
            if (value is int) return (int)value;
            if (value != null) return value.ToString().ToDouble(defaultValue);
            else return defaultValue;
        }
        /*
        public static System.Data.SqlTypes.SqlDouble ParseSQL2005Float(double numeric_value)
        {
            if (double.IsInfinity(numeric_value) || double.IsNaN(numeric_value)) return System.Data.SqlTypes.SqlDouble.Null; // Invalid SqlDouble
            else if ((BitConverter.ToUInt16(BitConverter.GetBytes(numeric_value), 6) & 0x7FF0) == 0x00) return 0; // Denormal number...
            else return new System.Data.SqlTypes.SqlDouble(numeric_value);
        }

        public static SQL2005FloatState GetSQL2005FloatState(double numeric_value)
        {
            if (double.IsNegativeInfinity(numeric_value)) return SQL2005FloatState.NegativeInfinity;
            else if (double.IsPositiveInfinity(numeric_value)) return SQL2005FloatState.PositiveInfinity;
            else if (double.IsNaN(numeric_value)) return SQL2005FloatState.NaN;
            else if ((BitConverter.ToUInt16(BitConverter.GetBytes(numeric_value), 6) & 0x7FF0) == 0x00) return SQL2005FloatState.DeNormal;
            else return SQL2005FloatState.Normal;
        }

        internal static bool TryParseSQL2005Float(string numeric_string, out System.Data.SqlTypes.SqlDouble dblvalue, out SQL2005FloatState state)
        {
            double numeric_value;
            bool isvalid;
            if (double.TryParse(numeric_string, out numeric_value))
            {
                isvalid = TryParseSQL2005Float(numeric_value, out dblvalue, out state);
            }
            else
            {
                dblvalue = System.Data.SqlTypes.SqlDouble.Null;
                state = SQL2005FloatState.NaN;
                isvalid = false;
            }
            return isvalid;
        }

        internal static bool Double_IsDenormalized(double numeric_value)
        {
            long value = BitConverter.DoubleToInt64Bits(numeric_value);
            if (((value & 0x7FF0000000000000) == 0x0000000000000000) && ((value & 0x000FFFFFFFFFFFFF) != 0x0000000000000000))
                return false; // Denormalized
            else
                return true; // !Denormalized
        }

        internal static bool TryParseSQL2005Float(double numeric_value, out System.Data.SqlTypes.SqlDouble dblvalue, out SQL2005FloatState state)
        {
            bool isvalid;
            if (double.IsNegativeInfinity(numeric_value)) { dblvalue = System.Data.SqlTypes.SqlDouble.Null; state = SQL2005FloatState.NegativeInfinity; isvalid = false; }
            else if (double.IsPositiveInfinity(numeric_value)) { dblvalue = System.Data.SqlTypes.SqlDouble.Null; state = SQL2005FloatState.PositiveInfinity; isvalid = false; }
            else if (double.IsNaN(numeric_value)) { dblvalue = System.Data.SqlTypes.SqlDouble.Null; state = SQL2005FloatState.NaN; isvalid = false; }
            else if (Double_IsDenormalized(numeric_value)) { dblvalue = new System.Data.SqlTypes.SqlDouble(numeric_value); state = SQL2005FloatState.DeNormal; isvalid = false; }
            else { dblvalue = new System.Data.SqlTypes.SqlDouble(numeric_value); state = SQL2005FloatState.Normal; isvalid = true; }
            return isvalid;
        }
        */
        /*
        public static DateTime? ParseDateTime(string value)
        {
            DateTime result;
            if (DateTime.TryParse(value, out result)) return result;
            else return null;
        }*/
        public static DateTime ParseDateTime(object value, DateTime defaultValue)
        {
            if (value is DateTime) return (DateTime)value;
            if (value != null) return value.ToString().ToDateTime(defaultValue);
            else return defaultValue;
        }

        public static bool ParseBool(object value, bool defaultValue)
        {
            if (value is bool) return (bool)value;
            if (value is int) return (int)value != 0;
            if (value != null) return value.ToString().ToBool(defaultValue);
            else return defaultValue;
        }
        /*
        public static Int16 ParseInt16(object obj, Int16 defaultValue)
        {
            try { return System.Convert.ToInt16(obj); }
            catch { return defaultValue; }
        }
        */

        static private Regex _invalidXMLChars = new Regex(
            // Filters control characters but allows only properly-formed surrogate sequences
            @"(?<![\uD800-\uDBFF])[\uDC00-\uDFFF]|[\uD800-\uDBFF](?![\uDC00-\uDFFF])|[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F\uFEFF\uFFFE\uFFFF]",
            RegexOptions.Compiled);

        public static string ReplaceInvalidXmlCharacters(string s, string replace_value)
        {            
            return s == null || string.IsNullOrEmpty(s) ? "" : _invalidXMLChars.Replace(s, replace_value);
        }

        public static int GetMaxLengthFromAttribute<Type>(string propertyName)
        {
            StringLengthAttribute strLenAttr = typeof(Type).GetProperty(propertyName).GetCustomAttributes(typeof(StringLengthAttribute), false).Cast<StringLengthAttribute>().SingleOrDefault();
            if (strLenAttr != null)
                return strLenAttr.MaximumLength;
            else
                return 0;
        }


        public static Guid ParseGuid(object obj, Guid defaultValue)
        {
            //Type objtype = source.GetType();
            try
            {
                if (obj is Guid) return (Guid)obj;
                else if (obj is string) return new Guid((string)obj);
                else if (obj is byte[]) return new Guid((byte[])obj);
                else return defaultValue;
            }
            catch { return defaultValue; }
        }
        /*
        public static Guid? ParseNGuid(string value)
        {
            Guid ret;
            if (GuidTryParse(value, out ret)) return ret;
            else return null;
        }
        */
        public static bool GuidTryParse(string s, out Guid result)
        {

            if (s == null) { result = Guid.Empty; return false; }
            Regex format = new Regex(
                "^[A-Fa-f0-9]{32}$|" +
                "^({|\\()?[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12}(}|\\))?$|" +
                "^({)?[0xA-Fa-f0-9]{3,10}(, {0,1}[0xA-Fa-f0-9]{3,6}){2}, {0,1}({)([0xA-Fa-f0-9]{3,4}, {0,1}){7}[0xA-Fa-f0-9]{3,4}(}})$");
            Match match = format.Match(s);
            if (match.Success)
            {
                result = new Guid(s);
                return true;
            }
            else
            {
                result = Guid.Empty;
                return false;
            }
        }
        /*
        public static Guid ToGuid(object source)
        {
            try
            {
                if (source.GetType() == typeof(Guid)) return (Guid)source;
                else if (source.GetType() == typeof(String)) return new Guid((string)source);
                else return new Guid((byte[])source);
            }
            catch { return Guid.Empty; }
        }

        public static object Convert(object value, Type type, object DefaultValue)
        {
            try { return System.Convert.ChangeType(value, type); }
            catch { return DefaultValue; }
        }

        public static string HtmlStatusColorCode(StatusType StatusCode)
        {
            System.Drawing.Color col = StatusColorCode(StatusCode);
            return String.Format("#{0:x2}{1:x2}{2:x2}", col.R, col.G, col.B);
        }

        public static System.Drawing.Color StatusColorCode(StatusType StatusCode)
        {
            switch (StatusCode)
            {
                case StatusType.Passed: return System.Drawing.Color.FromArgb(0x00, 0xff, 0x00);
                case StatusType.Failed: return System.Drawing.Color.FromArgb(0xff, 0x00, 0x00);
                case StatusType.Terminated: return System.Drawing.Color.FromArgb(0x00, 0x00, 0xff);
                case StatusType.Error: return System.Drawing.Color.FromArgb(0xff, 0x99, 0x00);
                case StatusType.Done: return System.Drawing.Color.FromArgb(0x00, 0xff, 0xcc);
                case StatusType.Skipped: return System.Drawing.Color.FromArgb(0xff, 0xff, 0x00);
                default: return System.Drawing.Color.FromArgb(0xff, 0xff, 0xff);
            }
        }

        public static StatusType ParseStatusText(string StatusText)
        {
            StatusType status;
            if (!EnumTryParse<StatusType>(StatusText, out status)) status = StatusType.Unknown;
            return status;
        }

        public static System.Drawing.Color GetStatusColor(string status)
        {
            return Virinco.WATS.Utilities.StatusColorCode(Virinco.WATS.Utilities.ParseStatusText(status));
        }
        */
        public static bool EnumTryParse<T>(string strType, out T result)
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

        public static string GetCompOpText(string CompOp)
        {
            switch (CompOp.ToUpper())
            {
                case "EQ": return "EQ (==)";
                case "EQUAL": return "EQ (==)";
                case "NE": return "NE (!=)";
                case "GT": return "GT (>)";
                case "LT": return "LT (<)";
                case "GE": return "GE (>=)";
                case "LE": return "LE (<=)";
                case "GTLT": return "GTLT (> AND <)";
                case "GELE": return "GELE (>= AND <=)";
                case "GELT": return "GELT(>= AND <)";
                case "GTLE": return "GTLE (> AND <=)";
                case "LTGT": return "LTGT (< OR >)";
                case "LEGE": return "LEGE (<= OR >=)";
                case "LEGT": return "LEGT(<= OR >)";
                case "LTGE": return "LTGE (< OR >=)";
                case "LOG": return "No Comparison";
                case "LOG DATA": return "No Comparison";
                case "CASESENSIT": return "Case Sensitive";
                case "IGNORECASE": return "Ignore Case";
                case "REGEX": return "Regular Expression";
                default: return "NONE";
            }
        }
        /*
        public static StepTypeEnum ParseStepType(string steptypetext)
        {
            try { return (StepTypeEnum)Enum.Parse(typeof(StepTypeEnum), steptypetext, true); }
            catch { return StepTypeEnum.Unknown; }
        }

        public static StepGroupEnum ParseStepGroup(string stepgrouptext)
        {
            try { return (StepGroupEnum)Enum.Parse(typeof(StepGroupEnum), stepgrouptext, true); }
            catch { return StepGroupEnum.Unknown; }
        }

        public static string GetStepTypeDescription(StepTypeEnum steptype)
        {
            switch (steptype)
            {
                case StepTypeEnum.SequenceCall: return "Sequence call";
                case StepTypeEnum.NumericLimitTest: return "Numeric limit test";
                case StepTypeEnum.ET_NLT: return "Numeric limit test";
                case StepTypeEnum.ET_MNLT: return "Multiple numeric limit test";
                case StepTypeEnum.PassFailTest: return "Pass/Fail test";
                case StepTypeEnum.ET_PFT: return "Pass/Fail test";
                case StepTypeEnum.ET_MPFT: return "Multiple Pass/Fail test";
                case StepTypeEnum.StringValueTest: return "String-value test";
                case StepTypeEnum.ET_SVT: return "String-value test";
                case StepTypeEnum.ET_MSVT: return "Multiple string-value test";
                case StepTypeEnum.Action: return "Action";
                case StepTypeEnum.ET_A: return "Action";
                case StepTypeEnum.CallExecutable: return "Call executable";
                case StepTypeEnum.MessagePopup: return "Message popup";
                case StepTypeEnum.NI_VariableAndPropertyLoader: return "Property loader";
                case StepTypeEnum.NI_Wait: return "Wait";
                case StepTypeEnum.Unknown: return "Unknown step type";
                default: return "Undefined step type";
            }
        }

        public static string AsterixToLikeSearch(string search)
        {
            string src = search.Trim();
            if (src.StartsWith("*")) src = "%" + src.Substring(1);
            if (src.EndsWith("*")) src = src.Substring(0, src.Length - 1) + "%";
            return src;
        }

        public static void SetStringRowValueTruncateOnOverflow(System.Data.DataRow row, System.Data.DataColumn column, string value, int MaxLength)
        {
            if (value.Length <= MaxLength) row[column] = value;
            else row[column] = value.Substring(0, MaxLength);
        }
        public static void SetStringRowValueTruncateOnOverflow(System.Data.DataRow row, System.Data.DataColumn column, string value)
        {
            SetStringRowValueTruncateOnOverflow(row, column, value, column.MaxLength);
        }
 */

        public static string SerializeToString<T>(T obj)
        {
            StringWriter sw = new StringWriter();

            System.Xml.XmlWriterSettings xws = new System.Xml.XmlWriterSettings();
            xws.Indent = false;

            System.Xml.XmlWriter wr = System.Xml.XmlWriter.Create(sw, xws);
            XmlSerializer serializer = new XmlSerializer(typeof(T));
            serializer.Serialize(wr, obj);
            return sw.ToString();
        }

        public static T DeSerializeFromString<T>(string obj)
        {
            StringReader sw = new StringReader(obj);

            XmlSerializer serializer = new XmlSerializer(typeof(T));
            return (T)serializer.Deserialize(sw);
        }

        public static string Compress(this string value)
        {
            if (value != null && value.Length > 400) // between 300-400 before compression rate is good enough
            {
                var buffer = Encoding.UTF8.GetBytes(value);
                var memoryStream = new MemoryStream();
                using (var gZipStream = new GZipStream(memoryStream, CompressionMode.Compress, true))
                {
                    gZipStream.Write(buffer, 0, buffer.Length);
                }
                memoryStream.Position = 0;
                var compressedData = new byte[memoryStream.Length];
                memoryStream.Read(compressedData, 0, compressedData.Length);
                var gZipBuffer = new byte[compressedData.Length + 4];
                Buffer.BlockCopy(compressedData, 0, gZipBuffer, 4, compressedData.Length);
                Buffer.BlockCopy(BitConverter.GetBytes(buffer.Length), 0, gZipBuffer, 0, 4);
                return Convert.ToBase64String(gZipBuffer);
            }
            return value;
        }

        public static string Decompress(this string value, bool emptyValueAllowed = false)
        {
            if (!emptyValueAllowed && value == string.Empty)
                value = null;
            var isBase64String = (value != null && value.Length % 4 == 0) && Regex.IsMatch(value, @"^[a-zA-Z0-9\+/]*={0,3}$", RegexOptions.None);
            if (isBase64String)
            {
                try
                {
                    var gZipBuffer = Convert.FromBase64String(value);
                    using (var memoryStream = new MemoryStream())
                    {
                        var dataLength = BitConverter.ToInt32(gZipBuffer, 0);
                        memoryStream.Write(gZipBuffer, 4, gZipBuffer.Length - 4);
                        var buffer = new byte[dataLength];
                        memoryStream.Position = 0;
                        using (var gZipStream = new GZipStream(memoryStream, CompressionMode.Decompress))
                        {
                            gZipStream.Read(buffer, 0, buffer.Length);
                        }
                        return Encoding.UTF8.GetString(buffer);
                    }
                }
                catch { }
            }
            return value;
        }

        public static Process UnsafeOpenFileInSystemDefaultProgram(string filepath)
        {
            System.Diagnostics.ProcessStartInfo psi = new(filepath) { UseShellExecute = true };
            var p = System.Diagnostics.Process.Start(psi);
            return p;
        }

        public static Process OpenFileInSystemDefaultProgram(string filepath)
        {
            try
            {
                var p = UnsafeOpenFileInSystemDefaultProgram(filepath);
                return p;
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Failed to open file: {filepath}");
                return null;
            }
        }

        public static Process UnsafeOpenUrlInSystemDefaultProgram(string url)
        {
            System.Diagnostics.ProcessStartInfo psi = new(url) { UseShellExecute = true };
            var p = System.Diagnostics.Process.Start(psi);
            return p;
        }

        public static Process OpenUrlInSystemDefaultProgram(string url)
        {
            try
            {
                var p = UnsafeOpenUrlInSystemDefaultProgram(url);
                return p;
            }
            catch (Exception e)
            {
                Env.LogException(e, $"Failed to open url: {url}");
                return null;
            }
        }

        public static string GetMSIVersionString(Version version)
        {
            return $"{version.Major}.{version.Minor}.{version.Revision}";
        }

        /*


        public static string SerializeToBinaryString<T>(T obj)
        {
            using (Stream fStream = new System.IO.MemoryStream())
            {
                System.Runtime.Serialization.IFormatter bfmtr = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
                bfmtr.Serialize(fStream, obj);
                fStream.Position = 0;
                using (StreamReader reader = new StreamReader(fStream))
                {
                    return reader.ReadToEnd();
                }
            }
        }

        public static T DeSerializeFromBinaryString<T>(string obj)
        {         
            using (Stream fStream = new System.IO.MemoryStream())
            {
                using (StreamWriter writer = new StreamWriter(fStream))
                {
                    writer.Write(obj);
                    writer.Flush();
                }

                fStream.Position = 0;
                System.Runtime.Serialization.IFormatter bfmtr = new System.Runtime.Serialization.Formatters.Binary.BinaryFormatter();
                return (T)bfmtr.Deserialize(fStream);
            }
        }
    }
    */
        /*
        public class MeasIdentifier
        {
            private void LoadStateBag(string ModifiedBase64)
            {
                byte[] bArr = System.Convert.FromBase64String(ModifiedBase64.Replace("!", "/").Replace("_", "=").Replace("-", "+"));
                ss_lcid = System.BitConverter.ToInt32(bArr, 0);
                LoopIndex = System.BitConverter.ToInt32(bArr, 4);
                Grouping = System.BitConverter.ToInt32(bArr, 8);
                MeasName = System.Text.UTF8Encoding.ASCII.GetString(bArr, 12, bArr.Length - 12);
            }

            public string GetModifiedBase64()
            {
                byte[] baMeasName = System.Text.UTF8Encoding.ASCII.GetBytes(MeasName);
                byte[] bArr = new byte[baMeasName.Length + 12];
                Array.Copy(System.BitConverter.GetBytes(ss_lcid), 0, bArr, 0, 4);
                Array.Copy(System.BitConverter.GetBytes(LoopIndex), 0, bArr, 4, 4);
                Array.Copy(System.BitConverter.GetBytes(Grouping), 0, bArr, 8, 4);
                Array.Copy(baMeasName, 0, bArr, 12, baMeasName.Length);
                return System.Convert.ToBase64String(bArr).Replace("/", "!").Replace("=", "_").Replace("+", "-");
            }
            public MeasIdentifier(int ss_lcid, int LoopIndex, string MeasName)
            {
                this.ss_lcid = ss_lcid;
                this.LoopIndex = LoopIndex;
                this.MeasName = MeasName;
            }
            public MeasIdentifier(int ss_lcid, int LoopIndex, string MeasName, int Grouping)
            {
                this.ss_lcid = ss_lcid;
                this.LoopIndex = LoopIndex;
                this.MeasName = MeasName;
                this.Grouping = Grouping;
            }
            public MeasIdentifier(string ModifiedBase64)
            {
                LoadStateBag(ModifiedBase64);
            }
            public int ss_lcid = -1;
            public int LoopIndex = -1;
            public string MeasName = "";
            public int Grouping = -1;
        */


#if NET8_0_OR_GREATER
        [SupportedOSPlatform("windows")]
#endif
        internal static void SetModifyControlPermissionsToEveryone(string path)
        {
            const FileSystemRights rights = FileSystemRights.Modify;

            var allUsers = new SecurityIdentifier(WellKnownSidType.BuiltinUsersSid, null);

            // Add Access Rule to the actual directory itself
            var accessRule = new FileSystemAccessRule(
                allUsers,
                rights,
                InheritanceFlags.None,
                PropagationFlags.NoPropagateInherit,
                AccessControlType.Allow);

            var info = new DirectoryInfo(path);
            var security = info.GetAccessControl(AccessControlSections.Access);

            bool result;
            security.ModifyAccessRule(AccessControlModification.Set, accessRule, out result);

            if (!result)
            {
                throw new InvalidOperationException("Failed to give full-control permission to all users for path " + path);
            }

            // add inheritance
            var inheritedAccessRule = new FileSystemAccessRule(
                allUsers,
                rights,
                InheritanceFlags.ContainerInherit | InheritanceFlags.ObjectInherit,
                PropagationFlags.InheritOnly,
                AccessControlType.Allow);

            bool inheritedResult;
            security.ModifyAccessRule(AccessControlModification.Add, inheritedAccessRule, out inheritedResult);

            if (!inheritedResult)
            {
                throw new InvalidOperationException("Failed to give full-control permission inheritance to all users for " + path);
            }

            info.SetAccessControl(security);
        }
    }
}
