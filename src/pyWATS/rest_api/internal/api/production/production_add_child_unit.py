from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_add_child_unit_response_200 import ProductionAddChildUnitResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,
    culture_code: str,
    check_phase: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["childSerialNumber"] = child_serial_number

    params["childPartNumber"] = child_part_number

    params["checkPartNumber"] = check_part_number

    params["checkRevision"] = check_revision

    params["cultureCode"] = culture_code

    params["checkPhase"] = check_phase


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Production/AddChildUnit",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionAddChildUnitResponse200]:
    if response.status_code == 200:
        response_200 = ProductionAddChildUnitResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionAddChildUnitResponse200]:
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
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,
    culture_code: str,
    check_phase: Union[Unset, bool] = UNSET,

) -> Response[ProductionAddChildUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        culture_code (str):
        check_phase (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionAddChildUnitResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,
culture_code=culture_code,
check_phase=check_phase,

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
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,
    culture_code: str,
    check_phase: Union[Unset, bool] = UNSET,

) -> Optional[ProductionAddChildUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        culture_code (str):
        check_phase (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionAddChildUnitResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,
culture_code=culture_code,
check_phase=check_phase,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,
    culture_code: str,
    check_phase: Union[Unset, bool] = UNSET,

) -> Response[ProductionAddChildUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        culture_code (str):
        check_phase (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionAddChildUnitResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,
culture_code=culture_code,
check_phase=check_phase,

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
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,
    culture_code: str,
    check_phase: Union[Unset, bool] = UNSET,

) -> Optional[ProductionAddChildUnitResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        culture_code (str):
        check_phase (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionAddChildUnitResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,
culture_code=culture_code,
check_phase=check_phase,

    )).parsed
