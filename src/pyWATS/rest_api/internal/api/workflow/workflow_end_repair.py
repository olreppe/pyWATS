from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_end_repair_data_body import WorkflowEndRepairDataBody
from ...models.workflow_end_repair_json_body import WorkflowEndRepairJsonBody
from ...models.workflow_end_repair_response_200 import WorkflowEndRepairResponse200
from ...models.workflow_end_repair_status import WorkflowEndRepairStatus
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        WorkflowEndRepairJsonBody,
        WorkflowEndRepairDataBody,
    ],
    serial_number: str,
    part_number: str,
    repair_type: str,
    status: Union[Unset, WorkflowEndRepairStatus] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["SerialNumber"] = serial_number

    params["PartNumber"] = part_number

    params["RepairType"] = repair_type

    json_status: Union[Unset, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["Status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Workflow/EndRepair",
        "params": params,
    }

    if isinstance(body, WorkflowEndRepairJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, WorkflowEndRepairDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowEndRepairResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowEndRepairResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowEndRepairResponse200]:
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
        WorkflowEndRepairJsonBody,
        WorkflowEndRepairDataBody,
    ],
    serial_number: str,
    part_number: str,
    repair_type: str,
    status: Union[Unset, WorkflowEndRepairStatus] = UNSET,

) -> Response[WorkflowEndRepairResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        repair_type (str):
        status (Union[Unset, WorkflowEndRepairStatus]):
        body (WorkflowEndRepairJsonBody):
        body (WorkflowEndRepairDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowEndRepairResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
repair_type=repair_type,
status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowEndRepairJsonBody,
        WorkflowEndRepairDataBody,
    ],
    serial_number: str,
    part_number: str,
    repair_type: str,
    status: Union[Unset, WorkflowEndRepairStatus] = UNSET,

) -> Optional[WorkflowEndRepairResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        repair_type (str):
        status (Union[Unset, WorkflowEndRepairStatus]):
        body (WorkflowEndRepairJsonBody):
        body (WorkflowEndRepairDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowEndRepairResponse200
     """


    return sync_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
repair_type=repair_type,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowEndRepairJsonBody,
        WorkflowEndRepairDataBody,
    ],
    serial_number: str,
    part_number: str,
    repair_type: str,
    status: Union[Unset, WorkflowEndRepairStatus] = UNSET,

) -> Response[WorkflowEndRepairResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        repair_type (str):
        status (Union[Unset, WorkflowEndRepairStatus]):
        body (WorkflowEndRepairJsonBody):
        body (WorkflowEndRepairDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowEndRepairResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
repair_type=repair_type,
status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowEndRepairJsonBody,
        WorkflowEndRepairDataBody,
    ],
    serial_number: str,
    part_number: str,
    repair_type: str,
    status: Union[Unset, WorkflowEndRepairStatus] = UNSET,

) -> Optional[WorkflowEndRepairResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        repair_type (str):
        status (Union[Unset, WorkflowEndRepairStatus]):
        body (WorkflowEndRepairJsonBody):
        body (WorkflowEndRepairDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowEndRepairResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
repair_type=repair_type,
status=status,

    )).parsed
