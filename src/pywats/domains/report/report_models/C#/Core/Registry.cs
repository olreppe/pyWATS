using System;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Text;
/*
 This file is beeing shared between WATS_TestStand_Support (dll) and WATS-Core (dll)
 * Make sure it compiles in both projects before checking in changes to this file!
 */
namespace Virinco.WATS
{
    public class Registry
    {
        const string WATSRegistryPath = "SOFTWARE\\Virinco\\WATS";

        private static UIntPtr HKEY_LOCAL_MACHINE = new UIntPtr(0x80000002u);
        private static UIntPtr HKEY_CURRENT_USER = new UIntPtr(0x80000001u);
        private const int KEY_QUERY_VALUE = 0x1;
        private const int KEY_ALL_ACCESS = 0xf003f;
        private const int KEY_SET_VALUE = 0x2;
        private const int KEY_CREATE_SUB_KEY = 0x4;
        private const int KEY_ENUMERATE_SUB_KEYS = 0x8;
        private const int KEY_NOTIFY = 0x10;
        private const int KEY_CREATE_LINK = 0x20;
        private const int KEY_WOW64_32KEY = 0x200;
        private const int KEY_WOW64_64KEY = 0x100;
        private const int KEY_WOW64_RES = 0x300;
        private const int REG_OPTION_NON_VOLATILE = 0x0;


        [DllImport("advapi32.dll", CharSet = CharSet.Auto)]
        public static extern int RegOpenKeyEx(UIntPtr hKey, string subKey, int ulOptions, int samDesired, out UIntPtr hkResult);

        enum RegistryDispositionValue : uint
        {
            REG_CREATED_NEW_KEY = 0x00000001,
            REG_OPENED_EXISTING_KEY = 0x00000002
        }
        [DllImport("advapi32.dll", SetLastError = true)]
        private static extern int RegCreateKeyEx(
                           UIntPtr hKey,
                           string lpSubKey,
                           uint reserved,
                           string lpClass,
                           uint dwOptions,
                           int samDesired,
                           UIntPtr lpSecurityAttributes,
                           out UIntPtr phkResult,
                           out RegistryDispositionValue lpdwDisposition);

        [DllImport("advapi32.dll", SetLastError = true, EntryPoint = "RegSetValueEx")]
        private static extern int RegSetValueEx_Str(UIntPtr hKey, [MarshalAs(UnmanagedType.LPStr)] string lpValueName, int Reserved, Microsoft.Win32.RegistryValueKind dwType, [MarshalAs(UnmanagedType.LPStr)] string lpData, int cbData);
        [DllImport("advapi32.dll", SetLastError = true, EntryPoint = "RegSetValueEx")]
        private static extern int RegSetValueEx_Bin(UIntPtr hKey, [MarshalAs(UnmanagedType.LPStr)] string lpValueName, int Reserved, Microsoft.Win32.RegistryValueKind dwType, byte[] lpData, int cbData);

        [DllImport("advapi32.dll", SetLastError = true, EntryPoint = "RegQueryValueEx")]
        public static extern int RegQueryValueEx_Bin(UIntPtr hKey, string lpValueName, int lpReserved, out uint lpType, byte[] lpData, ref int lpcbData);
        [DllImport("advapi32.dll", SetLastError = true, EntryPoint = "RegQueryValueEx")]
        public static extern int RegQueryValueEx_Str(UIntPtr hKey, string lpValueName, int lpReserved, out uint lpType, StringBuilder lpData, ref int lpcbData);

        [DllImport("advapi32.dll", SetLastError = true)]
        public static extern int RegCloseKey(UIntPtr hKey);

        public static string GetWATSRegistryValue(string keyName, string defaultValue)
        {
            try
            {
                return GetWATSRegistryValue(keyName);
            }
            catch { return defaultValue; }
        }

        private static long RegGetCreateWATSKey(out UIntPtr keyHandle, bool readOnly)
        {
            RegistryDispositionValue lpdwDisposition;            
            if (readOnly)
                return RegCreateKeyEx(HKEY_LOCAL_MACHINE, WATSRegistryPath, 0, null, REG_OPTION_NON_VOLATILE, KEY_QUERY_VALUE | KEY_WOW64_64KEY, UIntPtr.Zero, out keyHandle, out lpdwDisposition);
            else
                return RegCreateKeyEx(HKEY_LOCAL_MACHINE, WATSRegistryPath, 0, null, REG_OPTION_NON_VOLATILE, KEY_ALL_ACCESS| KEY_WOW64_64KEY, UIntPtr.Zero, out keyHandle, out lpdwDisposition);
        }

