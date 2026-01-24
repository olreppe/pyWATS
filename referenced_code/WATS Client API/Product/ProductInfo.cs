using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Service.MES.Contract;
using System.Diagnostics;
using System.Xml;
using System.Xml.Linq;

namespace Virinco.WATS.Interface.MES.Product
{
    /// <summary>
    /// Holds information about a product. Part Number, Name and child/parent relations.
    /// </summary>
    public class ProductInfo
    {
        private GetProductInfo_Result ProductInfoObject = null;
        private List<GetProductInfo_Result> RelatedProducts = null;

        internal ProductInfo(GetProductInfo_Result productObj, List<GetProductInfo_Result> relatedProducts )
        {
            ProductInfoObject = productObj;
            RelatedProducts = relatedProducts;
        }

        public ProductInfo(ProductInfoJson pir, List<ProductInfoJson> pirl)
        {
            ProductInfoObject = CopyProductInfo(pir);
            if (pirl.Count > 1)
                RelatedProducts = new List<GetProductInfo_Result>();
            foreach (ProductInfoJson pi in pirl)
            {
                if (pi.ProductRevisionId != pir.ProductRevisionId)
                    RelatedProducts.Add(CopyProductInfo(pi));
            }
        }

        private GetProductInfo_Result CopyProductInfo (ProductInfoJson pir)
        {
            GetProductInfo_Result productInfo_Result = new GetProductInfo_Result()
            {
                Category = pir.Category,
                hlevel = pir.hlevel,
                Name = pir.Name,
                ParentProductRevisionId = pir.ParentProductRevisionId,
                PartNumber = pir.PartNumber,
                PathStr = pir.PathStr,
                ProductDescription = pir.ProductDescription,
                ProductId = pir.ProductId,
                ProductRevisionId = pir.ProductRevisionId,
                ProductRevisionRelationId = pir.ProductRevisionRelationId,
                Quantity = pir.Quantity,
                Revision = pir.Revision,
                RevisionDescription = pir.RevisionDescription,
                RevisionMask = pir.RevisionMask,
                RevisionName = pir.RevisionName
            };

            //In 2019.2, JsonIgnore attribute was added to ProductData and RevisionData, and ProductSettings and RevisionSettings were added instead.
            productInfo_Result.ProductData = string.IsNullOrEmpty(pir.ProductData) ? GetXmlFromJson(pir.ProductSettings ?? new List<KeyValue>()) : pir.ProductData;
            productInfo_Result.RevisionData = string.IsNullOrEmpty(pir.RevisionData) ? GetXmlFromJson(pir.RevisionSettings ?? new List<KeyValue>()) : pir.RevisionData;
            return productInfo_Result;
        }

        private string GetXmlFromJson(List<KeyValue> productData)
        {
            XDocument xml = new XDocument();
            XElement root = new XElement("Root");
            xml.Add(root);
            foreach (KeyValue keyValue in productData)
            {
                XElement xval = new XElement(keyValue.key);
                xval.Add(new XAttribute("Value",keyValue.value));
                root.Add(xval);
            }
            return xml.ToString();
        }

        /// <summary>
        /// The product's Part Number
        /// </summary>
        public string PartNumber {
            get {
                if (ProductInfoObject != null && ProductInfoObject.PartNumber != null)
                    return ProductInfoObject.PartNumber;
                return string.Empty;
            }
        }
        
        /// <summary>
        /// The product's Name
        /// </summary>
        public string Name {
            get {
                if (ProductInfoObject != null && ProductInfoObject.Name != null)
                    return ProductInfoObject.Name;
                return string.Empty;
            }
        }

        /// <summary>
        /// The product's Revision
        /// </summary>
        public string Revision
        {
            get
            {
                if (ProductInfoObject != null && ProductInfoObject.Revision != null)
                    return ProductInfoObject.Revision;
                return string.Empty;
            }
        }

        /// <summary>
        /// The product's Revision name
        /// </summary>
        public string RevisionName
        {
            get
            {
                if (ProductInfoObject != null && ProductInfoObject.RevisionName != null)
                    return ProductInfoObject.RevisionName;
                return string.Empty;
            }
        }
        

        /// <summary>
        /// How many units like this Product Info object does the parent contain.
        /// </summary>
        public int? Quantity {
            get {
                if (ProductInfoObject != null)
                    return ProductInfoObject.Quantity;
                return null;            
            }
        }

        /// <summary>
        /// The product's description
        /// </summary>
        public string ProductDescription
        {
            get
            {
                if (ProductInfoObject != null && ProductInfoObject.ProductDescription != null)
                    return ProductInfoObject.ProductDescription;
                return string.Empty;
            }
        }

        /// <summary>
        /// The revision's description
        /// </summary>
        public string RevisionDescription
        {
            get
            {
                if (ProductInfoObject != null && ProductInfoObject.RevisionDescription != null)
                    return ProductInfoObject.RevisionDescription;
                return string.Empty;
            }
        }

        /// <summary>
        /// The product's category
        /// </summary>
        public string ProductCategory
        {
            get
            {
                if (ProductInfoObject != null && ProductInfoObject.Category != null)
                    return ProductInfoObject.Category;
                return string.Empty;
            }
        }

        /// <summary>
        /// Data attached to product. May be queried by <see cref="GetTagValue"/>
        /// </summary>
        public string Product_Data
        {
            get
            {
                if (ProductInfoObject != null && ProductInfoObject.ProductData != null)
                    return ProductInfoObject.ProductData;
                return string.Empty;
            }           
        }

