from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.transfer_set_state_response_200 import TransferSetStateResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    *,
    report_id: UUID,
    rulename: str,
    state: int,
    message: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_report_id = str(report_id)
    params["reportId"] = json_report_id

    params["rulename"] = rulename

    params["state"] = state

    params["message"] = message


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Transfer/Pending/SetState",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TransferSetStateResponse200]:
    if response.status_code == 200:
        response_200 = TransferSetStateResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TransferSetStateResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    rulename: str,
    state: int,
    message: Union[Unset, str] = UNSET,

) -> Response[TransferSetStateResponse200]:
    """ 
    Args:
        report_id (UUID):
        rulename (str):
        state (int):
        message (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferSetStateResponse200]
     """


    kwargs = _get_kwargs(
        report_id=report_id,
rulename=rulename,
state=state,
message=message,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    rulename: str,
    state: int,
    message: Union[Unset, str] = UNSET,

) -> Optional[TransferSetStateResponse200]:
    """ 
    Args:
        report_id (UUID):
        rulename (str):
        state (int):
        message (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferSetStateResponse200
     """


    return sync_detailed(
        client=client,
report_id=report_id,
rulename=rulename,
state=state,
message=message,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    rulename: str,
    state: int,
    message: Union[Unset, str] = UNSET,

) -> Response[TransferSetStateResponse200]:
    """ 
    Args:
        report_id (UUID):
        rulename (str):
        state (int):
        message (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferSetStateResponse200]
     """


    kwargs = _get_kwargs(
        report_id=report_id,
rulename=rulename,
state=state,
message=message,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    rulename: str,
    state: int,
    message: Union[Unset, str] = UNSET,

) -> Optional[TransferSetStateResponse200]:
    """ 
    Args:
        report_id (UUID):
        rulename (str):
        state (int):
        message (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferSetStateResponse200
     """


    return (await asyncio_detailed(
        client=client,
report_id=report_id,
rulename=rulename,
state=state,
message=message,

    )).parsed