        public static string GetWATSRegistryValue(string keyName)
        {
            string regValue = "";
            //using (System.IO.StreamWriter writer = new System.IO.StreamWriter("c:\\debug.txt", true))
            //{
                //writer.WriteLine("{0:s};Starting getregistryvalue", DateTime.Now);
                //writer.WriteLine("\t;Get '{0}'", keyName);
                Microsoft.Win32.RegistryKey key = null;
                try
                {
                    //writer.WriteLine("\t;ProcessType='{0}'", ProcessType);

                    //TODO: Replace P/Invoke with RegistryKey.OpenBaseKey (.Net 4.0) when WATS-Core is upgraded to .Net 4.0
                    if (ProcessType == ProcessTypeEnum.w32on64) // Process is 32bit on 64bit OS; must use P/Invoke to read from 64bit Hive...
                    {
                        UIntPtr keyHandle;
                    long result = RegGetCreateWATSKey(out keyHandle,true);
                        if (result != 0) throw new ApplicationException("OpenSubKey: Cannot open key " + WATSRegistryPath);
                        try
                        {
                            int valuelength = 0;
                            uint valuetype;
                            result = RegQueryValueEx_Str(keyHandle, keyName, 0, out valuetype, null, ref valuelength);
                            if (result == 0)
                            {
                                StringBuilder sb = new StringBuilder(valuelength);
                                result = RegQueryValueEx_Str(keyHandle, keyName, 0, out valuetype, sb, ref valuelength);
                                if (result == 0) regValue = sb.ToString();
                            }
                        }
                        finally
                        {
                            result = RegCloseKey(keyHandle);
                        }
                    }
                    else // Either 32on32 or 64on64, use Normal Managed code to access default registry hive
                    {
                        //writer.WriteLine("\t;Using managed code");
                        key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(WATSRegistryPath, false);
                        if (key != null)
                        {
                            object o = key.GetValue(keyName);
                            regValue = o == null ? null : o.ToString();
                        }
                        else
                        {
                            throw new ApplicationException("OpenSubKey: Cannot open key " + WATSRegistryPath);
                        }
                    }
                }
                finally
                {
                    if (key != null) key.Close();
                }
            //    writer.WriteLine("{0:s};getregistryvalue done, Data:{1}", DateTime.Now,regValue);
            //}
            return regValue;
        }


        public static Guid GetWATSRegistryGuidValue(string keyName, Guid defaultValue)
        {
            try
            {
                return GetWATSRegistryGuidValue(keyName);
            }
            catch { return defaultValue; }
        }

        public static Guid GetWATSRegistryGuidValue(string keyName)
        {
            byte[] regValue = null;
            Microsoft.Win32.RegistryKey key = null;
            try
            {
                if (ProcessType == ProcessTypeEnum.w32on64) // Process is 32bit on 64bit OS; must use P/Invoke to read from 64bit Hive...
                {
                    UIntPtr keyHandle;
                    long result = RegGetCreateWATSKey(out keyHandle,true);
                    if (result != 0) throw new ApplicationException("OpenSubKey: Cannot open key " + WATSRegistryPath);
                    try
                    {
                        int valuelength = 0;
                        uint valuetype;
                        result = RegQueryValueEx_Bin(keyHandle, keyName, 0, out valuetype, null, ref valuelength);
                        if (result == 0)
                        {
                            regValue = new byte[valuelength];
                            result = RegQueryValueEx_Bin(keyHandle, keyName, 0, out valuetype, regValue, ref valuelength);
                            if (result != 0) regValue = null;
                        }
                    }
                    finally
                    {
                        result = RegCloseKey(keyHandle);
                    }
                }
                else // Either 32on32 or 64on64, use Normal Managed code to access default registry hive
                {
                    key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(WATSRegistryPath, false);
                    if (key != null)
                    {
                        regValue = (byte[])key.GetValue(keyName);
                    }
                    else
                    {
                        throw new ApplicationException("OpenSubKey: Cannot open key " + WATSRegistryPath);
                    }
                }
            }            
            finally
            {
                if (key != null) key.Close();
            }
            return (regValue == null) ? Guid.Empty : new Guid(regValue);
        }

        public static void SetWATSRegistryValue(string keyName, string stringValue)
        {
            if (ProcessType == ProcessTypeEnum.w32on64) // Process is 32bit on 64bit OS; must use P/Invoke to read from 64bit Hive...
            {
                UIntPtr keyHandle;
                long result = RegGetCreateWATSKey(out keyHandle,false);
                if (result == 0)
                {
                    try
                    {
                        int t = RegSetValueEx_Str(keyHandle, keyName, 0, Microsoft.Win32.RegistryValueKind.String, stringValue, stringValue.Length);
                    }
                    finally
                    {
                        result = RegCloseKey(keyHandle);
                    }
                }
            }
            else // Either 32on32 or 64on64, use Normal Managed code to access default registry hive
            {
                Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(WATSRegistryPath, true);
                if (key == null)
                    key = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(WATSRegistryPath);
                if (key != null)
                {
                    key.SetValue(keyName, stringValue);
                }
                key.Close();
            }
        }

