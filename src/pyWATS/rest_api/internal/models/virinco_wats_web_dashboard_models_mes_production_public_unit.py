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
  from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
  from ..models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import VirincoWATSWebDashboardModelsMesProductPublicProductRevision
  from ..models.virinco_wats_web_dashboard_models_mes_product_public_product import VirincoWATSWebDashboardModelsMesProductPublicProduct





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProductionPublicUnit")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProductionPublicUnit:
    """ 
        Attributes:
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            parent_serial_number (Union[Unset, str]):
            batch_number (Union[Unset, str]):
            serial_date (Union[Unset, datetime.datetime]):
            current_location (Union[Unset, str]):
            xml_data (Union[Unset, str]):
            unit_phase_id (Union[Unset, int]):
            unit_phase (Union[Unset, str]):
            process_code (Union[Unset, str]):
            tags (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']]): JSON formated xmlData
            product_revision (Union[Unset, VirincoWATSWebDashboardModelsMesProductPublicProductRevision]):
            product (Union[Unset, VirincoWATSWebDashboardModelsMesProductPublicProduct]):
            sub_units (Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionPublicUnit']]):
     """

    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    parent_serial_number: Union[Unset, str] = UNSET
    batch_number: Union[Unset, str] = UNSET
    serial_date: Union[Unset, datetime.datetime] = UNSET
    current_location: Union[Unset, str] = UNSET
    xml_data: Union[Unset, str] = UNSET
    unit_phase_id: Union[Unset, int] = UNSET
    unit_phase: Union[Unset, str] = UNSET
    process_code: Union[Unset, str] = UNSET
    tags: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductSetting']] = UNSET
    product_revision: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductPublicProductRevision'] = UNSET
    product: Union[Unset, 'VirincoWATSWebDashboardModelsMesProductPublicProduct'] = UNSET
    sub_units: Union[Unset, list['VirincoWATSWebDashboardModelsMesProductionPublicUnit']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import VirincoWATSWebDashboardModelsMesProductPublicProductRevision
        from ..models.virinco_wats_web_dashboard_models_mes_product_public_product import VirincoWATSWebDashboardModelsMesProductPublicProduct
        serial_number = self.serial_number

        part_number = self.part_number

        revision = self.revision

        parent_serial_number = self.parent_serial_number

        batch_number = self.batch_number

        serial_date: Union[Unset, str] = UNSET
        if not isinstance(self.serial_date, Unset):
            serial_date = self.serial_date.isoformat()

        current_location = self.current_location

        xml_data = self.xml_data

        unit_phase_id = self.unit_phase_id

        unit_phase = self.unit_phase

        process_code = self.process_code

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)



        product_revision: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.product_revision, Unset):
            product_revision = self.product_revision.to_dict()

        product: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.product, Unset):
            product = self.product.to_dict()

        sub_units: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sub_units, Unset):
            sub_units = []
            for sub_units_item_data in self.sub_units:
                sub_units_item = sub_units_item_data.to_dict()
                sub_units.append(sub_units_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if parent_serial_number is not UNSET:
            field_dict["parentSerialNumber"] = parent_serial_number
        if batch_number is not UNSET:
            field_dict["batchNumber"] = batch_number
        if serial_date is not UNSET:
            field_dict["serialDate"] = serial_date
        if current_location is not UNSET:
            field_dict["currentLocation"] = current_location
        if xml_data is not UNSET:
            field_dict["xmlData"] = xml_data
        if unit_phase_id is not UNSET:
            field_dict["unitPhaseId"] = unit_phase_id
        if unit_phase is not UNSET:
            field_dict["unitPhase"] = unit_phase
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if product_revision is not UNSET:
            field_dict["productRevision"] = product_revision
        if product is not UNSET:
            field_dict["product"] = product
        if sub_units is not UNSET:
            field_dict["subUnits"] = sub_units

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_product_setting import VirincoWATSWebDashboardModelsMesProductSetting
        from ..models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import VirincoWATSWebDashboardModelsMesProductPublicProductRevision
        from ..models.virinco_wats_web_dashboard_models_mes_product_public_product import VirincoWATSWebDashboardModelsMesProductPublicProduct
        d = dict(src_dict)
        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        parent_serial_number = d.pop("parentSerialNumber", UNSET)

        batch_number = d.pop("batchNumber", UNSET)

        _serial_date = d.pop("serialDate", UNSET)
        serial_date: Union[Unset, datetime.datetime]
        if isinstance(_serial_date,  Unset):
            serial_date = UNSET
        else:
            serial_date = isoparse(_serial_date)




        current_location = d.pop("currentLocation", UNSET)

        xml_data = d.pop("xmlData", UNSET)

        unit_phase_id = d.pop("unitPhaseId", UNSET)

        unit_phase = d.pop("unitPhase", UNSET)

        process_code = d.pop("processCode", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in (_tags or []):
            tags_item = VirincoWATSWebDashboardModelsMesProductSetting.from_dict(tags_item_data)



            tags.append(tags_item)


        _product_revision = d.pop("productRevision", UNSET)
        product_revision: Union[Unset, VirincoWATSWebDashboardModelsMesProductPublicProductRevision]
        if isinstance(_product_revision,  Unset):
            product_revision = UNSET
        else:
            product_revision = VirincoWATSWebDashboardModelsMesProductPublicProductRevision.from_dict(_product_revision)




        _product = d.pop("product", UNSET)
        product: Union[Unset, VirincoWATSWebDashboardModelsMesProductPublicProduct]
        if isinstance(_product,  Unset):
            product = UNSET
        else:
            product = VirincoWATSWebDashboardModelsMesProductPublicProduct.from_dict(_product)




        sub_units = []
        _sub_units = d.pop("subUnits", UNSET)
        for sub_units_item_data in (_sub_units or []):
            sub_units_item = VirincoWATSWebDashboardModelsMesProductionPublicUnit.from_dict(sub_units_item_data)



            sub_units.append(sub_units_item)


        virinco_wats_web_dashboard_models_mes_production_public_unit = cls(
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            parent_serial_number=parent_serial_number,
            batch_number=batch_number,
            serial_date=serial_date,
            current_location=current_location,
            xml_data=xml_data,
            unit_phase_id=unit_phase_id,
            unit_phase=unit_phase,
            process_code=process_code,
            tags=tags,
            product_revision=product_revision,
            product=product,
            sub_units=sub_units,
        )


        virinco_wats_web_dashboard_models_mes_production_public_unit.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_production_public_unit

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
