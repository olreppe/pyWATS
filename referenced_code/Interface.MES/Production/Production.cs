extern alias newclientapi;

using napi = newclientapi::Virinco.WATS.Interface.MES;
using napict = newclientapi::Virinco.WATS.Service.MES.Contract;
using ct = Virinco.WATS.Service.MES.Contract;
using System.Collections.Generic;
using System;
using System.Linq;

namespace Virinco.WATS.Interface.MES.Production
{
    /// <summary>
    /// Class provided to handle unit info (on serialnumber/parnumber)
    /// </summary>
    public class Production : MesBase
    {
        private napi.Production.Production _instance;

        internal Production(napi.Production.Production production)
        {
            this._instance = production;
        }


        public new bool isConnected()
            => _instance.isConnected();

        /// <summary>
        /// If <see cref="IdentifyUUT(out bool, string)"/> is called and this is set to true,
        /// the Display TreeView checkbox is checked. If the checkbox
        /// is not checked, the form will automatically close when the serialnumber
        /// ends with \r\n
        /// </summary>
        public bool DisplayTreeView
        {
            get => _instance.DisplayTreeView;
            set => _instance.DisplayTreeView = value;
        }

        /// <summary>
        /// Holds information about the last scanned serialnumber
        /// </summary>
        public string LastScannedSerialnumber
        {
            get => _instance.LastScannedSerialnumber;
            set => _instance.LastScannedSerialnumber = value;
        }

        /// <summary>
        /// Return <see cref="UnitInfo"/> object (no GUI)
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <returns>A <see cref="UnitInfo"/> object with info about the SN supplied.</returns>
        public UnitInfo GetUnitInfo(string SerialNumber, string PartNumber = "")
            => new UnitInfo(_instance.GetUnitInfo(SerialNumber, PartNumber));

        /// <summary>
        /// Displays SN textbox if connected to service
        /// </summary>
        /// <returns>A <see cref="UnitInfo"/> object of the scanned unit.</returns>
        /// <param name="Continue">Boolean value indicating if the process was stopped</param>        
        /// <param name="PartNumber">PartNumber of unit to identify (used in case of none unique serialnumbers)</param>
        public UnitInfo IdentifyUUT(out bool Continue, string PartNumber = "")
            => new UnitInfo(_instance.IdentifyUUT(out Continue, PartNumber));

        /// <summary>
        /// Display dialog to prompt for serial number
        /// </summary>
        /// <param name="Continue"></param>
        /// <param name="SelectedTestOperation"></param>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <param name="IncludeTestOperation"></param>
        /// <param name="SelectTestOperation"></param>
        /// <param name="CustomText"></param>
        /// <param name="AlwaysOnTop"></param>
        /// <param name="UseWorkflow"></param>
        /// <param name="WorkflowStatus"></param>
        /// <param name="context"></param>
        /// <returns></returns>
        public UnitInfo IdentifyUUT(out bool Continue, ref Virinco.WATS.Service.MES.Contract.Process SelectedTestOperation, string SerialNumber = "", string PartNumber = "", bool IncludeTestOperation = false, bool SelectTestOperation = true, string CustomText = null, bool AlwaysOnTop = true, bool UseWorkflow = false, ct.StatusEnum WorkflowStatus = ct.StatusEnum.Released, Dictionary<string, object> context = null)
        {
            napict.Process p = SelectedTestOperation.NewApiInstance;
            var res = _instance.IdentifyUUT(out Continue, ref p, SerialNumber, PartNumber, IncludeTestOperation, SelectTestOperation, CustomText, AlwaysOnTop, UseWorkflow, (napict.StatusEnum)(int)WorkflowStatus, context);
            SelectedTestOperation.NewApiInstance = p;
            return new UnitInfo(res);
        }
        //=> _instance.IdentifyUUT(out Continue, ref SelectedTestOperation, SerialNumber, PartNumber, IncludeTestOperation, SelectTestOperation, CustomText, AlwaysOnTop, UseWorkflow, WorkflowStatus, context);

        /// <summary>
        /// Sets a unit's process to a given value
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <param name="ProcessName">Unit's new processname</param>        
        public void SetUnitProcess(string SerialNumber, string PartNumber, string ProcessName)
            => _instance.SetUnitProcess(SerialNumber, PartNumber, ProcessName);

        /// <summary>
        /// Sets a unit's phase.
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <param name="Phase">Unit's new phase,</param>
        public void SetUnitPhase(string SerialNumber, string PartNumber, ct.Unit_Phase Phase)
            => _instance.SetUnitPhase(SerialNumber, PartNumber, (napict.Unit_Phase)(int)Phase);

