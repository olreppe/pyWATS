from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user_delete_user_folder_response_200 import UserDeleteUserFolderResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    folder_id: UUID,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_folder_id = str(folder_id)
    params["folderId"] = json_folder_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/User/DeleteUserFolder",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UserDeleteUserFolderResponse200]:
    if response.status_code == 200:
        response_200 = UserDeleteUserFolderResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UserDeleteUserFolderResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    folder_id: UUID,

) -> Response[UserDeleteUserFolderResponse200]:
    """ Deletes a user folder.

    Args:
        folder_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDeleteUserFolderResponse200]
     """


    kwargs = _get_kwargs(
        folder_id=folder_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    folder_id: UUID,

) -> Optional[UserDeleteUserFolderResponse200]:
    """ Deletes a user folder.

    Args:
        folder_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDeleteUserFolderResponse200
     """


    return sync_detailed(
        client=client,
folder_id=folder_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    folder_id: UUID,

) -> Response[UserDeleteUserFolderResponse200]:
    """ Deletes a user folder.

    Args:
        folder_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserDeleteUserFolderResponse200]
     """


    kwargs = _get_kwargs(
        folder_id=folder_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    folder_id: UUID,

) -> Optional[UserDeleteUserFolderResponse200]:
    """ Deletes a user folder.

    Args:
        folder_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserDeleteUserFolderResponse200
     """


    return (await asyncio_detailed(
        client=client,
folder_id=folder_id,

    )).parsed
