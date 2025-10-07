from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_put_asset_type_internal_response_200 import AssetPutAssetTypeInternalResponse200
from ...models.virinco_wats_web_dashboard_models_mes_asset_asset_type import VirincoWATSWebDashboardModelsMesAssetAssetType
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Asset/Types",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetType):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetType):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetType):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetPutAssetTypeInternalResponse200]:
    if response.status_code == 200:
        response_200 = AssetPutAssetTypeInternalResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetPutAssetTypeInternalResponse200]:
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
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
    ],

) -> Response[AssetPutAssetTypeInternalResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetTypeInternalResponse200]
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
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
    ],

) -> Optional[AssetPutAssetTypeInternalResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetTypeInternalResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
    ],

) -> Response[AssetPutAssetTypeInternalResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetTypeInternalResponse200]
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
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
        VirincoWATSWebDashboardModelsMesAssetAssetType,
    ],

) -> Optional[AssetPutAssetTypeInternalResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):
        body (VirincoWATSWebDashboardModelsMesAssetAssetType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetTypeInternalResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
