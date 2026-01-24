extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using System;
using System.Linq;

namespace Virinco.WATS.Interface.MES.Production
{
    /// <summary>
    /// Response from <see cref="Production.GetUnitVerification(string, string)" />.
    /// </summary>
    public class UnitVerificationResponse
    {
        private napi.Production.UnitVerificationResponse _instance;

        internal UnitVerificationResponse(napi.Production.UnitVerificationResponse instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Response status. <c>true</c> if unit has finished testing in all processes, else <c>false</c>.
        /// </summary>
        public bool Ok // r/o
        {
            get => _instance.Ok;
            //set => _instance.Ok = value;
        }

        /// <summary>
        /// Unit status.
        /// </summary>
        public string Status
        {
            get => _instance.Status;
            set => _instance.Status = value;
        }

        /// <summary>
        /// Unit grade.
        /// </summary>
        public string Grade
        {
            get => _instance.Grade;
            set => _instance.Grade = value;
        }

        /// <summary>
        /// Unit was tested in correct process order according to process index.
        /// </summary>
        public bool AllProcessesExecutedInCorrectOrder
        {
            get => _instance.AllProcessesExecutedInCorrectOrder;
            set => _instance.AllProcessesExecutedInCorrectOrder = value;
        }

        /// <summary>
        /// Unit passed in each process first time.
        /// </summary>
        public bool AllProcessesPassedFirstRun
        {
            get => _instance.AllProcessesPassedFirstRun;
            set => _instance.AllProcessesPassedFirstRun = value;
        }

        /// <summary>
        /// Unit passed at some point in each process, maybe after or before fail and repair.
        /// </summary>
        public bool AllProcessesPassedAnyRun
        {
            get => _instance.AllProcessesPassedAnyRun;
            set => _instance.AllProcessesPassedAnyRun = value;
        }

        /// <summary>
        /// Unit eventually passed in each process, maybe after fail and repair. See <see cref="TestProcessResult.NonPassedCount"/> and <see cref="TestProcessResult.RepairCount"/> per process.
        /// </summary>
        public bool AllProcessesPassedLastRun
        {
            get => _instance.AllProcessesPassedLastRun;
            set => _instance.AllProcessesPassedLastRun = value;
        }

        /// <summary>
        /// Unit never needed repair.
        /// </summary>
        public bool NoRepairs
        {
            get => _instance.NoRepairs;
            set => _instance.NoRepairs = value;
        }

        /// <summary>
        /// Unit results per process in verification rule.
        /// </summary>
        public TestProcessResult[] ProcessResults
        {
            get => _instance.ProcessResults.Select(i => new TestProcessResult(i)).ToArray();
            set => _instance.ProcessResults = value.Select(i => i._instance).ToArray();
        }
    }


    /// <summary>
    /// Unit results per process in verification rule.
    /// </summary>
    public class TestProcessResult
    {
        internal napi.Production.TestProcessResult _instance;

        internal TestProcessResult(napi.Production.TestProcessResult instance)
        {
            _instance = instance;
        }

        /// <summary>
        /// Test operation code.
        /// </summary>
        public short ProcessCode
        {
            get => _instance.ProcessCode;
            set => _instance.ProcessCode = value;
        }

        /// <summary>
        /// Test operation name.
        /// </summary>
        public string ProcessName
        {
            get => _instance.ProcessName;
            set => _instance.ProcessName = value;
        }

        /// <summary>
        /// Test operation order index.
        /// </summary>
        public string ProcessIndex
        {
            get => _instance.ProcessIndex;
            set => _instance.ProcessIndex = value;
        }

        /// <summary>
        /// Unit test status in this process.
        /// </summary>
        public string StatusText
        {
            get => _instance.StatusText;
            set => _instance.StatusText = value;
        }

        /// <summary>
        /// Test start date and time.
        /// </summary>
        public DateTime StartUtc
        {
            get => _instance.StartUtc;
            set => _instance.StartUtc = value;
        }

        /// <summary>
        /// Name of test station.
        /// </summary>
        public string StationName
        {
            get => _instance.StationName;
            set => _instance.StationName = value;
        }

        /// <summary>
        /// How many times the unit was tested.
        /// </summary>
        public int TotalCount
        {
            get => _instance.TotalCount;
            set => _instance.TotalCount = value;
        }

        /// <summary>
        /// How many times the unit didn't pass the test.
        /// </summary>
        public int NonPassedCount
        {
            get => _instance.NonPassedCount;
            set => _instance.NonPassedCount = value;
        }

        /// <summary>
        /// How many times the unit was repaired.
        /// </summary>
        public int RepairCount
        {
            get => _instance.RepairCount;
            set => _instance.RepairCount = value;
        }
    }
}
