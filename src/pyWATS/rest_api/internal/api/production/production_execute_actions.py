from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_execute_actions_data_body import ProductionExecuteActionsDataBody
from ...models.production_execute_actions_json_body import ProductionExecuteActionsJsonBody
from ...models.production_execute_actions_response_200 import ProductionExecuteActionsResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        ProductionExecuteActionsJsonBody,
        ProductionExecuteActionsDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Production/ExecuteActions",
    }

    if isinstance(body, ProductionExecuteActionsJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, ProductionExecuteActionsDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionExecuteActionsResponse200]:
    if response.status_code == 200:
        response_200 = ProductionExecuteActionsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionExecuteActionsResponse200]:
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
        ProductionExecuteActionsJsonBody,
        ProductionExecuteActionsDataBody,
    ],

) -> Response[ProductionExecuteActionsResponse200]:
    """ Executes pending unit actions based on parameters

    Args:
        body (ProductionExecuteActionsJsonBody):
        body (ProductionExecuteActionsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionExecuteActionsResponse200]
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
        ProductionExecuteActionsJsonBody,
        ProductionExecuteActionsDataBody,
    ],

) -> Optional[ProductionExecuteActionsResponse200]:
    """ Executes pending unit actions based on parameters

    Args:
        body (ProductionExecuteActionsJsonBody):
        body (ProductionExecuteActionsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionExecuteActionsResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ProductionExecuteActionsJsonBody,
        ProductionExecuteActionsDataBody,
    ],

) -> Response[ProductionExecuteActionsResponse200]:
    """ Executes pending unit actions based on parameters

    Args:
        body (ProductionExecuteActionsJsonBody):
        body (ProductionExecuteActionsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionExecuteActionsResponse200]
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
        ProductionExecuteActionsJsonBody,
        ProductionExecuteActionsDataBody,
    ],

) -> Optional[ProductionExecuteActionsResponse200]:
    """ Executes pending unit actions based on parameters

    Args:
        body (ProductionExecuteActionsJsonBody):
        body (ProductionExecuteActionsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionExecuteActionsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
