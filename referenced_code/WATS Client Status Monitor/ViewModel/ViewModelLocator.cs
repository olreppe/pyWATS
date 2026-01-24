/*
  In App.xaml:
  <Application.Resources>
      <vm:ViewModelLocatorTemplate xmlns:vm="clr-namespace:MvvmLight2.ViewModel"
                                   x:Key="Locator" />
  </Application.Resources>
  
  In the View:
  DataContext="{Binding Source={StaticResource Locator}, Path=ViewModelName}"
  
  OR (WPF only):
  
  xmlns:vm="clr-namespace:MvvmLight2.ViewModel"
  DataContext="{Binding Source={x:Static vm:ViewModelLocatorTemplate.ViewModelNameStatic}}"
*/

namespace Virinco.WATS.Client.StatusMonitor.ViewModel
{
    /// <summary>
    /// This class contains static references to all the view models in the
    /// application and provides an entry point for the bindings.
    /// <para>
    /// Use the <strong>mvvmlocatorproperty</strong> snippet to add ViewModels
    /// to this locator.
    /// </para>
    /// <para>
    /// In Silverlight and WPF, place the ViewModelLocatorTemplate in the App.xaml resources:
    /// </para>
    /// <code>
    /// &lt;Application.Resources&gt;
    ///     &lt;vm:ViewModelLocatorTemplate xmlns:vm="clr-namespace:MvvmLight2.ViewModel"
    ///                                  x:Key="Locator" /&gt;
    /// &lt;/Application.Resources&gt;
    /// </code>
    /// <para>
    /// Then use:
    /// </para>
    /// <code>
    /// DataContext="{Binding Source={StaticResource Locator}, Path=ViewModelName}"
    /// </code>
    /// <para>
    /// You can also use Blend to do all this with the tool's support.
    /// </para>
    /// <para>
    /// See http://www.galasoft.ch/mvvm/getstarted
    /// </para>
    /// <para>
    /// In <strong>*WPF only*</strong> (and if databinding in Blend is not relevant), you can delete
    /// the Main property and bind to the ViewModelNameStatic property instead:
    /// </para>
    /// <code>
    /// xmlns:vm="clr-namespace:MvvmLight2.ViewModel"
    /// DataContext="{Binding Source={x:Static vm:ViewModelLocatorTemplate.ViewModelNameStatic}}"
    /// </code>
    /// </summary>
    public class ViewModelLocator
    {

        /// <summary>
        /// Initializes a new instance of the ViewModelLocator class.
        /// </summary>
        public ViewModelLocator()
        {
            ////if (ViewModelBase.IsInDesignModeStatic)
            ////{
            ////    // Create design time view models
            ////}
            ////else
            ////{
            ////    // Create run time view models
            ////}         
        }

        //COMMON
        private static TDM_ClientConfig _api;
        //<if:TDM x:Key="api" xmlns:if="clr-namespace:Virinco.WATS.Interface;assembly=Virinco.WATS.Interface.TDM" />

        /// <summary>
        /// Gets the Main property.
        /// </summary>
        internal static TDM_ClientConfig TDMAPIStatic
        {
            get
            {
                if (_api == null) { CreateTDMAPI(); }
                return _api;
            }
        }

        /// <summary>
        /// Gets the Main property.
        /// </summary>
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Performance",
            "CA1822:MarkMembersAsStatic",
            Justification = "This non-static member is needed for data binding purposes.")]
        internal TDM_ClientConfig TDMAPI
        {
            get { return TDMAPIStatic; }
        }

        /// <summary>
        /// Provides a deterministic way to delete the Main property.
        /// </summary>
        public static void ClearTDMAPI()
        {
            if (_api != null) _api.Dispose();
            _api = null;
        }

        /// <summary>
        /// Provides a deterministic way to create the Main property.
        /// </summary>
        public static void CreateTDMAPI()
        {
            if (_api == null)
            {
                _api = new TDM_ClientConfig();
                _api.InitializeAPI(Interface.TDM.InitializationMode.Syncronous, false);
            }
        }


        //Client Monitor specific - Status Monitor
        private static ClientMonitorViewModel _status;
        public static ClientMonitorViewModel StatusStatic
        {
            get
            {
                if (_status == null) { CreateStatus(); }
                return _status;
            }
        }
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Performance",
            "CA1822:MarkMembersAsStatic",
            Justification = "This non-static member is needed for data binding purposes.")]
        public ClientMonitorViewModel Status
        {
            get { return StatusStatic; }
        }

        /// <summary>
        /// Provides a deterministic way to delete the Main property.
        /// </summary>
        public static void ClearStatus()
        {
            if (_status != null) _status.Dispose();
            _status = null;
        }
        /// <summary>
        /// Provides a deterministic way to create the Main property.
        /// </summary>
        public static void CreateStatus()
        {
            if (_status == null) { _status = new ClientMonitorViewModel(TDMAPIStatic); }
        }


        //Log UserControl specific - Log Tab
        private static LogViewModel _log;
        public static LogViewModel LogStatic
        {
            get
            {
                if (_log == null) { CreateLog(); }
                return _log;
            }
        }
        [System.Diagnostics.CodeAnalysis.SuppressMessage("Microsoft.Performance",
            "CA1822:MarkMembersAsStatic",
            Justification = "This non-static member is needed for data binding purposes.")]
        public LogViewModel Log
        {
            get { return LogStatic; }
        }

        /// <summary>
        /// Provides a deterministic way to delete the Main property.
        /// </summary>
        public static void ClearLog()
        {
            if (_log != null) _log.Dispose();
            _log = null;
        }
        /// <summary>
        /// Provides a deterministic way to create the Main property.
        /// </summary>
        public static void CreateLog()
        {
            if (_log == null) { _log = new LogViewModel(ViewModel.ViewModelLocator.TDMAPIStatic); }
        }


        /// <summary>
        /// Cleans up all the resources.
        /// </summary>
        public static void Cleanup()
        {
            ClearTDMAPI();
            ClearStatus();
            ClearLog();
        }
    }
}