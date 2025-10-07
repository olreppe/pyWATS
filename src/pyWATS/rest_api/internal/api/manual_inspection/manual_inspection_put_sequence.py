from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.manual_inspection_put_sequence_response_200 import ManualInspectionPutSequenceResponse200
from ...models.virinco_wats_web_dashboard_models_mes_mi_step import VirincoWATSWebDashboardModelsMesMIStep
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
    ],
    submit: Union[Unset, bool] = UNSET,
    return_root_sequence: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["submit"] = submit

    params["returnRootSequence"] = return_root_sequence


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/ManualInspection/PutSequence",
        "params": params,
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsMesMIStep']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesMIStep']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesMIStep']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ManualInspectionPutSequenceResponse200]:
    if response.status_code == 200:
        response_200 = ManualInspectionPutSequenceResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ManualInspectionPutSequenceResponse200]:
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
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
    ],
    submit: Union[Unset, bool] = UNSET,
    return_root_sequence: Union[Unset, bool] = UNSET,

) -> Response[ManualInspectionPutSequenceResponse200]:
    """ 
    Args:
        submit (Union[Unset, bool]):
        return_root_sequence (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManualInspectionPutSequenceResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
submit=submit,
return_root_sequence=return_root_sequence,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
    ],
    submit: Union[Unset, bool] = UNSET,
    return_root_sequence: Union[Unset, bool] = UNSET,

) -> Optional[ManualInspectionPutSequenceResponse200]:
    """ 
    Args:
        submit (Union[Unset, bool]):
        return_root_sequence (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManualInspectionPutSequenceResponse200
     """


    return sync_detailed(
        client=client,
body=body,
submit=submit,
return_root_sequence=return_root_sequence,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
    ],
    submit: Union[Unset, bool] = UNSET,
    return_root_sequence: Union[Unset, bool] = UNSET,

) -> Response[ManualInspectionPutSequenceResponse200]:
    """ 
    Args:
        submit (Union[Unset, bool]):
        return_root_sequence (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManualInspectionPutSequenceResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
submit=submit,
return_root_sequence=return_root_sequence,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
        list['VirincoWATSWebDashboardModelsMesMIStep'],
    ],
    submit: Union[Unset, bool] = UNSET,
    return_root_sequence: Union[Unset, bool] = UNSET,

) -> Optional[ManualInspectionPutSequenceResponse200]:
    """ 
    Args:
        submit (Union[Unset, bool]):
        return_root_sequence (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):
        body (list['VirincoWATSWebDashboardModelsMesMIStep']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManualInspectionPutSequenceResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
submit=submit,
return_root_sequence=return_root_sequence,

    )).parsed
