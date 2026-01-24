extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;

namespace Virinco.WATS.Interface.MES.Production
{
    public class SerialNumberType
    {
        private napi.Production.SerialNumberType _instance;

        internal SerialNumberType(napi.Production.SerialNumberType instance)
        {
            _instance = instance;
        }

        public string Name
        {
            get => _instance.Name;
            set => _instance.Name = value;
        }

        public string Description
        {
            get => _instance.Description;
            set => _instance.Description = value;
        }

        public string Format
        {
            get => _instance.Format;
            set => _instance.Format = value;
        }

        public string Regex
        {
            get => _instance.Regex;
            set => _instance.Regex = value;
        }
    }
}
