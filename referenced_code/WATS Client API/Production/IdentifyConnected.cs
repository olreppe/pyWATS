using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Virinco.WATS.Service.MES.Contract;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Versioning;

namespace Virinco.WATS.Interface.MES.Production
{
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    internal partial class IdentifyConnected : Form
    {
        Production apiRef;
        Workflow.Workflow wfApi;
        bool includeTestoperation, selectTestOperation;
        public bool DisplayTreeView = true;
        public UnitInfo UnitInfo { get; set; }
        public Unit_Phase UnitPhase;
        public bool Continue = true;
        public string PartNumber;
        public Process TestOperation;
        public bool useWorkflow = false;
        public StatusEnum wfStatus = StatusEnum.Released;
        public Dictionary<string, object> ctx;

        public IdentifyConnected(Production apiRef, bool DisplayTreeView, string SerialNumber, string PartNumber, Process SelectedTestOperation, bool IncludeTestOperation, bool SelectTestOperation, string CustomText, bool AlwaysOnTop, bool UseWorkflow, StatusEnum WorkflowStatus, Dictionary<string, object> context = null)
        {
            InitializeComponent();
            this.Shown += ActivateAndFocus;
            this.TopMost = AlwaysOnTop;
            if (AlwaysOnTop)
            {
                this.Leave += ActivateAndFocus;
                this.Deactivate += ActivateAndFocus;
            }

            string[] trans = apiRef.TranslateArray(new[] {
                "Search",
                "Search Again",
                "Stop",
                "Identify UUT",
                "Serial Number",
                "Test Operation",          
                "Part Number",
                "Revision", 
                "Batch Number",
                "Start"
            });

            //Paramters from SequenceContext etc...
            ctx = context;
            buttonOK.Text = trans[0];
            buttonSearchAgain.Text = trans[1];
            buttonClose.Text = trans[2];
            this.Text = trans[3];
            labelSN.Text = trans[4];
            labelTestOperation.Text = trans[5];

            Continue = true;
            this.apiRef = apiRef;
            this.wfApi = new Workflow.Workflow();
            this.DisplayTreeView = DisplayTreeView;
            this.PartNumber = PartNumber;

            textBoxCustomText.Text = CustomText;
            textBoxCustomText.Visible = !string.IsNullOrEmpty(CustomText);


            panelTestOperation.Visible = IncludeTestOperation;
            this.includeTestoperation = IncludeTestOperation;
            this.selectTestOperation = SelectTestOperation;

            if (IncludeTestOperation)
            {
                comboBoxTestOperation.DisplayMember = "Name";
                //Process[] processes = apiRef.GetProcesses();
                List<Process> processes = new List<Process>(apiRef.GetProcesses());
                processes.Insert(0, new Process() { Name = null });
                comboBoxTestOperation.DataSource = processes;
                comboBoxTestOperation.ValueMember = "Name";
                comboBoxTestOperation.DropDownStyle = ComboBoxStyle.DropDownList;
                try
                {
                    comboBoxTestOperation.AutoCompleteSource = AutoCompleteSource.ListItems;
                    comboBoxTestOperation.AutoCompleteMode = AutoCompleteMode.SuggestAppend;
                }
                catch { }

                comboBoxTestOperation.Enabled = SelectTestOperation;

                if (SelectedTestOperation != null && SelectedTestOperation.Name != null)
                {
                    comboBoxTestOperation.SelectedValue = SelectedTestOperation.Name;
                }

                comboBoxTestOperation.SelectedIndexChanged += comboBoxTestOperation_SelectedIndexChanged;
            }
            checkBoxDisplayTreeView.Checked = DisplayTreeView;
            treeViewUnitRelations.Visible = DisplayTreeView;
            this.useWorkflow = UseWorkflow;
            this.wfStatus = WorkflowStatus;
            buttonOK.Click += new EventHandler(buttonSearch_Click);

            textBoxSerialNumber.Text = SerialNumber;

            this.Height = tableLayoutPanel1.PreferredSize.Height + 200;
            Size s = this.MinimumSize;
            s.Height = this.Height;
            this.MinimumSize = s;
        }

        private void IdentifyUUT(string sn)
        {
            UnitInfo = apiRef.GetUnitInfo(sn, PartNumber);
            if (UnitInfo != null)
                UnitPhase = apiRef.GetUnitPhase(UnitInfo.SerialNumber, PartNumber);
            else
                UnitPhase = Unit_Phase.Unknown;
        }

        private void AddChildren(UnitInfo ui, TreeNode tn)
        {
            tn.Text = ui.PartNumberName;
            if (ui.SerialNumber == UnitInfo.SerialNumber)
            {
                tn.BackColor = Color.Gainsboro;
                tn.Nodes.Add(apiRef.TranslateString("Unit phase", null) + ":     " + UnitPhase);
            }
            tn.Nodes.Add(apiRef.TranslateString("Serial Number", null) + ":  " + ui.SerialNumber);
            tn.Nodes.Add(apiRef.TranslateString("Part Number", null) + ":    " + ui.PartNumber);
            tn.Nodes.Add(apiRef.TranslateString("Revision", null) + ":       " + ui.Revision);
            tn.Nodes.Add(apiRef.TranslateString("Batch Number", null) + ":   " + ui.BatchNumber);

            foreach (UnitInfo u in ui.GetChildren())
            {
                TreeNode tn2 = new TreeNode();
                AddChildren(u, tn2);
                tn.Nodes.Add(tn2);
            }
        }




        private void buttonSearch_Click(object sender, EventArgs e)
        {
            startIdentify();
        }

        private void buttonStart_Click(object sender, EventArgs e)
        {
            Continue = true;
            closeForm();
        }

        private void startIdentify()
        {
            try
            {
                textBoxSerialNumber.Enabled = false;
                buttonOK.Enabled = false;
                buttonSearchAgain.Enabled = false;
                buttonOK.Click -= new EventHandler(buttonSearch_Click);
                buttonOK.Click += new EventHandler(buttonStart_Click);

                // progressBar1.Style = ProgressBarStyle.Marquee;
                DisplayTreeView = checkBoxDisplayTreeView.Checked;
                IdentifyUnit.RunWorkerAsync();
            }
            catch { }
        }

        private void closeForm()
        {
            DialogResult = DialogResult.OK;
            closeOK = true;
            this.Close();
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            Continue = false;
            closeForm();
        }


        private void IdentifyUnit_DoWork(object sender, DoWorkEventArgs e)
        {
            IdentifyUUT(textBoxSerialNumber.Text);
        }

        private void IdentifyUnit_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            buttonOK.Text = apiRef.TranslateString("Start", null);
            buttonSearchAgain.Enabled = true;
            buttonSearchAgain.Visible = true;
            textBoxSerialNumber.Enabled = true;
            bool valid = validate();

            treeViewUnitRelations.Nodes.Clear();
            if (e.Error == null)
            {
                if (UnitInfo == null)//Display tree
                {
                    TreeNode udne = treeViewUnitRelations.Nodes.Add(apiRef.TranslateString("Unit does not exist", null));
                    udne.Nodes.Add(apiRef.TranslateString("Serial Number ", null) + ":  " + textBoxSerialNumber.Text);
                    udne.Nodes.Add(apiRef.TranslateString("Part Number ", null) + ":    " + PartNumber);
                    udne.ExpandAll();
                }
                else if (DisplayTreeView || !valid)
                {
                    UnitInfo parent = UnitInfo;
                    int maxLoops = 100;
                    while (parent.HasParent() && maxLoops-- > 0)
                    {
                        UnitInfo p = parent.GetParent();
                        if (p == null)
                            break;
                        parent = p;
                    }

                    TreeNode n = new TreeNode();
                    AddChildren(parent, n);
                    treeViewUnitRelations.Nodes.Add(n);
                    treeViewUnitRelations.ExpandAll();
                }

                treeViewUnitRelations.Visible = DisplayTreeView || UnitInfo == null || !valid;

                if (treeViewUnitRelations.Visible)
                {
                    int height = 16 * (GetTotalNodes(treeViewUnitRelations.Nodes) + 3);
                    this.Height = this.Height + height - treeViewUnitRelations.Height;
                    int max = Screen.GetBounds(this).Height - 50;
                    if (this.Height > max)
                        this.Height = max;
                }
            }

            if (valid && useWorkflow)
            {

                if (!textBoxCustomText.Visible) textBoxCustomText.Visible = true;
                textBoxCustomText.BackColor = Color.White;
                Dictionary<string,object> inputvalues = new Dictionary<string,object>();
                WorkflowResponse response = wfApi.Validate(UnitInfo.SerialNumber, UnitInfo.PartNumber, ActivityMethod.StartTest, (string)comboBoxTestOperation.SelectedValue, inputvalues, wfStatus); //wf_svc.Validate(UnitInfo.SerialNumber, UnitInfo.PartNumber, ActivityMethod.StartTest, (string)comboBoxTestOperation.SelectedValue, inputvalues, wfStatus);

                if (response.InstanceStatus == WorkflowInstanceStatus.WorkflowCancelled || response.InstanceStatus==WorkflowInstanceStatus.WorkflowNotInitialized)
                {
                    response = wfApi.Initialize(UnitInfo.SerialNumber, UnitInfo.PartNumber, inputvalues, false, false,wfStatus);
                    response = wfApi.Validate(UnitInfo.SerialNumber, UnitInfo.PartNumber, ActivityMethod.StartTest, (string)comboBoxTestOperation.SelectedValue, inputvalues, wfStatus);
                }
                if (!response.ok)
                {
                    textBoxCustomText.Text = apiRef.TranslateString("Error: ", null) + response.ErrorMessage + "\r\n";
                    if (!String.IsNullOrEmpty(response.Description)) textBoxCustomText.Text += apiRef.TranslateString("Go to: ", null) + response.Description;
                    textBoxCustomText.BackColor = Color.Pink;
                    buttonOK.Enabled = false;
                    valid = false;
                }
                else
                {
                    if (response.InstanceStatus==WorkflowInstanceStatus.ActiveWorkflowExist)
                    {
                        int testCount = r2int(response.ReturnValues, "TestCount");
                        int maxFailCount = r2int(response.ReturnValues, "MaxFailedCount");
                        ActivityTestResult lastTestResult = response.ReturnValues.ContainsKey("LastTestResult") ? (ActivityTestResult)Enum.Parse(typeof(ActivityTestResult),response.ReturnValues["LastTestResult"].ToString()) : ActivityTestResult.Unknown;
                        textBoxCustomText.Text = apiRef.TranslateString("OK to test, {0} of {1} attempt{2}.", 
                            new object[] {testCount+1, maxFailCount, maxFailCount > 1 ? "s" : ""});
                    }
                    else if (response.InstanceStatus==WorkflowInstanceStatus.WorkflowCompleted && r2bool(ctx,"DenyWFCompleted"))
                    {
                        ShowWorkflowError("Error: Unit is already completed");
                        valid = false;
                    }
                    else if (response.InstanceStatus == WorkflowInstanceStatus.WorkflowNotDefined && r2bool(ctx, "DenyWFNotDefined"))
                    {
                        ShowWorkflowError("Error: No workflow defined for this unit");
                        valid = false;
                    }
                    else if (response.InstanceStatus == WorkflowInstanceStatus.WorkflowSuspended)
                    {
                        if (r2bool(ctx, "DenyWFSuspended"))
                        {
                            ShowWorkflowError("Error: This teststation does not allow suspended units");
                            valid = false;
                        }
                        else
                            ShowWorkflowWarning("Warning: This unit is suspended in repair or a golden sample.");
                    }
                }
            }

            if (!DisplayTreeView && valid)
                closeForm();
        }

