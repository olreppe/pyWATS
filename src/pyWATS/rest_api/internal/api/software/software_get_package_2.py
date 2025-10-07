from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_models_software_package import VirincoWATSModelsSoftwarePackage
from typing import cast
from uuid import UUID



def _get_kwargs(
    package_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/Packages/{package_id}".format(package_id=package_id,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSModelsSoftwarePackage]:
    if response.status_code == 200:
        response_200 = VirincoWATSModelsSoftwarePackage.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSModelsSoftwarePackage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    package_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[VirincoWATSModelsSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSModelsSoftwarePackage]
     """


    kwargs = _get_kwargs(
        package_id=package_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    package_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[VirincoWATSModelsSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSModelsSoftwarePackage
     """


    return sync_detailed(
        package_id=package_id,
client=client,

    ).parsed

async def asyncio_detailed(
    package_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[VirincoWATSModelsSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSModelsSoftwarePackage]
     """


    kwargs = _get_kwargs(
        package_id=package_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    package_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[VirincoWATSModelsSoftwarePackage]:
    """ 
    Args:
        package_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSModelsSoftwarePackage
     """


    return (await asyncio_detailed(
        package_id=package_id,
client=client,

    )).parsed
