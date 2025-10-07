from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...types import UNSET, Unset
from typing import Union



def _get_kwargs(
    identifier: str,
    *,
    reset: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["reset"] = reset


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Auth/GetToken/{identifier}".format(identifier=identifier,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    reset: Union[Unset, bool] = UNSET,

) -> Response[Any]:
    """  Creat and return a new access token with a specific identifier

     You will get access to the WATS API by specifying the Authorization header together with the
    returned token.

     The token is visible only once, please store it secure.

     Specify the reset flag to create a new token (the old one is no longer valid).

    ‏‏‎ ‎

     Ex.

     Authorization: Basic ReturnedToken

    Args:
        identifier (str):
        reset (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        identifier=identifier,
reset=reset,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],
    reset: Union[Unset, bool] = UNSET,

) -> Response[Any]:
    """  Creat and return a new access token with a specific identifier

     You will get access to the WATS API by specifying the Authorization header together with the
    returned token.

     The token is visible only once, please store it secure.

     Specify the reset flag to create a new token (the old one is no longer valid).

    ‏‏‎ ‎

     Ex.

     Authorization: Basic ReturnedToken

    Args:
        identifier (str):
        reset (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        identifier=identifier,
reset=reset,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

