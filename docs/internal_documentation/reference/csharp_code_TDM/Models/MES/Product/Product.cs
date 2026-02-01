//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using Virinco.WATS.Service.MES.Contract;
//using System.Diagnostics;
//using System.Xml;
//using System.Windows.Forms;
//using Newtonsoft.Json;
//using System.IO;

//namespace Virinco.WATS.Interface.MES.Product
//{
//    /// <summary>
//    /// Class to handle product info
//    /// </summary>
//    public class Product : MesBase
//    {
//        /// <summary>
//        /// True if connected to server
//        /// </summary>
//        /// <returns></returns>
//        new public bool isConnected()
//        {
//            return base.isConnected();
//        }

//        /// <summary>
//        /// Holds information about the last scanned partnumber
//        /// </summary>
//        public string LastScannedPartnumber = string.Empty;


//        public static object DeserializeFromStream(Stream stream)
//        {
//            var serializer = new JsonSerializer();

//            using (var sr = new StreamReader(stream))
//            using (var jsonTextReader = new JsonTextReader(sr))
//            {
//                return serializer.Deserialize(jsonTextReader);
//            }
//        }

//        /// <summary>
//        /// Return <see cref="ProductInfo"/> object
//        /// </summary>
//        /// <param name="partNumber">Part Number to search</param>
//        /// <param name="revision">Revision</param>
//        /// <returns>A <see cref="ProductInfo"/> object with info about the PN supplied.</returns>
//        public ProductInfo GetProductInfo(string partNumber, string revision = "")
//        {
//            LastScannedPartnumber = partNumber;
//            if (isConnected())
//            {
//                try
//                {
//                    List<ProductInfoJson> pirl = serviceProxy.GetJson<List<ProductInfoJson>>($"api/internal/Product/GetProductInfo?partNumber={partNumber}&revision={revision}");
//                    ProductInfoJson pir = pirl.Where(p => p.PartNumber == partNumber && (string.IsNullOrEmpty(revision) || p.Revision == revision)).FirstOrDefault();
//                    ProductInfo pi = new ProductInfo(pir,pirl);
//                    return pi;
//                }
//                catch (Exception e) { Env.LogException(e, "GetProductInfo"); }
//            }
//            //Trace.WriteLine("GetProductInfo returns null");
//            return null;
//        }

//        /// <summary>
//        /// Identify Product with a popup GUI
//        /// </summary>
//        /// <param name="Filter">Filter down the products available in dropdown </param>
//        /// <param name="TopCount">Max count of products in the dropdown</param>
//        /// <param name="FreePartnumber">If PartNumber MUST be selected from the dropdown or not</param>
//        /// <param name="IncludeRevision">If Revision should be selected or not</param>
//        /// <param name="IncludeSerialNumber">If SerialNumber should be included or not</param>
//        /// <param name="SelectedSerialNumber"></param>
//        /// <param name="SelectedPartNumber"></param>
//        /// <param name="SelectedRevision"></param>
//        /// <param name="SelectedTestOperation"></param>
//        /// <param name="Continue">Stopped or Continue execution</param>
//        /// <param name="CustomText"></param>
//        /// <param name="AlwaysOnTop"></param>
//        public void IdentifyProduct(string Filter, int TopCount, bool FreePartnumber, bool IncludeRevision, bool IncludeSerialNumber, out string SelectedSerialNumber, out string SelectedPartNumber, out string SelectedRevision, out Virinco.WATS.Service.MES.Contract.Process SelectedTestOperation, out bool Continue, string CustomText = "", bool AlwaysOnTop = true)
//        {
//            SelectedSerialNumber = null;
//            SelectedPartNumber = null;
//            SelectedRevision = null;
//            SelectedTestOperation = null;
//            Continue = false;
//            try
//            {
//                //Trace.WriteLine("IdentifyProduct start");
//                if (isConnected())
//                {
//                    using (IdentifyProduct form = new IdentifyProduct(this, IncludeRevision, IncludeSerialNumber, FreePartnumber, Filter, TopCount, CustomText, AlwaysOnTop))
//                    {
//                        form.ShowDialog();
//                        Continue = form.Continue;
//                        SelectedSerialNumber = form.SelectedSerialNumber;
//                        SelectedPartNumber = form.SelectedPartNumber;
//                        SelectedRevision = form.SelectedRevision;
//                        SelectedTestOperation = form.SelectedTestOperation;
//                    }
//                }
//            }
//            catch (Exception e) { Env.LogException(e, ""); }
//        }



//        /// <summary>
//        /// Get products and revisions with a PartNumber containing filter
//        /// </summary>
//        /// <param name="filter">PartNumbers containing this value are returned (* and % are removed)</param>
//        /// <param name="topCount">Max products to return</param>
//        /// <param name="includeNonSerial">Boolean value to include nonSerial product or not</param>
//        /// <param name="includeRevision">Include Revision object on matching objects</param>
//        /// <returns></returns>
//        public Virinco.WATS.Service.MES.Contract.Product[] GetProduct(string filter, int topCount, bool includeNonSerial, bool includeRevision)
//        {
//            if (isConnected())
//            {
//                try
//                {
//                    List<Service.MES.Contract.Product> products = serviceProxy.GetJson<List<Service.MES.Contract.Product>>($"api/internal/Product/GetProducts?filter={filter}&includeNonSerial={includeNonSerial}&includeRevision={includeRevision}&topCount={topCount}");
//                    return products.ToArray(); ;
//                }
//                catch (Exception e) { Env.LogException(e, "GetProduct"); }
//            }
//            return null;
//        }

//    }
//}
