from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_referenced_by_uur import VirincoWATSSchemasWSJFReferencedByUUR





T = TypeVar("T", bound="VirincoWATSSchemasWSJFUUT")



@_attrs_define
class VirincoWATSSchemasWSJFUUT:
    """ 
        Attributes:
            exec_time (Union[Unset, float]): Execution time of the report.
            exec_time_format (Union[Unset, str]): Numeric format of execution time.
            test_socket_index (Union[Unset, int]): Index of socket used in test.
            test_socket_index_format (Union[Unset, str]): Numeric format of test socket index.
            batch_sn (Union[Unset, str]): Serial number of batch the report belongs to.
            comment (Union[Unset, str]): Comment of the report.
            error_code (Union[Unset, int]): Error code of the report.
            error_code_format (Union[Unset, str]): Numeric format of error code.
            error_message (Union[Unset, str]): Error message of the report.
            fixture_id (Union[Unset, str]): Id of fixture used in report.
            user (Union[Unset, str]): Name of test operator.
            batch_fail_count (Union[Unset, int]): Batch fail count.
            batch_fail_count_format (Union[Unset, str]): Numeric format of batch fail count.
            batch_loop_index (Union[Unset, int]): Batch loop index.
            batch_loop_index_format (Union[Unset, str]): Numeric format of batch loop index.
            step_id_caused_uut_failure (Union[Unset, int]): Id of step that caused uut failure.
            ref_uu_rs (Union[Unset, list['VirincoWATSSchemasWSJFReferencedByUUR']]): Repair reports that reference this test
                report.
     """

    exec_time: Union[Unset, float] = UNSET
    exec_time_format: Union[Unset, str] = UNSET
    test_socket_index: Union[Unset, int] = UNSET
    test_socket_index_format: Union[Unset, str] = UNSET
    batch_sn: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    error_code: Union[Unset, int] = UNSET
    error_code_format: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    fixture_id: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    batch_fail_count: Union[Unset, int] = UNSET
    batch_fail_count_format: Union[Unset, str] = UNSET
    batch_loop_index: Union[Unset, int] = UNSET
    batch_loop_index_format: Union[Unset, str] = UNSET
    step_id_caused_uut_failure: Union[Unset, int] = UNSET
    ref_uu_rs: Union[Unset, list['VirincoWATSSchemasWSJFReferencedByUUR']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_referenced_by_uur import VirincoWATSSchemasWSJFReferencedByUUR
        exec_time = self.exec_time

        exec_time_format = self.exec_time_format

        test_socket_index = self.test_socket_index

        test_socket_index_format = self.test_socket_index_format

        batch_sn = self.batch_sn

        comment = self.comment

        error_code = self.error_code

        error_code_format = self.error_code_format

        error_message = self.error_message

        fixture_id = self.fixture_id

        user = self.user

        batch_fail_count = self.batch_fail_count

        batch_fail_count_format = self.batch_fail_count_format

        batch_loop_index = self.batch_loop_index

        batch_loop_index_format = self.batch_loop_index_format

        step_id_caused_uut_failure = self.step_id_caused_uut_failure

        ref_uu_rs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.ref_uu_rs, Unset):
            ref_uu_rs = []
            for ref_uu_rs_item_data in self.ref_uu_rs:
                ref_uu_rs_item = ref_uu_rs_item_data.to_dict()
                ref_uu_rs.append(ref_uu_rs_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if exec_time is not UNSET:
            field_dict["execTime"] = exec_time
        if exec_time_format is not UNSET:
            field_dict["execTimeFormat"] = exec_time_format
        if test_socket_index is not UNSET:
            field_dict["testSocketIndex"] = test_socket_index
        if test_socket_index_format is not UNSET:
            field_dict["testSocketIndexFormat"] = test_socket_index_format
        if batch_sn is not UNSET:
            field_dict["batchSN"] = batch_sn
        if comment is not UNSET:
            field_dict["comment"] = comment
        if error_code is not UNSET:
            field_dict["errorCode"] = error_code
        if error_code_format is not UNSET:
            field_dict["errorCodeFormat"] = error_code_format
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if fixture_id is not UNSET:
            field_dict["fixtureId"] = fixture_id
        if user is not UNSET:
            field_dict["user"] = user
        if batch_fail_count is not UNSET:
            field_dict["batchFailCount"] = batch_fail_count
        if batch_fail_count_format is not UNSET:
            field_dict["batchFailCountFormat"] = batch_fail_count_format
        if batch_loop_index is not UNSET:
            field_dict["batchLoopIndex"] = batch_loop_index
        if batch_loop_index_format is not UNSET:
            field_dict["batchLoopIndexFormat"] = batch_loop_index_format
        if step_id_caused_uut_failure is not UNSET:
            field_dict["stepIdCausedUUTFailure"] = step_id_caused_uut_failure
        if ref_uu_rs is not UNSET:
            field_dict["refUURs"] = ref_uu_rs

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_referenced_by_uur import VirincoWATSSchemasWSJFReferencedByUUR
        d = dict(src_dict)
        exec_time = d.pop("execTime", UNSET)

        exec_time_format = d.pop("execTimeFormat", UNSET)

        test_socket_index = d.pop("testSocketIndex", UNSET)

        test_socket_index_format = d.pop("testSocketIndexFormat", UNSET)

        batch_sn = d.pop("batchSN", UNSET)

        comment = d.pop("comment", UNSET)

        error_code = d.pop("errorCode", UNSET)

        error_code_format = d.pop("errorCodeFormat", UNSET)

        error_message = d.pop("errorMessage", UNSET)

        fixture_id = d.pop("fixtureId", UNSET)

        user = d.pop("user", UNSET)

        batch_fail_count = d.pop("batchFailCount", UNSET)

        batch_fail_count_format = d.pop("batchFailCountFormat", UNSET)

        batch_loop_index = d.pop("batchLoopIndex", UNSET)

        batch_loop_index_format = d.pop("batchLoopIndexFormat", UNSET)

        step_id_caused_uut_failure = d.pop("stepIdCausedUUTFailure", UNSET)

        ref_uu_rs = []
        _ref_uu_rs = d.pop("refUURs", UNSET)
        for ref_uu_rs_item_data in (_ref_uu_rs or []):
            ref_uu_rs_item = VirincoWATSSchemasWSJFReferencedByUUR.from_dict(ref_uu_rs_item_data)



            ref_uu_rs.append(ref_uu_rs_item)


        virinco_wats_schemas_wsjfuut = cls(
            exec_time=exec_time,
            exec_time_format=exec_time_format,
            test_socket_index=test_socket_index,
            test_socket_index_format=test_socket_index_format,
            batch_sn=batch_sn,
            comment=comment,
            error_code=error_code,
            error_code_format=error_code_format,
            error_message=error_message,
            fixture_id=fixture_id,
            user=user,
            batch_fail_count=batch_fail_count,
            batch_fail_count_format=batch_fail_count_format,
            batch_loop_index=batch_loop_index,
            batch_loop_index_format=batch_loop_index_format,
            step_id_caused_uut_failure=step_id_caused_uut_failure,
            ref_uu_rs=ref_uu_rs,
        )


        virinco_wats_schemas_wsjfuut.additional_properties = d
        return virinco_wats_schemas_wsjfuut

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
