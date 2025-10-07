from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    package_id: UUID,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_package_id = str(package_id)
    params["packageId"] = json_package_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/GetPackage",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebDashboardModelsMesSoftwarePackage.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]
     """


    kwargs = _get_kwargs(
        package_id=package_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePackage
     """


    return sync_detailed(
        client=client,
package_id=package_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]
     """


    kwargs = _get_kwargs(
        package_id=package_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePackage
     """


    return (await asyncio_detailed(
        client=client,
package_id=package_id,

    )).parsed
