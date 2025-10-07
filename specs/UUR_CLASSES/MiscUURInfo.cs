using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Interface.Models;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    public class MiscUURInfoColletion : IEnumerable<MiscUURInfo>
    {
        //private IEnumerable<MiscUURInfo> miscInfos;
        private MiscUURInfo[] miscInfos;

        public MiscUURInfoColletion(IEnumerable<MiscUURInfo> value)
        {
            this.miscInfos = value.ToArray();
        }

        public IEnumerator<MiscUURInfo> GetEnumerator()
        {
            return miscInfos.AsEnumerable<MiscUURInfo>().GetEnumerator();
        }

        IEnumerator IEnumerable.GetEnumerator()
        {
            return miscInfos.GetEnumerator();
        }

        /// <summary>
        /// Collection property accessor for UUR MiscInfo using ordinal index field. 
        /// </summary>
        /// <param name="fieldIndex">UUR MiscInfo field ordinal index</param>
        /// <returns>Sets or gets the value for the given repair miscinfo field</returns>
        public string this[int fieldIndex]
        {
            get
            {
                return miscInfos[fieldIndex].DataString;//.Where(e => string.Compare(e.Description, fieldName, true) == 0).Single().DataString;
            }
            set
            {
                var mi = miscInfos[fieldIndex];

                mi.DataString = value;
            }
        }

        /// <summary>
        /// Collection property accessor for UUR MiscInfo using description field. FieldName must be unique in the repair definition, or this indexer will fail
        /// </summary>
        /// <param name="fieldName">UUR MiscInfo Description field name</param>
        /// <returns>Sets or gets the value for the given repair miscinfo field</returns>
        public string this[string fieldName]
        {
            get
            {
                return miscInfos.Where(e => string.Compare(e.Description, fieldName, true) == 0).Single().DataString;
            }
            set
            {
                var mi = miscInfos.Single(e => string.Compare(e.Description, fieldName, true) == 0).DataString = value;
            }
        }
        
        ///TODO: Decide if get/set by id (guid) should be allowed (Id field is only internal accessible).
        /*        
        /// <summary>
        /// Collection property accessor for UUR MiscInfo using miscinfo id-field. 
        /// </summary>
        /// <param name="fieldIndex">UUR MiscInfo field ordinal index</param>
        /// <returns>Sets or gets the value for the given repair miscinfo field</returns>
        public string this[Guid fieldId]
        {
            get
            {
                return miscInfos.Where(e => e.Id == fieldId).Single().DataString;

            }
            set
            {
                miscInfos.Where(e => e.Id == fieldId).Single().DataString = value;
            }
        }
        */

    }

    /// <summary>
    /// Misc information attached to an UUR
    /// </summary>
    public class MiscUURInfo
    {
        internal MiscInfo_type miData;
        private Virinco.WATS.Interface.Models.MiscInfo miDef;
        private UURReport report;

        internal MiscUURInfo(MiscInfo miscInfoDefinition, MiscInfo_type miscInfoData, UURReport uur)
        {
            report = uur;
            this.miDef = miscInfoDefinition;
            if (miscInfoData != null)
                this.miData = miscInfoData;
            else
                this.miData = new MiscInfo_type()
                { Id = miDef.GUID.ToString(), Description = miDef.Description };
        }

        /// <summary>
        /// A regular expression will be validated 
        /// </summary>
        public string ValidRegularExpression
        {
            get { return miDef.ValidRegex; }
        }

        /// <summary>
        /// GUI mask
        /// </summary>
        public string InputMask
        {
            get { return miDef.InputMask; }
        }


        /// <summary>
        /// The information description, e.g. SWVer1
        /// </summary>
        public string Description
        {
            get { return miDef.Description; }
        }

        /// <summary>
        /// The string value of the info, e.g. 1.15.3
        /// </summary>
        public string DataString
        {
            get { return miData.Value; }
            set { miData.Value = report.api.SetPropertyValidated<MiscInfo_type>("Value", value, "DataString"); }
        }

        internal Guid Id
        {
            get { return miDef.GUID; }
        }
    }
}

