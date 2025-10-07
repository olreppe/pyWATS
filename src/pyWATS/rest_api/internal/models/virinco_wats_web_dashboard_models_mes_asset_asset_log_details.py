from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_log import VirincoWATSWebDashboardModelsMesAssetAssetLog





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesAssetAssetLogDetails")



@_attrs_define
class VirincoWATSWebDashboardModelsMesAssetAssetLogDetails:
    """ 
        Attributes:
            log_id (Union[Unset, int]):
            asset_log (Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetLog]):
     """

    log_id: Union[Unset, int] = UNSET
    asset_log: Union[Unset, 'VirincoWATSWebDashboardModelsMesAssetAssetLog'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_log import VirincoWATSWebDashboardModelsMesAssetAssetLog
        log_id = self.log_id

        asset_log: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.asset_log, Unset):
            asset_log = self.asset_log.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if log_id is not UNSET:
            field_dict["logId"] = log_id
        if asset_log is not UNSET:
            field_dict["assetLog"] = asset_log

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_asset_asset_log import VirincoWATSWebDashboardModelsMesAssetAssetLog
        d = dict(src_dict)
        log_id = d.pop("logId", UNSET)

        _asset_log = d.pop("assetLog", UNSET)
        asset_log: Union[Unset, VirincoWATSWebDashboardModelsMesAssetAssetLog]
        if isinstance(_asset_log,  Unset):
            asset_log = UNSET
        else:
            asset_log = VirincoWATSWebDashboardModelsMesAssetAssetLog.from_dict(_asset_log)




        virinco_wats_web_dashboard_models_mes_asset_asset_log_details = cls(
            log_id=log_id,
            asset_log=asset_log,
        )


        virinco_wats_web_dashboard_models_mes_asset_asset_log_details.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_asset_asset_log_details

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
