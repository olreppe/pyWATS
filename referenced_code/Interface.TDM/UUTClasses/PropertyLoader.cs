extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Teststand property loader
    /// </summary>
    public class PropertyLoaderStep : Step
    {
        internal napi.PropertyLoaderStep _instance;
        internal PropertyLoaderStep(napi.PropertyLoaderStep instance) : base(instance) { _instance = instance; }

        public short PropertiesRead
        {
            get => _instance.PropertiesRead;
            set => _instance.PropertiesRead = value;
        }

        public short PropertiesApplied
        {
            get => _instance.PropertiesApplied;
            set => _instance.PropertiesApplied = value;
        }
    }
}
