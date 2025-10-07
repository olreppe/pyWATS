from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_put_multiple_workflows_data_body import DistributionPutMultipleWorkflowsDataBody
from ...models.distribution_put_multiple_workflows_json_body import DistributionPutMultipleWorkflowsJsonBody
from ...models.distribution_put_multiple_workflows_response_200 import DistributionPutMultipleWorkflowsResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        DistributionPutMultipleWorkflowsJsonBody,
        DistributionPutMultipleWorkflowsDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Distribution/Multi/Workflows",
    }

    if isinstance(body, DistributionPutMultipleWorkflowsJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, DistributionPutMultipleWorkflowsDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionPutMultipleWorkflowsResponse200]:
    if response.status_code == 200:
        response_200 = DistributionPutMultipleWorkflowsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionPutMultipleWorkflowsResponse200]:
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
        DistributionPutMultipleWorkflowsJsonBody,
        DistributionPutMultipleWorkflowsDataBody,
    ],

) -> Response[DistributionPutMultipleWorkflowsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleWorkflowsJsonBody):
        body (DistributionPutMultipleWorkflowsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMultipleWorkflowsResponse200]
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
        DistributionPutMultipleWorkflowsJsonBody,
        DistributionPutMultipleWorkflowsDataBody,
    ],

) -> Optional[DistributionPutMultipleWorkflowsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleWorkflowsJsonBody):
        body (DistributionPutMultipleWorkflowsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMultipleWorkflowsResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DistributionPutMultipleWorkflowsJsonBody,
        DistributionPutMultipleWorkflowsDataBody,
    ],

) -> Response[DistributionPutMultipleWorkflowsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleWorkflowsJsonBody):
        body (DistributionPutMultipleWorkflowsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMultipleWorkflowsResponse200]
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
        DistributionPutMultipleWorkflowsJsonBody,
        DistributionPutMultipleWorkflowsDataBody,
    ],

) -> Optional[DistributionPutMultipleWorkflowsResponse200]:
    """ 
    Args:
        body (DistributionPutMultipleWorkflowsJsonBody):
        body (DistributionPutMultipleWorkflowsDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMultipleWorkflowsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
