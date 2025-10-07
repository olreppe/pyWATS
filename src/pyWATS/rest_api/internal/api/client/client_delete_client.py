from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_delete_client_response_200 import ClientDeleteClientResponse200
from typing import cast



def _get_kwargs(
    mac: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/Internal/Client/Delete/{mac}".format(mac=mac,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ClientDeleteClientResponse200]:
    if response.status_code == 200:
        response_200 = ClientDeleteClientResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ClientDeleteClientResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    mac: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ClientDeleteClientResponse200]:
    """ Devtest method for cleaning up after running internal tests. This should not be used in production,
    and it will fail outside devtest environment

    Args:
        mac (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientDeleteClientResponse200]
     """


    kwargs = _get_kwargs(
        mac=mac,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    mac: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ClientDeleteClientResponse200]:
    """ Devtest method for cleaning up after running internal tests. This should not be used in production,
    and it will fail outside devtest environment

    Args:
        mac (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientDeleteClientResponse200
     """


    return sync_detailed(
        mac=mac,
client=client,

    ).parsed

async def asyncio_detailed(
    mac: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ClientDeleteClientResponse200]:
    """ Devtest method for cleaning up after running internal tests. This should not be used in production,
    and it will fail outside devtest environment

    Args:
        mac (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientDeleteClientResponse200]
     """


    kwargs = _get_kwargs(
        mac=mac,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    mac: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ClientDeleteClientResponse200]:
    """ Devtest method for cleaning up after running internal tests. This should not be used in production,
    and it will fail outside devtest environment

    Args:
        mac (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientDeleteClientResponse200
     """


    return (await asyncio_detailed(
        mac=mac,
client=client,

    )).parsed
