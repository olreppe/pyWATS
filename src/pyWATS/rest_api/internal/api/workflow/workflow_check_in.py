from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_check_in_data_body import WorkflowCheckInDataBody
from ...models.workflow_check_in_json_body import WorkflowCheckInJsonBody
from ...models.workflow_check_in_response_200 import WorkflowCheckInResponse200
from ...models.workflow_check_in_status import WorkflowCheckInStatus
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        WorkflowCheckInJsonBody,
        WorkflowCheckInDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    status: Union[Unset, WorkflowCheckInStatus] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["SerialNumber"] = serial_number

    params["PartNumber"] = part_number

    params["Operation"] = operation

    json_status: Union[Unset, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["Status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Workflow/CheckIn",
        "params": params,
    }

    if isinstance(body, WorkflowCheckInJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, WorkflowCheckInDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowCheckInResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowCheckInResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowCheckInResponse200]:
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
        WorkflowCheckInJsonBody,
        WorkflowCheckInDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    status: Union[Unset, WorkflowCheckInStatus] = UNSET,

) -> Response[WorkflowCheckInResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        status (Union[Unset, WorkflowCheckInStatus]):
        body (WorkflowCheckInJsonBody):
        body (WorkflowCheckInDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowCheckInResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
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
        WorkflowCheckInJsonBody,
        WorkflowCheckInDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    status: Union[Unset, WorkflowCheckInStatus] = UNSET,

) -> Optional[WorkflowCheckInResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        status (Union[Unset, WorkflowCheckInStatus]):
        body (WorkflowCheckInJsonBody):
        body (WorkflowCheckInDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowCheckInResponse200
     """


    return sync_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowCheckInJsonBody,
        WorkflowCheckInDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    status: Union[Unset, WorkflowCheckInStatus] = UNSET,

) -> Response[WorkflowCheckInResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        status (Union[Unset, WorkflowCheckInStatus]):
        body (WorkflowCheckInJsonBody):
        body (WorkflowCheckInDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowCheckInResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
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
        WorkflowCheckInJsonBody,
        WorkflowCheckInDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    status: Union[Unset, WorkflowCheckInStatus] = UNSET,

) -> Optional[WorkflowCheckInResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        status (Union[Unset, WorkflowCheckInStatus]):
        body (WorkflowCheckInJsonBody):
        body (WorkflowCheckInDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowCheckInResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
status=status,

    )).parsed
