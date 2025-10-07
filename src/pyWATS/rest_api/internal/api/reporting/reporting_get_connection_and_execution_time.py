from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.reporting_get_connection_and_execution_time_response_200 import ReportingGetConnectionAndExecutionTimeResponse200
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
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["minConnectionTime"] = min_connection_time

    params["maxConnectionTime"] = max_connection_time

    params["minExecutionTime"] = min_execution_time

    params["maxExecutionTime"] = max_execution_time


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Reporting/GetConnectionAndExecutionTime",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportingGetConnectionAndExecutionTimeResponse200]:
    if response.status_code == 200:
        response_200 = ReportingGetConnectionAndExecutionTimeResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportingGetConnectionAndExecutionTimeResponse200]:
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
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,

) -> Response[ReportingGetConnectionAndExecutionTimeResponse200]:
    """ Get connection and execution time results

    Args:
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
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
        Response[ReportingGetConnectionAndExecutionTimeResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,

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
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,

) -> Optional[ReportingGetConnectionAndExecutionTimeResponse200]:
    """ Get connection and execution time results

    Args:
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
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
        ReportingGetConnectionAndExecutionTimeResponse200
     """


    return sync_detailed(
        client=client,
body=body,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,

) -> Response[ReportingGetConnectionAndExecutionTimeResponse200]:
    """ Get connection and execution time results

    Args:
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
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
        Response[ReportingGetConnectionAndExecutionTimeResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,

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
    min_connection_time: Union[Unset, int] = UNSET,
    max_connection_time: Union[Unset, int] = UNSET,
    min_execution_time: Union[Unset, int] = UNSET,
    max_execution_time: Union[Unset, int] = UNSET,

) -> Optional[ReportingGetConnectionAndExecutionTimeResponse200]:
    """ Get connection and execution time results

    Args:
        min_connection_time (Union[Unset, int]):
        max_connection_time (Union[Unset, int]):
        min_execution_time (Union[Unset, int]):
        max_execution_time (Union[Unset, int]):
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
        ReportingGetConnectionAndExecutionTimeResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
min_connection_time=min_connection_time,
max_connection_time=max_connection_time,
min_execution_time=min_execution_time,
max_execution_time=max_execution_time,

    )).parsed
