from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.client_update_put_client_update_data_body import ClientUpdatePutClientUpdateDataBody
from ...models.client_update_put_client_update_json_body import ClientUpdatePutClientUpdateJsonBody
from ...models.client_update_put_client_update_response_200 import ClientUpdatePutClientUpdateResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        ClientUpdatePutClientUpdateJsonBody,
        ClientUpdatePutClientUpdateDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/ClientUpdate/PutClientUpdate",
    }

    if isinstance(body, ClientUpdatePutClientUpdateJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, ClientUpdatePutClientUpdateDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ClientUpdatePutClientUpdateResponse200]:
    if response.status_code == 200:
        response_200 = ClientUpdatePutClientUpdateResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ClientUpdatePutClientUpdateResponse200]:
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
        ClientUpdatePutClientUpdateJsonBody,
        ClientUpdatePutClientUpdateDataBody,
    ],

) -> Response[ClientUpdatePutClientUpdateResponse200]:
    """ Updates an existing client update file - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePutClientUpdateJsonBody):
        body (ClientUpdatePutClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientUpdatePutClientUpdateResponse200]
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
        ClientUpdatePutClientUpdateJsonBody,
        ClientUpdatePutClientUpdateDataBody,
    ],

) -> Optional[ClientUpdatePutClientUpdateResponse200]:
    """ Updates an existing client update file - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePutClientUpdateJsonBody):
        body (ClientUpdatePutClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientUpdatePutClientUpdateResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ClientUpdatePutClientUpdateJsonBody,
        ClientUpdatePutClientUpdateDataBody,
    ],

) -> Response[ClientUpdatePutClientUpdateResponse200]:
    """ Updates an existing client update file - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePutClientUpdateJsonBody):
        body (ClientUpdatePutClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ClientUpdatePutClientUpdateResponse200]
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
        ClientUpdatePutClientUpdateJsonBody,
        ClientUpdatePutClientUpdateDataBody,
    ],

) -> Optional[ClientUpdatePutClientUpdateResponse200]:
    """ Updates an existing client update file - NOT IMPLEMENTED

    Args:
        body (ClientUpdatePutClientUpdateJsonBody):
        body (ClientUpdatePutClientUpdateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ClientUpdatePutClientUpdateResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
