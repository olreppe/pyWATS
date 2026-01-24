using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Client.Configurator
{
    public interface IPageViewModel
    {
        string Name { get; }
    }

    public interface IPageViewModel_v2 : IPageViewModel
    {
        void Initialize();

        void Uninitialize();
    }
}
