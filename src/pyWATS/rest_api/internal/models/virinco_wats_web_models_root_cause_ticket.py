from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_models_root_cause_ticket_priority import VirincoWATSWebModelsRootCauseTicketPriority
from ..models.virinco_wats_web_models_root_cause_ticket_status import VirincoWATSWebModelsRootCauseTicketStatus
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_models_root_cause_update import VirincoWATSWebModelsRootCauseUpdate
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting





T = TypeVar("T", bound="VirincoWATSWebModelsRootCauseTicket")



@_attrs_define
class VirincoWATSWebModelsRootCauseTicket:
    """ 
        Attributes:
            ticket_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            ticket_number (Union[Unset, int]):
            progress (Union[Unset, str]):
            owner (Union[Unset, str]):
            assignee (Union[Unset, str]):
            subject (Union[Unset, str]):
            status (Union[Unset, VirincoWATSWebModelsRootCauseTicketStatus]):
            priority (Union[Unset, VirincoWATSWebModelsRootCauseTicketPriority]):
            report_uuid (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            created_utc (Union[Unset, datetime.datetime]):
            updated_utc (Union[Unset, datetime.datetime]):
            team (Union[Unset, str]):
            origin (Union[Unset, str]):
            tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]):
            history (Union[Unset, list['VirincoWATSWebModelsRootCauseUpdate']]):
            update (Union[Unset, VirincoWATSWebModelsRootCauseUpdate]):
     """

    ticket_id: Union[Unset, UUID] = UNSET
    ticket_number: Union[Unset, int] = UNSET
    progress: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    assignee: Union[Unset, str] = UNSET
    subject: Union[Unset, str] = UNSET
    status: Union[Unset, VirincoWATSWebModelsRootCauseTicketStatus] = UNSET
    priority: Union[Unset, VirincoWATSWebModelsRootCauseTicketPriority] = UNSET
    report_uuid: Union[Unset, UUID] = UNSET
    created_utc: Union[Unset, datetime.datetime] = UNSET
    updated_utc: Union[Unset, datetime.datetime] = UNSET
    team: Union[Unset, str] = UNSET
    origin: Union[Unset, str] = UNSET
    tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    history: Union[Unset, list['VirincoWATSWebModelsRootCauseUpdate']] = UNSET
    update: Union[Unset, 'VirincoWATSWebModelsRootCauseUpdate'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_models_root_cause_update import VirincoWATSWebModelsRootCauseUpdate
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        ticket_id: Union[Unset, str] = UNSET
        if not isinstance(self.ticket_id, Unset):
            ticket_id = str(self.ticket_id)

        ticket_number = self.ticket_number

        progress = self.progress

        owner = self.owner

        assignee = self.assignee

        subject = self.subject

        status: Union[Unset, int] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


        priority: Union[Unset, int] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.value


        report_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.report_uuid, Unset):
            report_uuid = str(self.report_uuid)

        created_utc: Union[Unset, str] = UNSET
        if not isinstance(self.created_utc, Unset):
            created_utc = self.created_utc.isoformat()

        updated_utc: Union[Unset, str] = UNSET
        if not isinstance(self.updated_utc, Unset):
            updated_utc = self.updated_utc.isoformat()

        team = self.team

        origin = self.origin

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)



        history: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.history, Unset):
            history = []
            for history_item_data in self.history:
                history_item = history_item_data.to_dict()
                history.append(history_item)



        update: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.update, Unset):
            update = self.update.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if ticket_id is not UNSET:
            field_dict["ticketId"] = ticket_id
        if ticket_number is not UNSET:
            field_dict["ticketNumber"] = ticket_number
        if progress is not UNSET:
            field_dict["progress"] = progress
        if owner is not UNSET:
            field_dict["owner"] = owner
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if subject is not UNSET:
            field_dict["subject"] = subject
        if status is not UNSET:
            field_dict["status"] = status
        if priority is not UNSET:
            field_dict["priority"] = priority
        if report_uuid is not UNSET:
            field_dict["reportUuid"] = report_uuid
        if created_utc is not UNSET:
            field_dict["createdUtc"] = created_utc
        if updated_utc is not UNSET:
            field_dict["updatedUtc"] = updated_utc
        if team is not UNSET:
            field_dict["team"] = team
        if origin is not UNSET:
            field_dict["origin"] = origin
        if tags is not UNSET:
            field_dict["tags"] = tags
        if history is not UNSET:
            field_dict["history"] = history
        if update is not UNSET:
            field_dict["update"] = update

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_models_root_cause_update import VirincoWATSWebModelsRootCauseUpdate
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        d = dict(src_dict)
        _ticket_id = d.pop("ticketId", UNSET)
        ticket_id: Union[Unset, UUID]
        if isinstance(_ticket_id,  Unset):
            ticket_id = UNSET
        else:
            ticket_id = UUID(_ticket_id)




        ticket_number = d.pop("ticketNumber", UNSET)

        progress = d.pop("progress", UNSET)

        owner = d.pop("owner", UNSET)

        assignee = d.pop("assignee", UNSET)

        subject = d.pop("subject", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, VirincoWATSWebModelsRootCauseTicketStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = VirincoWATSWebModelsRootCauseTicketStatus(_status)




        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, VirincoWATSWebModelsRootCauseTicketPriority]
        if isinstance(_priority,  Unset):
            priority = UNSET
        else:
            priority = VirincoWATSWebModelsRootCauseTicketPriority(_priority)




        _report_uuid = d.pop("reportUuid", UNSET)
        report_uuid: Union[Unset, UUID]
        if isinstance(_report_uuid,  Unset):
            report_uuid = UNSET
        else:
            report_uuid = UUID(_report_uuid)




        _created_utc = d.pop("createdUtc", UNSET)
        created_utc: Union[Unset, datetime.datetime]
        if isinstance(_created_utc,  Unset):
            created_utc = UNSET
        else:
            created_utc = isoparse(_created_utc)




        _updated_utc = d.pop("updatedUtc", UNSET)
        updated_utc: Union[Unset, datetime.datetime]
        if isinstance(_updated_utc,  Unset):
            updated_utc = UNSET
        else:
            updated_utc = isoparse(_updated_utc)




        team = d.pop("team", UNSET)

        origin = d.pop("origin", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in (_tags or []):
            tags_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(tags_item_data)



            tags.append(tags_item)


        history = []
        _history = d.pop("history", UNSET)
        for history_item_data in (_history or []):
            history_item = VirincoWATSWebModelsRootCauseUpdate.from_dict(history_item_data)



            history.append(history_item)


        _update = d.pop("update", UNSET)
        update: Union[Unset, VirincoWATSWebModelsRootCauseUpdate]
        if isinstance(_update,  Unset):
            update = UNSET
        else:
            update = VirincoWATSWebModelsRootCauseUpdate.from_dict(_update)




        virinco_wats_web_models_root_cause_ticket = cls(
            ticket_id=ticket_id,
            ticket_number=ticket_number,
            progress=progress,
            owner=owner,
            assignee=assignee,
            subject=subject,
            status=status,
            priority=priority,
            report_uuid=report_uuid,
            created_utc=created_utc,
            updated_utc=updated_utc,
            team=team,
            origin=origin,
            tags=tags,
            history=history,
            update=update,
        )


        virinco_wats_web_models_root_cause_ticket.additional_properties = d
        return virinco_wats_web_models_root_cause_ticket

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
