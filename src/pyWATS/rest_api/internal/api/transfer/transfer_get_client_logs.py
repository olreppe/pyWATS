from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.transfer_get_client_logs_response_200 import TransferGetClientLogsResponse200
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime



def _get_kwargs(
    *,
    logs_from: Union[Unset, datetime.datetime] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_logs_from: Union[Unset, str] = UNSET
    if not isinstance(logs_from, Unset):
        json_logs_from = logs_from.isoformat()
    params["logsFrom"] = json_logs_from


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Transfer/Client/Log",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TransferGetClientLogsResponse200]:
    if response.status_code == 200:
        response_200 = TransferGetClientLogsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TransferGetClientLogsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    logs_from: Union[Unset, datetime.datetime] = UNSET,

) -> Response[TransferGetClientLogsResponse200]:
    """ 
    Args:
        logs_from (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferGetClientLogsResponse200]
     """


    kwargs = _get_kwargs(
        logs_from=logs_from,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    logs_from: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[TransferGetClientLogsResponse200]:
    """ 
    Args:
        logs_from (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferGetClientLogsResponse200
     """


    return sync_detailed(
        client=client,
logs_from=logs_from,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    logs_from: Union[Unset, datetime.datetime] = UNSET,

) -> Response[TransferGetClientLogsResponse200]:
    """ 
    Args:
        logs_from (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferGetClientLogsResponse200]
     """


    kwargs = _get_kwargs(
        logs_from=logs_from,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    logs_from: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[TransferGetClientLogsResponse200]:
    """ 
    Args:
        logs_from (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferGetClientLogsResponse200
     """


    return (await asyncio_detailed(
        client=client,
logs_from=logs_from,

    )).parsed
