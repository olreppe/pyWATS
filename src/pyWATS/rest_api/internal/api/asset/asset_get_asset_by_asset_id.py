from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_get_asset_by_asset_id_response_200 import AssetGetAssetByAssetIdResponse200
from typing import cast



def _get_kwargs(
    asset_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Asset/{asset_id}".format(asset_id=asset_id,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetGetAssetByAssetIdResponse200]:
    if response.status_code == 200:
        response_200 = AssetGetAssetByAssetIdResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetGetAssetByAssetIdResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    asset_id: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[AssetGetAssetByAssetIdResponse200]:
    """ Get an asset

    Args:
        asset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetByAssetIdResponse200]
     """


    kwargs = _get_kwargs(
        asset_id=asset_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    asset_id: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[AssetGetAssetByAssetIdResponse200]:
    """ Get an asset

    Args:
        asset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetByAssetIdResponse200
     """


    return sync_detailed(
        asset_id=asset_id,
client=client,

    ).parsed

async def asyncio_detailed(
    asset_id: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[AssetGetAssetByAssetIdResponse200]:
    """ Get an asset

    Args:
        asset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetByAssetIdResponse200]
     """


    kwargs = _get_kwargs(
        asset_id=asset_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    asset_id: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[AssetGetAssetByAssetIdResponse200]:
    """ Get an asset

    Args:
        asset_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetByAssetIdResponse200
     """


    return (await asyncio_detailed(
        asset_id=asset_id,
client=client,

    )).parsed
