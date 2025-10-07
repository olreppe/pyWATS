from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.product_put_bom_response_200 import ProductPutBomResponse200
from typing import cast



def _get_kwargs(
    *,
    part_number: str,
    revision: str,
    format_: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["partNumber"] = part_number

    params["revision"] = revision

    params["format"] = format_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Product/BOM",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductPutBomResponse200]:
    if response.status_code == 200:
        response_200 = ProductPutBomResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductPutBomResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    format_: str,

) -> Response[ProductPutBomResponse200]:
    """ 
    Args:
        part_number (str):
        revision (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductPutBomResponse200]
     """


    kwargs = _get_kwargs(
        part_number=part_number,
revision=revision,
format_=format_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    format_: str,

) -> Optional[ProductPutBomResponse200]:
    """ 
    Args:
        part_number (str):
        revision (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductPutBomResponse200
     """


    return sync_detailed(
        client=client,
part_number=part_number,
revision=revision,
format_=format_,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    format_: str,

) -> Response[ProductPutBomResponse200]:
    """ 
    Args:
        part_number (str):
        revision (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductPutBomResponse200]
     """


    kwargs = _get_kwargs(
        part_number=part_number,
revision=revision,
format_=format_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    format_: str,

) -> Optional[ProductPutBomResponse200]:
    """ 
    Args:
        part_number (str):
        revision (str):
        format_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductPutBomResponse200
     """


    return (await asyncio_detailed(
        client=client,
part_number=part_number,
revision=revision,
format_=format_,

    )).parsed
