using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Versioning;

namespace Virinco.WATS.Interface.MES.Asset
{
    /// <summary>
    /// Class that contains functions for Asset handling.
    /// </summary>
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows")]
#endif
    public class AssetHandler : MesBase
    {
        /// <summary>
        /// True if connected to server.
        /// </summary>
        /// <returns></returns>
        new public bool isConnected()
        {
            return base.isConnected();
        }

        /// <summary>
        /// Creates an Asset of specified type.
        /// </summary>
        /// <param name="serialNumber">Asset serial number</param>
        /// <param name="assetType">Asset type</param>
        /// <param name="parentAssetSerialNumber">Optional. Serial number of the parent asset. If blank, the new asset will have no parent</param>
        /// <param name="assetName">Optional. Asset name</param>
        /// <param name="assetDescription">Optional Asset description</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse CreateAsset(string serialNumber, string assetType, string parentAssetSerialNumber = null, string assetName = null, string assetDescription = null)
        {
            var response = new AssetResponse();

            try
            {
                response = GetAsset(serialNumber);
                if (!response.Ok && response.Status == Asset_Status.NotRegistered)
                {
                    var assetTypes = serviceProxy.GetJson<AssetType[]>($"api/Asset/Types?$filter=typeName eq '{assetType}'");
                    if (assetTypes.Length == 1) //Type must exist
                    {
                        var asset = new Asset 
                        { 
                            TypeId = assetTypes[0].TypeId, 
                            SerialNumber = serialNumber, 
                            AssetName = assetName, 
                            Description = assetDescription
                        };

                        if (!string.IsNullOrEmpty(parentAssetSerialNumber))                        
                            asset.ParentSerialNumber = parentAssetSerialNumber;
                        
                        asset = serviceProxy.PutJson<Asset>("api/Asset", asset);
                        response = GetAsset(serialNumber);
                    }
                    else
                        response.SetError($"Asset type '{assetType}' does not exist");
                }
                else if (response.Status != Asset_Status.SystemError)
                    response.SetError($"Asset '{serialNumber}' already exists");
            }
            catch (Exception e) 
            { 
                Env.LogException(e, "Asset:CreateAsset"); 
                response.SetError(e.Message, Asset_Status.SystemError); 
            }

            return response;
        }

        /// <summary>
        /// Creates an Asset Type.
        /// </summary>
        /// <param name="name">Name of the type. Must be unique.</param>
        /// <param name="calibrationInterval">How often assets of this type must be calibrated in days (e.g 1.0 or 1.5).</param>
        /// <param name="maintenanceInterval">How often assets of this type must be maintained in days (e.g 1.0 or 1.5).</param>
        /// <param name="runningCountLimit">Max number of uses before the next calibration of the asset must be performed.</param>
        /// <param name="totalCountLimit">Max number of uses of the asset in its lifetime.</param>
        /// <param name="warningThreshold">How close to the limits an asset can be before a warning is issued (0-100).</param>
        /// <param name="alarmTreshold">How close to the limits an asset can be before an alarm is issued (0-100).</param>
        /// <returns></returns>
        public AssetResponse CreateAssetType(string name, decimal? calibrationInterval = null, decimal? maintenanceInterval = null, int? runningCountLimit = null, int? totalCountLimit = null, decimal? warningThreshold = null, decimal? alarmTreshold = null)
        {
            var response = new AssetResponse();
            try
            {               
                var assetTypes = serviceProxy.GetJson<AssetType[]>($"api/Asset/Types?$filter=typeName eq '{name}'");
                if (assetTypes.Length == 0) //Type must not exist
                {
                    var type = new AssetType
                    {
                        TypeId = Guid.NewGuid(),
                        CalibrationInterval = calibrationInterval,
                        AlarmThreshold = alarmTreshold,
                        MaintenanceInterval = maintenanceInterval,
                        RunningCountLimit = runningCountLimit,
                        TotalCountLimit = totalCountLimit,
                        TypeName = name,
                        WarningThreshold = warningThreshold
                    };                    

                    type = serviceProxy.PutJson<AssetType>("api/Asset/Types", type);                    
                }
                else
                    response.SetError($"Asset type '{name}' already exist");
            }
            catch (Exception e)
            {
                Env.LogException(e, "Asset:CreateAsset");
                response.SetError(e.Message, Asset_Status.SystemError);
            }

            return response;
        }

