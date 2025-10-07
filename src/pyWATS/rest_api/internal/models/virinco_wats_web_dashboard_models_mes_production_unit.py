from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
  from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision
  from ..models.virinco_wats_web_dashboard_models_mes_production_production_batch import VirincoWATSWebDashboardModelsMesProductionProductionBatch
  from ..models.virinco_wats_web_dashboard_models_mes_product_product import VirincoWATSWebDashboardModelsMesProductProduct
  from ..models.virinco_wats_web_dashboard_models_mes_process import VirincoWATSWebDashboardModelsMesProcess





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionUnit")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionUnit:
    """ 
        Attributes:
            unit_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_unit_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            product_revision_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            batch_sn (Union[Unset, str]):
            serial_number (Union[Unset, str]):
            serial_date (Union[Unset, datetime.datetime]):
            current_location (Union[Unset, str]):
            xml_data (Union[Unset, str]):
            unit_phase_id (Union[Unset, int]):
            process_code (Union[Unset, int]):
            product_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            product_revision (Union[Unset, VirincoWATSWebDashboardModelsMesProductProductRevision]):
            process (Union[Unset, VirincoWATSWebDashboardModelsMesProcess]):
            product (Union[Unset, VirincoWATSWebDashboardModelsMesProductProduct]):
            production_batch (Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionBatch]):
            action (Union[Unset, str]):
            error (Union[Unset, str]):
            children (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionUnit']]):
            settings (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]):
            level (Union[Unset, int]):
     """

    unit_id: Union[Unset, UUID] = UNSET
    parent_unit_id: Union[Unset, UUID] = UNSET
    product_revision_id: Union[Unset, UUID] = UNSET
    batch_sn: Union[Unset, str] = UNSET
    serial_number: Union[Unset, str] = UNSET
    serial_date: Union[Unset, datetime.datetime] = UNSET
    current_location: Union[Unset, str] = UNSET
    xml_data: Union[Unset, str] = UNSET
    unit_phase_id: Union[Unset, int] = UNSET
    process_code: Union[Unset, int] = UNSET
    product_id: Union[Unset, UUID] = UNSET
    product_revision: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductProductRevision'] = UNSET
    process: Union[Unset, 'VirincoWATSWebDashboardModelsMesProcess'] = UNSET
    product: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductProduct'] = UNSET
    production_batch: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductionProductionBatch'] = UNSET
    action: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    children: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionUnit']] = UNSET
    settings: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    level: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_batch import VirincoWATSWebDashboardModelsMesProductionProductionBatch
        from ..models.virinco_wats_web_dashboard_models_mes_product_product import VirincoWATSWebDashboardModelsMesProductProduct
        from ..models.virinco_wats_web_dashboard_models_mes_process import VirincoWATSWebDashboardModelsMesProcess
        unit_id: Union[Unset, str] = UNSET
        if not isinstance(self.unit_id, Unset):
            unit_id = str(self.unit_id)

        parent_unit_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_unit_id, Unset):
            parent_unit_id = str(self.parent_unit_id)

        product_revision_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_revision_id, Unset):
            product_revision_id = str(self.product_revision_id)

        batch_sn = self.batch_sn

        serial_number = self.serial_number

        serial_date: Union[Unset, str] = UNSET
        if not isinstance(self.serial_date, Unset):
            serial_date = self.serial_date.isoformat()

        current_location = self.current_location

        xml_data = self.xml_data

        unit_phase_id = self.unit_phase_id

        process_code = self.process_code

        product_id: Union[Unset, str] = UNSET
        if not isinstance(self.product_id, Unset):
            product_id = str(self.product_id)

        product_revision: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.product_revision, Unset):
            product_revision = self.product_revision.to_dict()

        process: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.process, Unset):
            process = self.process.to_dict()

        product: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.product, Unset):
            product = self.product.to_dict()

        production_batch: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.production_batch, Unset):
            production_batch = self.production_batch.to_dict()

        action = self.action

        error = self.error

        children: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)



        settings: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.settings, Unset):
            settings = []
            for settings_item_data in self.settings:
                settings_item = settings_item_data.to_dict()
                settings.append(settings_item)



        level = self.level


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if unit_id is not UNSET:
            field_dict["UnitId"] = unit_id
        if parent_unit_id is not UNSET:
            field_dict["ParentUnitId"] = parent_unit_id
        if product_revision_id is not UNSET:
            field_dict["ProductRevisionId"] = product_revision_id
        if batch_sn is not UNSET:
            field_dict["BatchSN"] = batch_sn
        if serial_number is not UNSET:
            field_dict["SerialNumber"] = serial_number
        if serial_date is not UNSET:
            field_dict["SerialDate"] = serial_date
        if current_location is not UNSET:
            field_dict["CurrentLocation"] = current_location
        if xml_data is not UNSET:
            field_dict["XMLData"] = xml_data
        if unit_phase_id is not UNSET:
            field_dict["UnitPhaseId"] = unit_phase_id
        if process_code is not UNSET:
            field_dict["ProcessCode"] = process_code
        if product_id is not UNSET:
            field_dict["ProductId"] = product_id
        if product_revision is not UNSET:
            field_dict["ProductRevision"] = product_revision
        if process is not UNSET:
            field_dict["Process"] = process
        if product is not UNSET:
            field_dict["Product"] = product
        if production_batch is not UNSET:
            field_dict["ProductionBatch"] = production_batch
        if action is not UNSET:
            field_dict["Action"] = action
        if error is not UNSET:
            field_dict["Error"] = error
        if children is not UNSET:
            field_dict["Children"] = children
        if settings is not UNSET:
            field_dict["Settings"] = settings
        if level is not UNSET:
            field_dict["Level"] = level

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_product_product_revision import VirincoWATSWebDashboardModelsMesProductProductRevision
        from ..models.virinco_wats_web_dashboard_models_mes_production_production_batch import VirincoWATSWebDashboardModelsMesProductionProductionBatch
        from ..models.virinco_wats_web_dashboard_models_mes_product_product import VirincoWATSWebDashboardModelsMesProductProduct
        from ..models.virinco_wats_web_dashboard_models_mes_process import VirincoWATSWebDashboardModelsMesProcess
        d = dict(src_dict)
        _unit_id = d.pop("UnitId", UNSET)
        unit_id: Union[Unset, UUID]
        if isinstance(_unit_id,  Unset):
            unit_id = UNSET
        else:
            unit_id = UUID(_unit_id)




        _parent_unit_id = d.pop("ParentUnitId", UNSET)
        parent_unit_id: Union[Unset, UUID]
        if isinstance(_parent_unit_id,  Unset):
            parent_unit_id = UNSET
        else:
            parent_unit_id = UUID(_parent_unit_id)




        _product_revision_id = d.pop("ProductRevisionId", UNSET)
        product_revision_id: Union[Unset, UUID]
        if isinstance(_product_revision_id,  Unset):
            product_revision_id = UNSET
        else:
            product_revision_id = UUID(_product_revision_id)




        batch_sn = d.pop("BatchSN", UNSET)

        serial_number = d.pop("SerialNumber", UNSET)

        _serial_date = d.pop("SerialDate", UNSET)
        serial_date: Union[Unset, datetime.datetime]
        if isinstance(_serial_date,  Unset):
            serial_date = UNSET
        else:
            serial_date = isoparse(_serial_date)




        current_location = d.pop("CurrentLocation", UNSET)

        xml_data = d.pop("XMLData", UNSET)

        unit_phase_id = d.pop("UnitPhaseId", UNSET)

        process_code = d.pop("ProcessCode", UNSET)

        _product_id = d.pop("ProductId", UNSET)
        product_id: Union[Unset, UUID]
        if isinstance(_product_id,  Unset):
            product_id = UNSET
        else:
            product_id = UUID(_product_id)




        _product_revision = d.pop("ProductRevision", UNSET)
        product_revision: Union[Unset, VirincoWATSWebDashboardModelsMesProductProductRevision]
        if isinstance(_product_revision,  Unset):
            product_revision = UNSET
        else:
            product_revision = VirincoWATSWebDashboardModelsMesProductProductRevision.from_dict(_product_revision)




        _process = d.pop("Process", UNSET)
        process: Union[Unset, VirincoWATSWebDashboardModelsMesProcess]
        if isinstance(_process,  Unset):
            process = UNSET
        else:
            process = VirincoWATSWebDashboardModelsMesProcess.from_dict(_process)




        _product = d.pop("Product", UNSET)
        product: Union[Unset, VirincoWATSWebDashboardModelsMesProductProduct]
        if isinstance(_product,  Unset):
            product = UNSET
        else:
            product = VirincoWATSWebDashboardModelsMesProductProduct.from_dict(_product)




        _production_batch = d.pop("ProductionBatch", UNSET)
        production_batch: Union[Unset, VirincoWATSWebDashboardModelsMesProductionProductionBatch]
        if isinstance(_production_batch,  Unset):
            production_batch = UNSET
        else:
            production_batch = VirincoWATSWebDashboardModelsMesProductionProductionBatch.from_dict(_production_batch)




        action = d.pop("Action", UNSET)

        error = d.pop("Error", UNSET)

        children = []
        _children = d.pop("Children", UNSET)
        for children_item_data in (_children or []):
            children_item = VirincoWATSWebDashboardModelsMesProductionUnit.from_dict(children_item_data)



            children.append(children_item)


        settings = []
        _settings = d.pop("Settings", UNSET)
        for settings_item_data in (_settings or []):
            settings_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(settings_item_data)



            settings.append(settings_item)


        level = d.pop("Level", UNSET)

        virinco_wats_web_dashboard_models_mes_production_unit = cls(
            unit_id=unit_id,
            parent_unit_id=parent_unit_id,
            product_revision_id=product_revision_id,
            batch_sn=batch_sn,
            serial_number=serial_number,
            serial_date=serial_date,
            current_location=current_location,
            xml_data=xml_data,
            unit_phase_id=unit_phase_id,
            process_code=process_code,
            product_id=product_id,
            product_revision=product_revision,
            process=process,
            product=product,
            production_batch=production_batch,
            action=action,
            error=error,
            children=children,
            settings=settings,
            level=level,
        )


        virinco_wats_web_dashboard_models_mes_production_unit.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_unit

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