        private void ShowWorkflowError(string message)
        {
            textBoxCustomText.Text = apiRef.TranslateString(message, null);
            textBoxCustomText.BackColor = Color.Pink;
            buttonOK.Enabled = false;            
        }

        private void ShowWorkflowWarning(string message)
        {
            textBoxCustomText.Text = apiRef.TranslateString(message, null);
            textBoxCustomText.BackColor = Color.Yellow;
        }


        private static int r2int(Dictionary<string, object> returnValues, string key)
        {
            if (returnValues !=null && returnValues.ContainsKey(key))
                return Convert.ToInt32(returnValues[key]);
            else
                return 0;
        }

        private static bool r2bool(Dictionary<string, object> returnValues, string key)
        {
            if (returnValues != null && returnValues.ContainsKey(key))
                return (bool)returnValues[key];
            else
                return false;
        }

        private bool validate()
        {
            bool valid = UnitInfo != null && !(includeTestoperation && selectTestOperation && comboBoxTestOperation.SelectedValue == null);
            buttonOK.Enabled = valid || !buttonSearchAgain.Visible;
            labelOperationRequired.Visible = includeTestoperation && selectTestOperation && comboBoxTestOperation.SelectedValue == null;

            if (buttonOK.Enabled)
                buttonOK.Select();
            else
                textBoxSerialNumber.Select();

            return valid;
        }

