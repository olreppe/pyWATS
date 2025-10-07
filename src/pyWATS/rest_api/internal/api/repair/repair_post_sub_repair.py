from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.repair_post_sub_repair_response_200 import RepairPostSubRepairResponse200
from ...models.virinco_wats_web_dashboard_models_sub_repair import VirincoWATSWebDashboardModelsSubRepair
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
    ],
    station_name: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["stationName"] = station_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Internal/SubRepair",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsSubRepair):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsSubRepair):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsSubRepair):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[RepairPostSubRepairResponse200]:
    if response.status_code == 200:
        response_200 = RepairPostSubRepairResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[RepairPostSubRepairResponse200]:
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
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
    ],
    station_name: str,

) -> Response[RepairPostSubRepairResponse200]:
    """ 
    Args:
        station_name (str):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairPostSubRepairResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
station_name=station_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
    ],
    station_name: str,

) -> Optional[RepairPostSubRepairResponse200]:
    """ 
    Args:
        station_name (str):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairPostSubRepairResponse200
     """


    return sync_detailed(
        client=client,
body=body,
station_name=station_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
    ],
    station_name: str,

) -> Response[RepairPostSubRepairResponse200]:
    """ 
    Args:
        station_name (str):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RepairPostSubRepairResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
station_name=station_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
        VirincoWATSWebDashboardModelsSubRepair,
    ],
    station_name: str,

) -> Optional[RepairPostSubRepairResponse200]:
    """ 
    Args:
        station_name (str):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):
        body (VirincoWATSWebDashboardModelsSubRepair):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RepairPostSubRepairResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
station_name=station_name,

    )).parsed
