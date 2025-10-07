from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_put_asset_count_response_200 import AssetPutAssetCountResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    total_count: Union[Unset, int] = UNSET,
    increment_by: Union[Unset, int] = UNSET,
    increment_children: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["id"] = id

    params["serialNumber"] = serial_number

    params["totalCount"] = total_count

    params["incrementBy"] = increment_by

    params["incrementChildren"] = increment_children

    params["cultureCode"] = culture_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/Asset/Count",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetPutAssetCountResponse200]:
    if response.status_code == 200:
        response_200 = AssetPutAssetCountResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetPutAssetCountResponse200]:
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
    total_count: Union[Unset, int] = UNSET,
    increment_by: Union[Unset, int] = UNSET,
    increment_children: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[AssetPutAssetCountResponse200]:
    """ Increment the running and total count on an asset.

    Use 'totalCount' or 'incrementBy' query parameters to increment the running count and total count.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        total_count (Union[Unset, int]):
        increment_by (Union[Unset, int]):
        increment_children (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetCountResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
serial_number=serial_number,
total_count=total_count,
increment_by=increment_by,
increment_children=increment_children,
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
    total_count: Union[Unset, int] = UNSET,
    increment_by: Union[Unset, int] = UNSET,
    increment_children: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[AssetPutAssetCountResponse200]:
    """ Increment the running and total count on an asset.

    Use 'totalCount' or 'incrementBy' query parameters to increment the running count and total count.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        total_count (Union[Unset, int]):
        increment_by (Union[Unset, int]):
        increment_children (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetCountResponse200
     """


    return sync_detailed(
        client=client,
id=id,
serial_number=serial_number,
total_count=total_count,
increment_by=increment_by,
increment_children=increment_children,
culture_code=culture_code,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    total_count: Union[Unset, int] = UNSET,
    increment_by: Union[Unset, int] = UNSET,
    increment_children: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[AssetPutAssetCountResponse200]:
    """ Increment the running and total count on an asset.

    Use 'totalCount' or 'incrementBy' query parameters to increment the running count and total count.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        total_count (Union[Unset, int]):
        increment_by (Union[Unset, int]):
        increment_children (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPutAssetCountResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
serial_number=serial_number,
total_count=total_count,
increment_by=increment_by,
increment_children=increment_children,
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
    total_count: Union[Unset, int] = UNSET,
    increment_by: Union[Unset, int] = UNSET,
    increment_children: Union[Unset, bool] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[AssetPutAssetCountResponse200]:
    """ Increment the running and total count on an asset.

    Use 'totalCount' or 'incrementBy' query parameters to increment the running count and total count.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        total_count (Union[Unset, int]):
        increment_by (Union[Unset, int]):
        increment_children (Union[Unset, bool]):
        culture_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPutAssetCountResponse200
     """


    return (await asyncio_detailed(
        client=client,
id=id,
serial_number=serial_number,
total_count=total_count,
increment_by=increment_by,
increment_children=increment_children,
culture_code=culture_code,

    )).parsed
