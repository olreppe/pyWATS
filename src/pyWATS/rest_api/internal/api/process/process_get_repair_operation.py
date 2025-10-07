from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.process_get_repair_operation_response_200 import ProcessGetRepairOperationResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    process_code: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["processCode"] = process_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Process/GetRepairOperation/{id}".format(id=id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProcessGetRepairOperationResponse200]:
    if response.status_code == 200:
        response_200 = ProcessGetRepairOperationResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProcessGetRepairOperationResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,

) -> Response[ProcessGetRepairOperationResponse200]:
    """ 
    Args:
        id (UUID):
        process_code (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProcessGetRepairOperationResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
process_code=process_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,

) -> Optional[ProcessGetRepairOperationResponse200]:
    """ 
    Args:
        id (UUID):
        process_code (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProcessGetRepairOperationResponse200
     """


    return sync_detailed(
        id=id,
client=client,
process_code=process_code,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,

) -> Response[ProcessGetRepairOperationResponse200]:
    """ 
    Args:
        id (UUID):
        process_code (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProcessGetRepairOperationResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
process_code=process_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,

) -> Optional[ProcessGetRepairOperationResponse200]:
    """ 
    Args:
        id (UUID):
        process_code (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProcessGetRepairOperationResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
process_code=process_code,

    )).parsed
