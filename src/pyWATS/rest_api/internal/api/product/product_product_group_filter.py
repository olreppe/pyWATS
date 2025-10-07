from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.product_product_group_filter_response_200 import ProductProductGroupFilterResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    product_group: str,
    part_number: str,
    revision: Union[Unset, str] = UNSET,
    exclude: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["productGroup"] = product_group

    params["partNumber"] = part_number

    params["revision"] = revision

    params["exclude"] = exclude


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Product/ProductGroupFilter",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductProductGroupFilterResponse200]:
    if response.status_code == 200:
        response_200 = ProductProductGroupFilterResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductProductGroupFilterResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    product_group: str,
    part_number: str,
    revision: Union[Unset, str] = UNSET,
    exclude: Union[Unset, bool] = UNSET,

) -> Response[ProductProductGroupFilterResponse200]:
    """ Add a product group filter to a pre-existing product group.

    Args:
        product_group (str):
        part_number (str):
        revision (Union[Unset, str]):
        exclude (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductProductGroupFilterResponse200]
     """


    kwargs = _get_kwargs(
        product_group=product_group,
part_number=part_number,
revision=revision,
exclude=exclude,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    product_group: str,
    part_number: str,
    revision: Union[Unset, str] = UNSET,
    exclude: Union[Unset, bool] = UNSET,

) -> Optional[ProductProductGroupFilterResponse200]:
    """ Add a product group filter to a pre-existing product group.

    Args:
        product_group (str):
        part_number (str):
        revision (Union[Unset, str]):
        exclude (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductProductGroupFilterResponse200
     """


    return sync_detailed(
        client=client,
product_group=product_group,
part_number=part_number,
revision=revision,
exclude=exclude,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    product_group: str,
    part_number: str,
    revision: Union[Unset, str] = UNSET,
    exclude: Union[Unset, bool] = UNSET,

) -> Response[ProductProductGroupFilterResponse200]:
    """ Add a product group filter to a pre-existing product group.

    Args:
        product_group (str):
        part_number (str):
        revision (Union[Unset, str]):
        exclude (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductProductGroupFilterResponse200]
     """


    kwargs = _get_kwargs(
        product_group=product_group,
part_number=part_number,
revision=revision,
exclude=exclude,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    product_group: str,
    part_number: str,
    revision: Union[Unset, str] = UNSET,
    exclude: Union[Unset, bool] = UNSET,

) -> Optional[ProductProductGroupFilterResponse200]:
    """ Add a product group filter to a pre-existing product group.

    Args:
        product_group (str):
        part_number (str):
        revision (Union[Unset, str]):
        exclude (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductProductGroupFilterResponse200
     """


    return (await asyncio_detailed(
        client=client,
product_group=product_group,
part_number=part_number,
revision=revision,
exclude=exclude,

    )).parsed
