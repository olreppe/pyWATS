from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.software_delete_package_folder_files_response_200 import SoftwareDeletePackageFolderFilesResponse200
from typing import cast



def _get_kwargs(
    *,
    package_folder_file_ids: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["packageFolderFileIds"] = package_folder_file_ids


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Software/DeletePackageFolderFiles",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SoftwareDeletePackageFolderFilesResponse200]:
    if response.status_code == 200:
        response_200 = SoftwareDeletePackageFolderFilesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SoftwareDeletePackageFolderFilesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package_folder_file_ids: str,

) -> Response[SoftwareDeletePackageFolderFilesResponse200]:
    """ 
    Args:
        package_folder_file_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareDeletePackageFolderFilesResponse200]
     """


    kwargs = _get_kwargs(
        package_folder_file_ids=package_folder_file_ids,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    package_folder_file_ids: str,

) -> Optional[SoftwareDeletePackageFolderFilesResponse200]:
    """ 
    Args:
        package_folder_file_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareDeletePackageFolderFilesResponse200
     """


    return sync_detailed(
        client=client,
package_folder_file_ids=package_folder_file_ids,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package_folder_file_ids: str,

) -> Response[SoftwareDeletePackageFolderFilesResponse200]:
    """ 
    Args:
        package_folder_file_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareDeletePackageFolderFilesResponse200]
     """


    kwargs = _get_kwargs(
        package_folder_file_ids=package_folder_file_ids,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    package_folder_file_ids: str,

) -> Optional[SoftwareDeletePackageFolderFilesResponse200]:
    """ 
    Args:
        package_folder_file_ids (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareDeletePackageFolderFilesResponse200
     """


    return (await asyncio_detailed(
        client=client,
package_folder_file_ids=package_folder_file_ids,

    )).parsed
