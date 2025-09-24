using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Virinco.WATS.Service.MES.Contract;
using System.Diagnostics;
using System.Xml;
using System.Windows.Forms;
using System.Net;
using System.IO;
using Virinco.Newtonsoft.Json;
using Virinco.WATS.REST;

namespace Virinco.WATS.Interface.MES.Production
{
    /// <summary>
    /// Class provided to handle unit info (on serialnumber/parnumber)
    /// </summary>
    public class Production : MesBase
    {
        /// <summary>
        /// Empty constructor
        /// </summary>
        public Production() : base() { }
        /// <summary>
        /// Constructor with Culture code
        /// </summary>
        /// <param name="CultureCode"></param>
        public Production(string CultureCode) : base(CultureCode) { }

        /// <summary>
        /// True if connected to server
        /// </summary>
        /// <returns></returns>
        new public bool isConnected()
        {
            return base.isConnected();
        }

        /// <summary>
        /// If <see cref="IdentifyUUT(out bool, string)"/> is called and this is set to true,
        /// the Display TreeView checkbox is checked. If the checkbox
        /// is not checked, the form will automatically close when the serialnumber
        /// ends with \r\n
        /// </summary>
        public bool DisplayTreeView = true;

        /// <summary>
        /// Holds information about the last scanned serialnumber
        /// </summary>
        public string LastScannedSerialnumber = string.Empty;

        /// <summary>
        /// Return <see cref="UnitInfo"/> object (no GUI)
        /// </summary>
        /// <param name="SerialNumber"></param>
        /// <param name="PartNumber"></param>
        /// <returns>A <see cref="UnitInfo"/> object with info about the SN supplied.</returns>
        public UnitInfo GetUnitInfo(string SerialNumber, string PartNumber = "")
        {
            LastScannedSerialnumber = SerialNumber;
            if (isConnected())
            {
                try
                {
                    List<GetUnitInfo_Result> uirl = serviceProxy.GetJson<List<GetUnitInfo_Result>>($"api/internal/Production/GetUnitInfo?serialNumber={SerialNumber}&partNumber={PartNumber}");
                    if (uirl != null && uirl.Count > 0)
                    {
                        GetUnitInfo_Result uir = uirl[0]; //Unit that is searched is returned as #1 (Requires WATS Version 4.2)
                        UnitInfo ui = new UnitInfo(uir, uirl, this);
                        return ui;
                    }
                }
                catch (Exception e) { Env.LogException(e, "GetUnitInfo"); }
            }
            return null;
        }


        /// <summary>
        /// Displays SN textbox if connected to service
        /// </summary>
        /// <returns>A <see cref="UnitInfo"/> object of the scanned unit.</returns>
        /// <param name="Continue">Boolean value indicating if the process was stopped</param>        
        /// <param name="PartNumber">PartNumber of unit to identify (used in case of none unique serialnumbers)</param>
        public UnitInfo IdentifyUUT(out bool Continue, string PartNumber = "")
        {
            Virinco.WATS.Service.MES.Contract.Process p = null;
            return IdentifyUUT(out Continue, ref p, "", PartNumber);
        }


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
        public UnitInfo IdentifyUUT(out bool Continue, ref Virinco.WATS.Service.MES.Contract.Process SelectedTestOperation, string SerialNumber = "", string PartNumber = "", bool IncludeTestOperation = false, bool SelectTestOperation = true, string CustomText = null, bool AlwaysOnTop = true, bool UseWorkflow = false, StatusEnum WorkflowStatus = StatusEnum.Released, Dictionary<string, object> context = null)
        {
            //SelectedTestOperation = null;
            Continue = false;
            try
            {
                //Trace.WriteLine("IdentifyUUT start");
                if (isConnected())
                {
                    using (IdentifyConnected form = new IdentifyConnected(this, DisplayTreeView, SerialNumber, PartNumber, SelectedTestOperation, IncludeTestOperation, SelectTestOperation, CustomText, AlwaysOnTop, UseWorkflow, WorkflowStatus, context))
                    {
                        if (form.ShowDialog() == DialogResult.OK)
                        {
                            DisplayTreeView = form.DisplayTreeView;
                            Continue = form.Continue;
                            SelectedTestOperation = form.TestOperation;
                            return form.UnitInfo;
                        }
                    }
                }
            }
            catch (Exception e) { Env.LogException(e, ""); }
            //Trace.WriteLine("IdentifyUUT returns null");
            return null;
        }

