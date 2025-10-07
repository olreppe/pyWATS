from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_remove_child_unit_public_response_200 import ProductionRemoveChildUnitPublicResponse200
from typing import cast



def _get_kwargs(
    *,
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["parentSerialNumber"] = parent_serial_number

    params["parentPartNumber"] = parent_part_number

    params["childSerialNumber"] = child_serial_number

    params["childPartNumber"] = child_part_number


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Production/RemoveChildUnit",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionRemoveChildUnitPublicResponse200]:
    if response.status_code == 200:
        response_200 = ProductionRemoveChildUnitPublicResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionRemoveChildUnitPublicResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,

) -> Response[ProductionRemoveChildUnitPublicResponse200]:
    """ Removes the parent/child relation between two units. The parent/child relation must already exist.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionRemoveChildUnitPublicResponse200]
     """


    kwargs = _get_kwargs(
        parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,

) -> Optional[ProductionRemoveChildUnitPublicResponse200]:
    """ Removes the parent/child relation between two units. The parent/child relation must already exist.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionRemoveChildUnitPublicResponse200
     """


    return sync_detailed(
        client=client,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,

) -> Response[ProductionRemoveChildUnitPublicResponse200]:
    """ Removes the parent/child relation between two units. The parent/child relation must already exist.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionRemoveChildUnitPublicResponse200]
     """


    kwargs = _get_kwargs(
        parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,

) -> Optional[ProductionRemoveChildUnitPublicResponse200]:
    """ Removes the parent/child relation between two units. The parent/child relation must already exist.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionRemoveChildUnitPublicResponse200
     """


    return (await asyncio_detailed(
        client=client,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,

    )).parsed
