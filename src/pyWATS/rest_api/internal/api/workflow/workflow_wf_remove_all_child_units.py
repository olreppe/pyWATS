from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_wf_remove_all_child_units_data_body import WorkflowWFRemoveAllChildUnitsDataBody
from ...models.workflow_wf_remove_all_child_units_json_body import WorkflowWFRemoveAllChildUnitsJsonBody
from ...models.workflow_wf_remove_all_child_units_response_200 import WorkflowWFRemoveAllChildUnitsResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    body: Union[
        WorkflowWFRemoveAllChildUnitsJsonBody,
        WorkflowWFRemoveAllChildUnitsDataBody,
    ],
    native_workflow_instance_id: UUID,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    json_native_workflow_instance_id = str(native_workflow_instance_id)
    params["NativeWorkflowInstanceId"] = json_native_workflow_instance_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Workflow/WFRemoveAllChildUnits",
        "params": params,
    }

    if isinstance(body, WorkflowWFRemoveAllChildUnitsJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, WorkflowWFRemoveAllChildUnitsDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowWFRemoveAllChildUnitsResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowWFRemoveAllChildUnitsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowWFRemoveAllChildUnitsResponse200]:
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
        WorkflowWFRemoveAllChildUnitsJsonBody,
        WorkflowWFRemoveAllChildUnitsDataBody,
    ],
    native_workflow_instance_id: UUID,

) -> Response[WorkflowWFRemoveAllChildUnitsResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        body (WorkflowWFRemoveAllChildUnitsJsonBody):
        body (WorkflowWFRemoveAllChildUnitsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFRemoveAllChildUnitsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
native_workflow_instance_id=native_workflow_instance_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowWFRemoveAllChildUnitsJsonBody,
        WorkflowWFRemoveAllChildUnitsDataBody,
    ],
    native_workflow_instance_id: UUID,

) -> Optional[WorkflowWFRemoveAllChildUnitsResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        body (WorkflowWFRemoveAllChildUnitsJsonBody):
        body (WorkflowWFRemoveAllChildUnitsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFRemoveAllChildUnitsResponse200
     """


    return sync_detailed(
        client=client,
body=body,
native_workflow_instance_id=native_workflow_instance_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowWFRemoveAllChildUnitsJsonBody,
        WorkflowWFRemoveAllChildUnitsDataBody,
    ],
    native_workflow_instance_id: UUID,

) -> Response[WorkflowWFRemoveAllChildUnitsResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        body (WorkflowWFRemoveAllChildUnitsJsonBody):
        body (WorkflowWFRemoveAllChildUnitsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowWFRemoveAllChildUnitsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
native_workflow_instance_id=native_workflow_instance_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowWFRemoveAllChildUnitsJsonBody,
        WorkflowWFRemoveAllChildUnitsDataBody,
    ],
    native_workflow_instance_id: UUID,

) -> Optional[WorkflowWFRemoveAllChildUnitsResponse200]:
    """ 
    Args:
        native_workflow_instance_id (UUID):
        body (WorkflowWFRemoveAllChildUnitsJsonBody):
        body (WorkflowWFRemoveAllChildUnitsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowWFRemoveAllChildUnitsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
native_workflow_instance_id=native_workflow_instance_id,

    )).parsed
