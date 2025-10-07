from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.export_get_exported_file_response_200 import ExportGetExportedFileResponse200
from typing import cast



def _get_kwargs(
    file_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Export/{file_name}".format(file_name=file_name,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ExportGetExportedFileResponse200]:
    if response.status_code == 200:
        response_200 = ExportGetExportedFileResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ExportGetExportedFileResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    file_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ExportGetExportedFileResponse200]:
    """ Get file created by export wizard. A user cannot get other user's exports.

    Args:
        file_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportGetExportedFileResponse200]
     """


    kwargs = _get_kwargs(
        file_name=file_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    file_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ExportGetExportedFileResponse200]:
    """ Get file created by export wizard. A user cannot get other user's exports.

    Args:
        file_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportGetExportedFileResponse200
     """


    return sync_detailed(
        file_name=file_name,
client=client,

    ).parsed

async def asyncio_detailed(
    file_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ExportGetExportedFileResponse200]:
    """ Get file created by export wizard. A user cannot get other user's exports.

    Args:
        file_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportGetExportedFileResponse200]
     """


    kwargs = _get_kwargs(
        file_name=file_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    file_name: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ExportGetExportedFileResponse200]:
    """ Get file created by export wizard. A user cannot get other user's exports.

    Args:
        file_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportGetExportedFileResponse200
     """


    return (await asyncio_detailed(
        file_name=file_name,
client=client,

    )).parsed
