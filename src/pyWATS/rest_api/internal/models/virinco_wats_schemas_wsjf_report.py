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
  from ..models.virinco_wats_schemas_wsjf_sub_unit import VirincoWATSSchemasWSJFSubUnit
  from ..models.virinco_wats_schemas_wsjf_binary_data import VirincoWATSSchemasWSJFBinaryData
  from ..models.virinco_wats_schemas_wsjf_step import VirincoWATSSchemasWSJFStep
  from ..models.virinco_wats_schemas_wsjf_misc_info import VirincoWATSSchemasWSJFMiscInfo
  from ..models.virinco_wats_schemas_wsjf_additional_data import VirincoWATSSchemasWSJFAdditionalData
  from ..models.virinco_wats_schemas_wsjfuur import VirincoWATSSchemasWSJFUUR
  from ..models.virinco_wats_schemas_wsjfuut import VirincoWATSSchemasWSJFUUT
  from ..models.virinco_wats_schemas_wsjf_asset import VirincoWATSSchemasWSJFAsset
  from ..models.virinco_wats_schemas_wsjf_asset_stats import VirincoWATSSchemasWSJFAssetStats





T = TypeVar("T", bound="VirincoWATSSchemasWSJFReport")



@_attrs_define
class VirincoWATSSchemasWSJFReport:
    """ 
        Attributes:
            type_ (Union[Unset, str]): Report type, valid values: T,R (Test, Repair).
            id (Union[Unset, UUID]): Report unique identifier (Guid). Example: 00000000-0000-0000-0000-000000000000.
            pn (Union[Unset, str]): Part number of the unit.
            sn (Union[Unset, str]): Serial number of the unit.
            rev (Union[Unset, str]): Revision number of the unit.
            product_name (Union[Unset, str]): Product name of the unit.
            process_code (Union[Unset, int]): Process code of the report.
            process_code_format (Union[Unset, str]): Number format of process code.
            process_name (Union[Unset, str]): Name of process of the report.
            result (Union[Unset, str]): Status code, valid values: P,F,E,T (Passed, Failed, Error, Terminated).
            machine_name (Union[Unset, str]): Station's machine name.
            location (Union[Unset, str]): Station's location.
            purpose (Union[Unset, str]): Station's purpose.
            origin (Union[Unset, str]): The client or user the report belongs to.
            start (Union[Unset, datetime.datetime]): Report start date/time in local timezone.
            start_utc (Union[Unset, datetime.datetime]): Report start date/time in utc timezone.
            root (Union[Unset, VirincoWATSSchemasWSJFStep]):
            uut (Union[Unset, VirincoWATSSchemasWSJFUUT]):
            uur (Union[Unset, VirincoWATSSchemasWSJFUUR]):
            misc_infos (Union[Unset, list['VirincoWATSSchemasWSJFMiscInfo']]): List of misc-infos.
            sub_units (Union[Unset, list['VirincoWATSSchemasWSJFSubUnit']]): List of subunits.
                Can also be specified a hierachy (currently used only in repairs) using parent relation.
            assets (Union[Unset, list['VirincoWATSSchemasWSJFAsset']]): List of assets used in test.
            asset_stats (Union[Unset, list['VirincoWATSSchemasWSJFAssetStats']]): List of stats for assets used in test.
            binary_data (Union[Unset, list['VirincoWATSSchemasWSJFBinaryData']]): List of attachments on main unit (only
                valid for repair).
            additional_data (Union[Unset, list['VirincoWATSSchemasWSJFAdditionalData']]): List of additional header data.
     """

    type_: Union[Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    pn: Union[Unset, str] = UNSET
    sn: Union[Unset, str] = UNSET
    rev: Union[Unset, str] = UNSET
    product_name: Union[Unset, str] = UNSET
    process_code: Union[Unset, int] = UNSET
    process_code_format: Union[Unset, str] = UNSET
    process_name: Union[Unset, str] = UNSET
    result: Union[Unset, str] = UNSET
    machine_name: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    purpose: Union[Unset, str] = UNSET
    origin: Union[Unset, str] = UNSET
    start: Union[Unset, datetime.datetime] = UNSET
    start_utc: Union[Unset, datetime.datetime] = UNSET
    root: Union[Unset, 'VirincoWATSSchemasWSJFStep'] = UNSET
    uut: Union[Unset, 'VirincoWATSSchemasWSJFUUT'] = UNSET
    uur: Union[Unset, 'VirincoWATSSchemasWSJFUUR'] = UNSET
    misc_infos: Union[Unset, list['VirincoWATSSchemasWSJFMiscInfo']] = UNSET
    sub_units: Union[Unset, list['VirincoWATSSchemasWSJFSubUnit']] = UNSET
    assets: Union[Unset, list['VirincoWATSSchemasWSJFAsset']] = UNSET
    asset_stats: Union[Unset, list['VirincoWATSSchemasWSJFAssetStats']] = UNSET
    binary_data: Union[Unset, list['VirincoWATSSchemasWSJFBinaryData']] = UNSET
    additional_data: Union[Unset, list['VirincoWATSSchemasWSJFAdditionalData']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_sub_unit import VirincoWATSSchemasWSJFSubUnit
        from ..models.virinco_wats_schemas_wsjf_binary_data import VirincoWATSSchemasWSJFBinaryData
        from ..models.virinco_wats_schemas_wsjf_step import VirincoWATSSchemasWSJFStep
        from ..models.virinco_wats_schemas_wsjf_misc_info import VirincoWATSSchemasWSJFMiscInfo
        from ..models.virinco_wats_schemas_wsjf_additional_data import VirincoWATSSchemasWSJFAdditionalData
        from ..models.virinco_wats_schemas_wsjfuur import VirincoWATSSchemasWSJFUUR
        from ..models.virinco_wats_schemas_wsjfuut import VirincoWATSSchemasWSJFUUT
        from ..models.virinco_wats_schemas_wsjf_asset import VirincoWATSSchemasWSJFAsset
        from ..models.virinco_wats_schemas_wsjf_asset_stats import VirincoWATSSchemasWSJFAssetStats
        type_ = self.type_

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        pn = self.pn

        sn = self.sn

        rev = self.rev

        product_name = self.product_name

        process_code = self.process_code

        process_code_format = self.process_code_format

        process_name = self.process_name

        result = self.result

        machine_name = self.machine_name

        location = self.location

        purpose = self.purpose

        origin = self.origin

        start: Union[Unset, str] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.isoformat()

        start_utc: Union[Unset, str] = UNSET
        if not isinstance(self.start_utc, Unset):
            start_utc = self.start_utc.isoformat()

        root: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.root, Unset):
            root = self.root.to_dict()

        uut: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.uut, Unset):
            uut = self.uut.to_dict()

        uur: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.uur, Unset):
            uur = self.uur.to_dict()

        misc_infos: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.misc_infos, Unset):
            misc_infos = []
            for misc_infos_item_data in self.misc_infos:
                misc_infos_item = misc_infos_item_data.to_dict()
                misc_infos.append(misc_infos_item)



        sub_units: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sub_units, Unset):
            sub_units = []
            for sub_units_item_data in self.sub_units:
                sub_units_item = sub_units_item_data.to_dict()
                sub_units.append(sub_units_item)



        assets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.assets, Unset):
            assets = []
            for assets_item_data in self.assets:
                assets_item = assets_item_data.to_dict()
                assets.append(assets_item)



        asset_stats: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.asset_stats, Unset):
            asset_stats = []
            for asset_stats_item_data in self.asset_stats:
                asset_stats_item = asset_stats_item_data.to_dict()
                asset_stats.append(asset_stats_item)



        binary_data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.binary_data, Unset):
            binary_data = []
            for binary_data_item_data in self.binary_data:
                binary_data_item = binary_data_item_data.to_dict()
                binary_data.append(binary_data_item)



        additional_data: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.additional_data, Unset):
            additional_data = []
            for additional_data_item_data in self.additional_data:
                additional_data_item = additional_data_item_data.to_dict()
                additional_data.append(additional_data_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_ is not UNSET:
            field_dict["type"] = type_
        if id is not UNSET:
            field_dict["id"] = id
        if pn is not UNSET:
            field_dict["pn"] = pn
        if sn is not UNSET:
            field_dict["sn"] = sn
        if rev is not UNSET:
            field_dict["rev"] = rev
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if process_code is not UNSET:
            field_dict["processCode"] = process_code
        if process_code_format is not UNSET:
            field_dict["processCodeFormat"] = process_code_format
        if process_name is not UNSET:
            field_dict["processName"] = process_name
        if result is not UNSET:
            field_dict["result"] = result
        if machine_name is not UNSET:
            field_dict["machineName"] = machine_name
        if location is not UNSET:
            field_dict["location"] = location
        if purpose is not UNSET:
            field_dict["purpose"] = purpose
        if origin is not UNSET:
            field_dict["origin"] = origin
        if start is not UNSET:
            field_dict["start"] = start
        if start_utc is not UNSET:
            field_dict["startUTC"] = start_utc
        if root is not UNSET:
            field_dict["root"] = root
        if uut is not UNSET:
            field_dict["uut"] = uut
        if uur is not UNSET:
            field_dict["uur"] = uur
        if misc_infos is not UNSET:
            field_dict["miscInfos"] = misc_infos
        if sub_units is not UNSET:
            field_dict["subUnits"] = sub_units
        if assets is not UNSET:
            field_dict["assets"] = assets
        if asset_stats is not UNSET:
            field_dict["assetStats"] = asset_stats
        if binary_data is not UNSET:
            field_dict["binaryData"] = binary_data
        if additional_data is not UNSET:
            field_dict["additionalData"] = additional_data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_sub_unit import VirincoWATSSchemasWSJFSubUnit
        from ..models.virinco_wats_schemas_wsjf_binary_data import VirincoWATSSchemasWSJFBinaryData
        from ..models.virinco_wats_schemas_wsjf_step import VirincoWATSSchemasWSJFStep
        from ..models.virinco_wats_schemas_wsjf_misc_info import VirincoWATSSchemasWSJFMiscInfo
        from ..models.virinco_wats_schemas_wsjf_additional_data import VirincoWATSSchemasWSJFAdditionalData
        from ..models.virinco_wats_schemas_wsjfuur import VirincoWATSSchemasWSJFUUR
        from ..models.virinco_wats_schemas_wsjfuut import VirincoWATSSchemasWSJFUUT
        from ..models.virinco_wats_schemas_wsjf_asset import VirincoWATSSchemasWSJFAsset
        from ..models.virinco_wats_schemas_wsjf_asset_stats import VirincoWATSSchemasWSJFAssetStats
        d = dict(src_dict)
        type_ = d.pop("type", UNSET)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        pn = d.pop("pn", UNSET)

        sn = d.pop("sn", UNSET)

        rev = d.pop("rev", UNSET)

        product_name = d.pop("productName", UNSET)

        process_code = d.pop("processCode", UNSET)

        process_code_format = d.pop("processCodeFormat", UNSET)

        process_name = d.pop("processName", UNSET)

        result = d.pop("result", UNSET)

        machine_name = d.pop("machineName", UNSET)

        location = d.pop("location", UNSET)

        purpose = d.pop("purpose", UNSET)

        origin = d.pop("origin", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, datetime.datetime]
        if isinstance(_start,  Unset):
            start = UNSET
        else:
            start = isoparse(_start)




        _start_utc = d.pop("startUTC", UNSET)
        start_utc: Union[Unset, datetime.datetime]
        if isinstance(_start_utc,  Unset):
            start_utc = UNSET
        else:
            start_utc = isoparse(_start_utc)




        _root = d.pop("root", UNSET)
        root: Union[Unset, VirincoWATSSchemasWSJFStep]
        if isinstance(_root,  Unset):
            root = UNSET
        else:
            root = VirincoWATSSchemasWSJFStep.from_dict(_root)




        _uut = d.pop("uut", UNSET)
        uut: Union[Unset, VirincoWATSSchemasWSJFUUT]
        if isinstance(_uut,  Unset):
            uut = UNSET
        else:
            uut = VirincoWATSSchemasWSJFUUT.from_dict(_uut)




        _uur = d.pop("uur", UNSET)
        uur: Union[Unset, VirincoWATSSchemasWSJFUUR]
        if isinstance(_uur,  Unset):
            uur = UNSET
        else:
            uur = VirincoWATSSchemasWSJFUUR.from_dict(_uur)




        misc_infos = []
        _misc_infos = d.pop("miscInfos", UNSET)
        for misc_infos_item_data in (_misc_infos or []):
            misc_infos_item = VirincoWATSSchemasWSJFMiscInfo.from_dict(misc_infos_item_data)



            misc_infos.append(misc_infos_item)


        sub_units = []
        _sub_units = d.pop("subUnits", UNSET)
        for sub_units_item_data in (_sub_units or []):
            sub_units_item = VirincoWATSSchemasWSJFSubUnit.from_dict(sub_units_item_data)



            sub_units.append(sub_units_item)


        assets = []
        _assets = d.pop("assets", UNSET)
        for assets_item_data in (_assets or []):
            assets_item = VirincoWATSSchemasWSJFAsset.from_dict(assets_item_data)



            assets.append(assets_item)


        asset_stats = []
        _asset_stats = d.pop("assetStats", UNSET)
        for asset_stats_item_data in (_asset_stats or []):
            asset_stats_item = VirincoWATSSchemasWSJFAssetStats.from_dict(asset_stats_item_data)



            asset_stats.append(asset_stats_item)


        binary_data = []
        _binary_data = d.pop("binaryData", UNSET)
        for binary_data_item_data in (_binary_data or []):
            binary_data_item = VirincoWATSSchemasWSJFBinaryData.from_dict(binary_data_item_data)



            binary_data.append(binary_data_item)


        additional_data = []
        _additional_data = d.pop("additionalData", UNSET)
        for additional_data_item_data in (_additional_data or []):
            additional_data_item = VirincoWATSSchemasWSJFAdditionalData.from_dict(additional_data_item_data)



            additional_data.append(additional_data_item)


        virinco_wats_schemas_wsjf_report = cls(
            type_=type_,
            id=id,
            pn=pn,
            sn=sn,
            rev=rev,
            product_name=product_name,
            process_code=process_code,
            process_code_format=process_code_format,
            process_name=process_name,
            result=result,
            machine_name=machine_name,
            location=location,
            purpose=purpose,
            origin=origin,
            start=start,
            start_utc=start_utc,
            root=root,
            uut=uut,
            uur=uur,
            misc_infos=misc_infos,
            sub_units=sub_units,
            assets=assets,
            asset_stats=asset_stats,
            binary_data=binary_data,
            additional_data=additional_data,
        )


        virinco_wats_schemas_wsjf_report.additional_properties = d
        return virinco_wats_schemas_wsjf_report

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
