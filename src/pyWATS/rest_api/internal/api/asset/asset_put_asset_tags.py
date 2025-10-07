from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_put_asset_tags_response_200 import AssetPutAssetTagsResponse200
from ...models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
from typing import cast



def _get_kwargs(
    id: str,
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Asset/{id}/Tags".format(id=id,),
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductSetting']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductSetting']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductSetting']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetPutAssetTagsResponse200]:
    if response.status_code == 200:
        response_200 = AssetPutAssetTagsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetPutAssetTagsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
    ],

) -> Response[AssetPutAssetTagsResponse200]:
    """ 
    Args:
        id (str):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetTagsResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
    ],

) -> Optional[AssetPutAssetTagsResponse200]:
    """ 
    Args:
        id (str):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetTagsResponse200
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
    ],

) -> Response[AssetPutAssetTagsResponse200]:
    """ 
    Args:
        id (str):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetTagsResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
        list['VirincoWATSWebDashboardModelsMesProductSetting'],
    ],

) -> Optional[AssetPutAssetTagsResponse200]:
    """ 
    Args:
        id (str):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):
        body (list['VirincoWATSWebDashboardModelsMesProductSetting']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetTagsResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