        /// <summary>
        /// Sets a unit's process to a given value
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <param name="ProcessName">Unit's new processname</param>        
        public void SetUnitProcess(string SerialNumber, string PartNumber, string ProcessName)
        {
            try
            {
                if (isConnected())
                {
                    serviceProxy.GetJson<dynamic>($"api/internal/Production/SetUnitProcess?serialNumber={SerialNumber}&partNumber={PartNumber}&processName={ProcessName}");
                }
            }
            catch (Exception e) { Env.LogException(e, "SetUnitState"); }
        }

        /// <summary>
        /// Sets a unit's phase.
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <param name="Phase">Unit's new phase,</param>
        public void SetUnitPhase(string SerialNumber, string PartNumber, Unit_Phase Phase)
        {
            try
            {
                if (isConnected())
                {
                    serviceProxy.GetJson<dynamic>($"api/internal/Production/SetUnitPhase?serialNumber={SerialNumber}&partNumber={PartNumber}&phase={(short)Phase}");
                }
            }
            catch (Exception e) { Env.LogException(e, "SetUnitPhase"); }
        }

        /// <summary>
        /// Sets a unit's phase.
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <param name="Phase">Unit's new phase,</param>
        public void SetUnitPhase(string SerialNumber, string PartNumber, string Phase)
        {
            try
            {
                if (isConnected())
                {
                    if (Enum.IsDefined(typeof(Unit_Phase), Phase))
                    {
                        Unit_Phase up = (Unit_Phase)Enum.Parse(typeof(Unit_Phase), Phase);
                        serviceProxy.GetJson<dynamic>($"api/internal/Production/SetUnitPhase?serialNumber={SerialNumber}&partNumber={PartNumber}&phase={(short)up}");
                    }
                    else
                    {
                        throw new Exception(Phase + " is not a valid Unit_phase enum");
                    }
                }
            }
            catch (Exception e) { Env.LogException(e, "SetUnitPhase"); }
        }

        /// <summary>
        /// Get a unit's current process
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>
        /// <returns>Unit's current process</returns>
        public string GetUnitProcess(string SerialNumber, string PartNumber)
        {
            try
            {
                if (isConnected())
                {
                    return serviceProxy.GetJson<string>($"api/internal/Production/GetUnitProcess?serialNumber={SerialNumber}&partNumber={PartNumber}");
                }
            }
            catch (Exception e) { Env.LogException(e, "GetUnitState"); }
            return string.Empty;
        }

        /// <summary>
        /// Get a unit's phase.         
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>        
        /// <returns>Units current Phase enum</returns>
        public Unit_Phase GetUnitPhase(string SerialNumber, string PartNumber)
        {
            try
            {
                if (isConnected())
                {
                    return (Unit_Phase)serviceProxy.GetJson<short>($"api/internal/Production/GetUnitPhase?serialNumber={SerialNumber}&partNumber={PartNumber}");
                }
            }
            catch (Exception e) { Env.LogException(e, "GetUnitPhase"); }
            return Unit_Phase.Unknown;
        }

        /// <summary>
        /// Get a unit's phase.         
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number</param>
        /// <param name="PartNumber">Unit's part number</param>       
        /// <returns>Units current Phase as string</returns>
        public string GetUnitPhaseString(string SerialNumber, string PartNumber)
        {
            try
            {
                if (isConnected())
                {
                    return ((Unit_Phase)serviceProxy.GetJson<short>($"api/internal/Production/GetUnitPhase?serialNumber={SerialNumber}&partNumber={PartNumber}")).ToString();
                }
            }
            catch (Exception e) { Env.LogException(e, "GetUnitPhase"); }
            return Unit_Phase.Unknown.ToString();
        }

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
        {
            states = null;
            phases = null;
            dateTime = null;
            try
            {
                if (isConnected())
                {
                    var res = serviceProxy.GetJson<UnitStateHistory>($"api/internal/Production/GetUnitStateHistory?serialNumber={serialNumber}&partNumber={partNumber}");

                    states = res.processes;
                    phases = res.phases;
                    dateTime = res.dateTimes;

                    return states.Length;
                }
            }
            catch (Exception e) { Env.LogException(e, "GetUnitStateHistory"); }
            return -1;
        }

