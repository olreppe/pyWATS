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
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/Software/Package/{id}".format(id=id,),
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == 200:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> Response[Any]:
    """ Puts a Package. Note: This will overwrite existing configuration. Use POST api/Software/Package for
    new package versions.
    Package in Draft allows for editing of all details. If package is Pending or Released, only Status
    and Tags can be edited.
    Status follows these validation rules: Draft to Pending, Pending to Draft OR Released, Released to
    Revoked.
    Tags has to be in this format:
    <PackageInfo><tagName>TagValue</tagName><tagName2>TagValue2</tagName2></PackageInfo>.

     Will overwrite any existing data for this Package with the new data.

    Args:
        id (str):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> Response[Any]:
    """ Puts a Package. Note: This will overwrite existing configuration. Use POST api/Software/Package for
    new package versions.
    Package in Draft allows for editing of all details. If package is Pending or Released, only Status
    and Tags can be edited.
    Status follows these validation rules: Draft to Pending, Pending to Draft OR Released, Released to
    Revoked.
    Tags has to be in this format:
    <PackageInfo><tagName>TagValue</tagName><tagName2>TagValue2</tagName2></PackageInfo>.

     Will overwrite any existing data for this Package with the new data.

    Args:
        id (str):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