        /// <summary>
        /// Sets a unit's phase.
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <param name="Phase">Unit's new phase,</param>
        public void SetUnitPhase(string SerialNumber, string PartNumber, string Phase)
            => _instance.SetUnitPhase(SerialNumber, PartNumber, Phase);

        /// <summary>
        /// Get a unit's current process
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <returns>Unit's current process</returns>
        public string GetUnitProcess(string SerialNumber, string PartNumber)
            => _instance?.GetUnitProcess(SerialNumber, PartNumber);

        /// <summary>
        /// Get a unit's phase.         
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>        
        /// <returns>Units current Phase enum</returns>
        public ct.Unit_Phase GetUnitPhase(string SerialNumber, string PartNumber)
            => (ct.Unit_Phase)(int)_instance.GetUnitPhase(SerialNumber, PartNumber);

        /// <summary>
        /// Get a unit's phase.         
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>       
        /// <returns>Units current Phase as string</returns>
        public string GetUnitPhaseString(string SerialNumber, string PartNumber)
            => _instance.GetUnitPhaseString(SerialNumber, PartNumber);

        /// <summary>
        /// Returns unit history of state / phase changes. Changes are returned in three corresponding arrays due to index. Latest change is found on index 0;
        /// </summary>
        /// <param name="serialNumber"></param>
        /// <param name="partNumber"></param>
        /// <param name="states">Returned array of previous states</param>
        /// <param name="phases">Returned array of previous phases</param>
        /// <param name="dateTime">Returned array of date / time of change</param>
        /// <returns>Arrays + return value -1 if error, number of changes (index range) if ok</returns>
        public int GetUnitStateHistory(string serialNumber, string partNumber, out string[] states, out string[] phases, out DateTime[] dateTime)
            => _instance.GetUnitStateHistory(serialNumber, partNumber, out states, out phases, out dateTime);

        /// <summary>
        /// Returns list of unit history in order of newest to latest.
        /// </summary>
        /// <param name="serialNumber">Unit serial number</param>
        /// <param name="partNumber">Unit part number</param>
        /// <param name="details">If <c>true</c>, includes details (info and error messages) for the unit.</param>
        public IEnumerable<UnitHistory> GetUnitHistory(string serialNumber, string partNumber = null, bool details = false)
            => _instance.GetUnitHistory(serialNumber, partNumber, details).Select(i => new UnitHistory(i));

        /// <summary>
        /// Create a parent/child relation between two units.
        /// </summary>
        /// <param name="ParentSerialNumber">Serial Number of parent unit.</param>
        /// <param name="SerialNumber">Serial Number of child unit.</param>
        /// <returns>Value indicating if the action was successfull or not.</returns>
        public bool SetParent(string SerialNumber, string ParentSerialNumber)
            => _instance.SetParent(SerialNumber, ParentSerialNumber);

        /// <summary>
        /// Creates a new unit. The part number (product) and revision will be created if they don't exist.
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number.</param>
        /// <param name="PartNumber">Unit's part number.</param>
        /// <param name="Revision">Unit's revision.</param>
        /// <param name="batchNumber">Unit's batch number.</param>
        /// <returns>True if unit was created.</returns>
        public bool CreateUnit(string SerialNumber, string PartNumber, string Revision, string batchNumber)
            => _instance.CreateUnit(SerialNumber, PartNumber, Revision, batchNumber);

        /// <summary>
        /// Adds a child unit. If Neither CheckPartNumber or CheckRevision is given ProductRelations according to product manager are checked
        /// </summary>
        /// <param name="CultureCode">Culture code used to translate the <paramref name="message"/>.</param>
        /// <param name="ParentSerialNumber">Serial number of the parent unit.</param>
        /// <param name="ParentPartNumber">Part number of the parent unit.</param>
        /// <param name="ChildSerialNumber">Serial number of the child unit to add as child.</param>
        /// <param name="ChildPartNumber">Part number of the child unit to add as child.</param>
        /// <param name="CheckPartNumber">If given, will verify that <paramref name="ChildPartNumber"/> is the same as this. If null, will use Box Build in WATS to verify that the child unit is allowed to be a child of the parent unit.</param>
        /// <param name="CheckRevision">If given, will verify that <paramref name="ChildPartNumber"/> is the same as this. If null, will use Box Build in WATS to verify that the child unit is allowed to be a child of the parent unit.</param>
        /// <param name="message">Translated response message from WATS.</param>
        public bool AddChildUnit(string CultureCode, string ParentSerialNumber, string ParentPartNumber, string ChildSerialNumber, string ChildPartNumber, string CheckPartNumber, string CheckRevision, out string message)
            => _instance.AddChildUnit(CultureCode, ParentSerialNumber, ParentPartNumber, ChildSerialNumber, ChildPartNumber, CheckPartNumber, CheckRevision, out message);

