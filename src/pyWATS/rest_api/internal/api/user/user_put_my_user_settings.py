from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.user_put_my_user_settings_response_200 import UserPutMyUserSettingsResponse200
from ...models.virinco_wats_web_dashboard_models_tdm_my_settings_user import VirincoWATSWebDashboardModelsTdmMySettingsUser
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/User/PutMyUserSettings",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsTdmMySettingsUser):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmMySettingsUser):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmMySettingsUser):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UserPutMyUserSettingsResponse200]:
    if response.status_code == 200:
        response_200 = UserPutMyUserSettingsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UserPutMyUserSettingsResponse200]:
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
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
    ],

) -> Response[UserPutMyUserSettingsResponse200]:
    """ Updates My-Settings data for logged in user

    Args:
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPutMyUserSettingsResponse200]
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
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
    ],

) -> Optional[UserPutMyUserSettingsResponse200]:
    """ Updates My-Settings data for logged in user

    Args:
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPutMyUserSettingsResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
    ],

) -> Response[UserPutMyUserSettingsResponse200]:
    """ Updates My-Settings data for logged in user

    Args:
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UserPutMyUserSettingsResponse200]
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
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
        VirincoWATSWebDashboardModelsTdmMySettingsUser,
    ],

) -> Optional[UserPutMyUserSettingsResponse200]:
    """ Updates My-Settings data for logged in user

    Args:
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings
        body (VirincoWATSWebDashboardModelsTdmMySettingsUser): Wrapper model used for updating
            user settings, used in conjunction with My Settings

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UserPutMyUserSettingsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
