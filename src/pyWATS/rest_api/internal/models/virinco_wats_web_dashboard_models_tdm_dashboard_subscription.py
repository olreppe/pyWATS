from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_dashboard_subscription_change_type import VirincoWATSWebDashboardModelsTdmDashboardSubscriptionChangeType
from ..models.virinco_wats_web_dashboard_models_tdm_dashboard_subscription_send_interval import VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSendInterval
from ..models.virinco_wats_web_dashboard_models_tdm_dashboard_subscription_subscriber_type import VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSubscriberType
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmDashboardSubscription")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmDashboardSubscription:
    """ 
        Attributes:
            id (Union[Unset, int]):
            dashboard_id (Union[Unset, int]): The id of the dashboard this subscription belongs to
            created_by (Union[Unset, str]): The if of the user which created the subscription
            subscriber (Union[Unset, str]): The user id or role which is subscribing to the dashboard
            subscriber_type (Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSubscriberType]): The type of
                subscriber
            send_interval (Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSendInterval]): The interval in
                which to send the dashboard to subscriber(s)
            processed_at (Union[Unset, datetime.datetime]):
            change_type (Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionChangeType]): The type of change
                made to this subscription, if any
     """

    id: Union[Unset, int] = UNSET
    dashboard_id: Union[Unset, int] = UNSET
    created_by: Union[Unset, str] = UNSET
    subscriber: Union[Unset, str] = UNSET
    subscriber_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSubscriberType] = UNSET
    send_interval: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSendInterval] = UNSET
    processed_at: Union[Unset, datetime.datetime] = UNSET
    change_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionChangeType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        dashboard_id = self.dashboard_id

        created_by = self.created_by

        subscriber = self.subscriber

        subscriber_type: Union[Unset, int] = UNSET
        if not isinstance(self.subscriber_type, Unset):
            subscriber_type = self.subscriber_type.value


        send_interval: Union[Unset, int] = UNSET
        if not isinstance(self.send_interval, Unset):
            send_interval = self.send_interval.value


        processed_at: Union[Unset, str] = UNSET
        if not isinstance(self.processed_at, Unset):
            processed_at = self.processed_at.isoformat()

        change_type: Union[Unset, int] = UNSET
        if not isinstance(self.change_type, Unset):
            change_type = self.change_type.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if dashboard_id is not UNSET:
            field_dict["dashboardId"] = dashboard_id
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if subscriber is not UNSET:
            field_dict["subscriber"] = subscriber
        if subscriber_type is not UNSET:
            field_dict["subscriberType"] = subscriber_type
        if send_interval is not UNSET:
            field_dict["sendInterval"] = send_interval
        if processed_at is not UNSET:
            field_dict["processedAt"] = processed_at
        if change_type is not UNSET:
            field_dict["changeType"] = change_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        dashboard_id = d.pop("dashboardId", UNSET)

        created_by = d.pop("createdBy", UNSET)

        subscriber = d.pop("subscriber", UNSET)

        _subscriber_type = d.pop("subscriberType", UNSET)
        subscriber_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSubscriberType]
        if isinstance(_subscriber_type,  Unset):
            subscriber_type = UNSET
        else:
            subscriber_type = VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSubscriberType(_subscriber_type)




        _send_interval = d.pop("sendInterval", UNSET)
        send_interval: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSendInterval]
        if isinstance(_send_interval,  Unset):
            send_interval = UNSET
        else:
            send_interval = VirincoWATSWebDashboardModelsTdmDashboardSubscriptionSendInterval(_send_interval)




        _processed_at = d.pop("processedAt", UNSET)
        processed_at: Union[Unset, datetime.datetime]
        if isinstance(_processed_at,  Unset):
            processed_at = UNSET
        else:
            processed_at = isoparse(_processed_at)




        _change_type = d.pop("changeType", UNSET)
        change_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardSubscriptionChangeType]
        if isinstance(_change_type,  Unset):
            change_type = UNSET
        else:
            change_type = VirincoWATSWebDashboardModelsTdmDashboardSubscriptionChangeType(_change_type)




        virinco_wats_web_dashboard_models_tdm_dashboard_subscription = cls(
            id=id,
            dashboard_id=dashboard_id,
            created_by=created_by,
            subscriber=subscriber,
            subscriber_type=subscriber_type,
            send_interval=send_interval,
            processed_at=processed_at,
            change_type=change_type,
        )


        virinco_wats_web_dashboard_models_tdm_dashboard_subscription.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_dashboard_subscription

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
