using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Reserved for use with TestStand. Does not show up in analysis.
    /// An additional result can represent any kind of data as XML. Only data formatted the way TestStand does is shown in UUT report. 
    /// </summary>
    public class AdditionalResult
    {
        private readonly UUTReport report;
        private readonly AdditionalResults_type row;

        internal AdditionalResult(UUTReport uut, Step parentStep, string Name, System.Xml.Linq.XElement Contents)
        {
            report = uut;
            row = new AdditionalResults_type() 
            { 
                StepID = parentStep.StepOrderNumber, 
                StepIDSpecified = true
            };

            this.Name = Name;
            this.Contents = Contents;

            uut.reportRow.Items.Add(row);
        }

        internal AdditionalResult(UUTReport uut, AdditionalResults_type additionalResults)
        {
            report = uut;
            row = additionalResults;
        }

        /// <summary>
        /// Element Name
        /// </summary>
        public string Name
        {
            get { return row.Name; }
            set { row.Name = report.api.SetPropertyValidated<AdditionalResults_type>("Name", value); }
        }
        /// <summary>
        /// Contents
        /// </summary>
        public System.Xml.Linq.XElement Contents
        {
            get { return System.Xml.Linq.XElement.Parse(row.Any.First().OuterXml); }
            set 
            {
                if (new System.Xml.XmlDocument().ReadNode(value.CreateReader()) is System.Xml.XmlElement el)
                    row.Any.Add(el);
            }
        }
    }
}
