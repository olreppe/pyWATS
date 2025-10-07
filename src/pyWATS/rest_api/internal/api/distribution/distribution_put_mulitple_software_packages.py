from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_put_mulitple_software_packages_data_body import DistributionPutMulitpleSoftwarePackagesDataBody
from ...models.distribution_put_mulitple_software_packages_json_body import DistributionPutMulitpleSoftwarePackagesJsonBody
from ...models.distribution_put_mulitple_software_packages_response_200 import DistributionPutMulitpleSoftwarePackagesResponse200
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        DistributionPutMulitpleSoftwarePackagesJsonBody,
        DistributionPutMulitpleSoftwarePackagesDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Distribution/Multi/Software/Packages",
    }

    if isinstance(body, DistributionPutMulitpleSoftwarePackagesJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, DistributionPutMulitpleSoftwarePackagesDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionPutMulitpleSoftwarePackagesResponse200]:
    if response.status_code == 200:
        response_200 = DistributionPutMulitpleSoftwarePackagesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionPutMulitpleSoftwarePackagesResponse200]:
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
        DistributionPutMulitpleSoftwarePackagesJsonBody,
        DistributionPutMulitpleSoftwarePackagesDataBody,
    ],

) -> Response[DistributionPutMulitpleSoftwarePackagesResponse200]:
    """ 
    Args:
        body (DistributionPutMulitpleSoftwarePackagesJsonBody):
        body (DistributionPutMulitpleSoftwarePackagesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMulitpleSoftwarePackagesResponse200]
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
        DistributionPutMulitpleSoftwarePackagesJsonBody,
        DistributionPutMulitpleSoftwarePackagesDataBody,
    ],

) -> Optional[DistributionPutMulitpleSoftwarePackagesResponse200]:
    """ 
    Args:
        body (DistributionPutMulitpleSoftwarePackagesJsonBody):
        body (DistributionPutMulitpleSoftwarePackagesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMulitpleSoftwarePackagesResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        DistributionPutMulitpleSoftwarePackagesJsonBody,
        DistributionPutMulitpleSoftwarePackagesDataBody,
    ],

) -> Response[DistributionPutMulitpleSoftwarePackagesResponse200]:
    """ 
    Args:
        body (DistributionPutMulitpleSoftwarePackagesJsonBody):
        body (DistributionPutMulitpleSoftwarePackagesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionPutMulitpleSoftwarePackagesResponse200]
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
        DistributionPutMulitpleSoftwarePackagesJsonBody,
        DistributionPutMulitpleSoftwarePackagesDataBody,
    ],

) -> Optional[DistributionPutMulitpleSoftwarePackagesResponse200]:
    """ 
    Args:
        body (DistributionPutMulitpleSoftwarePackagesJsonBody):
        body (DistributionPutMulitpleSoftwarePackagesDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionPutMulitpleSoftwarePackagesResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
