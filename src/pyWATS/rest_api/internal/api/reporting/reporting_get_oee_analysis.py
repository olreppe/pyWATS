from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.reporting_get_oee_analysis_response_200 import ReportingGetOeeAnalysisResponse200
from ...models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    available_time: str,
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,
    target_output: Union[Unset, float] = UNSET,
    is_export: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["availableTime"] = available_time

    params["minConnectionTime"] = min_connection_time

    params["maxConnectionTime"] = max_connection_time

    params["minExecutionTime"] = min_execution_time

    params["maxExecutionTime"] = max_execution_time

    params["targetOutput"] = target_output

    params["isExport"] = is_export


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Reporting/GetOeeAnalysis",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportingGetOeeAnalysisResponse200]:
    if response.status_code == 200:
        response_200 = ReportingGetOeeAnalysisResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportingGetOeeAnalysisResponse200]:
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
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    available_time: str,
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,
    target_output: Union[Unset, float] = UNSET,
    is_export: Union[Unset, bool] = UNSET,

) -> Response[ReportingGetOeeAnalysisResponse200]:
    """ 
    Args:
        available_time (str):
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
        target_output (Union[Unset, float]):
        is_export (Union[Unset, bool]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportingGetOeeAnalysisResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
available_time=available_time,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,
target_output=target_output,
is_export=is_export,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    available_time: str,
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,
    target_output: Union[Unset, float] = UNSET,
    is_export: Union[Unset, bool] = UNSET,

) -> Optional[ReportingGetOeeAnalysisResponse200]:
    """ 
    Args:
        available_time (str):
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
        target_output (Union[Unset, float]):
        is_export (Union[Unset, bool]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportingGetOeeAnalysisResponse200
     """


    return sync_detailed(
        client=client,
body=body,
available_time=available_time,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,
target_output=target_output,
is_export=is_export,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    available_time: str,
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,
    target_output: Union[Unset, float] = UNSET,
    is_export: Union[Unset, bool] = UNSET,

) -> Response[ReportingGetOeeAnalysisResponse200]:
    """ 
    Args:
        available_time (str):
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
        target_output (Union[Unset, float]):
        is_export (Union[Unset, bool]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportingGetOeeAnalysisResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
available_time=available_time,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,
target_output=target_output,
is_export=is_export,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    available_time: str,
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,
    target_output: Union[Unset, float] = UNSET,
    is_export: Union[Unset, bool] = UNSET,

) -> Optional[ReportingGetOeeAnalysisResponse200]:
    """ 
    Args:
        available_time (str):
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
        target_output (Union[Unset, float]):
        is_export (Union[Unset, bool]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportingGetOeeAnalysisResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
available_time=available_time,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,
target_output=target_output,
is_export=is_export,

    )).parsed