        private int GetTotalNodes(TreeNodeCollection nodes)
        {
            int rootNodes = nodes.Count;
            foreach (TreeNode node in nodes)
                rootNodes += this.GetTotalNodes(node.Nodes);
            return rootNodes;
        }



        bool closeOK = false;
        private void IdentifyConnected_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (!closeOK)
                e.Cancel = true;
            TestOperation = comboBoxTestOperation.SelectedItem as Process;
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
            if (textBoxSerialNumber.Text.EndsWith("\r\n"))
            {
                textBoxSerialNumber.Text = textBoxSerialNumber.Text.Substring(0, textBoxSerialNumber.Text.Length - 2);
                startIdentify();
            }
        }


        private void checkBoxDisplayTreeView_CheckedChanged(object sender, EventArgs e)
        {
            if (!buttonSearchAgain.Visible)
                buttonOK.Text = checkBoxDisplayTreeView.Checked ? apiRef.TranslateString("Search", null) : apiRef.TranslateString("Start", null);
            buttonSearchAgain.Enabled = checkBoxDisplayTreeView.Checked || !buttonOK.Enabled;
        }


        private void ActivateAndFocus(object sender, EventArgs e)
        {
            this.Activate();
            textBoxSerialNumber.Focus();
        }

        private void comboBoxTestOperation_SelectedIndexChanged(object sender, EventArgs e)
        {
            validate();
            if (useWorkflow) buttonOK.Enabled = false;  //Must search again..
        }
    }
}

