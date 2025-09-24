using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.Newtonsoft.Json;

namespace Virinco.WATS.Interface.MES.Product
{
    public class KeyValue
    {
        public string key { get; set; }
        public string value { get; set; }
    }

    public class ProductInfoJson
    {
        public Guid ProductId { get; set; }

        public string PartNumber { get; set; }

        public string Name { get; set; }

        public string Revision { get; set; }

        public int Quantity { get; set; }

        public int? hlevel { get; set; }

        public Guid ProductRevisionId { get; set; }

        public Guid? ParentProductRevisionId { get; set; }

        public string RevisionName { get; set; }

        public string PathStr { get; set; }

        public Guid? ProductRevisionRelationId { get; set; }

        public string ProductData { get; set; }

        public string RevisionData { get; set; }

        public List<KeyValue> ProductSettings { get; set; }

        public List<KeyValue> RevisionSettings { get; set; }

        public string RevisionMask { get; set; }

        public string ProductDescription { get; set; }

        public string RevisionDescription { get; set; }

        public string Category { get; set; }
    }
}