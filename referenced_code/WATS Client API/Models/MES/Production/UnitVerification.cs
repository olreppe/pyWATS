//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;
//using Newtonsoft.Json;

//namespace Virinco.WATS.Interface.MES.Production
//{
//    /// <summary>
//    /// Response from <see cref="Production.GetUnitVerification(string, string)" />.
//    /// </summary>
//    public class UnitVerificationResponse
//    {
//        /// <summary>
//        /// Response status. <c>true</c> if unit has finished testing in all processes, else <c>false</c>.
//        /// </summary>
//        public bool Ok => string.Equals(Status, "ok", StringComparison.OrdinalIgnoreCase) || string.Equals(Status, "warning", StringComparison.OrdinalIgnoreCase);

//        /// <summary>
//        /// Unit status.
//        /// </summary>
//        [JsonProperty("status")]
//        public string Status { get; set; }

//        /// <summary>
//        /// Unit grade.
//        /// </summary>
//        [JsonProperty("grade")]
//        public string Grade { get; set; }

//        /// <summary>
//        /// Unit was tested in correct process order according to process index.
//        /// </summary>
//        [JsonProperty("allProcessesExecutedInCorrectOrder")]
//        public bool AllProcessesExecutedInCorrectOrder { get; set; }

//        /// <summary>
//        /// Unit passed in each process first time.
//        /// </summary>
//        [JsonProperty("allProcessesPassedFirstRun")]
//        public bool AllProcessesPassedFirstRun { get; set; }

//        /// <summary>
//        /// Unit passed at some point in each process, maybe after or before fail and repair.
//        /// </summary>
//        [JsonProperty("allProcessesPassedAnyRun")]
//        public bool AllProcessesPassedAnyRun { get; set; }

//        /// <summary>
//        /// Unit eventually passed in each process, maybe after fail and repair. See <see cref="TestProcessResult.NonPassedCount"/> and <see cref="TestProcessResult.RepairCount"/> per process.
//        /// </summary>
//        [JsonProperty("allProcessesPassedLastRun")]
//        public bool AllProcessesPassedLastRun { get; set; }

//        /// <summary>
//        /// Unit never needed repair.
//        /// </summary>
//        [JsonProperty("noRepairs")]
//        public bool NoRepairs { get; set; }

//        /// <summary>
//        /// Unit results per process in verification rule.
//        /// </summary>
//        [JsonProperty("results")]
//        public TestProcessResult[] ProcessResults { get; set; }        
//    }

//    /// <summary>
//    /// Unit results per process in verification rule.
//    /// </summary>
//    public class TestProcessResult
//    {
//        /// <summary>
//        /// Test operation code.
//        /// </summary>
//        [JsonProperty("processCode")]
//        public short ProcessCode { get; set; }

//        /// <summary>
//        /// Test operation name.
//        /// </summary>
//        [JsonProperty("processName")]
//        public string ProcessName { get; set; }

//        /// <summary>
//        /// Test operation order index.
//        /// </summary>
//        [JsonProperty("processIndex")]
//        public string ProcessIndex { get; set; }

//        /// <summary>
//        /// Unit test status in this process.
//        /// </summary>
//        [JsonProperty("status")]
//        public string StatusText { get; set; }

//        [JsonProperty("startUtc")]
//        private DateTime? startUtc;

//        /// <summary>
//        /// Test start date and time.
//        /// </summary>
//        [JsonIgnore]
//        public DateTime StartUtc 
//        {
//            get => startUtc ?? default;
//            set => startUtc = value;
//        }

//        /// <summary>
//        /// Name of test station.
//        /// </summary>
//        [JsonProperty("stationName")]
//        public string StationName { get; set; }

//        /// <summary>
//        /// How many times the unit was tested.
//        /// </summary>
//        [JsonProperty("totalCount")]
//        public int TotalCount { get; set; }

//        /// <summary>
//        /// How many times the unit didn't pass the test.
//        /// </summary>
//        [JsonProperty("nonPassedCount")]
//        public int NonPassedCount { get; set; }

//        [JsonProperty("repairCount")]
//        private int? repairCount;

//        /// <summary>
//        /// How many times the unit was repaired.
//        /// </summary>
//        [JsonIgnore]
//        public int RepairCount 
//        {
//            get => repairCount ?? 0;
//            set => repairCount = value;
//        }
//    }
//}
