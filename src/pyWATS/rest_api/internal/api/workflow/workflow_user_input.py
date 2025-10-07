from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_user_input_data_body import WorkflowUserInputDataBody
from ...models.workflow_user_input_json_body import WorkflowUserInputJsonBody
from ...models.workflow_user_input_response_200 import WorkflowUserInputResponse200
from ...models.workflow_user_input_status import WorkflowUserInputStatus
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        WorkflowUserInputJsonBody,
        WorkflowUserInputDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    result: str,
    status: Union[Unset, WorkflowUserInputStatus] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["SerialNumber"] = serial_number

    params["PartNumber"] = part_number

    params["Operation"] = operation

    params["Result"] = result

    json_status: Union[Unset, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["Status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Workflow/UserInput",
        "params": params,
    }

    if isinstance(body, WorkflowUserInputJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, WorkflowUserInputDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowUserInputResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowUserInputResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowUserInputResponse200]:
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
        WorkflowUserInputJsonBody,
        WorkflowUserInputDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    result: str,
    status: Union[Unset, WorkflowUserInputStatus] = UNSET,

) -> Response[WorkflowUserInputResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        result (str):
        status (Union[Unset, WorkflowUserInputStatus]):
        body (WorkflowUserInputJsonBody):
        body (WorkflowUserInputDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowUserInputResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
result=result,
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
        WorkflowUserInputJsonBody,
        WorkflowUserInputDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    result: str,
    status: Union[Unset, WorkflowUserInputStatus] = UNSET,

) -> Optional[WorkflowUserInputResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        result (str):
        status (Union[Unset, WorkflowUserInputStatus]):
        body (WorkflowUserInputJsonBody):
        body (WorkflowUserInputDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowUserInputResponse200
     """


    return sync_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
result=result,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowUserInputJsonBody,
        WorkflowUserInputDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    result: str,
    status: Union[Unset, WorkflowUserInputStatus] = UNSET,

) -> Response[WorkflowUserInputResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        result (str):
        status (Union[Unset, WorkflowUserInputStatus]):
        body (WorkflowUserInputJsonBody):
        body (WorkflowUserInputDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowUserInputResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
result=result,
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
        WorkflowUserInputJsonBody,
        WorkflowUserInputDataBody,
    ],
    serial_number: str,
    part_number: str,
    operation: str,
    result: str,
    status: Union[Unset, WorkflowUserInputStatus] = UNSET,

) -> Optional[WorkflowUserInputResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        operation (str):
        result (str):
        status (Union[Unset, WorkflowUserInputStatus]):
        body (WorkflowUserInputJsonBody):
        body (WorkflowUserInputDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowUserInputResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
operation=operation,
result=result,
status=status,

    )).parsed
