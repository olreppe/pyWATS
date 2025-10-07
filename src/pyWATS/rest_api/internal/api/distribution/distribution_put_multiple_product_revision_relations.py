from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_put_multiple_product_revision_relations_data_body import DistributionPutMultipleProductRevisionRelationsDataBody
from ...models.distribution_put_multiple_product_revision_relations_json_body import DistributionPutMultipleProductRevisionRelationsJsonBody
from ...models.distribution_put_multiple_product_revision_relations_response_200 import DistributionPutMultipleProductRevisionRelationsResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        DistributionPutMultipleProductRevisionRelationsJsonBody,
        DistributionPutMultipleProductRevisionRelationsDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Distribution/Multi/Products/Revisions/Relations",
    }

    if isinstance(body, DistributionPutMultipleProductRevisionRelationsJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, DistributionPutMultipleProductRevisionRelationsDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionPutMultipleProductRevisionRelationsResponse200]:
    if response.status_code == 200:
        response_200 = DistributionPutMultipleProductRevisionRelationsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionPutMultipleProductRevisionRelationsResponse200]:
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
        DistributionPutMultipleProductRevisionRelationsJsonBody,
        DistributionPutMultipleProductRevisionRelationsDataBody,
    ],

) -> Response[DistributionPutMultipleProductRevisionRelationsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductRevisionRelationsJsonBody):
        body (DistributionPutMultipleProductRevisionRelationsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMultipleProductRevisionRelationsResponse200]
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
        DistributionPutMultipleProductRevisionRelationsJsonBody,
        DistributionPutMultipleProductRevisionRelationsDataBody,
    ],

) -> Optional[DistributionPutMultipleProductRevisionRelationsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductRevisionRelationsJsonBody):
        body (DistributionPutMultipleProductRevisionRelationsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMultipleProductRevisionRelationsResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DistributionPutMultipleProductRevisionRelationsJsonBody,
        DistributionPutMultipleProductRevisionRelationsDataBody,
    ],

) -> Response[DistributionPutMultipleProductRevisionRelationsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductRevisionRelationsJsonBody):
        body (DistributionPutMultipleProductRevisionRelationsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMultipleProductRevisionRelationsResponse200]
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
        DistributionPutMultipleProductRevisionRelationsJsonBody,
        DistributionPutMultipleProductRevisionRelationsDataBody,
    ],

) -> Optional[DistributionPutMultipleProductRevisionRelationsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleProductRevisionRelationsJsonBody):
        body (DistributionPutMultipleProductRevisionRelationsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMultipleProductRevisionRelationsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
