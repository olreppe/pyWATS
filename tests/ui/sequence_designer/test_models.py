"""Tests for the Sequence Designer data model.

Tests the StepNode tree, SequenceModel operations, and serialization
without requiring a running Qt application.
"""
import json
import pytest
from unittest.mock import MagicMock

from PySide6.QtWidgets import QApplication

from pywats_ui.apps.production_manager.models import (
    STEP_META,
    SequenceModel,
    StepNode,
    StepStatus,
    StepType,
)


# Ensure a QApplication exists for signal tests
@pytest.fixture(scope="session", autouse=True)
def qapp():
    """Create a QApplication instance for the test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


# =============================================================================
# StepNode Tests
# =============================================================================


class TestStepNode:
    """Tests for individual StepNode behaviour."""

    def test_create_step_defaults(self) -> None:
        node = StepNode(StepType.NUMERIC_LIMIT)
        assert node.step_type == StepType.NUMERIC_LIMIT
        assert node.name == "Numeric Limit"
        assert node.parent is None
        assert node.children == []
        assert node.status == StepStatus.NONE
        assert "units" in node.properties
        assert "comp_operator" in node.properties

    def test_create_step_custom_name(self) -> None:
        node = StepNode(StepType.PASS_FAIL, name="Solder Check")
        assert node.name == "Solder Check"

    def test_add_child(self) -> None:
        parent = StepNode(StepType.SEQUENCE, name="Root")
        child = StepNode(StepType.NUMERIC_LIMIT)
        parent.add_child(child)
        assert len(parent.children) == 1
        assert child.parent is parent
        assert parent.children[0] is child

    def test_add_child_at_index(self) -> None:
        parent = StepNode(StepType.SEQUENCE, name="Root")
        a = StepNode(StepType.PASS_FAIL, name="A")
        b = StepNode(StepType.PASS_FAIL, name="B")
        c = StepNode(StepType.PASS_FAIL, name="C")
        parent.add_child(a)
        parent.add_child(c)
        parent.add_child(b, index=1)
        assert [ch.name for ch in parent.children] == ["A", "B", "C"]

    def test_remove_child(self) -> None:
        parent = StepNode(StepType.SEQUENCE, name="Root")
        child = StepNode(StepType.PASS_FAIL)
        parent.add_child(child)
        parent.remove_child(child)
        assert len(parent.children) == 0
        assert child.parent is None

    def test_index_in_parent(self) -> None:
        parent = StepNode(StepType.SEQUENCE)
        a = StepNode(StepType.PASS_FAIL, name="A")
        b = StepNode(StepType.PASS_FAIL, name="B")
        parent.add_child(a)
        parent.add_child(b)
        assert a.index_in_parent() == 0
        assert b.index_in_parent() == 1

    def test_depth(self) -> None:
        root = StepNode(StepType.SEQUENCE)
        child = StepNode(StepType.SEQUENCE)
        grandchild = StepNode(StepType.PASS_FAIL)
        root.add_child(child)
        child.add_child(grandchild)
        assert root.depth == 0
        assert child.depth == 1
        assert grandchild.depth == 2

    def test_is_container(self) -> None:
        seq = StepNode(StepType.SEQUENCE)
        nl = StepNode(StepType.NUMERIC_LIMIT)
        assert seq.is_container is True
        assert nl.is_container is False

    def test_serialization_round_trip(self) -> None:
        root = StepNode(StepType.SEQUENCE, name="Test Seq")
        root.add_child(StepNode(StepType.NUMERIC_LIMIT, name="Measure Voltage"))
        root.add_child(StepNode(StepType.PASS_FAIL, name="Visual Check"))

        data = root.to_dict()
        restored = StepNode.from_dict(data)

        assert restored.name == "Test Seq"
        assert restored.step_type == StepType.SEQUENCE
        assert len(restored.children) == 2
        assert restored.children[0].name == "Measure Voltage"
        assert restored.children[1].name == "Visual Check"

    def test_nested_serialization(self) -> None:
        root = StepNode(StepType.SEQUENCE, name="Root")
        sub = StepNode(StepType.SEQUENCE, name="Sub")
        sub.add_child(StepNode(StepType.WAIT, name="Wait 5s"))
        root.add_child(sub)

        data = root.to_dict()
        restored = StepNode.from_dict(data)

        assert len(restored.children) == 1
        assert restored.children[0].name == "Sub"
        assert len(restored.children[0].children) == 1
        assert restored.children[0].children[0].name == "Wait 5s"

    def test_all_step_types_have_meta(self) -> None:
        for st in StepType:
            assert st in STEP_META, f"Missing STEP_META for {st}"
            meta = STEP_META[st]
            assert "label" in meta
            assert "color" in meta
            assert "is_container" in meta


# =============================================================================
# SequenceModel Tests
# =============================================================================


class TestSequenceModel:
    """Tests for the SequenceModel observable wrapper."""

    def test_new_model_has_root(self) -> None:
        model = SequenceModel(name="My Seq")
        assert model.root.step_type == StepType.SEQUENCE
        assert model.name == "My Seq"
        assert model.is_dirty is False

    def test_add_step_to_root(self) -> None:
        model = SequenceModel()
        node = model.add_step(StepType.NUMERIC_LIMIT)
        assert len(model.root.children) == 1
        assert model.root.children[0] is node
        assert model.is_dirty is True

    def test_add_step_to_container(self) -> None:
        model = SequenceModel()
        sub = model.add_step(StepType.SEQUENCE, name="Sub Seq")
        child = model.add_step(StepType.PASS_FAIL, parent_id=sub.id)
        assert len(sub.children) == 1
        assert sub.children[0] is child

    def test_remove_step(self) -> None:
        model = SequenceModel()
        node = model.add_step(StepType.PASS_FAIL)
        assert model.remove_step(node.id) is True
        assert len(model.root.children) == 0

    def test_cannot_remove_root(self) -> None:
        model = SequenceModel()
        assert model.remove_step(model.root.id) is False

    def test_move_step(self) -> None:
        model = SequenceModel()
        a = model.add_step(StepType.PASS_FAIL, name="A")
        sub = model.add_step(StepType.SEQUENCE, name="Sub")
        assert model.move_step(a.id, sub.id) is True
        assert len(model.root.children) == 1  # only sub remains at root
        assert len(sub.children) == 1
        assert sub.children[0] is a

    def test_cannot_move_into_own_subtree(self) -> None:
        model = SequenceModel()
        parent = model.add_step(StepType.SEQUENCE, name="Parent")
        child = model.add_step(StepType.SEQUENCE, parent_id=parent.id, name="Child")
        assert model.move_step(parent.id, child.id) is False

    def test_rename_step(self) -> None:
        model = SequenceModel()
        node = model.add_step(StepType.PASS_FAIL, name="Old")
        model.rename_step(node.id, "New")
        assert node.name == "New"

    def test_update_properties(self) -> None:
        model = SequenceModel()
        node = model.add_step(StepType.NUMERIC_LIMIT)
        model.update_step_properties(node.id, units="V", low_limit=1.0, high_limit=5.0)
        assert node.properties["units"] == "V"
        assert node.properties["low_limit"] == 1.0
        assert node.properties["high_limit"] == 5.0

    def test_find_node(self) -> None:
        model = SequenceModel()
        a = model.add_step(StepType.PASS_FAIL, name="A")
        sub = model.add_step(StepType.SEQUENCE, name="Sub")
        b = model.add_step(StepType.NUMERIC_LIMIT, parent_id=sub.id, name="B")

        assert model.find_node(a.id) is a
        assert model.find_node(b.id) is b
        assert model.find_node("nonexistent") is None

    def test_selection(self) -> None:
        model = SequenceModel()
        node = model.add_step(StepType.PASS_FAIL)
        model.select(node.id)
        assert model.selected_id == node.id
        assert model.selected_node() is node

        model.deselect()
        assert model.selected_id == ""
        assert model.selected_node() is None

    def test_dirty_tracking(self) -> None:
        model = SequenceModel()
        assert model.is_dirty is False
        model.add_step(StepType.PASS_FAIL)
        assert model.is_dirty is True
        model.mark_clean()
        assert model.is_dirty is False

    def test_signals_emitted(self) -> None:
        model = SequenceModel()
        structure_spy = MagicMock()
        dirty_spy = MagicMock()
        model.structure_changed.connect(structure_spy)
        model.dirty_changed.connect(dirty_spy)

        model.add_step(StepType.PASS_FAIL)
        assert structure_spy.call_count == 1
        assert dirty_spy.call_count == 1  # False → True

    def test_full_serialization_round_trip(self) -> None:
        model = SequenceModel(name="Round Trip Test")
        model.definition_id = "def-123"
        model.add_step(StepType.NUMERIC_LIMIT, name="Voltage")
        sub = model.add_step(StepType.SEQUENCE, name="Sub")
        model.add_step(StepType.PASS_FAIL, parent_id=sub.id, name="Check")

        data = model.to_dict()
        json_str = json.dumps(data)
        restored_data = json.loads(json_str)
        restored = SequenceModel.from_dict(restored_data)

        assert restored.name == "Round Trip Test"
        assert restored.definition_id == "def-123"
        assert len(restored.root.children) == 2
        assert restored.root.children[0].name == "Voltage"
        assert restored.root.children[1].name == "Sub"
        assert len(restored.root.children[1].children) == 1
        assert restored.root.children[1].children[0].name == "Check"
        assert restored.is_dirty is False

    def test_clear(self) -> None:
        model = SequenceModel(name="Initial")
        model.add_step(StepType.PASS_FAIL)
        model.clear()
        assert model.name == "New Sequence"
        assert len(model.root.children) == 0
        assert model.is_dirty is False
        assert model.definition_id is None

    def test_set_name(self) -> None:
        model = SequenceModel(name="A")
        model.name = "B"
        assert model.name == "B"
        assert model.is_dirty is True
