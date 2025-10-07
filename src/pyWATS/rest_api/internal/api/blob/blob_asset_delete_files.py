from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.blob_asset_delete_files_response_200 import BlobAssetDeleteFilesResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    asset_id: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["assetId"] = asset_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/Blob/Assets",
        "params": params,
    }

    if isinstance(body, list[str]):
        _kwargs["json"] = body




        headers["Content-Type"] = "application/json"
    if isinstance(body, list[str]):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list[str]):
        _kwargs["json"] = body




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[BlobAssetDeleteFilesResponse200]:
    if response.status_code == 200:
        response_200 = BlobAssetDeleteFilesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[BlobAssetDeleteFilesResponse200]:
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
        list[str],
        list[str],
        list[str],
    ],
    asset_id: str,

) -> Response[BlobAssetDeleteFilesResponse200]:
    """ Delete Asset files

    Args:
        asset_id (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlobAssetDeleteFilesResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
asset_id=asset_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    asset_id: str,

) -> Optional[BlobAssetDeleteFilesResponse200]:
    """ Delete Asset files

    Args:
        asset_id (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlobAssetDeleteFilesResponse200
     """


    return sync_detailed(
        client=client,
body=body,
asset_id=asset_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    asset_id: str,

) -> Response[BlobAssetDeleteFilesResponse200]:
    """ Delete Asset files

    Args:
        asset_id (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BlobAssetDeleteFilesResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
asset_id=asset_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[str],
        list[str],
        list[str],
    ],
    asset_id: str,

) -> Optional[BlobAssetDeleteFilesResponse200]:
    """ Delete Asset files

    Args:
        asset_id (str):
        body (list[str]):
        body (list[str]):
        body (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BlobAssetDeleteFilesResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
asset_id=asset_id,

    )).parsed
