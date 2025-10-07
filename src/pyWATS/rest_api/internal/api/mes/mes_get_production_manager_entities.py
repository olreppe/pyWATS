from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_production_production_manager_entity import VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    search_string: str,
    wf: bool,
    mi: bool,
    sw: bool,
    draft: Union[Unset, bool] = UNSET,
    pending: Union[Unset, bool] = UNSET,
    released: Union[Unset, bool] = UNSET,
    revoked: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["searchString"] = search_string

    params["wf"] = wf

    params["mi"] = mi

    params["sw"] = sw

    params["draft"] = draft

    params["pending"] = pending

    params["released"] = released

    params["revoked"] = revoked


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Mes/GetProductionManagerEntities",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_string: str,
    wf: bool,
    mi: bool,
    sw: bool,
    draft: Union[Unset, bool] = UNSET,
    pending: Union[Unset, bool] = UNSET,
    released: Union[Unset, bool] = UNSET,
    revoked: Union[Unset, bool] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]:
    """ 
    Args:
        search_string (str):
        wf (bool):
        mi (bool):
        sw (bool):
        draft (Union[Unset, bool]):
        pending (Union[Unset, bool]):
        released (Union[Unset, bool]):
        revoked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]
     """


    kwargs = _get_kwargs(
        search_string=search_string,
wf=wf,
mi=mi,
sw=sw,
draft=draft,
pending=pending,
released=released,
revoked=revoked,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    search_string: str,
    wf: bool,
    mi: bool,
    sw: bool,
    draft: Union[Unset, bool] = UNSET,
    pending: Union[Unset, bool] = UNSET,
    released: Union[Unset, bool] = UNSET,
    revoked: Union[Unset, bool] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]:
    """ 
    Args:
        search_string (str):
        wf (bool):
        mi (bool):
        sw (bool):
        draft (Union[Unset, bool]):
        pending (Union[Unset, bool]):
        released (Union[Unset, bool]):
        revoked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']
     """


    return sync_detailed(
        client=client,
search_string=search_string,
wf=wf,
mi=mi,
sw=sw,
draft=draft,
pending=pending,
released=released,
revoked=revoked,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_string: str,
    wf: bool,
    mi: bool,
    sw: bool,
    draft: Union[Unset, bool] = UNSET,
    pending: Union[Unset, bool] = UNSET,
    released: Union[Unset, bool] = UNSET,
    revoked: Union[Unset, bool] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]:
    """ 
    Args:
        search_string (str):
        wf (bool):
        mi (bool):
        sw (bool):
        draft (Union[Unset, bool]):
        pending (Union[Unset, bool]):
        released (Union[Unset, bool]):
        revoked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]
     """


    kwargs = _get_kwargs(
        search_string=search_string,
wf=wf,
mi=mi,
sw=sw,
draft=draft,
pending=pending,
released=released,
revoked=revoked,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    search_string: str,
    wf: bool,
    mi: bool,
    sw: bool,
    draft: Union[Unset, bool] = UNSET,
    pending: Union[Unset, bool] = UNSET,
    released: Union[Unset, bool] = UNSET,
    revoked: Union[Unset, bool] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']]:
    """ 
    Args:
        search_string (str):
        wf (bool):
        mi (bool):
        sw (bool):
        draft (Union[Unset, bool]):
        pending (Union[Unset, bool]):
        released (Union[Unset, bool]):
        revoked (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesProductionProductionManagerEntity']
     """


    return (await asyncio_detailed(
        client=client,
search_string=search_string,
wf=wf,
mi=mi,
sw=sw,
draft=draft,
pending=pending,
released=released,
revoked=revoked,

    )).parsed
