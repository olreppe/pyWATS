from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.system_manager_update_system_manager_node_response_200 import SystemManagerUpdateSystemManagerNodeResponse200
from ...models.virinco_wats_web_dashboard_models_system_manager_node import VirincoWATSWebDashboardModelsSystemManagerNode
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["moveWithHistory"] = move_with_history


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/SystemManager/UpdateSystemManagerNode",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsSystemManagerNode):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsSystemManagerNode):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsSystemManagerNode):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SystemManagerUpdateSystemManagerNodeResponse200]:
    if response.status_code == 200:
        response_200 = SystemManagerUpdateSystemManagerNodeResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SystemManagerUpdateSystemManagerNodeResponse200]:
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
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> Response[SystemManagerUpdateSystemManagerNodeResponse200]:
    """ Update basic system manager node information.
    Client (clientId required): displayName, location,  purpose and parentId
    Level (clientGroupId required): name, type, gps and parentId.

    Args:
        move_with_history (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerUpdateSystemManagerNodeResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
move_with_history=move_with_history,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> Optional[SystemManagerUpdateSystemManagerNodeResponse200]:
    """ Update basic system manager node information.
    Client (clientId required): displayName, location,  purpose and parentId
    Level (clientGroupId required): name, type, gps and parentId.

    Args:
        move_with_history (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerUpdateSystemManagerNodeResponse200
     """


    return sync_detailed(
        client=client,
body=body,
move_with_history=move_with_history,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> Response[SystemManagerUpdateSystemManagerNodeResponse200]:
    """ Update basic system manager node information.
    Client (clientId required): displayName, location,  purpose and parentId
    Level (clientGroupId required): name, type, gps and parentId.

    Args:
        move_with_history (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerUpdateSystemManagerNodeResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
move_with_history=move_with_history,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
        VirincoWATSWebDashboardModelsSystemManagerNode,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> Optional[SystemManagerUpdateSystemManagerNodeResponse200]:
    """ Update basic system manager node information.
    Client (clientId required): displayName, location,  purpose and parentId
    Level (clientGroupId required): name, type, gps and parentId.

    Args:
        move_with_history (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):
        body (VirincoWATSWebDashboardModelsSystemManagerNode):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerUpdateSystemManagerNodeResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
move_with_history=move_with_history,

    )).parsed
