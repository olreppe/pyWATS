from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_mi_test_sequence_definition import VirincoWATSWebDashboardModelsMesMITestSequenceDefinition
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    site_code: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["siteCode"] = site_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Distribution/TestSequences/{id}".format(id=id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebDashboardModelsMesMITestSequenceDefinition.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    site_code: str,

) -> Response[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]:
    """ 
    Args:
        id (UUID):
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]
     """


    kwargs = _get_kwargs(
        id=id,
site_code=site_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    site_code: str,

) -> Optional[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]:
    """ 
    Args:
        id (UUID):
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesMITestSequenceDefinition
     """


    return sync_detailed(
        id=id,
client=client,
site_code=site_code,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    site_code: str,

) -> Response[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]:
    """ 
    Args:
        id (UUID):
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]
     """


    kwargs = _get_kwargs(
        id=id,
site_code=site_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    site_code: str,

) -> Optional[VirincoWATSWebDashboardModelsMesMITestSequenceDefinition]:
    """ 
    Args:
        id (UUID):
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesMITestSequenceDefinition
     """


    return (await asyncio_detailed(
        id=id,
client=client,
site_code=site_code,

    )).parsed
