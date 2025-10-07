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

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_user_settings import VirincoWATSWebDashboardModelsTdmUserSettings
  from ..models.microsoft_asp_net_identity_entity_framework_identity_user_login import MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin
  from ..models.microsoft_asp_net_identity_entity_framework_identity_user_claim import MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim
  from ..models.microsoft_asp_net_identity_entity_framework_identity_user_role import MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole
  from ..models.virinco_wats_web_dashboard_models_tdm_filter import VirincoWATSWebDashboardModelsTdmFilter
  from ..models.virinco_wats_web_dashboard_models_tdm_user_key_value import VirincoWATSWebDashboardModelsTdmUserKeyValue





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmApplicationUser")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmApplicationUser:
    """ 
        Attributes:
            last_activity_date (Union[Unset, datetime.datetime]):
            full_name (Union[Unset, str]):
            dob (Union[Unset, datetime.datetime]):
            eula_accepted_utc (Union[Unset, datetime.datetime]):
            eula_accepted_version (Union[Unset, int]):
            primary_contact (Union[Unset, bool]):
            web_client (Union[Unset, int]):
            headless (Union[Unset, bool]):
            description (Union[Unset, str]):
            expire_date (Union[Unset, datetime.datetime]):
            created_utc (Union[Unset, datetime.datetime]):
            job_role (Union[Unset, int]):
            password_sign_in_enabled (Union[Unset, bool]):
            user_settings (Union[Unset, VirincoWATSWebDashboardModelsTdmUserSettings]):
            filters (Union[Unset, list['VirincoWATSWebDashboardModelsTdmFilter']]):
            key_values (Union[Unset, list['VirincoWATSWebDashboardModelsTdmUserKeyValue']]):
            two_factor_key (Union[Unset, str]):
            email (Union[Unset, str]):
            email_confirmed (Union[Unset, bool]):
            password_hash (Union[Unset, str]):
            security_stamp (Union[Unset, str]):
            phone_number (Union[Unset, str]):
            phone_number_confirmed (Union[Unset, bool]):
            two_factor_enabled (Union[Unset, bool]):
            lockout_end_date_utc (Union[Unset, datetime.datetime]):
            lockout_enabled (Union[Unset, bool]):
            access_failed_count (Union[Unset, int]):
            roles (Union[Unset, list['MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole']]):
            claims (Union[Unset, list['MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim']]):
            logins (Union[Unset, list['MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin']]):
            id (Union[Unset, str]):
            user_name (Union[Unset, str]):
     """

    last_activity_date: Union[Unset, datetime.datetime] = UNSET
    full_name: Union[Unset, str] = UNSET
    dob: Union[Unset, datetime.datetime] = UNSET
    eula_accepted_utc: Union[Unset, datetime.datetime] = UNSET
    eula_accepted_version: Union[Unset, int] = UNSET
    primary_contact: Union[Unset, bool] = UNSET
    web_client: Union[Unset, int] = UNSET
    headless: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    expire_date: Union[Unset, datetime.datetime] = UNSET
    created_utc: Union[Unset, datetime.datetime] = UNSET
    job_role: Union[Unset, int] = UNSET
    password_sign_in_enabled: Union[Unset, bool] = UNSET
    user_settings: Union[Unset, 'VirincoWATSWebDashboardModelsTdmUserSettings'] = UNSET
    filters: Union[Unset, list['VirincoWATSWebDashboardModelsTdmFilter']] = UNSET
    key_values: Union[Unset, list['VirincoWATSWebDashboardModelsTdmUserKeyValue']] = UNSET
    two_factor_key: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    email_confirmed: Union[Unset, bool] = UNSET
    password_hash: Union[Unset, str] = UNSET
    security_stamp: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    phone_number_confirmed: Union[Unset, bool] = UNSET
    two_factor_enabled: Union[Unset, bool] = UNSET
    lockout_end_date_utc: Union[Unset, datetime.datetime] = UNSET
    lockout_enabled: Union[Unset, bool] = UNSET
    access_failed_count: Union[Unset, int] = UNSET
    roles: Union[Unset, list['MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole']] = UNSET
    claims: Union[Unset, list['MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim']] = UNSET
    logins: Union[Unset, list['MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin']] = UNSET
    id: Union[Unset, str] = UNSET
    user_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_user_settings import VirincoWATSWebDashboardModelsTdmUserSettings
        from ..models.microsoft_asp_net_identity_entity_framework_identity_user_login import MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin
        from ..models.microsoft_asp_net_identity_entity_framework_identity_user_claim import MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim
        from ..models.microsoft_asp_net_identity_entity_framework_identity_user_role import MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole
        from ..models.virinco_wats_web_dashboard_models_tdm_filter import VirincoWATSWebDashboardModelsTdmFilter
        from ..models.virinco_wats_web_dashboard_models_tdm_user_key_value import VirincoWATSWebDashboardModelsTdmUserKeyValue
        last_activity_date: Union[Unset, str] = UNSET
        if not isinstance(self.last_activity_date, Unset):
            last_activity_date = self.last_activity_date.isoformat()

        full_name = self.full_name

        dob: Union[Unset, str] = UNSET
        if not isinstance(self.dob, Unset):
            dob = self.dob.isoformat()

        eula_accepted_utc: Union[Unset, str] = UNSET
        if not isinstance(self.eula_accepted_utc, Unset):
            eula_accepted_utc = self.eula_accepted_utc.isoformat()

        eula_accepted_version = self.eula_accepted_version

        primary_contact = self.primary_contact

        web_client = self.web_client

        headless = self.headless

        description = self.description

        expire_date: Union[Unset, str] = UNSET
        if not isinstance(self.expire_date, Unset):
            expire_date = self.expire_date.isoformat()

        created_utc: Union[Unset, str] = UNSET
        if not isinstance(self.created_utc, Unset):
            created_utc = self.created_utc.isoformat()

        job_role = self.job_role

        password_sign_in_enabled = self.password_sign_in_enabled

        user_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user_settings, Unset):
            user_settings = self.user_settings.to_dict()

        filters: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.filters, Unset):
            filters = []
            for filters_item_data in self.filters:
                filters_item = filters_item_data.to_dict()
                filters.append(filters_item)



        key_values: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.key_values, Unset):
            key_values = []
            for key_values_item_data in self.key_values:
                key_values_item = key_values_item_data.to_dict()
                key_values.append(key_values_item)



        two_factor_key = self.two_factor_key

        email = self.email

        email_confirmed = self.email_confirmed

        password_hash = self.password_hash

        security_stamp = self.security_stamp

        phone_number = self.phone_number

        phone_number_confirmed = self.phone_number_confirmed

        two_factor_enabled = self.two_factor_enabled

        lockout_end_date_utc: Union[Unset, str] = UNSET
        if not isinstance(self.lockout_end_date_utc, Unset):
            lockout_end_date_utc = self.lockout_end_date_utc.isoformat()

        lockout_enabled = self.lockout_enabled

        access_failed_count = self.access_failed_count

        roles: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = []
            for roles_item_data in self.roles:
                roles_item = roles_item_data.to_dict()
                roles.append(roles_item)



        claims: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.claims, Unset):
            claims = []
            for claims_item_data in self.claims:
                claims_item = claims_item_data.to_dict()
                claims.append(claims_item)



        logins: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.logins, Unset):
            logins = []
            for logins_item_data in self.logins:
                logins_item = logins_item_data.to_dict()
                logins.append(logins_item)



        id = self.id

        user_name = self.user_name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if last_activity_date is not UNSET:
            field_dict["LastActivityDate"] = last_activity_date
        if full_name is not UNSET:
            field_dict["FullName"] = full_name
        if dob is not UNSET:
            field_dict["DOB"] = dob
        if eula_accepted_utc is not UNSET:
            field_dict["EulaAcceptedUtc"] = eula_accepted_utc
        if eula_accepted_version is not UNSET:
            field_dict["EulaAcceptedVersion"] = eula_accepted_version
        if primary_contact is not UNSET:
            field_dict["PrimaryContact"] = primary_contact
        if web_client is not UNSET:
            field_dict["WebClient"] = web_client
        if headless is not UNSET:
            field_dict["Headless"] = headless
        if description is not UNSET:
            field_dict["Description"] = description
        if expire_date is not UNSET:
            field_dict["ExpireDate"] = expire_date
        if created_utc is not UNSET:
            field_dict["CreatedUtc"] = created_utc
        if job_role is not UNSET:
            field_dict["JobRole"] = job_role
        if password_sign_in_enabled is not UNSET:
            field_dict["PasswordSignInEnabled"] = password_sign_in_enabled
        if user_settings is not UNSET:
            field_dict["UserSettings"] = user_settings
        if filters is not UNSET:
            field_dict["Filters"] = filters
        if key_values is not UNSET:
            field_dict["KeyValues"] = key_values
        if two_factor_key is not UNSET:
            field_dict["TwoFactorKey"] = two_factor_key
        if email is not UNSET:
            field_dict["Email"] = email
        if email_confirmed is not UNSET:
            field_dict["EmailConfirmed"] = email_confirmed
        if password_hash is not UNSET:
            field_dict["PasswordHash"] = password_hash
        if security_stamp is not UNSET:
            field_dict["SecurityStamp"] = security_stamp
        if phone_number is not UNSET:
            field_dict["PhoneNumber"] = phone_number
        if phone_number_confirmed is not UNSET:
            field_dict["PhoneNumberConfirmed"] = phone_number_confirmed
        if two_factor_enabled is not UNSET:
            field_dict["TwoFactorEnabled"] = two_factor_enabled
        if lockout_end_date_utc is not UNSET:
            field_dict["LockoutEndDateUtc"] = lockout_end_date_utc
        if lockout_enabled is not UNSET:
            field_dict["LockoutEnabled"] = lockout_enabled
        if access_failed_count is not UNSET:
            field_dict["AccessFailedCount"] = access_failed_count
        if roles is not UNSET:
            field_dict["Roles"] = roles
        if claims is not UNSET:
            field_dict["Claims"] = claims
        if logins is not UNSET:
            field_dict["Logins"] = logins
        if id is not UNSET:
            field_dict["Id"] = id
        if user_name is not UNSET:
            field_dict["UserName"] = user_name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_user_settings import VirincoWATSWebDashboardModelsTdmUserSettings
        from ..models.microsoft_asp_net_identity_entity_framework_identity_user_login import MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin
        from ..models.microsoft_asp_net_identity_entity_framework_identity_user_claim import MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim
        from ..models.microsoft_asp_net_identity_entity_framework_identity_user_role import MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole
        from ..models.virinco_wats_web_dashboard_models_tdm_filter import VirincoWATSWebDashboardModelsTdmFilter
        from ..models.virinco_wats_web_dashboard_models_tdm_user_key_value import VirincoWATSWebDashboardModelsTdmUserKeyValue
        d = dict(src_dict)
        _last_activity_date = d.pop("LastActivityDate", UNSET)
        last_activity_date: Union[Unset, datetime.datetime]
        if isinstance(_last_activity_date,  Unset):
            last_activity_date = UNSET
        else:
            last_activity_date = isoparse(_last_activity_date)




        full_name = d.pop("FullName", UNSET)

        _dob = d.pop("DOB", UNSET)
        dob: Union[Unset, datetime.datetime]
        if isinstance(_dob,  Unset):
            dob = UNSET
        else:
            dob = isoparse(_dob)




        _eula_accepted_utc = d.pop("EulaAcceptedUtc", UNSET)
        eula_accepted_utc: Union[Unset, datetime.datetime]
        if isinstance(_eula_accepted_utc,  Unset):
            eula_accepted_utc = UNSET
        else:
            eula_accepted_utc = isoparse(_eula_accepted_utc)




        eula_accepted_version = d.pop("EulaAcceptedVersion", UNSET)

        primary_contact = d.pop("PrimaryContact", UNSET)

        web_client = d.pop("WebClient", UNSET)

        headless = d.pop("Headless", UNSET)

        description = d.pop("Description", UNSET)

        _expire_date = d.pop("ExpireDate", UNSET)
        expire_date: Union[Unset, datetime.datetime]
        if isinstance(_expire_date,  Unset):
            expire_date = UNSET
        else:
            expire_date = isoparse(_expire_date)




        _created_utc = d.pop("CreatedUtc", UNSET)
        created_utc: Union[Unset, datetime.datetime]
        if isinstance(_created_utc,  Unset):
            created_utc = UNSET
        else:
            created_utc = isoparse(_created_utc)




        job_role = d.pop("JobRole", UNSET)

        password_sign_in_enabled = d.pop("PasswordSignInEnabled", UNSET)

        _user_settings = d.pop("UserSettings", UNSET)
        user_settings: Union[Unset, VirincoWATSWebDashboardModelsTdmUserSettings]
        if isinstance(_user_settings,  Unset):
            user_settings = UNSET
        else:
            user_settings = VirincoWATSWebDashboardModelsTdmUserSettings.from_dict(_user_settings)




        filters = []
        _filters = d.pop("Filters", UNSET)
        for filters_item_data in (_filters or []):
            filters_item = VirincoWATSWebDashboardModelsTdmFilter.from_dict(filters_item_data)



            filters.append(filters_item)


        key_values = []
        _key_values = d.pop("KeyValues", UNSET)
        for key_values_item_data in (_key_values or []):
            key_values_item = VirincoWATSWebDashboardModelsTdmUserKeyValue.from_dict(key_values_item_data)



            key_values.append(key_values_item)


        two_factor_key = d.pop("TwoFactorKey", UNSET)

        email = d.pop("Email", UNSET)

        email_confirmed = d.pop("EmailConfirmed", UNSET)

        password_hash = d.pop("PasswordHash", UNSET)

        security_stamp = d.pop("SecurityStamp", UNSET)

        phone_number = d.pop("PhoneNumber", UNSET)

        phone_number_confirmed = d.pop("PhoneNumberConfirmed", UNSET)

        two_factor_enabled = d.pop("TwoFactorEnabled", UNSET)

        _lockout_end_date_utc = d.pop("LockoutEndDateUtc", UNSET)
        lockout_end_date_utc: Union[Unset, datetime.datetime]
        if isinstance(_lockout_end_date_utc,  Unset):
            lockout_end_date_utc = UNSET
        else:
            lockout_end_date_utc = isoparse(_lockout_end_date_utc)




        lockout_enabled = d.pop("LockoutEnabled", UNSET)

        access_failed_count = d.pop("AccessFailedCount", UNSET)

        roles = []
        _roles = d.pop("Roles", UNSET)
        for roles_item_data in (_roles or []):
            roles_item = MicrosoftAspNetIdentityEntityFrameworkIdentityUserRole.from_dict(roles_item_data)



            roles.append(roles_item)


        claims = []
        _claims = d.pop("Claims", UNSET)
        for claims_item_data in (_claims or []):
            claims_item = MicrosoftAspNetIdentityEntityFrameworkIdentityUserClaim.from_dict(claims_item_data)



            claims.append(claims_item)


        logins = []
        _logins = d.pop("Logins", UNSET)
        for logins_item_data in (_logins or []):
            logins_item = MicrosoftAspNetIdentityEntityFrameworkIdentityUserLogin.from_dict(logins_item_data)



            logins.append(logins_item)


        id = d.pop("Id", UNSET)

        user_name = d.pop("UserName", UNSET)

        virinco_wats_web_dashboard_models_tdm_application_user = cls(
            last_activity_date=last_activity_date,
            full_name=full_name,
            dob=dob,
            eula_accepted_utc=eula_accepted_utc,
            eula_accepted_version=eula_accepted_version,
            primary_contact=primary_contact,
            web_client=web_client,
            headless=headless,
            description=description,
            expire_date=expire_date,
            created_utc=created_utc,
            job_role=job_role,
            password_sign_in_enabled=password_sign_in_enabled,
            user_settings=user_settings,
            filters=filters,
            key_values=key_values,
            two_factor_key=two_factor_key,
            email=email,
            email_confirmed=email_confirmed,
            password_hash=password_hash,
            security_stamp=security_stamp,
            phone_number=phone_number,
            phone_number_confirmed=phone_number_confirmed,
            two_factor_enabled=two_factor_enabled,
            lockout_end_date_utc=lockout_end_date_utc,
            lockout_enabled=lockout_enabled,
            access_failed_count=access_failed_count,
            roles=roles,
            claims=claims,
            logins=logins,
            id=id,
            user_name=user_name,
        )


        virinco_wats_web_dashboard_models_tdm_application_user.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_application_user

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
