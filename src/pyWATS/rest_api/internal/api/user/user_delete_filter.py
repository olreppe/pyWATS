from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user_delete_filter_response_200 import UserDeleteFilterResponse200
from typing import cast



def _get_kwargs(
    *,
    filter_name: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["filterName"] = filter_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/User/DeleteFilter",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UserDeleteFilterResponse200]:
    if response.status_code == 200:
        response_200 = UserDeleteFilterResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UserDeleteFilterResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    filter_name: str,

) -> Response[UserDeleteFilterResponse200]:
    """ Deletes a filter for the currently logged in user.

    Args:
        filter_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDeleteFilterResponse200]
     """


    kwargs = _get_kwargs(
        filter_name=filter_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    filter_name: str,

) -> Optional[UserDeleteFilterResponse200]:
    """ Deletes a filter for the currently logged in user.

    Args:
        filter_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDeleteFilterResponse200
     """


    return sync_detailed(
        client=client,
filter_name=filter_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    filter_name: str,

) -> Response[UserDeleteFilterResponse200]:
    """ Deletes a filter for the currently logged in user.

    Args:
        filter_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDeleteFilterResponse200]
     """


    kwargs = _get_kwargs(
        filter_name=filter_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    filter_name: str,

) -> Optional[UserDeleteFilterResponse200]:
    """ Deletes a filter for the currently logged in user.

    Args:
        filter_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDeleteFilterResponse200
     """


    return (await asyncio_detailed(
        client=client,
filter_name=filter_name,

    )).parsed
