from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_wf_set_unit_process_response_200 import WorkflowWFSetUnitProcessResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    native_workflow_instance_id: UUID,
    new_process: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_native_workflow_instance_id = str(native_workflow_instance_id)
    params["NativeWorkflowInstanceId"] = json_native_workflow_instance_id

    params["newProcess"] = new_process


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Workflow/WFSetUnitProcess",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowWFSetUnitProcessResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowWFSetUnitProcessResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowWFSetUnitProcessResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    native_workflow_instance_id: UUID,
    new_process: str,

) -> Response[WorkflowWFSetUnitProcessResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_process (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFSetUnitProcessResponse200]
     """


    kwargs = _get_kwargs(
        native_workflow_instance_id=native_workflow_instance_id,
new_process=new_process,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    native_workflow_instance_id: UUID,
    new_process: str,

) -> Optional[WorkflowWFSetUnitProcessResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_process (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFSetUnitProcessResponse200
     """


    return sync_detailed(
        client=client,
native_workflow_instance_id=native_workflow_instance_id,
new_process=new_process,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    native_workflow_instance_id: UUID,
    new_process: str,

) -> Response[WorkflowWFSetUnitProcessResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_process (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFSetUnitProcessResponse200]
     """


    kwargs = _get_kwargs(
        native_workflow_instance_id=native_workflow_instance_id,
new_process=new_process,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    native_workflow_instance_id: UUID,
    new_process: str,

) -> Optional[WorkflowWFSetUnitProcessResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_process (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFSetUnitProcessResponse200
     """


    return (await asyncio_detailed(
        client=client,
native_workflow_instance_id=native_workflow_instance_id,
new_process=new_process,

    )).parsed
