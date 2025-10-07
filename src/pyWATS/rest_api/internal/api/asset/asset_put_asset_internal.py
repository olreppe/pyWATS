from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_put_asset_internal_response_200 import AssetPutAssetInternalResponse200
from ...models.virinco_wats_web_dashboard_models_mes_asset_asset_manager_entity import VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
    ],
    is_new: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["isNew"] = is_new


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Asset",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetPutAssetInternalResponse200]:
    if response.status_code == 200:
        response_200 = AssetPutAssetInternalResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetPutAssetInternalResponse200]:
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
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
    ],
    is_new: Union[Unset, bool] = UNSET,

) -> Response[AssetPutAssetInternalResponse200]:
    """ 
    Args:
        is_new (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetInternalResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
is_new=is_new,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
    ],
    is_new: Union[Unset, bool] = UNSET,

) -> Optional[AssetPutAssetInternalResponse200]:
    """ 
    Args:
        is_new (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetInternalResponse200
     """


    return sync_detailed(
        client=client,
body=body,
is_new=is_new,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
    ],
    is_new: Union[Unset, bool] = UNSET,

) -> Response[AssetPutAssetInternalResponse200]:
    """ 
    Args:
        is_new (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetInternalResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
is_new=is_new,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
        VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity,
    ],
    is_new: Union[Unset, bool] = UNSET,

) -> Optional[AssetPutAssetInternalResponse200]:
    """ 
    Args:
        is_new (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):
        body (VirincoWATSWebDashboardModelsMesAssetAssetManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetInternalResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
is_new=is_new,

    )).parsed
