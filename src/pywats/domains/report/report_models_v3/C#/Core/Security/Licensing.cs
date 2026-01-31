using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Security.Cryptography.Xml;
using System.Xml;
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.IO;
using System.Security.Cryptography.Pkcs;

namespace Virinco.WATS.Security
{
    public class Licensing
    {

        public static byte[] GetMD5Hashcode(string data)
        {
            if (string.IsNullOrEmpty(data))
                throw new ArgumentNullException("data");
            MD5CryptoServiceProvider MD5 = new MD5CryptoServiceProvider();
            byte[] dataBytes = Encoding.Default.GetBytes(data);
            byte[] encryptedBytes = MD5.ComputeHash(dataBytes);
            return encryptedBytes;
        }


        public static bool installCertificate(StoreLocation storelocation, StoreName storename, X509Certificate2 certificate)
        {
            X509Store store = new X509Store(storename, storelocation);
            store.Open(OpenFlags.ReadOnly);
            bool installed = false;
            if (!store.Certificates.Contains(certificate))
            {
                store.Open(OpenFlags.ReadWrite); 
                store.Add(certificate);
                installed = true;
            }
            store.Close();
            return installed;
        }
                
        public static X509Certificate2 GetCertificate(string Subject, StoreName StoreName, StoreLocation StoreLocation)
        {
            return GetCertificate(Subject, StoreName, StoreLocation, "");
        }

        public static X509Certificate2 GetCertificate(string Subject, StoreName StoreName, StoreLocation StoreLocation, string Issuer)
        {
            X509Store store = new X509Store(StoreName, StoreLocation);
            store.Open(OpenFlags.ReadOnly);
            X509Certificate2Collection certCollection = store.Certificates;

            X509Certificate2 cert = null;
            // Loop through each certificate and find the appropriate one.
            foreach (X509Certificate2 c in certCollection)
            {
                if (c.Subject == Subject && (c.Issuer == Issuer || Issuer == ""))//"CN=TestCert")   
                {
                    cert = c;
                    break;
                }
            }
            store.Close();
            if (cert == null)
                throw new Exception("Unable to look up certificate.");

            return cert;
        }

        /// <summary>
        /// Sign a XML Document with a given private key
        /// </summary>
        /// <param name="Doc">XmlDocument to sign</param>
        /// <param name="Cert">Certificate to sign the document with</param>
        /// <exception cref="ArgumentException">XmlDocument (Doc) is null or Cert's private key is null</exception>
        public static void SignXml(XmlDocument Doc, X509Certificate2 Cert)
        {
            // Check arguments.
            if (Doc == null)
                throw new ArgumentException("Signing failed: Unable to read license file.");
            if (Cert == null)
                throw new ArgumentException("Signing failed: Unable to read certificate.");
            if (Cert.PrivateKey == null || !Cert.HasPrivateKey)
                throw new ArgumentException("Signing failed: Unable to read certificate's PrivateKey.");

            //Doc.PreserveWhitespace = false;
            // Create a SignedXml object.
            SignedXml signedXml = new SignedXml(Doc);

            // Add the key to the SignedXml document.
            signedXml.SigningKey = Cert.PrivateKey;

            // Create a reference to be signed.
            Reference reference = new Reference();
            reference.Uri = "";

            // Add an enveloped transformation to the reference.
            XmlDsigEnvelopedSignatureTransform env = new XmlDsigEnvelopedSignatureTransform();
            reference.AddTransform(env);

            // Add the reference to the SignedXml object.
            signedXml.AddReference(reference);

            // Compute the signature.
            signedXml.ComputeSignature();

            // Get the XML representation of the signature and save
            // it to an XmlElement object.
            XmlElement xmlDigitalSignature = signedXml.GetXml();

            // Append the element to the XML document.
            Doc.DocumentElement.AppendChild(Doc.ImportNode(xmlDigitalSignature, true));
        }

        /// <summary>
        /// Verify a signed XmlDocument against a Public Key
        /// </summary>
        /// <param name="Doc"></param>
        /// <param name="Cert">Certificate to Use in the verification</param>
        /// <returns>Boolean value indicating if the verfication was successfull or not</returns>
        public static Boolean VerifyXml(XmlDocument Doc, X509Certificate2 Cert)
        {
            // Check arguments.
            if (Doc == null)
                throw new ArgumentException("Verification failed: Unable to read license file.");
            if (Cert == null)
                throw new ArgumentException("Verification failed: Unable to read certificate.");
            if (Cert.PublicKey.Key == null)
                throw new ArgumentException("Verification failed: Unable to read certificate's PublicKey.");

            //Doc.PreserveWhitespace = false;
            // Create a new SignedXml object and pass it
            // the XML document class.
            SignedXml signedXml = new SignedXml(Doc);

            // Find the "Signature" node and create a new
            // XmlNodeList object.
            XmlNodeList nodeList = Doc.GetElementsByTagName("Signature");

            // Throw an exception if no signature was found.
            if (nodeList.Count <= 0)
            {
                throw new CryptographicException("Verification failed: No Signature was found in the document.");
            }

            // This example only supports one signature for
            // the entire XML document.  Throw an exception 
            // if more than one signature was found.
            if (nodeList.Count >= 2)
            {
                throw new CryptographicException("Verification failed: More that one signature was found for the document.");
            }

            // Load the first <signature> node.  
            signedXml.LoadXml((XmlElement)nodeList[0]);

            // Check the signature and return the result.
            return signedXml.CheckSignature(Cert.PublicKey.Key);
        }

        private const string VirincoRootCertificateUrl = "http://pki.virinco.com/certenroll/VirincoCA.p7b";
        public static int installDefaultChain()
        {
            return installChain(VirincoRootCertificateUrl);
        }
        public static int installChain(string p7b_uri)
        {
            System.Net.WebClient wc = new System.Net.WebClient();
            byte[] data = wc.DownloadData(p7b_uri);
            SignedCms sc = new SignedCms();
            sc.Decode(data);
            int counter = 0;
            foreach (X509Certificate2 c in sc.Certificates)
            {
                //CN=VirincoCA, DC=partner, DC=virinco, DC=local               
                string s =  c.GetNameInfo(X509NameType.SimpleName,false);
                string i =  c.GetNameInfo(X509NameType.SimpleName,true);

                if(s==i)// ( c.IssuerName.GetNameInfo(X509NameType.UpnName.Subject == c.Issuer)// .ToLower().Contains("root"))
                {
                    if (installCertificate(StoreLocation.LocalMachine, StoreName.Root, c))
                        counter++;
                }
                else //(c.Subject.ToLower().Contains("ca"))
                {
                    if (installCertificate(StoreLocation.LocalMachine, StoreName.CertificateAuthority, c))
                        counter++;
                }
                //else
                //{
                //    if (installCertificate(StoreLocation.LocalMachine, StoreName.My, c))
                //        counter++;
                //}
            }
            return counter;
        }
    }


}
