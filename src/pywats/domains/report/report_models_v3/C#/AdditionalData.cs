using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// An additional data can represent any kind of data, formatted as xml node.
    /// </summary>
    public class AdditionalData
    {
        private readonly Report report;
        private readonly AdditionalData_type _row;

        internal AdditionalData(Report report, string name, System.Xml.Linq.XElement contents)
        {
            this.report = report;
            _row = new AdditionalData_type { Name = name, Idx = report.reportRow.AdditionalData.Count, IdxSpecified = true };

            var el = new System.Xml.XmlDocument().ReadNode(contents.CreateReader()) as System.Xml.XmlElement;
            if (el != null)
                _row.Any.Add(el);

            report.reportRow.AdditionalData.Add(_row);            
        }

        /// <summary>
        /// Element Name
        /// </summary>
        public string Name
        {
            get { return _row.Name; }
            set { _row.Name = report.api.SetPropertyValidated<AdditionalData_type>("Name", value); }
        }

        /// <summary>
        /// Contents
        /// </summary>
        public System.Xml.Linq.XElement Contents
        {
            get { return System.Xml.Linq.XElement.Parse(_row.Any.First().OuterXml); }
            set
            {
                var el = (new System.Xml.XmlDocument()).ReadNode(value.CreateReader()) as System.Xml.XmlElement;
                if (el != null) 
                    _row.Any.Add(el);
            }
        }
    }
}
