from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_wf_set_unit_phase_new_phase import WorkflowWFSetUnitPhaseNewPhase
from ...models.workflow_wf_set_unit_phase_response_200 import WorkflowWFSetUnitPhaseResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    native_workflow_instance_id: UUID,
    new_phase: WorkflowWFSetUnitPhaseNewPhase,
    set_phase_on_sub_units: bool,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_native_workflow_instance_id = str(native_workflow_instance_id)
    params["NativeWorkflowInstanceId"] = json_native_workflow_instance_id

    json_new_phase = new_phase.value
    params["newPhase"] = json_new_phase

    params["setPhaseOnSubUnits"] = set_phase_on_sub_units


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Workflow/WFSetUnitPhase",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowWFSetUnitPhaseResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowWFSetUnitPhaseResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowWFSetUnitPhaseResponse200]:
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
    new_phase: WorkflowWFSetUnitPhaseNewPhase,
    set_phase_on_sub_units: bool,

) -> Response[WorkflowWFSetUnitPhaseResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_phase (WorkflowWFSetUnitPhaseNewPhase):
        set_phase_on_sub_units (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFSetUnitPhaseResponse200]
     """


    kwargs = _get_kwargs(
        native_workflow_instance_id=native_workflow_instance_id,
new_phase=new_phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    native_workflow_instance_id: UUID,
    new_phase: WorkflowWFSetUnitPhaseNewPhase,
    set_phase_on_sub_units: bool,

) -> Optional[WorkflowWFSetUnitPhaseResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_phase (WorkflowWFSetUnitPhaseNewPhase):
        set_phase_on_sub_units (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFSetUnitPhaseResponse200
     """


    return sync_detailed(
        client=client,
native_workflow_instance_id=native_workflow_instance_id,
new_phase=new_phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    native_workflow_instance_id: UUID,
    new_phase: WorkflowWFSetUnitPhaseNewPhase,
    set_phase_on_sub_units: bool,

) -> Response[WorkflowWFSetUnitPhaseResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_phase (WorkflowWFSetUnitPhaseNewPhase):
        set_phase_on_sub_units (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFSetUnitPhaseResponse200]
     """


    kwargs = _get_kwargs(
        native_workflow_instance_id=native_workflow_instance_id,
new_phase=new_phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    native_workflow_instance_id: UUID,
    new_phase: WorkflowWFSetUnitPhaseNewPhase,
    set_phase_on_sub_units: bool,

) -> Optional[WorkflowWFSetUnitPhaseResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        new_phase (WorkflowWFSetUnitPhaseNewPhase):
        set_phase_on_sub_units (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFSetUnitPhaseResponse200
     """


    return (await asyncio_detailed(
        client=client,
native_workflow_instance_id=native_workflow_instance_id,
new_phase=new_phase,
set_phase_on_sub_units=set_phase_on_sub_units,

    )).parsed
