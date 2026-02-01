using System.Drawing;

namespace Virinco.WATS.Interface.MES.Production
{
    partial class IdentifyConnected
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(IdentifyConnected));
            this.textBoxSerialNumber = new System.Windows.Forms.TextBox();
            this.buttonOK = new System.Windows.Forms.Button();
            this.buttonClose = new System.Windows.Forms.Button();
            this.labelSN = new System.Windows.Forms.Label();
            this.checkBoxDisplayTreeView = new System.Windows.Forms.CheckBox();
            this.treeViewUnitRelations = new System.Windows.Forms.TreeView();
            this.IdentifyUnit = new System.ComponentModel.BackgroundWorker();
            this.buttonSearchAgain = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.panel1 = new System.Windows.Forms.Panel();
            this.panelTestOperation = new System.Windows.Forms.Panel();
            this.comboBoxTestOperation = new System.Windows.Forms.ComboBox();
            this.labelTestOperation = new System.Windows.Forms.Label();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.textBoxCustomText = new System.Windows.Forms.TextBox();
            this.labelOperationRequired = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.panel1.SuspendLayout();
            this.panelTestOperation.SuspendLayout();
            this.tableLayoutPanel1.SuspendLayout();
            this.SuspendLayout();
            // 
            // textBoxSerialNumber
            // 
            this.textBoxSerialNumber.AcceptsReturn = true;
            this.textBoxSerialNumber.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.textBoxSerialNumber.Location = new System.Drawing.Point(89, 3);
            this.textBoxSerialNumber.Margin = new System.Windows.Forms.Padding(0);
            this.textBoxSerialNumber.Multiline = true;
            this.textBoxSerialNumber.Name = "textBoxSerialNumber";
            this.textBoxSerialNumber.Size = new System.Drawing.Size(219, 20);
            this.textBoxSerialNumber.TabIndex = 1;
            this.textBoxSerialNumber.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // buttonOK
            // 
            this.buttonOK.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.buttonOK.Location = new System.Drawing.Point(10, 277);
            this.buttonOK.Name = "buttonOK";
            this.buttonOK.Size = new System.Drawing.Size(75, 23);
            this.buttonOK.TabIndex = 1;
            this.buttonOK.Text = "&Search";
            this.buttonOK.UseVisualStyleBackColor = true;
            // 
            // buttonClose
            // 
            this.buttonClose.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonClose.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.buttonClose.Location = new System.Drawing.Point(248, 277);
            this.buttonClose.Name = "buttonClose";
            this.buttonClose.Size = new System.Drawing.Size(75, 23);
            this.buttonClose.TabIndex = 3;
            this.buttonClose.Text = "Stop";
            this.buttonClose.UseVisualStyleBackColor = true;
            this.buttonClose.Click += new System.EventHandler(this.buttonClose_Click);
            // 
            // labelSN
            // 
            this.labelSN.AutoSize = true;
            this.labelSN.Location = new System.Drawing.Point(3, 6);
            this.labelSN.Margin = new System.Windows.Forms.Padding(0);
            this.labelSN.Name = "labelSN";
            this.labelSN.Size = new System.Drawing.Size(76, 13);
            this.labelSN.TabIndex = 0;
            this.labelSN.Text = "&Serial Number:";
            // 
            // checkBoxDisplayTreeView
            // 
            this.checkBoxDisplayTreeView.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.checkBoxDisplayTreeView.AutoSize = true;
            this.checkBoxDisplayTreeView.Checked = true;
            this.checkBoxDisplayTreeView.CheckState = System.Windows.Forms.CheckState.Checked;
            this.checkBoxDisplayTreeView.Location = new System.Drawing.Point(12, 256);
            this.checkBoxDisplayTreeView.Name = "checkBoxDisplayTreeView";
            this.checkBoxDisplayTreeView.Size = new System.Drawing.Size(108, 17);
            this.checkBoxDisplayTreeView.TabIndex = 0;
            this.checkBoxDisplayTreeView.Text = "&Display TreeView";
            this.checkBoxDisplayTreeView.UseVisualStyleBackColor = true;
            this.checkBoxDisplayTreeView.CheckedChanged += new System.EventHandler(this.checkBoxDisplayTreeView_CheckedChanged);
            // 
            // treeViewUnitRelations
            // 
            this.treeViewUnitRelations.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.treeViewUnitRelations.Font = new System.Drawing.Font("Courier New", 11F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Pixel, ((byte)(0)));
            this.treeViewUnitRelations.Location = new System.Drawing.Point(2, 102);
            this.treeViewUnitRelations.Margin = new System.Windows.Forms.Padding(2);
            this.treeViewUnitRelations.Name = "treeViewUnitRelations";
            this.treeViewUnitRelations.Size = new System.Drawing.Size(307, 90);
            this.treeViewUnitRelations.TabIndex = 1;
            // 
            // IdentifyUnit
            // 
            this.IdentifyUnit.DoWork += new System.ComponentModel.DoWorkEventHandler(this.IdentifyUnit_DoWork);
            this.IdentifyUnit.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.IdentifyUnit_RunWorkerCompleted);
            // 
            // buttonSearchAgain
            // 
            this.buttonSearchAgain.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.buttonSearchAgain.Location = new System.Drawing.Point(91, 277);
            this.buttonSearchAgain.Name = "buttonSearchAgain";
            this.buttonSearchAgain.Size = new System.Drawing.Size(84, 23);
            this.buttonSearchAgain.TabIndex = 2;
            this.buttonSearchAgain.Text = "Search &Again";
            this.buttonSearchAgain.UseVisualStyleBackColor = true;
            this.buttonSearchAgain.Visible = false;
            this.buttonSearchAgain.Click += new System.EventHandler(this.buttonSearch_Click);
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(253)))), ((int)(((byte)(196)))), ((int)(((byte)(0)))));
            this.label2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.label2.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.label2.Location = new System.Drawing.Point(0, 307);
            this.label2.Name = "label2";
            this.label2.Padding = new System.Windows.Forms.Padding(5, 0, 0, 0);
            this.label2.Size = new System.Drawing.Size(342, 22);
            this.label2.TabIndex = 4;
            this.label2.Text = "WATS.com";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // pictureBox1
            // 
            this.pictureBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureBox1.Image = global::Virinco.WATS.Interface.MES.Properties.Resources.wats_icon_128__002_;
            this.pictureBox1.Location = new System.Drawing.Point(223, 0);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(100, 50);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBox1.TabIndex = 6;
            this.pictureBox1.TabStop = false;
            // 
            // panel1
            // 
            this.panel1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.panel1.Controls.Add(this.labelSN);
            this.panel1.Controls.Add(this.textBoxSerialNumber);
            this.panel1.Location = new System.Drawing.Point(0, 46);
            this.panel1.Margin = new System.Windows.Forms.Padding(0);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(311, 27);
            this.panel1.TabIndex = 2;
            // 
            // panelTestOperation
            // 
            this.panelTestOperation.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.panelTestOperation.Controls.Add(this.comboBoxTestOperation);
            this.panelTestOperation.Controls.Add(this.labelTestOperation);
            this.panelTestOperation.Location = new System.Drawing.Point(0, 73);
            this.panelTestOperation.Margin = new System.Windows.Forms.Padding(0);
            this.panelTestOperation.Name = "panelTestOperation";
            this.panelTestOperation.Size = new System.Drawing.Size(311, 27);
            this.panelTestOperation.TabIndex = 3;
            // 
            // comboBoxTestOperation
            // 
            this.comboBoxTestOperation.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.comboBoxTestOperation.FormattingEnabled = true;
            this.comboBoxTestOperation.Location = new System.Drawing.Point(89, 3);
            this.comboBoxTestOperation.Margin = new System.Windows.Forms.Padding(0);
            this.comboBoxTestOperation.Name = "comboBoxTestOperation";
            this.comboBoxTestOperation.Size = new System.Drawing.Size(219, 21);
            this.comboBoxTestOperation.TabIndex = 1;
            // 
            // labelTestOperation
            // 
            this.labelTestOperation.AutoSize = true;
            this.labelTestOperation.Location = new System.Drawing.Point(3, 6);
            this.labelTestOperation.Margin = new System.Windows.Forms.Padding(0);
            this.labelTestOperation.Name = "labelTestOperation";
            this.labelTestOperation.Size = new System.Drawing.Size(80, 13);
            this.labelTestOperation.TabIndex = 0;
            this.labelTestOperation.Text = "Test Operation:";
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle());
            this.tableLayoutPanel1.Controls.Add(this.textBoxCustomText, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.treeViewUnitRelations, 0, 3);
            this.tableLayoutPanel1.Controls.Add(this.panel1, 0, 1);
            this.tableLayoutPanel1.Controls.Add(this.panelTestOperation, 0, 2);
            this.tableLayoutPanel1.Location = new System.Drawing.Point(12, 56);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 4;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.tableLayoutPanel1.Size = new System.Drawing.Size(311, 194);
            this.tableLayoutPanel1.TabIndex = 11;
            // 
            // textBoxCustomText
            // 
            this.textBoxCustomText.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.textBoxCustomText.BackColor = System.Drawing.Color.White;
            this.textBoxCustomText.Location = new System.Drawing.Point(0, 0);
            this.textBoxCustomText.Margin = new System.Windows.Forms.Padding(0);
            this.textBoxCustomText.Multiline = true;
            this.textBoxCustomText.Name = "textBoxCustomText";
            this.textBoxCustomText.ReadOnly = true;
            this.textBoxCustomText.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBoxCustomText.Size = new System.Drawing.Size(311, 46);
            this.textBoxCustomText.TabIndex = 0;
            this.textBoxCustomText.Text = "Her kan du legge inn tekst som strekker seg over flere linjer. Her kan du legge i" +
    "nn tekst som strekker seg over flere linjer. Her kan du legge inn tekst som stre" +
    "kker seg over flere linjer. ";
            // 
            // labelOperationRequired
            // 
            this.labelOperationRequired.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.labelOperationRequired.AutoSize = true;
            this.labelOperationRequired.ForeColor = System.Drawing.Color.Red;
            this.labelOperationRequired.Location = new System.Drawing.Point(323, 139);
            this.labelOperationRequired.Name = "labelOperationRequired";
            this.labelOperationRequired.Size = new System.Drawing.Size(11, 13);
            this.labelOperationRequired.TabIndex = 12;
            this.labelOperationRequired.Text = "*";
            this.labelOperationRequired.Visible = false;
            // 
            // IdentifyConnected
            // 
            this.AcceptButton = this.buttonOK;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.CancelButton = this.buttonClose;
            this.ClientSize = new System.Drawing.Size(342, 329);
            this.Controls.Add(this.labelOperationRequired);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.buttonSearchAgain);
            this.Controls.Add(this.checkBoxDisplayTreeView);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.buttonClose);
            this.Controls.Add(this.buttonOK);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(350, 39);
            this.Name = "IdentifyConnected";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Identify UUT";
            this.TopMost = true;
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.IdentifyConnected_FormClosing);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            this.panelTestOperation.ResumeLayout(false);
            this.panelTestOperation.PerformLayout();
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBoxSerialNumber;
        private System.Windows.Forms.Button buttonOK;
        private System.Windows.Forms.Button buttonClose;
        private System.Windows.Forms.Label labelSN;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.CheckBox checkBoxDisplayTreeView;
        private System.Windows.Forms.TreeView treeViewUnitRelations;
        private System.ComponentModel.BackgroundWorker IdentifyUnit;
        private System.Windows.Forms.Button buttonSearchAgain;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Panel panelTestOperation;
        private System.Windows.Forms.ComboBox comboBoxTestOperation;
        private System.Windows.Forms.Label labelTestOperation;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.TextBox textBoxCustomText;
        private System.Windows.Forms.Label labelOperationRequired;
    }
}