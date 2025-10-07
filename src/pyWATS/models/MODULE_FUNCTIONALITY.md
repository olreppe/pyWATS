# MES Public Function Signatures

Summary of all public methods (functions) in the Interface.MES module, grouped by functional area (folders).
Excluded: properties, constructors where noted as none, non‑public members, internal/protected/private methods, and fields.
Obsolete methods are marked with [Obsolete]. Generic type parameters and default values included.  
Namespaces shortened to module context for readability.

---

## Root (MesInterface)

_No public methods (only accessor properties for modules)_

---

## Root (MesBase)
```
MesBase()
MesBase(string CultureCode)

void SetAdminCredentials(string userName, string password)

responseType RESTGetJson<responseType>(string query, bool useAdminCredentials = false)
responseType RESTPostJson<responseType>(string query, object obj, bool useAdminCredentials = false)
responseType RESTPutJson<responseType>(string query, object obj = null, bool useAdminCredentials = false)
responseType RESTDeleteJson<responseType>(string query, object obj = null, bool useAdminCredentials = false)

bool isConnected()

string   TranslateString(string Culture, string EnglishText, object[] arguments)
string   TranslateString(string EnglishText, object[] arguments)
string[] TranslateArray(string[] englishText)
string[] TranslateArray(string CultureCode, string[] englishText)

Process[] GetProcesses(bool IsTestOperation = true,
                       bool IsRepairOperation = false,
                       bool IsWIPOperation = false)

void GetMesServerSettings(out string[] stringValues,
                          out bool[] boolValues,
                          out int[] numberValues,
                          string[] stringKeys = null,
                          string[] boolKeys = null,
                          string[] numberKeys = null)

CommonUserSettings GetCommonUserSettings(string UserName)

string GetGeneralOptionString(string key)
bool   GetGeneralOptionBool(string key)
int    GetGeneralOptionInt(string key)

void DisplayMesTestGUI()

string GetStorageXml(string key)
string GetStorageValue(string key)
bool   PutStorageData(string key, string value, string xml)
bool   RemoveStorageData(string key)

void StartTraceToEventLog()
void StopTraceToEventLog()
```

---

## Asset
### Asset
```
string ToString()
```

### AssetHandler
```
bool isConnected()

AssetResponse CreateAsset(string serialNumber, string assetType,
                          string parentAssetSerialNumber = null,
                          string assetName = null,
                          string assetDescription = null)

AssetResponse CreateAssetType(string name,
                              decimal? calibrationInterval = null,
                              decimal? maintenanceInterval = null,
                              int? runningCountLimit = null,
                              int? totalCountLimit = null,
                              decimal? warningThreshold = null,
                              decimal? alarmTreshold = null)

AssetResponse GetAsset(string serialNumber)
AssetResponse UpdateAsset(Asset asset)
AssetResponse SetParent(string serialNumber, string parentSerialNumber)
AssetResponse IncrementAssetUsageCount(string serialNumber,
                                       int usageCount = 1,
                                       bool incrementSubAssets = false)
AssetResponse GetAssets(string filter)
AssetResponse GetAssetsByTag(string tag)
AssetResponse GetSubAssets(string serialNumber)
AssetResponse GetSubAssets(string serialNumber, int level)
AssetResponse Calibration(string serialNumber,
                          DateTime? dateTime = null,
                          string comment = null)
AssetResponse Calibration(string serialNumber, DateTime dateTime, string comment)
AssetResponse Maintenance(string serialNumber,
                          DateTime? dateTime = null,
                          string comment = null)
AssetResponse Maintenance(string serialNumber, DateTime dateTime, string comment)
AssetResponse ResetRunningCount(string serialNumber, string comment = null)
AssetResponse DeleteAsset(string serialNumber)
```

---

## Product
### Product
```
bool   isConnected()
static object DeserializeFromStream(System.IO.Stream stream)
ProductInfo GetProductInfo(string partNumber, string revision = "")
void IdentifyProduct(string Filter, int TopCount, bool FreePartnumber,
                     bool IncludeRevision, bool IncludeSerialNumber,
                     out string SelectedSerialNumber,
                     out string SelectedPartNumber,
                     out string SelectedRevision,
                     out Process SelectedTestOperation,
                     out bool Continue,
                     string CustomText = "", bool AlwaysOnTop = true)
Virinco.WATS.Service.MES.Contract.Product[] GetProduct(string filter,
                                                       int topCount,
                                                       bool includeNonSerial,
                                                       bool includeRevision)
```

