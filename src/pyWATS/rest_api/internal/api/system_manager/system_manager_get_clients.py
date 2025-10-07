from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_system_manager_node import VirincoWATSWebDashboardModelsSystemManagerNode
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    client_id: Union[Unset, int] = UNSET,
    include_details: Union[Unset, bool] = UNSET,
    refresh: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["clientId"] = client_id

    params["includeDetails"] = include_details

    params["refresh"] = refresh


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/SystemManager/GetClients",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsSystemManagerNode']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsSystemManagerNode.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsSystemManagerNode']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: Union[Unset, int] = UNSET,
    include_details: Union[Unset, bool] = UNSET,
    refresh: Union[Unset, bool] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsSystemManagerNode']]:
    """ Get System manager nodes

    Args:
        client_id (Union[Unset, int]):
        include_details (Union[Unset, bool]):
        refresh (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsSystemManagerNode']]
     """


    kwargs = _get_kwargs(
        client_id=client_id,
include_details=include_details,
refresh=refresh,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: Union[Unset, int] = UNSET,
    include_details: Union[Unset, bool] = UNSET,
    refresh: Union[Unset, bool] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsSystemManagerNode']]:
    """ Get System manager nodes

    Args:
        client_id (Union[Unset, int]):
        include_details (Union[Unset, bool]):
        refresh (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsSystemManagerNode']
     """


    return sync_detailed(
        client=client,
client_id=client_id,
include_details=include_details,
refresh=refresh,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: Union[Unset, int] = UNSET,
    include_details: Union[Unset, bool] = UNSET,
    refresh: Union[Unset, bool] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsSystemManagerNode']]:
    """ Get System manager nodes

    Args:
        client_id (Union[Unset, int]):
        include_details (Union[Unset, bool]):
        refresh (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsSystemManagerNode']]
     """


    kwargs = _get_kwargs(
        client_id=client_id,
include_details=include_details,
refresh=refresh,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: Union[Unset, int] = UNSET,
    include_details: Union[Unset, bool] = UNSET,
    refresh: Union[Unset, bool] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsSystemManagerNode']]:
    """ Get System manager nodes

    Args:
        client_id (Union[Unset, int]):
        include_details (Union[Unset, bool]):
        refresh (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsSystemManagerNode']
     """


    return (await asyncio_detailed(
        client=client,
client_id=client_id,
include_details=include_details,
refresh=refresh,

    )).parsed
