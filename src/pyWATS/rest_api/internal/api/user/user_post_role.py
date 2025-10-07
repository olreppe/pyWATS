from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user_post_role_response_200 import UserPostRoleResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        str,
        str,
        str,
    ],
    headless: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["headless"] = headless


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/User/PostRole",
        "params": params,
    }

    if isinstance(body, str):
        _kwargs["json"] = body


        headers["Content-Type"] = "application/json"
    if isinstance(body, str):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, str):
        _kwargs["json"] = body


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UserPostRoleResponse200]:
    if response.status_code == 200:
        response_200 = UserPostRoleResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UserPostRoleResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],
    headless: Union[Unset, bool] = UNSET,

) -> Response[UserPostRoleResponse200]:
    """ 
    Args:
        headless (Union[Unset, bool]):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPostRoleResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
headless=headless,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],
    headless: Union[Unset, bool] = UNSET,

) -> Optional[UserPostRoleResponse200]:
    """ 
    Args:
        headless (Union[Unset, bool]):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPostRoleResponse200
     """


    return sync_detailed(
        client=client,
body=body,
headless=headless,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],
    headless: Union[Unset, bool] = UNSET,

) -> Response[UserPostRoleResponse200]:
    """ 
    Args:
        headless (Union[Unset, bool]):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPostRoleResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
headless=headless,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],
    headless: Union[Unset, bool] = UNSET,

) -> Optional[UserPostRoleResponse200]:
    """ 
    Args:
        headless (Union[Unset, bool]):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPostRoleResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
headless=headless,

    )).parsed
