from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_put_asset_response_200 import AssetPutAssetResponse200
from ...models.virinco_wats_web_dashboard_models_mes_asset_asset import VirincoWATSWebDashboardModelsMesAssetAsset
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/Asset",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAsset):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAsset):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAsset):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetPutAssetResponse200]:
    if response.status_code == 200:
        response_200 = AssetPutAssetResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetPutAssetResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
    ],

) -> Response[AssetPutAssetResponse200]:
    """ Create or update an asset.

    Properties such as 'runningCount' and 'totalCount' must be updated using appropriate API methods
    (e.g. api/Asset/Count).

    Properties such as 'lastCalibrationDate' and 'lastMaintenanceDate' must be updated using appropriate
    API methods (e.g. api/Asset/Calibration).

    The 'assetId' property can be left empty.

    The 'typeId' property must be specified. Use the 'typeId' of the desired asset type (see:
    api/Asset/Types).

    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
    ],

) -> Optional[AssetPutAssetResponse200]:
    """ Create or update an asset.

    Properties such as 'runningCount' and 'totalCount' must be updated using appropriate API methods
    (e.g. api/Asset/Count).

    Properties such as 'lastCalibrationDate' and 'lastMaintenanceDate' must be updated using appropriate
    API methods (e.g. api/Asset/Calibration).

    The 'assetId' property can be left empty.

    The 'typeId' property must be specified. Use the 'typeId' of the desired asset type (see:
    api/Asset/Types).

    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
    ],

) -> Response[AssetPutAssetResponse200]:
    """ Create or update an asset.

    Properties such as 'runningCount' and 'totalCount' must be updated using appropriate API methods
    (e.g. api/Asset/Count).

    Properties such as 'lastCalibrationDate' and 'lastMaintenanceDate' must be updated using appropriate
    API methods (e.g. api/Asset/Calibration).

    The 'assetId' property can be left empty.

    The 'typeId' property must be specified. Use the 'typeId' of the desired asset type (see:
    api/Asset/Types).

    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
        VirincoWATSWebDashboardModelsMesAssetAsset,
    ],

) -> Optional[AssetPutAssetResponse200]:
    """ Create or update an asset.

    Properties such as 'runningCount' and 'totalCount' must be updated using appropriate API methods
    (e.g. api/Asset/Count).

    Properties such as 'lastCalibrationDate' and 'lastMaintenanceDate' must be updated using appropriate
    API methods (e.g. api/Asset/Calibration).

    The 'assetId' property can be left empty.

    The 'typeId' property must be specified. Use the 'typeId' of the desired asset type (see:
    api/Asset/Types).

    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)
        body (VirincoWATSWebDashboardModelsMesAssetAsset): External Asset Model (Public REST API)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