        /// <summary>
        /// Removes a child unit of a given unit.
        /// </summary>
        /// <param name="CultureCode">Culture code used to translate the <paramref name="message"/>.</param>
        /// <param name="ParentSerialNumber">Serial number of the parent unit.</param>
        /// <param name="ParentPartNumber">Part number of the parent unit.</param>
        /// <param name="ChildSerialNumber">Serial number of the child unit to remove as child.</param>
        /// <param name="ChildPartNumber">Part number of the child unit to remove as child.</param>
        /// <param name="message">Translated response message from WATS.</param>
        public bool RemoveChildUnit(string CultureCode, string ParentSerialNumber, string ParentPartNumber, string ChildSerialNumber, string ChildPartNumber, out string message)
            => _instance.RemoveChildUnit(CultureCode, ParentSerialNumber, ParentPartNumber, ChildSerialNumber, ChildPartNumber, out message);

        /// <summary>
        /// Removes all children of a given unit.
        /// </summary>
        /// <param name="CultureCode">Culture code used to translate the <paramref name="message"/></param>
        /// <param name="ParentSerialNumber">Serial number of the parent unit to remove child units from.</param>
        /// <param name="ParentPartNumber">Part number of the parent unit to remove child units from.</param>
        /// <param name="message">Translated response message from WATS.</param>
        /// <returns></returns>
        public bool RemoveAllChildUnits(string CultureCode, string ParentSerialNumber, string ParentPartNumber, out string message)
            => _instance.RemoveAllChildUnits(CultureCode, ParentSerialNumber, ParentPartNumber, out message);

        /// <summary>
        /// Change a unit's partNumber and revision.
        /// </summary>
        /// <param name="SerialNumber">Serial number of unit to update.</param>
        /// <param name="NewPartNumber">New/updated part number.</param>
        /// <param name="NewRevision">New/updated revision.</param>
        [Obsolete("Use overload with partnumber!")]
        public bool UpdateUnit(string SerialNumber, string NewPartNumber, string NewRevision)
            => _instance.UpdateUnit(SerialNumber, NewPartNumber, NewRevision);

        /// <summary>
        /// Change a unit's partNumber and revision. <paramref name="partNumber"/> can be empty, but is required if units do not have unique serial number.
        /// </summary>
        /// <param name="serialNumber">Serial number of unit to update.</param>
        /// <param name="partNumber">Part number of unit to update. Can be empty, but is required if units do not have unique serial number.</param>
        /// <param name="newPartNumber">New/updated part number.</param>
        /// <param name="newRevision">New/updated revision.</param>
        public bool UpdateUnit(string serialNumber, string partNumber, string newPartNumber, string newRevision)
            => _instance.UpdateUnit(serialNumber, partNumber, newPartNumber, newRevision);

        /// <summary>
        /// Add or update a tag value on a unit.
        /// </summary>
        /// <param name="SerialNumber">Serial number of unit to update.</param>
        /// <param name="AttributeName">Tag key.</param>
        /// <param name="AttributeValue">Tag value.</param>
        [Obsolete("Use UpdateUnitTag with specified partnumber!")]
        public bool UpdateUnitAttribute(string SerialNumber, string AttributeName, string AttributeValue)
            => _instance.UpdateUnitAttribute(SerialNumber, AttributeName, AttributeValue);

        /// <summary>
        /// Add or update a tag value on a unit. <paramref name="partNumber"/> can be empty, but is required if units do not have unique serial number.
        /// </summary>
        /// <param name="serialNumber">Serial number of unit to update.</param>
        /// <param name="partNumber">Part number of unit to update. Can be empty, but is required if units do not have unique serial number.</param>
        /// <param name="tagName">Tag key.</param>
        /// <param name="tagValue">Tag value.</param>
        public bool UpdateUnitTag(string serialNumber, string partNumber, string tagName, string tagValue)
            => _instance.UpdateUnitTag(serialNumber, partNumber, tagName, tagValue);

        public UnitVerificationResponse GetUnitVerification(string serialNumber, string partNumber = null)
            => new UnitVerificationResponse(_instance.GetUnitVerification(serialNumber, partNumber));
    }
}
