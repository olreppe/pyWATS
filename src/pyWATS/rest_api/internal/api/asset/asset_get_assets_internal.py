from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_get_assets_internal_response_200 import AssetGetAssetsInternalResponse200
from ...models.virinco_wats_web_dashboard_models_mes_asset_asset_manager_filter import VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
    ],
    bypass_cache: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["bypassCache"] = bypass_cache


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Asset/List",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetGetAssetsInternalResponse200]:
    if response.status_code == 200:
        response_200 = AssetGetAssetsInternalResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetGetAssetsInternalResponse200]:
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
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
    ],
    bypass_cache: Union[Unset, bool] = UNSET,

) -> Response[AssetGetAssetsInternalResponse200]:
    """ 
    Args:
        bypass_cache (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetsInternalResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
bypass_cache=bypass_cache,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
    ],
    bypass_cache: Union[Unset, bool] = UNSET,

) -> Optional[AssetGetAssetsInternalResponse200]:
    """ 
    Args:
        bypass_cache (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetsInternalResponse200
     """


    return sync_detailed(
        client=client,
body=body,
bypass_cache=bypass_cache,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
    ],
    bypass_cache: Union[Unset, bool] = UNSET,

) -> Response[AssetGetAssetsInternalResponse200]:
    """ 
    Args:
        bypass_cache (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetsInternalResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
bypass_cache=bypass_cache,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter,
    ],
    bypass_cache: Union[Unset, bool] = UNSET,

) -> Optional[AssetGetAssetsInternalResponse200]:
    """ 
    Args:
        bypass_cache (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetsInternalResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
bypass_cache=bypass_cache,

    )).parsed
