from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_sn_history_report import VirincoWATSWebDashboardModelsSnHistoryReport
from ...models.virinco_wats_web_dashboard_models_sn_history_unit import VirincoWATSWebDashboardModelsSnHistoryUnit
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Reporting/GetUnitReports",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsSnHistoryUnit):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsSnHistoryUnit):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsSnHistoryUnit):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsSnHistoryReport']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsSnHistoryReport.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsSnHistoryReport']]:
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
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
    ],

) -> Response[list['VirincoWATSWebDashboardModelsSnHistoryReport']]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsSnHistoryReport']]
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
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
    ],

) -> Optional[list['VirincoWATSWebDashboardModelsSnHistoryReport']]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsSnHistoryReport']
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
    ],

) -> Response[list['VirincoWATSWebDashboardModelsSnHistoryReport']]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsSnHistoryReport']]
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
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
        VirincoWATSWebDashboardModelsSnHistoryUnit,
    ],

) -> Optional[list['VirincoWATSWebDashboardModelsSnHistoryReport']]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):
        body (VirincoWATSWebDashboardModelsSnHistoryUnit):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsSnHistoryReport']
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
