from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.utils_log_usage_data_body import UtilsLogUsageDataBody
from ...models.utils_log_usage_json_body import UtilsLogUsageJsonBody
from ...models.utils_log_usage_response_200 import UtilsLogUsageResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        UtilsLogUsageJsonBody,
        UtilsLogUsageDataBody,
    ],
    app: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["app"] = app


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Utils/TrackUsage",
        "params": params,
    }

    if isinstance(body, UtilsLogUsageJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, UtilsLogUsageDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UtilsLogUsageResponse200]:
    if response.status_code == 200:
        response_200 = UtilsLogUsageResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UtilsLogUsageResponse200]:
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
        UtilsLogUsageJsonBody,
        UtilsLogUsageDataBody,
    ],
    app: str,

) -> Response[UtilsLogUsageResponse200]:
    """ Logs usage of other apps to an ingestion service (Application Insights).

    Args:
        app (str):
        body (UtilsLogUsageJsonBody):
        body (UtilsLogUsageDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UtilsLogUsageResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
app=app,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UtilsLogUsageJsonBody,
        UtilsLogUsageDataBody,
    ],
    app: str,

) -> Optional[UtilsLogUsageResponse200]:
    """ Logs usage of other apps to an ingestion service (Application Insights).

    Args:
        app (str):
        body (UtilsLogUsageJsonBody):
        body (UtilsLogUsageDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UtilsLogUsageResponse200
     """


    return sync_detailed(
        client=client,
body=body,
app=app,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UtilsLogUsageJsonBody,
        UtilsLogUsageDataBody,
    ],
    app: str,

) -> Response[UtilsLogUsageResponse200]:
    """ Logs usage of other apps to an ingestion service (Application Insights).

    Args:
        app (str):
        body (UtilsLogUsageJsonBody):
        body (UtilsLogUsageDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UtilsLogUsageResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
app=app,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UtilsLogUsageJsonBody,
        UtilsLogUsageDataBody,
    ],
    app: str,

) -> Optional[UtilsLogUsageResponse200]:
    """ Logs usage of other apps to an ingestion service (Application Insights).

    Args:
        app (str):
        body (UtilsLogUsageJsonBody):
        body (UtilsLogUsageDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UtilsLogUsageResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
app=app,

    )).parsed
