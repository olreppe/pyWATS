using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS
{
 
}

namespace Virinco.WATS.ClientService
{
    public enum WATSServiceCustomCommand
    {
        ReloadConfig = 0x80,
        CheckConnection = 0x81,
        SubmitConnectionTestReport = 0x82
    }

    public enum ConverterStateEnum
    {
        Created = 0,
        Running = 1,
        Failed = 2,
        Disposing = 3,
        FailedToStart = 4,
        NotStarted = 5,
    }
}