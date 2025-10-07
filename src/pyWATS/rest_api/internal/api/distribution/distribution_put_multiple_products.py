from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_put_multiple_products_data_body import DistributionPutMultipleProductsDataBody
from ...models.distribution_put_multiple_products_json_body import DistributionPutMultipleProductsJsonBody
from ...models.distribution_put_multiple_products_response_200 import DistributionPutMultipleProductsResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        DistributionPutMultipleProductsJsonBody,
        DistributionPutMultipleProductsDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Distribution/Multi/Products",
    }

    if isinstance(body, DistributionPutMultipleProductsJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, DistributionPutMultipleProductsDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionPutMultipleProductsResponse200]:
    if response.status_code == 200:
        response_200 = DistributionPutMultipleProductsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionPutMultipleProductsResponse200]:
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
        DistributionPutMultipleProductsJsonBody,
        DistributionPutMultipleProductsDataBody,
    ],

) -> Response[DistributionPutMultipleProductsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductsJsonBody):
        body (DistributionPutMultipleProductsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMultipleProductsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DistributionPutMultipleProductsJsonBody,
        DistributionPutMultipleProductsDataBody,
    ],

) -> Optional[DistributionPutMultipleProductsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductsJsonBody):
        body (DistributionPutMultipleProductsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMultipleProductsResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DistributionPutMultipleProductsJsonBody,
        DistributionPutMultipleProductsDataBody,
    ],

) -> Response[DistributionPutMultipleProductsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductsJsonBody):
        body (DistributionPutMultipleProductsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMultipleProductsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DistributionPutMultipleProductsJsonBody,
        DistributionPutMultipleProductsDataBody,
    ],

) -> Optional[DistributionPutMultipleProductsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductsJsonBody):
        body (DistributionPutMultipleProductsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMultipleProductsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
