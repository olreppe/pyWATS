from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.reporting_get_grr_sequence_step_list_response_200 import ReportingGetGrrSequenceStepListResponse200
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
    sw_filename: str,
    sw_version: str,
    appraisers: str,
    step_ids: Union[Unset, str] = UNSET,
    excluded_report_ids: Union[Unset, str] = UNSET,
    limit1: Union[Unset, float] = UNSET,
    limit2: Union[Unset, float] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["swFilename"] = sw_filename

    params["swVersion"] = sw_version

    params["appraisers"] = appraisers

    params["stepIds"] = step_ids

    params["excludedReportIds"] = excluded_report_ids

    params["limit1"] = limit1

    params["limit2"] = limit2


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Reporting/GetGrrSequenceStepList",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportingGetGrrSequenceStepListResponse200]:
    if response.status_code == 200:
        response_200 = ReportingGetGrrSequenceStepListResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportingGetGrrSequenceStepListResponse200]:
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
    sw_filename: str,
    sw_version: str,
    appraisers: str,
    step_ids: Union[Unset, str] = UNSET,
    excluded_report_ids: Union[Unset, str] = UNSET,
    limit1: Union[Unset, float] = UNSET,
    limit2: Union[Unset, float] = UNSET,

) -> Response[ReportingGetGrrSequenceStepListResponse200]:
    """ 
    Args:
        sw_filename (str):
        sw_version (str):
        appraisers (str):
        step_ids (Union[Unset, str]):
        excluded_report_ids (Union[Unset, str]):
        limit1 (Union[Unset, float]):
        limit2 (Union[Unset, float]):
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
        Response[ReportingGetGrrSequenceStepListResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
sw_filename=sw_filename,
sw_version=sw_version,
appraisers=appraisers,
step_ids=step_ids,
excluded_report_ids=excluded_report_ids,
limit1=limit1,
limit2=limit2,

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
    sw_filename: str,
    sw_version: str,
    appraisers: str,
    step_ids: Union[Unset, str] = UNSET,
    excluded_report_ids: Union[Unset, str] = UNSET,
    limit1: Union[Unset, float] = UNSET,
    limit2: Union[Unset, float] = UNSET,

) -> Optional[ReportingGetGrrSequenceStepListResponse200]:
    """ 
    Args:
        sw_filename (str):
        sw_version (str):
        appraisers (str):
        step_ids (Union[Unset, str]):
        excluded_report_ids (Union[Unset, str]):
        limit1 (Union[Unset, float]):
        limit2 (Union[Unset, float]):
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
        ReportingGetGrrSequenceStepListResponse200
     """


    return sync_detailed(
        client=client,
body=body,
sw_filename=sw_filename,
sw_version=sw_version,
appraisers=appraisers,
step_ids=step_ids,
excluded_report_ids=excluded_report_ids,
limit1=limit1,
limit2=limit2,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    sw_filename: str,
    sw_version: str,
    appraisers: str,
    step_ids: Union[Unset, str] = UNSET,
    excluded_report_ids: Union[Unset, str] = UNSET,
    limit1: Union[Unset, float] = UNSET,
    limit2: Union[Unset, float] = UNSET,

) -> Response[ReportingGetGrrSequenceStepListResponse200]:
    """ 
    Args:
        sw_filename (str):
        sw_version (str):
        appraisers (str):
        step_ids (Union[Unset, str]):
        excluded_report_ids (Union[Unset, str]):
        limit1 (Union[Unset, float]):
        limit2 (Union[Unset, float]):
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
        Response[ReportingGetGrrSequenceStepListResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
sw_filename=sw_filename,
sw_version=sw_version,
appraisers=appraisers,
step_ids=step_ids,
excluded_report_ids=excluded_report_ids,
limit1=limit1,
limit2=limit2,

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
    sw_filename: str,
    sw_version: str,
    appraisers: str,
    step_ids: Union[Unset, str] = UNSET,
    excluded_report_ids: Union[Unset, str] = UNSET,
    limit1: Union[Unset, float] = UNSET,
    limit2: Union[Unset, float] = UNSET,

) -> Optional[ReportingGetGrrSequenceStepListResponse200]:
    """ 
    Args:
        sw_filename (str):
        sw_version (str):
        appraisers (str):
        step_ids (Union[Unset, str]):
        excluded_report_ids (Union[Unset, str]):
        limit1 (Union[Unset, float]):
        limit2 (Union[Unset, float]):
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
        ReportingGetGrrSequenceStepListResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
sw_filename=sw_filename,
sw_version=sw_version,
appraisers=appraisers,
step_ids=step_ids,
excluded_report_ids=excluded_report_ids,
limit1=limit1,
limit2=limit2,

    )).parsed
