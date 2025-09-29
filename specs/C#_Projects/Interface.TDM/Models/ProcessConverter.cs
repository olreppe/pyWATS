using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.Newtonsoft.Json;
using Virinco.Newtonsoft.Json.Linq;

namespace Virinco.WATS.Interface.Models
{
    internal class ProcessPropertiesConverter : JsonConverter
    {
        public override bool CanConvert(Type objectType)
        {
            return (objectType == typeof(RepairType));
        }

        public override object ReadJson(JsonReader reader, Type objectType, object existingValue, JsonSerializer serializer)
        {
            if (reader == null) return null;
            try
            {
                JObject jo = JObject.Load(reader);
                // For now, just reurn as RepairType - no other Subclasses exists...
                return jo.ToObject<RepairType>(serializer);
            }
            catch
            {
                // Unable to parse json, return null
                return null;
            }
        }

        public override bool CanWrite
        {
            get { return false; }
        }

        public override void WriteJson(JsonWriter writer, object value, JsonSerializer serializer)
        {
            //??? implement special writer for
            throw new NotImplementedException();
        }
    }
}
