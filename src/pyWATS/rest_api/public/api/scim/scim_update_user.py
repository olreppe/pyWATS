from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.scim_update_user_data_body import ScimUpdateUserDataBody
from ...models.scim_update_user_json_body import ScimUpdateUserJsonBody
from ...models.scim_update_user_response_200 import ScimUpdateUserResponse200
from typing import cast



def _get_kwargs(
    id: str,
    *,
    body: Union[
        ScimUpdateUserJsonBody,
        ScimUpdateUserDataBody,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/SCIM/v2/Users/{id}".format(id=id,),
    }

    if isinstance(body, ScimUpdateUserJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, ScimUpdateUserDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ScimUpdateUserResponse200]:
    if response.status_code == 200:
        response_200 = ScimUpdateUserResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ScimUpdateUserResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ScimUpdateUserJsonBody,
        ScimUpdateUserDataBody,
    ],

) -> Response[ScimUpdateUserResponse200]:
    r""" Updates user details for the provided username using JSON following the SCIM protocol.
    Has to be in a SCIM patchOp format with schema.
    Only \"replace\" is supported and value has to be either a string or boolean, depending on their
    original data type.

     See https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2 for more details.<br></br>
    Currently accepted path values are: fullName, familyName, givenName, roles, email, active, levels,
    productGroups. <br></br>
    levels and productGroups are a multi-value string with ';' as a separator. levels and productGroups
    will only add new restrictions. <br></br>
    active is a boolean and will de-activate the user in WATS if updated to false.<br></br>
    fullName, familyName, givenName, roles and email are a single-value string. Roles will throw an
    error if role cannot be found

    Args:
        id (str):
        body (ScimUpdateUserJsonBody):
        body (ScimUpdateUserDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimUpdateUserResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ScimUpdateUserJsonBody,
        ScimUpdateUserDataBody,
    ],

) -> Optional[ScimUpdateUserResponse200]:
    r""" Updates user details for the provided username using JSON following the SCIM protocol.
    Has to be in a SCIM patchOp format with schema.
    Only \"replace\" is supported and value has to be either a string or boolean, depending on their
    original data type.

     See https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2 for more details.<br></br>
    Currently accepted path values are: fullName, familyName, givenName, roles, email, active, levels,
    productGroups. <br></br>
    levels and productGroups are a multi-value string with ';' as a separator. levels and productGroups
    will only add new restrictions. <br></br>
    active is a boolean and will de-activate the user in WATS if updated to false.<br></br>
    fullName, familyName, givenName, roles and email are a single-value string. Roles will throw an
    error if role cannot be found

    Args:
        id (str):
        body (ScimUpdateUserJsonBody):
        body (ScimUpdateUserDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimUpdateUserResponse200
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ScimUpdateUserJsonBody,
        ScimUpdateUserDataBody,
    ],

) -> Response[ScimUpdateUserResponse200]:
    r""" Updates user details for the provided username using JSON following the SCIM protocol.
    Has to be in a SCIM patchOp format with schema.
    Only \"replace\" is supported and value has to be either a string or boolean, depending on their
    original data type.

     See https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2 for more details.<br></br>
    Currently accepted path values are: fullName, familyName, givenName, roles, email, active, levels,
    productGroups. <br></br>
    levels and productGroups are a multi-value string with ';' as a separator. levels and productGroups
    will only add new restrictions. <br></br>
    active is a boolean and will de-activate the user in WATS if updated to false.<br></br>
    fullName, familyName, givenName, roles and email are a single-value string. Roles will throw an
    error if role cannot be found

    Args:
        id (str):
        body (ScimUpdateUserJsonBody):
        body (ScimUpdateUserDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimUpdateUserResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        ScimUpdateUserJsonBody,
        ScimUpdateUserDataBody,
    ],

) -> Optional[ScimUpdateUserResponse200]:
    r""" Updates user details for the provided username using JSON following the SCIM protocol.
    Has to be in a SCIM patchOp format with schema.
    Only \"replace\" is supported and value has to be either a string or boolean, depending on their
    original data type.

     See https://www.rfc-editor.org/rfc/rfc7644#section-3.5.2 for more details.<br></br>
    Currently accepted path values are: fullName, familyName, givenName, roles, email, active, levels,
    productGroups. <br></br>
    levels and productGroups are a multi-value string with ';' as a separator. levels and productGroups
    will only add new restrictions. <br></br>
    active is a boolean and will de-activate the user in WATS if updated to false.<br></br>
    fullName, familyName, givenName, roles and email are a single-value string. Roles will throw an
    error if role cannot be found

    Args:
        id (str):
        body (ScimUpdateUserJsonBody):
        body (ScimUpdateUserDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimUpdateUserResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
