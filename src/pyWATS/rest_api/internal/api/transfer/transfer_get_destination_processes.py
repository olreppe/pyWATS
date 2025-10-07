from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.transfer_get_destination_processes_response_200 import TransferGetDestinationProcessesResponse200
from typing import cast



def _get_kwargs(
    *,
    url_query: str,
    token: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["url"] = url_query

    params["token"] = token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Transfer/Share/Processes",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TransferGetDestinationProcessesResponse200]:
    if response.status_code == 200:
        response_200 = TransferGetDestinationProcessesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TransferGetDestinationProcessesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    token: str,

) -> Response[TransferGetDestinationProcessesResponse200]:
    """ 
    Args:
        url_query (str):
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferGetDestinationProcessesResponse200]
     """


    kwargs = _get_kwargs(
        url_query=url_query,
token=token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    token: str,

) -> Optional[TransferGetDestinationProcessesResponse200]:
    """ 
    Args:
        url_query (str):
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferGetDestinationProcessesResponse200
     """


    return sync_detailed(
        client=client,
url_query=url_query,
token=token,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    token: str,

) -> Response[TransferGetDestinationProcessesResponse200]:
    """ 
    Args:
        url_query (str):
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferGetDestinationProcessesResponse200]
     """


    kwargs = _get_kwargs(
        url_query=url_query,
token=token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    url_query: str,
    token: str,

) -> Optional[TransferGetDestinationProcessesResponse200]:
    """ 
    Args:
        url_query (str):
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferGetDestinationProcessesResponse200
     """


    return (await asyncio_detailed(
        client=client,
url_query=url_query,
token=token,

    )).parsed
