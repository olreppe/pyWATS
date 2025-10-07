from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_trigger_type import VirincoWATSWebDashboardModelsTdmTriggerType
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_trigger_field import VirincoWATSWebDashboardModelsTdmTriggerField
  from ..models.virinco_wats_web_dashboard_models_tdm_trigger_action import VirincoWATSWebDashboardModelsTdmTriggerAction





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmTrigger")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmTrigger:
    """ 
        Attributes:
            id (Union[Unset, int]):
            name (Union[Unset, str]):
            owner (Union[Unset, str]):
            created (Union[Unset, datetime.datetime]):
            last_triggered (Union[Unset, datetime.datetime]):
            trigger_fields (Union[Unset, list['VirincoWATSWebDashboardModelsTdmTriggerField']]):
            trigger_actions (Union[Unset, list['VirincoWATSWebDashboardModelsTdmTriggerAction']]):
            cooldown (Union[Unset, int]): Cooldown Minutes - No actions performed during this period (LastTriggered +
                Cooldown)
            description (Union[Unset, str]):
            status (Union[Unset, int]):
            type_ (Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerType]):
            last_run (Union[Unset, datetime.datetime]):
            total_executions (Union[Unset, int]):
            max_executions (Union[Unset, int]):
            periods (Union[Unset, int]):
     """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    last_triggered: Union[Unset, datetime.datetime] = UNSET
    trigger_fields: Union[Unset, list['VirincoWATSWebDashboardModelsTdmTriggerField']] = UNSET
    trigger_actions: Union[Unset, list['VirincoWATSWebDashboardModelsTdmTriggerAction']] = UNSET
    cooldown: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    type_: Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerType] = UNSET
    last_run: Union[Unset, datetime.datetime] = UNSET
    total_executions: Union[Unset, int] = UNSET
    max_executions: Union[Unset, int] = UNSET
    periods: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_trigger_field import VirincoWATSWebDashboardModelsTdmTriggerField
        from ..models.virinco_wats_web_dashboard_models_tdm_trigger_action import VirincoWATSWebDashboardModelsTdmTriggerAction
        id = self.id

        name = self.name

        owner = self.owner

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        last_triggered: Union[Unset, str] = UNSET
        if not isinstance(self.last_triggered, Unset):
            last_triggered = self.last_triggered.isoformat()

        trigger_fields: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.trigger_fields, Unset):
            trigger_fields = []
            for trigger_fields_item_data in self.trigger_fields:
                trigger_fields_item = trigger_fields_item_data.to_dict()
                trigger_fields.append(trigger_fields_item)



        trigger_actions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.trigger_actions, Unset):
            trigger_actions = []
            for trigger_actions_item_data in self.trigger_actions:
                trigger_actions_item = trigger_actions_item_data.to_dict()
                trigger_actions.append(trigger_actions_item)



        cooldown = self.cooldown

        description = self.description

        status = self.status

        type_: Union[Unset, int] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value


        last_run: Union[Unset, str] = UNSET
        if not isinstance(self.last_run, Unset):
            last_run = self.last_run.isoformat()

        total_executions = self.total_executions

        max_executions = self.max_executions

        periods = self.periods


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if owner is not UNSET:
            field_dict["owner"] = owner
        if created is not UNSET:
            field_dict["created"] = created
        if last_triggered is not UNSET:
            field_dict["lastTriggered"] = last_triggered
        if trigger_fields is not UNSET:
            field_dict["triggerFields"] = trigger_fields
        if trigger_actions is not UNSET:
            field_dict["triggerActions"] = trigger_actions
        if cooldown is not UNSET:
            field_dict["cooldown"] = cooldown
        if description is not UNSET:
            field_dict["description"] = description
        if status is not UNSET:
            field_dict["status"] = status
        if type_ is not UNSET:
            field_dict["type"] = type_
        if last_run is not UNSET:
            field_dict["lastRun"] = last_run
        if total_executions is not UNSET:
            field_dict["totalExecutions"] = total_executions
        if max_executions is not UNSET:
            field_dict["maxExecutions"] = max_executions
        if periods is not UNSET:
            field_dict["periods"] = periods

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_trigger_field import VirincoWATSWebDashboardModelsTdmTriggerField
        from ..models.virinco_wats_web_dashboard_models_tdm_trigger_action import VirincoWATSWebDashboardModelsTdmTriggerAction
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        owner = d.pop("owner", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created,  Unset):
            created = UNSET
        else:
            created = isoparse(_created)




        _last_triggered = d.pop("lastTriggered", UNSET)
        last_triggered: Union[Unset, datetime.datetime]
        if isinstance(_last_triggered,  Unset):
            last_triggered = UNSET
        else:
            last_triggered = isoparse(_last_triggered)




        trigger_fields = []
        _trigger_fields = d.pop("triggerFields", UNSET)
        for trigger_fields_item_data in (_trigger_fields or []):
            trigger_fields_item = VirincoWATSWebDashboardModelsTdmTriggerField.from_dict(trigger_fields_item_data)



            trigger_fields.append(trigger_fields_item)


        trigger_actions = []
        _trigger_actions = d.pop("triggerActions", UNSET)
        for trigger_actions_item_data in (_trigger_actions or []):
            trigger_actions_item = VirincoWATSWebDashboardModelsTdmTriggerAction.from_dict(trigger_actions_item_data)



            trigger_actions.append(trigger_actions_item)


        cooldown = d.pop("cooldown", UNSET)

        description = d.pop("description", UNSET)

        status = d.pop("status", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerType]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = VirincoWATSWebDashboardModelsTdmTriggerType(_type_)




        _last_run = d.pop("lastRun", UNSET)
        last_run: Union[Unset, datetime.datetime]
        if isinstance(_last_run,  Unset):
            last_run = UNSET
        else:
            last_run = isoparse(_last_run)




        total_executions = d.pop("totalExecutions", UNSET)

        max_executions = d.pop("maxExecutions", UNSET)

        periods = d.pop("periods", UNSET)

        virinco_wats_web_dashboard_models_tdm_trigger = cls(
            id=id,
            name=name,
            owner=owner,
            created=created,
            last_triggered=last_triggered,
            trigger_fields=trigger_fields,
            trigger_actions=trigger_actions,
            cooldown=cooldown,
            description=description,
            status=status,
            type_=type_,
            last_run=last_run,
            total_executions=total_executions,
            max_executions=max_executions,
            periods=periods,
        )


        virinco_wats_web_dashboard_models_tdm_trigger.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_trigger

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
