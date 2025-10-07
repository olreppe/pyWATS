from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.utils_learning_resources_data_body import UtilsLearningResourcesDataBody
from ...models.utils_learning_resources_json_body import UtilsLearningResourcesJsonBody
from ...models.utils_learning_resources_response_200 import UtilsLearningResourcesResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        UtilsLearningResourcesJsonBody,
        UtilsLearningResourcesDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Utils/LearningResources",
    }

    if isinstance(body, UtilsLearningResourcesJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, UtilsLearningResourcesDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UtilsLearningResourcesResponse200]:
    if response.status_code == 200:
        response_200 = UtilsLearningResourcesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UtilsLearningResourcesResponse200]:
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
        UtilsLearningResourcesJsonBody,
        UtilsLearningResourcesDataBody,
    ],

) -> Response[UtilsLearningResourcesResponse200]:
    r""" Get learning resources defined in instances.wats.com/learningResources

    body:
       {
       testMode : true,
       jobRole : \"Operator\"
       }

    Args:
        body (UtilsLearningResourcesJsonBody):
        body (UtilsLearningResourcesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UtilsLearningResourcesResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UtilsLearningResourcesJsonBody,
        UtilsLearningResourcesDataBody,
    ],

) -> Optional[UtilsLearningResourcesResponse200]:
    r""" Get learning resources defined in instances.wats.com/learningResources

    body:
       {
       testMode : true,
       jobRole : \"Operator\"
       }

    Args:
        body (UtilsLearningResourcesJsonBody):
        body (UtilsLearningResourcesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UtilsLearningResourcesResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UtilsLearningResourcesJsonBody,
        UtilsLearningResourcesDataBody,
    ],

) -> Response[UtilsLearningResourcesResponse200]:
    r""" Get learning resources defined in instances.wats.com/learningResources

    body:
       {
       testMode : true,
       jobRole : \"Operator\"
       }

    Args:
        body (UtilsLearningResourcesJsonBody):
        body (UtilsLearningResourcesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UtilsLearningResourcesResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        UtilsLearningResourcesJsonBody,
        UtilsLearningResourcesDataBody,
    ],

) -> Optional[UtilsLearningResourcesResponse200]:
    r""" Get learning resources defined in instances.wats.com/learningResources

    body:
       {
       testMode : true,
       jobRole : \"Operator\"
       }

    Args:
        body (UtilsLearningResourcesJsonBody):
        body (UtilsLearningResourcesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UtilsLearningResourcesResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
