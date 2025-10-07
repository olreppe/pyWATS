from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.upgrade_hangfire_single_server_mode_response_200 import UpgradeHangfireSingleServerModeResponse200
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime



def _get_kwargs(
    *,
    server_name: Union[Unset, str] = UNSET,
    time_out: Union[Unset, datetime.datetime] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serverName"] = server_name

    json_time_out: Union[Unset, str] = UNSET
    if not isinstance(time_out, Unset):
        json_time_out = time_out.isoformat()
    params["timeOut"] = json_time_out


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Upgrade/HangfireSingleServerMode",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UpgradeHangfireSingleServerModeResponse200]:
    if response.status_code == 200:
        response_200 = UpgradeHangfireSingleServerModeResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UpgradeHangfireSingleServerModeResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    server_name: Union[Unset, str] = UNSET,
    time_out: Union[Unset, datetime.datetime] = UNSET,

) -> Response[UpgradeHangfireSingleServerModeResponse200]:
    """ Specify a given servername as the only server to run hangfire queues.
    NOTE: Other servers will recycle to apply single server mode.
    A cfg.setting record is added in following format: Hangfire:SingelServerUntilUtc	desktop-
    rvuq22s|2024-04-04T10:46:31.7575160Z

    Args:
        server_name (Union[Unset, str]):
        time_out (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeHangfireSingleServerModeResponse200]
     """


    kwargs = _get_kwargs(
        server_name=server_name,
time_out=time_out,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    server_name: Union[Unset, str] = UNSET,
    time_out: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[UpgradeHangfireSingleServerModeResponse200]:
    """ Specify a given servername as the only server to run hangfire queues.
    NOTE: Other servers will recycle to apply single server mode.
    A cfg.setting record is added in following format: Hangfire:SingelServerUntilUtc	desktop-
    rvuq22s|2024-04-04T10:46:31.7575160Z

    Args:
        server_name (Union[Unset, str]):
        time_out (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeHangfireSingleServerModeResponse200
     """


    return sync_detailed(
        client=client,
server_name=server_name,
time_out=time_out,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    server_name: Union[Unset, str] = UNSET,
    time_out: Union[Unset, datetime.datetime] = UNSET,

) -> Response[UpgradeHangfireSingleServerModeResponse200]:
    """ Specify a given servername as the only server to run hangfire queues.
    NOTE: Other servers will recycle to apply single server mode.
    A cfg.setting record is added in following format: Hangfire:SingelServerUntilUtc	desktop-
    rvuq22s|2024-04-04T10:46:31.7575160Z

    Args:
        server_name (Union[Unset, str]):
        time_out (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeHangfireSingleServerModeResponse200]
     """


    kwargs = _get_kwargs(
        server_name=server_name,
time_out=time_out,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    server_name: Union[Unset, str] = UNSET,
    time_out: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[UpgradeHangfireSingleServerModeResponse200]:
    """ Specify a given servername as the only server to run hangfire queues.
    NOTE: Other servers will recycle to apply single server mode.
    A cfg.setting record is added in following format: Hangfire:SingelServerUntilUtc	desktop-
    rvuq22s|2024-04-04T10:46:31.7575160Z

    Args:
        server_name (Union[Unset, str]):
        time_out (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeHangfireSingleServerModeResponse200
     """


    return (await asyncio_detailed(
        client=client,
server_name=server_name,
time_out=time_out,

    )).parsed
