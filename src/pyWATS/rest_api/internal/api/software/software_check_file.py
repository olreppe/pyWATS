from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.software_check_file_response_200 import SoftwareCheckFileResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    checksum: str,
    parent_folder_id: UUID,
    file_path: str,
    package_id: UUID,
    file_date_epoch: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["checksum"] = checksum

    json_parent_folder_id = str(parent_folder_id)
    params["parentFolderId"] = json_parent_folder_id

    params["filePath"] = file_path

    json_package_id = str(package_id)
    params["packageId"] = json_package_id

    params["fileDateEpoch"] = file_date_epoch


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/CheckFile",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SoftwareCheckFileResponse200]:
    if response.status_code == 200:
        response_200 = SoftwareCheckFileResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SoftwareCheckFileResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    checksum: str,
    parent_folder_id: UUID,
    file_path: str,
    package_id: UUID,
    file_date_epoch: int,

) -> Response[SoftwareCheckFileResponse200]:
    """ 
    Args:
        checksum (str):
        parent_folder_id (UUID):
        file_path (str):
        package_id (UUID):
        file_date_epoch (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareCheckFileResponse200]
     """


    kwargs = _get_kwargs(
        checksum=checksum,
parent_folder_id=parent_folder_id,
file_path=file_path,
package_id=package_id,
file_date_epoch=file_date_epoch,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    checksum: str,
    parent_folder_id: UUID,
    file_path: str,
    package_id: UUID,
    file_date_epoch: int,

) -> Optional[SoftwareCheckFileResponse200]:
    """ 
    Args:
        checksum (str):
        parent_folder_id (UUID):
        file_path (str):
        package_id (UUID):
        file_date_epoch (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareCheckFileResponse200
     """


    return sync_detailed(
        client=client,
checksum=checksum,
parent_folder_id=parent_folder_id,
file_path=file_path,
package_id=package_id,
file_date_epoch=file_date_epoch,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    checksum: str,
    parent_folder_id: UUID,
    file_path: str,
    package_id: UUID,
    file_date_epoch: int,

) -> Response[SoftwareCheckFileResponse200]:
    """ 
    Args:
        checksum (str):
        parent_folder_id (UUID):
        file_path (str):
        package_id (UUID):
        file_date_epoch (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareCheckFileResponse200]
     """


    kwargs = _get_kwargs(
        checksum=checksum,
parent_folder_id=parent_folder_id,
file_path=file_path,
package_id=package_id,
file_date_epoch=file_date_epoch,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    checksum: str,
    parent_folder_id: UUID,
    file_path: str,
    package_id: UUID,
    file_date_epoch: int,

) -> Optional[SoftwareCheckFileResponse200]:
    """ 
    Args:
        checksum (str):
        parent_folder_id (UUID):
        file_path (str):
        package_id (UUID):
        file_date_epoch (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareCheckFileResponse200
     """


    return (await asyncio_detailed(
        client=client,
checksum=checksum,
parent_folder_id=parent_folder_id,
file_path=file_path,
package_id=package_id,
file_date_epoch=file_date_epoch,

    )).parsed
