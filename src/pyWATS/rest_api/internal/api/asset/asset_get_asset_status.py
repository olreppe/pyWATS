from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_get_asset_status_response_200 import AssetGetAssetStatusResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    translate: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["id"] = id

    params["serialNumber"] = serial_number

    params["translate"] = translate

    params["cultureCode"] = culture_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Asset/Status",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetGetAssetStatusResponse200]:
    if response.status_code == 200:
        response_200 = AssetGetAssetStatusResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetGetAssetStatusResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    translate: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[AssetGetAssetStatusResponse200]:
    """ Get the current status for an asset.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        translate (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetStatusResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
serial_number=serial_number,
translate=translate,
culture_code=culture_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    translate: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[AssetGetAssetStatusResponse200]:
    """ Get the current status for an asset.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        translate (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetStatusResponse200
     """


    return sync_detailed(
        client=client,
id=id,
serial_number=serial_number,
translate=translate,
culture_code=culture_code,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    translate: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[AssetGetAssetStatusResponse200]:
    """ Get the current status for an asset.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        translate (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetGetAssetStatusResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
serial_number=serial_number,
translate=translate,
culture_code=culture_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    translate: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[AssetGetAssetStatusResponse200]:
    """ Get the current status for an asset.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        translate (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetGetAssetStatusResponse200
     """


    return (await asyncio_detailed(
        client=client,
id=id,
serial_number=serial_number,
translate=translate,
culture_code=culture_code,

    )).parsed
