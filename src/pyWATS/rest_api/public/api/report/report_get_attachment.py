from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.report_get_attachment_response_200 import ReportGetAttachmentResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    *,
    report_id: UUID,
    attachment_id: Union[Unset, UUID] = UNSET,
    step_id: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_report_id = str(report_id)
    params["reportId"] = json_report_id

    json_attachment_id: Union[Unset, str] = UNSET
    if not isinstance(attachment_id, Unset):
        json_attachment_id = str(attachment_id)
    params["attachmentId"] = json_attachment_id

    params["stepId"] = step_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Report/Attachment",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportGetAttachmentResponse200]:
    if response.status_code == 200:
        response_200 = ReportGetAttachmentResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportGetAttachmentResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    attachment_id: Union[Unset, UUID] = UNSET,
    step_id: Union[Unset, int] = UNSET,

) -> Response[ReportGetAttachmentResponse200]:
    """ Get an attachment from a report using either attachmentId or stepId.

    Args:
        report_id (UUID):
        attachment_id (Union[Unset, UUID]):
        step_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetAttachmentResponse200]
     """


    kwargs = _get_kwargs(
        report_id=report_id,
attachment_id=attachment_id,
step_id=step_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    attachment_id: Union[Unset, UUID] = UNSET,
    step_id: Union[Unset, int] = UNSET,

) -> Optional[ReportGetAttachmentResponse200]:
    """ Get an attachment from a report using either attachmentId or stepId.

    Args:
        report_id (UUID):
        attachment_id (Union[Unset, UUID]):
        step_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetAttachmentResponse200
     """


    return sync_detailed(
        client=client,
report_id=report_id,
attachment_id=attachment_id,
step_id=step_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    attachment_id: Union[Unset, UUID] = UNSET,
    step_id: Union[Unset, int] = UNSET,

) -> Response[ReportGetAttachmentResponse200]:
    """ Get an attachment from a report using either attachmentId or stepId.

    Args:
        report_id (UUID):
        attachment_id (Union[Unset, UUID]):
        step_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetAttachmentResponse200]
     """


    kwargs = _get_kwargs(
        report_id=report_id,
attachment_id=attachment_id,
step_id=step_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    report_id: UUID,
    attachment_id: Union[Unset, UUID] = UNSET,
    step_id: Union[Unset, int] = UNSET,

) -> Optional[ReportGetAttachmentResponse200]:
    """ Get an attachment from a report using either attachmentId or stepId.

    Args:
        report_id (UUID):
        attachment_id (Union[Unset, UUID]):
        step_id (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetAttachmentResponse200
     """


    return (await asyncio_detailed(
        client=client,
report_id=report_id,
attachment_id=attachment_id,
step_id=step_id,

    )).parsed
