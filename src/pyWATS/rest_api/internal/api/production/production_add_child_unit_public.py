from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_add_child_unit_public_response_200 import ProductionAddChildUnitPublicResponse200
from typing import cast



def _get_kwargs(
    *,
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["parentSerialNumber"] = parent_serial_number

    params["parentPartNumber"] = parent_part_number

    params["childSerialNumber"] = child_serial_number

    params["childPartNumber"] = child_part_number

    params["checkPartNumber"] = check_part_number

    params["checkRevision"] = check_revision


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Production/AddChildUnit",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionAddChildUnitPublicResponse200]:
    if response.status_code == 200:
        response_200 = ProductionAddChildUnitPublicResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionAddChildUnitPublicResponse200]:
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
    check_part_number: str,
    check_revision: str,

) -> Response[ProductionAddChildUnitPublicResponse200]:
    """ Create a parent/child relation between two units.

     Create a parent/child relation between two units.


    There are several validation rules:
    - The child unit must not already have a parent.
    - The parent unit's box build must define the child unit as valid. Alternatively the
    {checkPartNumber} and {checkRevision} parameters can be provided to override the part number and
    revision the child unit is validated against.
    - The child unit must be in phase Finalized, or its ProductRevision has the PhaseFinalized tag and
    the unit is in the specified phase. Example: PhaseFinalized tag = In Storage and unit Phase = In
    Storage is valid.
    - The relation cannot create a loop of parent/child relations.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionAddChildUnitPublicResponse200]
     """


    kwargs = _get_kwargs(
        parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,

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
    check_part_number: str,
    check_revision: str,

) -> Optional[ProductionAddChildUnitPublicResponse200]:
    """ Create a parent/child relation between two units.

     Create a parent/child relation between two units.


    There are several validation rules:
    - The child unit must not already have a parent.
    - The parent unit's box build must define the child unit as valid. Alternatively the
    {checkPartNumber} and {checkRevision} parameters can be provided to override the part number and
    revision the child unit is validated against.
    - The child unit must be in phase Finalized, or its ProductRevision has the PhaseFinalized tag and
    the unit is in the specified phase. Example: PhaseFinalized tag = In Storage and unit Phase = In
    Storage is valid.
    - The relation cannot create a loop of parent/child relations.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionAddChildUnitPublicResponse200
     """


    return sync_detailed(
        client=client,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    parent_serial_number: str,
    parent_part_number: str,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,

) -> Response[ProductionAddChildUnitPublicResponse200]:
    """ Create a parent/child relation between two units.

     Create a parent/child relation between two units.


    There are several validation rules:
    - The child unit must not already have a parent.
    - The parent unit's box build must define the child unit as valid. Alternatively the
    {checkPartNumber} and {checkRevision} parameters can be provided to override the part number and
    revision the child unit is validated against.
    - The child unit must be in phase Finalized, or its ProductRevision has the PhaseFinalized tag and
    the unit is in the specified phase. Example: PhaseFinalized tag = In Storage and unit Phase = In
    Storage is valid.
    - The relation cannot create a loop of parent/child relations.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionAddChildUnitPublicResponse200]
     """


    kwargs = _get_kwargs(
        parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,

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
    check_part_number: str,
    check_revision: str,

) -> Optional[ProductionAddChildUnitPublicResponse200]:
    """ Create a parent/child relation between two units.

     Create a parent/child relation between two units.


    There are several validation rules:
    - The child unit must not already have a parent.
    - The parent unit's box build must define the child unit as valid. Alternatively the
    {checkPartNumber} and {checkRevision} parameters can be provided to override the part number and
    revision the child unit is validated against.
    - The child unit must be in phase Finalized, or its ProductRevision has the PhaseFinalized tag and
    the unit is in the specified phase. Example: PhaseFinalized tag = In Storage and unit Phase = In
    Storage is valid.
    - The relation cannot create a loop of parent/child relations.

    Args:
        parent_serial_number (str):
        parent_part_number (str):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionAddChildUnitPublicResponse200
     """


    return (await asyncio_detailed(
        client=client,
parent_serial_number=parent_serial_number,
parent_part_number=parent_part_number,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,

    )).parsed
