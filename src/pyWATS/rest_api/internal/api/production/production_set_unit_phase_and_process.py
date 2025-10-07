from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_set_unit_phase_and_process_response_200 import ProductionSetUnitPhaseAndProcessResponse200
from typing import cast



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    phase: int,
    process_name: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["SerialNumber"] = serial_number

    params["PartNumber"] = part_number

    params["Phase"] = phase

    params["ProcessName"] = process_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Production/SetUnitPhaseAndProcess",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionSetUnitPhaseAndProcessResponse200]:
    if response.status_code == 200:
        response_200 = ProductionSetUnitPhaseAndProcessResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionSetUnitPhaseAndProcessResponse200]:
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
    phase: int,
    process_name: str,

) -> Response[ProductionSetUnitPhaseAndProcessResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase (int):
        process_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionSetUnitPhaseAndProcessResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase=phase,
process_name=process_name,

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
    phase: int,
    process_name: str,

) -> Optional[ProductionSetUnitPhaseAndProcessResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase (int):
        process_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionSetUnitPhaseAndProcessResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase=phase,
process_name=process_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    phase: int,
    process_name: str,

) -> Response[ProductionSetUnitPhaseAndProcessResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase (int):
        process_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionSetUnitPhaseAndProcessResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase=phase,
process_name=process_name,

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
    phase: int,
    process_name: str,

) -> Optional[ProductionSetUnitPhaseAndProcessResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        phase (int):
        process_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionSetUnitPhaseAndProcessResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase=phase,
process_name=process_name,

    )).parsed