        public static void SetWATSRegistryValue(string keyName, Guid regValue)
        {
            if (ProcessType == ProcessTypeEnum.w32on64) // Process is 32bit on 64bit OS; must use P/Invoke to read from 64bit Hive...
            {
                UIntPtr keyHandle;
                long result = RegGetCreateWATSKey(out keyHandle,false);
                if (result == 0)
                {
                    try
                    {
                        RegSetValueEx_Bin(keyHandle, keyName, 0, Microsoft.Win32.RegistryValueKind.String, regValue.ToByteArray(), 0);
                    }
                    finally
                    {
                        result = RegCloseKey(keyHandle);
                    }
                }
            }
            else // Either 32on32 or 64on64, use Normal Managed code to access default registry hive
            {
                Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(WATSRegistryPath, true);
                if (key == null)
                    key = Microsoft.Win32.Registry.LocalMachine.CreateSubKey(WATSRegistryPath);
                if (key != null)
                {
                    key.SetValue(keyName, regValue.ToByteArray());
                }
                key.Close();
            }
        }

        public enum ProcessTypeEnum { Unknown, w32on32, w32on64, w64on64 }
        private static ProcessTypeEnum _processtype;
        [DllImport("kernel32.dll", SetLastError = true, CallingConvention = CallingConvention.Winapi)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool IsWow64Process([In] IntPtr hProcess, [Out] out bool wow64Process);

        public static ProcessTypeEnum ProcessType
        {
            get
            {
                if (_processtype == ProcessTypeEnum.Unknown)
                {
                    if (IntPtr.Size == 8) _processtype = ProcessTypeEnum.w64on64;
                    else
                    {
                        using (Process p = Process.GetCurrentProcess())
                        {
                            bool retVal;
                            if (IsWow64Process(p.Handle, out retVal))
                                _processtype = retVal ? ProcessTypeEnum.w32on64 : ProcessTypeEnum.w32on32;
                            else
                                _processtype = ProcessTypeEnum.w32on32;
                        }
                    }
                }
                return _processtype;
            }
        }
        /// <summary>
        /// Read 32bit value from HKLM Registry hive
        /// 32on32: Use normal regread
        /// 32on64: Use normal regread (opens wow-node)
        /// 64on64: Use p/invoke to open 32bit registry hive
        /// </summary>
        /// <param name="regkey"></param>
        /// <param name="p"></param>
        /// <param name="regValue"></param>
        /// <returns></returns>
        public static bool TryReadHKLM32Value(string regkey, string keyName, out string regValue)
        {
            if (ProcessType == ProcessTypeEnum.w64on64) // Process is 64bit on 64bit OS; must use P/Invoke to read from 32bit Hive...
            {
                UIntPtr keyHandle;
                long result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, regkey, 0, KEY_QUERY_VALUE | KEY_WOW64_32KEY, out keyHandle);
                if (result != 0) { regValue = null; return false; }
                try
                {
                    int valuelength = 0;
                    uint valuetype;
                    result = RegQueryValueEx_Str(keyHandle, keyName, 0, out valuetype, null, ref valuelength);
                    if (result == 0)
                    {
                        StringBuilder sb = new StringBuilder(valuelength);
                        result = RegQueryValueEx_Str(keyHandle, keyName, 0, out valuetype, sb, ref valuelength);
                        if (result == 0) { regValue = sb.ToString(); return true; }
                        else { regValue = null; return false; }
                    }
                    else { regValue = null; return false; }
                }
                finally
                {
                    result = RegCloseKey(keyHandle);
                }
            }
            else
            {
                Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(regkey, false);
                if (key != null)
                {
                    object o = key.GetValue(keyName);
                    if (o != null) { regValue = o.ToString(); return true; }
                    else { regValue = null; return false; }
                }
                else
                { regValue = null; return false; }
            }
        }
        /// <summary>
        /// Read 64bit value from HKLM Registry hive
        /// 32on32: Use normal regread (64 bit value not available)
        /// 32on64: Use p/invoke to open 64bit registry hive
        /// 64on64: Use normal regread
        /// </summary>
        /// <param name="regkey"></param>
        /// <param name="keyName"></param>
        /// <param name="regValue"></param>
        /// <returns></returns>
        public static bool TryReadHKLM64Value(string regkey, string keyName, out string regValue)
        {
            if (ProcessType == ProcessTypeEnum.w32on64) // Process is 32bit on 64bit OS; must use P/Invoke to read from 64bit Hive...
            {
                UIntPtr keyHandle;
                long result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, regkey, 0, KEY_QUERY_VALUE | KEY_WOW64_64KEY, out keyHandle);
                if (result != 0) { regValue = null; return false; }
                try
                {
                    int valuelength = 0;
                    uint valuetype;
                    result = RegQueryValueEx_Str(keyHandle, keyName, 0, out valuetype, null, ref valuelength);
                    if (result == 0)
                    {
                        StringBuilder sb = new StringBuilder(valuelength);
                        result = RegQueryValueEx_Str(keyHandle, keyName, 0, out valuetype, sb, ref valuelength);
                        if (result == 0) { regValue = sb.ToString(); return true; }
                        else { regValue = null; return false; }
                    }
                    else { regValue = null; return false; }
                }
                finally
                {
                    result = RegCloseKey(keyHandle);
                }
            }
            else
            {
                Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.LocalMachine.OpenSubKey(regkey, false);
                if (key != null)
                {
                    object o = key.GetValue(keyName);
                    if (o != null) { regValue = o.ToString(); return true; }
                    else { regValue = null; return false; }
                }
                else
                { regValue = null; return false; }
            }
        }
    }
}
