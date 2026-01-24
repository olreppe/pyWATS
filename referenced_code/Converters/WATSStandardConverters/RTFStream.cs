using System.IO;
using System.Windows.Forms;

namespace Virinco.WATS.Integration
{
    public class RTFStream : StreamReader
    {
        string text;
        int currentPosition=0;
        bool endOfStream=false;

        public RTFStream(Stream f) : base(f)
        {
            using (RichTextBox rtf = new RichTextBox())
            {
                using (StreamReader reader = new StreamReader(f))
                {
                    string rtfText = reader.ReadToEnd();
                    rtf.Rtf = rtfText;
                    text = rtf.Text;
                }
            }
        }

        public new bool EndOfStream
        {
            get { return endOfStream; }
        }

        public override string ReadLine()
        {
            string line = null;
            if (currentPosition >= text.Length)
            {
                endOfStream = true;
            }
            else
            {
                int nextEndOfLine = text.Substring(currentPosition).IndexOf('\n');
                if (nextEndOfLine == -1)
                {
                    line = text.Substring(currentPosition);
                    endOfStream = true;
                    currentPosition = text.Length;
                }
                else
                {
                    line = text.Substring(currentPosition, nextEndOfLine);
                    currentPosition = currentPosition + nextEndOfLine + 1;                    
                }
            }
            return line;
        }
    }
}
