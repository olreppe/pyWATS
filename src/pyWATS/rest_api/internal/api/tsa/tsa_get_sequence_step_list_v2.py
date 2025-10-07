from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_sequence_step import VirincoWATSWebDashboardModelsSequenceStep
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
        "url": "/api/internal/TSA/GetSequenceStepListV2",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsSequenceStep']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsSequenceStep.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsSequenceStep']]:
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

) -> Response[list['VirincoWATSWebDashboardModelsSequenceStep']]:
    r"""  Get step and measurement list

     {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"yield\":1
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"stepGrouping\":13,
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
        Response[list['VirincoWATSWebDashboardModelsSequenceStep']]
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

) -> Optional[list['VirincoWATSWebDashboardModelsSequenceStep']]:
    r"""  Get step and measurement list

     {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"yield\":1
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"stepGrouping\":13,
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
        list['VirincoWATSWebDashboardModelsSequenceStep']
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

) -> Response[list['VirincoWATSWebDashboardModelsSequenceStep']]:
    r"""  Get step and measurement list

     {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"yield\":1
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"stepGrouping\":13,
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
        Response[list['VirincoWATSWebDashboardModelsSequenceStep']]
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

) -> Optional[list['VirincoWATSWebDashboardModelsSequenceStep']]:
    r"""  Get step and measurement list

     {
    \"watsFilter\": {
         \"partNumber\":\"OLC-140-C\",
         \"testOperation\":\"1100\",
         \"dateFrom\":\"2016-11-01T00:00:00\",
         \"yield\":1
    },
    \"selectionFilter\":[{
         \"partNumber\":\"OLC-140-C\",
         \"processName\":\"PCBA (demo)\"
    },
    {
         \"partNumber\":\"OLC-140-P\",
         \"processName\":\"PCBA (demo)\"
    }],
    \"stepGrouping\":13,
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
        list['VirincoWATSWebDashboardModelsSequenceStep']
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
