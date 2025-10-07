from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.process_put_repair_operation_response_200 import ProcessPutRepairOperationResponse200
from ...models.virinco_wats_interface_models_repair_type import VirincoWATSInterfaceModelsRepairType
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
    ],
    process_id: UUID,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    json_process_id = str(process_id)
    params["processId"] = json_process_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Process/PutRepairOperation",
        "params": params,
    }

    if isinstance(body, VirincoWATSInterfaceModelsRepairType):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSInterfaceModelsRepairType):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSInterfaceModelsRepairType):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProcessPutRepairOperationResponse200]:
    if response.status_code == 200:
        response_200 = ProcessPutRepairOperationResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProcessPutRepairOperationResponse200]:
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
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
    ],
    process_id: UUID,

) -> Response[ProcessPutRepairOperationResponse200]:
    """ Updates the data for a repair operation in a process.

    Args:
        process_id (UUID):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProcessPutRepairOperationResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
process_id=process_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
    ],
    process_id: UUID,

) -> Optional[ProcessPutRepairOperationResponse200]:
    """ Updates the data for a repair operation in a process.

    Args:
        process_id (UUID):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProcessPutRepairOperationResponse200
     """


    return sync_detailed(
        client=client,
body=body,
process_id=process_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
    ],
    process_id: UUID,

) -> Response[ProcessPutRepairOperationResponse200]:
    """ Updates the data for a repair operation in a process.

    Args:
        process_id (UUID):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProcessPutRepairOperationResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
process_id=process_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
        VirincoWATSInterfaceModelsRepairType,
    ],
    process_id: UUID,

) -> Optional[ProcessPutRepairOperationResponse200]:
    """ Updates the data for a repair operation in a process.

    Args:
        process_id (UUID):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):
        body (VirincoWATSInterfaceModelsRepairType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProcessPutRepairOperationResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
process_id=process_id,

    )).parsed
