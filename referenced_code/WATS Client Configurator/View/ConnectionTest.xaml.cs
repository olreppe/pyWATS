using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;
using Virinco.WATS.Interface;
using System.Windows.Threading;
using System.Threading;
using Virinco.WATS.Interface.MES;
using System.ComponentModel;
using System.ServiceProcess;

namespace Virinco.WATS.Client.Configurator.View
{
    /// <summary>
    /// Interaction logic for ConnectionTest.xaml
    /// </summary>
    public partial class ConnectionTest : Window
    {
        public ConnectionTest(bool testTdm, bool testMes)
        {
            InitializeComponent();
            this.testTdm = testTdm;
            tdm = new TDM_ClientConfig();
            tdm.InitializeAPI(TDM.InitializationMode.NoConnect, false);
            this.BaseAddress = tdm.TargetURL;
            if (tdm.ClientState == ClientStateType.NotConfigured)
            {
                // Run authorize client to continue...
                AuthorizeClient popup = new AuthorizeClient();
                var res = popup.ShowDialog();
                if (res.HasValue && res.Value && popup.DialogResult.HasValue && popup.DialogResult.Value)
                {
                    // Test & Save
                    tdm.RegisterClient(BaseAddress, popup.authUsername, popup.authUserpass);
                }
                else
                {
                    //this.DialogResult = false;
                    this.Close();
                }
            }
            if (testMes)
            {
                mes = new MesInterface();
                //mes.Production.StartTraceToEventLog();
            }
        }

        private bool testTdm;
        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            textBlockApiVersions.Text = "TDM API Version: " + Utilities.GetMSIVersionString(System.Reflection.Assembly.GetAssembly(tdm.GetType()).GetName().Version);
            if (mes != null)
                textBlockApiVersions.Text += "\r\nMES API Version: " + Utilities.GetMSIVersionString(System.Reflection.Assembly.GetAssembly(mes.GetType()).GetName().Version);
            BackgroundWorker worker = new BackgroundWorker();
            worker.WorkerReportsProgress = true;
            worker.ProgressChanged += new ProgressChangedEventHandler(worker_ProgressChanged);
            worker.DoWork += new DoWorkEventHandler(worker_DoWork);
            worker.RunWorkerAsync();
        }

        private TDM_ClientConfig tdm;
        private MesInterface mes;

        void worker_ProgressChanged(object sender, System.ComponentModel.ProgressChangedEventArgs e)
        {
            progressBar1.Value = e.ProgressPercentage;
        }

        void worker_DoWork(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            BackgroundWorker worker = (BackgroundWorker)sender;
            try
            {
                worker.ReportProgress(0);

                addString("Initializing API.", 20, worker);
                addString($"\r\nConnecting to server {tdm.TargetURL}.", 20, worker);
                tdm.InitializeAPI(TDM.InitializationMode.Syncronous, false);
                addString($"\r\nServer status {tdm.Status}.", 60, worker);
                addString($"\r\nServer version {tdm.ServerVersion}.", 60, worker);

                if (mes != null)
                {
                    addString("\r\nQuerying server for MES modules.", 60, worker);

                    // Getting available MES Modules
                    mes.Production.GetMesServerSettings(out _, out bool[] boolValues, out _, null, new[] 
                    { 
                        "IsProductEnabled", 
                        "IsProductionEnabled", 
                        "IsSoftwareEnabled", 
                        "IsWorkflowEnabled" 
                    }, null);
                
                    var modules = new List<string>();
                    if (boolValues[0])
                        modules.Add("Product");
                    if (boolValues[1])
                        modules.Add("Production");
                    if (boolValues[2])
                        modules.Add("Software");
                    if (boolValues[3])
                        modules.Add("Workflow");

                    if (modules.Any())                
                        addString($"\r\nEnabled MES modules: {string.Join(", ", modules)}.", 90, worker);                
                    else                
                        addString("\r\nNo MES modules are enabled on the server.", 90, worker);                
                }

                if (tdm.Status == APIStatusType.Online)                
                    addString("\r\nWATS is connected.", 100, worker);
                else
                {
                    addString("\r\nWATS has connection problems.", 100, worker);
                    RestartService();
                }                
                
                serviceRecheck();
            }
            catch
            {
                addString("\r\nWATS has connection problems.", 100, worker);
                RestartService();
            }
        }

        private void RestartService()
        {
            try
            {
                using (var ctrl = new Configuration.ClientServiceController())
                {
                    ctrl.Stop(TimeSpan.FromMilliseconds(10000));
                    ctrl.Start(TimeSpan.FromMilliseconds(10000));
                }
            }
            catch (Exception ex)
            {
                Env.LogException(ex, "Failed to restart WATS Client Service after failed connection test.");
            }
        }

