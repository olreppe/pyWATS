using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS.Interface.Statistics
{
    /// <summary>
    /// Used to get client test yield for a part number and test operation.
    /// </summary>
    public class YieldMonitor
    {
        /// <summary>
        /// Yield monitor transparency setting. Set in WATS Client Configurator.
        /// </summary>
        public double Tranparency 
        {
            get => reader.Transparency; 
        }

        /// <summary>
        /// Yield monitor always on top setting. Set in WATS Client Configurator.
        /// </summary>
        public bool AlwaysOnTop
        {
            get => reader.AlwaysOnTop;
        }

        /// <summary>
        /// Yield monitor run on startup setting. Set in WATS Client Configurator.
        /// </summary>
        public bool RunOnStartup
        {
            get => reader.RunOnStartUp;
        }

        /// <summary>
        /// Event invoked when any statistics are updated.
        /// </summary>
        public event EventHandler Updated; 

        private readonly TDM api;
        private readonly StatisticsReader reader;

        internal YieldMonitor(TDM api)
        {
            this.api = api;
            reader = new StatisticsReader();
            reader.PropertyChanged += (s, e) => OnUpdated();
        }

        /// <summary>
        /// Get test yield for a part number and test operation from this client.
        /// </summary>
        /// <param name="partNumber">The part number to get test yield for.</param>
        /// <param name="testOperationCode">The test operation to get test yield for.</param>
        public TestYield GetTestYield(string partNumber, string testOperationCode)
        {  
            if (string.IsNullOrEmpty(testOperationCode))
                throw new ArgumentException("Cannot be empty.", nameof(testOperationCode));

            if (!short.TryParse(testOperationCode, out short code))
                throw new ArgumentException("Must be a number.", nameof(testOperationCode));

            return GetTestYield(partNumber, code);
        }

        /// <summary>
        /// Get test yield for a part number and test operation from this client.
        /// </summary>
        /// <param name="partNumber">The part number to get test yield for.</param>
        /// <param name="testOperationCode">The test operation to get test yield for.</param>
        public TestYield GetTestYield(string partNumber, short testOperationCode)
        {
            var testOperation = api.GetOperationType(testOperationCode);
            return GetTestYield(partNumber, testOperation);
        }

        /// <summary>
        /// Get test yield for a part number and test operation from this client.
        /// </summary>
        /// <param name="partNumber">The part number to get test yield for.</param>
        /// <param name="operationType">The test operation to get test yield for.</param>
        public TestYield GetTestYield(string partNumber, OperationType operationType)
        {
            if (string.IsNullOrEmpty(partNumber))
                throw new ArgumentException("Cannot be empty.", nameof(partNumber));

            if (!operationType.process.IsTestOperation)
                throw new ArgumentException($"Must be a test operation.", nameof(operationType));

            var product = reader.GetProduct(partNumber);
            var productOperation = reader.GetProductOperation(product, operationType.Id.ToString());

            return new TestYield
            (
                product.PN,
                operationType.Code,
                operationType.Name,
                product.TotalCount,
                product.LastCount,
                reader.GetTestYieldTotal(productOperation),
                reader.GetTestYieldLast(product, productOperation),
                reader.GetTestYieldDiff(product, productOperation),
                reader.GetTotalCount(productOperation),
                reader.GetLastCount(product, productOperation),
                reader.GetTotalResults(productOperation),
                reader.GetLastResults(product, productOperation),
                reader.GetTrend(product, productOperation).ToArray(),
                product.WarnLevel,
                product.CriticalLevel
            );
        }

        private void OnUpdated()
        {
            Updated?.Invoke(this, new EventArgs());
        }
    }
}