        /// <summary>
        /// Returns list of unit history in order of newest to latest.
        /// </summary>
        /// <param name="serialNumber">Unit serial number</param>
        /// <param name="partNumber">Unit part number</param>
        /// <param name="details">If <c>true</c>, includes details (info and error messages) for the unit.</param>
        public List<UnitHistory> GetUnitHistory(string serialNumber, string partNumber = null, bool details = false)
        {
            var filter = new PublicWatsFilter
            {
                serialNumber = serialNumber,
                partNumber = partNumber ?? ""
            };

            return serviceProxy.PostJson<List<UnitHistory>>("api/internal/Survey/GetUnitReportHistory" + (details ? "?details=true" : ""), filter);           
        }       

        /// <summary>
        /// Create a parent/child relation between two units.
        /// </summary>
        /// <param name="ParentSerialNumber">Serial Number of parent unit.</param>
        /// <param name="SerialNumber">Serial Number of child unit.</param>
        /// <returns>Value indicating if the action was successfull or not.</returns>
        public bool SetParent(string SerialNumber, string ParentSerialNumber)
        {
            try
            {
                if (isConnected())
                {
                    return serviceProxy.PostJson<bool>($"api/internal/Production/SetParent?serialNumber={SerialNumber}&partNumber=&parentSerialNumber={ParentSerialNumber}&parentPartNumber=", SerialNumber);
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, "SetParent"); 
            }

            return false;
        }

        /// <summary>
        /// Creates a new unit. The part number (product) and revision will be created if they don't exist.
        /// </summary>
        /// <param name="SerialNumber">Unit's serial number.</param>
        /// <param name="PartNumber">Unit's part number.</param>
        /// <param name="Revision">Unit's revision.</param>
        /// <param name="batchNumber">Unit's batch number.</param>
        /// <returns>True if unit was created.</returns>
        public bool CreateUnit(string SerialNumber, string PartNumber, string Revision, string batchNumber)
        {
            try
            {
                Unit u = null;
                if (isConnected())
                {
                    u = serviceProxy.PostJson<Unit>($"api/internal/Production/CreateUnit?serialNumber={SerialNumber}&partNumber={PartNumber}&revision={Revision}&batchNumber={batchNumber}", SerialNumber);
                }
                return u != null;
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, "CreateUnit"); 
            }

            return false;
        }

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
        {
            message = "";
            try
            {
                if (isConnected())
                {
                    HttpWebResponse resp = (HttpWebResponse)serviceProxy.CreateHttpWebRequest("POST", $"api/internal/Production/AddChildUnit?serialNumber={ParentSerialNumber}&partNumber={ParentPartNumber}&childSerialNumber={ChildSerialNumber}&childPartNumber={ChildPartNumber}&checkPartNumber={CheckPartNumber}&checkRevision={CheckRevision}&cultureCode={CultureCode}", 10000, "application/json", "application/json", 0).GetResponseWithoutException();
                    using (var sr = new StreamReader(resp.GetResponseStream()))
                        message = sr.ReadToEnd();
                    var ret = (resp.StatusCode == HttpStatusCode.OK);
                    resp.Close();
                    return ret;
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, "AddChildUnit"); 
            }

            return false;
        }


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
        {
            message = "";
            try
            {
                if (isConnected())
                {
                    HttpWebResponse resp = (HttpWebResponse)serviceProxy.CreateHttpWebRequest("POST", $"api/internal/Production/RemoveChildUnit?serialNumber={ParentSerialNumber}&partNumber={ParentPartNumber}&childSerialNumber={ChildSerialNumber}&childPartNumber={ChildPartNumber}&cultureCode={CultureCode}", 10000, "application/json", "application/json", 0).GetResponseWithoutException();
                    using (var sr = new StreamReader(resp.GetResponseStream()))
                        message = sr.ReadToEnd();
                    var ret = (resp.StatusCode == HttpStatusCode.OK);
                    resp.Close();
                    return ret;
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, "RemoveChildUnit"); 
            }

            return false;
        }


        /// <summary>
        /// Removes all children of a given unit.
        /// </summary>
        /// <param name="CultureCode">Culture code used to translate the <paramref name="message"/></param>
        /// <param name="ParentSerialNumber">Serial number of the parent unit to remove child units from.</param>
        /// <param name="ParentPartNumber">Part number of the parent unit to remove child units from.</param>
        /// <param name="message">Translated response message from WATS.</param>
        /// <returns></returns>
        public bool RemoveAllChildUnits(string CultureCode, string ParentSerialNumber, string ParentPartNumber, out string message)
        {
            message = "";
            try
            {
                if (isConnected())
                {
                    HttpWebResponse resp = (HttpWebResponse)serviceProxy.CreateHttpWebRequest("POST", $"api/internal/Production/RemoveAllChildUnits?serialNumber={ParentSerialNumber}&partNumber={ParentPartNumber}&cultureCode={CultureCode}", 10000, "application/json", "application/json", 0).GetResponseWithoutException();
                    using (var sr = new StreamReader(resp.GetResponseStream()))
                        message = sr.ReadToEnd();
                    var ret = (resp.StatusCode == HttpStatusCode.OK);
                    resp.Close();
                    return ret;
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, nameof(RemoveAllChildUnits)); 
            }

            return false;
        }