        private void serviceRecheck()
        {
            try
            {
                using (var svc = new Configuration.ClientServiceController())
                {
                    if (svc.Service != null)
                        svc.Service.ExecuteCommand((int)Virinco.WATS.ClientService.WATSServiceCustomCommand.CheckConnection);
                }
            }
            catch (Exception ex)
            {
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Information, 0, new WATSLogItem() { ex = ex, Message = "Failed to send CheckConnection message to local WATS Service." });
            }
        }

        void addString(string value, int progress, BackgroundWorker worker)
        {
            this.Dispatcher.Invoke((Action)(() => { textBox1.AppendText(value); textBox1.ScrollToEnd(); }));
            worker.ReportProgress(progress);
        }

        private void buttonOK_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }


        public string BaseAddress { get; internal set; }

        private void button1_Click(object sender, RoutedEventArgs e)
        {
            //Test Connection
            try
            {
                BackgroundWorker worker = new BackgroundWorker();
                worker.WorkerReportsProgress = true;
                worker.ProgressChanged += new ProgressChangedEventHandler(worker_ProgressChanged);
                worker.DoWork += new DoWorkEventHandler(SendSimpleUUT);
                worker.RunWorkerAsync();
            }
            catch { }
        }

        private void button2_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                //Submit Advanced UUT
                BackgroundWorker worker = new BackgroundWorker();
                worker.WorkerReportsProgress = true;
                worker.ProgressChanged += new ProgressChangedEventHandler(worker_ProgressChanged);
                worker.DoWork += new DoWorkEventHandler(SendAdvancedUUT);
                worker.RunWorkerAsync();                
            }
            catch { }
        }

        private void SendAdvancedUUT(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            var worker = (BackgroundWorker)sender;
            try
            {
                worker.ReportProgress(0);

                addString("\r\n\r\nGenerating advanced UUT.", 50, worker);

                try
                {
                    _ = tdm.GetOperationType(10);
                }
                catch (Exception ex)
                {
                    Env.LogException(ex, "Failed to generate advanced UUT from ConnectionTest.");
                    addString("\r\nCould not generate advanced UUT: Test Operation 'SW Debug' (code: 10) is missing. Possible reasons:", 100, worker);
                    addString("\r\n- Downloading processes from WATS has failed. Contact support for help.", 100, worker);
                    addString("\r\n- SW Debug (code: 10) has been deactivated in the WATS Control Panel.", 100, worker);
                    addString("\r\nDetailed error report in wats.log.", 100, worker);

                    return;
                }

                var report = new ExampleReport();
                var uut = report.GenerateExampleUUT(tdm);
                addString($"\r\nSN: {uut.SerialNumber}, PN: {uut.PartNumber}, Rev: {uut.PartRevisionNumber}, Test operation: {uut.OperationType.Name} ({uut.OperationType.Code})", 50, worker);

                addString("\r\nSubmitting advanced UUT.", 80, worker);
                if (tdm.Submit(SubmitMethod.Online, uut))
                    addString("\r\nSuccessfully submitted advanced UUT.", 100, worker);
                else
                    addString("\r\nFailed to submit advanced UUT.", 100, worker);
            }
            catch (Exception ex)
            {
                Env.LogException(ex, "Failed to submit advanced UUT from ConnectionTest.");
                addString($"\r\nCould not submit advanced UUT: {ex.Message}", 100, worker);
                addString("\r\nDetailed error report in wats.log.", 100, worker);
            }
        }

        private void SendSimpleUUT(object sender, System.ComponentModel.DoWorkEventArgs e)
        {
            var worker = (BackgroundWorker)sender;
            try
            {
                try
                {
                    _ = tdm.GetOperationType(10);
                }
                catch (Exception ex)
                {
                    Env.LogException(ex, "Failed to generate simple UUT from ConnectionTest.");
                    addString("\r\nCould not generate simple UUT: Test Operation 'SW Debug' (code: 10) is missing. Possible reasons:", 100, worker);
                    addString("\r\n- Downloading processes from WATS has failed. Contact support for help.", 100, worker);
                    addString("\r\n- SW Debug (code: 10) has been deactivated in the WATS Control Panel.", 100, worker);
                    addString("\r\nDetailed error report in wats.log.", 100, worker);
                }

                var uut = tdm.CreateUUTReport("Operator", "WATS API TEST", "1", "123123456789", "10", "TestSequence", "1.0.0");
                uut.AddUUTPartInfo("Controller", "123456AH", "API12345", "3.4");
                uut.AddMiscUUTInfo("Misc", "stringvalue", 123);
                uut.GetRootSequenceCall().AddNumericLimitStep("Num1").AddTest(1, CompOperatorType.LT, 2, "V");
                addString($"\r\nSN: {uut.SerialNumber}, PN: {uut.PartNumber}, Rev: {uut.PartRevisionNumber}, Test operation: {uut.OperationType.Name} ({uut.OperationType.Code})", 50, worker);

                addString("\r\nSubmitting simple UUT.", 75, worker);
                string filePath = System.IO.Path.Combine(tdm.ReportsDirectory, $"{uut.ReportId}.ConnectionTest");
                var r = new Schemas.WRML.Reports();
                r.Report.Add(tdm.GetAsWRML(uut));
                using (System.Xml.XmlWriter writer = System.Xml.XmlWriter.Create(filePath))
                    new System.Xml.Serialization.XmlSerializer(typeof(Schemas.WRML.Reports)).Serialize(writer, r);

                //Loads the report from file, submits online, and deletes the file.
                using (var ctrl = new Configuration.ClientServiceController())
                    ctrl.Service.ExecuteCommand((int)ClientService.WATSServiceCustomCommand.SubmitConnectionTestReport);

                //Wait 10 seconds for file to be deleted.
                for (int i = 0; i < 10; i++)
                {
                    if (!System.IO.File.Exists(filePath))
                        break;

                    worker.ReportProgress(75 + (i * 2));
                    Thread.Sleep(1000);
                }

                if (!System.IO.File.Exists(filePath))
                    addString("\r\nSuccessfully submitted simple UUT.", 95, worker);
                else
                {
                    addString("\r\nFailed to submit UUT.", 95, worker);
                    addString("\r\nDetailed error report in wats.log.", 100, worker);
                    System.IO.File.Delete(filePath);
                }

                addString($"\r\nPending reports: {tdm.GetPendingReportCount()}", 100, worker);                
            }
            catch (Exception ex)
            {
                Env.LogException(ex, "Failed to submit simple UUT from ConnectionTest.");
                addString($"\r\nCould not submit simple UUT: {ex.Message}", 100, worker);
                addString("\r\nDetailed error report in wats.log.", 100, worker);
            }            
        }
    }
}
