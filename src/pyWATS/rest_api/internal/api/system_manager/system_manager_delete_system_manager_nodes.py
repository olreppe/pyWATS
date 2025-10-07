from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.system_manager_delete_system_manager_nodes_response_200 import SystemManagerDeleteSystemManagerNodesResponse200
from ...models.virinco_wats_web_dashboard_models_system_manager_node import VirincoWATSWebDashboardModelsSystemManagerNode
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/SystemManager/DeleteSystemManagerNodes",
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SystemManagerDeleteSystemManagerNodesResponse200]:
    if response.status_code == 200:
        response_200 = SystemManagerDeleteSystemManagerNodesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SystemManagerDeleteSystemManagerNodesResponse200]:
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
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
    ],

) -> Response[SystemManagerDeleteSystemManagerNodesResponse200]:
    """ 
    Args:
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerDeleteSystemManagerNodesResponse200]
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
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
    ],

) -> Optional[SystemManagerDeleteSystemManagerNodesResponse200]:
    """ 
    Args:
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerDeleteSystemManagerNodesResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
    ],

) -> Response[SystemManagerDeleteSystemManagerNodesResponse200]:
    """ 
    Args:
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerDeleteSystemManagerNodesResponse200]
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
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
        list['VirincoWATSWebDashboardModelsSystemManagerNode'],
    ],

) -> Optional[SystemManagerDeleteSystemManagerNodesResponse200]:
    """ 
    Args:
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):
        body (list['VirincoWATSWebDashboardModelsSystemManagerNode']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerDeleteSystemManagerNodesResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
