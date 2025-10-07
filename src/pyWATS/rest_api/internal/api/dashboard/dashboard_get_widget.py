from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.dashboard_get_widget_response_200 import DashboardGetWidgetResponse200
from typing import cast



def _get_kwargs(
    *,
    widget_id: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["widgetId"] = widget_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Dashboard/GetWidget",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DashboardGetWidgetResponse200]:
    if response.status_code == 200:
        response_200 = DashboardGetWidgetResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DashboardGetWidgetResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    widget_id: int,

) -> Response[DashboardGetWidgetResponse200]:
    """ 
    Args:
        widget_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardGetWidgetResponse200]
     """


    kwargs = _get_kwargs(
        widget_id=widget_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    widget_id: int,

) -> Optional[DashboardGetWidgetResponse200]:
    """ 
    Args:
        widget_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardGetWidgetResponse200
     """


    return sync_detailed(
        client=client,
widget_id=widget_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    widget_id: int,

) -> Response[DashboardGetWidgetResponse200]:
    """ 
    Args:
        widget_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardGetWidgetResponse200]
     """


    kwargs = _get_kwargs(
        widget_id=widget_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    widget_id: int,

) -> Optional[DashboardGetWidgetResponse200]:
    """ 
    Args:
        widget_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardGetWidgetResponse200
     """


    return (await asyncio_detailed(
        client=client,
widget_id=widget_id,

    )).parsed
