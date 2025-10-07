from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_unit_phase_bit_response_200 import ProductionUnitPhaseBitResponse200
from typing import cast



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    phase_bit: int,
    clear_bit: bool,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["SerialNumber"] = serial_number

    params["PartNumber"] = part_number

    params["PhaseBit"] = phase_bit

    params["ClearBit"] = clear_bit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Production/UnitPhaseBit",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionUnitPhaseBitResponse200]:
    if response.status_code == 200:
        response_200 = ProductionUnitPhaseBitResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionUnitPhaseBitResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    phase_bit: int,
    clear_bit: bool,

) -> Response[ProductionUnitPhaseBitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase_bit (int):
        clear_bit (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionUnitPhaseBitResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase_bit=phase_bit,
clear_bit=clear_bit,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    phase_bit: int,
    clear_bit: bool,

) -> Optional[ProductionUnitPhaseBitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase_bit (int):
        clear_bit (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionUnitPhaseBitResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase_bit=phase_bit,
clear_bit=clear_bit,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    phase_bit: int,
    clear_bit: bool,

) -> Response[ProductionUnitPhaseBitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase_bit (int):
        clear_bit (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionUnitPhaseBitResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase_bit=phase_bit,
clear_bit=clear_bit,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    phase_bit: int,
    clear_bit: bool,

) -> Optional[ProductionUnitPhaseBitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase_bit (int):
        clear_bit (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionUnitPhaseBitResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase_bit=phase_bit,
clear_bit=clear_bit,

    )).parsed
