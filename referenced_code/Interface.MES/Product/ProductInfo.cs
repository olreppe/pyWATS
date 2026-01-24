extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System.Collections.Generic;
using System.Linq;

namespace Virinco.WATS.Interface.MES.Product
{
    /// <summary>
    /// Holds information about a product. Part Number, Name and child/parent relations.
    /// </summary>
    public class ProductInfo
    {
        private napi.Product.ProductInfo _instance;

        internal ProductInfo(napi.Product.ProductInfo product)
        {
            this._instance = product;
        }

        public ProductInfo(ProductInfoJson pir, List<ProductInfoJson> pirl)
        {
            this._instance = new napi.Product.ProductInfo(pir._instance, pirl.Select(pi => pi._instance).ToList());
        }

        /// <summary>
        /// The product's Part Number
        /// </summary>
        public string PartNumber // r/o
        {
            get => this._instance.PartNumber;
            //set => this._instance.PartNumber = value;
        }

        /// <summary>
        /// The product's Name
        /// </summary>
        public string Name // r/o
        {
            get => this._instance.Name;
            //set => this._instance.Name = value;
        }

        /// <summary>
        /// The product's Revision
        /// </summary>
        public string Revision // r/o
        {
            get => this._instance.Revision;
            //set => this._instance.Revision = value;
        }

        /// <summary>
        /// The product's Revision name
        /// </summary>
        public string RevisionName // r/o
        {
            get => this._instance.RevisionName;
            //set => this._instance.RevisionName = value;
        }

        /// <summary>
        /// How many units like this Product Info object does the parent contain.
        /// </summary>
        public int? Quantity // r/o
        {
            get => this._instance.Quantity;
            //set => this._instance.Quantity = value;
        }

        /// <summary>
        /// The product's description
        /// </summary>
        public string ProductDescription // r/o
        {
            get => this._instance.ProductDescription;
            //set => this._instance.ProductDescription = value;
        }

        /// <summary>
        /// The revision's description
        /// </summary>
        public string RevisionDescription // r/o
        {
            get => this._instance.RevisionDescription;
            //set => this._instance.RevisionDescription = value;
        }

        /// <summary>
        /// The product's category
        /// </summary>
        public string ProductCategory // r/o
        {
            get => this._instance.ProductCategory;
            //set => this._instance.ProductCategory = value;
        }

        /// <summary>
        /// Data attached to product. May be queried by <see cref="GetTagValue"/>
        /// </summary>
        public string Product_Data // r/o
        {
            get => this._instance.Product_Data;
            //set => this._instance.Product_Data = value;
        }

        /// <summary>
        /// Data attached to product revision. May be queried by <see cref="GetTagValue"/>
        /// </summary>
        public string Revision_Data // r/o
        {
            get => this._instance.Revision_Data;
            //set => this._instance.Revision_Data = value;
        }

        /// <summary>
        /// Indicates if the product is a top level product
        /// </summary>
        /// <returns>Boolean value indicating if the product has any parent products.</returns>
        public bool HasParent()
            => this._instance.HasParent();

        /// <summary>
        /// Get parent <see cref="ProductInfo"/> object
        /// </summary>
        /// <returns></returns>
        public ProductInfo GetParent()
            => new ProductInfo(this._instance.GetParent());

        /// <summary>
        /// Get the number of child <see cref="ProductInfo"/> objects
        /// </summary>
        /// <returns>Number of child products or -1 of unknown</returns>
        public int GetChildCount()
            => this._instance.GetChildCount();

        /// <summary>
        /// Get Child <see cref="ProductInfo"/> object at index
        /// </summary>
        /// <param name="index"></param>
        /// <returns></returns>
        public ProductInfo GetChild(int index)
            => new ProductInfo(_instance.GetChild(index));

        /// <summary>
        /// Get Child <see cref="ProductInfo"/> objects
        /// </summary>
        /// <returns></returns>
        public ProductInfo[] GetChildren()
            => _instance.GetChildren().Select(i => new ProductInfo(i)).ToArray();

        /// <summary>
        /// Query data attached to product or revision.
        /// </summary>
        /// <param name="Tag">Name of Tag</param>
        /// <param name="Type">Type of XML data (1=ProductData,2=RevisionData)</param>
        /// <returns>Tag value</returns>
        public string GetTagValue(string Tag, int Type)
            => _instance.GetTagValue(Tag, Type);

        /// <summary>
        /// Query Product XML data given a XPath
        /// </summary>
        /// <param name="XPath">The XPath to query</param>        
        /// <returns>XPath query result as string</returns>
        public string GetInfo(string XPath)
            => _instance.GetInfo(XPath);
    }
}
