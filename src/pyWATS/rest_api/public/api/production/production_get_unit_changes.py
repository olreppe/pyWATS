from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_production_public_unit_change import VirincoWATSWebDashboardModelsMesProductionPublicUnitChange
from typing import cast



def _get_kwargs(
    *,
    max_count: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["maxCount"] = max_count


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Production/Units/Changes",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMesProductionPublicUnitChange.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: int,

) -> Response[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]:
    """ Get old and new parent unit, part number, revision, and unitphase for units that have changed.
    Delete the change once handled using the DELETE method.

    Args:
        max_count (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]
     """


    kwargs = _get_kwargs(
        max_count=max_count,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: int,

) -> Optional[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]:
    """ Get old and new parent unit, part number, revision, and unitphase for units that have changed.
    Delete the change once handled using the DELETE method.

    Args:
        max_count (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']
     """


    return sync_detailed(
        client=client,
max_count=max_count,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: int,

) -> Response[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]:
    """ Get old and new parent unit, part number, revision, and unitphase for units that have changed.
    Delete the change once handled using the DELETE method.

    Args:
        max_count (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]
     """


    kwargs = _get_kwargs(
        max_count=max_count,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: int,

) -> Optional[list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']]:
    """ Get old and new parent unit, part number, revision, and unitphase for units that have changed.
    Delete the change once handled using the DELETE method.

    Args:
        max_count (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesProductionPublicUnitChange']
     """


    return (await asyncio_detailed(
        client=client,
max_count=max_count,

    )).parsed