        /// <summary>
        /// Fetches a specific asset.
        /// </summary>
        /// <param name="serialNumber">Asset serial number</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse GetAsset(string serialNumber)
        {
            var response = new AssetResponse();

            try
            {
                var assets = serviceProxy.GetJson<InternalAsset[]>($"api/Asset?$filter=serialNumber eq '{serialNumber}'");
                if (assets.Length == 1)
                {
                    response.AssetObject = assets[0];
                    response.AssetObject.SetTagsArray();
                    response.AssetObject.AssetStatus = serviceProxy.GetJson<AssetStatus>($"api/Asset/Status?serialNumber={serialNumber}");
                    response.AssetObject.AssetType= serviceProxy.GetJson<AssetType[]>($"api/Asset/Types?$filter=typeId eq {assets[0].TypeId}")[0];
                }
                else
                    response.SetError($"Asset '{serialNumber}' does not exist", Asset_Status.NotRegistered);
            }
            catch (Exception e) 
            {
                Env.LogException(e, "Asset:GetAsset"); 
                response.SetError(e.Message, Asset_Status.SystemError);
            }

            return response;
        }

        /// <summary>
        /// Updates asset object changes.
        /// </summary>
        /// <param name="asset">Asset object to be updated</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse UpdateAsset(Asset asset)
        {
            var response = new AssetResponse();

            try
            {
                //Let parent serial number decide asset will be parent
                asset.ParentAssetId = null;

                //update Tags from TagsArray if TagsArray has changed
                asset.UpdateTags();

                asset = serviceProxy.PutJson<Asset>("api/Asset", asset);
                asset.SetTagsArray();
                response.AssetObject = asset;
            }
            catch (Exception e) 
            {
                Env.LogException(e, "Asset:UpdateAsset"); 
                response.SetError(e.Message, Asset_Status.SystemError); 
            }

            return response;
        }

        /// <summary>
        /// Sets, updates or remove an asset's parent.
        /// </summary>
        /// <param name="serialNumber">Asset serial number for the asset whose parent will be set.</param>
        /// <param name="parentSerialNumber">New parent serialNumber for the asset (can be null).</param>
        /// <returns>AssetResponse object (with the asset's parent serial number set)</returns>
        public AssetResponse SetParent(string serialNumber, string parentSerialNumber)
        {
            var response = new AssetResponse();

            try
            {
                response = GetAsset(serialNumber);
                if (response.Ok)
                {
                    response.AssetObject.ParentSerialNumber = parentSerialNumber;
                    response = UpdateAsset(response.AssetObject);
                }
            }
            catch(Exception e) 
            { 
                Env.LogException(e, "Asset:SetParent");
                response.SetError(e.Message, Asset_Status.SystemError); 
            }

            return response;
        }

        /// <summary>
        /// Increment an asset's usage count by default (1) or specified int value.
        /// </summary>
        /// <param name="serialNumber">Asset serial number</param>
        /// <param name="usageCount">Value of usage count increment (default 1)</param>
        /// <param name="incrementSubAssets">Boolean with default=false. Set to true if you want to increment the asset's sub-assets.</param>
        /// <returns>AssetResponse object (with the incremented asset)</returns>
        public AssetResponse IncrementAssetUsageCount(string serialNumber, int usageCount = 1, bool incrementSubAssets = false)
        {
            var response = new AssetResponse();

            try
            {
                Asset_Status assetStatus = serviceProxy.PutJson<Asset_Status>($"api/Asset/Count?serialNumber={serialNumber}&incrementBy={usageCount}&incrementChildren={incrementSubAssets}&cultureCode={CultureCode}", null);
                response = GetAsset(serialNumber);
                response.AssetObject.AssetStatus.Status = assetStatus;
            }
            catch (Exception e) 
            { 
                Env.LogException(e, "Asset:IncrementAssetUsageCount");
                response.SetError(e.Message, Asset_Status.SystemError);
            }

            return response;
        }

