from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.dashboard_post_to_be_added_widget_response_200 import DashboardPostToBeAddedWidgetResponse200
from ...models.virinco_wats_web_dashboard_controllers_api_dashboard_controller_widget_add_data import VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
    ],
    widget_type: int,
    dashboard_id: Union[Unset, int] = UNSET,
    new_dashboard_name: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["widgetType"] = widget_type

    params["dashboardId"] = dashboard_id

    params["newDashboardName"] = new_dashboard_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Dashboard/PostToBeAddedWidget",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DashboardPostToBeAddedWidgetResponse200]:
    if response.status_code == 200:
        response_200 = DashboardPostToBeAddedWidgetResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DashboardPostToBeAddedWidgetResponse200]:
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
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
    ],
    widget_type: int,
    dashboard_id: Union[Unset, int] = UNSET,
    new_dashboard_name: Union[Unset, str] = UNSET,

) -> Response[DashboardPostToBeAddedWidgetResponse200]:
    """ Adds a new partial widget which is to be fully created the next time the dashboard loads

    Args:
        widget_type (int):
        dashboard_id (Union[Unset, int]):
        new_dashboard_name (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardPostToBeAddedWidgetResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
widget_type=widget_type,
dashboard_id=dashboard_id,
new_dashboard_name=new_dashboard_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
    ],
    widget_type: int,
    dashboard_id: Union[Unset, int] = UNSET,
    new_dashboard_name: Union[Unset, str] = UNSET,

) -> Optional[DashboardPostToBeAddedWidgetResponse200]:
    """ Adds a new partial widget which is to be fully created the next time the dashboard loads

    Args:
        widget_type (int):
        dashboard_id (Union[Unset, int]):
        new_dashboard_name (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardPostToBeAddedWidgetResponse200
     """


    return sync_detailed(
        client=client,
body=body,
widget_type=widget_type,
dashboard_id=dashboard_id,
new_dashboard_name=new_dashboard_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
    ],
    widget_type: int,
    dashboard_id: Union[Unset, int] = UNSET,
    new_dashboard_name: Union[Unset, str] = UNSET,

) -> Response[DashboardPostToBeAddedWidgetResponse200]:
    """ Adds a new partial widget which is to be fully created the next time the dashboard loads

    Args:
        widget_type (int):
        dashboard_id (Union[Unset, int]):
        new_dashboard_name (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardPostToBeAddedWidgetResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
widget_type=widget_type,
dashboard_id=dashboard_id,
new_dashboard_name=new_dashboard_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
        VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData,
    ],
    widget_type: int,
    dashboard_id: Union[Unset, int] = UNSET,
    new_dashboard_name: Union[Unset, str] = UNSET,

) -> Optional[DashboardPostToBeAddedWidgetResponse200]:
    """ Adds a new partial widget which is to be fully created the next time the dashboard loads

    Args:
        widget_type (int):
        dashboard_id (Union[Unset, int]):
        new_dashboard_name (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):
        body (VirincoWATSWebDashboardControllersApiDashboardControllerWidgetAddData):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardPostToBeAddedWidgetResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
widget_type=widget_type,
dashboard_id=dashboard_id,
new_dashboard_name=new_dashboard_name,

    )).parsed
