from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_workflow_workflow_definition import VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition
from ...models.workflow_post_definition_response_200 import WorkflowPostDefinitionResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
    ],
    return_as_production_manager_entity: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["returnAsProductionManagerEntity"] = return_as_production_manager_entity


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Workflow/PostDefinition",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowPostDefinitionResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowPostDefinitionResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowPostDefinitionResponse200]:
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
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
    ],
    return_as_production_manager_entity: Union[Unset, bool] = UNSET,

) -> Response[WorkflowPostDefinitionResponse200]:
    """ 
    Args:
        return_as_production_manager_entity (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowPostDefinitionResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
return_as_production_manager_entity=return_as_production_manager_entity,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
    ],
    return_as_production_manager_entity: Union[Unset, bool] = UNSET,

) -> Optional[WorkflowPostDefinitionResponse200]:
    """ 
    Args:
        return_as_production_manager_entity (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowPostDefinitionResponse200
     """


    return sync_detailed(
        client=client,
body=body,
return_as_production_manager_entity=return_as_production_manager_entity,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
    ],
    return_as_production_manager_entity: Union[Unset, bool] = UNSET,

) -> Response[WorkflowPostDefinitionResponse200]:
    """ 
    Args:
        return_as_production_manager_entity (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowPostDefinitionResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
return_as_production_manager_entity=return_as_production_manager_entity,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
        VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition,
    ],
    return_as_production_manager_entity: Union[Unset, bool] = UNSET,

) -> Optional[WorkflowPostDefinitionResponse200]:
    """ 
    Args:
        return_as_production_manager_entity (Union[Unset, bool]):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):
        body (VirincoWATSWebDashboardModelsMesWorkflowWorkflowDefinition):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowPostDefinitionResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
return_as_production_manager_entity=return_as_production_manager_entity,

    )).parsed
