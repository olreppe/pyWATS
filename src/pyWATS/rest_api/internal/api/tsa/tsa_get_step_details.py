from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.tsa_get_step_details_response_200 import TSAGetStepDetailsResponse200
from ...models.virinco_wats_web_dashboard_models_tsa_filter import VirincoWATSWebDashboardModelsTSAFilter
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/TSA/GetStepDetails",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TSAGetStepDetailsResponse200]:
    if response.status_code == 200:
        response_200 = TSAGetStepDetailsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TSAGetStepDetailsResponse200]:
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

) -> Response[TSAGetStepDetailsResponse200]:
    r"""  Get step details.

     Options: None = 0, Measurements = 1, ShrinkMeasurements = 2, NormalDist = 8, XbarR = 16, Cusum =
    32, Quartiles = 64, Imr = 128, Suggestions = 256
     Grouping: None = 0, PartNumber = 1, Operator = 2, Station = 4, SerialNumber = 8, Revision = 16,
    BatchNumber = 32, FixtureId = 64, SocketIndex = 128, ProcessName = 256, SwFilename = 512, SwVersion
    = 1024, Misc = 2048


    {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"run\":1,
         \"dateGrouping\":3
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"sequenceSteps\":[{\"sequenceStepIds\":[2,4,80],\"measureName\":\"measurementName\"},{\"sequenceSte
    pIds\":[12,14,18],\"measureName\":\"measurementName2\"}],
    \"stepDetailsOptions\":7,
    \"loopIndex\":-1,
    \"period\":\"2022\",
    \"stepDetailsGrouping\":1,

     \"filterFailedMeasures\":false,
     \"filterMeasureHigh\":15.2,
     \"filterMeasureLow\":3.3,
     \"highTestLimit\":14.5,
     \"lowTestLimit\":5.5,
     \"numberOfMeasurements\":1000 ?? specified in watsFilter?
     \"groupByMiscDescriptions\" : [\"d1\"],
     \"measureStatus\": 64, //All = 0, Passed = 1, Failed=64
     \"includeEarlierRuns\":true,
     \"forceRefresh\":false
    }

    Args:
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TSAGetStepDetailsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

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

) -> Optional[TSAGetStepDetailsResponse200]:
    r"""  Get step details.

     Options: None = 0, Measurements = 1, ShrinkMeasurements = 2, NormalDist = 8, XbarR = 16, Cusum =
    32, Quartiles = 64, Imr = 128, Suggestions = 256
     Grouping: None = 0, PartNumber = 1, Operator = 2, Station = 4, SerialNumber = 8, Revision = 16,
    BatchNumber = 32, FixtureId = 64, SocketIndex = 128, ProcessName = 256, SwFilename = 512, SwVersion
    = 1024, Misc = 2048


    {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"run\":1,
         \"dateGrouping\":3
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"sequenceSteps\":[{\"sequenceStepIds\":[2,4,80],\"measureName\":\"measurementName\"},{\"sequenceSte
    pIds\":[12,14,18],\"measureName\":\"measurementName2\"}],
    \"stepDetailsOptions\":7,
    \"loopIndex\":-1,
    \"period\":\"2022\",
    \"stepDetailsGrouping\":1,

     \"filterFailedMeasures\":false,
     \"filterMeasureHigh\":15.2,
     \"filterMeasureLow\":3.3,
     \"highTestLimit\":14.5,
     \"lowTestLimit\":5.5,
     \"numberOfMeasurements\":1000 ?? specified in watsFilter?
     \"groupByMiscDescriptions\" : [\"d1\"],
     \"measureStatus\": 64, //All = 0, Passed = 1, Failed=64
     \"includeEarlierRuns\":true,
     \"forceRefresh\":false
    }

    Args:
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TSAGetStepDetailsResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
        VirincoWATSWebDashboardModelsTSAFilter,
    ],

) -> Response[TSAGetStepDetailsResponse200]:
    r"""  Get step details.

     Options: None = 0, Measurements = 1, ShrinkMeasurements = 2, NormalDist = 8, XbarR = 16, Cusum =
    32, Quartiles = 64, Imr = 128, Suggestions = 256
     Grouping: None = 0, PartNumber = 1, Operator = 2, Station = 4, SerialNumber = 8, Revision = 16,
    BatchNumber = 32, FixtureId = 64, SocketIndex = 128, ProcessName = 256, SwFilename = 512, SwVersion
    = 1024, Misc = 2048


    {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"run\":1,
         \"dateGrouping\":3
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"sequenceSteps\":[{\"sequenceStepIds\":[2,4,80],\"measureName\":\"measurementName\"},{\"sequenceSte
    pIds\":[12,14,18],\"measureName\":\"measurementName2\"}],
    \"stepDetailsOptions\":7,
    \"loopIndex\":-1,
    \"period\":\"2022\",
    \"stepDetailsGrouping\":1,

     \"filterFailedMeasures\":false,
     \"filterMeasureHigh\":15.2,
     \"filterMeasureLow\":3.3,
     \"highTestLimit\":14.5,
     \"lowTestLimit\":5.5,
     \"numberOfMeasurements\":1000 ?? specified in watsFilter?
     \"groupByMiscDescriptions\" : [\"d1\"],
     \"measureStatus\": 64, //All = 0, Passed = 1, Failed=64
     \"includeEarlierRuns\":true,
     \"forceRefresh\":false
    }

    Args:
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TSAGetStepDetailsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

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

) -> Optional[TSAGetStepDetailsResponse200]:
    r"""  Get step details.

     Options: None = 0, Measurements = 1, ShrinkMeasurements = 2, NormalDist = 8, XbarR = 16, Cusum =
    32, Quartiles = 64, Imr = 128, Suggestions = 256
     Grouping: None = 0, PartNumber = 1, Operator = 2, Station = 4, SerialNumber = 8, Revision = 16,
    BatchNumber = 32, FixtureId = 64, SocketIndex = 128, ProcessName = 256, SwFilename = 512, SwVersion
    = 1024, Misc = 2048


    {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"run\":1,
         \"dateGrouping\":3
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"sequenceSteps\":[{\"sequenceStepIds\":[2,4,80],\"measureName\":\"measurementName\"},{\"sequenceSte
    pIds\":[12,14,18],\"measureName\":\"measurementName2\"}],
    \"stepDetailsOptions\":7,
    \"loopIndex\":-1,
    \"period\":\"2022\",
    \"stepDetailsGrouping\":1,

     \"filterFailedMeasures\":false,
     \"filterMeasureHigh\":15.2,
     \"filterMeasureLow\":3.3,
     \"highTestLimit\":14.5,
     \"lowTestLimit\":5.5,
     \"numberOfMeasurements\":1000 ?? specified in watsFilter?
     \"groupByMiscDescriptions\" : [\"d1\"],
     \"measureStatus\": 64, //All = 0, Passed = 1, Failed=64
     \"includeEarlierRuns\":true,
     \"forceRefresh\":false
    }

    Args:
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):
        body (VirincoWATSWebDashboardModelsTSAFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TSAGetStepDetailsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
