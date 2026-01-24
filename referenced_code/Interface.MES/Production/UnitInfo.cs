extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System;
using System.Linq;

namespace Virinco.WATS.Interface.MES.Production
{
    /// <summary>
    /// UnitInfo object which holds information about a scanned unit. 
    /// This object may be retrieved from MES Production interface.
    /// </summary>    
    public class UnitInfo
    {
        private napi.Production.UnitInfo _instance;
        internal UnitInfo(napi.Production.UnitInfo instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// XML data attached to product. May be queried by <see cref="GetInfo"/>
        /// </summary>
        public string Product_Data // r/o
        {
            get => _instance.Product_Data;
            //set => _instance.Product_Data = value;
        }

        /// <summary>
        /// XML data attached to unit. May be queried by <see cref="GetInfo"/>
        /// </summary>
        public string Unit_Data // r/o
        {
            get => _instance.Unit_Data;
            //set => _instance.Unit_Data = value;
        }

        /// <summary>
        /// XML data attached to revision. May be queried by <see cref="GetInfo"/>
        /// </summary>
        public string Revision_Data // r/o
        {
            get => _instance.Revision_Data;
            //set => _instance.Revision_Data = value;
        }

        /// <summary>
        /// Unit's Serial Number
        /// </summary>
        public string SerialNumber // r/o
        {
            get => _instance.SerialNumber;
            //set => _instance.SerialNumber = value;
        }

        /// <summary>
        /// When unit is produced
        /// </summary>
        public DateTime? SerialDate // r/o
        {
            get => _instance.SerialDate;
            //set => _instance.SerialDate = value;
        }

        /// <summary>
        /// Part number
        /// </summary>
        public string PartNumber // r/o
        {
            get => _instance.PartNumber;
            //set => _instance.PartNumber = value;
        }

        /// <summary>
        /// Name of product
        /// </summary>
        public string PartNumberName // r/o
        {
            get => _instance.PartNumberName;
            //set => _instance.PartNumberName = value;
        }

        /// <summary>
        /// Description of a product
        /// </summary>
        public string PartNumberDescription // r/o
        {
            get => _instance.PartNumberDescription;
            //set => _instance.PartNumberDescription = value;
        }

        /// <summary>
        /// Batch number
        /// </summary>
        public string BatchNumber // r/o
        {
            get => _instance.BatchNumber;
            //set => _instance.BatchNumber = value;
        }
        /// <summary>
        /// Revision of a product
        /// </summary>
        public string Revision // r/o
        {
            get => _instance.Revision;
            //set => _instance.Revision = value;
        }

        /// <summary>
        /// Revision name of a product
        /// </summary>
        public string RevisionName // r/o
        {
            get => _instance.RevisionName;
            //set => _instance.RevisionName = value;
        }

        /// <summary>
        /// Description of a revision (overrides ProductDescription)
        /// </summary>
        public string RevisionDescription // r/o
        {
            get => _instance.RevisionDescription;
            //set => _instance.RevisionDescription = value;
        }

        /// <summary>
        /// Query XML data given a field name
        /// </summary>
        /// <param name="Field">Name of field</param>
        /// <param name="Type">Type of XML data (enum)</param>
        /// <returns>Attribute value</returns>
        [Obsolete("GetInfoByField is deprecated, please use GetTagValue instead.")]
        public string GetInfoByField(string Field, DataType Type)
            => _instance.GetInfoByField(Field, (int)Type);

        /// <summary>
        /// Query data attached to unit, product or revision.
        /// </summary>
        /// <param name="Tag">Name of Tag</param>
        /// <param name="Type">Type of XML data (enum)</param>
        /// <returns>Tag value</returns>        
        public string GetTagValue(string Tag, DataType Type)
            => _instance.GetTagValue(Tag, (int)Type);

        /// <summary>
        /// Query XML data given a field name
        /// </summary>
        /// <param name="Field">Name of field</param>
        /// <param name="Type">Type of XML data (0=UnitData,1=ProductData,2=RevisionData)</param>
        /// <returns>Attribute value</returns>
        [Obsolete("GetInfoByField is deprecated, please use GetTagValue instead.")]
        public string GetInfoByField(string Field, int Type)
        => _instance.GetInfoByField(Field, Type);

        /// <summary>
        /// Query data attached to unit, product or revision.
        /// </summary>
        /// <param name="Tag">Name of Tag</param>
        /// <param name="Type">Type of XML data (0=UnitData,1=ProductData,2=RevisionData)</param>
        /// <returns>Tag value</returns>
        public string GetTagValue(string Tag, int Type)
            => _instance.GetTagValue(Tag, Type);

        /// <summary>
        /// Change or add the value of a unit tag.
        /// </summary>
        /// <param name="Tag">Name of Tag.</param>
        /// <param name="TagValue">Value of Tag.</param>
        /// <returns>Success</returns>
        public bool SetTagValue(string Tag, string TagValue)
            => _instance.SetTagValue(Tag, TagValue);

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
            => _instance.GetInfo(XPath, (int)type);

        /// <summary>
        /// Query XML data given a XPath and XML <see cref="DataType"/>
        /// </summary>
        /// <param name="XPath">The XPath to query</param>
        /// <param name="type">The XML type to query (0=UnitData,1=ProductData,2=RevisionData)</param>
        /// <returns>XPath query result as string</returns>
        public string GetInfo(string XPath, int type)
            => _instance.GetInfo(XPath, type);

        /// <summary>
        /// Indicates if the unit is a top level unit
        /// </summary>
        /// <returns>Boolean value indicating if the unit has any parent units.</returns>
        public bool HasParent()
            => _instance.HasParent();

        /// <summary>
        /// Get the number of child <see cref="UnitInfo"/> objects
        /// </summary>
        /// <returns>Number of child units or -1 of unknown</returns>
        public int GetChildCount()
            => _instance.GetChildCount();

        /// <summary>
        /// Get parent <see cref="UnitInfo"/> object
        /// </summary>
        /// <returns></returns>
        public UnitInfo GetParent()
            => new UnitInfo(_instance.GetParent());

        /// <summary>
        /// Get Child <see cref="UnitInfo"/> object at index
        /// </summary>
        /// <param name="index"></param>
        /// <returns></returns>
        public UnitInfo GetChild(int index)
            => new UnitInfo(_instance.GetChild(index));

        /// <summary>
        /// Get Child <see cref="UnitInfo"/> object at index
        /// </summary>
        /// <returns></returns>
        public UnitInfo[] GetChildren()
            => _instance.GetChildren().Select(c => new UnitInfo(c)).ToArray();
    }
}
