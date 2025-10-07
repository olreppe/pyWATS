from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.account_post_custom_sso_provider_response_200 import AccountPostCustomSsoProviderResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    client_id: str,
    authority_url: str,
    client_secret: Union[Unset, str] = UNSET,
    sso_name: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["clientId"] = client_id

    params["authorityUrl"] = authority_url

    params["clientSecret"] = client_secret

    params["ssoName"] = sso_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Account/PostCustomSsoProvider",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AccountPostCustomSsoProviderResponse200]:
    if response.status_code == 200:
        response_200 = AccountPostCustomSsoProviderResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AccountPostCustomSsoProviderResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    authority_url: str,
    client_secret: Union[Unset, str] = UNSET,
    sso_name: Union[Unset, str] = UNSET,

) -> Response[AccountPostCustomSsoProviderResponse200]:
    """ Updates the Custom SSO values of WATS, then restarts the application after saving to database.

    Args:
        client_id (str):
        authority_url (str):
        client_secret (Union[Unset, str]):
        sso_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountPostCustomSsoProviderResponse200]
     """


    kwargs = _get_kwargs(
        client_id=client_id,
authority_url=authority_url,
client_secret=client_secret,
sso_name=sso_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    authority_url: str,
    client_secret: Union[Unset, str] = UNSET,
    sso_name: Union[Unset, str] = UNSET,

) -> Optional[AccountPostCustomSsoProviderResponse200]:
    """ Updates the Custom SSO values of WATS, then restarts the application after saving to database.

    Args:
        client_id (str):
        authority_url (str):
        client_secret (Union[Unset, str]):
        sso_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountPostCustomSsoProviderResponse200
     """


    return sync_detailed(
        client=client,
client_id=client_id,
authority_url=authority_url,
client_secret=client_secret,
sso_name=sso_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    authority_url: str,
    client_secret: Union[Unset, str] = UNSET,
    sso_name: Union[Unset, str] = UNSET,

) -> Response[AccountPostCustomSsoProviderResponse200]:
    """ Updates the Custom SSO values of WATS, then restarts the application after saving to database.

    Args:
        client_id (str):
        authority_url (str):
        client_secret (Union[Unset, str]):
        sso_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountPostCustomSsoProviderResponse200]
     """


    kwargs = _get_kwargs(
        client_id=client_id,
authority_url=authority_url,
client_secret=client_secret,
sso_name=sso_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: str,
    authority_url: str,
    client_secret: Union[Unset, str] = UNSET,
    sso_name: Union[Unset, str] = UNSET,

) -> Optional[AccountPostCustomSsoProviderResponse200]:
    """ Updates the Custom SSO values of WATS, then restarts the application after saving to database.

    Args:
        client_id (str):
        authority_url (str):
        client_secret (Union[Unset, str]):
        sso_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountPostCustomSsoProviderResponse200
     """


    return (await asyncio_detailed(
        client=client,
client_id=client_id,
authority_url=authority_url,
client_secret=client_secret,
sso_name=sso_name,

    )).parsed
