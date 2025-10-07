from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_software_public_package import VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
from typing import cast



def _get_kwargs(
    id: str,
    *,
    status: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["status"] = status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Software/PackageStatus/{id}".format(id=id,),
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
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    status: str,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Updates the status of the Software Package defined by ID.
    Status can only go from Draft to Pending, Pending to Draft OR Released, and Released to Revoked. Any
    other configuration will be refused.

    Args:
        id (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]
     """


    kwargs = _get_kwargs(
        id=id,
status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    status: str,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Updates the status of the Software Package defined by ID.
    Status can only go from Draft to Pending, Pending to Draft OR Released, and Released to Revoked. Any
    other configuration will be refused.

    Args:
        id (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
     """


    return sync_detailed(
        id=id,
client=client,
status=status,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    status: str,

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Updates the status of the Software Package defined by ID.
    Status can only go from Draft to Pending, Pending to Draft OR Released, and Released to Revoked. Any
    other configuration will be refused.

    Args:
        id (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]
     """


    kwargs = _get_kwargs(
        id=id,
status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    status: str,

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    """ Updates the status of the Software Package defined by ID.
    Status can only go from Draft to Pending, Pending to Draft OR Released, and Released to Revoked. Any
    other configuration will be refused.

    Args:
        id (str):
        status (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
     """


    return (await asyncio_detailed(
        id=id,
client=client,
status=status,

    )).parsed
