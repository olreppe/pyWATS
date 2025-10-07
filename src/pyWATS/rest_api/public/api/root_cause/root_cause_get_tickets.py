from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.root_cause_get_tickets_status import RootCauseGetTicketsStatus
from ...models.root_cause_get_tickets_view import RootCauseGetTicketsView
from ...models.virinco_wats_web_models_root_cause_ticket import VirincoWATSWebModelsRootCauseTicket
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    status: RootCauseGetTicketsStatus,
    view: RootCauseGetTicketsView,
    search_string: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_status = status.value
    params["status"] = json_status

    json_view = view.value
    params["view"] = json_view

    params["searchString"] = search_string


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/RootCause/Tickets",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebModelsRootCauseTicket']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebModelsRootCauseTicket.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebModelsRootCauseTicket']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    status: RootCauseGetTicketsStatus,
    view: RootCauseGetTicketsView,
    search_string: Union[Unset, str] = UNSET,

) -> Response[list['VirincoWATSWebModelsRootCauseTicket']]:
    """ Get root cause tickets with a given status.

    Args:
        status (RootCauseGetTicketsStatus):
        view (RootCauseGetTicketsView):
        search_string (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebModelsRootCauseTicket']]
     """


    kwargs = _get_kwargs(
        status=status,
view=view,
search_string=search_string,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    status: RootCauseGetTicketsStatus,
    view: RootCauseGetTicketsView,
    search_string: Union[Unset, str] = UNSET,

) -> Optional[list['VirincoWATSWebModelsRootCauseTicket']]:
    """ Get root cause tickets with a given status.

    Args:
        status (RootCauseGetTicketsStatus):
        view (RootCauseGetTicketsView):
        search_string (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebModelsRootCauseTicket']
     """


    return sync_detailed(
        client=client,
status=status,
view=view,
search_string=search_string,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    status: RootCauseGetTicketsStatus,
    view: RootCauseGetTicketsView,
    search_string: Union[Unset, str] = UNSET,

) -> Response[list['VirincoWATSWebModelsRootCauseTicket']]:
    """ Get root cause tickets with a given status.

    Args:
        status (RootCauseGetTicketsStatus):
        view (RootCauseGetTicketsView):
        search_string (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebModelsRootCauseTicket']]
     """


    kwargs = _get_kwargs(
        status=status,
view=view,
search_string=search_string,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    status: RootCauseGetTicketsStatus,
    view: RootCauseGetTicketsView,
    search_string: Union[Unset, str] = UNSET,

) -> Optional[list['VirincoWATSWebModelsRootCauseTicket']]:
    """ Get root cause tickets with a given status.

    Args:
        status (RootCauseGetTicketsStatus):
        view (RootCauseGetTicketsView):
        search_string (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebModelsRootCauseTicket']
     """


    return (await asyncio_detailed(
        client=client,
status=status,
view=view,
search_string=search_string,

    )).parsed
