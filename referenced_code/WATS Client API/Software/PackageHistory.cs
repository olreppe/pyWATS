using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Runtime.Versioning;
using System.Text;
using System.Windows.Forms;
using Virinco.WATS.Service.MES.Contract;

namespace Virinco.WATS.Interface.MES.Software
{
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    internal partial class PackageHistory : Form
    {
        private Software software;
        private List<Package> packages;

        public Package SelectedPackage = null;
        public bool Continue = false;

        internal PackageHistory(Software software, List<Package> p)
        {
            InitializeComponent();
            this.software = software;
            this.packages = p;

            foreach (Package package in packages)
                comboBoxPackages.Items.Add(string.Format("{0} v{1} - {2}", package.Name, package.Version, package.Description));

            if (comboBoxPackages.Items.Count > 0)
                comboBoxPackages.SelectedIndex = 0;
        }

        private void buttonOK_Click(object sender, EventArgs e)
        {
            this.DialogResult = System.Windows.Forms.DialogResult.OK;
            Continue = true;
            SelectedPackage = getSelectedPackage();
            this.Close();
        }

        private void buttonStop_Click(object sender, EventArgs e)
        {
            this.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            Continue = false;
            this.Close();
        }

        private void comboBoxPackages_SelectedIndexChanged(object sender, EventArgs e)
        {
            Package p = getSelectedPackage();
            if (p != null)
            {
                textBoxDescription.Text = "Description:\r\n" + p.Description;
            }
            else
                textBoxDescription.Text = "";

            buttonOK.Enabled = (p != null);
        }

        private Package getSelectedPackage()
        {
            Package selected = null;
            if (comboBoxPackages.SelectedIndex > -1 && packages.Count >= comboBoxPackages.SelectedIndex + 1 && packages[comboBoxPackages.SelectedIndex] != null)
                selected = packages[comboBoxPackages.SelectedIndex];

            return selected;
        }

    }
}
