from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.report_get_chart_data_response_200 import ReportGetChartDataResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    step_order_number: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["stepOrderNumber"] = step_order_number


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Report/GetChartData/{id}".format(id=id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportGetChartDataResponse200]:
    if response.status_code == 200:
        response_200 = ReportGetChartDataResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportGetChartDataResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    step_order_number: int,

) -> Response[ReportGetChartDataResponse200]:
    """ 
    Args:
        id (UUID):
        step_order_number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetChartDataResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
step_order_number=step_order_number,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    step_order_number: int,

) -> Optional[ReportGetChartDataResponse200]:
    """ 
    Args:
        id (UUID):
        step_order_number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetChartDataResponse200
     """


    return sync_detailed(
        id=id,
client=client,
step_order_number=step_order_number,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    step_order_number: int,

) -> Response[ReportGetChartDataResponse200]:
    """ 
    Args:
        id (UUID):
        step_order_number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetChartDataResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
step_order_number=step_order_number,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    step_order_number: int,

) -> Optional[ReportGetChartDataResponse200]:
    """ 
    Args:
        id (UUID):
        step_order_number (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetChartDataResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
step_order_number=step_order_number,

    )).parsed
