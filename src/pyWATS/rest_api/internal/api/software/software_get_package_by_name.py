from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.software_get_package_by_name_status import SoftwareGetPackageByNameStatus
from ...models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
from typing import cast



def _get_kwargs(
    *,
    package_name: str,
    status: SoftwareGetPackageByNameStatus,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["packageName"] = package_name

    json_status = status.value
    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/GetPackageByName",
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
    package_name: str,
    status: SoftwareGetPackageByNameStatus,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ Get Package with a given name. The one with the highest version number is returned

    Args:
        package_name (str):
        status (SoftwareGetPackageByNameStatus):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]
     """


    kwargs = _get_kwargs(
        package_name=package_name,
status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    package_name: str,
    status: SoftwareGetPackageByNameStatus,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ Get Package with a given name. The one with the highest version number is returned

    Args:
        package_name (str):
        status (SoftwareGetPackageByNameStatus):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePackage
     """


    return sync_detailed(
        client=client,
package_name=package_name,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package_name: str,
    status: SoftwareGetPackageByNameStatus,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ Get Package with a given name. The one with the highest version number is returned

    Args:
        package_name (str):
        status (SoftwareGetPackageByNameStatus):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePackage]
     """


    kwargs = _get_kwargs(
        package_name=package_name,
status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    package_name: str,
    status: SoftwareGetPackageByNameStatus,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePackage]:
    """ Get Package with a given name. The one with the highest version number is returned

    Args:
        package_name (str):
        status (SoftwareGetPackageByNameStatus):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePackage
     """


    return (await asyncio_detailed(
        client=client,
package_name=package_name,
status=status,

    )).parsed
