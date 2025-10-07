from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.system_manager_client_log_response_200 import SystemManagerClientLogResponse200
from typing import cast



def _get_kwargs(
    identifier: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/SystemManager/ClientLog/{identifier}".format(identifier=identifier,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SystemManagerClientLogResponse200]:
    if response.status_code == 200:
        response_200 = SystemManagerClientLogResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SystemManagerClientLogResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[SystemManagerClientLogResponse200]:
    """ Get most recent client log for specified client (6.0 or newer)

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerClientLogResponse200]
     """


    kwargs = _get_kwargs(
        identifier=identifier,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[SystemManagerClientLogResponse200]:
    """ Get most recent client log for specified client (6.0 or newer)

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerClientLogResponse200
     """


    return sync_detailed(
        identifier=identifier,
client=client,

    ).parsed

async def asyncio_detailed(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[SystemManagerClientLogResponse200]:
    """ Get most recent client log for specified client (6.0 or newer)

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerClientLogResponse200]
     """


    kwargs = _get_kwargs(
        identifier=identifier,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[SystemManagerClientLogResponse200]:
    """ Get most recent client log for specified client (6.0 or newer)

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerClientLogResponse200
     """


    return (await asyncio_detailed(
        identifier=identifier,
client=client,

    )).parsed