### ProductInfo
```
bool        HasParent()
ProductInfo GetParent()
int         GetChildCount()
ProductInfo GetChild(int index)
ProductInfo[] GetChildren()

string GetTagValue(string Tag, int Type)
string GetInfo(string XPath)
```

---

## Production
### Production
```
Production()
Production(string CultureCode)

bool isConnected()

UnitInfo GetUnitInfo(string SerialNumber, string PartNumber = "")

UnitInfo IdentifyUUT(out bool Continue, string PartNumber = "")
UnitInfo IdentifyUUT(out bool Continue,
                     ref Process SelectedTestOperation,
                     string SerialNumber = "",
                     string PartNumber = "",
                     bool IncludeTestOperation = false,
                     bool SelectTestOperation = true,
                     string CustomText = null,
                     bool AlwaysOnTop = true,
                     bool UseWorkflow = false,
                     StatusEnum WorkflowStatus = StatusEnum.Released,
                     System.Collections.Generic.Dictionary<string, object> context = null)

void       SetUnitProcess(string SerialNumber, string PartNumber, string ProcessName)
void       SetUnitPhase(string SerialNumber, string PartNumber, Unit_Phase Phase)
void       SetUnitPhase(string SerialNumber, string PartNumber, string Phase)
string     GetUnitProcess(string SerialNumber, string PartNumber)
Unit_Phase GetUnitPhase(string SerialNumber, string PartNumber)
string     GetUnitPhaseString(string SerialNumber, string PartNumber)

int GetUnitStateHistory(string serialNumber, string partNumber,
                        out string[] states,
                        out string[] phases,
                        out DateTime[] dateTime)

System.Collections.Generic.List<UnitHistory> GetUnitHistory(string serialNumber,
                                                            string partNumber = null,
                                                            bool details = false)

bool SetParent(string SerialNumber, string ParentSerialNumber)
bool CreateUnit(string SerialNumber, string PartNumber, string Revision, string batchNumber)

bool AddChildUnit(string CultureCode,
                  string ParentSerialNumber,
                  string ParentPartNumber,
                  string ChildSerialNumber,
                  string ChildPartNumber,
                  string CheckPartNumber,
                  string CheckRevision,
                  out string message)

bool RemoveChildUnit(string CultureCode,
                     string ParentSerialNumber,
                     string ParentPartNumber,
                     string ChildSerialNumber,
                     string ChildPartNumber,
                     out string message)

bool RemoveAllChildUnits(string CultureCode,
                         string ParentSerialNumber,
                         string ParentPartNumber,
                         out string message)

[Obsolete] bool UpdateUnit(string SerialNumber, string NewPartNumber, string NewRevision)
bool UpdateUnit(string serialNumber,
                string partNumber,
                string newPartNumber,
                string newRevision)

[Obsolete] bool UpdateUnitAttribute(string SerialNumber,
                                    string AttributeName,
                                    string AttributeValue)

bool UpdateUnitTag(string serialNumber,
                   string partNumber,
                   string tagName,
                   string tagValue)

UnitVerificationResponse GetUnitVerification(string serialNumber,
                                             string partNumber = null)
```

### SerialNumberHandler
```
SerialNumberHandler(string serialNumberTypeName)

static System.Collections.Generic.IEnumerable<SerialNumberType> GetSerialNumberTypes()
System.Collections.Generic.IEnumerable<SerialNumbersSN> GetLocalSerialNumbers()

string FormatAsMAC(long i, char separator)

System.Collections.Generic.List<string> GenerateAndUploadSerialNumbers(string tokenID,
                                string serviceUrl,
                                long fromSN,
                                long toSN,
                                char separator,
                                out int uploaded,
                                out int rejected,
                                Guid token)

System.Collections.Generic.List<string> UploadSerialNumbersFromFile(string tokenID,
                                string serviceUrl,
                                string fileName,
                                out int uploaded,
                                out int rejected,
                                Guid token)

void Initialize(string tokenID,
                string serviceUrl,
                SerialNumberHandler.RequestType requestType,
                bool onlyInSequence,
                int batchSize,
                int fetchWhenLessThan,
                string startFromSerialNumber,
                string siteName,
                Guid token = new Guid())

void SetReuseOnDuplicateRequest(bool on)
bool GetResuseOnDuplicateRequest()
void CancelReservations(Guid token = new Guid())

SerialNumberHandler.Status GetStatus()
int  GetFreeLocalSerialNumbers()

void GetPoolInfo(out bool onlyInSequence,
                 out int batchSize,
                 out int fetchWhenLessThan,
                 out string startFromSerialNumber,
                 out string siteName)

void GetPoolInfo(out bool onlyInSequence,
                 out int batchSize,
                 out int fetchWhenLessThan,
                 out string startFromSerialNumber,
                 out string siteName,
                 out SerialNumberHandler.RequestType requestType)

string[] GetSerialNumbers(int numToGet, string serialnumberRef, string partnumberRef)
string   GetSerialNumber(string serialnumberRef, string partnumberRef)
string[] GetTakenSerialNumbers(string serialnumberRef, string partnumberRef)

long MACToInt(string mac)

static void CancelAllReservations()
```

