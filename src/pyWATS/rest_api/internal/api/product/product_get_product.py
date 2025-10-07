from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.product_get_product_response_200 import ProductGetProductResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    product_id: UUID,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_product_id = str(product_id)
    params["productId"] = json_product_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Product/GetProduct",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductGetProductResponse200]:
    if response.status_code == 200:
        response_200 = ProductGetProductResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductGetProductResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    product_id: UUID,

) -> Response[ProductGetProductResponse200]:
    """ 
    Args:
        product_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductGetProductResponse200]
     """


    kwargs = _get_kwargs(
        product_id=product_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    product_id: UUID,

) -> Optional[ProductGetProductResponse200]:
    """ 
    Args:
        product_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductGetProductResponse200
     """


    return sync_detailed(
        client=client,
product_id=product_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    product_id: UUID,

) -> Response[ProductGetProductResponse200]:
    """ 
    Args:
        product_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductGetProductResponse200]
     """


    kwargs = _get_kwargs(
        product_id=product_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    product_id: UUID,

) -> Optional[ProductGetProductResponse200]:
    """ 
    Args:
        product_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductGetProductResponse200
     """


    return (await asyncio_detailed(
        client=client,
product_id=product_id,

    )).parsed
