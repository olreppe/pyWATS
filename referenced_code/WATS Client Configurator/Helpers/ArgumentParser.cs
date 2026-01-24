using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.CLUtil
{
    internal class ArgumentParser
    {
        internal ArgumentParser(string Command, string[] arguments)
        {
            this.Command = Command;
            parseArgs(arguments, 0);
        }
        internal ArgumentParser(string[] arguments)
        {
            this.Command = arguments[0];
            parseArgs(arguments, 1);
        }
        private void parseArgs(string[] arguments, int startIndex)
        {
            Options = new Dictionary<string, ArgumentOption>();
            if (arguments.Length > startIndex)
            {
                ArgumentOption option = null;
                for (int i = startIndex; i < arguments.Length; i++)
                {
                    if (arguments[i].StartsWith("/"))
                    {
                        option = new ArgumentOption(arguments[i].Substring(1));
                        Options.Add(option.Option, option);
                    }
                    else if (option != null)
                        option.OptionParameters.Add(arguments[i]);
                    //else
                    //    secondary command???
                }
            }
        }
        public string Command { get; private set; }
        public IDictionary<string, ArgumentOption> Options;
    }
    internal class ArgumentOption
    {
        internal ArgumentOption(string Option)
        {
            int colonIndex=Option.IndexOf(':');
            if (colonIndex > 0)
            {
                this.Option = Option.Substring(0, colonIndex);
                this.OptionParameters = new List<string>();
                this.OptionParameters.Add(Option.Substring(colonIndex + 1));
            }
            else
            {
                this.Option = Option;
                this.OptionParameters = new List<string>();
            }
        }
        public string Option { get; private set; }
        public IList<string> OptionParameters;
        public string Value { get { return String.Join(" ", OptionParameters.ToArray()); } }
    }

}
