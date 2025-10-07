from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_get_unit_public_response_200 import ProductionGetUnitPublicResponse200
from typing import cast



def _get_kwargs(
    serial_number: str,
    part_number: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Production/Unit/{serial_number}/{part_number}".format(serial_number=serial_number,part_number=part_number,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionGetUnitPublicResponse200]:
    if response.status_code == 200:
        response_200 = ProductionGetUnitPublicResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionGetUnitPublicResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    serial_number: str,
    part_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ProductionGetUnitPublicResponse200]:
    """ PREVIEW - Get unit information.

     Returns information about a unit and sub-units.

    Args:
        serial_number (str):
        part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionGetUnitPublicResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    serial_number: str,
    part_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ProductionGetUnitPublicResponse200]:
    """ PREVIEW - Get unit information.

     Returns information about a unit and sub-units.

    Args:
        serial_number (str):
        part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionGetUnitPublicResponse200
     """


    return sync_detailed(
        serial_number=serial_number,
part_number=part_number,
client=client,

    ).parsed

async def asyncio_detailed(
    serial_number: str,
    part_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[ProductionGetUnitPublicResponse200]:
    """ PREVIEW - Get unit information.

     Returns information about a unit and sub-units.

    Args:
        serial_number (str):
        part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionGetUnitPublicResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    serial_number: str,
    part_number: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[ProductionGetUnitPublicResponse200]:
    """ PREVIEW - Get unit information.

     Returns information about a unit and sub-units.

    Args:
        serial_number (str):
        part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionGetUnitPublicResponse200
     """


    return (await asyncio_detailed(
        serial_number=serial_number,
part_number=part_number,
client=client,

    )).parsed
