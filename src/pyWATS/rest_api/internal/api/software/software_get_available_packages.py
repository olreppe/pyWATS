from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
from typing import cast



def _get_kwargs(
    *,
    installed_packages: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["installedPackages"] = installed_packages


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/GetAvailablePackages",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMesSoftwarePackage.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    installed_packages: str,

) -> Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Check server for new version of installed packages

    Args:
        installed_packages (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]
     """


    kwargs = _get_kwargs(
        installed_packages=installed_packages,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    installed_packages: str,

) -> Optional[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Check server for new version of installed packages

    Args:
        installed_packages (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesSoftwarePackage']
     """


    return sync_detailed(
        client=client,
installed_packages=installed_packages,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    installed_packages: str,

) -> Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Check server for new version of installed packages

    Args:
        installed_packages (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]
     """


    kwargs = _get_kwargs(
        installed_packages=installed_packages,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    installed_packages: str,

) -> Optional[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Check server for new version of installed packages

    Args:
        installed_packages (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesSoftwarePackage']
     """


    return (await asyncio_detailed(
        client=client,
installed_packages=installed_packages,

    )).parsed
