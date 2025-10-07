from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.repair_submit_unsubmitted_repair_reports_response_200 import RepairSubmitUnsubmittedRepairReportsResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    station_name: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["stationName"] = station_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Repair/SubmitUnsubmittedRepairReports",
        "params": params,
    }

    if isinstance(body, list[str]):
        _kwargs["json"] = body




        headers["Content-Type"] = "application/json"
    if isinstance(body, list[str]):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list[str]):
        _kwargs["json"] = body




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[RepairSubmitUnsubmittedRepairReportsResponse200]:
    if response.status_code == 200:
        response_200 = RepairSubmitUnsubmittedRepairReportsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[RepairSubmitUnsubmittedRepairReportsResponse200]:
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
        list[str],
        list[str],
        list[str],
    ],
    station_name: str,

) -> Response[RepairSubmitUnsubmittedRepairReportsResponse200]:
    """ 
    Args:
        station_name (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairSubmitUnsubmittedRepairReportsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
station_name=station_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    station_name: str,

) -> Optional[RepairSubmitUnsubmittedRepairReportsResponse200]:
    """ 
    Args:
        station_name (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairSubmitUnsubmittedRepairReportsResponse200
     """


    return sync_detailed(
        client=client,
body=body,
station_name=station_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    station_name: str,

) -> Response[RepairSubmitUnsubmittedRepairReportsResponse200]:
    """ 
    Args:
        station_name (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairSubmitUnsubmittedRepairReportsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
station_name=station_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    station_name: str,

) -> Optional[RepairSubmitUnsubmittedRepairReportsResponse200]:
    """ 
    Args:
        station_name (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairSubmitUnsubmittedRepairReportsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
station_name=station_name,

    )).parsed
