from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_get_asset_by_serial_number_response_200 import AssetGetAssetBySerialNumberResponse200
from typing import cast



def _get_kwargs(
    serial_number: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Asset/{serial_number}".format(serial_number=serial_number,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetGetAssetBySerialNumberResponse200]:
    if response.status_code == 200:
        response_200 = AssetGetAssetBySerialNumberResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetGetAssetBySerialNumberResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    serial_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[AssetGetAssetBySerialNumberResponse200]:
    """ Get an asset

    Args:
        serial_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetBySerialNumberResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    serial_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[AssetGetAssetBySerialNumberResponse200]:
    """ Get an asset

    Args:
        serial_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetBySerialNumberResponse200
     """


    return sync_detailed(
        serial_number=serial_number,
client=client,

    ).parsed

async def asyncio_detailed(
    serial_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[AssetGetAssetBySerialNumberResponse200]:
    """ Get an asset

    Args:
        serial_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetBySerialNumberResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    serial_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[AssetGetAssetBySerialNumberResponse200]:
    """ Get an asset

    Args:
        serial_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetBySerialNumberResponse200
     """


    return (await asyncio_detailed(
        serial_number=serial_number,
client=client,

    )).parsed
