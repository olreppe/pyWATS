from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.app_dynamic_repair_response_200 import AppDynamicRepairResponse200
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
    dimensions: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["dimensions"] = dimensions


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/App/DynamicRepair",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AppDynamicRepairResponse200]:
    if response.status_code == 200:
        response_200 = AppDynamicRepairResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AppDynamicRepairResponse200]:
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
    dimensions: Union[Unset, str] = UNSET,

) -> Response[AppDynamicRepairResponse200]:
    r""" PREVIEW - Calculate repair statistics by custom dimensions.

     Please note that this endpoint is in preview and may be a subject to changes.

    Repair statistic calculated by custom dimensions defined in the dimensions filter. Multiple values
    are separated with semicolon (;).

    ```
    Supported dimensions:

    partNumber, revision, productName, productGroup, unitType, repairOperation, period, level,
    stationName, location, purpose,
    operator, miscInfoDescription, miscInfoString, repairCode, repairCategory, repairType, componentRef,
    componentNumber,
    componentRevision, componentVendor, componentDescription, functionBlock, referencedStep,
    referencedStepPath,
    testOperation, testPeriod, testLevel, testStationName, testLocation, testPurpose, testOperator,
    batchNumber, swFilename, swVersion
    ```

    The result is ordered by the order specified. Direction may be specified with direction hints (asc
    or desc).


    You may order the result by repair kpis

    ```
    Supported kpis:
    repairReportCount, repairCount
    ```


    Default filter:

    Top 10 partNumber/repairOperation combinations from the last 30 days.

    ```
    {
    \"topCount\":10,
    \"periodCount\":30,
    \"dateGrouping\":1,
    \"includeCurrentPeriod\":true,
    \"dimensions\" : \"repairCount desc;repairReportCount desc;partNumber;repairOperation\"
    }
    ```

    Args:
        dimensions (Union[Unset, str]):
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
        Response[AppDynamicRepairResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
dimensions=dimensions,

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
    dimensions: Union[Unset, str] = UNSET,

) -> Optional[AppDynamicRepairResponse200]:
    r""" PREVIEW - Calculate repair statistics by custom dimensions.

     Please note that this endpoint is in preview and may be a subject to changes.

    Repair statistic calculated by custom dimensions defined in the dimensions filter. Multiple values
    are separated with semicolon (;).

    ```
    Supported dimensions:

    partNumber, revision, productName, productGroup, unitType, repairOperation, period, level,
    stationName, location, purpose,
    operator, miscInfoDescription, miscInfoString, repairCode, repairCategory, repairType, componentRef,
    componentNumber,
    componentRevision, componentVendor, componentDescription, functionBlock, referencedStep,
    referencedStepPath,
    testOperation, testPeriod, testLevel, testStationName, testLocation, testPurpose, testOperator,
    batchNumber, swFilename, swVersion
    ```

    The result is ordered by the order specified. Direction may be specified with direction hints (asc
    or desc).


    You may order the result by repair kpis

    ```
    Supported kpis:
    repairReportCount, repairCount
    ```


    Default filter:

    Top 10 partNumber/repairOperation combinations from the last 30 days.

    ```
    {
    \"topCount\":10,
    \"periodCount\":30,
    \"dateGrouping\":1,
    \"includeCurrentPeriod\":true,
    \"dimensions\" : \"repairCount desc;repairReportCount desc;partNumber;repairOperation\"
    }
    ```

    Args:
        dimensions (Union[Unset, str]):
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
        AppDynamicRepairResponse200
     """


    return sync_detailed(
        client=client,
body=body,
dimensions=dimensions,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    dimensions: Union[Unset, str] = UNSET,

) -> Response[AppDynamicRepairResponse200]:
    r""" PREVIEW - Calculate repair statistics by custom dimensions.

     Please note that this endpoint is in preview and may be a subject to changes.

    Repair statistic calculated by custom dimensions defined in the dimensions filter. Multiple values
    are separated with semicolon (;).

    ```
    Supported dimensions:

    partNumber, revision, productName, productGroup, unitType, repairOperation, period, level,
    stationName, location, purpose,
    operator, miscInfoDescription, miscInfoString, repairCode, repairCategory, repairType, componentRef,
    componentNumber,
    componentRevision, componentVendor, componentDescription, functionBlock, referencedStep,
    referencedStepPath,
    testOperation, testPeriod, testLevel, testStationName, testLocation, testPurpose, testOperator,
    batchNumber, swFilename, swVersion
    ```

    The result is ordered by the order specified. Direction may be specified with direction hints (asc
    or desc).


    You may order the result by repair kpis

    ```
    Supported kpis:
    repairReportCount, repairCount
    ```


    Default filter:

    Top 10 partNumber/repairOperation combinations from the last 30 days.

    ```
    {
    \"topCount\":10,
    \"periodCount\":30,
    \"dateGrouping\":1,
    \"includeCurrentPeriod\":true,
    \"dimensions\" : \"repairCount desc;repairReportCount desc;partNumber;repairOperation\"
    }
    ```

    Args:
        dimensions (Union[Unset, str]):
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
        Response[AppDynamicRepairResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
dimensions=dimensions,

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
    dimensions: Union[Unset, str] = UNSET,

) -> Optional[AppDynamicRepairResponse200]:
    r""" PREVIEW - Calculate repair statistics by custom dimensions.

     Please note that this endpoint is in preview and may be a subject to changes.

    Repair statistic calculated by custom dimensions defined in the dimensions filter. Multiple values
    are separated with semicolon (;).

    ```
    Supported dimensions:

    partNumber, revision, productName, productGroup, unitType, repairOperation, period, level,
    stationName, location, purpose,
    operator, miscInfoDescription, miscInfoString, repairCode, repairCategory, repairType, componentRef,
    componentNumber,
    componentRevision, componentVendor, componentDescription, functionBlock, referencedStep,
    referencedStepPath,
    testOperation, testPeriod, testLevel, testStationName, testLocation, testPurpose, testOperator,
    batchNumber, swFilename, swVersion
    ```

    The result is ordered by the order specified. Direction may be specified with direction hints (asc
    or desc).


    You may order the result by repair kpis

    ```
    Supported kpis:
    repairReportCount, repairCount
    ```


    Default filter:

    Top 10 partNumber/repairOperation combinations from the last 30 days.

    ```
    {
    \"topCount\":10,
    \"periodCount\":30,
    \"dateGrouping\":1,
    \"includeCurrentPeriod\":true,
    \"dimensions\" : \"repairCount desc;repairReportCount desc;partNumber;repairOperation\"
    }
    ```

    Args:
        dimensions (Union[Unset, str]):
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
        AppDynamicRepairResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
dimensions=dimensions,

    )).parsed
