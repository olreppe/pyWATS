from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_wf_add_child_unit_data_body import WorkflowWFAddChildUnitDataBody
from ...models.workflow_wf_add_child_unit_json_body import WorkflowWFAddChildUnitJsonBody
from ...models.workflow_wf_add_child_unit_response_200 import WorkflowWFAddChildUnitResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    body: Union[
        WorkflowWFAddChildUnitJsonBody,
        WorkflowWFAddChildUnitDataBody,
    ],
    native_workflow_instance_id: UUID,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    json_native_workflow_instance_id = str(native_workflow_instance_id)
    params["NativeWorkflowInstanceId"] = json_native_workflow_instance_id

    params["ChildSerialNumber"] = child_serial_number

    params["ChildPartNumber"] = child_part_number

    params["CheckPartNumber"] = check_part_number

    params["CheckRevision"] = check_revision


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Workflow/WFAddChildUnit",
        "params": params,
    }

    if isinstance(body, WorkflowWFAddChildUnitJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, WorkflowWFAddChildUnitDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowWFAddChildUnitResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowWFAddChildUnitResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowWFAddChildUnitResponse200]:
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
        WorkflowWFAddChildUnitJsonBody,
        WorkflowWFAddChildUnitDataBody,
    ],
    native_workflow_instance_id: UUID,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,

) -> Response[WorkflowWFAddChildUnitResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        body (WorkflowWFAddChildUnitJsonBody):
        body (WorkflowWFAddChildUnitDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFAddChildUnitResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
native_workflow_instance_id=native_workflow_instance_id,
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
    body: Union[
        WorkflowWFAddChildUnitJsonBody,
        WorkflowWFAddChildUnitDataBody,
    ],
    native_workflow_instance_id: UUID,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,

) -> Optional[WorkflowWFAddChildUnitResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        body (WorkflowWFAddChildUnitJsonBody):
        body (WorkflowWFAddChildUnitDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFAddChildUnitResponse200
     """


    return sync_detailed(
        client=client,
body=body,
native_workflow_instance_id=native_workflow_instance_id,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowWFAddChildUnitJsonBody,
        WorkflowWFAddChildUnitDataBody,
    ],
    native_workflow_instance_id: UUID,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,

) -> Response[WorkflowWFAddChildUnitResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        body (WorkflowWFAddChildUnitJsonBody):
        body (WorkflowWFAddChildUnitDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFAddChildUnitResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
native_workflow_instance_id=native_workflow_instance_id,
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
    body: Union[
        WorkflowWFAddChildUnitJsonBody,
        WorkflowWFAddChildUnitDataBody,
    ],
    native_workflow_instance_id: UUID,
    child_serial_number: str,
    child_part_number: str,
    check_part_number: str,
    check_revision: str,

) -> Optional[WorkflowWFAddChildUnitResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        child_serial_number (str):
        child_part_number (str):
        check_part_number (str):
        check_revision (str):
        body (WorkflowWFAddChildUnitJsonBody):
        body (WorkflowWFAddChildUnitDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFAddChildUnitResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
native_workflow_instance_id=native_workflow_instance_id,
child_serial_number=child_serial_number,
child_part_number=child_part_number,
check_part_number=check_part_number,
check_revision=check_revision,

    )).parsed
