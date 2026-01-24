extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;

namespace Virinco.WATS.Interface
{
  

    /// <summary>
    /// This steptype supports steps that is not a test
    /// Depending on the Step
    /// </summary>
    public class GenericStep : Step
    {
        internal napi.GenericStep _instance;
        internal GenericStep(napi.GenericStep instance) : base(instance) { _instance = instance; }

        // No additional properties
    }
}
