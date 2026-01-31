using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Interface used for converting files into WATS Reports using WATS TDM API.
    /// </summary>
    /// <remarks>
    /// Previously defined method Interface.Report ImportReport(TDM, System.IO.FileInfo) is now removed from this interface.
    /// </remarks>
    public interface IReportConverter
    {
        //Interface.Report ImportReport(TDM api, System.IO.FileInfo file);
        /// <summary>
        /// Called from WATS Client Service when incoming files matches configured converter filters
        /// Use constructor ReportConverter(IDictionary(string string) args)
        /// </summary>
        /// <param name="api">Initialized WATS TDM API Instance</param>
        /// <param name="file">An exclusively locked file stream, opened readonly and ready for use</param>
        /// <returns>If return value contains an instance to a Report, the calling client will (auto-)submit the report. If null is returned the implementation is responsible for report submission</returns>
        Interface.Report ImportReport(TDM api, System.IO.Stream file);
        /// <summary>
        /// Clean up after import. e.g. delete linked or "external" import files etc.
        /// Called on the same instance, but after submission and without a valid TDM API
        /// </summary>
        void CleanUp();
    }

    /// <summary>
    /// New version of the converter interface
    /// Use Default constructor to retrieve default ConverterParameters
    /// </summary>
    public interface IReportConverter_v2 : IReportConverter
    {
        /// <summary>
        /// Exposes Default parmeters to the converter. Will be used by the client configurator.
        /// </summary>
        Dictionary<string, string> ConverterParameters { get; }
    }
}
