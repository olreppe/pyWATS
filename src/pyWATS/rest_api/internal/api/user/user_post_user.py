from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user_post_user_response_200 import UserPostUserResponse200
from ...models.virinco_wats_web_dashboard_models_tdm_user import VirincoWATSWebDashboardModelsTdmUser
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/User/PostUser",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsTdmUser):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmUser):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmUser):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UserPostUserResponse200]:
    if response.status_code == 200:
        response_200 = UserPostUserResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UserPostUserResponse200]:
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
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
    ],

) -> Response[UserPostUserResponse200]:
    """ Adds a single new user. If the Password property is not present or empty, a password will be
    generated. If a boolean Property SendSkywatsMail is set to true,
    this method will automatically send am email to the user with user credentials.

    Args:
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPostUserResponse200]
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
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
    ],

) -> Optional[UserPostUserResponse200]:
    """ Adds a single new user. If the Password property is not present or empty, a password will be
    generated. If a boolean Property SendSkywatsMail is set to true,
    this method will automatically send am email to the user with user credentials.

    Args:
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPostUserResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
    ],

) -> Response[UserPostUserResponse200]:
    """ Adds a single new user. If the Password property is not present or empty, a password will be
    generated. If a boolean Property SendSkywatsMail is set to true,
    this method will automatically send am email to the user with user credentials.

    Args:
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPostUserResponse200]
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
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
        VirincoWATSWebDashboardModelsTdmUser,
    ],

) -> Optional[UserPostUserResponse200]:
    """ Adds a single new user. If the Password property is not present or empty, a password will be
    generated. If a boolean Property SendSkywatsMail is set to true,
    this method will automatically send am email to the user with user credentials.

    Args:
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)
        body (VirincoWATSWebDashboardModelsTdmUser): DTO - User (data transfer object)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPostUserResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
