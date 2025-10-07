from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_reset_asset_counter_response_200 import AssetResetAssetCounterResponse200
from typing import cast



def _get_kwargs(
    id: str,
    *,
    comment: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["comment"] = comment


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Asset/Reset/{id}".format(id=id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetResetAssetCounterResponse200]:
    if response.status_code == 200:
        response_200 = AssetResetAssetCounterResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetResetAssetCounterResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    comment: str,

) -> Response[AssetResetAssetCounterResponse200]:
    """ 
    Args:
        id (str):
        comment (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetResetAssetCounterResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
comment=comment,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    comment: str,

) -> Optional[AssetResetAssetCounterResponse200]:
    """ 
    Args:
        id (str):
        comment (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetResetAssetCounterResponse200
     """


    return sync_detailed(
        id=id,
client=client,
comment=comment,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    comment: str,

) -> Response[AssetResetAssetCounterResponse200]:
    """ 
    Args:
        id (str):
        comment (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetResetAssetCounterResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
comment=comment,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    comment: str,

) -> Optional[AssetResetAssetCounterResponse200]:
    """ 
    Args:
        id (str):
        comment (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetResetAssetCounterResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
comment=comment,

    )).parsed
