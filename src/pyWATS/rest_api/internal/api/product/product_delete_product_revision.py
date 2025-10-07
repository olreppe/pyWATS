from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.product_delete_product_revision_response_200 import ProductDeleteProductRevisionResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    product_revision_id: UUID,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_product_revision_id = str(product_revision_id)
    params["productRevisionId"] = json_product_revision_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/Product/DeleteProductRevision",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductDeleteProductRevisionResponse200]:
    if response.status_code == 200:
        response_200 = ProductDeleteProductRevisionResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductDeleteProductRevisionResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    product_revision_id: UUID,

) -> Response[ProductDeleteProductRevisionResponse200]:
    """ 
    Args:
        product_revision_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductDeleteProductRevisionResponse200]
     """


    kwargs = _get_kwargs(
        product_revision_id=product_revision_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    product_revision_id: UUID,

) -> Optional[ProductDeleteProductRevisionResponse200]:
    """ 
    Args:
        product_revision_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductDeleteProductRevisionResponse200
     """


    return sync_detailed(
        client=client,
product_revision_id=product_revision_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    product_revision_id: UUID,

) -> Response[ProductDeleteProductRevisionResponse200]:
    """ 
    Args:
        product_revision_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductDeleteProductRevisionResponse200]
     """


    kwargs = _get_kwargs(
        product_revision_id=product_revision_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    product_revision_id: UUID,

) -> Optional[ProductDeleteProductRevisionResponse200]:
    """ 
    Args:
        product_revision_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductDeleteProductRevisionResponse200
     """


    return (await asyncio_detailed(
        client=client,
product_revision_id=product_revision_id,

    )).parsed
