from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.app_processes_response_200 import AppProcessesResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    include_test_operations: Union[Unset, bool] = UNSET,
    include_repair_operations: Union[Unset, bool] = UNSET,
    include_wip_operations: Union[Unset, bool] = UNSET,
    include_inactive_processes: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["includeTestOperations"] = include_test_operations

    params["includeRepairOperations"] = include_repair_operations

    params["includeWipOperations"] = include_wip_operations

    params["includeInactiveProcesses"] = include_inactive_processes


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/App/Processes",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AppProcessesResponse200]:
    if response.status_code == 200:
        response_200 = AppProcessesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AppProcessesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_test_operations: Union[Unset, bool] = UNSET,
    include_repair_operations: Union[Unset, bool] = UNSET,
    include_wip_operations: Union[Unset, bool] = UNSET,
    include_inactive_processes: Union[Unset, bool] = UNSET,

) -> Response[AppProcessesResponse200]:
    """ Get processes.

     Non-filtered requests retrieves active processes marked as isTestOperation, isRepairOperation or
    isWipOperation.

    RepairOperation details:

    uutBinding: 0 = required, 1 = optional, 2 = never

    bomBinding:  0 = required, 1 = optional, 2 = never

    vendorBinding:  0 = required, 1 = optional, 2 = never

    imageConstraint: 0 = required, 1 = optional, 2 = never

    repairType: Default = 0, AutomaticProcess = 1, Scrapped = 2, NoFailureFound = 3, Component = 4,
    Design = 5, ManualProcess = 6, Replaced = 7

    Args:
        include_test_operations (Union[Unset, bool]):
        include_repair_operations (Union[Unset, bool]):
        include_wip_operations (Union[Unset, bool]):
        include_inactive_processes (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AppProcessesResponse200]
     """


    kwargs = _get_kwargs(
        include_test_operations=include_test_operations,
include_repair_operations=include_repair_operations,
include_wip_operations=include_wip_operations,
include_inactive_processes=include_inactive_processes,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    include_test_operations: Union[Unset, bool] = UNSET,
    include_repair_operations: Union[Unset, bool] = UNSET,
    include_wip_operations: Union[Unset, bool] = UNSET,
    include_inactive_processes: Union[Unset, bool] = UNSET,

) -> Optional[AppProcessesResponse200]:
    """ Get processes.

     Non-filtered requests retrieves active processes marked as isTestOperation, isRepairOperation or
    isWipOperation.

    RepairOperation details:

    uutBinding: 0 = required, 1 = optional, 2 = never

    bomBinding:  0 = required, 1 = optional, 2 = never

    vendorBinding:  0 = required, 1 = optional, 2 = never

    imageConstraint: 0 = required, 1 = optional, 2 = never

    repairType: Default = 0, AutomaticProcess = 1, Scrapped = 2, NoFailureFound = 3, Component = 4,
    Design = 5, ManualProcess = 6, Replaced = 7

    Args:
        include_test_operations (Union[Unset, bool]):
        include_repair_operations (Union[Unset, bool]):
        include_wip_operations (Union[Unset, bool]):
        include_inactive_processes (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AppProcessesResponse200
     """


    return sync_detailed(
        client=client,
include_test_operations=include_test_operations,
include_repair_operations=include_repair_operations,
include_wip_operations=include_wip_operations,
include_inactive_processes=include_inactive_processes,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_test_operations: Union[Unset, bool] = UNSET,
    include_repair_operations: Union[Unset, bool] = UNSET,
    include_wip_operations: Union[Unset, bool] = UNSET,
    include_inactive_processes: Union[Unset, bool] = UNSET,

) -> Response[AppProcessesResponse200]:
    """ Get processes.

     Non-filtered requests retrieves active processes marked as isTestOperation, isRepairOperation or
    isWipOperation.

    RepairOperation details:

    uutBinding: 0 = required, 1 = optional, 2 = never

    bomBinding:  0 = required, 1 = optional, 2 = never

    vendorBinding:  0 = required, 1 = optional, 2 = never

    imageConstraint: 0 = required, 1 = optional, 2 = never

    repairType: Default = 0, AutomaticProcess = 1, Scrapped = 2, NoFailureFound = 3, Component = 4,
    Design = 5, ManualProcess = 6, Replaced = 7

    Args:
        include_test_operations (Union[Unset, bool]):
        include_repair_operations (Union[Unset, bool]):
        include_wip_operations (Union[Unset, bool]):
        include_inactive_processes (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AppProcessesResponse200]
     """


    kwargs = _get_kwargs(
        include_test_operations=include_test_operations,
include_repair_operations=include_repair_operations,
include_wip_operations=include_wip_operations,
include_inactive_processes=include_inactive_processes,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    include_test_operations: Union[Unset, bool] = UNSET,
    include_repair_operations: Union[Unset, bool] = UNSET,
    include_wip_operations: Union[Unset, bool] = UNSET,
    include_inactive_processes: Union[Unset, bool] = UNSET,

) -> Optional[AppProcessesResponse200]:
    """ Get processes.

     Non-filtered requests retrieves active processes marked as isTestOperation, isRepairOperation or
    isWipOperation.

    RepairOperation details:

    uutBinding: 0 = required, 1 = optional, 2 = never

    bomBinding:  0 = required, 1 = optional, 2 = never

    vendorBinding:  0 = required, 1 = optional, 2 = never

    imageConstraint: 0 = required, 1 = optional, 2 = never

    repairType: Default = 0, AutomaticProcess = 1, Scrapped = 2, NoFailureFound = 3, Component = 4,
    Design = 5, ManualProcess = 6, Replaced = 7

    Args:
        include_test_operations (Union[Unset, bool]):
        include_repair_operations (Union[Unset, bool]):
        include_wip_operations (Union[Unset, bool]):
        include_inactive_processes (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AppProcessesResponse200
     """


    return (await asyncio_detailed(
        client=client,
include_test_operations=include_test_operations,
include_repair_operations=include_repair_operations,
include_wip_operations=include_wip_operations,
include_inactive_processes=include_inactive_processes,

    )).parsed
