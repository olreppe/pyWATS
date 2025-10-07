from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_update_post_client_update_data_body import ClientUpdatePostClientUpdateDataBody
from ...models.client_update_post_client_update_json_body import ClientUpdatePostClientUpdateJsonBody
from ...models.client_update_post_client_update_response_200 import ClientUpdatePostClientUpdateResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        ClientUpdatePostClientUpdateJsonBody,
        ClientUpdatePostClientUpdateDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/ClientUpdate/PostClientUpdate",
    }

    if isinstance(body, ClientUpdatePostClientUpdateJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, ClientUpdatePostClientUpdateDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ClientUpdatePostClientUpdateResponse200]:
    if response.status_code == 200:
        response_200 = ClientUpdatePostClientUpdateResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ClientUpdatePostClientUpdateResponse200]:
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
        ClientUpdatePostClientUpdateJsonBody,
        ClientUpdatePostClientUpdateDataBody,
    ],

) -> Response[ClientUpdatePostClientUpdateResponse200]:
    """ Inserts a new client update - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePostClientUpdateJsonBody):
        body (ClientUpdatePostClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientUpdatePostClientUpdateResponse200]
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
        ClientUpdatePostClientUpdateJsonBody,
        ClientUpdatePostClientUpdateDataBody,
    ],

) -> Optional[ClientUpdatePostClientUpdateResponse200]:
    """ Inserts a new client update - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePostClientUpdateJsonBody):
        body (ClientUpdatePostClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientUpdatePostClientUpdateResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ClientUpdatePostClientUpdateJsonBody,
        ClientUpdatePostClientUpdateDataBody,
    ],

) -> Response[ClientUpdatePostClientUpdateResponse200]:
    """ Inserts a new client update - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePostClientUpdateJsonBody):
        body (ClientUpdatePostClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientUpdatePostClientUpdateResponse200]
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
        ClientUpdatePostClientUpdateJsonBody,
        ClientUpdatePostClientUpdateDataBody,
    ],

) -> Optional[ClientUpdatePostClientUpdateResponse200]:
    """ Inserts a new client update - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePostClientUpdateJsonBody):
        body (ClientUpdatePostClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientUpdatePostClientUpdateResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
