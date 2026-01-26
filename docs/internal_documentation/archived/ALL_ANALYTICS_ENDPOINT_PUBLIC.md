post /api/App/OeeAnalysis
Overall Equipment Effectiveness - analysis

Supported filters: productGroup, level, partNumber, revision, stationName, testOperation, status, swFilename, swVersion, socket, dateFrom, dateTo

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filter	
(required)

Parameter content type: 
application/json
WATS filter

body	
ModelExample Value
{
  "serialNumber": "string",
  "partNumber": "string",
  "revision": "string",
  "batchNumber": "string",
  "stationName": "string",
  "testOperation": "string",
  "status": "string",
  "yield": 0,
  "miscDescription": "string",
  "miscValue": "string",
  "productGroup": "string",
  "level": "string",
  "swFilename": "string",
  "swVersion": "string",
  "socket": "string",
  "dateFrom": "2025-12-21T13:43:14.773Z",
  "dateTo": "2025-12-21T13:43:14.773Z",
  "dateGrouping": 0,
  "periodCount": 0,
  "includeCurrentPeriod": true,
  "maxCount": 0,
  "minCount": 0,
  "topCount": 0,
  "dimensions": "string"
}
availableTime	
(required)
Available hours by weekday. Ex. 24,24,24,24,24,24,24

query	string
minConnectionTime	
Minimum connection time filter

query	integer
maxConnectionTime	
Maximum connection time filter

query	integer
minExecutionTime	
Minimum execution time filter

query	integer
maxExecutionTime	
Maximum execution time filter

query	integer
targetOutput	
Target output per day

query	integer
get /api/App/Processes
Get processes.

Implementation Notes
Non-filtered requests retrieves active processes marked as isTestOperation, isRepairOperation or isWipOperation.

RepairOperation details:

uutBinding: 0 = required, 1 = optional, 2 = never

bomBinding: 0 = required, 1 = optional, 2 = never

vendorBinding: 0 = required, 1 = optional, 2 = never

imageConstraint: 0 = required, 1 = optional, 2 = never

repairType: Default = 0, AutomaticProcess = 1, Scrapped = 2, NoFailureFound = 3, Component = 4, Design = 5, ManualProcess = 6, Replaced = 7

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
includeTestOperations	
Include processes masrked as IsTestOperation

query	boolean
includeRepairOperations	
Include processes masrked as IsTestOperation

query	boolean
includeWipOperations	
Include processes masrked as IsTestOperation

query	boolean
includeInactiveProcesses	
Include inactive processes

query	boolean
get /api/App/ProductGroups
Retrieves all ProductGroups

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
includeFilters	
Include or exclude product group filters

query	boolean
get /api/App/RelatedRepairHistory
Get list of repaired failures related to the part number and revision.

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
partNumber	
(required)
Related part number.

query	string
revision	
(required)
Related revision.

query	string
repairOperationCode	
Repair operation code filter.

query	string
testOperationCode	
Test operation code filter.

query	string
post /api/App/SerialNumberHistory
Serial Number History.

Supported filters: productGroup, level, serialNumber, partNumber, batchNumber, miscValue

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filter	
(required)

Parameter content type: 
application/json
body	
ModelExample Value
{
  "serialNumber": "string",
  "partNumber": "string",
  "revision": "string",
  "batchNumber": "string",
  "stationName": "string",
  "testOperation": "string",
  "status": "string",
  "yield": 0,
  "miscDescription": "string",
  "miscValue": "string",
  "productGroup": "string",
  "level": "string",
  "swFilename": "string",
  "swVersion": "string",
  "socket": "string",
  "dateFrom": "2025-12-21T13:43:14.781Z",
  "dateTo": "2025-12-21T13:43:14.781Z",
  "dateGrouping": 0,
  "periodCount": 0,
  "includeCurrentPeriod": true,
  "maxCount": 0,
  "minCount": 0,
  "topCount": 0,
  "dimensions": "string"
}
post /api/App/TestStepAnalysis
PREVIEW - Get step and measurement statistics.

Implementation Notes
Please note that this endpoint is in preview and may be a subject to changes.

Default filter values if not specified:

{ 
"maxCount":10000 ,
"dateFrom": "DateTime.Now - 30 days",
"run": 1 (1 = first, 2 = second, 3 = third, -1 = last run, -2 = All)
}
Note: partnumber and testOperation filter required

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filter	
(required)

Parameter content type: 
application/json
body	
ModelExample Value
{
  "serialNumber": "string",
  "partNumber": "string",
  "revision": "string",
  "batchNumber": "string",
  "stationName": "string",
  "testOperation": "string",
  "status": "string",
  "yield": 0,
  "miscDescription": "string",
  "miscValue": "string",
  "productGroup": "string",
  "level": "string",
  "swFilename": "string",
  "swVersion": "string",
  "socket": "string",
  "dateFrom": "2025-12-21T13:43:14.783Z",
  "dateTo": "2025-12-21T13:43:14.783Z",
  "dateGrouping": 0,
  "periodCount": 0,
  "includeCurrentPeriod": true,
  "maxCount": 0,
  "minCount": 0,
  "topCount": 0,
  "dimensions": "string"
}
get /api/App/TopFailed
Get the top failed steps for the reports with the specified parameters.

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
partNumber	
(required)
Part number of reports to get failed steps from.

