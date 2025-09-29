using System;
using System.Windows.Forms;
using Virinco.WATS.Service.MES.Contract;

namespace Virinco.WATS.Interface.MES
{
    internal partial class MesTestGUI : Form
    {
        public MesTestGUI()
        {
            InitializeComponent();
            comboBoxStatus.SelectedIndex = 0;
        }

        private void buttonClose_Click(object sender, EventArgs e)
        {
            DialogResult = DialogResult.OK;            
            this.Close();
        }

        private void buttonGetPackage_Click(object sender, EventArgs e)
        {
            StatusEnum s = StatusEnum.Draft;
            try
            {
                s = (StatusEnum)Enum.Parse(typeof(StatusEnum), comboBoxStatus.SelectedText);
            }
            catch { comboBoxStatus.SelectedIndex = 0; }

            MesInterface mes = new MesInterface();
            Package p = mes.Software.GetPackageByName(textBoxPackageName.Text, true, true, true, s);

            if(p != null){
            textBoxResult.Text = string.Format("Package Name: {0}\r\nVersion: {1}\r\nStatus: {2}\r\n\r\nTags: {3}",
                p.Name,
                p.Version,
                p.PackageStatus,
                p.Tags);

            }else
                textBoxResult.Text = string.Format("Package not found");

        }
              

        private void buttonbuttonIdentifyUUT_Click(object sender, EventArgs e)
        {
            try
            {
                MesInterface mes = new MesInterface();
                bool stopped = false;
                Virinco.WATS.Interface.MES.Production.UnitInfo ui = mes.Production.IdentifyUUT(out stopped);
            }
            catch (Exception ex) { System.Windows.Forms.MessageBox.Show("An error occurred" + ex.ToString()); }

        }
    }
}
