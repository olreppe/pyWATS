from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_controllers_api_transfer_result_request import VirincoWATSWebDashboardControllersApiTransferResultRequest





T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiTransferBatchResult")



@_attrs_define
class VirincoWATSWebDashboardControllersApiTransferBatchResult:
    """ 
        Attributes:
            rulename (Union[Unset, str]): Rule name of transferbatch
            reports (Union[Unset, list['VirincoWATSWebDashboardControllersApiTransferResultRequest']]): Results in batch
     """

    rulename: Union[Unset, str] = UNSET
    reports: Union[Unset, list['VirincoWATSWebDashboardControllersApiTransferResultRequest']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_controllers_api_transfer_result_request import VirincoWATSWebDashboardControllersApiTransferResultRequest
        rulename = self.rulename

        reports: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.reports, Unset):
            reports = []
            for reports_item_data in self.reports:
                reports_item = reports_item_data.to_dict()
                reports.append(reports_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if rulename is not UNSET:
            field_dict["rulename"] = rulename
        if reports is not UNSET:
            field_dict["reports"] = reports

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_controllers_api_transfer_result_request import VirincoWATSWebDashboardControllersApiTransferResultRequest
        d = dict(src_dict)
        rulename = d.pop("rulename", UNSET)

        reports = []
        _reports = d.pop("reports", UNSET)
        for reports_item_data in (_reports or []):
            reports_item = VirincoWATSWebDashboardControllersApiTransferResultRequest.from_dict(reports_item_data)



            reports.append(reports_item)


        virinco_wats_web_dashboard_controllers_api_transfer_batch_result = cls(
            rulename=rulename,
            reports=reports,
        )


        virinco_wats_web_dashboard_controllers_api_transfer_batch_result.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_transfer_batch_result

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
