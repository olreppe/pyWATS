using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS.Client.PackageManager
{
    public class HelpViewModel : ObservableObject
    {
        public string HelpText 
        {
            get => helpText;
            set
            {
                helpText = value;
                OnPropertyChanged(HelpText);
            }
        }

        public string Version { get; }

        private string helpText = @"---!!! HELP !!!---
The download manager will contact the WATS server and check for available packages at configured intervals.
The configured filter is used to create an XPath query. 

Example filter:
PartNumber=pn1|pn2|pn3;
StationName=st3;
OR;
PartNumber=pn4 OR Misc=misc1;

Result: 
2 groups as follow:
PartNumber equal pn1, pn2 or pn3 AND StationName equal st3
Or
Partnumber equal pn4 OR Misc equal misc1


- Lines must end with semicolon
    ;

- All lines in a group must match
    Lines are AND'ed together (&&)
                           
- Tags and values are separated with =
    TagName=TagValue

- Use the | (pipe) character to specify multiple values
    TagName=TagValue1|TagValue2|TagValue3

- Match multiple tags with OR
    TagName1=Value1 OR TagName2=Value2

- Create multiple groups by specifying a single OR
    OR;

-Use <StationName> to replace with the current machine-name
    StationName=<StationName>
    
    
";

        public HelpViewModel()
        {
            Version version = System.Reflection.Assembly.GetExecutingAssembly().GetName().Version;
            Version = Utilities.GetMSIVersionString(version);
        }
    }
}
