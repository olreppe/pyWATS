from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_unit_verification_grade import VirincoWATSWebDashboardModelsUnitVerificationGrade
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    include_subsites: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["includeSubsites"] = include_subsites


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/UnitVerification/GetUnitVerificationGrade",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebDashboardModelsUnitVerificationGrade]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebDashboardModelsUnitVerificationGrade.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebDashboardModelsUnitVerificationGrade]:
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
    include_subsites: Union[Unset, bool] = UNSET,

) -> Response[VirincoWATSWebDashboardModelsUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns it's grade

    Args:
        serial_number (str):
        part_number (str):
        include_subsites (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsUnitVerificationGrade]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
include_subsites=include_subsites,

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
    include_subsites: Union[Unset, bool] = UNSET,

) -> Optional[VirincoWATSWebDashboardModelsUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns it's grade

    Args:
        serial_number (str):
        part_number (str):
        include_subsites (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsUnitVerificationGrade
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
include_subsites=include_subsites,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    include_subsites: Union[Unset, bool] = UNSET,

) -> Response[VirincoWATSWebDashboardModelsUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns it's grade

    Args:
        serial_number (str):
        part_number (str):
        include_subsites (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsUnitVerificationGrade]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
include_subsites=include_subsites,

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
    include_subsites: Union[Unset, bool] = UNSET,

) -> Optional[VirincoWATSWebDashboardModelsUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns it's grade

    Args:
        serial_number (str):
        part_number (str):
        include_subsites (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsUnitVerificationGrade
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
include_subsites=include_subsites,

    )).parsed
