from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.repair_get_report_response_200 import RepairGetReportResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    *,
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,
    revision: Union[Unset, str] = UNSET,
    process_code: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["revision"] = revision

    params["processCode"] = process_code

    params["stationName"] = station_name

    json_uuid: Union[Unset, str] = UNSET
    if not isinstance(uuid, Unset):
        json_uuid = str(uuid)
    params["uuid"] = json_uuid


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Internal/Repair",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[RepairGetReportResponse200]:
    if response.status_code == 200:
        response_200 = RepairGetReportResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[RepairGetReportResponse200]:
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
    revision: Union[Unset, str] = UNSET,
    process_code: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,

) -> Response[RepairGetReportResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        revision (Union[Unset, str]):
        process_code (Union[Unset, str]):
        station_name (Union[Unset, str]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairGetReportResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
revision=revision,
process_code=process_code,
station_name=station_name,
uuid=uuid,

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
    revision: Union[Unset, str] = UNSET,
    process_code: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,

) -> Optional[RepairGetReportResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        revision (Union[Unset, str]):
        process_code (Union[Unset, str]):
        station_name (Union[Unset, str]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairGetReportResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
revision=revision,
process_code=process_code,
station_name=station_name,
uuid=uuid,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: Union[Unset, str] = UNSET,
    revision: Union[Unset, str] = UNSET,
    process_code: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,

) -> Response[RepairGetReportResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        revision (Union[Unset, str]):
        process_code (Union[Unset, str]):
        station_name (Union[Unset, str]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairGetReportResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
revision=revision,
process_code=process_code,
station_name=station_name,
uuid=uuid,

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
    revision: Union[Unset, str] = UNSET,
    process_code: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    uuid: Union[Unset, UUID] = UNSET,

) -> Optional[RepairGetReportResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (Union[Unset, str]):
        revision (Union[Unset, str]):
        process_code (Union[Unset, str]):
        station_name (Union[Unset, str]):
        uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairGetReportResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
revision=revision,
process_code=process_code,
station_name=station_name,
uuid=uuid,

    )).parsed
