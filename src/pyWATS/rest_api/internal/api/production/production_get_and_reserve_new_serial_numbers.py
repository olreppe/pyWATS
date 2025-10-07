from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_get_and_reserve_new_serial_numbers_data_body import ProductionGetAndReserveNewSerialNumbersDataBody
from ...models.production_get_and_reserve_new_serial_numbers_json_body import ProductionGetAndReserveNewSerialNumbersJsonBody
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        ProductionGetAndReserveNewSerialNumbersJsonBody,
        ProductionGetAndReserveNewSerialNumbersDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Production/GetAndReserveNewSerialNumbers",
    }

    if isinstance(body, ProductionGetAndReserveNewSerialNumbersJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, ProductionGetAndReserveNewSerialNumbersDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
        ProductionGetAndReserveNewSerialNumbersJsonBody,
        ProductionGetAndReserveNewSerialNumbersDataBody,
    ],

) -> Response[Any]:
    """ Gets and reserves new serial numbers (Take/Reserve). In use in WATS Client.

    Args:
        body (ProductionGetAndReserveNewSerialNumbersJsonBody):
        body (ProductionGetAndReserveNewSerialNumbersDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ProductionGetAndReserveNewSerialNumbersJsonBody,
        ProductionGetAndReserveNewSerialNumbersDataBody,
    ],

) -> Response[Any]:
    """ Gets and reserves new serial numbers (Take/Reserve). In use in WATS Client.

    Args:
        body (ProductionGetAndReserveNewSerialNumbersJsonBody):
        body (ProductionGetAndReserveNewSerialNumbersDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

