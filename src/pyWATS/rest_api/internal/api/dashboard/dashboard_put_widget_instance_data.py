from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.dashboard_put_widget_instance_data_data_body import DashboardPutWidgetInstanceDataDataBody
from ...models.dashboard_put_widget_instance_data_json_body import DashboardPutWidgetInstanceDataJsonBody
from ...models.dashboard_put_widget_instance_data_response_200 import DashboardPutWidgetInstanceDataResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        DashboardPutWidgetInstanceDataJsonBody,
        DashboardPutWidgetInstanceDataDataBody,
    ],
    widget_id: int,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["widgetId"] = widget_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Dashboard/PutWidgetInstanceData",
        "params": params,
    }

    if isinstance(body, DashboardPutWidgetInstanceDataJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, DashboardPutWidgetInstanceDataDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DashboardPutWidgetInstanceDataResponse200]:
    if response.status_code == 200:
        response_200 = DashboardPutWidgetInstanceDataResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DashboardPutWidgetInstanceDataResponse200]:
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
        DashboardPutWidgetInstanceDataJsonBody,
        DashboardPutWidgetInstanceDataDataBody,
    ],
    widget_id: int,

) -> Response[DashboardPutWidgetInstanceDataResponse200]:
    """ Updates internal data needed by a widget instance

    Args:
        widget_id (int):
        body (DashboardPutWidgetInstanceDataJsonBody):
        body (DashboardPutWidgetInstanceDataDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardPutWidgetInstanceDataResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
widget_id=widget_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DashboardPutWidgetInstanceDataJsonBody,
        DashboardPutWidgetInstanceDataDataBody,
    ],
    widget_id: int,

) -> Optional[DashboardPutWidgetInstanceDataResponse200]:
    """ Updates internal data needed by a widget instance

    Args:
        widget_id (int):
        body (DashboardPutWidgetInstanceDataJsonBody):
        body (DashboardPutWidgetInstanceDataDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardPutWidgetInstanceDataResponse200
     """


    return sync_detailed(
        client=client,
body=body,
widget_id=widget_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DashboardPutWidgetInstanceDataJsonBody,
        DashboardPutWidgetInstanceDataDataBody,
    ],
    widget_id: int,

) -> Response[DashboardPutWidgetInstanceDataResponse200]:
    """ Updates internal data needed by a widget instance

    Args:
        widget_id (int):
        body (DashboardPutWidgetInstanceDataJsonBody):
        body (DashboardPutWidgetInstanceDataDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DashboardPutWidgetInstanceDataResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
widget_id=widget_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DashboardPutWidgetInstanceDataJsonBody,
        DashboardPutWidgetInstanceDataDataBody,
    ],
    widget_id: int,

) -> Optional[DashboardPutWidgetInstanceDataResponse200]:
    """ Updates internal data needed by a widget instance

    Args:
        widget_id (int):
        body (DashboardPutWidgetInstanceDataJsonBody):
        body (DashboardPutWidgetInstanceDataDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DashboardPutWidgetInstanceDataResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
widget_id=widget_id,

    )).parsed
