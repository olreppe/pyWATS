using System.Runtime.CompilerServices;

// Type forwarding from WATS-Core to WATS Client API
// This assembly now only contains type forwards to redirect requests to the WATS Client API assembly

// Core exception and logging types that have been moved to WATS Client API
[assembly: TypeForwardedTo(typeof(Virinco.WATS.WATSException))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.WATSLogMessage))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.WATSLogItem))]

// Core utility classes that have been moved to WATS Client API
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Env))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Extensions))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Utilities))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Registry))]

// Configuration types that have been moved to WATS Client API
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Configuration.ClientSettings))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Configuration.ProxySettings))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Configuration.ProxyMethodEnum))]

// Security types that have been moved to WATS Client API
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Security.SimpleAes))]

// REST types that have been moved to WATS Client API
[assembly: TypeForwardedTo(typeof(Virinco.WATS.REST.ServiceProxy))]

// Reporting types that have been moved to WATS Client API
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Reporting.watsfilter))]

//// Trace listeners that have been moved to WATS Client API
//[assembly: TypeForwardedTo(typeof(Virinco.WATS.RollingTextWriterTraceListener))]

// Enum types that have been moved to WATS Client API
[assembly: TypeForwardedTo(typeof(Virinco.WATS.ClientFunctions))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.ClientLicenseTypes))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.ClientIdentifierType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Logging.LogCategory))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Logging.LogSeverity))]

//// Windows Location Service that has been moved to WATS Client API
//[assembly: TypeForwardedTo(typeof(Virinco.WATS.WindowsLocationService))]

//// Interface types that have been moved to WATS Client API
//[assembly: TypeForwardedTo(typeof(Virinco.WATS.Interface.CustomClientChannel<>))]

// Schema types from Converters.cs
[assembly: TypeForwardedTo(typeof(converters))]
[assembly: TypeForwardedTo(typeof(convertersConverter))]
[assembly: TypeForwardedTo(typeof(ParametersCollection))]
[assembly: TypeForwardedTo(typeof(ParametersCollectionParameter))]

// Schema types from WATS Report.designer.cs (WRML namespace)
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Reports))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.WATSReport))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.UUR_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.UUT_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Process_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Step_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Step_typeLoop))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.NumericLimit_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.StringValue_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.PassFail_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Failures_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Binary_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Binary_typeData))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Chart_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.SPCData_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.AdditionalResults_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.AdditionalData_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.ReportInfo_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.MiscInfo_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.PartInfo_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Asset_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.AssetStats_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.Callexe_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.MessagePopup_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.PropertyLoader_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.SequenceCall_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.ReportUnitHierarchy_type))]

// Enum types from WATS Report.designer.cs
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.ReportType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.ReportResultType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.MeasurementResultType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.StepGroup_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WRML.StepResultType))]

// Schema types from WATS WSXF Report.cs (WSXF namespace)
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Reports))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.WATSReport))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.UUR_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.UUT_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Process_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Step_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Step_typeLoop))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.NumericLimit_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.StringValue_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.PassFail_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Failures_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Binary_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Binary_typeData))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Chart_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.ChartSeries_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.SPCData_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.AdditionalResults_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.AdditionalData_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.ReportInfo_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.MiscInfo_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.PartInfo_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Asset_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Attachment_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.Callexe_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.MessagePopup_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.PropertyLoader_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.SequenceCall_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.ReportUnitHierarchy_type))]

// Enum types from WATS WSXF Report.cs
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.ReportType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.ReportResultType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.MeasurementResultType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.StepGroup_type))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.StepResultType))]
[assembly: TypeForwardedTo(typeof(Virinco.WATS.Schemas.WSXF.ChartSeriesDataType))]