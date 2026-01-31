using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represent a popup message box to user.
    /// </summary>
    public class MessagePopupStep : Step
    {
        private readonly MessagePopup_type row;

        internal MessagePopupStep(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName, short buttonPressed, string response) :
            base(uut, reportRow, parentStep, stepName)
        {
            stepRow.StepType = StepTypeEnum.MessagePopup.ToString();
            row = new MessagePopup_type()
            {
                StepID = base.stepRow.StepID,
                MeasIndex = 0,
                Button = buttonPressed,
                ButtonSpecified = true,
                Response = report.api.SetPropertyValidated<MessagePopup_type>("Response", response)
            };
            reportRow.Items.Add(row);
        }

        internal MessagePopupStep(Step_type step, WATSReport reportRow, MessagePopup_type messagePopup, UUTReport uut) : base(step, reportRow, uut)
        {
            row = messagePopup;
        }

        /// <summary>
        /// The index of the button pressed in the popup.
        /// </summary>
        public short ButtonPressed
        {
            get { return row.Button; }
            set { row.Button = value; }
        }

        /// <summary>
        /// The response text of the popup.
        /// </summary>
        public string Response
        {
            get { return row.Response; }
            set { row.Response = report.api.SetPropertyValidated<MessagePopup_type>("Response", value); }
        }

        /// <summary>
        /// The number format for the button. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string ButtonFormat
        {
            get => row.ButtonFormat;
            set => row.ButtonFormat = value;
        }

        protected internal override void RemoveStepData()
        {
            base.RemoveStepData();
            reportRow.Items.RemoveAll(o => o is MessagePopup_type m && m.StepID == stepRow.StepID);
        }
    }
}
