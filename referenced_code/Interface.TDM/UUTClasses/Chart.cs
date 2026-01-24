extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface;
using System.Linq;

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
        internal napi.ChartSerie _instance;
        internal ChartSerie(napi.ChartSerie instance) { _instance = instance; }

        /// <summary>
        /// Name of plot serie
        /// </summary>
        public string PlotName // r/o
        {
            get => _instance.PlotName;
            //set => _instance.PlotName = value;
        }

        /// <summary>
        /// Gets the X and Y values of a plot serie
        /// </summary>
        /// <param name="xValues"></param>
        /// <param name="yValues"></param>
        public void GetValues(out double[] xValues, out double[] yValues)
            => _instance.GetValues(out xValues, out yValues);
    }

    /// <summary>
    /// A chart step represents graph of numeric series.
    /// </summary>
    public class Chart
    {
        internal napi.Chart _instance;
        internal Chart(napi.Chart instance) { _instance = instance; }

        /// <summary>
        /// Returns Chart series 
        /// </summary>
        public ChartSerie[] Series // r/o
        {
            get => _instance.Series.Select(s => new ChartSerie(s)).ToArray();
            //set => _instance.Series.Select(s => new ChartSerie(s)).ToArray() = value;
        }

        /// <summary>
        /// Chart type
        /// </summary>
        public ChartType ChartType // r/o
        {
            get => _instance.ChartType.CastTo<ChartType>();
            //set => _instance.ChartType.CastTo<ChartType>() = value;
        }

        /// <summary>
        /// Chart label
        /// </summary>
        public string ChartLabel // r/o
        {
            get => _instance.ChartLabel;
            //set => _instance.ChartLabel = value;
        }

        /// <summary>
        /// XLabel
        /// </summary>
        public string XLabel // r/o
        {
            get => _instance.XLabel;
            //set => _instance.XLabel = value;
        }

        /// <summary>
        /// XUnit
        /// </summary>
        public string XUnit // r/o
        {
            get => _instance.XUnit;
            //set => _instance.XUnit = value;
        }

        /// <summary>
        /// YLabel
        /// </summary>
        public string YLabel // r/o
        {
            get => _instance.YLabel;
            //set => _instance.YLabel = value;
        }

        /// <summary>
        /// YUnit
        /// </summary>
        public string YUnit // r/o
        {
            get => _instance.YUnit;
            //set => _instance.YUnit = value;
        }

        /// <summary>
        /// Adds a plot series to the graph
        /// </summary>
        /// <param name="seriesName"></param>
        /// <param name="dataValues"></param>
        public void AddSeries(string seriesName, double[,] dataValues)
            => _instance.AddSeries(seriesName, dataValues);

        /// <summary>
        /// Adds a series to the graph, specifying data in two double arrays
        /// </summary>
        /// <param name="seriesName"></param>
        /// <param name="xValues"></param>
        /// <param name="yValues"></param>
        public void AddSeries(string seriesName, double[] xValues, double[] yValues)
            => _instance.AddSeries(seriesName, xValues, yValues);

        /// <summary>
        /// Adds a series to the graph, using x values 0,1,2..N-1
        /// </summary>
        /// <param name="seriesName"></param>
        /// <param name="yValues"></param>
        public void AddSeries(string seriesName, double[] yValues)
            => _instance.AddSeries(seriesName, yValues);
    }
}
