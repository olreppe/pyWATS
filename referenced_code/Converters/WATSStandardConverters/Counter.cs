using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Virinco.WATS.Integration
{
    class Counter
    {
        protected int currentCounter = 0;
        public int Increment()
        {
            return currentCounter++;
        }

        public void ResetCounter()
        {
            currentCounter = 0;
        }
    }

    class StackableCounter : Counter
    {
        private Stack<int> counters = new Stack<int>();

        public void NewCounter()
        {
            counters.Push(currentCounter);
            currentCounter = 0;
        }

        public void PreviousCounter()
        {
            currentCounter = counters.Pop();
        }
    }
}
