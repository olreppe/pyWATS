from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_mobile_app_token_response_200 import AuthMobileAppTokenResponse200
from typing import cast



def _get_kwargs(
    *,
    device_id: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["deviceId"] = device_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/auth/MobileAppToken",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AuthMobileAppTokenResponse200]:
    if response.status_code == 200:
        response_200 = AuthMobileAppTokenResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AuthMobileAppTokenResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    device_id: str,

) -> Response[AuthMobileAppTokenResponse200]:
    """ Retrive a token for the mobile app

    Args:
        device_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthMobileAppTokenResponse200]
     """


    kwargs = _get_kwargs(
        device_id=device_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    device_id: str,

) -> Optional[AuthMobileAppTokenResponse200]:
    """ Retrive a token for the mobile app

    Args:
        device_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthMobileAppTokenResponse200
     """


    return sync_detailed(
        client=client,
device_id=device_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    device_id: str,

) -> Response[AuthMobileAppTokenResponse200]:
    """ Retrive a token for the mobile app

    Args:
        device_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthMobileAppTokenResponse200]
     """


    kwargs = _get_kwargs(
        device_id=device_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    device_id: str,

) -> Optional[AuthMobileAppTokenResponse200]:
    """ Retrive a token for the mobile app

    Args:
        device_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthMobileAppTokenResponse200
     """


    return (await asyncio_detailed(
        client=client,
device_id=device_id,

    )).parsed
