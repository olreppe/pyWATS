from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.mes_put_entity_parent_id_response_200 import MesPutEntityParentIdResponse200
from ...models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity_modification_instruction import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
    ],
    new_parent_id: UUID,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    json_new_parent_id = str(new_parent_id)
    params["newParentId"] = json_new_parent_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Mes/PutEntityParentId",
        "params": params,
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[MesPutEntityParentIdResponse200]:
    if response.status_code == 200:
        response_200 = MesPutEntityParentIdResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[MesPutEntityParentIdResponse200]:
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
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
    ],
    new_parent_id: UUID,

) -> Response[MesPutEntityParentIdResponse200]:
    """ 
    Args:
        new_parent_id (UUID):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesPutEntityParentIdResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
new_parent_id=new_parent_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
    ],
    new_parent_id: UUID,

) -> Optional[MesPutEntityParentIdResponse200]:
    """ 
    Args:
        new_parent_id (UUID):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesPutEntityParentIdResponse200
     """


    return sync_detailed(
        client=client,
body=body,
new_parent_id=new_parent_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
    ],
    new_parent_id: UUID,

) -> Response[MesPutEntityParentIdResponse200]:
    """ 
    Args:
        new_parent_id (UUID):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesPutEntityParentIdResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
new_parent_id=new_parent_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationInstruction'],
    ],
    new_parent_id: UUID,

) -> Optional[MesPutEntityParentIdResponse200]:
    """ 
    Args:
        new_parent_id (UUID):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):
        body (list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntityModificationI
            nstruction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesPutEntityParentIdResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
new_parent_id=new_parent_id,

    )).parsed
