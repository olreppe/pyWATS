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
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Software/Package",
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
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    r""" Create a new Package in Draft. If name exists, version will be previous version + 1.

     Rules for Tags: Key-value pair of tags in a list. Formatted like [{ \"key\": \"keyname\", \"value\":
    \"myValue\"}]. Examples: [{\"key\": \"Test_Tag\",\"value\": \"TestValue\"}], [{\"key\":
    \"Test_Tag\",\"value\": \"TestValue\"}, {\"key\": \"Test_Tag2\", \"value\": \"NewTestValue\"}]

    Args:
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    r""" Create a new Package in Draft. If name exists, version will be previous version + 1.

     Rules for Tags: Key-value pair of tags in a list. Formatted like [{ \"key\": \"keyname\", \"value\":
    \"myValue\"}]. Examples: [{\"key\": \"Test_Tag\",\"value\": \"TestValue\"}], [{\"key\":
    \"Test_Tag\",\"value\": \"TestValue\"}, {\"key\": \"Test_Tag2\", \"value\": \"NewTestValue\"}]

    Args:
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    r""" Create a new Package in Draft. If name exists, version will be previous version + 1.

     Rules for Tags: Key-value pair of tags in a list. Formatted like [{ \"key\": \"keyname\", \"value\":
    \"myValue\"}]. Examples: [{\"key\": \"Test_Tag\",\"value\": \"TestValue\"}], [{\"key\":
    \"Test_Tag\",\"value\": \"TestValue\"}, {\"key\": \"Test_Tag2\", \"value\": \"NewTestValue\"}]

    Args:
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage,
    ],

) -> Optional[VirincoWATSWebDashboardModelsMesSoftwarePublicPackage]:
    r""" Create a new Package in Draft. If name exists, version will be previous version + 1.

     Rules for Tags: Key-value pair of tags in a list. Formatted like [{ \"key\": \"keyname\", \"value\":
    \"myValue\"}]. Examples: [{\"key\": \"Test_Tag\",\"value\": \"TestValue\"}], [{\"key\":
    \"Test_Tag\",\"value\": \"TestValue\"}, {\"key\": \"Test_Tag2\", \"value\": \"NewTestValue\"}]

    Args:
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):
        body (VirincoWATSWebDashboardModelsMesSoftwarePublicPackage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsMesSoftwarePublicPackage
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
