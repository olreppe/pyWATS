from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.scim_get_jwt_response_200 import ScimGetJWTResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    duration: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["duration"] = duration


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/SCIM/v2/Token",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ScimGetJWTResponse200]:
    if response.status_code == 200:
        response_200 = ScimGetJWTResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ScimGetJWTResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    duration: Union[Unset, int] = UNSET,

) -> Response[ScimGetJWTResponse200]:
    """ Creates a Json Web Token to be used with automatic provisioning from Azure.
    Provided with duration, you can specify the amount of days until the token expires and will need to
    have a new one generated.
    The default duration is set to 90 days.

     Due to security reasons, we recommend leaving the duration to default. If you still wish
    to increase the duration, you do so at your own risk.

    Args:
        duration (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimGetJWTResponse200]
     """


    kwargs = _get_kwargs(
        duration=duration,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    duration: Union[Unset, int] = UNSET,

) -> Optional[ScimGetJWTResponse200]:
    """ Creates a Json Web Token to be used with automatic provisioning from Azure.
    Provided with duration, you can specify the amount of days until the token expires and will need to
    have a new one generated.
    The default duration is set to 90 days.

     Due to security reasons, we recommend leaving the duration to default. If you still wish
    to increase the duration, you do so at your own risk.

    Args:
        duration (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimGetJWTResponse200
     """


    return sync_detailed(
        client=client,
duration=duration,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    duration: Union[Unset, int] = UNSET,

) -> Response[ScimGetJWTResponse200]:
    """ Creates a Json Web Token to be used with automatic provisioning from Azure.
    Provided with duration, you can specify the amount of days until the token expires and will need to
    have a new one generated.
    The default duration is set to 90 days.

     Due to security reasons, we recommend leaving the duration to default. If you still wish
    to increase the duration, you do so at your own risk.

    Args:
        duration (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimGetJWTResponse200]
     """


    kwargs = _get_kwargs(
        duration=duration,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    duration: Union[Unset, int] = UNSET,

) -> Optional[ScimGetJWTResponse200]:
    """ Creates a Json Web Token to be used with automatic provisioning from Azure.
    Provided with duration, you can specify the amount of days until the token expires and will need to
    have a new one generated.
    The default duration is set to 90 days.

     Due to security reasons, we recommend leaving the duration to default. If you still wish
    to increase the duration, you do so at your own risk.

    Args:
        duration (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimGetJWTResponse200
     """


    return (await asyncio_detailed(
        client=client,
duration=duration,

    )).parsed
