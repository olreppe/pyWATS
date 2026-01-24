using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.ServiceModel;

namespace Virinco.WATS.ClientService
{
    [ServiceContract(Namespace = "http://www.virinco.com/wats/ClientPipe")]
    public interface IClientIPC
    {
        [OperationContract]
        Interface.APIStatusType GetAPIStatus();
    }
}
