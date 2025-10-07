from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.reporting_get_serial_number_history_response_200 import ReportingGetSerialNumberHistoryResponse200
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
    include_actions: Union[Unset, bool] = UNSET,
    strict_units: Union[Unset, bool] = UNSET,
    use_cache: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["includeActions"] = include_actions

    params["strictUnits"] = strict_units

    params["useCache"] = use_cache


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Reporting/GetSerialNumberHistory",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportingGetSerialNumberHistoryResponse200]:
    if response.status_code == 200:
        response_200 = ReportingGetSerialNumberHistoryResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportingGetSerialNumberHistoryResponse200]:
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
    include_actions: Union[Unset, bool] = UNSET,
    strict_units: Union[Unset, bool] = UNSET,
    use_cache: Union[Unset, bool] = UNSET,

) -> Response[ReportingGetSerialNumberHistoryResponse200]:
    """ 
    Args:
        include_actions (Union[Unset, bool]):
        strict_units (Union[Unset, bool]):
        use_cache (Union[Unset, bool]):
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
        Response[ReportingGetSerialNumberHistoryResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
include_actions=include_actions,
strict_units=strict_units,
use_cache=use_cache,

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
    include_actions: Union[Unset, bool] = UNSET,
    strict_units: Union[Unset, bool] = UNSET,
    use_cache: Union[Unset, bool] = UNSET,

) -> Optional[ReportingGetSerialNumberHistoryResponse200]:
    """ 
    Args:
        include_actions (Union[Unset, bool]):
        strict_units (Union[Unset, bool]):
        use_cache (Union[Unset, bool]):
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
        ReportingGetSerialNumberHistoryResponse200
     """


    return sync_detailed(
        client=client,
body=body,
include_actions=include_actions,
strict_units=strict_units,
use_cache=use_cache,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    include_actions: Union[Unset, bool] = UNSET,
    strict_units: Union[Unset, bool] = UNSET,
    use_cache: Union[Unset, bool] = UNSET,

) -> Response[ReportingGetSerialNumberHistoryResponse200]:
    """ 
    Args:
        include_actions (Union[Unset, bool]):
        strict_units (Union[Unset, bool]):
        use_cache (Union[Unset, bool]):
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
        Response[ReportingGetSerialNumberHistoryResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
include_actions=include_actions,
strict_units=strict_units,
use_cache=use_cache,

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
    include_actions: Union[Unset, bool] = UNSET,
    strict_units: Union[Unset, bool] = UNSET,
    use_cache: Union[Unset, bool] = UNSET,

) -> Optional[ReportingGetSerialNumberHistoryResponse200]:
    """ 
    Args:
        include_actions (Union[Unset, bool]):
        strict_units (Union[Unset, bool]):
        use_cache (Union[Unset, bool]):
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
        ReportingGetSerialNumberHistoryResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
include_actions=include_actions,
strict_units=strict_units,
use_cache=use_cache,

    )).parsed
