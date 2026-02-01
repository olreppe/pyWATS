In the latest WATS server release additional functionality has been added to the asset module.

Here are the release notes:
(Not all applies as much of this relates to the server and web app, but the new asset functionality and backend needs to be updated.)
------------------------------------------------------------------------------
Dec 2025
WATS Feature Release Note
Asset Calibration improvements 25.3
WATS Feature Release Note
WATS.com | ©Virinco AS page 2 of 4
Major Feature Areas
Asset Manager........................................................................................................................... 3
Asset Types................................................................................................................................ 3
API & Integration....................................................................................................................... 4
Database & backend.................................................................................................................. 4
WATS Feature Release Note
WATS.com | ©Virinco AS page 3 of 4
The Asset Manager and related APIs have been significantly improved to enhance calibration
handling, integration flexibility, and data accuracy.
Asset Manager
The Calibration interface has been redesigned with improved usability:
• The Reset button has been renamed to “Calibrate” or “Set Calibration” for clearer
function labeling.
• A new “To Date” field has been added when the Calibration Interval is set to
External.
• A Total Count reset option has been introduced (with appropriate restrictions).
o Editing Total Count requires the new “Edit Total count” permission, found
under Control Panel -> System & Assets -> Asset Manager -> Edit counters
and limits. Administrators and Managers will get this permission by default.
• Logging improvements prevent duplicate entries when the calibration date is
unchanged.
Asset Types
• New dropdown options have been added for Running Count Limit, Total Count Limit,
Calibration Interval, and Maintenance Interval, allowing for enhanced configuration.
You can now set Running Count Limit and Total Count Limit to Unlimited, while
Calibration Interval and Maintenance Interval offer both Unlimited and External
options. This upgrade makes it easier to integrate with external calibration and
maintenance systems.
WATS Feature Release Note
WATS.com | ©Virinco AS page 4 of 4
API & Integration
• New REST API endpoints introduced for external system integration:
o Asset/Calibration/External – Enables calibration updates with custom date
ranges.
o Asset/Maintenance/External – Enables maintenance updates with custom
date ranges.
o Asset/SetRunningCount and Asset/SetTotalCount – Allow external systems
to update count values.
o Asset/ResetRunningCount – Backend endpoint for controlled running count
resets.
• Existing API calls have been verified and extended to support External calibration
and count scenarios.
Database & backend
• Database schema updated to support Next Calibration and Next Maintenance dates.
• Added new columns and flags to support External and Unlimited configuration
values.
• Internal services and background jobs (e.g., Hangfire triggers) updated to recognize
and handle External calibration logic.

------------------------------------------------------------------------------

Here are all the available public endpoints. Please confirm that they are all implemented and up to date. If there are new ones here, assess if they should replace currently used internal endpoints and make sure the endpoints can solve the updates from release notes. If not, we will need to investigate additional internal endpoints

PUBLIC ENDPOINTS:

AssetShow/HideList OperationsExpand Operations
delete /api/Asset
Delete the asset which has the specified identifier.

Log records for the asset will also be deleted.

Any assets which has the asset as parent will not be deleted, but will change parent.

get /api/Asset
Returns a list of assets matching the specified filter.

put /api/Asset
Create or update an asset.

Properties such as 'runningCount' and 'totalCount' must be updated using appropriate API methods (e.g. api/Asset/Count).

Properties such as 'lastCalibrationDate' and 'lastMaintenanceDate' must be updated using appropriate API methods (e.g. api/Asset/Calibration).

The 'assetId' property can be left empty.

The 'typeId' property must be specified. Use the 'typeId' of the desired asset type (see: api/Asset/Types).

get /api/Asset/{assetId}
Get an asset

get /api/Asset/{serialNumber}
Get an asset

post /api/Asset/Calibration
Inform that an asset has been calibrated.

post /api/Asset/Calibration/External
Inform that an asset has been calibrated.

put /api/Asset/Count
Increment the running and total count on an asset.

Use 'totalCount' or 'incrementBy' query parameters to increment the running count and total count.

get /api/Asset/Log
Returns a list of asset log records matching the specified filter.

post /api/Asset/Maintenance
Inform that an asset has had maintenance.

post /api/Asset/Maintenance/External
Inform that an asset has had maintenance, and when next maintenance is due.

post /api/Asset/Message
Post a message/comment to the asset log.

post /api/Asset/ResetRunningCount
Reset running count to 0.

put /api/Asset/SetRunningCount
Sets the running count to provided integer. Id or serialNumber is required

put /api/Asset/SetTotalCount
Sets total run count to provided integer. Id or serialNumber is required

put /api/Asset/State
Set the state of an asset (e.g. "In Operation").

get /api/Asset/Status
Get the current status for an asset.

get /api/Asset/SubAssets
Return a list of sub assets/children of the specified asset.

get /api/Asset/Types
Returns a list of asset types matching the specified filter.

put /api/Asset/Types
