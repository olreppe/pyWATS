from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_take_serial_numbers_response_200 import ProductionTakeSerialNumbersResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number_type: str,
    quantity: int,
    ref_sn: Union[Unset, str] = UNSET,
    ref_pn: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    only_in_sequence: Union[Unset, bool] = UNSET,
    format_: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumberType"] = serial_number_type

    params["quantity"] = quantity

    params["refSN"] = ref_sn

    params["refPN"] = ref_pn

    params["stationName"] = station_name

    params["onlyInSequence"] = only_in_sequence

    params["format"] = format_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Production/SerialNumbers/Take",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionTakeSerialNumbersResponse200]:
    if response.status_code == 200:
        response_200 = ProductionTakeSerialNumbersResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionTakeSerialNumbersResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    quantity: int,
    ref_sn: Union[Unset, str] = UNSET,
    ref_pn: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    only_in_sequence: Union[Unset, bool] = UNSET,
    format_: Union[Unset, str] = UNSET,

) -> Response[ProductionTakeSerialNumbersResponse200]:
    """ Take free serial numbers and return them in either XML or CSV format.

    Args:
        serial_number_type (str):
        quantity (int):
        ref_sn (Union[Unset, str]):
        ref_pn (Union[Unset, str]):
        station_name (Union[Unset, str]):
        only_in_sequence (Union[Unset, bool]):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionTakeSerialNumbersResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
quantity=quantity,
ref_sn=ref_sn,
ref_pn=ref_pn,
station_name=station_name,
only_in_sequence=only_in_sequence,
format_=format_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    quantity: int,
    ref_sn: Union[Unset, str] = UNSET,
    ref_pn: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    only_in_sequence: Union[Unset, bool] = UNSET,
    format_: Union[Unset, str] = UNSET,

) -> Optional[ProductionTakeSerialNumbersResponse200]:
    """ Take free serial numbers and return them in either XML or CSV format.

    Args:
        serial_number_type (str):
        quantity (int):
        ref_sn (Union[Unset, str]):
        ref_pn (Union[Unset, str]):
        station_name (Union[Unset, str]):
        only_in_sequence (Union[Unset, bool]):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionTakeSerialNumbersResponse200
     """


    return sync_detailed(
        client=client,
serial_number_type=serial_number_type,
quantity=quantity,
ref_sn=ref_sn,
ref_pn=ref_pn,
station_name=station_name,
only_in_sequence=only_in_sequence,
format_=format_,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    quantity: int,
    ref_sn: Union[Unset, str] = UNSET,
    ref_pn: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    only_in_sequence: Union[Unset, bool] = UNSET,
    format_: Union[Unset, str] = UNSET,

) -> Response[ProductionTakeSerialNumbersResponse200]:
    """ Take free serial numbers and return them in either XML or CSV format.

    Args:
        serial_number_type (str):
        quantity (int):
        ref_sn (Union[Unset, str]):
        ref_pn (Union[Unset, str]):
        station_name (Union[Unset, str]):
        only_in_sequence (Union[Unset, bool]):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionTakeSerialNumbersResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
quantity=quantity,
ref_sn=ref_sn,
ref_pn=ref_pn,
station_name=station_name,
only_in_sequence=only_in_sequence,
format_=format_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    quantity: int,
    ref_sn: Union[Unset, str] = UNSET,
    ref_pn: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    only_in_sequence: Union[Unset, bool] = UNSET,
    format_: Union[Unset, str] = UNSET,

) -> Optional[ProductionTakeSerialNumbersResponse200]:
    """ Take free serial numbers and return them in either XML or CSV format.

    Args:
        serial_number_type (str):
        quantity (int):
        ref_sn (Union[Unset, str]):
        ref_pn (Union[Unset, str]):
        station_name (Union[Unset, str]):
        only_in_sequence (Union[Unset, bool]):
        format_ (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionTakeSerialNumbersResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number_type=serial_number_type,
quantity=quantity,
ref_sn=ref_sn,
ref_pn=ref_pn,
station_name=station_name,
only_in_sequence=only_in_sequence,
format_=format_,

    )).parsed