        /// <summary>
        /// Change a unit's partNumber and revision.
        /// </summary>
        /// <param name="SerialNumber">Serial number of unit to update.</param>
        /// <param name="NewPartNumber">New/updated part number.</param>
        /// <param name="NewRevision">New/updated revision.</param>
        [Obsolete]
        public bool UpdateUnit(string SerialNumber, string NewPartNumber, string NewRevision)
        {
            try
            {
                if (isConnected())
                {
                    return serviceProxy.PostJson<bool>($"api/internal/Production/UpdateUnit?serialNumber={SerialNumber}&partNumber=&newPartNumber={NewPartNumber}&newRevision={NewRevision}", SerialNumber);
                }
            }
            catch (Exception ex) { Env.LogException(ex, nameof(UpdateUnit) + " (obsolete)"); }
            return false;
        }

        /// <summary>
        /// Change a unit's partNumber and revision. <paramref name="partNumber"/> can be empty, but is required if units do not have unique serial number.
        /// </summary>
        /// <param name="serialNumber">Serial number of unit to update.</param>
        /// <param name="partNumber">Part number of unit to update. Can be empty, but is required if units do not have unique serial number.</param>
        /// <param name="newPartNumber">New/updated part number.</param>
        /// <param name="newRevision">New/updated revision.</param>
        public bool UpdateUnit(string serialNumber, string partNumber, string newPartNumber, string newRevision)
        {
            try
            {
                if (isConnected())
                {
                    return serviceProxy.PostJson<bool>($"api/internal/Production/UpdateUnit?serialNumber={serialNumber}&partNumber={partNumber}&newPartNumber={newPartNumber}&newRevision={newRevision}", serialNumber);
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, nameof(UpdateUnit)); 
            }
            return false;
        }

        /// <summary>
        /// Add or update a tag value on a unit.
        /// </summary>
        /// <param name="SerialNumber">Serial number of unit to update.</param>
        /// <param name="AttributeName">Tag key.</param>
        /// <param name="AttributeValue">Tag value.</param>
        [Obsolete]
        public bool UpdateUnitAttribute(string SerialNumber, string AttributeName, string AttributeValue)
        {
            try
            {
                if (isConnected())
                {
                    return serviceProxy.PostJson<bool>($"api/internal/Production/UpdateUnitAttribute?serialNumber={SerialNumber}&partNumber=&attributeName={AttributeName}&attributeValue={AttributeValue}", SerialNumber);
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, nameof(UpdateUnitAttribute)); 
            }
            
            return false; 
        }

        /// <summary>
        /// Add or update a tag value on a unit. <paramref name="partNumber"/> can be empty, but is required if units do not have unique serial number.
        /// </summary>
        /// <param name="serialNumber">Serial number of unit to update.</param>
        /// <param name="partNumber">Part number of unit to update. Can be empty, but is required if units do not have unique serial number.</param>
        /// <param name="tagName">Tag key.</param>
        /// <param name="tagValue">Tag value.</param>
        public bool UpdateUnitTag(string serialNumber, string partNumber, string tagName, string tagValue)
        {
            try
            {
                if (isConnected())
                {
                    return serviceProxy.PostJson<bool>($"api/internal/Production/UpdateUnitAttribute?serialNumber={serialNumber}&partNumber={partNumber}&attributeName={tagName}&attributeValue={tagValue}", serialNumber);
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, nameof(UpdateUnitTag)); 
            }

            return false;
        }

        public UnitVerificationResponse GetUnitVerification(string serialNumber, string partNumber = null)
        {
            try
            {
                if (isConnected())
                {
                    return serviceProxy.GetJson<UnitVerificationResponse>($"api/Production/UnitVerification?serialNumber={serialNumber}&partNumber={partNumber}");
                }
            }
            catch (Exception ex) 
            { 
                Env.LogException(ex, nameof(GetUnitVerification));
            }

            return null;
        }
    }
}
