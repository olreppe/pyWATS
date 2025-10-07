from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_create_web_client_response_200 import ClientCreateWebClientResponse200
from ...models.virinco_wats_web_dashboard_models_tdm_client_dto import VirincoWATSWebDashboardModelsTdmClientDto
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Client/WebClient",
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



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ClientCreateWebClientResponse200]:
    if response.status_code == 200:
        response_200 = ClientCreateWebClientResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ClientCreateWebClientResponse200]:
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

) -> Response[ClientCreateWebClientResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientCreateWebClientResponse200]
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
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
    ],

) -> Optional[ClientCreateWebClientResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientCreateWebClientResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
    ],

) -> Response[ClientCreateWebClientResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientCreateWebClientResponse200]
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
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
        VirincoWATSWebDashboardModelsTdmClientDto,
    ],

) -> Optional[ClientCreateWebClientResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO
        body (VirincoWATSWebDashboardModelsTdmClientDto): Client DTO

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientCreateWebClientResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
