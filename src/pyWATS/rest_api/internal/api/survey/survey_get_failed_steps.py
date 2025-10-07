from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.survey_get_failed_steps_response_200 import SurveyGetFailedStepsResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    get_all_steps: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["getAllSteps"] = get_all_steps


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Survey/GetFailedSteps/{id}".format(id=id,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SurveyGetFailedStepsResponse200]:
    if response.status_code == 200:
        response_200 = SurveyGetFailedStepsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SurveyGetFailedStepsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    get_all_steps: Union[Unset, bool] = UNSET,

) -> Response[SurveyGetFailedStepsResponse200]:
    """ 
    Args:
        id (UUID):
        get_all_steps (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SurveyGetFailedStepsResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
get_all_steps=get_all_steps,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    get_all_steps: Union[Unset, bool] = UNSET,

) -> Optional[SurveyGetFailedStepsResponse200]:
    """ 
    Args:
        id (UUID):
        get_all_steps (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SurveyGetFailedStepsResponse200
     """


    return sync_detailed(
        id=id,
client=client,
get_all_steps=get_all_steps,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    get_all_steps: Union[Unset, bool] = UNSET,

) -> Response[SurveyGetFailedStepsResponse200]:
    """ 
    Args:
        id (UUID):
        get_all_steps (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SurveyGetFailedStepsResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
get_all_steps=get_all_steps,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    get_all_steps: Union[Unset, bool] = UNSET,

) -> Optional[SurveyGetFailedStepsResponse200]:
    """ 
    Args:
        id (UUID):
        get_all_steps (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SurveyGetFailedStepsResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
get_all_steps=get_all_steps,

    )).parsed
