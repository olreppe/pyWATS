using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Service.MES.Contract;
using Virinco.WATS.Interface.MES.Production;
using Virinco.WATS.Interface.MES.Software;
using Virinco.WATS.Interface.MES.Asset;
using Virinco.WATS.Interface.MES.Workflow;
using Virinco.WATS.Interface.MES.Product;

namespace Virinco.WATS.Interface.MES
{
    /// <summary>
    /// Holding references to all MES components.
    /// </summary>
    public class MesInterface
    {

        private string _defaultCultureCode = "en";
        /// <summary>
        /// Default culture code to use. If not specified, en is used.
        /// </summary>
        public string DefaultCultureCode 
        { 
            get{return _defaultCultureCode;} set{_defaultCultureCode = value;}
        }        

        Production.Production _production = null;
        /// <summary>
        /// Gets the MES Production module.
        /// </summary>
        public Production.Production Production
        {
            get {
                if (_production == null)
                {
                    _production = new Production.Production();
                    _production.CultureCode = DefaultCultureCode;
                }
                return _production;
            }
        }

        Product.Product _product = null;
        /// <summary>
        /// Gets the MES Product module.
        /// </summary>
        public Product.Product Product
        {
            get
            {
                if (_product == null)
                {
                    _product = new Product.Product();
                    _product.CultureCode = DefaultCultureCode;
                }
                return _product;
            }
        }

        Software.Software _software = null;
        /// <summary>
        /// Gets the MES Software module
        /// </summary>
        public Software.Software Software
        {
            get
            {
                if (_software == null)
                {
                    _software = new Software.Software();
                    _software.CultureCode = DefaultCultureCode;
                }
                return _software;
            }
        }


        Asset.AssetHandler _asset = null;
        /// <summary>
        /// Gets the MES Asset module
        /// </summary>
        public Asset.AssetHandler Asset
        {
            get
            {
                if (_asset == null)
                {
                    _asset = new Asset.AssetHandler();
                    _asset.CultureCode = DefaultCultureCode;
                }
                return _asset;
            }
        }

        Workflow.Workflow _workflow = null;
        /// <summary>
        /// Gets the MES Workflow module
        /// </summary>
        public Workflow.Workflow Workflow
        {
            get
            {
                if (_workflow == null)
                {
                    _workflow = new Workflow.Workflow();
                    _workflow.CultureCode = DefaultCultureCode;
                }
                return _workflow;
            }
        }
            
    }
}
