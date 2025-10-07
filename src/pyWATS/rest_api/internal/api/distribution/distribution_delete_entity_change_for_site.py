from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_delete_entity_change_for_site_response_200 import DistributionDeleteEntityChangeForSiteResponse200
from typing import cast



def _get_kwargs(
    site_code: str,
    entity_type: str,
    entity_id: str,
    *,
    body: Union[
        str,
        str,
        str,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/Distribution/Changes/{site_code}/{entity_type}/{entity_id}".format(site_code=site_code,entity_type=entity_type,entity_id=entity_id,),
    }

    if isinstance(body, str):
        _kwargs["json"] = body


        headers["Content-Type"] = "application/json"
    if isinstance(body, str):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, str):
        _kwargs["json"] = body


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionDeleteEntityChangeForSiteResponse200]:
    if response.status_code == 200:
        response_200 = DistributionDeleteEntityChangeForSiteResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionDeleteEntityChangeForSiteResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    site_code: str,
    entity_type: str,
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],

) -> Response[DistributionDeleteEntityChangeForSiteResponse200]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        entity_id (str):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionDeleteEntityChangeForSiteResponse200]
     """


    kwargs = _get_kwargs(
        site_code=site_code,
entity_type=entity_type,
entity_id=entity_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    site_code: str,
    entity_type: str,
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],

) -> Optional[DistributionDeleteEntityChangeForSiteResponse200]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        entity_id (str):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionDeleteEntityChangeForSiteResponse200
     """


    return sync_detailed(
        site_code=site_code,
entity_type=entity_type,
entity_id=entity_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    site_code: str,
    entity_type: str,
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],

) -> Response[DistributionDeleteEntityChangeForSiteResponse200]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        entity_id (str):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionDeleteEntityChangeForSiteResponse200]
     """


    kwargs = _get_kwargs(
        site_code=site_code,
entity_type=entity_type,
entity_id=entity_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    site_code: str,
    entity_type: str,
    entity_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        str,
        str,
        str,
    ],

) -> Optional[DistributionDeleteEntityChangeForSiteResponse200]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        entity_id (str):
        body (str):
        body (str):
        body (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionDeleteEntityChangeForSiteResponse200
     """


    return (await asyncio_detailed(
        site_code=site_code,
entity_type=entity_type,
entity_id=entity_id,
client=client,
body=body,

    )).parsed
