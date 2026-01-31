using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

namespace Virinco.WATS.Security
{
    public class Cryptography
    {
        public static string DecryptEncryptString(string key, string text, bool encrypt = true)
        {
            if (String.IsNullOrEmpty(text)) return text;
            byte[] data = encrypt ? Encoding.Unicode.GetBytes(text) : Convert.FromBase64String(text);
            using (Aes encryption = Aes.Create())
            {
                Rfc2898DeriveBytes pdb = new Rfc2898DeriveBytes(key, new byte[] { 0x49, 0x76, 0x61, 0x6e, 0x20, 0x4d, 0x65, 0x64, 0x76, 0x65, 0x64, 0x65, 0x76 });
                encryption.Key = pdb.GetBytes(32);
                encryption.IV = pdb.GetBytes(16);
                using (MemoryStream ms = new MemoryStream())
                {
                    using (CryptoStream cs = new CryptoStream(ms, encrypt ? encryption.CreateEncryptor() : encryption.CreateDecryptor(), CryptoStreamMode.Write))
                    {
                        cs.Write(data, 0, data.Length);
                        cs.Close();
                    }
                    text = encrypt ? Convert.ToBase64String(ms.ToArray()) : Encoding.Unicode.GetString(ms.ToArray());
                }
            }
            return text;
        }
    }
}