        /// <summary>
        /// Data attached to product revision. May be queried by <see cref="GetTagValue"/>
        /// </summary>
        public string Revision_Data
        {
            get
            {
                if (ProductInfoObject != null && ProductInfoObject.RevisionData != null)
                    return ProductInfoObject.RevisionData;
                return string.Empty;
            }           
        }

        /// <summary>
        /// Indicates if the product is a top level product
        /// </summary>
        /// <returns>Boolean value indicating if the product has any parent products.</returns>
        public bool HasParent()
        {
            //try
            //{
            //Trace.WriteLine("HasParent start");
            if (ProductInfoObject != null)
                return ProductInfoObject.ParentProductRevisionId != null;
            return false;
            //}
            //catch (Exception e) { Env.LogException(e, "HasParent"); }
            //return false;
        }
        
        /// <summary>
        /// Get parent <see cref="ProductInfo"/> object
        /// </summary>
        /// <returns></returns>
        public ProductInfo GetParent()
        {
            try
            {
                //Trace.WriteLine("GetParent start");                
                if (HasParent() && RelatedProducts != null)
                    return createObject(RelatedProducts.Where(p => p.ProductRevisionId == ProductInfoObject.ParentProductRevisionId).SingleOrDefault());
            }
            catch (Exception e) { Env.LogException(e, "GetParent"); }
            return null;
        }

        /// <summary>
        /// Get the number of child <see cref="ProductInfo"/> objects
        /// </summary>
        /// <returns>Number of child products or -1 of unknown</returns>
        public int GetChildCount()
        {
            try
            {
                //Trace.WriteLine("GetChildCount start");
                if (ProductInfoObject != null && RelatedProducts != null)
                    return RelatedProducts.Where(p => p.ParentProductRevisionId == ProductInfoObject.ProductRevisionId).Count();
            }
            catch (Exception e) { Env.LogException(e, "GetChildCount"); }
            return -1;
        }

        /// <summary>
        /// Get Child <see cref="ProductInfo"/> object at index
        /// </summary>
        /// <param name="index"></param>
        /// <returns></returns>
        public ProductInfo GetChild(int index)
        {
            try
            {
                //Trace.WriteLine("GetChild start");                
                return GetChildren()[index];

            }
            catch (Exception e) { Env.LogException(e, "GetChild"); }
            return null;
        }

        /// <summary>
        /// Get Child <see cref="ProductInfo"/> objects
        /// </summary>
        /// <returns></returns>
        public ProductInfo[] GetChildren()
        {
            try
            {
                //Trace.WriteLine("GetChildren start");
                List<ProductInfo> pl = new List<ProductInfo>();
                foreach (GetProductInfo_Result pir in RelatedProducts.Where(p => p.ParentProductRevisionId == ProductInfoObject.ProductRevisionId))
                {
                    pl.Add(createObject(pir));
                }
                return pl.ToArray();
            }
            catch (Exception e) { Env.LogException(e, "GetChildren"); }
            return null;
        }

        /// <summary>
        /// Query data attached to product or revision.
        /// </summary>
        /// <param name="Tag">Name of Tag</param>
        /// <param name="Type">Type of XML data (1=ProductData,2=RevisionData)</param>
        /// <returns>Tag value</returns>
        public string GetTagValue(string Tag, int Type)
        {
            try
            {
                if (!string.IsNullOrEmpty(Tag))
                {
                    string XPath = string.Format("/Root/{0}/@Value", Tag);
                    return GetInfo(XPath, Type);
                }
            }
            catch (Exception e) { Env.LogException(e, "GetTagValue"); }
            return string.Empty;
        }

        /// <summary>
        /// Query Product XML data given a XPath
        /// </summary>
        /// <param name="XPath">The XPath to query</param>        
        /// <returns>XPath query result as string</returns>
        public string GetInfo(string XPath)
        {
            try
            {
                XmlDocument doc = new XmlDocument();
                if (Product_Data != null)
                    doc.LoadXml(Product_Data);                    
                return getXpathInfo(doc, XPath);
            }
            catch (Exception e) { Env.LogException(e, "GetInfo"); }
            return string.Empty;
        }

        /// <summary>
        /// Query XML data given a XPath and XML <see cref="DataType"/>. 
        /// </summary>
        /// <param name="XPath">The XPath to query</param>
        /// <param name="type">The XML type to query (1=ProductData,2=RevisionData)</param>
        /// <returns>XPath query result as string</returns>
        private string GetInfo(string XPath, int type)
        {
            try
            {
                XmlDocument doc = new XmlDocument();
                switch (type)
                {
                    case 1:
                        if (Product_Data != null)
                            doc.LoadXml(Product_Data);
                        break;

                    case 2:
                        if (Revision_Data != null)
                            doc.LoadXml(Revision_Data);
                        break;

                    default: break;
                }
                return getXpathInfo(doc, XPath);
            }
            catch (Exception e) { Env.LogException(e, "GetInfo(string XPath, int type)"); }
            return string.Empty;
        }


        private string getXpathInfo(XmlDocument doc, string XPath)
        {
            XmlNode node = doc.SelectSingleNode(XPath);
            if (node != null)
                return node.InnerXml;
            return string.Empty;
        }

        private ProductInfo createObject(GetProductInfo_Result pir)
        {
            if (pir != null)
                return new ProductInfo(pir, RelatedProducts);
            return null;
        }

    }
}
