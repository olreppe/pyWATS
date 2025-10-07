from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.mes_translate_data_body_item import MesTranslateDataBodyItem
from ...models.mes_translate_json_body_item import MesTranslateJsonBodyItem
from ...models.mes_translate_response_200 import MesTranslateResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        list['MesTranslateJsonBodyItem'],
        list['MesTranslateDataBodyItem'],
    ],
    culture_code: str,
    english_text: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["cultureCode"] = culture_code

    params["englishText"] = english_text


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Mes/Translate",
        "params": params,
    }

    if isinstance(body, list['MesTranslateJsonBodyItem']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['MesTranslateDataBodyItem']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[MesTranslateResponse200]:
    if response.status_code == 200:
        response_200 = MesTranslateResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[MesTranslateResponse200]:
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
        list['MesTranslateJsonBodyItem'],
        list['MesTranslateDataBodyItem'],
    ],
    culture_code: str,
    english_text: str,

) -> Response[MesTranslateResponse200]:
    """ 
    Args:
        culture_code (str):
        english_text (str):
        body (list['MesTranslateJsonBodyItem']):
        body (list['MesTranslateDataBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesTranslateResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
culture_code=culture_code,
english_text=english_text,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['MesTranslateJsonBodyItem'],
        list['MesTranslateDataBodyItem'],
    ],
    culture_code: str,
    english_text: str,

) -> Optional[MesTranslateResponse200]:
    """ 
    Args:
        culture_code (str):
        english_text (str):
        body (list['MesTranslateJsonBodyItem']):
        body (list['MesTranslateDataBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesTranslateResponse200
     """


    return sync_detailed(
        client=client,
body=body,
culture_code=culture_code,
english_text=english_text,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['MesTranslateJsonBodyItem'],
        list['MesTranslateDataBodyItem'],
    ],
    culture_code: str,
    english_text: str,

) -> Response[MesTranslateResponse200]:
    """ 
    Args:
        culture_code (str):
        english_text (str):
        body (list['MesTranslateJsonBodyItem']):
        body (list['MesTranslateDataBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesTranslateResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
culture_code=culture_code,
english_text=english_text,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['MesTranslateJsonBodyItem'],
        list['MesTranslateDataBodyItem'],
    ],
    culture_code: str,
    english_text: str,

) -> Optional[MesTranslateResponse200]:
    """ 
    Args:
        culture_code (str):
        english_text (str):
        body (list['MesTranslateJsonBodyItem']):
        body (list['MesTranslateDataBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesTranslateResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
culture_code=culture_code,
english_text=english_text,

    )).parsed
