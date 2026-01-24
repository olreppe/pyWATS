extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System.Collections.Generic;
using System;
using System.Linq;

namespace Virinco.WATS.Interface.MES.Product
{
    public class KeyValue
    {
        internal napi.Product.KeyValue _instance;

        internal KeyValue(napi.Product.KeyValue kv)
        {
            this._instance = kv;
        }

        public string key
        {
            get => _instance.key;
            set => _instance.key = value;
        }
        public string value
        {
            get => _instance.value;
            set => _instance.value = value;
        }
    }

    public class ProductInfoJson
    {
        internal napi.Product.ProductInfoJson _instance;

        internal ProductInfoJson(napi.Product.ProductInfoJson pijson)
        {
            this._instance = pijson;
        }

        public Guid ProductId
        {
            get => _instance.ProductId;
            set => _instance.ProductId = value;
        }

        public string PartNumber
        {
            get => _instance.PartNumber;
            set => _instance.PartNumber = value;
        }

        public string Name
        {
            get => _instance.Name;
            set => _instance.Name = value;
        }

        public string Revision
        {
            get => _instance.Revision;
            set => _instance.Revision = value;
        }

        public int Quantity
        {
            get => _instance.Quantity;
            set => _instance.Quantity = value;
        }

        public int? hlevel
        {
            get => _instance.hlevel;
            set => _instance.hlevel = value;
        }

        public Guid ProductRevisionId
        {
            get => _instance.ProductRevisionId;
            set => _instance.ProductRevisionId = value;
        }

        public Guid? ParentProductRevisionId
        {
            get => _instance.ParentProductRevisionId;
            set => _instance.ParentProductRevisionId = value;
        }

        public string RevisionName
        {
            get => _instance.RevisionName;
            set => _instance.RevisionName = value;
        }

        public string PathStr
        {
            get => _instance.PathStr;
            set => _instance.PathStr = value;
        }

        public Guid? ProductRevisionRelationId
        {
            get => _instance.ProductRevisionRelationId;
            set => _instance.ProductRevisionRelationId = value;
        }

        public string ProductData
        {
            get => _instance.ProductData;
            set => _instance.ProductData = value;
        }

        public string RevisionData
        {
            get => _instance.RevisionData;
            set => _instance.RevisionData = value;
        }

        public List<KeyValue> ProductSettings
        {
            get { return _instance.ProductSettings.Select(s => new KeyValue(s)).ToList(); }
            set { _instance.ProductSettings = value.Select(s => s._instance).ToList(); }
        }

        public List<KeyValue> RevisionSettings
        {
            get { return _instance.RevisionSettings.Select(s => new KeyValue(s)).ToList(); }
            set { _instance.RevisionSettings = value.Select(s => s._instance).ToList(); }
        }

        public string RevisionMask
        {
            get => _instance.RevisionMask;
            set => _instance.RevisionMask = value;
        }

        public string ProductDescription
        {
            get => _instance.ProductDescription;
            set => _instance.ProductDescription = value;
        }

        public string RevisionDescription
        {
            get => _instance.RevisionDescription;
            set => _instance.RevisionDescription = value;
        }

        public string Category
        {
            get => _instance.Category;
            set => _instance.Category = value;
        }
    }
}