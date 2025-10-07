from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import VirincoWATSWebDashboardModelsMesProductPublicProductRevision
from typing import cast



def _get_kwargs(
    part_number: str,
    revision: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Product/{part_number}/{revision}".format(part_number=part_number,revision=revision,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebDashboardModelsMesProductPublicProductRevision.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    part_number: str,
    revision: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]:
    """ Get product revision

    Args:
        part_number (str):
        revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]
     """


    kwargs = _get_kwargs(
        part_number=part_number,
revision=revision,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    part_number: str,
    revision: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]:
    """ Get product revision

    Args:
        part_number (str):
        revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesProductPublicProductRevision
     """


    return sync_detailed(
        part_number=part_number,
revision=revision,
client=client,

    ).parsed

async def asyncio_detailed(
    part_number: str,
    revision: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]:
    """ Get product revision

    Args:
        part_number (str):
        revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]
     """


    kwargs = _get_kwargs(
        part_number=part_number,
revision=revision,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    part_number: str,
    revision: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[VirincoWATSWebDashboardModelsMesProductPublicProductRevision]:
    """ Get product revision

    Args:
        part_number (str):
        revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesProductPublicProductRevision
     """


    return (await asyncio_detailed(
        part_number=part_number,
revision=revision,
client=client,

    )).parsed
