from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.report_get_report_as_wsjf_response_200 import ReportGetReportAsWSJFResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    detail_level: Union[Unset, int] = UNSET,
    include_chartdata: Union[Unset, bool] = UNSET,
    include_attachments: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["detailLevel"] = detail_level

    params["includeChartdata"] = include_chartdata

    params["includeAttachments"] = include_attachments


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Report/Wsjf/{id}".format(id=id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportGetReportAsWSJFResponse200]:
    if response.status_code == 200:
        response_200 = ReportGetReportAsWSJFResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportGetReportAsWSJFResponse200]:
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
    detail_level: Union[Unset, int] = UNSET,
    include_chartdata: Union[Unset, bool] = UNSET,
    include_attachments: Union[Unset, bool] = UNSET,

) -> Response[ReportGetReportAsWSJFResponse200]:
    r""" Return a report in WSJF (Wats Standard JSON Format).

     See <a target=\"_blank\" href=\"https://support.virinco.com/hc/en-us/articles/360015705199\">Details
    about the WSJF format.</a>

    Args:
        id (UUID):
        detail_level (Union[Unset, int]):
        include_chartdata (Union[Unset, bool]):
        include_attachments (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetReportAsWSJFResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
detail_level=detail_level,
include_chartdata=include_chartdata,
include_attachments=include_attachments,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    detail_level: Union[Unset, int] = UNSET,
    include_chartdata: Union[Unset, bool] = UNSET,
    include_attachments: Union[Unset, bool] = UNSET,

) -> Optional[ReportGetReportAsWSJFResponse200]:
    r""" Return a report in WSJF (Wats Standard JSON Format).

     See <a target=\"_blank\" href=\"https://support.virinco.com/hc/en-us/articles/360015705199\">Details
    about the WSJF format.</a>

    Args:
        id (UUID):
        detail_level (Union[Unset, int]):
        include_chartdata (Union[Unset, bool]):
        include_attachments (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetReportAsWSJFResponse200
     """


    return sync_detailed(
        id=id,
client=client,
detail_level=detail_level,
include_chartdata=include_chartdata,
include_attachments=include_attachments,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    detail_level: Union[Unset, int] = UNSET,
    include_chartdata: Union[Unset, bool] = UNSET,
    include_attachments: Union[Unset, bool] = UNSET,

) -> Response[ReportGetReportAsWSJFResponse200]:
    r""" Return a report in WSJF (Wats Standard JSON Format).

     See <a target=\"_blank\" href=\"https://support.virinco.com/hc/en-us/articles/360015705199\">Details
    about the WSJF format.</a>

    Args:
        id (UUID):
        detail_level (Union[Unset, int]):
        include_chartdata (Union[Unset, bool]):
        include_attachments (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetReportAsWSJFResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
detail_level=detail_level,
include_chartdata=include_chartdata,
include_attachments=include_attachments,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    detail_level: Union[Unset, int] = UNSET,
    include_chartdata: Union[Unset, bool] = UNSET,
    include_attachments: Union[Unset, bool] = UNSET,

) -> Optional[ReportGetReportAsWSJFResponse200]:
    r""" Return a report in WSJF (Wats Standard JSON Format).

     See <a target=\"_blank\" href=\"https://support.virinco.com/hc/en-us/articles/360015705199\">Details
    about the WSJF format.</a>

    Args:
        id (UUID):
        detail_level (Union[Unset, int]):
        include_chartdata (Union[Unset, bool]):
        include_attachments (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetReportAsWSJFResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
detail_level=detail_level,
include_chartdata=include_chartdata,
include_attachments=include_attachments,

    )).parsed