        /// <summary>
        /// Fetches all assets, filtered by a specified OData (REST) filter.
        /// </summary>
        /// <param name="filter">OData filter (syntax example: ($"startswith(serialNumber,'{Prefix}')"). NB! Uses camel casing.</param>
        /// <returns>AssetResponse object with filtered assets in SubAssets property</returns>
        public AssetResponse GetAssets(string filter)
        {
            var response = new AssetResponse();

            try
            {
                var assets = serviceProxy.GetJson<InternalAsset[]>($"api/Asset" + (string.IsNullOrEmpty(filter) ? "" : $"?$filter={filter}"));
                if (assets.Length > 0)
                {
                    response.SubAssets = assets;
                    foreach (var asset in assets)
                        asset.SetTagsArray();
                }
                else 
                    response.SetError("No asset matches filter", Asset_Status.NotRegistered);
            }
            catch (Exception e) 
            { 
                Env.LogException(e, "Asset:GetAssets"); 
                response.SetError(e.Message, Asset_Status.SystemError); 
            }

            return response;
        }

        /// <summary>
        /// Fetches all assets, filtered by tag.
        /// </summary>
        /// <param name="tag">Name of tag.</param>
        /// <returns>AssetResponse object with filtered assets in SubAssets property</returns>
        public AssetResponse GetAssetsByTag(string tag)
        {
            var filter = $"xmldata eq '//{tag}'";
            return GetAssets(filter);
        }

        /// <summary>
        /// Fetches all sub assets of a parent asset.
        /// </summary>
        /// <param name="serialNumber">Parent asset serial number</param>
        /// <returns>AssetResponse object (with sub-assets)</returns>
        public AssetResponse GetSubAssets(string serialNumber)
        {
            return GetSubAssets(serialNumber, 0);
        }

        /// <summary>
        /// Fetches sub assets of a parent asset down to and including level.
        /// </summary>
        /// <param name="serialNumber">Parent asset serial number</param>
        /// <param name="level">How many sub assets of sub assets to get. 0 to get all, 1 to get direct children only.</param>
        /// <returns>AssetResponse object (with sub-assets)</returns>
        public AssetResponse GetSubAssets(string serialNumber, int level)
        {
            var response = new AssetResponse();

            try
            {
                var assets = serviceProxy.GetJson<Asset[]>($"api/Asset/SubAssets?serialNumber={serialNumber}&level={level}");
                if (assets.Length > 0)
                {
                    response.SubAssets = assets;

                    foreach (var asset in assets)
                    {
                        asset.SetTagsArray();
                        asset.AssetStatus = serviceProxy.GetJson<AssetStatus>($"api/Asset/Status?serialNumber={asset.SerialNumber}");
                        asset.AssetType = serviceProxy.GetJson<AssetType[]>($"api/Asset/Types?$filter=typeId eq {asset.TypeId}")[0];
                    }
                }
                else
                    response.SetError("Asset has no sub assets", Asset_Status.NotRegistered);
            }
            catch (Exception e)
            {
                Env.LogException(e, "Asset:GetSubAssets");
                response.SetError(e.Message, Asset_Status.SystemError);
            }

            return response;
        }

        /// <summary>
        /// Register calibration to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Calibration asset's serial number.</param>
        /// <param name="dateTime">If specified, sets the LastCalibrationDate to the specified date and time. Default = null (today).</param>
        /// <param name="comment">Asset log comment.</param>
        /// <returns>AssetResponse object (with the calibrated asset).</returns>
        public AssetResponse Calibration(string serialNumber, DateTime? dateTime = null, string comment = null)
        {
            var response = new AssetResponse();

            try
            {
                //if (string.IsNullOrEmpty(adminToken))
                //    throw new ApplicationException("Admin credentials not set, use SetAdminCredentials prior to call");

                var parameters = new List<string>();
                parameters.Add(GetParameter("serialNumber", serialNumber));

                if (dateTime != null)
                    parameters.Add(GetParameter("dateTime", dateTime.Value.ToString("s")));

                if (comment != null)
                    parameters.Add(GetParameter("comment", comment));

                serviceProxy.PostJson<string>($"api/Asset/Calibration?{string.Join("&", parameters)}", null);
                response = GetAsset(serialNumber);
            }
            catch (Exception e) 
            { 
                Env.LogException(e, "Asset:Calibration"); 
                response.SetError(e.Message, Asset_Status.SystemError); 
            }

            return response;

            string GetParameter(string key, string value) => $"{key}={value}";
        }

