from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.software_delete_software_package_by_name_response_200 import SoftwareDeleteSoftwarePackageByNameResponse200
from typing import cast



def _get_kwargs(
    *,
    name: str,
    version: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["name"] = name

    params["version"] = version


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/Software/PackageByName",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]:
    if response.status_code == 200:
        response_200 = SoftwareDeleteSoftwarePackageByNameResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    version: int,

) -> Response[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]:
    """ Deletes the Software Package by using name and version. Status of Software Package has to be Draft
    or Revoked before being deleted.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]
     """


    kwargs = _get_kwargs(
        name=name,
version=version,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    version: int,

) -> Optional[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]:
    """ Deletes the Software Package by using name and version. Status of Software Package has to be Draft
    or Revoked before being deleted.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]
     """


    return sync_detailed(
        client=client,
name=name,
version=version,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    version: int,

) -> Response[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]:
    """ Deletes the Software Package by using name and version. Status of Software Package has to be Draft
    or Revoked before being deleted.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]
     """


    kwargs = _get_kwargs(
        name=name,
version=version,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    name: str,
    version: int,

) -> Optional[Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]]:
    """ Deletes the Software Package by using name and version. Status of Software Package has to be Draft
    or Revoked before being deleted.

    Args:
        name (str):
        version (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, SoftwareDeleteSoftwarePackageByNameResponse200]
     """


    return (await asyncio_detailed(
        client=client,
name=name,
version=version,

    )).parsed
