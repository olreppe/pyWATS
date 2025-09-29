using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Service.MES.Contract;
using System.Diagnostics;
using System.Xml;
using System.Windows.Forms;

namespace Virinco.WATS.Interface.MES.Workflow
{
    /// <summary>
    /// Class that represent a workflow
    /// </summary>
    public class Workflow : MesBase
    {
        /// <summary>
        /// True if connected to server
        /// </summary>
        /// <returns></returns>
        new public bool isConnected()
        {
            return base.isConnected();
        }

        //todo: remove this
        /// <summary>
        /// For internal testing only.
        /// This property getter wil be removed in a forthcoming release! 
        /// </summary>
        public IWorkflowService Service { get { return ServicePool.GetWorkflowService(Env.WCFConfigFile); } }

        private void ShowErrordialog(WorkflowResponse response, bool AlwaysOnTop = true)
        {
            ErrorDialog dlg;
            if (response.InstanceStatus == WorkflowInstanceStatus.ValidationError)
                dlg = new ErrorDialog(this, CultureCode, "Wrong unit process", "Next process for this unit is:", 
                  string.Format("{0}\r\n{1}\r\n(tech. info: {2})",response.Description,response.CurrentActivityName,response.ErrorMessage),AlwaysOnTop);
            else
                dlg = new ErrorDialog(this, CultureCode, "WATS Workflow error", "System error, contact technicihan", response.Description + "\r\n" + response.ErrorMessage,AlwaysOnTop);
            dlg.ShowDialog();
        }

        private Dictionary<string, object> CheckDefaultCulture(Dictionary<string, object> inputValues)
        {
            if (inputValues == null)
                inputValues = new Dictionary<string, object>();
            if (!inputValues.ContainsKey("culture"))
                inputValues.Add("culture", CultureCode);
            return inputValues;
        }

