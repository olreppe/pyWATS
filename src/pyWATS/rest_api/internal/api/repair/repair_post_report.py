from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.repair_post_report_response_200 import RepairPostReportResponse200
from ...models.virinco_wats_schemas_wsjf_report import VirincoWATSSchemasWSJFReport
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
    ],
    station_name: str,
    culture_code: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["stationName"] = station_name

    params["cultureCode"] = culture_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Internal/Repair",
        "params": params,
    }

    if isinstance(body, VirincoWATSSchemasWSJFReport):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSSchemasWSJFReport):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSSchemasWSJFReport):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[RepairPostReportResponse200]:
    if response.status_code == 200:
        response_200 = RepairPostReportResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[RepairPostReportResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
    ],
    station_name: str,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[RepairPostReportResponse200]:
    """ 
    Args:
        station_name (str):
        culture_code (Union[Unset, str]):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairPostReportResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
station_name=station_name,
culture_code=culture_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
    ],
    station_name: str,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[RepairPostReportResponse200]:
    """ 
    Args:
        station_name (str):
        culture_code (Union[Unset, str]):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairPostReportResponse200
     """


    return sync_detailed(
        client=client,
body=body,
station_name=station_name,
culture_code=culture_code,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
    ],
    station_name: str,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[RepairPostReportResponse200]:
    """ 
    Args:
        station_name (str):
        culture_code (Union[Unset, str]):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairPostReportResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
station_name=station_name,
culture_code=culture_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
        VirincoWATSSchemasWSJFReport,
    ],
    station_name: str,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[RepairPostReportResponse200]:
    """ 
    Args:
        station_name (str):
        culture_code (Union[Unset, str]):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):
        body (VirincoWATSSchemasWSJFReport):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairPostReportResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
station_name=station_name,
culture_code=culture_code,

    )).parsed
