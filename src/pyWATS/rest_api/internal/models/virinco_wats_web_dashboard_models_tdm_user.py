from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmUser")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmUser:
    """ DTO - User (data transfer object)

        Attributes:
            id (Union[Unset, str]):
            username (Union[Unset, str]):
            description (Union[Unset, str]):
            password (Union[Unset, str]):
            full_name (Union[Unset, str]):
            email (Union[Unset, str]):
            is_readonly (Union[Unset, bool]):
            is_locked_out (Union[Unset, bool]):
            roles (Union[Unset, list[str]]):
            created_utc (Union[Unset, datetime.datetime]):
            last_activity (Union[Unset, datetime.datetime]):
            web_client_id (Union[Unset, int]):
            job_role (Union[Unset, int]):
            product_group_ids (Union[Unset, list[int]]):
            client_group_ids (Union[Unset, list[int]]):
            primary_contact (Union[Unset, bool]):
            headless (Union[Unset, bool]):
            expire_date (Union[Unset, datetime.datetime]):
            password_sign_in_enabled (Union[Unset, bool]):
            two_factor_key (Union[Unset, str]):
            two_factor_enabled (Union[Unset, bool]):
            eula_accepted_utc (Union[Unset, datetime.datetime]):
            culture_code (Union[Unset, str]):
            is_restricted (Union[Unset, bool]):
     """

    id: Union[Unset, str] = UNSET
    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    password: Union[Unset, str] = UNSET
    full_name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    is_readonly: Union[Unset, bool] = UNSET
    is_locked_out: Union[Unset, bool] = UNSET
    roles: Union[Unset, list[str]] = UNSET
    created_utc: Union[Unset, datetime.datetime] = UNSET
    last_activity: Union[Unset, datetime.datetime] = UNSET
    web_client_id: Union[Unset, int] = UNSET
    job_role: Union[Unset, int] = UNSET
    product_group_ids: Union[Unset, list[int]] = UNSET
    client_group_ids: Union[Unset, list[int]] = UNSET
    primary_contact: Union[Unset, bool] = UNSET
    headless: Union[Unset, bool] = UNSET
    expire_date: Union[Unset, datetime.datetime] = UNSET
    password_sign_in_enabled: Union[Unset, bool] = UNSET
    two_factor_key: Union[Unset, str] = UNSET
    two_factor_enabled: Union[Unset, bool] = UNSET
    eula_accepted_utc: Union[Unset, datetime.datetime] = UNSET
    culture_code: Union[Unset, str] = UNSET
    is_restricted: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        username = self.username

        description = self.description

        password = self.password

        full_name = self.full_name

        email = self.email

        is_readonly = self.is_readonly

        is_locked_out = self.is_locked_out

        roles: Union[Unset, list[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles



        created_utc: Union[Unset, str] = UNSET
        if not isinstance(self.created_utc, Unset):
            created_utc = self.created_utc.isoformat()

        last_activity: Union[Unset, str] = UNSET
        if not isinstance(self.last_activity, Unset):
            last_activity = self.last_activity.isoformat()

        web_client_id = self.web_client_id

        job_role = self.job_role

        product_group_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.product_group_ids, Unset):
            product_group_ids = self.product_group_ids



        client_group_ids: Union[Unset, list[int]] = UNSET
        if not isinstance(self.client_group_ids, Unset):
            client_group_ids = self.client_group_ids



        primary_contact = self.primary_contact

        headless = self.headless

        expire_date: Union[Unset, str] = UNSET
        if not isinstance(self.expire_date, Unset):
            expire_date = self.expire_date.isoformat()

        password_sign_in_enabled = self.password_sign_in_enabled

        two_factor_key = self.two_factor_key

        two_factor_enabled = self.two_factor_enabled

        eula_accepted_utc: Union[Unset, str] = UNSET
        if not isinstance(self.eula_accepted_utc, Unset):
            eula_accepted_utc = self.eula_accepted_utc.isoformat()

        culture_code = self.culture_code

        is_restricted = self.is_restricted


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["Id"] = id
        if username is not UNSET:
            field_dict["Username"] = username
        if description is not UNSET:
            field_dict["Description"] = description
        if password is not UNSET:
            field_dict["Password"] = password
        if full_name is not UNSET:
            field_dict["FullName"] = full_name
        if email is not UNSET:
            field_dict["Email"] = email
        if is_readonly is not UNSET:
            field_dict["IsReadonly"] = is_readonly
        if is_locked_out is not UNSET:
            field_dict["IsLockedOut"] = is_locked_out
        if roles is not UNSET:
            field_dict["Roles"] = roles
        if created_utc is not UNSET:
            field_dict["CreatedUtc"] = created_utc
        if last_activity is not UNSET:
            field_dict["LastActivity"] = last_activity
        if web_client_id is not UNSET:
            field_dict["WebClientId"] = web_client_id
        if job_role is not UNSET:
            field_dict["JobRole"] = job_role
        if product_group_ids is not UNSET:
            field_dict["ProductGroupIds"] = product_group_ids
        if client_group_ids is not UNSET:
            field_dict["ClientGroupIds"] = client_group_ids
        if primary_contact is not UNSET:
            field_dict["PrimaryContact"] = primary_contact
        if headless is not UNSET:
            field_dict["Headless"] = headless
        if expire_date is not UNSET:
            field_dict["ExpireDate"] = expire_date
        if password_sign_in_enabled is not UNSET:
            field_dict["PasswordSignInEnabled"] = password_sign_in_enabled
        if two_factor_key is not UNSET:
            field_dict["TwoFactorKey"] = two_factor_key
        if two_factor_enabled is not UNSET:
            field_dict["TwoFactorEnabled"] = two_factor_enabled
        if eula_accepted_utc is not UNSET:
            field_dict["EulaAcceptedUtc"] = eula_accepted_utc
        if culture_code is not UNSET:
            field_dict["CultureCode"] = culture_code
        if is_restricted is not UNSET:
            field_dict["IsRestricted"] = is_restricted

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("Id", UNSET)

        username = d.pop("Username", UNSET)

        description = d.pop("Description", UNSET)

        password = d.pop("Password", UNSET)

        full_name = d.pop("FullName", UNSET)

        email = d.pop("Email", UNSET)

        is_readonly = d.pop("IsReadonly", UNSET)

        is_locked_out = d.pop("IsLockedOut", UNSET)

        roles = cast(list[str], d.pop("Roles", UNSET))


        _created_utc = d.pop("CreatedUtc", UNSET)
        created_utc: Union[Unset, datetime.datetime]
        if isinstance(_created_utc,  Unset):
            created_utc = UNSET
        else:
            created_utc = isoparse(_created_utc)




        _last_activity = d.pop("LastActivity", UNSET)
        last_activity: Union[Unset, datetime.datetime]
        if isinstance(_last_activity,  Unset):
            last_activity = UNSET
        else:
            last_activity = isoparse(_last_activity)




        web_client_id = d.pop("WebClientId", UNSET)

        job_role = d.pop("JobRole", UNSET)

        product_group_ids = cast(list[int], d.pop("ProductGroupIds", UNSET))


        client_group_ids = cast(list[int], d.pop("ClientGroupIds", UNSET))


        primary_contact = d.pop("PrimaryContact", UNSET)

        headless = d.pop("Headless", UNSET)

        _expire_date = d.pop("ExpireDate", UNSET)
        expire_date: Union[Unset, datetime.datetime]
        if isinstance(_expire_date,  Unset):
            expire_date = UNSET
        else:
            expire_date = isoparse(_expire_date)




        password_sign_in_enabled = d.pop("PasswordSignInEnabled", UNSET)

        two_factor_key = d.pop("TwoFactorKey", UNSET)

        two_factor_enabled = d.pop("TwoFactorEnabled", UNSET)

        _eula_accepted_utc = d.pop("EulaAcceptedUtc", UNSET)
        eula_accepted_utc: Union[Unset, datetime.datetime]
        if isinstance(_eula_accepted_utc,  Unset):
            eula_accepted_utc = UNSET
        else:
            eula_accepted_utc = isoparse(_eula_accepted_utc)




        culture_code = d.pop("CultureCode", UNSET)

        is_restricted = d.pop("IsRestricted", UNSET)

        virinco_wats_web_dashboard_models_tdm_user = cls(
            id=id,
            username=username,
            description=description,
            password=password,
            full_name=full_name,
            email=email,
            is_readonly=is_readonly,
            is_locked_out=is_locked_out,
            roles=roles,
            created_utc=created_utc,
            last_activity=last_activity,
            web_client_id=web_client_id,
            job_role=job_role,
            product_group_ids=product_group_ids,
            client_group_ids=client_group_ids,
            primary_contact=primary_contact,
            headless=headless,
            expire_date=expire_date,
            password_sign_in_enabled=password_sign_in_enabled,
            two_factor_key=two_factor_key,
            two_factor_enabled=two_factor_enabled,
            eula_accepted_utc=eula_accepted_utc,
            culture_code=culture_code,
            is_restricted=is_restricted,
        )


        virinco_wats_web_dashboard_models_tdm_user.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_user

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
