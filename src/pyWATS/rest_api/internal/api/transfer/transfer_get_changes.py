from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.transfer_get_changes_response_200 import TransferGetChangesResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    transferred: Union[Unset, bool] = UNSET,
    max_: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["transferred"] = transferred

    params["max"] = max_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Transfer/Change",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TransferGetChangesResponse200]:
    if response.status_code == 200:
        response_200 = TransferGetChangesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TransferGetChangesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    transferred: Union[Unset, bool] = UNSET,
    max_: Union[Unset, int] = UNSET,

) -> Response[TransferGetChangesResponse200]:
    """ 
    Args:
        transferred (Union[Unset, bool]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferGetChangesResponse200]
     """


    kwargs = _get_kwargs(
        transferred=transferred,
max_=max_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    transferred: Union[Unset, bool] = UNSET,
    max_: Union[Unset, int] = UNSET,

) -> Optional[TransferGetChangesResponse200]:
    """ 
    Args:
        transferred (Union[Unset, bool]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferGetChangesResponse200
     """


    return sync_detailed(
        client=client,
transferred=transferred,
max_=max_,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    transferred: Union[Unset, bool] = UNSET,
    max_: Union[Unset, int] = UNSET,

) -> Response[TransferGetChangesResponse200]:
    """ 
    Args:
        transferred (Union[Unset, bool]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferGetChangesResponse200]
     """


    kwargs = _get_kwargs(
        transferred=transferred,
max_=max_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    transferred: Union[Unset, bool] = UNSET,
    max_: Union[Unset, int] = UNSET,

) -> Optional[TransferGetChangesResponse200]:
    """ 
    Args:
        transferred (Union[Unset, bool]):
        max_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferGetChangesResponse200
     """


    return (await asyncio_detailed(
        client=client,
transferred=transferred,
max_=max_,

    )).parsed