        /// <summary>
        /// Register calibration to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Calibration asset's serial number.</param>
        /// <param name="dateTime">Sets the LastCalibrationDate to the specified date and time.</param>
        /// <param name="comment">Asset log comment.</param>
        /// <returns>AssetResponse object (with the calibrated asset)</returns>
        public AssetResponse Calibration(string serialNumber, DateTime dateTime, string comment)
        {
            return Calibration(serialNumber, (DateTime?)dateTime, comment);
        }

        /// <summary>
        /// Register maintenance to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Maintenance asset serialNumber.</param>
        /// <param name="dateTime">If specified, sets the LastMaintenanceDate to the specified date and time. Default = null (today).</param>
        /// <param name="comment">Asset log comment.</param>
        /// <returns>AssetResponse Object (with the maintenanced asset).</returns>
        public AssetResponse Maintenance(string serialNumber, DateTime? dateTime = null, string comment = null)
        {
            var response = new AssetResponse();

            try
            {
                //if (string.IsNullOrEmpty(adminToken))
                //    throw new ApplicationException("Admin credentials not set, use SetAdminCredentials prior to call");

                var parameters = new List<string>();
                parameters.Add(GetParameter("serialNumber", serialNumber));

                if (dateTime != null)
                    parameters.Add(GetParameter("dateTime", dateTime.Value.ToString("s")));

                if (comment != null)
                    parameters.Add(GetParameter("comment", comment));

                serviceProxy.PostJson<string>($"api/Asset/Maintenance?{string.Join("&", parameters)}", null);
                response = GetAsset(serialNumber);
            }
            catch (Exception e) 
            { 
                Env.LogException(e, "Asset:Maintenance"); 
                response.SetError(e.Message, Asset_Status.SystemError); 
            }

            return response;

            string GetParameter(string key, string value) => $"{key}={value}";
        }

        /// <summary>
        /// Register maintenance to the specified asset.
        /// </summary>
        /// <param name="serialNumber">Maintenance asset serialNumber</param>
        /// <param name="dateTime">Sets the LastMaintenanceDate to the specified date and time.</param>
        /// <param name="comment">Asset log comment</param>
        /// <returns>AssetResponse Object (with the maintenanced asset)</returns>
        public AssetResponse Maintenance(string serialNumber, DateTime dateTime, string comment)
        {
            return Maintenance(serialNumber, (DateTime?)dateTime, comment);
        }

        /// <summary>
        /// Reset running count to 0.
        /// </summary>
        /// <param name="serialNumber">Maintenance asset serialNumber</param>
        /// <param name="comment">Asset log comment</param>
        /// <returns>AssetResponse Object (with the reset asset)</returns>
        public AssetResponse ResetRunningCount(string serialNumber, string comment = null)
        {
            var response = new AssetResponse();

            try
            {
                var parameters = new List<string>();
                parameters.Add(GetParameter("serialNumber", serialNumber));

                if (comment != null)
                    parameters.Add(GetParameter("comment", comment));

                serviceProxy.PostJson<string>($"api/Asset/ResetRunningCount?{string.Join("&", parameters)}", null);
                response = GetAsset(serialNumber);
            }
            catch (Exception e)
            {
                Env.LogException(e, "Asset:ResetRunningCount");
                response.SetError(e.Message, Asset_Status.SystemError);
            }

            return response;

            string GetParameter(string key, string value) => $"{key}={value}";
        }

        /// <summary>
        /// Deletes the specified asset.
        /// Sub-assets will be updated to no longer contain have a parent.
        /// Client must have admin credentials to delete an asset.
        /// </summary>
        /// <param name="serialNumber">Delete asset serial number</param>
        /// <returns>AssetResponse object</returns>
        public AssetResponse DeleteAsset(string serialNumber)
        {
            var response = new AssetResponse();

            try
            {
                Asset asset = serviceProxy.DeleteJson<Asset>($"api/Asset?serialNumber={serialNumber}", null);
                if (asset != null)
                {
                    asset.SetTagsArray();
                    response.AssetObject = asset;
                }
                else 
                    response.SetError($"Could not delete asset {serialNumber}");
            }
            catch (Exception e) 
            { 
                Env.LogException(e, "Asset:DeleteAsset"); 
                response.SetError(e.Message, Asset_Status.SystemError); 
            }

            return response;
        }
    }
}