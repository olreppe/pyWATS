from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_set_unit_phase_public_response_200 import ProductionSetUnitPhasePublicResponse200
from typing import cast



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    phase: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["phase"] = phase


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/Production/SetUnitPhase",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionSetUnitPhasePublicResponse200]:
    if response.status_code == 200:
        response_200 = ProductionSetUnitPhasePublicResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionSetUnitPhasePublicResponse200]:
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

) -> Response[ProductionSetUnitPhasePublicResponse200]:
    r""" Set a unit's current phase.

     Set a unit's current phase.

    Phases:
    - 1: \"Unknown unit phase\"
    - 2: \"Unit is under production\"
    - 4: \"Unit is being repaired\"
    - 8: \"Unit is being repaired for service (RMA)\"
    - 16: \"Unit is finalized\"
    - 32: \"Unit is scrapped\"
    - 64: \"Unit is under extended test\"
    - 128: \"Unit is under customization\"
    - 256: \"Unit has been repaired\"
    - 512: \"Unit is marked as missing\"
    - 1024: \"Unit is in store (warehouse)\"
    - 2048: \"Unit is shipped (out of factory)\"
    - 4098: \"Unit is under production in a queue\"
    - 4100: \"Unit is waiting for production repair\"
    - 4104: \"Unit is waiting for service repair (RMA)\"

    Args:
        serial_number (str):
        part_number (str):
        phase (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionSetUnitPhasePublicResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase=phase,

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

) -> Optional[ProductionSetUnitPhasePublicResponse200]:
    r""" Set a unit's current phase.

     Set a unit's current phase.

    Phases:
    - 1: \"Unknown unit phase\"
    - 2: \"Unit is under production\"
    - 4: \"Unit is being repaired\"
    - 8: \"Unit is being repaired for service (RMA)\"
    - 16: \"Unit is finalized\"
    - 32: \"Unit is scrapped\"
    - 64: \"Unit is under extended test\"
    - 128: \"Unit is under customization\"
    - 256: \"Unit has been repaired\"
    - 512: \"Unit is marked as missing\"
    - 1024: \"Unit is in store (warehouse)\"
    - 2048: \"Unit is shipped (out of factory)\"
    - 4098: \"Unit is under production in a queue\"
    - 4100: \"Unit is waiting for production repair\"
    - 4104: \"Unit is waiting for service repair (RMA)\"

    Args:
        serial_number (str):
        part_number (str):
        phase (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionSetUnitPhasePublicResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase=phase,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    phase: int,

) -> Response[ProductionSetUnitPhasePublicResponse200]:
    r""" Set a unit's current phase.

     Set a unit's current phase.

    Phases:
    - 1: \"Unknown unit phase\"
    - 2: \"Unit is under production\"
    - 4: \"Unit is being repaired\"
    - 8: \"Unit is being repaired for service (RMA)\"
    - 16: \"Unit is finalized\"
    - 32: \"Unit is scrapped\"
    - 64: \"Unit is under extended test\"
    - 128: \"Unit is under customization\"
    - 256: \"Unit has been repaired\"
    - 512: \"Unit is marked as missing\"
    - 1024: \"Unit is in store (warehouse)\"
    - 2048: \"Unit is shipped (out of factory)\"
    - 4098: \"Unit is under production in a queue\"
    - 4100: \"Unit is waiting for production repair\"
    - 4104: \"Unit is waiting for service repair (RMA)\"

    Args:
        serial_number (str):
        part_number (str):
        phase (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionSetUnitPhasePublicResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
phase=phase,

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

) -> Optional[ProductionSetUnitPhasePublicResponse200]:
    r""" Set a unit's current phase.

     Set a unit's current phase.

    Phases:
    - 1: \"Unknown unit phase\"
    - 2: \"Unit is under production\"
    - 4: \"Unit is being repaired\"
    - 8: \"Unit is being repaired for service (RMA)\"
    - 16: \"Unit is finalized\"
    - 32: \"Unit is scrapped\"
    - 64: \"Unit is under extended test\"
    - 128: \"Unit is under customization\"
    - 256: \"Unit has been repaired\"
    - 512: \"Unit is marked as missing\"
    - 1024: \"Unit is in store (warehouse)\"
    - 2048: \"Unit is shipped (out of factory)\"
    - 4098: \"Unit is under production in a queue\"
    - 4100: \"Unit is waiting for production repair\"
    - 4104: \"Unit is waiting for service repair (RMA)\"

    Args:
        serial_number (str):
        part_number (str):
        phase (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionSetUnitPhasePublicResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
phase=phase,

    )).parsed
