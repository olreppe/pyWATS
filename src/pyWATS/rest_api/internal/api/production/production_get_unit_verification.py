from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_public_unit_verification_grade import VirincoWATSWebDashboardModelsPublicUnitVerificationGrade
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Production/UnitVerification",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebDashboardModelsPublicUnitVerificationGrade.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]:
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

) -> Response[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns its grade.

    Args:
        serial_number (str):
        part_number (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,

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

) -> Optional[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns its grade.

    Args:
        serial_number (str):
        part_number (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsPublicUnitVerificationGrade
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,

) -> Response[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns its grade.

    Args:
        serial_number (str):
        part_number (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,

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

) -> Optional[VirincoWATSWebDashboardModelsPublicUnitVerificationGrade]:
    """ Verifies the unit according to verification rules and returns its grade.

    Args:
        serial_number (str):
        part_number (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsPublicUnitVerificationGrade
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,

    )).parsed
