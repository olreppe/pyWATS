from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmFilter")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmFilter:
    """ 
        Attributes:
            filter_id (Union[Unset, int]):
            filter_name (Union[Unset, str]):
            filter_order (Union[Unset, int]):
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            sequence_name (Union[Unset, str]):
            sequence_version (Union[Unset, str]):
            batch_number (Union[Unset, str]):
            station_name (Union[Unset, str]):
            socket (Union[Unset, str]):
            top_count (Union[Unset, str]):
            max_count (Union[Unset, str]):
            min_count (Union[Unset, str]):
            operation_type (Union[Unset, str]):
            repair_type (Union[Unset, str]):
            status (Union[Unset, str]):
            grouping (Union[Unset, str]):
            yield_ (Union[Unset, str]):
            run (Union[Unset, str]):
            phase (Union[Unset, str]):
            state (Union[Unset, str]):
            misc (Union[Unset, str]):
            date_from (Union[Unset, str]):
            date_to (Union[Unset, str]):
            repaired_units (Union[Unset, str]):
            date_from_ticks (Union[Unset, int]):
            date_to_ticks (Union[Unset, int]):
            product_group (Union[Unset, str]):
            site (Union[Unset, str]):
            date_time_type (Union[Unset, str]):
            is_local_date_time (Union[Unset, bool]):
            use_time_range (Union[Unset, bool]):
            period_count (Union[Unset, str]):
            include_current_period (Union[Unset, bool]):
            step_failed_caused_uut_failed (Union[Unset, bool]):
            appraiser_type (Union[Unset, str]):
            appraiser_value (Union[Unset, str]):
            misc_desc (Union[Unset, str]):
            dimensions (Union[Unset, str]):
            unit_type (Union[Unset, str]):
            failure_type (Union[Unset, str]):
            test_operator (Union[Unset, str]):
            component_reference (Union[Unset, str]):
            component_number (Union[Unset, str]):
            component_revision (Union[Unset, str]):
            vendor (Union[Unset, str]):
            function_block (Union[Unset, str]):
            repair_code (Union[Unset, str]):
     """

    filter_id: Union[Unset, int] = UNSET
    filter_name: Union[Unset, str] = UNSET
    filter_order: Union[Unset, int] = UNSET
    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    sequence_name: Union[Unset, str] = UNSET
    sequence_version: Union[Unset, str] = UNSET
    batch_number: Union[Unset, str] = UNSET
    station_name: Union[Unset, str] = UNSET
    socket: Union[Unset, str] = UNSET
    top_count: Union[Unset, str] = UNSET
    max_count: Union[Unset, str] = UNSET
    min_count: Union[Unset, str] = UNSET
    operation_type: Union[Unset, str] = UNSET
    repair_type: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    grouping: Union[Unset, str] = UNSET
    yield_: Union[Unset, str] = UNSET
    run: Union[Unset, str] = UNSET
    phase: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    misc: Union[Unset, str] = UNSET
    date_from: Union[Unset, str] = UNSET
    date_to: Union[Unset, str] = UNSET
    repaired_units: Union[Unset, str] = UNSET
    date_from_ticks: Union[Unset, int] = UNSET
    date_to_ticks: Union[Unset, int] = UNSET
    product_group: Union[Unset, str] = UNSET
    site: Union[Unset, str] = UNSET
    date_time_type: Union[Unset, str] = UNSET
    is_local_date_time: Union[Unset, bool] = UNSET
    use_time_range: Union[Unset, bool] = UNSET
    period_count: Union[Unset, str] = UNSET
    include_current_period: Union[Unset, bool] = UNSET
    step_failed_caused_uut_failed: Union[Unset, bool] = UNSET
    appraiser_type: Union[Unset, str] = UNSET
    appraiser_value: Union[Unset, str] = UNSET
    misc_desc: Union[Unset, str] = UNSET
    dimensions: Union[Unset, str] = UNSET
    unit_type: Union[Unset, str] = UNSET
    failure_type: Union[Unset, str] = UNSET
    test_operator: Union[Unset, str] = UNSET
    component_reference: Union[Unset, str] = UNSET
    component_number: Union[Unset, str] = UNSET
    component_revision: Union[Unset, str] = UNSET
    vendor: Union[Unset, str] = UNSET
    function_block: Union[Unset, str] = UNSET
    repair_code: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        filter_id = self.filter_id

        filter_name = self.filter_name

        filter_order = self.filter_order

        serial_number = self.serial_number

        part_number = self.part_number

        revision = self.revision

        sequence_name = self.sequence_name

        sequence_version = self.sequence_version

        batch_number = self.batch_number

        station_name = self.station_name

        socket = self.socket

        top_count = self.top_count

        max_count = self.max_count

        min_count = self.min_count

        operation_type = self.operation_type

        repair_type = self.repair_type

        status = self.status

        grouping = self.grouping

        yield_ = self.yield_

        run = self.run

        phase = self.phase

        state = self.state

        misc = self.misc

        date_from = self.date_from

        date_to = self.date_to

        repaired_units = self.repaired_units

        date_from_ticks = self.date_from_ticks

        date_to_ticks = self.date_to_ticks

        product_group = self.product_group

        site = self.site

        date_time_type = self.date_time_type

        is_local_date_time = self.is_local_date_time

        use_time_range = self.use_time_range

        period_count = self.period_count

        include_current_period = self.include_current_period

        step_failed_caused_uut_failed = self.step_failed_caused_uut_failed

        appraiser_type = self.appraiser_type

        appraiser_value = self.appraiser_value

        misc_desc = self.misc_desc

        dimensions = self.dimensions

        unit_type = self.unit_type

        failure_type = self.failure_type

        test_operator = self.test_operator

        component_reference = self.component_reference

        component_number = self.component_number

        component_revision = self.component_revision

        vendor = self.vendor

        function_block = self.function_block

        repair_code = self.repair_code


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if filter_id is not UNSET:
            field_dict["FilterId"] = filter_id
        if filter_name is not UNSET:
            field_dict["FilterName"] = filter_name
        if filter_order is not UNSET:
            field_dict["FilterOrder"] = filter_order
        if serial_number is not UNSET:
            field_dict["SerialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["PartNumber"] = part_number
        if revision is not UNSET:
            field_dict["Revision"] = revision
        if sequence_name is not UNSET:
            field_dict["SequenceName"] = sequence_name
        if sequence_version is not UNSET:
            field_dict["SequenceVersion"] = sequence_version
        if batch_number is not UNSET:
            field_dict["BatchNumber"] = batch_number
        if station_name is not UNSET:
            field_dict["StationName"] = station_name
        if socket is not UNSET:
            field_dict["Socket"] = socket
        if top_count is not UNSET:
            field_dict["TopCount"] = top_count
        if max_count is not UNSET:
            field_dict["MaxCount"] = max_count
        if min_count is not UNSET:
            field_dict["MinCount"] = min_count
        if operation_type is not UNSET:
            field_dict["OperationType"] = operation_type
        if repair_type is not UNSET:
            field_dict["RepairType"] = repair_type
        if status is not UNSET:
            field_dict["Status"] = status
        if grouping is not UNSET:
            field_dict["Grouping"] = grouping
        if yield_ is not UNSET:
            field_dict["Yield"] = yield_
        if run is not UNSET:
            field_dict["Run"] = run
        if phase is not UNSET:
            field_dict["Phase"] = phase
        if state is not UNSET:
            field_dict["State"] = state
        if misc is not UNSET:
            field_dict["Misc"] = misc
        if date_from is not UNSET:
            field_dict["DateFrom"] = date_from
        if date_to is not UNSET:
            field_dict["DateTo"] = date_to
        if repaired_units is not UNSET:
            field_dict["RepairedUnits"] = repaired_units
        if date_from_ticks is not UNSET:
            field_dict["DateFromTicks"] = date_from_ticks
        if date_to_ticks is not UNSET:
            field_dict["DateToTicks"] = date_to_ticks
        if product_group is not UNSET:
            field_dict["ProductGroup"] = product_group
        if site is not UNSET:
            field_dict["Site"] = site
        if date_time_type is not UNSET:
            field_dict["DateTimeType"] = date_time_type
        if is_local_date_time is not UNSET:
            field_dict["IsLocalDateTime"] = is_local_date_time
        if use_time_range is not UNSET:
            field_dict["UseTimeRange"] = use_time_range
        if period_count is not UNSET:
            field_dict["PeriodCount"] = period_count
        if include_current_period is not UNSET:
            field_dict["IncludeCurrentPeriod"] = include_current_period
        if step_failed_caused_uut_failed is not UNSET:
            field_dict["StepFailedCausedUUTFailed"] = step_failed_caused_uut_failed
        if appraiser_type is not UNSET:
            field_dict["AppraiserType"] = appraiser_type
        if appraiser_value is not UNSET:
            field_dict["AppraiserValue"] = appraiser_value
        if misc_desc is not UNSET:
            field_dict["MiscDesc"] = misc_desc
        if dimensions is not UNSET:
            field_dict["Dimensions"] = dimensions
        if unit_type is not UNSET:
            field_dict["UnitType"] = unit_type
        if failure_type is not UNSET:
            field_dict["FailureType"] = failure_type
        if test_operator is not UNSET:
            field_dict["TestOperator"] = test_operator
        if component_reference is not UNSET:
            field_dict["ComponentReference"] = component_reference
        if component_number is not UNSET:
            field_dict["ComponentNumber"] = component_number
        if component_revision is not UNSET:
            field_dict["ComponentRevision"] = component_revision
        if vendor is not UNSET:
            field_dict["Vendor"] = vendor
        if function_block is not UNSET:
            field_dict["FunctionBlock"] = function_block
        if repair_code is not UNSET:
            field_dict["RepairCode"] = repair_code

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filter_id = d.pop("FilterId", UNSET)

        filter_name = d.pop("FilterName", UNSET)

        filter_order = d.pop("FilterOrder", UNSET)

        serial_number = d.pop("SerialNumber", UNSET)

        part_number = d.pop("PartNumber", UNSET)

        revision = d.pop("Revision", UNSET)

        sequence_name = d.pop("SequenceName", UNSET)

        sequence_version = d.pop("SequenceVersion", UNSET)

        batch_number = d.pop("BatchNumber", UNSET)

        station_name = d.pop("StationName", UNSET)

        socket = d.pop("Socket", UNSET)

        top_count = d.pop("TopCount", UNSET)

        max_count = d.pop("MaxCount", UNSET)

        min_count = d.pop("MinCount", UNSET)

        operation_type = d.pop("OperationType", UNSET)

        repair_type = d.pop("RepairType", UNSET)

        status = d.pop("Status", UNSET)

        grouping = d.pop("Grouping", UNSET)

        yield_ = d.pop("Yield", UNSET)

        run = d.pop("Run", UNSET)

        phase = d.pop("Phase", UNSET)

        state = d.pop("State", UNSET)

        misc = d.pop("Misc", UNSET)

        date_from = d.pop("DateFrom", UNSET)

        date_to = d.pop("DateTo", UNSET)

        repaired_units = d.pop("RepairedUnits", UNSET)

        date_from_ticks = d.pop("DateFromTicks", UNSET)

        date_to_ticks = d.pop("DateToTicks", UNSET)

        product_group = d.pop("ProductGroup", UNSET)

        site = d.pop("Site", UNSET)

        date_time_type = d.pop("DateTimeType", UNSET)

        is_local_date_time = d.pop("IsLocalDateTime", UNSET)

        use_time_range = d.pop("UseTimeRange", UNSET)

        period_count = d.pop("PeriodCount", UNSET)

        include_current_period = d.pop("IncludeCurrentPeriod", UNSET)

        step_failed_caused_uut_failed = d.pop("StepFailedCausedUUTFailed", UNSET)

        appraiser_type = d.pop("AppraiserType", UNSET)

        appraiser_value = d.pop("AppraiserValue", UNSET)

        misc_desc = d.pop("MiscDesc", UNSET)

        dimensions = d.pop("Dimensions", UNSET)

        unit_type = d.pop("UnitType", UNSET)

        failure_type = d.pop("FailureType", UNSET)

        test_operator = d.pop("TestOperator", UNSET)

        component_reference = d.pop("ComponentReference", UNSET)

        component_number = d.pop("ComponentNumber", UNSET)

        component_revision = d.pop("ComponentRevision", UNSET)

        vendor = d.pop("Vendor", UNSET)

        function_block = d.pop("FunctionBlock", UNSET)

        repair_code = d.pop("RepairCode", UNSET)

        virinco_wats_web_dashboard_models_tdm_filter = cls(
            filter_id=filter_id,
            filter_name=filter_name,
            filter_order=filter_order,
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            sequence_name=sequence_name,
            sequence_version=sequence_version,
            batch_number=batch_number,
            station_name=station_name,
            socket=socket,
            top_count=top_count,
            max_count=max_count,
            min_count=min_count,
            operation_type=operation_type,
            repair_type=repair_type,
            status=status,
            grouping=grouping,
            yield_=yield_,
            run=run,
            phase=phase,
            state=state,
            misc=misc,
            date_from=date_from,
            date_to=date_to,
            repaired_units=repaired_units,
            date_from_ticks=date_from_ticks,
            date_to_ticks=date_to_ticks,
            product_group=product_group,
            site=site,
            date_time_type=date_time_type,
            is_local_date_time=is_local_date_time,
            use_time_range=use_time_range,
            period_count=period_count,
            include_current_period=include_current_period,
            step_failed_caused_uut_failed=step_failed_caused_uut_failed,
            appraiser_type=appraiser_type,
            appraiser_value=appraiser_value,
            misc_desc=misc_desc,
            dimensions=dimensions,
            unit_type=unit_type,
            failure_type=failure_type,
            test_operator=test_operator,
            component_reference=component_reference,
            component_number=component_number,
            component_revision=component_revision,
            vendor=vendor,
            function_block=function_block,
            repair_code=repair_code,
        )


        virinco_wats_web_dashboard_models_tdm_filter.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_filter

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