query	string
processCode	
(required)
Process code of reports to get failed steps from.

query	string
productGroupId	
(required)
Product group of reports to get failed steps from.

query	string
levelId	
(required)
Level of reports to get failed steps from.

query	string
days	
(required)
Number of days ago reports to get failed steps from were submitted.

query	integer
count	
(required)
Number of items to return

query	integer
post /api/App/TopFailed
Get the top failed steps for the reports with the specified parameters.

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filter	
(required)

Parameter content type: 
application/json
Supported filters: partNumber, testOperation, yield, productGroup, level, periodCount, grouping, includeCurrentPeriod, topCount

body	
ModelExample Value
{
  "serialNumber": "string",
  "partNumber": "string",
  "revision": "string",
  "batchNumber": "string",
  "stationName": "string",
  "testOperation": "string",
  "status": "string",
  "yield": 0,
  "miscDescription": "string",
  "miscValue": "string",
  "productGroup": "string",
  "level": "string",
  "swFilename": "string",
  "swVersion": "string",
  "socket": "string",
  "dateFrom": "2025-12-21T13:43:14.787Z",
  "dateTo": "2025-12-21T13:43:14.787Z",
  "dateGrouping": 0,
  "periodCount": 0,
  "includeCurrentPeriod": true,
  "maxCount": 0,
  "minCount": 0,
  "topCount": 0,
  "dimensions": "string"
}


/api/App/Version
Get server/api version

Response Class (Status 200)
string


Response Content Type 
application/json
get /api/App/VolumeYield
Volume/Yield list filtered by productGroup and level

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
days	
(required)
number of days to include

query	integer
productGroupId	
(required)
productGroup filter (split multiple groups with ;)

query	string
levelId	
(required)
level filter (split multiple groups with ;)

query	string
post /api/App/VolumeYield
Volume/Yield list filtered by productGroup and level

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filter	
(required)

Parameter content type: 
application/json
Supported filters: productGroup, level, periodCount, grouping, includeCurrentPeriod

body	
ModelExample Value
{
  "serialNumber": "string",
  "partNumber": "string",
  "revision": "string",
  "batchNumber": "string",
  "stationName": "string",
  "testOperation": "string",
  "status": "string",
  "yield": 0,
  "miscDescription": "string",
  "miscValue": "string",
  "productGroup": "string",
  "level": "string",
  "swFilename": "string",
  "swVersion": "string",
  "socket": "string",
  "dateFrom": "2025-12-21T13:43:14.799Z",
  "dateTo": "2025-12-21T13:43:14.799Z",
  "dateGrouping": 0,
  "periodCount": 0,
  "includeCurrentPeriod": true,
  "maxCount": 0,
  "minCount": 0,
  "topCount": 0,
  "dimensions": "string"
}
get /api/App/WorstYield
Worst Yield list filtered by productGroup and level

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
days	
(required)
number of days to include

query	integer
productGroupId	
(required)
productGroup filter (split multiple groups with ;)

query	string
levelId	
(required)
level filter (split multiple groups with ;)

query	string
post /api/App/WorstYield
Yield sorted by lowest yield.

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filter	
(required)

Parameter content type: 
application/json
Supported filters: productGroup, level, periodCount, grouping, includeCurrentPeriod, topCount, minCount.

body	
ModelExample Value
{
  "serialNumber": "string",
  "partNumber": "string",
  "revision": "string",
  "batchNumber": "string",
  "stationName": "string",
  "testOperation": "string",
  "status": "string",
  "yield": 0,
  "miscDescription": "string",
  "miscValue": "string",
  "productGroup": "string",
  "level": "string",
  "swFilename": "string",
  "swVersion": "string",
  "socket": "string",
  "dateFrom": "2025-12-21T13:43:14.802Z",
  "dateTo": "2025-12-21T13:43:14.802Z",
  "dateGrouping": 0,
  "periodCount": 0,
  "includeCurrentPeriod": true,
  "maxCount": 0,
  "minCount": 0,
  "topCount": 0,
  "dimensions": "string"
}
post /api/App/WorstYieldByProductGroup
Yield by product group sorted by lowest yield.

Response Class (Status 200)
OK

ModelExample Value
{}


Response Content Type 
application/json
Parameters
Parameter	Value	Description	Parameter Type	Data Type
filter	
(required)

Parameter content type: 
application/json
Supported filters: productGroup, level, periodCount, grouping, includeCurrentPeriod, topCount, minCount.

body	
ModelExample Value
{
  "serialNumber": "string",
  "partNumber": "string",
  "revision": "string",
  "batchNumber": "string",
  "stationName": "string",
  "testOperation": "string",
  "status": "string",
  "yield": 0,
  "miscDescription": "string",
  "miscValue": "string",
  "productGroup": "string",
  "level": "string",
  "swFilename": "string",
  "swVersion": "string",
  "socket": "string",
  "dateFrom": "2025-12-21T13:43:14.804Z",
  "dateTo": "2025-12-21T13:43:14.804Z",
  "dateGrouping": 0,
  "periodCount": 0,
  "includeCurrentPeriod": true,
  "maxCount": 0,
  "minCount": 0,
  "topCount": 0,
  "dimensions": "string"
}
