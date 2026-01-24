extern alias newclientapi;

namespace Virinco.WATS.Interface.MES
{
    /// <summary>
    /// Holding references to all MES components.
    /// </summary>
    public class MesInterface
    {
        private readonly newclientapi::Virinco.WATS.Interface.MES.MesInterface _instance = new newclientapi::Virinco.WATS.Interface.MES.MesInterface();
        public string DefaultCultureCode
        {
            get => _instance.DefaultCultureCode;
            set => _instance.DefaultCultureCode = value;
        }

        /// <summary>
        /// Gets the MES Production module.
        /// </summary>
        public Production.Production Production
        {
            get => new Production.Production(_instance.Production);
        }

        /// <summary>
        /// Gets the MES Product module.
        /// </summary>
        public Product.Product Product
        {
            get => new Product.Product(_instance.Product);
        }

        /// <summary>
        /// Gets the MES Software module
        /// </summary>
        public Software.Software Software
        {
            get => new Software.Software(_instance.Software);
        }

        /// <summary>
        /// Gets the MES Asset module
        /// </summary>
        public Asset.AssetHandler Asset
        {
            get => new Asset.AssetHandler(_instance.Asset);
        }

        /// <summary>
        /// Gets the MES Workflow module
        /// </summary>
        public Workflow.Workflow Workflow
        {
            get => new Workflow.Workflow(_instance.Workflow);
        }
    }
}
