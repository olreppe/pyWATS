using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.ClientService
{

    internal class ClientIPC : IClientIPC
    {
        private ClientSvc service;
        internal ClientIPC(ClientSvc service)
        {
            this.service = service;
        }

        public Interface.APIStatusType GetAPIStatus()
        {
            return service.api.Status;
        }
    }
}
