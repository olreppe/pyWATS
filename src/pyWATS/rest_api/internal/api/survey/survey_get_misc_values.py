from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.survey_get_misc_values_response_200 import SurveyGetMiscValuesResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    search_text: str,
    type_: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["searchText"] = search_text

    params["type"] = type_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Survey/GetMiscValues",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SurveyGetMiscValuesResponse200]:
    if response.status_code == 200:
        response_200 = SurveyGetMiscValuesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SurveyGetMiscValuesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_text: str,
    type_: Union[Unset, int] = UNSET,

) -> Response[SurveyGetMiscValuesResponse200]:
    """ 
    Args:
        search_text (str):
        type_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SurveyGetMiscValuesResponse200]
     """


    kwargs = _get_kwargs(
        search_text=search_text,
type_=type_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    search_text: str,
    type_: Union[Unset, int] = UNSET,

) -> Optional[SurveyGetMiscValuesResponse200]:
    """ 
    Args:
        search_text (str):
        type_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SurveyGetMiscValuesResponse200
     """


    return sync_detailed(
        client=client,
search_text=search_text,
type_=type_,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search_text: str,
    type_: Union[Unset, int] = UNSET,

) -> Response[SurveyGetMiscValuesResponse200]:
    """ 
    Args:
        search_text (str):
        type_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SurveyGetMiscValuesResponse200]
     """


    kwargs = _get_kwargs(
        search_text=search_text,
type_=type_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    search_text: str,
    type_: Union[Unset, int] = UNSET,

) -> Optional[SurveyGetMiscValuesResponse200]:
    """ 
    Args:
        search_text (str):
        type_ (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SurveyGetMiscValuesResponse200
     """


    return (await asyncio_detailed(
        client=client,
search_text=search_text,
type_=type_,

    )).parsed
