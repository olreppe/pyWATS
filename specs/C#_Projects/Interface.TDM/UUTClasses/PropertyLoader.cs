using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Teststand property loader
    /// </summary>
    public class PropertyLoaderStep : Step
    {
        private readonly PropertyLoader_type row;

        internal PropertyLoaderStep(UUTReport uut, WATSReport reportRow, SequenceCall parentStep, string stepName, short numPropApplied, short numPropRead) :
            base(uut, reportRow, parentStep, stepName)
        {
            stepRow.StepType = StepTypeEnum.NI_VariableAndPropertyLoader.ToString();
            row = new PropertyLoader_type()
            {
                StepID = stepRow.StepID,
                MeasIndex = 0,
                MeasIndexSpecified = true,
                Applied = numPropApplied,
                AppliedSpecified = true,
                Read = numPropRead,
                ReadSpecified = true
            };
            reportRow.Items.Add(row);

        }

        internal PropertyLoaderStep(Step_type step, WATSReport reportRow, PropertyLoader_type propertyLoader, UUTReport uut) : base(step, reportRow, uut)
        {
            row = propertyLoader;
        }

        public short PropertiesRead
        {
            get => row.Read;
            set => row.Read = value;
        }

        public short PropertiesApplied
        {
            get => row.Applied;
            set => row.Applied = value;
        }

        protected internal override void RemoveStepData()
        {
            base.RemoveStepData();
            reportRow.Items.RemoveAll(o => o is PropertyLoader_type p && p.StepID == stepRow.StepID);
        }
    }
}
