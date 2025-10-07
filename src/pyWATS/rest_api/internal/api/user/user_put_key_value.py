from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user_put_key_value_data_body import UserPutKeyValueDataBody
from ...models.user_put_key_value_json_body import UserPutKeyValueJsonBody
from ...models.user_put_key_value_response_200 import UserPutKeyValueResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        UserPutKeyValueJsonBody,
        UserPutKeyValueDataBody,
    ],
    key: str,
    json: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["key"] = key

    params["JSON"] = json


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/User/PutKeyValue",
        "params": params,
    }

    if isinstance(body, UserPutKeyValueJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, UserPutKeyValueDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UserPutKeyValueResponse200]:
    if response.status_code == 200:
        response_200 = UserPutKeyValueResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UserPutKeyValueResponse200]:
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
        UserPutKeyValueJsonBody,
        UserPutKeyValueDataBody,
    ],
    key: str,
    json: Union[Unset, bool] = UNSET,

) -> Response[UserPutKeyValueResponse200]:
    """ 
    Args:
        key (str):
        json (Union[Unset, bool]):
        body (UserPutKeyValueJsonBody):
        body (UserPutKeyValueDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPutKeyValueResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
key=key,
json=json,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UserPutKeyValueJsonBody,
        UserPutKeyValueDataBody,
    ],
    key: str,
    json: Union[Unset, bool] = UNSET,

) -> Optional[UserPutKeyValueResponse200]:
    """ 
    Args:
        key (str):
        json (Union[Unset, bool]):
        body (UserPutKeyValueJsonBody):
        body (UserPutKeyValueDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPutKeyValueResponse200
     """


    return sync_detailed(
        client=client,
body=body,
key=key,
json=json,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UserPutKeyValueJsonBody,
        UserPutKeyValueDataBody,
    ],
    key: str,
    json: Union[Unset, bool] = UNSET,

) -> Response[UserPutKeyValueResponse200]:
    """ 
    Args:
        key (str):
        json (Union[Unset, bool]):
        body (UserPutKeyValueJsonBody):
        body (UserPutKeyValueDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPutKeyValueResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
key=key,
json=json,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UserPutKeyValueJsonBody,
        UserPutKeyValueDataBody,
    ],
    key: str,
    json: Union[Unset, bool] = UNSET,

) -> Optional[UserPutKeyValueResponse200]:
    """ 
    Args:
        key (str):
        json (Union[Unset, bool]):
        body (UserPutKeyValueJsonBody):
        body (UserPutKeyValueDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPutKeyValueResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
key=key,
json=json,

    )).parsed
