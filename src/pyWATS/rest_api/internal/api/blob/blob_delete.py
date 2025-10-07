from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.blob_delete_response_200 import BlobDeleteResponse200
from typing import cast



def _get_kwargs(
    identifier: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/Blob/clientlog/{identifier}".format(identifier=identifier,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[BlobDeleteResponse200]:
    if response.status_code == 200:
        response_200 = BlobDeleteResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[BlobDeleteResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[BlobDeleteResponse200]:
    """ Delete client log for specified client (6.0 or newer)
    Deleting the log should only be done if the client is being removed/moved or renamed .

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlobDeleteResponse200]
     """


    kwargs = _get_kwargs(
        identifier=identifier,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[BlobDeleteResponse200]:
    """ Delete client log for specified client (6.0 or newer)
    Deleting the log should only be done if the client is being removed/moved or renamed .

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlobDeleteResponse200
     """


    return sync_detailed(
        identifier=identifier,
client=client,

    ).parsed

async def asyncio_detailed(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[BlobDeleteResponse200]:
    """ Delete client log for specified client (6.0 or newer)
    Deleting the log should only be done if the client is being removed/moved or renamed .

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlobDeleteResponse200]
     """


    kwargs = _get_kwargs(
        identifier=identifier,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    identifier: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[BlobDeleteResponse200]:
    """ Delete client log for specified client (6.0 or newer)
    Deleting the log should only be done if the client is being removed/moved or renamed .

    Args:
        identifier (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlobDeleteResponse200
     """


    return (await asyncio_detailed(
        identifier=identifier,
client=client,

    )).parsed
