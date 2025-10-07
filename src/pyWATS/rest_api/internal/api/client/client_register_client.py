from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_register_client_response_200 import ClientRegisterClientResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    mac: str,
    name: str,
    location: Union[Unset, str] = UNSET,
    purpose: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    utc_offset: Union[Unset, float] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["mac"] = mac

    params["name"] = name

    params["location"] = location

    params["purpose"] = purpose

    params["description"] = description

    params["utcOffset"] = utc_offset


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Client/Register",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ClientRegisterClientResponse200]:
    if response.status_code == 200:
        response_200 = ClientRegisterClientResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ClientRegisterClientResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mac: str,
    name: str,
    location: Union[Unset, str] = UNSET,
    purpose: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    utc_offset: Union[Unset, float] = UNSET,

) -> Response[ClientRegisterClientResponse200]:
    """ 
    Args:
        mac (str):
        name (str):
        location (Union[Unset, str]):
        purpose (Union[Unset, str]):
        description (Union[Unset, str]):
        utc_offset (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientRegisterClientResponse200]
     """


    kwargs = _get_kwargs(
        mac=mac,
name=name,
location=location,
purpose=purpose,
description=description,
utc_offset=utc_offset,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    mac: str,
    name: str,
    location: Union[Unset, str] = UNSET,
    purpose: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    utc_offset: Union[Unset, float] = UNSET,

) -> Optional[ClientRegisterClientResponse200]:
    """ 
    Args:
        mac (str):
        name (str):
        location (Union[Unset, str]):
        purpose (Union[Unset, str]):
        description (Union[Unset, str]):
        utc_offset (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientRegisterClientResponse200
     """


    return sync_detailed(
        client=client,
mac=mac,
name=name,
location=location,
purpose=purpose,
description=description,
utc_offset=utc_offset,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    mac: str,
    name: str,
    location: Union[Unset, str] = UNSET,
    purpose: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    utc_offset: Union[Unset, float] = UNSET,

) -> Response[ClientRegisterClientResponse200]:
    """ 
    Args:
        mac (str):
        name (str):
        location (Union[Unset, str]):
        purpose (Union[Unset, str]):
        description (Union[Unset, str]):
        utc_offset (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientRegisterClientResponse200]
     """


    kwargs = _get_kwargs(
        mac=mac,
name=name,
location=location,
purpose=purpose,
description=description,
utc_offset=utc_offset,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    mac: str,
    name: str,
    location: Union[Unset, str] = UNSET,
    purpose: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    utc_offset: Union[Unset, float] = UNSET,

) -> Optional[ClientRegisterClientResponse200]:
    """ 
    Args:
        mac (str):
        name (str):
        location (Union[Unset, str]):
        purpose (Union[Unset, str]):
        description (Union[Unset, str]):
        utc_offset (Union[Unset, float]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientRegisterClientResponse200
     """


    return (await asyncio_detailed(
        client=client,
mac=mac,
name=name,
location=location,
purpose=purpose,
description=description,
utc_offset=utc_offset,

    )).parsed
