using System;
using System.Collections.Generic;
using System.Linq;
//using System.Web;

namespace Virinco.WATS.Service.MES.Contract
{
    public partial class Tag
    {

        string _value = string.Empty;
        public string Value
        {
            get
            {
                return _value;
            }

            set
            {
                if (_value != value)
                {
                    _value = value;
                    OnPropertyChanged("Value");
                }
            }
        }
                
        public bool ReadOnly
        {
            get
            {
                return ((TagType & TagTypeEnum.ReadOnly) == TagTypeEnum.ReadOnly);
            }

            set
            {
                //TagTypeEnum tes = TagTypeEnum.None;
                //tes = TagType | TagTypeEnum.ReadOnly;
                //tes = TagType & ~TagTypeEnum.ReadOnly;

                if (value)
                    TagType |= TagTypeEnum.ReadOnly;
                else
                    TagType &= ~TagTypeEnum.ReadOnly;

                OnPropertyChanged("ReadOnly");
            }
        }



        TagTypeEnum _tagType = TagTypeEnum.None;
        public TagTypeEnum TagType
        {
            
            get
            {
                #if NETFX_35
                    Utilities.EnumTryParse<TagTypeEnum>(Type.ToString(), out _tagType);
                #else 
                    Enum.TryParse<TagTypeEnum>(Type.ToString(), out _tagType);
                #endif
                return _tagType;
            }

            set
            {
                if (_tagType != value)
                {
                    _tagType = value;
                    Type = (int)_tagType;
                    OnPropertyChanged("TagType");
                }
            }
        }

    }
}