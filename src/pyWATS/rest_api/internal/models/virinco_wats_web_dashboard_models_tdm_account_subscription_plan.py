from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_account_subscription_plan_subscription import VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlanSubscription
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_storage_usage_history import VirincoWATSWebDashboardModelsTdmStorageUsageHistory





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlan:
    """ 
        Attributes:
            subscription (Union[Unset, VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlanSubscription]):
            user_count (Union[Unset, int]):
            storage_usage_history (Union[Unset, list['VirincoWATSWebDashboardModelsTdmStorageUsageHistory']]):
            active_storage_plan (Union[Unset, int]):
            binary_file_storage_gb (Union[Unset, int]):
            binary_storage_used_gb (Union[Unset, int]):
            is_degraded (Union[Unset, bool]):
            is_suspended (Union[Unset, bool]):
     """

    subscription: Union[Unset, VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlanSubscription] = UNSET
    user_count: Union[Unset, int] = UNSET
    storage_usage_history: Union[Unset, list['VirincoWATSWebDashboardModelsTdmStorageUsageHistory']] = UNSET
    active_storage_plan: Union[Unset, int] = UNSET
    binary_file_storage_gb: Union[Unset, int] = UNSET
    binary_storage_used_gb: Union[Unset, int] = UNSET
    is_degraded: Union[Unset, bool] = UNSET
    is_suspended: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_storage_usage_history import VirincoWATSWebDashboardModelsTdmStorageUsageHistory
        subscription: Union[Unset, int] = UNSET
        if not isinstance(self.subscription, Unset):
            subscription = self.subscription.value


        user_count = self.user_count

        storage_usage_history: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.storage_usage_history, Unset):
            storage_usage_history = []
            for storage_usage_history_item_data in self.storage_usage_history:
                storage_usage_history_item = storage_usage_history_item_data.to_dict()
                storage_usage_history.append(storage_usage_history_item)



        active_storage_plan = self.active_storage_plan

        binary_file_storage_gb = self.binary_file_storage_gb

        binary_storage_used_gb = self.binary_storage_used_gb

        is_degraded = self.is_degraded

        is_suspended = self.is_suspended


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if subscription is not UNSET:
            field_dict["subscription"] = subscription
        if user_count is not UNSET:
            field_dict["userCount"] = user_count
        if storage_usage_history is not UNSET:
            field_dict["storageUsageHistory"] = storage_usage_history
        if active_storage_plan is not UNSET:
            field_dict["activeStoragePlan"] = active_storage_plan
        if binary_file_storage_gb is not UNSET:
            field_dict["binaryFileStorageGB"] = binary_file_storage_gb
        if binary_storage_used_gb is not UNSET:
            field_dict["binaryStorageUsedGB"] = binary_storage_used_gb
        if is_degraded is not UNSET:
            field_dict["isDegraded"] = is_degraded
        if is_suspended is not UNSET:
            field_dict["isSuspended"] = is_suspended

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_storage_usage_history import VirincoWATSWebDashboardModelsTdmStorageUsageHistory
        d = dict(src_dict)
        _subscription = d.pop("subscription", UNSET)
        subscription: Union[Unset, VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlanSubscription]
        if isinstance(_subscription,  Unset):
            subscription = UNSET
        else:
            subscription = VirincoWATSWebDashboardModelsTdmAccountSubscriptionPlanSubscription(_subscription)




        user_count = d.pop("userCount", UNSET)

        storage_usage_history = []
        _storage_usage_history = d.pop("storageUsageHistory", UNSET)
        for storage_usage_history_item_data in (_storage_usage_history or []):
            storage_usage_history_item = VirincoWATSWebDashboardModelsTdmStorageUsageHistory.from_dict(storage_usage_history_item_data)



            storage_usage_history.append(storage_usage_history_item)


        active_storage_plan = d.pop("activeStoragePlan", UNSET)

        binary_file_storage_gb = d.pop("binaryFileStorageGB", UNSET)

        binary_storage_used_gb = d.pop("binaryStorageUsedGB", UNSET)

        is_degraded = d.pop("isDegraded", UNSET)

        is_suspended = d.pop("isSuspended", UNSET)

        virinco_wats_web_dashboard_models_tdm_account_subscription_plan = cls(
            subscription=subscription,
            user_count=user_count,
            storage_usage_history=storage_usage_history,
            active_storage_plan=active_storage_plan,
            binary_file_storage_gb=binary_file_storage_gb,
            binary_storage_used_gb=binary_storage_used_gb,
            is_degraded=is_degraded,
            is_suspended=is_suspended,
        )


        virinco_wats_web_dashboard_models_tdm_account_subscription_plan.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_account_subscription_plan

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
