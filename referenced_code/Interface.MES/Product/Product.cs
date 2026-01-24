extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using napict = newclientapi::Virinco.WATS.Service.MES.Contract;
using ct = Virinco.WATS.Service.MES.Contract;
using Virinco.WATS.Service.MES.Contract;
using System.Linq;
using System.IO;

namespace Virinco.WATS.Interface.MES.Product
{
    /// <summary>
    /// Class to handle product info
    /// </summary>
    public class Product : MesBase
    {
        private napi.Product.Product _instance;

        internal Product(napi.Product.Product product)
        {
            this._instance = product;
        }
        /// <summary>
        /// True if connected to server
        /// </summary>
        /// <returns></returns>
        public new bool isConnected() => _instance.isConnected();

        /// <summary>
        /// Holds information about the last scanned partnumber
        /// </summary>
        public string LastScannedPartnumber
        {
            get => _instance.LastScannedPartnumber;
            set => _instance.LastScannedPartnumber = value;
        }

        public static object DeserializeFromStream(Stream stream) => napi.Product.Product.DeserializeFromStream(stream);

        /// <summary>
        /// Return <see cref="ProductInfo"/> object
        /// </summary>
        /// <param name="partNumber">Part Number to search</param>
        /// <param name="revision">Revision</param>
        /// <returns>A <see cref="ProductInfo"/> object with info about the PN supplied.</returns>
        public ProductInfo GetProductInfo(string partNumber, string revision = "") => new ProductInfo(_instance.GetProductInfo(partNumber, revision));

        /// <summary>
        /// Identify Product with a popup GUI
        /// </summary>
        /// <param name="Filter">Filter down the products available in dropdown </param>
        /// <param name="TopCount">Max count of products in the dropdown</param>
        /// <param name="FreePartnumber">If PartNumber MUST be selected from the dropdown or not</param>
        /// <param name="IncludeRevision">If Revision should be selected or not</param>
        /// <param name="IncludeSerialNumber">If SerialNumber should be included or not</param>
        /// <param name="SelectedSerialNumber"></param>
        /// <param name="SelectedPartNumber"></param>
        /// <param name="SelectedRevision"></param>
        /// <param name="SelectedTestOperation"></param>
        /// <param name="Continue">Stopped or Continue execution</param>
        /// <param name="CustomText"></param>
        /// <param name="AlwaysOnTop"></param>
        public void IdentifyProduct(string Filter, int TopCount, bool FreePartnumber, bool IncludeRevision, bool IncludeSerialNumber, out string SelectedSerialNumber, out string SelectedPartNumber, out string SelectedRevision, out Virinco.WATS.Service.MES.Contract.Process SelectedTestOperation, out bool Continue, string CustomText = "", bool AlwaysOnTop = true)
        {
            napict.Process selectedTestOperation;
            _instance.IdentifyProduct(Filter, TopCount, FreePartnumber, IncludeRevision, IncludeSerialNumber, out SelectedSerialNumber, out SelectedPartNumber, out SelectedRevision, out selectedTestOperation, out Continue, CustomText, AlwaysOnTop);
            SelectedTestOperation = new Process(selectedTestOperation);
        }

        /// <summary>
        /// Get products and revisions with a PartNumber containing filter
        /// </summary>
        /// <param name="filter">PartNumbers containing this value are returned (* and % are removed)</param>
        /// <param name="topCount">Max products to return</param>
        /// <param name="includeNonSerial">Boolean value to include nonSerial product or not</param>
        /// <param name="includeRevision">Include Revision object on matching objects</param>
        /// <returns></returns>
        public Virinco.WATS.Service.MES.Contract.Product[] GetProduct(string filter, int topCount, bool includeNonSerial, bool includeRevision)
            => _instance.GetProduct(filter, topCount, includeNonSerial, includeRevision).Select(i => new ct.Product(i)).ToArray();
    }
}