### UnitInfo
```
[Obsolete] string GetInfoByField(string Field, UnitInfo.DataType Type)
string       GetTagValue(string Tag, UnitInfo.DataType Type)
[Obsolete] string GetInfoByField(string Field, int Type)
string       GetTagValue(string Tag, int Type)
bool         SetTagValue(string Tag, string TagValue)
string       GetInfo(string XPath, UnitInfo.DataType type)
string       GetInfo(string XPath, int type)

bool       HasParent()
int        GetChildCount()
UnitInfo   GetParent()
UnitInfo   GetChild(int index)
UnitInfo[] GetChildren()
```

---

## Software
### Software
```
bool isConnected()

Package[] GetRevokedPackages(string[] tagNames,
                             string[] tagValues,
                             out Package SelectedPackage,
                             out bool Continue,
                             out System.Collections.Generic.List<System.IO.FileInfo> ExecuteFiles,
                             out System.Collections.Generic.List<System.IO.FileInfo> TopLevelSequences)

Package[] GetPackages(string PartNumber = null,
                      string Process = null,
                      string StationType = null,
                      string Revision = null,
                      string StationName = null,
                      string Misc = null,
                      bool Install = true,
                      bool DisplayProgress = true,
                      bool WaitForExecution = true,
                      StatusEnum PackageStatus = StatusEnum.Released)

Package[] GetPackagesByTag(string XPath,
                           out System.Collections.Generic.List<System.IO.FileInfo> ExecuteFiles,
                           out System.Collections.Generic.List<System.IO.FileInfo> TopLevelSequences,
                           bool Install = true,
                           bool DisplayProgress = true,
                           bool WaitForExecution = true,
                           StatusEnum PackageStatus = StatusEnum.Released)

Package[] GetPackagesByTag(string XPath,
                           bool Install = true,
                           bool DisplayProgress = true,
                           bool WaitForExecution = true,
                           StatusEnum PackageStatus = StatusEnum.Released)

Package[] GetPackagesByTag(System.Collections.Generic.Dictionary<string,string> TagValue,
                           bool Install,
                           bool DisplayProgress,
                           bool WaitForExecution,
                           StatusEnum PackageStatus = StatusEnum.Released)

Package[] GetPackagesByTag(string[] tagNames,
                           string[] tagValues,
                           bool Install,
                           bool DisplayProgress,
                           bool WaitForExecution,
                           out System.Collections.Generic.List<System.IO.FileInfo> ExecuteFiles,
                           out System.Collections.Generic.List<System.IO.FileInfo> TopLevelSequences,
                           StatusEnum PackageStatus = StatusEnum.Released)

Package[] GetPackagesByTag(System.Collections.Generic.Dictionary<string,string> TagValue,
                           bool Install,
                           bool DisplayProgress,
                           bool WaitForExecution,
                           out System.Collections.Generic.List<System.IO.FileInfo> ExecuteFiles,
                           out System.Collections.Generic.List<System.IO.FileInfo> TopLevelSequences,
                           StatusEnum PackageStatus = StatusEnum.Released)

Package GetPackageByName(string PackageName,
                         bool Install,
                         bool DisplayProgress,
                         bool WaitForExecution,
                         out System.Collections.Generic.List<System.IO.FileInfo> ExecuteFiles,
                         out System.Collections.Generic.List<System.IO.FileInfo> TopLevelSequences,
                         StatusEnum PackageStatus = StatusEnum.Released)

Package GetPackageByName(string PackageName,
                         bool Install = true,
                         bool DisplayProgress = true,
                         bool WaitForExecution = true,
                         StatusEnum PackageStatus = StatusEnum.Released)

void InstallPackage(Package[] packages,
                    bool DisplayProgress,
                    bool WaitForExecution,
                    out System.Collections.Generic.List<System.IO.FileInfo> ExecuteFiles,
                    out System.Collections.Generic.List<System.IO.FileInfo> TopLevelSequences)

void InstallPackage(Package[] packages, bool DisplayProgress, bool WaitForExecution)

void InstallPackage(Package package,
                    bool DisplayProgress,
                    bool WaitForExecution,
                    out System.Collections.Generic.List<System.IO.FileInfo> ExecuteFiles,
                    out System.Collections.Generic.List<System.IO.FileInfo> TopLevelSequences)

void InstallPackage(Package package, bool DisplayProgress, bool WaitForExecution)

static void   SetRootFolderPath(string rootFolderPath, bool moveExistingPackages = true)
static string GetRootFolderPath()

void DeleteAllPackages(bool PromptOperator = true)
void DeleteRevokedPackages(bool PromptOperator = true)

Package[] GetAvailablePackages(out bool PackagesAvailable)
```

