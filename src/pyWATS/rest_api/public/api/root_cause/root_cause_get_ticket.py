from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_models_root_cause_ticket import VirincoWATSWebModelsRootCauseTicket
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    ticket_id: UUID,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_ticket_id = str(ticket_id)
    params["ticketId"] = json_ticket_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/RootCause/Ticket",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebModelsRootCauseTicket]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebModelsRootCauseTicket.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebModelsRootCauseTicket]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ticket_id: UUID,

) -> Response[VirincoWATSWebModelsRootCauseTicket]:
    """ Get a root cause ticket

    Args:
        ticket_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebModelsRootCauseTicket]
     """


    kwargs = _get_kwargs(
        ticket_id=ticket_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    ticket_id: UUID,

) -> Optional[VirincoWATSWebModelsRootCauseTicket]:
    """ Get a root cause ticket

    Args:
        ticket_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebModelsRootCauseTicket
     """


    return sync_detailed(
        client=client,
ticket_id=ticket_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    ticket_id: UUID,

) -> Response[VirincoWATSWebModelsRootCauseTicket]:
    """ Get a root cause ticket

    Args:
        ticket_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebModelsRootCauseTicket]
     """


    kwargs = _get_kwargs(
        ticket_id=ticket_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    ticket_id: UUID,

) -> Optional[VirincoWATSWebModelsRootCauseTicket]:
    """ Get a root cause ticket

    Args:
        ticket_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebModelsRootCauseTicket
     """


    return (await asyncio_detailed(
        client=client,
ticket_id=ticket_id,

    )).parsed
