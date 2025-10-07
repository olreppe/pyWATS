from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_create_unit_response_200 import ProductionCreateUnitResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    revision: str,
    batch_number: Union[Unset, str] = UNSET,
    unit_phase: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["revision"] = revision

    params["batchNumber"] = batch_number

    params["unitPhase"] = unit_phase


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Production/CreateUnit",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionCreateUnitResponse200]:
    if response.status_code == 200:
        response_200 = ProductionCreateUnitResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionCreateUnitResponse200]:
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
    revision: str,
    batch_number: Union[Unset, str] = UNSET,
    unit_phase: Union[Unset, int] = UNSET,

) -> Response[ProductionCreateUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        revision (str):
        batch_number (Union[Unset, str]):
        unit_phase (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionCreateUnitResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
revision=revision,
batch_number=batch_number,
unit_phase=unit_phase,

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
    revision: str,
    batch_number: Union[Unset, str] = UNSET,
    unit_phase: Union[Unset, int] = UNSET,

) -> Optional[ProductionCreateUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        revision (str):
        batch_number (Union[Unset, str]):
        unit_phase (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionCreateUnitResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
revision=revision,
batch_number=batch_number,
unit_phase=unit_phase,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    revision: str,
    batch_number: Union[Unset, str] = UNSET,
    unit_phase: Union[Unset, int] = UNSET,

) -> Response[ProductionCreateUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        revision (str):
        batch_number (Union[Unset, str]):
        unit_phase (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionCreateUnitResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
revision=revision,
batch_number=batch_number,
unit_phase=unit_phase,

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
    revision: str,
    batch_number: Union[Unset, str] = UNSET,
    unit_phase: Union[Unset, int] = UNSET,

) -> Optional[ProductionCreateUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        revision (str):
        batch_number (Union[Unset, str]):
        unit_phase (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionCreateUnitResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
revision=revision,
batch_number=batch_number,
unit_phase=unit_phase,

    )).parsed
