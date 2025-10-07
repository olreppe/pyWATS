from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.app_aggregated_measurements_response_200 import AppAggregatedMeasurementsResponse200
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
    measurement_paths: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["measurementPaths"] = measurement_paths


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/App/AggregatedMeasurements",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AppAggregatedMeasurementsResponse200]:
    if response.status_code == 200:
        response_200 = AppAggregatedMeasurementsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AppAggregatedMeasurementsResponse200]:
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
    measurement_paths: Union[Unset, str] = UNSET,

) -> Response[AppAggregatedMeasurementsResponse200]:
    """ Get aggregated numeric measurements by measurement path. A maximum of 10000 measurements are
    returned.
    Requesting the endpoint with a empty filter will return measurements from the last seven days most
    failed steps

     Split sequence steps with the paragraph mark - ¶
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test

    Measurement name must be specified for multi numeric measurements. In those cases, simply prepend
    the measurement name with two paragraph marks.
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0

    Separate multiple paths with semi colon (;)
    ex.
    MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0;MainSequence
    Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement1


    partnumber and testOperation filter required

    Args:
        measurement_paths (Union[Unset, str]):
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
        Response[AppAggregatedMeasurementsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
measurement_paths=measurement_paths,

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
    measurement_paths: Union[Unset, str] = UNSET,

) -> Optional[AppAggregatedMeasurementsResponse200]:
    """ Get aggregated numeric measurements by measurement path. A maximum of 10000 measurements are
    returned.
    Requesting the endpoint with a empty filter will return measurements from the last seven days most
    failed steps

     Split sequence steps with the paragraph mark - ¶
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test

    Measurement name must be specified for multi numeric measurements. In those cases, simply prepend
    the measurement name with two paragraph marks.
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0

    Separate multiple paths with semi colon (;)
    ex.
    MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0;MainSequence
    Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement1


    partnumber and testOperation filter required

    Args:
        measurement_paths (Union[Unset, str]):
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
        AppAggregatedMeasurementsResponse200
     """


    return sync_detailed(
        client=client,
body=body,
measurement_paths=measurement_paths,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    measurement_paths: Union[Unset, str] = UNSET,

) -> Response[AppAggregatedMeasurementsResponse200]:
    """ Get aggregated numeric measurements by measurement path. A maximum of 10000 measurements are
    returned.
    Requesting the endpoint with a empty filter will return measurements from the last seven days most
    failed steps

     Split sequence steps with the paragraph mark - ¶
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test

    Measurement name must be specified for multi numeric measurements. In those cases, simply prepend
    the measurement name with two paragraph marks.
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0

    Separate multiple paths with semi colon (;)
    ex.
    MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0;MainSequence
    Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement1


    partnumber and testOperation filter required

    Args:
        measurement_paths (Union[Unset, str]):
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
        Response[AppAggregatedMeasurementsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
measurement_paths=measurement_paths,

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
    measurement_paths: Union[Unset, str] = UNSET,

) -> Optional[AppAggregatedMeasurementsResponse200]:
    """ Get aggregated numeric measurements by measurement path. A maximum of 10000 measurements are
    returned.
    Requesting the endpoint with a empty filter will return measurements from the last seven days most
    failed steps

     Split sequence steps with the paragraph mark - ¶
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test

    Measurement name must be specified for multi numeric measurements. In those cases, simply prepend
    the measurement name with two paragraph marks.
    ex. MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0

    Separate multiple paths with semi colon (;)
    ex.
    MainSequence Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement0;MainSequence
    Callback¶NI steps (NI seq call)¶Multiple Numeric Limit Test¶¶Measurement1


    partnumber and testOperation filter required

    Args:
        measurement_paths (Union[Unset, str]):
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
        AppAggregatedMeasurementsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
measurement_paths=measurement_paths,

    )).parsed