        /// <summary>
        /// Start automated test
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse StartTest(string SerialNumber, string PartNumber, string Operation, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:StartTest");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                        serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/StartTest?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response, AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:StartTest"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// End test with result
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="Result"></param>
        /// <param name="ForceExit"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse EndTest(string SerialNumber, string PartNumber, string Operation, ActivityTestResult Result, bool ForceExit, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:EndTest");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                        serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/EndTest?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Result={Result}&ForceExit={ForceExit}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response,AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:EndTest"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Validate workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Method"></param>
        /// <param name="Name"></param>
        /// <param name="inputValues"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <param name="generateImage"></param>
        /// <returns></returns>
        public WorkflowResponse Validate(string SerialNumber, string PartNumber, ActivityMethod Method, string Name, Dictionary<string, object> inputValues, StatusEnum workflowDefinitionStatus = StatusEnum.Released, bool generateImage = false)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:Validate");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);
                    return
                        serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/Validate?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Method={Method}&Name={Name}&Status={workflowDefinitionStatus}&GenerateImage={generateImage}", inputValues);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:Validate"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Initialize a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Initialize(string SerialNumber, string PartNumber, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:Initialize");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                        serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/Initialize?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response,AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:Initialize"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Performs a Check-In on a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse CheckIn(string SerialNumber, string PartNumber, string Operation, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:CheckIn");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                        serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/CheckIn?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response, AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:CheckIn"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Performs a Check-Out on a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse CheckOut(string SerialNumber, string PartNumber, string Operation, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:CheckOut");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                        serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/CheckOut?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response, AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:CheckOut"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Performs a UserInput on a workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse UserInput(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:UserInput");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                        serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/UserInput?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Result={UserInput}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response, AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:UserInput"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Start repair
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse StartRepair(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:StartRepair");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/StartRepair?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response, AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:StartRepair"); response.SetError(e.Message, null); }
            return response;
        }


        /// <summary>
        /// End repair
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse EndRepair(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:EndRepair");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/EndRepair?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response, AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:EndRepair"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Scrap a unit under repair
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="Operation"></param>
        /// <param name="UserInput"></param>
        /// <param name="inputValues"></param>
        /// <param name="promptOperator"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Scrap(string SerialNumber, string PartNumber, string Operation, string UserInput, Dictionary<string, object> inputValues, bool promptOperator = false, bool AlwaysOnTop = true, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:Scrap");
            try
            {
                if (isConnected())
                {
                    inputValues = CheckDefaultCulture(inputValues);

                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/Scrap?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Operation={Operation}&Status={workflowDefinitionStatus}", inputValues);

                    if (promptOperator && !response.ok)
                        ShowErrordialog(response, AlwaysOnTop);
                }
                else response.SetError("Not connected", "");//NB: Do not set description due to Eltek usage
            }
            catch (Exception e) { Env.LogException(e, "WF:Scrap"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Suspends a workflow 
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Suspend(string SerialNumber, string PartNumber,  StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:Scrap");
            try
            {
                if (isConnected())
                {
                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/Suspend?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Status={workflowDefinitionStatus}",null);
                }
                else response.SetError("Not connected", "");
            }
            catch (Exception e) { Env.LogException(e, "WF:Suspend"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Resumes a suspended workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Resume(string SerialNumber, string PartNumber, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            //Trace.WriteLine("WF:Scrap");
            try
            {
                if (isConnected())
                {
                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/Resume?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Status={workflowDefinitionStatus}", null);
                }
                else response.SetError("Not connected", "");
            }
            catch (Exception e) { Env.LogException(e, "WF:Resume"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Cancels an active workflow
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse Cancel(string SerialNumber, string PartNumber, StatusEnum workflowDefinitionStatus = StatusEnum.Released)
        {
            WorkflowResponse response = new WorkflowResponse();
            try
            {
                if (isConnected())
                {
                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/Cancel?SerialNumber={SerialNumber}&PartNumber={PartNumber}&Status={workflowDefinitionStatus}", null);
                }
                else response.SetError("Not connected", "");
            }
            catch (Exception e) { Env.LogException(e, "WF:Cancel"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Adds unit in a boxbuild
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="ChildSerialNumber"></param>
        /// <param name="ChildPartNumber"></param>
        /// <param name="ActivityName"></param>
        /// <param name="inputValues"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse AddUnit(string SerialNumber, string PartNumber, string ChildSerialNumber, string ChildPartNumber, string ActivityName, Dictionary<string, object> inputValues, StatusEnum workflowDefinitionStatus)
        {
            WorkflowResponse response = new WorkflowResponse();
            try
            {
                if (isConnected())
                {
                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/AddUnit?SerialNumber={SerialNumber}&PartNumber={PartNumber}&ChildSerialNumber={ChildSerialNumber}&ChildPartNumber={ChildPartNumber}&ActivityName={ActivityName}&Status={workflowDefinitionStatus}", inputValues);
                }
                else response.SetError("Not connected", "");
            }
            catch (Exception e) { Env.LogException(e, "WF:AddUnit"); response.SetError(e.Message, null); }
            return response;
        }

        /// <summary>
        /// Removes a sub unit
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="ChildSerialNumber"></param>
        /// <param name="ChildPartNumber"></param>
        /// <param name="ActivityName"></param>
        /// <param name="inputValues"></param>
        /// <param name="workflowDefinitionStatus"></param>
        /// <returns></returns>
        public WorkflowResponse RemoveUnit(string SerialNumber, string PartNumber, string ChildSerialNumber, string ChildPartNumber, string ActivityName, Dictionary<string, object> inputValues, StatusEnum workflowDefinitionStatus)
        {
            WorkflowResponse response = new WorkflowResponse();
            try
            {
                if (isConnected())
                {
                    response =
                       serviceProxy.PostJson<WorkflowResponse>($"api/internal/Workflow/RemoveUnit?SerialNumber={SerialNumber}&PartNumber={PartNumber}&ChildSerialNumber={ChildSerialNumber}&ChildPartNumber={ChildPartNumber}&ActivityName={ActivityName}&Status={workflowDefinitionStatus}", inputValues);
                }
                else response.SetError("Not connected", "");
            }
            catch (Exception e) { Env.LogException(e, "WF:RemoveUnit"); response.SetError(e.Message, null); }
            return response;
        }

    }
}