---

## Workflow
### Workflow
```
bool isConnected()

WorkflowResponse StartTest(string SerialNumber,
                           string PartNumber,
                           string Operation,
                           System.Collections.Generic.Dictionary<string, object> inputValues,
                           bool promptOperator = false,
                           bool AlwaysOnTop = true,
                           StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse EndTest(string SerialNumber,
                         string PartNumber,
                         string Operation,
                         ActivityTestResult Result,
                         bool ForceExit,
                         System.Collections.Generic.Dictionary<string, object> inputValues,
                         bool promptOperator = false,
                         bool AlwaysOnTop = true,
                         StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse Validate(string SerialNumber,
                          string PartNumber,
                          ActivityMethod Method,
                          string Name,
                          System.Collections.Generic.Dictionary<string, object> inputValues,
                          StatusEnum workflowDefinitionStatus = StatusEnum.Released,
                          bool generateImage = false)

WorkflowResponse Initialize(string SerialNumber,
                            string PartNumber,
                            System.Collections.Generic.Dictionary<string, object> inputValues,
                            bool promptOperator = false,
                            bool AlwaysOnTop = true,
                            StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse CheckIn(string SerialNumber,
                         string PartNumber,
                         string Operation,
                         System.Collections.Generic.Dictionary<string, object> inputValues,
                         bool promptOperator = false,
                         bool AlwaysOnTop = true,
                         StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse CheckOut(string SerialNumber,
                          string PartNumber,
                          string Operation,
                          System.Collections.Generic.Dictionary<string, object> inputValues,
                          bool promptOperator = false,
                          bool AlwaysOnTop = true,
                          StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse UserInput(string SerialNumber,
                           string PartNumber,
                           string Operation,
                           string UserInput,
                           System.Collections.Generic.Dictionary<string, object> inputValues,
                           bool promptOperator = false,
                           bool AlwaysOnTop = true,
                           StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse StartRepair(string SerialNumber,
                             string PartNumber,
                             string Operation,
                             string UserInput,
                             System.Collections.Generic.Dictionary<string, object> inputValues,
                             bool promptOperator = false,
                             bool AlwaysOnTop = true,
                             StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse EndRepair(string SerialNumber,
                           string PartNumber,
                           string Operation,
                           string UserInput,
                           System.Collections.Generic.Dictionary<string, object> inputValues,
                           bool promptOperator = false,
                           bool AlwaysOnTop = true,
                           StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse Scrap(string SerialNumber,
                       string PartNumber,
                       string Operation,
                       string UserInput,
                       System.Collections.Generic.Dictionary<string, object> inputValues,
                       bool promptOperator = false,
                       bool AlwaysOnTop = true,
                       StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse Suspend(string SerialNumber,
                         string PartNumber,
                         StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse Resume(string SerialNumber,
                        string PartNumber,
                        StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse Cancel(string Serial Number,
                        string PartNumber,
                        StatusEnum workflowDefinitionStatus = StatusEnum.Released)

WorkflowResponse AddUnit(string SerialNumber,
                         string PartNumber,
                         string ChildSerialNumber,
                         string ChildPartNumber,
                         string ActivityName,
                         System.Collections.Generic.Dictionary<string, object> inputValues,
                         StatusEnum workflowDefinitionStatus)

WorkflowResponse RemoveUnit(string SerialNumber,
                            string PartNumber,
                            string ChildSerialNumber,
                            string ChildPartNumber,
                            string ActivityName,
                            System.Collections.Generic.Dictionary<string, object> inputValues,
                            StatusEnum workflowDefinitionStatus)
```

---

Generated by GitHub Copilot.
