from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.dashboard_get_dashboard_response_200 import DashboardGetDashboardResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    id: int,
    *,
    include_widgets: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["includeWidgets"] = include_widgets


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Dashboard/GetDashboard/{id}".format(id=id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DashboardGetDashboardResponse200]:
    if response.status_code == 200:
        response_200 = DashboardGetDashboardResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DashboardGetDashboardResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    include_widgets: Union[Unset, bool] = UNSET,

) -> Response[DashboardGetDashboardResponse200]:
    """ Retrieve data about a dashboard, and optionally its widgets.

    Args:
        id (int):
        include_widgets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardGetDashboardResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
include_widgets=include_widgets,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    include_widgets: Union[Unset, bool] = UNSET,

) -> Optional[DashboardGetDashboardResponse200]:
    """ Retrieve data about a dashboard, and optionally its widgets.

    Args:
        id (int):
        include_widgets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardGetDashboardResponse200
     """


    return sync_detailed(
        id=id,
client=client,
include_widgets=include_widgets,

    ).parsed

async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    include_widgets: Union[Unset, bool] = UNSET,

) -> Response[DashboardGetDashboardResponse200]:
    """ Retrieve data about a dashboard, and optionally its widgets.

    Args:
        id (int):
        include_widgets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardGetDashboardResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
include_widgets=include_widgets,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    include_widgets: Union[Unset, bool] = UNSET,

) -> Optional[DashboardGetDashboardResponse200]:
    """ Retrieve data about a dashboard, and optionally its widgets.

    Args:
        id (int):
        include_widgets (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardGetDashboardResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
include_widgets=include_widgets,

    )).parsed
