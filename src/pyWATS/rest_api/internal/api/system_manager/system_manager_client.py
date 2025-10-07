from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_tdm_client_dto import VirincoWATSWebDashboardModelsTdmClientDto
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["moveWithHistory"] = move_with_history


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/SystemManager/Client",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsTdmClientDto):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmClientDto):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmClientDto):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> Response[Any]:
    """ Update basic WATS Client information.

    displayName, location, purpose and clientGroupId.

    ClientId of an existing client is required. Name and Type are not changeable.

    Type values:
    LocalServer = 1,
    MasterServer = 2,
    Client = 5,
    WebClient = 6,

    Args:
        move_with_history (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,
move_with_history=move_with_history,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
    ],
    move_with_history: Union[Unset, bool] = UNSET,

) -> Response[Any]:
    """ Update basic WATS Client information.

    displayName, location, purpose and clientGroupId.

    ClientId of an existing client is required. Name and Type are not changeable.

    Type values:
    LocalServer = 1,
    MasterServer = 2,
    Client = 5,
    WebClient = 6,

    Args:
        move_with_history (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,
move_with_history=move_with_history,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

