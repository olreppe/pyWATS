using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using Virinco.WATS.Service.MES.Contract;
using System.Diagnostics;
using System.Runtime.Versioning;


namespace Virinco.WATS.Interface.MES.Production
{
    /// <summary>
    /// UnitInfo object which holds information about a scanned unit. 
    /// This object may be retrieved from MES Production interface.
    /// </summary>    
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    public class UnitInfo
    {
        private List<GetUnitInfo_Result> RelatedUnits = null;
        private GetUnitInfo_Result UnitInfoObject = null;
        //private IProductionService ServiceRef = null;
        private Production ProductionRef = null;

        //private UnitInfo() { }

        internal UnitInfo(GetUnitInfo_Result unitObj, List<GetUnitInfo_Result> relatedUnits, Production productionRef/*, IProductionService serviceRef*/)
        {
            UnitInfoObject = unitObj;
            RelatedUnits = relatedUnits;
            //ServiceRef = serviceRef;
            ProductionRef = productionRef;
        }

        private Unit _unitObject = null;
        private Unit UnitObject
        {
            get
            {
                if (_unitObject == null)
                    _unitObject = ProductionRef.serviceProxy.GetJson<Unit>($"api/internal/Production/GetUnit?unitId={ UnitInfoObject.UnitId }");
                //_unitObject = ServiceRef.GetUnit(UnitInfoObject.UnitId); 

                return _unitObject;
            }
        }

        /// <summary>
        /// XML data attached to product. May be queried by <see cref="GetInfo(string, DataType)"/>
        /// </summary>
        public string Product_Data
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.ProductXML != null)
                    return UnitInfoObject.ProductXML;
                return string.Empty;
            }
            //set
            //{
            //    UnitObject.ProductRevision.Product.XMLData = value;
            //    UnitInfoObject.ProductXML = value;
            //}
        }


        /// <summary>
        /// XML data attached to unit. May be queried by <see cref="GetInfo(string, DataType)"/>
        /// </summary>
        public string Unit_Data
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.UnitXML != null)
                    return UnitInfoObject.UnitXML;
                return string.Empty;
            }
            //set
            //{
            //    UnitObject.XMLData = value;
            //    UnitInfoObject.UnitXML = value;
            //}
        }


        /// <summary>
        /// XML data attached to revision. May be queried by <see cref="GetInfo(string, DataType)"/>
        /// </summary>
        public string Revision_Data
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.RevisionXML != null)
                    return UnitInfoObject.RevisionXML;
                return string.Empty;
            }
            //set
            //{
            //    UnitObject.ProductRevision.XMLData = value;
            //    UnitInfoObject.RevisionXML = value;
            //}
        }

        /// <summary>
        /// Unit's Serial Number
        /// </summary>
        public string SerialNumber
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.SerialNumber != null)
                    return UnitInfoObject.SerialNumber;
                return string.Empty;
            }
        }

        /// <summary>
        /// When unit is produced
        /// </summary>
        public DateTime? SerialDate
        {
            get
            {
                if (UnitInfoObject != null)
                    return UnitInfoObject.SerialDate;
                return null;
            }
        }

        /// <summary>
        /// Part number
        /// </summary>
        public string PartNumber
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.PartNumber != null)
                    return UnitInfoObject.PartNumber;
                return string.Empty;
            }

            //set
            //{
            //    UnitObject.ProductRevision.Product.PartNumber = value;
            //    UnitInfoObject.PartNumber = value;
            //}
        }

        /// <summary>
        /// Name of product
        /// </summary>
        public string PartNumberName
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.Name != null)
                    return UnitInfoObject.Name;
                return string.Empty;
            }

            //set
            //{
            //    UnitObject.ProductRevision.Product.Name = value;
            //    UnitInfoObject.Name = value;
            //}
        }

        /// <summary>
        /// Description of a product
        /// </summary>
        public string PartNumberDescription
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.ProductDescription != null)
                    return UnitInfoObject.ProductDescription;
                return string.Empty;
            }
            //set
            //{
            //    UnitObject.ProductRevision.Product.Description = value;
            //    UnitInfoObject.ProductDescription = value;
            //}
        }

        /// <summary>
        /// Batch number
        /// </summary>
        public string BatchNumber
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.BatchNumber != null)
                    return UnitInfoObject.BatchNumber;
                return string.Empty;
            }
        }

        /// <summary>
        /// Revision of a product
        /// </summary>
        public string Revision
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.Revision != null)
                    return UnitInfoObject.Revision;
                return string.Empty;
            }
            //set
            //{
            //    UnitObject.ProductRevision.Revision = value;
            //    UnitInfoObject.Revision = value;
            //}
        }

        /// <summary>
        /// Revision name of a product
        /// </summary>
        public string RevisionName
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.RevisionName != null)
                    return UnitInfoObject.RevisionName;
                return string.Empty;
            }
            //set
            //{
            //    UnitObject.ProductRevision.RevisionName = value;
            //    UnitInfoObject.RevisionName = value;
            //}
        }

        /// <summary>
        /// Description of a revision (overrides ProductDescription)
        /// </summary>
        public string RevisionDescription
        {
            get
            {
                if (UnitInfoObject != null && UnitInfoObject.RevisionDescription != null)
                    return UnitInfoObject.RevisionDescription;
                return string.Empty;
            }
            //set
            //{
            //    UnitObject.ProductRevision.Description = value;
            //    UnitInfoObject.RevisionDescription = value;
            //}
        }

        /// <summary>
        /// Query XML data given a field name
        /// </summary>
        /// <param name="Field">Name of field</param>
        /// <param name="Type">Type of XML data (enum)</param>
        /// <returns>Attribute value</returns>
        [Obsolete("GetInfoByField is deprecated, please use GetTagValue instead.")]
        public string GetInfoByField(string Field, DataType Type)
        {
            return GetInfoByField(Field, (int)Type);
        }

        /// <summary>
        /// Query data attached to unit, product or revision.
        /// </summary>
        /// <param name="Tag">Name of Tag</param>
        /// <param name="Type">Type of XML data (enum)</param>
        /// <returns>Tag value</returns>        
        public string GetTagValue(string Tag, DataType Type)
        {
            return GetTagValue(Tag, (int)Type);
        }

        /// <summary>
        /// Query XML data given a field name
        /// </summary>
        /// <param name="Field">Name of field</param>
        /// <param name="Type">Type of XML data (0=UnitData,1=ProductData,2=RevisionData)</param>
        /// <returns>Attribute value</returns>
        [Obsolete("GetInfoByField is deprecated, please use GetTagValue instead.")]
        public string GetInfoByField(string Field, int Type)
        {
            try
            {
                if (!string.IsNullOrEmpty(Field))
                {
                    string XPath = string.Format("/Root/{0}/@Value", Field);
                    return GetInfo(XPath, Type);
                }
            }
            catch (Exception e) { Env.LogException(e, "GetInfoByField"); }
            return string.Empty;
        }

        /// <summary>
        /// Query data attached to unit, product or revision.
        /// </summary>
        /// <param name="Tag">Name of Tag</param>
        /// <param name="Type">Type of XML data (0=UnitData,1=ProductData,2=RevisionData)</param>
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
        /// Change or add the value of a unit tag.
        /// </summary>
        /// <param name="Tag">Name of Tag.</param>
        /// <param name="TagValue">Value of Tag.</param>
        /// <returns>Success</returns>
        public bool SetTagValue(string Tag, string TagValue)
        {
            try
            {
                if (ProductionRef.isConnected())
                {
                    return ProductionRef.serviceProxy.PostJson<bool>($"api/internal/Production/UpdateUnitAttribute?serialNumber={SerialNumber}&partNumber=&attributeName={Tag}&attributeValue={TagValue}", SerialNumber);
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, "SetTagValue"); 
            }
            return false;
        }

        //public void saveChanges()
        //{
        //    ServiceRef.UpdateUnit(UnitObject);
        //}


        /// <summary>
        /// Type of XML data to query using <see cref="GetInfo(string, DataType)"/>
        /// </summary>
        public enum DataType
        {
            /// <summary>Unit data</summary>
            UnitData = 0,
            /// <summary>Product data</summary>
            ProductData = 1,
            /// <summary>Revision data</summary>
            RevisionData = 2
        }

        /// <summary>
        /// Query XML data given a XPath and XML <see cref="DataType"/>
        /// </summary>
        /// <param name="XPath">The XPath to query</param>
        /// <param name="type">The XML type to query</param>
        /// <returns>XPath query result as string</returns>
        public string GetInfo(string XPath, DataType type)
        {
            return GetInfo(XPath, (int)type);
        }

        /// <summary>
        /// Query XML data given a XPath and XML <see cref="DataType"/>
        /// </summary>
        /// <param name="XPath">The XPath to query</param>
        /// <param name="type">The XML type to query (0=UnitData,1=ProductData,2=RevisionData)</param>
        /// <returns>XPath query result as string</returns>
        public string GetInfo(string XPath, int type)
        {
            try
            {
                //Trace.WriteLine("GetInfo start");
                XmlDocument doc = new XmlDocument();
                switch (type)
                {
                    case 0:
                        if (Unit_Data != null)
                            doc.LoadXml(Unit_Data);
                        break;

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
            catch (Exception e) { Env.LogException(e, "GetInfo"); }
            return string.Empty;
        }


        private string getXpathInfo(XmlDocument doc, string XPath)
        {
            XmlNode node = doc.SelectSingleNode(XPath);
            if (node != null)
                return node.InnerXml;
            return string.Empty;
        }

        /// <summary>
        /// Indicates if the unit is a top level unit
        /// </summary>
        /// <returns>Boolean value indicating if the unit has any parent units.</returns>
        public bool HasParent()
        {
            if (UnitInfoObject != null)
                return UnitInfoObject.ParentUnitID != null;
            return false;
        }

        /// <summary>
        /// Get the number of child <see cref="UnitInfo"/> objects
        /// </summary>
        /// <returns>Number of child units or -1 of unknown</returns>
        public int GetChildCount()
        {
            try
            {
                //Trace.WriteLine("GetChildCount start");
                if (UnitInfoObject != null && RelatedUnits != null)
                    return RelatedUnits.Where(u => u.ParentUnitID == UnitInfoObject.UnitId).Count();
            }
            catch (Exception e) { Env.LogException(e, "GetChildCount"); }
            return -1;
        }


        /// <summary>
        /// Get parent <see cref="UnitInfo"/> object
        /// </summary>
        /// <returns></returns>
        public UnitInfo GetParent()
        {
            try
            {
                //Trace.WriteLine("GetParent start");
                //return createObject(UnitObject.ParentUnit);
                if (HasParent() && RelatedUnits != null)
                    return createObject(RelatedUnits.Where(u => u.UnitId == UnitInfoObject.ParentUnitID).SingleOrDefault());
            }
            catch (Exception e) { Env.LogException(e, "GetParent"); }
            return null;
        }

        /// <summary>
        /// Get Child <see cref="UnitInfo"/> object at index
        /// </summary>
        /// <param name="index"></param>
        /// <returns></returns>
        public UnitInfo GetChild(int index)
        {
            try
            {
                //Trace.WriteLine("GetChild start");
                //return createObject(UnitObject.ChildUnits[index]);
                return GetChildren()[index];

            }
            catch (Exception e) { Env.LogException(e, "GetChild"); }
            return null;
        }

        /// <summary>
        /// Get Child <see cref="UnitInfo"/> object at index
        /// </summary>
        /// <returns></returns>
        public UnitInfo[] GetChildren()
        {
            try
            {
                //Trace.WriteLine("GetChildren start");
                List<UnitInfo> ul = new List<UnitInfo>();
                foreach (GetUnitInfo_Result uir in RelatedUnits.Where(u => u.ParentUnitID == UnitInfoObject.UnitId))
                {
                    ul.Add(createObject(uir));
                }
                return ul.ToArray();
            }
            catch (Exception e) { Env.LogException(e, "GetChildren"); }
            return null;
        }

        private UnitInfo createObject(GetUnitInfo_Result uir)
        {
            if (uir != null)
                return new UnitInfo(uir, RelatedUnits, ProductionRef);
            return null;
        }

        ///// <summary>
        ///// Update/change current unit's PartNumber and Revision
        ///// </summary>
        ///// <param name="PartNumber">Unit's new PartNumber</param>
        ///// <param name="Revision">Unit's new Revision</param>
        //public void ChangeUnit(string PartNumber, string Revision)
        //{
        //    try
        //    {
        //        //ServiceRef.ChangeUnit(UnitObject, PartNumber, Revision);
        //    }
        //    catch (Exception ex) { Env.LogException(ex, "Error in ChangeUnit"); }
        //}

    }
}
