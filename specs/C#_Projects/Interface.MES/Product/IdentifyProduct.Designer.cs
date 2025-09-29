namespace Virinco.WATS.Interface.MES.Product
{
    partial class IdentifyProduct
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(IdentifyProduct));
            this.buttonOK = new System.Windows.Forms.Button();
            this.buttonStop = new System.Windows.Forms.Button();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.textBoxCutomText = new System.Windows.Forms.TextBox();
            this.tableLayoutPanel1 = new System.Windows.Forms.TableLayoutPanel();
            this.panelSN = new System.Windows.Forms.Panel();
            this.textBoxSerialNumber = new System.Windows.Forms.TextBox();
            this.labelSN = new System.Windows.Forms.Label();
            this.panelPN = new System.Windows.Forms.Panel();
            this.comboBoxPartNumbers = new System.Windows.Forms.ComboBox();
            this.labelPN = new System.Windows.Forms.Label();
            this.panelRev = new System.Windows.Forms.Panel();
            this.comboBoxRevision = new System.Windows.Forms.ComboBox();
            this.labelRev = new System.Windows.Forms.Label();
            this.panelOperation = new System.Windows.Forms.Panel();
            this.comboBoxOperations = new System.Windows.Forms.ComboBox();
            this.labelTestOperation = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.tableLayoutPanel1.SuspendLayout();
            this.panelSN.SuspendLayout();
            this.panelPN.SuspendLayout();
            this.panelRev.SuspendLayout();
            this.panelOperation.SuspendLayout();
            this.SuspendLayout();
            // 
            // buttonOK
            // 
            this.buttonOK.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonOK.Location = new System.Drawing.Point(166, 222);
            this.buttonOK.Name = "buttonOK";
            this.buttonOK.Size = new System.Drawing.Size(75, 23);
            this.buttonOK.TabIndex = 0;
            this.buttonOK.Text = "&OK";
            this.buttonOK.UseVisualStyleBackColor = true;
            this.buttonOK.Click += new System.EventHandler(this.buttonOK_Click);
            // 
            // buttonStop
            // 
            this.buttonStop.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonStop.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.buttonStop.Location = new System.Drawing.Point(247, 222);
            this.buttonStop.Name = "buttonStop";
            this.buttonStop.Size = new System.Drawing.Size(75, 23);
            this.buttonStop.TabIndex = 1;
            this.buttonStop.Text = "&Stop";
            this.buttonStop.UseVisualStyleBackColor = true;
            this.buttonStop.Click += new System.EventHandler(this.buttonStop_Click);
            // 
            // pictureBox1
            // 
            this.pictureBox1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.pictureBox1.Image = global::Virinco.WATS.Interface.MES.Properties.Resources.wats_icon_128__002_;
            this.pictureBox1.Location = new System.Drawing.Point(222, 0);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(100, 50);
            this.pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.pictureBox1.TabIndex = 17;
            this.pictureBox1.TabStop = false;
            // 
            // textBoxCutomText
            // 
            this.textBoxCutomText.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.textBoxCutomText.BackColor = System.Drawing.Color.White;
            this.textBoxCutomText.Location = new System.Drawing.Point(0, 0);
            this.textBoxCutomText.Margin = new System.Windows.Forms.Padding(0);
            this.textBoxCutomText.Multiline = true;
            this.textBoxCutomText.Name = "textBoxCutomText";
            this.textBoxCutomText.ReadOnly = true;
            this.textBoxCutomText.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBoxCutomText.Size = new System.Drawing.Size(310, 46);
            this.textBoxCutomText.TabIndex = 0;
            this.textBoxCutomText.Text = "Her kan du legge inn tekst som strekker seg over flere linjer. Her kan du legge i" +
    "nn tekst som strekker seg over flere linjer. Her kan du legge inn tekst som stre" +
    "kker seg over flere linjer. ";
            // 
            // tableLayoutPanel1
            // 
            this.tableLayoutPanel1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.tableLayoutPanel1.ColumnCount = 1;
            this.tableLayoutPanel1.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle());
            this.tableLayoutPanel1.Controls.Add(this.panelSN, 0, 1);
            this.tableLayoutPanel1.Controls.Add(this.textBoxCutomText, 0, 0);
            this.tableLayoutPanel1.Controls.Add(this.panelPN, 0, 2);
            this.tableLayoutPanel1.Controls.Add(this.panelRev, 0, 3);
            this.tableLayoutPanel1.Controls.Add(this.panelOperation, 0, 4);
            this.tableLayoutPanel1.Location = new System.Drawing.Point(12, 56);
            this.tableLayoutPanel1.Name = "tableLayoutPanel1";
            this.tableLayoutPanel1.RowCount = 6;
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.RowStyles.Add(new System.Windows.Forms.RowStyle());
            this.tableLayoutPanel1.Size = new System.Drawing.Size(310, 160);
            this.tableLayoutPanel1.TabIndex = 18;
            // 
            // panelSN
            // 
            this.panelSN.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.panelSN.Controls.Add(this.textBoxSerialNumber);
            this.panelSN.Controls.Add(this.labelSN);
            this.panelSN.Location = new System.Drawing.Point(0, 46);
            this.panelSN.Margin = new System.Windows.Forms.Padding(0);
            this.panelSN.Name = "panelSN";
            this.panelSN.Size = new System.Drawing.Size(310, 27);
            this.panelSN.TabIndex = 1;
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
            this.textBoxSerialNumber.Size = new System.Drawing.Size(218, 20);
            this.textBoxSerialNumber.TabIndex = 1;
            // 
            // labelSN
            // 
            this.labelSN.AutoSize = true;
            this.labelSN.Location = new System.Drawing.Point(3, 6);
            this.labelSN.Margin = new System.Windows.Forms.Padding(0);
            this.labelSN.Name = "labelSN";
            this.labelSN.Size = new System.Drawing.Size(73, 13);
            this.labelSN.TabIndex = 0;
            this.labelSN.Text = "Serial Number";
            // 
            // panelPN
            // 
            this.panelPN.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.panelPN.Controls.Add(this.comboBoxPartNumbers);
            this.panelPN.Controls.Add(this.labelPN);
            this.panelPN.Location = new System.Drawing.Point(0, 73);
            this.panelPN.Margin = new System.Windows.Forms.Padding(0);
            this.panelPN.Name = "panelPN";
            this.panelPN.Size = new System.Drawing.Size(310, 27);
            this.panelPN.TabIndex = 2;
            // 
            // comboBoxPartNumbers
            // 
            this.comboBoxPartNumbers.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.comboBoxPartNumbers.FormattingEnabled = true;
            this.comboBoxPartNumbers.Location = new System.Drawing.Point(89, 3);
            this.comboBoxPartNumbers.Margin = new System.Windows.Forms.Padding(0);
            this.comboBoxPartNumbers.Name = "comboBoxPartNumbers";
            this.comboBoxPartNumbers.Size = new System.Drawing.Size(218, 21);
            this.comboBoxPartNumbers.TabIndex = 1;
            this.comboBoxPartNumbers.SelectedIndexChanged += new System.EventHandler(this.comboBoxPartNumbers_SelectedIndexChanged);
            // 
            // labelPN
            // 
            this.labelPN.AutoSize = true;
            this.labelPN.Location = new System.Drawing.Point(3, 6);
            this.labelPN.Margin = new System.Windows.Forms.Padding(0);
            this.labelPN.Name = "labelPN";
            this.labelPN.Size = new System.Drawing.Size(66, 13);
            this.labelPN.TabIndex = 0;
            this.labelPN.Text = "Part Number";
            // 
            // panelRev
            // 
            this.panelRev.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.panelRev.Controls.Add(this.comboBoxRevision);
            this.panelRev.Controls.Add(this.labelRev);
            this.panelRev.Location = new System.Drawing.Point(0, 100);
            this.panelRev.Margin = new System.Windows.Forms.Padding(0);
            this.panelRev.Name = "panelRev";
            this.panelRev.Size = new System.Drawing.Size(310, 27);
            this.panelRev.TabIndex = 3;
            // 
            // comboBoxRevision
            // 
            this.comboBoxRevision.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.comboBoxRevision.FormattingEnabled = true;
            this.comboBoxRevision.Location = new System.Drawing.Point(89, 3);
            this.comboBoxRevision.Margin = new System.Windows.Forms.Padding(0);
            this.comboBoxRevision.Name = "comboBoxRevision";
            this.comboBoxRevision.Size = new System.Drawing.Size(218, 21);
            this.comboBoxRevision.TabIndex = 1;
            // 
            // labelRev
            // 
            this.labelRev.AutoSize = true;
            this.labelRev.Location = new System.Drawing.Point(3, 6);
            this.labelRev.Margin = new System.Windows.Forms.Padding(0);
            this.labelRev.Name = "labelRev";
            this.labelRev.Size = new System.Drawing.Size(48, 13);
            this.labelRev.TabIndex = 0;
            this.labelRev.Text = "Revision";
            // 
            // panelOperation
            // 
            this.panelOperation.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Left | System.Windows.Forms.AnchorStyles.Right)));
            this.panelOperation.Controls.Add(this.comboBoxOperations);
            this.panelOperation.Controls.Add(this.labelTestOperation);
            this.panelOperation.Location = new System.Drawing.Point(0, 127);
            this.panelOperation.Margin = new System.Windows.Forms.Padding(0);
            this.panelOperation.Name = "panelOperation";
            this.panelOperation.Size = new System.Drawing.Size(310, 27);
            this.panelOperation.TabIndex = 4;
            // 
            // comboBoxOperations
            // 
            this.comboBoxOperations.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.comboBoxOperations.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBoxOperations.FormattingEnabled = true;
            this.comboBoxOperations.Location = new System.Drawing.Point(89, 3);
            this.comboBoxOperations.Margin = new System.Windows.Forms.Padding(0);
            this.comboBoxOperations.Name = "comboBoxOperations";
            this.comboBoxOperations.Size = new System.Drawing.Size(218, 21);
            this.comboBoxOperations.TabIndex = 1;
            // 
            // labelTestOperation
            // 
            this.labelTestOperation.AutoSize = true;
            this.labelTestOperation.Location = new System.Drawing.Point(3, 6);
            this.labelTestOperation.Margin = new System.Windows.Forms.Padding(0);
            this.labelTestOperation.Name = "labelTestOperation";
            this.labelTestOperation.Size = new System.Drawing.Size(77, 13);
            this.labelTestOperation.TabIndex = 0;
            this.labelTestOperation.Text = "Test Operation";
            // 
            // label2
            // 
            this.label2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(253)))), ((int)(((byte)(196)))), ((int)(((byte)(0)))));
            this.label2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.label2.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.label2.Location = new System.Drawing.Point(0, 251);
            this.label2.Name = "label2";
            this.label2.Padding = new System.Windows.Forms.Padding(5, 0, 0, 0);
            this.label2.Size = new System.Drawing.Size(342, 22);
            this.label2.TabIndex = 2;
            this.label2.Text = "WATS.com";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // IdentifyProduct
            // 
            this.AcceptButton = this.buttonOK;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.CancelButton = this.buttonStop;
            this.ClientSize = new System.Drawing.Size(342, 273);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.tableLayoutPanel1);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.buttonStop);
            this.Controls.Add(this.buttonOK);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(350, 39);
            this.Name = "IdentifyProduct";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Select Operation Type & Product to test";
            this.TopMost = true;
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.IdentifyProduct_FormClosing);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.tableLayoutPanel1.ResumeLayout(false);
            this.tableLayoutPanel1.PerformLayout();
            this.panelSN.ResumeLayout(false);
            this.panelSN.PerformLayout();
            this.panelPN.ResumeLayout(false);
            this.panelPN.PerformLayout();
            this.panelRev.ResumeLayout(false);
            this.panelRev.PerformLayout();
            this.panelOperation.ResumeLayout(false);
            this.panelOperation.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button buttonOK;
        private System.Windows.Forms.Button buttonStop;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.TextBox textBoxCutomText;
        private System.Windows.Forms.TableLayoutPanel tableLayoutPanel1;
        private System.Windows.Forms.Panel panelRev;
        private System.Windows.Forms.Label labelRev;
        private System.Windows.Forms.Panel panelPN;
        private System.Windows.Forms.ComboBox comboBoxPartNumbers;
        private System.Windows.Forms.Label labelPN;
        private System.Windows.Forms.ComboBox comboBoxRevision;
        private System.Windows.Forms.Panel panelOperation;
        private System.Windows.Forms.ComboBox comboBoxOperations;
        private System.Windows.Forms.Label labelTestOperation;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Panel panelSN;
        private System.Windows.Forms.Label labelSN;
        private System.Windows.Forms.TextBox textBoxSerialNumber;

    }
}