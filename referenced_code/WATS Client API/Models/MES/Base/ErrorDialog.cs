using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Globalization;
using System.Runtime.Versioning;

namespace Virinco.WATS.Interface.MES
{
    /// <summary>
    /// Error dialog for user
    /// </summary>
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    public partial class ErrorDialog : Form
    {

        MesBase apiRef;
        string cultureCode;

        /// <summary>
        /// Displays an error message to user
        /// </summary>
        /// <param name="apiRef"></param>
        /// <param name="cultureCode"></param>
        /// <param name="Caption"></param>
        /// <param name="Header"></param>
        /// <param name="Message"></param>
        /// <param name="AlwaysOnTop"></param>
        public ErrorDialog(MesBase apiRef, string cultureCode, string Caption, string Header, string Message, bool AlwaysOnTop=true)
        {
            this.apiRef = apiRef;
            this.cultureCode = cultureCode;
            this.TopMost = AlwaysOnTop;
            InitializeComponent();

            this.Caption = Caption;
            this.Message = Message;
            this.Header = Header;
        }
        
        /// <summary>Dialog caption</summary>
        public string Caption { get; set; }
        /// <summary>Dialog message</summary>
        public string Message { get; set; }
        /// <summary>Dialog header</summary>
        public string Header { get; set; }

        private void ErrorDialog_Load(object sender, EventArgs e)
        {
            string[] translations = apiRef.TranslateArray(cultureCode, new string[] { "Ok", Caption,Header});
            btnOK.Text = translations[0];
            this.Text = translations[1];
            lblErrorCaption.Text = translations[2];
            errorMessage.Text = Message; //Do not translate message
        }


    }
}
