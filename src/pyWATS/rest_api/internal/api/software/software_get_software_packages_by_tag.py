from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_software_public_package import VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
from typing import cast



def _get_kwargs(
    *,
    tag: str,
    status: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["tag"] = tag

    params["status"] = status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Software/PackagesByTag",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebDashboardModelsMesSoftwarePublicPackage.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: str,
    status: str,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Filters for Software Packages with the provided tag and tag value and status.

    Args:
        tag (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]
     """


    kwargs = _get_kwargs(
        tag=tag,
status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: str,
    status: str,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Filters for Software Packages with the provided tag and tag value and status.

    Args:
        tag (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
     """


    return sync_detailed(
        client=client,
tag=tag,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: str,
    status: str,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Filters for Software Packages with the provided tag and tag value and status.

    Args:
        tag (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]
     """


    kwargs = _get_kwargs(
        tag=tag,
status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    tag: str,
    status: str,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Filters for Software Packages with the provided tag and tag value and status.

    Args:
        tag (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
     """


    return (await asyncio_detailed(
        client=client,
tag=tag,
status=status,

    )).parsed
