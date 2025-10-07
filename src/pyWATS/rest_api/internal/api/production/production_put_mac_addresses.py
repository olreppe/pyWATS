from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_put_mac_addresses_response_200 import ProductionPutMACAddressesResponse200
from typing import cast



def _get_kwargs(
    *,
    serial_number_type: str,
    start_address: str,
    end_address: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumberType"] = serial_number_type

    params["startAddress"] = start_address

    params["endAddress"] = end_address


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Production/SerialNumbers/Generate",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionPutMACAddressesResponse200]:
    if response.status_code == 200:
        response_200 = ProductionPutMACAddressesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionPutMACAddressesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    start_address: str,
    end_address: str,

) -> Response[ProductionPutMACAddressesResponse200]:
    """ Generates a new MAC range. Only for MAC-like types.

    Args:
        serial_number_type (str):
        start_address (str):
        end_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionPutMACAddressesResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    start_address: str,
    end_address: str,

) -> Optional[ProductionPutMACAddressesResponse200]:
    """ Generates a new MAC range. Only for MAC-like types.

    Args:
        serial_number_type (str):
        start_address (str):
        end_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionPutMACAddressesResponse200
     """


    return sync_detailed(
        client=client,
serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    start_address: str,
    end_address: str,

) -> Response[ProductionPutMACAddressesResponse200]:
    """ Generates a new MAC range. Only for MAC-like types.

    Args:
        serial_number_type (str):
        start_address (str):
        end_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionPutMACAddressesResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    start_address: str,
    end_address: str,

) -> Optional[ProductionPutMACAddressesResponse200]:
    """ Generates a new MAC range. Only for MAC-like types.

    Args:
        serial_number_type (str):
        start_address (str):
        end_address (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionPutMACAddressesResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,

    )).parsed
