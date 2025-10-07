from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.tsa_get_step_chart_response_200 import TSAGetStepChartResponse200
from ...models.virinco_wats_web_dashboard_models_tsa_filter import VirincoWATSWebDashboardModelsTSAFilter
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
    ],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["skip"] = skip

    params["take"] = take


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/TSA/GetStepChart",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsTSAFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsTSAFilter):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsTSAFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TSAGetStepChartResponse200]:
    if response.status_code == 200:
        response_200 = TSAGetStepChartResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TSAGetStepChartResponse200]:
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
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
    ],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,

) -> Response[TSAGetStepChartResponse200]:
    r"""  Get chart data

     load chart data from \"take amount\" new UUT reports. The newest \"chart.loadedReports\" UUTs are
    skipped (loading from newest to oldest UUT).


     {
    \"watsFilter\":{\"dateIsLocal\":false,\"maxCount\":10000,\"partNumber\":\"241119.825\",\"testOperati
    on\":\"26506\",\"run\":1,\"dateFrom\":\"2024-05-20T00:00:00\"},
    \"selectionFilter\":[{\"swFilename\":\"241119.825 rev9.0 DECNWJ-BTS BurnIn v1.7.seq\",\"swVersion\":
    \"1.7.0\",\"partNumber\":\"241119.825\",\"revision\":\"10\",\"processName\":\"Burn-in Test
    (demo)\"}],
    \"sequenceSteps\":[
    {
    \"chart\":{
    \"loadedReports\":0,
    \"totalReports\":94
    },
    \"sequenceStepIds\":[805],
    }],

    \"loopIndex\":-1,
    \"stepStatus\":0
    }

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TSAGetStepChartResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
skip=skip,
take=take,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
    ],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,

) -> Optional[TSAGetStepChartResponse200]:
    r"""  Get chart data

     load chart data from \"take amount\" new UUT reports. The newest \"chart.loadedReports\" UUTs are
    skipped (loading from newest to oldest UUT).


     {
    \"watsFilter\":{\"dateIsLocal\":false,\"maxCount\":10000,\"partNumber\":\"241119.825\",\"testOperati
    on\":\"26506\",\"run\":1,\"dateFrom\":\"2024-05-20T00:00:00\"},
    \"selectionFilter\":[{\"swFilename\":\"241119.825 rev9.0 DECNWJ-BTS BurnIn v1.7.seq\",\"swVersion\":
    \"1.7.0\",\"partNumber\":\"241119.825\",\"revision\":\"10\",\"processName\":\"Burn-in Test
    (demo)\"}],
    \"sequenceSteps\":[
    {
    \"chart\":{
    \"loadedReports\":0,
    \"totalReports\":94
    },
    \"sequenceStepIds\":[805],
    }],

    \"loopIndex\":-1,
    \"stepStatus\":0
    }

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TSAGetStepChartResponse200
     """


    return sync_detailed(
        client=client,
body=body,
skip=skip,
take=take,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
    ],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,

) -> Response[TSAGetStepChartResponse200]:
    r"""  Get chart data

     load chart data from \"take amount\" new UUT reports. The newest \"chart.loadedReports\" UUTs are
    skipped (loading from newest to oldest UUT).


     {
    \"watsFilter\":{\"dateIsLocal\":false,\"maxCount\":10000,\"partNumber\":\"241119.825\",\"testOperati
    on\":\"26506\",\"run\":1,\"dateFrom\":\"2024-05-20T00:00:00\"},
    \"selectionFilter\":[{\"swFilename\":\"241119.825 rev9.0 DECNWJ-BTS BurnIn v1.7.seq\",\"swVersion\":
    \"1.7.0\",\"partNumber\":\"241119.825\",\"revision\":\"10\",\"processName\":\"Burn-in Test
    (demo)\"}],
    \"sequenceSteps\":[
    {
    \"chart\":{
    \"loadedReports\":0,
    \"totalReports\":94
    },
    \"sequenceStepIds\":[805],
    }],

    \"loopIndex\":-1,
    \"stepStatus\":0
    }

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TSAGetStepChartResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
skip=skip,
take=take,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
    ],
    skip: Union[Unset, int] = UNSET,
    take: Union[Unset, int] = UNSET,

) -> Optional[TSAGetStepChartResponse200]:
    r"""  Get chart data

     load chart data from \"take amount\" new UUT reports. The newest \"chart.loadedReports\" UUTs are
    skipped (loading from newest to oldest UUT).


     {
    \"watsFilter\":{\"dateIsLocal\":false,\"maxCount\":10000,\"partNumber\":\"241119.825\",\"testOperati
    on\":\"26506\",\"run\":1,\"dateFrom\":\"2024-05-20T00:00:00\"},
    \"selectionFilter\":[{\"swFilename\":\"241119.825 rev9.0 DECNWJ-BTS BurnIn v1.7.seq\",\"swVersion\":
    \"1.7.0\",\"partNumber\":\"241119.825\",\"revision\":\"10\",\"processName\":\"Burn-in Test
    (demo)\"}],
    \"sequenceSteps\":[
    {
    \"chart\":{
    \"loadedReports\":0,
    \"totalReports\":94
    },
    \"sequenceStepIds\":[805],
    }],

    \"loopIndex\":-1,
    \"stepStatus\":0
    }

    Args:
        skip (Union[Unset, int]):
        take (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TSAGetStepChartResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
skip=skip,
take=take,

    )).parsed
