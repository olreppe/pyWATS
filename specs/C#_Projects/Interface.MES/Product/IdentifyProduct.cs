using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using Virinco.WATS.Service.MES.Contract;

namespace Virinco.WATS.Interface.MES.Product
{
    internal partial class IdentifyProduct : Form
    {

        Product apiRef;
        private Process[] operations = null;
        private bool IncludeRevision;
        private bool IncludeSerialNumber;
        private bool EnableFreePartnumber;
        private Service.MES.Contract.Product[] Products;

        public IdentifyProduct(Product apiRef, bool IncludeRevision, bool IncludeSerialNumber, bool EnableFreePartnumber, string Filter, int TopCount, string CustomText, bool AlwaysOnTop)
        {
            InitializeComponent();
            this.apiRef = apiRef;
            this.TopMost = AlwaysOnTop;

            //textBoxCutomText.Visible = !string.IsNullOrEmpty(CustomText);

            this.IncludeRevision = IncludeRevision;
            panelRev.Visible = IncludeRevision;

            this.IncludeSerialNumber = IncludeSerialNumber;
            panelSN.Visible = IncludeSerialNumber;



            comboBoxRevision.DisplayMember = "Revision";
            comboBoxPartNumbers.DisplayMember = "PartNumber";

            this.EnableFreePartnumber = EnableFreePartnumber;
            comboBoxRevision.DropDownStyle = comboBoxPartNumbers.DropDownStyle = EnableFreePartnumber ? ComboBoxStyle.DropDown : ComboBoxStyle.DropDownList;

            this.Products = apiRef.GetProduct(Filter, TopCount, true, false); ;
            if (Products != null)
                comboBoxPartNumbers.Items.AddRange(Products);

            if (comboBoxPartNumbers.Items.Count > 0)
                comboBoxPartNumbers.SelectedItem = comboBoxPartNumbers.Items[0];

            Continue = true;

            string[] trans = apiRef.TranslateArray(new[] {
                "Select Product & Test Operation",
                 string.IsNullOrEmpty(CustomText)? "Select product and test operation":CustomText,
                "Serial Number",
                "Test Operation",
                "Revision",
                "Part Number",
                "Ok",
                "Stop"
            });

            this.Text = trans[0];
            textBoxCutomText.Text = trans[1];
            labelSN.Text = trans[2];
            labelTestOperation.Text = trans[3];
            labelRev.Text = trans[4];
            labelPN.Text = trans[5];
            buttonOK.Text = trans[6];
            buttonStop.Text = trans[7];

            try
            {
                this.operations = apiRef.GetProcesses();
                if (operations != null)
                {
                    foreach (Process p in operations)
                        comboBoxOperations.Items.Add(p.Name);
                    if (comboBoxOperations.Items.Count > 0)
                        comboBoxOperations.SelectedIndex = 0;
                }

                comboBoxPartNumbers.AutoCompleteSource = comboBoxRevision.AutoCompleteSource = comboBoxOperations.AutoCompleteSource = AutoCompleteSource.ListItems;
                comboBoxPartNumbers.AutoCompleteMode = comboBoxRevision.AutoCompleteMode = comboBoxOperations.AutoCompleteMode = AutoCompleteMode.SuggestAppend;

            }
            catch { }

            this.Height = tableLayoutPanel1.PreferredSize.Height + 180;
            Size s = this.MinimumSize;
            s.Height = this.Height;
            this.MinimumSize = s;
        }



        public string SelectedSerialNumber { get; set; }
        public string SelectedPartNumber { get; set; }
        public string SelectedRevision { get; set; }
        public Process SelectedTestOperation { get; set; }
        public bool Continue { get; set; }

        private void IdentifyProduct_FormClosing(object sender, FormClosingEventArgs e)
        {
            try
            {
                SelectedSerialNumber = textBoxSerialNumber.Text;
                SelectedPartNumber = comboBoxPartNumbers.Text;
                SelectedRevision = comboBoxRevision.Text;
                SelectedTestOperation = (Process)operations[comboBoxOperations.SelectedIndex];
            }
            catch { }
        }



        private void comboBoxPartNumbers_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (IncludeRevision && comboBoxPartNumbers.SelectedItem != null)
            {
                Virinco.WATS.Service.MES.Contract.Product p1 = (Virinco.WATS.Service.MES.Contract.Product)comboBoxPartNumbers.SelectedItem;
                Virinco.WATS.Service.MES.Contract.Product p2 = apiRef.GetProduct(p1.PartNumber, 1, true, true).FirstOrDefault();

                comboBoxRevision.Items.Clear();
                if (p2 != null && p2.ProductRevisions != null)
                {
                    comboBoxRevision.Items.AddRange(p2.ProductRevisions.ToArray());
                    if (comboBoxRevision.Items.Count > 0)
                        comboBoxRevision.SelectedIndex = 0;
                }
            }
        }

        private void buttonOK_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrEmpty(comboBoxPartNumbers.Text))
            {
                MessageBox.Show(this,
                    apiRef.TranslateString("Unspecified PartNumber. PartNumber cannot be empty", null),
                    apiRef.TranslateString("Unspecified value", null),
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else if (IncludeRevision && string.IsNullOrEmpty(comboBoxRevision.Text))
            {
                MessageBox.Show(this,
                    apiRef.TranslateString("Unspecified Revision. Revision cannot be empty", null),
                    apiRef.TranslateString("Unspecified value", null),
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            else
            {
                Continue = true;
                this.Close();
            }
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            Continue = false;
            this.Close();
        }


    }
}
