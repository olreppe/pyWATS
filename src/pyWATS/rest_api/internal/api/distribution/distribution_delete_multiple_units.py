from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_delete_multiple_units_response_200 import DistributionDeleteMultipleUnitsResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    body: Union[
        list[UUID],
        list[UUID],
        list[UUID],
    ],
    from_site_code: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["fromSiteCode"] = from_site_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/api/internal/Distribution/Multi/Units",
        "params": params,
    }

    if isinstance(body, list[UUID]):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = str(body_item_data)
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list[UUID]):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list[UUID]):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = str(body_item_data)
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionDeleteMultipleUnitsResponse200]:
    if response.status_code == 200:
        response_200 = DistributionDeleteMultipleUnitsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionDeleteMultipleUnitsResponse200]:
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
        list[UUID],
        list[UUID],
        list[UUID],
    ],
    from_site_code: str,

) -> Response[DistributionDeleteMultipleUnitsResponse200]:
    """ 
    Args:
        from_site_code (str):
        body (list[UUID]):
        body (list[UUID]):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionDeleteMultipleUnitsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
from_site_code=from_site_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[UUID],
        list[UUID],
        list[UUID],
    ],
    from_site_code: str,

) -> Optional[DistributionDeleteMultipleUnitsResponse200]:
    """ 
    Args:
        from_site_code (str):
        body (list[UUID]):
        body (list[UUID]):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionDeleteMultipleUnitsResponse200
     """


    return sync_detailed(
        client=client,
body=body,
from_site_code=from_site_code,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[UUID],
        list[UUID],
        list[UUID],
    ],
    from_site_code: str,

) -> Response[DistributionDeleteMultipleUnitsResponse200]:
    """ 
    Args:
        from_site_code (str):
        body (list[UUID]):
        body (list[UUID]):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionDeleteMultipleUnitsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
from_site_code=from_site_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list[UUID],
        list[UUID],
        list[UUID],
    ],
    from_site_code: str,

) -> Optional[DistributionDeleteMultipleUnitsResponse200]:
    """ 
    Args:
        from_site_code (str):
        body (list[UUID]):
        body (list[UUID]):
        body (list[UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionDeleteMultipleUnitsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
from_site_code=from_site_code,

    )).parsed
