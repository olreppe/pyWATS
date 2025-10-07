from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.scim_get_user_response_200 import ScimGetUserResponse200
from typing import cast



def _get_kwargs(
    user_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/SCIM/v2/Users/userName={user_name}".format(user_name=user_name,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ScimGetUserResponse200]:
    if response.status_code == 200:
        response_200 = ScimGetUserResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ScimGetUserResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ScimGetUserResponse200]:
    """ Gets a user using the provided user name.

    Args:
        user_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimGetUserResponse200]
     """


    kwargs = _get_kwargs(
        user_name=user_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    user_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ScimGetUserResponse200]:
    """ Gets a user using the provided user name.

    Args:
        user_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimGetUserResponse200
     """


    return sync_detailed(
        user_name=user_name,
client=client,

    ).parsed

async def asyncio_detailed(
    user_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ScimGetUserResponse200]:
    """ Gets a user using the provided user name.

    Args:
        user_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimGetUserResponse200]
     """


    kwargs = _get_kwargs(
        user_name=user_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    user_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ScimGetUserResponse200]:
    """ Gets a user using the provided user name.

    Args:
        user_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimGetUserResponse200
     """


    return (await asyncio_detailed(
        user_name=user_name,
client=client,

    )).parsed
