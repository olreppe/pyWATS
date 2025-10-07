from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_get_serial_number_stats_response_200 import ProductionGetSerialNumberStatsResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number_type: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumberType"] = serial_number_type


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Production/SerialNumbers/Statistics",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionGetSerialNumberStatsResponse200]:
    if response.status_code == 200:
        response_200 = ProductionGetSerialNumberStatsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionGetSerialNumberStatsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: Union[Unset, str] = UNSET,

) -> Response[ProductionGetSerialNumberStatsResponse200]:
    """ Gets statistic for a given serial number type

    Args:
        serial_number_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionGetSerialNumberStatsResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: Union[Unset, str] = UNSET,

) -> Optional[ProductionGetSerialNumberStatsResponse200]:
    """ Gets statistic for a given serial number type

    Args:
        serial_number_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionGetSerialNumberStatsResponse200
     """


    return sync_detailed(
        client=client,
serial_number_type=serial_number_type,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: Union[Unset, str] = UNSET,

) -> Response[ProductionGetSerialNumberStatsResponse200]:
    """ Gets statistic for a given serial number type

    Args:
        serial_number_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionGetSerialNumberStatsResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: Union[Unset, str] = UNSET,

) -> Optional[ProductionGetSerialNumberStatsResponse200]:
    """ Gets statistic for a given serial number type

    Args:
        serial_number_type (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionGetSerialNumberStatsResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number_type=serial_number_type,

    )).parsed
