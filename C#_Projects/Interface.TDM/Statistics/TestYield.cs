using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Virinco.WATS.Interface.Statistics
{
    /// <summary>
    /// Client test yield for a part number and test operation.
    /// </summary>
    public class TestYield
    {
        /// <summary>
        /// The part number the test yield is for.
        /// </summary>
        public string PartNumber { get; }

        /// <summary>
        /// The code of the test operation the test yield is for.
        /// </summary>
        public string OperationTypeCode { get;}

        /// <summary>
        /// The name of the test operation the test yield is for.
        /// </summary>
        public string OperationTypeName { get; }

        /// <summary>
        /// The max number of reports for this part number and test operation on this client that the client keeps statistics for. The default is 2000.
        /// </summary>
        public int TotalCount { get; }

        /// <summary>
        /// The max number of reports for this part number and test operation on this client that the client treats as the latest reports. The default is 100.
        /// </summary>
        public int LastCount { get; }

        /// <summary>
        /// The yield of all the reports for this part number and test operation on this client this client keeps statistics for.
        /// </summary>
        public double TotalTestYield { get; }

        /// <summary>
        /// The yield of the latest reports for this part number and test operation on this client.
        /// </summary>
        public double LastTestYield { get; }

        /// <summary>
        /// The yield difference between <see cref="TotalTestYield"/> and <see cref="LastTestYield"/>.
        /// </summary>
        public double TestYieldDifference { get; }

        /// <summary>
        /// The total number of reports for this part number and test operation on this client this client has statistics for.
        /// </summary>
        public int TotalUUTReportsCount { get; }

        /// <summary>
        /// The number of reports for this part number and test operation on this client that is treated as the latest reports.
        /// </summary>
        public int LastUUTReportsCount { get; }

        /// <summary>
        /// All the report results for this part number and test operation on this client this client has statistics for.
        /// It is a line of P and F characters, starting with the latest report.
        /// </summary>
        public string TotalResults { get; }

        /// <summary>
        /// The latest report results for this part number and test operation on this client this client has statistics for.
        /// It is a line of P and F characters, starting with the latest report.
        /// </summary>
        public string LastResults { get; }

        /// <summary>
        /// The test yield trend for this part number and test operation on this client.
        /// </summary>
        public int[] Trend { get; }

        /// <summary>
        /// The threshold for warning about low test yield.
        /// </summary>
        public double WarnLevel { get; }

        /// <summary>
        /// The threshold for the test yield being critically low.
        /// </summary>
        public double CriticalLevel { get; }

        public TestYield(string partNumber, string operationTypeCode, string operationTypeName, int totalCount, int lastCount, double totalTestYield, double lastTestYield, double testYieldDifference, int totalUUTReportsCount, int lastUUTReportsCount, string totalResults, string lastResults, int[] trend, double warnLevel, double criticalLevel)
        {
            PartNumber = partNumber;
            OperationTypeCode = operationTypeCode;
            OperationTypeName = operationTypeName;
            TotalCount = totalCount;
            LastCount = lastCount;
            TotalTestYield = totalTestYield;
            LastTestYield = lastTestYield;
            TestYieldDifference = testYieldDifference;
            TotalUUTReportsCount = totalUUTReportsCount;
            LastUUTReportsCount = lastUUTReportsCount;
            TotalResults = totalResults;
            LastResults = lastResults;
            Trend = trend;
            WarnLevel = warnLevel;
            CriticalLevel = criticalLevel;
        }
    }
}
