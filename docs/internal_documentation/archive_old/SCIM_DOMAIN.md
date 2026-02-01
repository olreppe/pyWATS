ScimShow/HideList OperationsExpand Operations
get /api/SCIM/v2/Token
Creates a Json Web Token to be used with automatic provisioning from Azure. Provided with duration, you can specify the amount of days until the token expires and will need to have a new one generated. The default duration is set to 90 days.

get /api/SCIM/v2/Users
Gets a list of all users.

post /api/SCIM/v2/Users
Creates a new user using the provided user information in JSON format.

delete /api/SCIM/v2/Users/{id}
Deletes a single user using userId.

get /api/SCIM/v2/Users/{id}
Gets the user associated with the provided id.

patch /api/SCIM/v2/Users/{id}
Updates user details for the provided username using JSON following the SCIM protocol. Has to be in a SCIM patchOp format with schema. Only "replace" is supported and value has to be either a string or boolean, depending on their original data type.

get /api/SCIM/v2/Users/userName={userName}
Gets a user using the provided user name.

