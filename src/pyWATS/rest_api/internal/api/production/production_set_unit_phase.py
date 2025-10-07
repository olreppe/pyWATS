from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_set_unit_phase_response_200 import ProductionSetUnitPhaseResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,
    phase: Union[Unset, int] = UNSET,
    set_phase_on_sub_units: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["phase"] = phase

    params["setPhaseOnSubUnits"] = set_phase_on_sub_units


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Production/SetUnitPhase",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionSetUnitPhaseResponse200]:
    if response.status_code == 200:
        response_200 = ProductionSetUnitPhaseResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionSetUnitPhaseResponse200]:
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
    part_number: Union[Unset, str] = UNSET,
    phase: Union[Unset, int] = UNSET,
    set_phase_on_sub_units: Union[Unset, bool] = UNSET,

) -> Response[ProductionSetUnitPhaseResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        phase (Union[Unset, int]):
        set_phase_on_sub_units (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionSetUnitPhaseResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase=phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,
    phase: Union[Unset, int] = UNSET,
    set_phase_on_sub_units: Union[Unset, bool] = UNSET,

) -> Optional[ProductionSetUnitPhaseResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        phase (Union[Unset, int]):
        set_phase_on_sub_units (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionSetUnitPhaseResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase=phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,
    phase: Union[Unset, int] = UNSET,
    set_phase_on_sub_units: Union[Unset, bool] = UNSET,

) -> Response[ProductionSetUnitPhaseResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        phase (Union[Unset, int]):
        set_phase_on_sub_units (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionSetUnitPhaseResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase=phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,
    phase: Union[Unset, int] = UNSET,
    set_phase_on_sub_units: Union[Unset, bool] = UNSET,

) -> Optional[ProductionSetUnitPhaseResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        phase (Union[Unset, int]):
        set_phase_on_sub_units (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionSetUnitPhaseResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase=phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    )).parsed
