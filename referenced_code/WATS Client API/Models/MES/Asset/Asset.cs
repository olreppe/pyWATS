//using System;
//using System.Collections.Generic;
//using System.Linq;

//namespace Virinco.WATS.Interface.MES.Asset
//{
//    /// <summary>
//    /// Class that represent an asset. An asset is normally a device used in testing that can be controlled for service maintenance, running count etc.
//    /// </summary>
//    public class Asset
//    {
//        /// <summary>
//        /// Unique asset Id
//        /// </summary>
//        public string AssetId { get; set; }

//        /// <summary>
//        /// Unique serial number
//        /// </summary>
//        public string SerialNumber { get; set; }

//        /// <summary>
//        /// Identity for an assets parent. Can be null
//        /// </summary>
//        public string ParentAssetId { get; set; }

//        /// <summary>
//        /// Serial number for an assets parent. Can be null
//        /// </summary>
//        public string ParentSerialNumber { get; set; }

//        /// <summary>
//        /// Alternate name of asset
//        /// </summary>
//        public string AssetName { get; set; }

//        /// <summary>
//        /// Asset part number
//        /// </summary>
//        public string PartNumber { get; set; }

//        /// <summary>
//        /// Asset part revision
//        /// </summary>
//        public string Revision { get; set; }

//        /// <summary>
//        /// Asset description
//        /// </summary>
//        public string Description { get; set; }

//        /// <summary>
//        /// Asset location
//        /// </summary>
//        public string Location { get; set; }

//        /// <summary>
//        /// Id of asset type
//        /// </summary>
//        public Guid TypeId { set; get; }

//        /// <summary>
//        /// Asset states
//        /// </summary>
//        public State State { get; set; }

//        /// <summary>
//        /// Type of Asset
//        /// </summary>
//        public AssetType AssetType { get; set; }

//        /// <summary>
//        /// ToString that contains serial number, parent serial number, name, partNumber and state for an asset.
//        /// </summary>
//        /// <returns></returns>
//        public string ToString()
//        {
//            return $"SerialNumber: {SerialNumber}, ParentSerialNumber: {ParentSerialNumber}, Name:{AssetName}, Partnumber:{PartNumber}, Status: {State}";
//        }

//        /// <summary>
//        /// AssetStatus object.
//        /// </summary>
//        public AssetStatus AssetStatus;

//        /// <summary>
//        /// TimeStamp for when the asset was created.
//        /// </summary>
//        public DateTime FirstSeenDate { get; set; }

//        /// <summary>
//        /// Timestamp for when the Asset was last seen/used.
//        /// </summary>
//        public DateTime? LastSeenDate { get; set; }

//        /// <summary>
//        /// Timestamp for when the Asset was last maintained
//        /// </summary>
//        public DateTime? LastMaintenanceDate { get; set; }

//        /// <summary>
//        /// Timestamp for when the Asset was last calibrated
//        /// </summary>
//        public DateTime? LastCalibrationDate { get; set; }

//        /// <summary>
//        /// Total asset usage
//        /// </summary>
//        public int TotalCount { get; set; }

//        /// <summary>
//        /// Running count for an instrument between each calibration.
//        /// </summary>
//        public int RunningCount { get; set; }

//        /// <summary>
//        /// List of asset tags and their values
//        /// </summary>
//        public List<KeyValuePair<string, string>> Tags { get; set; } = new List<KeyValuePair<string, string>>();
//    }

//    //Class for converting XmlData to Tags without exposing XmlData property...
//    internal class InternalAsset : Asset
//    {
//        public string XmlData 
//        { 
//            set
//            {
//                if (!string.IsNullOrEmpty(value))
//                {
//                    var root = System.Xml.Linq.XElement.Parse(value);
//                    foreach (var tag in root.Elements())
//                    {
//                        if (!Tags.Any(t => t.Key == tag.Name.LocalName))
//                            Tags.Add(new KeyValuePair<string, string>(tag.Name.LocalName, tag.Attribute("Value")?.Value));
//                    }
//                }
//            }
//        }
//    }
//}