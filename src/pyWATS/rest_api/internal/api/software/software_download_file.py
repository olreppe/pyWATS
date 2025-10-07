from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.software_download_file_response_200 import SoftwareDownloadFileResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    repository_folder_file_id: UUID,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_repository_folder_file_id = str(repository_folder_file_id)
    params["repositoryFolderFileId"] = json_repository_folder_file_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/DownloadFile",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SoftwareDownloadFileResponse200]:
    if response.status_code == 200:
        response_200 = SoftwareDownloadFileResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SoftwareDownloadFileResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    repository_folder_file_id: UUID,

) -> Response[SoftwareDownloadFileResponse200]:
    """ Initiates a download from server to client

    Args:
        repository_folder_file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareDownloadFileResponse200]
     """


    kwargs = _get_kwargs(
        repository_folder_file_id=repository_folder_file_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    repository_folder_file_id: UUID,

) -> Optional[SoftwareDownloadFileResponse200]:
    """ Initiates a download from server to client

    Args:
        repository_folder_file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareDownloadFileResponse200
     """


    return sync_detailed(
        client=client,
repository_folder_file_id=repository_folder_file_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    repository_folder_file_id: UUID,

) -> Response[SoftwareDownloadFileResponse200]:
    """ Initiates a download from server to client

    Args:
        repository_folder_file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareDownloadFileResponse200]
     """


    kwargs = _get_kwargs(
        repository_folder_file_id=repository_folder_file_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    repository_folder_file_id: UUID,

) -> Optional[SoftwareDownloadFileResponse200]:
    """ Initiates a download from server to client

    Args:
        repository_folder_file_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareDownloadFileResponse200
     """


    return (await asyncio_detailed(
        client=client,
repository_folder_file_id=repository_folder_file_id,

    )).parsed
