using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
  

    /// <summary>
    /// This steptype supports steps that is not a test
    /// Depending on the Step
    /// </summary>
    public class GenericStep : Step
    {
        internal GenericStep(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName, string stepType) :
            base(uut, reportRow, parentStep, stepName)
        {
            //Trace.WriteLine("NonTestSep constructor " + stepName);
            stepRow.StepType = stepType;
        }

    }
}
