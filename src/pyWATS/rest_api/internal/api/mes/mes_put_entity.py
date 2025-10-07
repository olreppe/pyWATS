from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.mes_put_entity_response_200 import MesPutEntityResponse200
from ...models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
    ],
    site_relation_ids: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["siteRelationIds"] = site_relation_ids


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Mes/PutEntity",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[MesPutEntityResponse200]:
    if response.status_code == 200:
        response_200 = MesPutEntityResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[MesPutEntityResponse200]:
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
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
    ],
    site_relation_ids: Union[Unset, str] = UNSET,

) -> Response[MesPutEntityResponse200]:
    """ 
    Args:
        site_relation_ids (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesPutEntityResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
site_relation_ids=site_relation_ids,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
    ],
    site_relation_ids: Union[Unset, str] = UNSET,

) -> Optional[MesPutEntityResponse200]:
    """ 
    Args:
        site_relation_ids (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesPutEntityResponse200
     """


    return sync_detailed(
        client=client,
body=body,
site_relation_ids=site_relation_ids,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
    ],
    site_relation_ids: Union[Unset, str] = UNSET,

) -> Response[MesPutEntityResponse200]:
    """ 
    Args:
        site_relation_ids (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesPutEntityResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
site_relation_ids=site_relation_ids,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
        VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity,
    ],
    site_relation_ids: Union[Unset, str] = UNSET,

) -> Optional[MesPutEntityResponse200]:
    """ 
    Args:
        site_relation_ids (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):
        body (VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesPutEntityResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
site_relation_ids=site_relation_ids,

    )).parsed
