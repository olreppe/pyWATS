from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.repair_put_report_data_body import RepairPutReportDataBody
from ...models.repair_put_report_json_body import RepairPutReportJsonBody
from ...models.repair_put_report_response_200 import RepairPutReportResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        RepairPutReportJsonBody,
        RepairPutReportDataBody,
    ],
    station_name: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["stationName"] = station_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/Internal/Repair",
        "params": params,
    }

    if isinstance(body, RepairPutReportJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, RepairPutReportDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[RepairPutReportResponse200]:
    if response.status_code == 200:
        response_200 = RepairPutReportResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[RepairPutReportResponse200]:
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
        RepairPutReportJsonBody,
        RepairPutReportDataBody,
    ],
    station_name: str,

) -> Response[RepairPutReportResponse200]:
    """ 
    Args:
        station_name (str):
        body (RepairPutReportJsonBody):
        body (RepairPutReportDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairPutReportResponse200]
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
        RepairPutReportJsonBody,
        RepairPutReportDataBody,
    ],
    station_name: str,

) -> Optional[RepairPutReportResponse200]:
    """ 
    Args:
        station_name (str):
        body (RepairPutReportJsonBody):
        body (RepairPutReportDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairPutReportResponse200
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
        RepairPutReportJsonBody,
        RepairPutReportDataBody,
    ],
    station_name: str,

) -> Response[RepairPutReportResponse200]:
    """ 
    Args:
        station_name (str):
        body (RepairPutReportJsonBody):
        body (RepairPutReportDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairPutReportResponse200]
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
        RepairPutReportJsonBody,
        RepairPutReportDataBody,
    ],
    station_name: str,

) -> Optional[RepairPutReportResponse200]:
    """ 
    Args:
        station_name (str):
        body (RepairPutReportJsonBody):
        body (RepairPutReportDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairPutReportResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
station_name=station_name,

    )).parsed
