from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user_delete_users_response_200 import UserDeleteUsersResponse200
from typing import cast



def _get_kwargs(
    *,
    user_ids: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["userIds"] = user_ids


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/User/DeleteUsers",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UserDeleteUsersResponse200]:
    if response.status_code == 200:
        response_200 = UserDeleteUsersResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UserDeleteUsersResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    user_ids: str,

) -> Response[UserDeleteUsersResponse200]:
    """ 
    Args:
        user_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDeleteUsersResponse200]
     """


    kwargs = _get_kwargs(
        user_ids=user_ids,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    user_ids: str,

) -> Optional[UserDeleteUsersResponse200]:
    """ 
    Args:
        user_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDeleteUsersResponse200
     """


    return sync_detailed(
        client=client,
user_ids=user_ids,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    user_ids: str,

) -> Response[UserDeleteUsersResponse200]:
    """ 
    Args:
        user_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDeleteUsersResponse200]
     """


    kwargs = _get_kwargs(
        user_ids=user_ids,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    user_ids: str,

) -> Optional[UserDeleteUsersResponse200]:
    """ 
    Args:
        user_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDeleteUsersResponse200
     """


    return (await asyncio_detailed(
        client=client,
user_ids=user_ids,

    )).parsed
