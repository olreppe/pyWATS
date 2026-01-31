using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{

    /// <summary>
    /// Chart type
    /// </summary>
    public enum ChartType : short
    {
        /// <summary>
        /// Normal, linear X-Y graph
        /// </summary>
        Line = 0,
        /// <summary>
        /// Use logaritmic scaling on both axis
        /// </summary>
        LineLogXY = 1,
        /// <summary>
        /// Use logaritmic scaling on X-Axis
        /// </summary>
        LineLogX = 2,
        /// <summary>
        /// Use logaritmic scaling on Y-Axis
        /// </summary>
        LineLogY = 3

    }


    /// <summary>
    /// Return a XY plot serie of a graph
    /// </summary>
    public class ChartSerie
    {
        Chart_type chartRow;
        internal ChartSerie(Chart_type chart_Type)
        {
            chartRow = chart_Type;
        }

        /// <summary>
        /// Name of plot serie
        /// </summary>
        public string PlotName { get { return chartRow.PlotName; } }
        /// <summary>
        /// Gets the X and Y values of a plot serie
        /// </summary>
        /// <param name="xValues"></param>
        /// <param name="yValues"></param>
        public void GetValues(out double[] xValues, out double[] yValues)
        {
            int valueCount = chartRow.Data.Length/16;
            xValues = new double[valueCount];
            yValues = new double[valueCount];
            for (int i = 0; i < valueCount; i++)
            {
                xValues[i] = BitConverter.ToDouble(chartRow.Data, i * 16);
                yValues[i] = BitConverter.ToDouble(chartRow.Data, (i * 16) + 8);
            }
        }
    }


    /// <summary>
    /// A chart step represents graph of numeric series.
    /// </summary>
    public class Chart
    {

        /// <summary>
        /// Returns Chart series 
        /// </summary>
        public ChartSerie[] Series
        {
            get
            {
                Chart_type[] charts = reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == parent.StepOrderNumber && c.idx>0).ToArray();
                List<ChartSerie> series = new List<ChartSerie>();
                for (int i = 0; i < charts.Length; i++)
                    series.Add(new ChartSerie(charts[i]));
                return series.ToArray();
            }
        }

        private Chart_type ChartRow
        {
            get
            {
                return reportRow.Items.OfType<Chart_type>().Where(c => c.StepID == parent.StepOrderNumber && c.idx == 0).FirstOrDefault();
            }
        }



        /// <summary>
        /// Chart type
        /// </summary>
        public ChartType ChartType { get { return (ChartType)Enum.Parse(typeof(ChartType), ChartRow.ChartType); } }
        /// <summary>
        /// Chart label
        /// </summary>
        public string ChartLabel { get { return ChartRow.Label; } }
        /// <summary>
        /// XLabel
        /// </summary>
        public string XLabel { get { return ChartRow.XLabel; } }
        /// <summary>
        /// XUnit
        /// </summary>
        public string XUnit { get { return ChartRow.XUnit; } }
        /// <summary>
        /// YLabel
        /// </summary>
        public string YLabel { get { return ChartRow.YLabel; } }
        /// <summary>
        /// YUnit
        /// </summary>
        public string YUnit { get { return ChartRow.YUnit; } }



        private WATSReport reportRow;
        private short measureIndex = 0;
        Step parent;
        UUTReport uutReport;

        internal Chart(UUTReport uut, WATSReport reportRow, Step parentStep)
        {
            this.reportRow = reportRow;
            uutReport = uut;
            parent = parentStep;
        }


        internal Chart(UUTReport uut, WATSReport reportRow, Step parentStep, ChartType chartType, string chartLabel, string xLabel, string xUnit, string yLabel, string yUnit)
        {
            this.reportRow = reportRow;
            uutReport = uut;
            parent = parentStep;
            Chart_type r = new Chart_type()
            {
                StepID = parent.stepRow.StepID,
                idx = measureIndex,
                idxSpecified = true,
                Label = uutReport.api.SetPropertyValidated<Chart_type>("Label", chartLabel),
                XLabel = uutReport.api.SetPropertyValidated<Chart_type>("XLabel", xLabel),
                XUnit = uutReport.api.SetPropertyValidated<Chart_type>("XUnit", xUnit),
                YLabel = uutReport.api.SetPropertyValidated<Chart_type>("YLabel", yLabel),
                YUnit = uutReport.api.SetPropertyValidated<Chart_type>("YUnit", yUnit),
                ChartType = chartType.ToString()
            };
            measureIndex++;
            this.reportRow.Items.Add(r);
        }

        /// <summary>
        /// Adds a plot series to the graph
        /// </summary>
        /// <param name="seriesName"></param>
        /// <param name="dataValues"></param>
        public void AddSeries(string seriesName, double[,] dataValues)
        {
            ValidateSeries();

            int points = dataValues.GetLength(1);
            int numberOfBytes = 16 * points; //Use 2x8 for X and Y
            byte[] data = new byte[numberOfBytes];
            for (int i = 0; i < points; i++)
            {
                byte[] x = BitConverter.GetBytes(dataValues[0, i]);
                byte[] y = BitConverter.GetBytes(dataValues[1, i]);
                Array.Copy(x, 0, data, i * 16, 8);
                Array.Copy(y, 0, data, i * 16 + 8, 8);
            }
            Chart_type r = new Chart_type()
            {
                StepID = parent.stepRow.StepID,
                idx = measureIndex,
                idxSpecified = true,
                PlotName = uutReport.api.SetPropertyValidated<Chart_type>(nameof(Chart_type.PlotName), seriesName, "seriesName"),
                Data = data,
                DataType = "XYG"
            };
            measureIndex++;
            reportRow.Items.Add(r);
        }


        /// <summary>
        /// Adds a series to the graph, specifying data in two double arrays
        /// </summary>
        /// <param name="seriesName"></param>
        /// <param name="xValues"></param>
        /// <param name="yValues"></param>
        public void AddSeries(string seriesName, double[] xValues, double[] yValues)
        {
            ValidateSeries();

            if (xValues.GetLength(0) != yValues.GetLength(0))
            {
                ApplicationException ex = new ApplicationException("X and Y arrays must have the same number of elements");
                Env.Trace.TraceData(System.Diagnostics.TraceEventType.Error, 0, new WATSLogItem() { ex = ex, Message = "AddSerie error" });
            }
            int points = xValues.GetLength(0);
            int numberOfBytes = 16 * points; //Use 2x8 for X and Y
            byte[] data = new byte[numberOfBytes];
            for (int i = 0; i < points; i++)
            {
                byte[] x = BitConverter.GetBytes(xValues[i]);
                byte[] y = BitConverter.GetBytes(yValues[i]);
                Array.Copy(x, 0, data, i * 16, 8);
                Array.Copy(y, 0, data, i * 16 + 8, 8);
            }

            Chart_type r = new Chart_type()
            {
                StepID = parent.stepRow.StepID,
                idx = measureIndex,
                idxSpecified = true,
                PlotName = uutReport.api.SetPropertyValidated<Chart_type>(nameof(Chart_type.PlotName), seriesName, "seriesName"),
                Data = data,
                DataType = "XYG"
            };
            measureIndex++;
            reportRow.Items.Add(r);
        }

        /// <summary>
        /// Adds a series to the graph, using x values 0,1,2..N-1
        /// </summary>
        /// <param name="seriesName"></param>
        /// <param name="yValues"></param>
        public void AddSeries(string seriesName, double[] yValues)
        {
            ValidateSeries();

            double[] xValues = new double[yValues.GetLength(0)];
            for (int i = 0; i < xValues.GetLength(0); i++)
                xValues[i] = i;
            AddSeries(seriesName, xValues, yValues);
        }

        private void ValidateSeries()
        {
            if(measureIndex > uutReport.api.proxy.MaxChartSeries)
            {
                switch(uutReport.api.ValidationMode)
                {
                    case ValidationModeType.ThrowExceptions:
                        throw new InvalidOperationException($"Cannot add more than {uutReport.api.proxy.MaxChartSeries} series to a chart");
                    case ValidationModeType.AutoTruncate:
                        return;
                }
            }
        }
    }
}
