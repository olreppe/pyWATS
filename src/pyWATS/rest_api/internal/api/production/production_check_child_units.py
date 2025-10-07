from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_check_child_units_response_200 import ProductionCheckChildUnitsResponse200
from typing import cast



def _get_kwargs(
    *,
    culture_code: str,
    parent_serial_number: str,
    parent_part_number: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["CultureCode"] = culture_code

    params["ParentSerialNumber"] = parent_serial_number

    params["ParentPartNumber"] = parent_part_number


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Production/CheckChildUnits",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionCheckChildUnitsResponse200]:
    if response.status_code == 200:
        response_200 = ProductionCheckChildUnitsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionCheckChildUnitsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    parent_serial_number: str,
    parent_part_number: str,

) -> Response[ProductionCheckChildUnitsResponse200]:
    """ 
    Args:
        culture_code (str):
        parent_serial_number (str):
        parent_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionCheckChildUnitsResponse200]
     """


    kwargs = _get_kwargs(
        culture_code=culture_code,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    parent_serial_number: str,
    parent_part_number: str,

) -> Optional[ProductionCheckChildUnitsResponse200]:
    """ 
    Args:
        culture_code (str):
        parent_serial_number (str):
        parent_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionCheckChildUnitsResponse200
     """


    return sync_detailed(
        client=client,
culture_code=culture_code,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    parent_serial_number: str,
    parent_part_number: str,

) -> Response[ProductionCheckChildUnitsResponse200]:
    """ 
    Args:
        culture_code (str):
        parent_serial_number (str):
        parent_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionCheckChildUnitsResponse200]
     """


    kwargs = _get_kwargs(
        culture_code=culture_code,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    parent_serial_number: str,
    parent_part_number: str,

) -> Optional[ProductionCheckChildUnitsResponse200]:
    """ 
    Args:
        culture_code (str):
        parent_serial_number (str):
        parent_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionCheckChildUnitsResponse200
     """


    return (await asyncio_detailed(
        client=client,
culture_code=culture_code,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,

    )).parsed
