from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_binary_data import VirincoWATSWebDashboardModelsBinaryData





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmAccountAdminSettings")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmAccountAdminSettings:
    """ 
        Attributes:
            logo_binary_data (Union[Unset, VirincoWATSWebDashboardModelsBinaryData]):
     """

    logo_binary_data: Union[Unset, 'VirincoWATSWebDashboardModelsBinaryData'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_binary_data import VirincoWATSWebDashboardModelsBinaryData
        logo_binary_data: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.logo_binary_data, Unset):
            logo_binary_data = self.logo_binary_data.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if logo_binary_data is not UNSET:
            field_dict["logoBinaryData"] = logo_binary_data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_binary_data import VirincoWATSWebDashboardModelsBinaryData
        d = dict(src_dict)
        _logo_binary_data = d.pop("logoBinaryData", UNSET)
        logo_binary_data: Union[Unset, VirincoWATSWebDashboardModelsBinaryData]
        if isinstance(_logo_binary_data,  Unset):
            logo_binary_data = UNSET
        else:
            logo_binary_data = VirincoWATSWebDashboardModelsBinaryData.from_dict(_logo_binary_data)




        virinco_wats_web_dashboard_models_tdm_account_admin_settings = cls(
            logo_binary_data=logo_binary_data,
        )


        virinco_wats_web_dashboard_models_tdm_account_admin_settings.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_account_admin_settings

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
