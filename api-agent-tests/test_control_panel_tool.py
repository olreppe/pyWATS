"""
Tests for Control Panel Manager tool.

Tests cover:
- Input validation (domain, operation, entity type)
- Domain routing (asset, product, production, software, process)
- Operation handling (list, get, create, update, delete, domain-specific)
- Error handling and edge cases
- Result formatting
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from datetime import datetime
from uuid import uuid4

from pywats_agent.tools.control_panel import (
    ControlPanelTool,
    ControlPanelInput,
    ControlPanelResult,
    ManagementDomain,
    OperationType,
    DOMAIN_ENTITIES,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def mock_api():
    """Create a mock pyWATS API."""
    api = MagicMock()
    
    # Setup asset service mocks
    api.asset.get_assets.return_value = []
    api.asset.get_asset.return_value = None
    api.asset.create_asset.return_value = None
    api.asset.delete_asset.return_value = False
    api.asset.set_asset_state.return_value = False
    api.asset.get_asset_types.return_value = []
    api.asset.get_asset_type.return_value = None
    
    # Setup product service mocks
    api.product.get_products.return_value = []
    api.product.get_product.return_value = None
    api.product.create_product.return_value = None
    api.product.get_revisions.return_value = []
    api.product.get_revision.return_value = None
    api.product.create_revision.return_value = None
    api.product.get_groups.return_value = []
    
    # Setup production service mocks
    api.production.get_unit.return_value = None
    api.production.create_units.return_value = []
    api.production.set_unit_phase.return_value = False
    api.production.get_unit_grade.return_value = None
    api.production.get_phases.return_value = []
    api.production.get_phase.return_value = None
    api.production.add_child_to_assembly.return_value = False
    api.production.remove_child_from_assembly.return_value = False
    api.production.verify_assembly.return_value = None
    
    # Setup software service mocks
    api.software.get_packages.return_value = []
    api.software.get_package.return_value = None
    api.software.get_package_by_name.return_value = None
    api.software.create_package.return_value = None
    api.software.delete_package.return_value = False
    api.software.delete_package_by_name.return_value = False
    api.software.submit_for_review.return_value = False
    api.software.release_package.return_value = False
    api.software.revoke_package.return_value = False
    api.software.get_virtual_folders.return_value = []
    
    # Setup process service mocks
    api.process.get_test_operations.return_value = []
    api.process.get_repair_operations.return_value = []
    api.process.get_wip_operations.return_value = []
    api.process.get_processes.return_value = []
    api.process.get_test_operation.return_value = None
    api.process.get_repair_operation.return_value = None
    api.process.get_wip_operation.return_value = None
    api.process.get_process.return_value = None
    
    return api


@pytest.fixture
def tool(mock_api):
    """Create a ControlPanelTool instance."""
    return ControlPanelTool(mock_api)


# =============================================================================
# Model Tests
# =============================================================================

class TestManagementDomain:
    """Tests for ManagementDomain enum."""
    
    def test_all_domains_defined(self):
        """All expected domains should be defined."""
        expected = {"asset", "product", "production", "software", "process"}
        actual = {d.value for d in ManagementDomain}
        assert actual == expected
    
    def test_domain_string_conversion(self):
        """Domain should convert to string properly."""
        assert ManagementDomain.ASSET.value == "asset"
        assert str(ManagementDomain.ASSET) == "ManagementDomain.ASSET"


class TestOperationType:
    """Tests for OperationType enum."""
    
    def test_read_operations(self):
        """Read operations should be defined."""
        assert OperationType.LIST.value == "list"
        assert OperationType.GET.value == "get"
        assert OperationType.SEARCH.value == "search"
    
    def test_write_operations(self):
        """Write operations should be defined."""
        assert OperationType.CREATE.value == "create"
        assert OperationType.UPDATE.value == "update"
        assert OperationType.DELETE.value == "delete"
    
    def test_domain_specific_operations(self):
        """Domain-specific operations should be defined."""
        domain_ops = {OperationType.SET_STATE, OperationType.SET_PHASE,
                      OperationType.ADD_CHILD, OperationType.REMOVE_CHILD,
                      OperationType.VERIFY, OperationType.RELEASE, OperationType.REVOKE}
        assert all(op.value for op in domain_ops)


class TestControlPanelInput:
    """Tests for ControlPanelInput model."""
    
    def test_minimal_input(self):
        """Should create input with just domain and operation."""
        inp = ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST
        )
        assert inp.domain == ManagementDomain.ASSET
        assert inp.operation == OperationType.LIST
        assert inp.entity_type is None
        assert inp.identifier is None
        assert inp.parameters is None
        assert inp.confirm_destructive is False
    
    def test_full_input(self):
        """Should create input with all fields."""
        inp = ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.DELETE,
            entity_type="package",
            identifier="some-uuid",
            parameters={"force": True},
            confirm_destructive=True
        )
        assert inp.domain == ManagementDomain.SOFTWARE
        assert inp.confirm_destructive is True


class TestControlPanelResult:
    """Tests for ControlPanelResult model."""
    
    def test_success_result(self):
        """Should create success result."""
        result = ControlPanelResult(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST,
            entity_type="asset",
            success=True,
            message="Found 5 assets",
            items=[{"name": "test"}],
            count=5
        )
        assert result.success is True
        assert result.count == 5
    
    def test_failure_result(self):
        """Should create failure result."""
        result = ControlPanelResult(
            domain=ManagementDomain.PRODUCT,
            operation=OperationType.CREATE,
            entity_type="product",
            success=False,
            message="Missing required parameter"
        )
        assert result.success is False


class TestDomainEntities:
    """Tests for DOMAIN_ENTITIES mapping."""
    
    def test_all_domains_have_entities(self):
        """All domains should have entity types defined."""
        for domain in ManagementDomain:
            assert domain in DOMAIN_ENTITIES
            assert len(DOMAIN_ENTITIES[domain]) > 0
    
    def test_asset_entities(self):
        """Asset domain should have correct entities."""
        assert "asset" in DOMAIN_ENTITIES[ManagementDomain.ASSET]
        assert "asset_type" in DOMAIN_ENTITIES[ManagementDomain.ASSET]
    
    def test_product_entities(self):
        """Product domain should have correct entities."""
        assert "product" in DOMAIN_ENTITIES[ManagementDomain.PRODUCT]
        assert "revision" in DOMAIN_ENTITIES[ManagementDomain.PRODUCT]
    
    def test_production_entities(self):
        """Production domain should have correct entities."""
        assert "unit" in DOMAIN_ENTITIES[ManagementDomain.PRODUCTION]
        assert "phase" in DOMAIN_ENTITIES[ManagementDomain.PRODUCTION]


# =============================================================================
# Tool Definition Tests
# =============================================================================

class TestToolDefinition:
    """Tests for tool definition."""
    
    def test_tool_name(self):
        """Tool should have correct name."""
        assert ControlPanelTool.name == "control_panel"
    
    def test_tool_description(self):
        """Tool should have description."""
        assert len(ControlPanelTool.description) > 100
    
    def test_get_definition(self):
        """Should return valid tool definition."""
        definition = ControlPanelTool.get_definition()
        assert "name" in definition
        assert definition["name"] == "control_panel"
        assert "parameters" in definition


# =============================================================================
# Asset Domain Tests
# =============================================================================

class TestAssetOperations:
    """Tests for asset domain operations."""
    
    def test_list_assets_empty(self, tool, mock_api):
        """Should handle empty asset list."""
        mock_api.asset.get_assets.return_value = []
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST
        ))
        
        assert result.success is True
        assert "0 assets" in result.summary
    
    def test_list_assets_with_data(self, tool, mock_api):
        """Should list assets with data."""
        mock_asset = MagicMock()
        mock_asset.asset_id = uuid4()
        mock_asset.serial_number = "ASSET001"
        mock_asset.asset_name = "Test Asset"
        mock_asset.type_id = uuid4()
        mock_asset.state = "OK"
        mock_asset.location = "Lab A"
        mock_asset.description = "Test"
        mock_api.asset.get_assets.return_value = [mock_asset]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST
        ))
        
        assert result.success is True
        assert "1 assets" in result.summary
    
    def test_get_asset_not_found(self, tool, mock_api):
        """Should handle asset not found."""
        mock_api.asset.get_asset.return_value = None
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.GET,
            identifier="NOTFOUND"
        ))
        
        assert result.success is True  # Tool execution succeeds
        data = result.data
        assert data["success"] is False
        assert "not found" in data["message"]
    
    def test_get_asset_missing_identifier(self, tool, mock_api):
        """Should require identifier for get."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.GET
        ))
        
        assert result.success is True  # Tool execution succeeds
        data = result.data
        assert data["success"] is False
        assert "required" in data["message"].lower()
    
    def test_create_asset_missing_params(self, tool, mock_api):
        """Should require parameters for create."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.CREATE,
            parameters={"serial_number": "TEST001"}  # Missing type_id
        ))
        
        data = result.data
        assert data["success"] is False
        assert "type_id" in data["message"]
    
    def test_delete_asset_requires_confirmation(self, tool, mock_api):
        """Should require confirmation for delete."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.DELETE,
            identifier="ASSET001",
            confirm_destructive=False
        ))
        
        data = result.data
        assert data["success"] is False
        assert "confirm_destructive" in data["message"]
    
    def test_set_asset_state(self, tool, mock_api):
        """Should set asset state."""
        mock_api.asset.set_asset_state.return_value = True
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.SET_STATE,
            identifier="ASSET001",
            parameters={"state": "IN_MAINTENANCE"}
        ))
        
        data = result.data
        assert data["success"] is True
    
    def test_list_asset_types(self, tool, mock_api):
        """Should list asset types."""
        mock_type = MagicMock()
        mock_type.type_id = uuid4()
        mock_type.name = "Equipment"
        mock_type.description = "Test equipment"
        mock_api.asset.get_asset_types.return_value = [mock_type]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST,
            entity_type="asset_type"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1


# =============================================================================
# Product Domain Tests
# =============================================================================

class TestProductOperations:
    """Tests for product domain operations."""
    
    def test_list_products(self, tool, mock_api):
        """Should list products."""
        mock_product = MagicMock()
        mock_product.part_number = "PN001"
        mock_product.name = "Product 1"
        mock_product.state = "Active"
        mock_api.product.get_products.return_value = [mock_product]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCT,
            operation=OperationType.LIST
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1
    
    def test_get_product(self, tool, mock_api):
        """Should get product by part number."""
        mock_product = MagicMock()
        mock_product.part_number = "PN001"
        mock_product.name = "Product 1"
        mock_product.description = "Test product"
        mock_product.state = "Active"
        mock_product.non_serial = False
        mock_product.revisions = []
        mock_api.product.get_product.return_value = mock_product
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCT,
            operation=OperationType.GET,
            identifier="PN001"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["data"]["part_number"] == "PN001"
    
    def test_create_product_missing_part_number(self, tool, mock_api):
        """Should require part_number for create."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCT,
            operation=OperationType.CREATE,
            parameters={"name": "Test"}  # Missing part_number
        ))
        
        data = result.data
        assert data["success"] is False
        assert "part_number" in data["message"]
    
    def test_list_revisions(self, tool, mock_api):
        """Should list product revisions."""
        mock_rev = MagicMock()
        mock_rev.revision = "A"
        mock_rev.name = "Rev A"
        mock_rev.state = "Active"
        mock_api.product.get_revisions.return_value = [mock_rev]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCT,
            operation=OperationType.LIST,
            entity_type="revision",
            parameters={"part_number": "PN001"}
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1
    
    def test_create_revision_missing_params(self, tool, mock_api):
        """Should require part_number and revision for create."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCT,
            operation=OperationType.CREATE,
            entity_type="revision",
            parameters={"part_number": "PN001"}  # Missing revision
        ))
        
        data = result.data
        assert data["success"] is False
        assert "revision" in data["message"]


# =============================================================================
# Production Domain Tests
# =============================================================================

class TestProductionOperations:
    """Tests for production domain operations."""
    
    def test_get_unit(self, tool, mock_api):
        """Should get production unit."""
        mock_unit = MagicMock()
        mock_unit.serial_number = "SN001"
        mock_unit.part_number = "PN001"
        mock_unit.revision = "A"
        mock_unit.unit_phase = "Under Production"
        mock_unit.unit_phase_id = 1
        mock_unit.batch_number = "BATCH001"
        mock_unit.current_location = "Station A"
        mock_unit.parent_serial_number = None
        mock_api.production.get_unit.return_value = mock_unit
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCTION,
            operation=OperationType.GET,
            identifier="SN001",
            parameters={"part_number": "PN001"}
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["data"]["serial_number"] == "SN001"
    
    def test_get_unit_missing_part_number(self, tool, mock_api):
        """Should require part_number for get unit."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCTION,
            operation=OperationType.GET,
            identifier="SN001"  # Missing part_number
        ))
        
        data = result.data
        assert data["success"] is False
        assert "part_number" in data["message"]
    
    def test_set_unit_phase(self, tool, mock_api):
        """Should set unit phase."""
        mock_api.production.set_unit_phase.return_value = True
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCTION,
            operation=OperationType.SET_PHASE,
            identifier="SN001",
            parameters={
                "part_number": "PN001",
                "phase": "Finalized"
            }
        ))
        
        data = result.data
        assert data["success"] is True
    
    def test_verify_unit(self, tool, mock_api):
        """Should verify unit grade."""
        mock_grade = MagicMock()
        mock_grade.status = "Verified"
        mock_grade.grade = "A"
        mock_grade.all_processes_passed_last_run = True
        mock_grade.all_processes_passed_first_run = True
        mock_grade.no_repairs = True
        mock_api.production.get_unit_grade.return_value = mock_grade
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCTION,
            operation=OperationType.VERIFY,
            identifier="SN001",
            parameters={"part_number": "PN001"}
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["data"]["grade"] == "A"
    
    def test_list_phases(self, tool, mock_api):
        """Should list production phases."""
        mock_phase = MagicMock()
        mock_phase.phase_id = 1
        mock_phase.code = "PROD"
        mock_phase.name = "Under Production"
        mock_api.production.get_phases.return_value = [mock_phase]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCTION,
            operation=OperationType.LIST,
            entity_type="phase"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1
    
    def test_add_child_to_assembly(self, tool, mock_api):
        """Should add child to assembly."""
        mock_api.production.add_child_to_assembly.return_value = True
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCTION,
            operation=OperationType.ADD_CHILD,
            entity_type="assembly",
            parameters={
                "parent_serial": "PARENT001",
                "parent_part": "PN001",
                "child_serial": "CHILD001",
                "child_part": "PN002"
            }
        ))
        
        data = result.data
        assert data["success"] is True
    
    def test_remove_child_from_assembly(self, tool, mock_api):
        """Should remove child from assembly."""
        mock_api.production.remove_child_from_assembly.return_value = True
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PRODUCTION,
            operation=OperationType.REMOVE_CHILD,
            entity_type="assembly",
            parameters={
                "parent_serial": "PARENT001",
                "parent_part": "PN001",
                "child_serial": "CHILD001",
                "child_part": "PN002"
            }
        ))
        
        data = result.data
        assert data["success"] is True


# =============================================================================
# Software Domain Tests
# =============================================================================

class TestSoftwareOperations:
    """Tests for software domain operations."""
    
    def test_list_packages(self, tool, mock_api):
        """Should list software packages."""
        mock_pkg = MagicMock()
        mock_pkg.package_id = uuid4()
        mock_pkg.name = "Test Package"
        mock_pkg.version = "1.0.0"
        mock_pkg.status = "Released"
        mock_api.software.get_packages.return_value = [mock_pkg]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.LIST
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1
    
    def test_get_package_by_uuid(self, tool, mock_api):
        """Should get package by UUID."""
        pkg_id = uuid4()
        mock_pkg = MagicMock()
        mock_pkg.package_id = pkg_id
        mock_pkg.name = "Test Package"
        mock_pkg.version = "1.0.0"
        mock_pkg.status = "Released"
        mock_pkg.description = "Test"
        mock_api.software.get_package.return_value = mock_pkg
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.GET,
            identifier=str(pkg_id)
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["data"]["name"] == "Test Package"
    
    def test_get_package_by_name(self, tool, mock_api):
        """Should get package by name."""
        mock_pkg = MagicMock()
        mock_pkg.package_id = uuid4()
        mock_pkg.name = "MyPackage"
        mock_pkg.version = "2.0.0"
        mock_pkg.status = "Released"
        mock_pkg.description = "Test"
        mock_api.software.get_package.return_value = None
        mock_api.software.get_package_by_name.return_value = mock_pkg
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.GET,
            identifier="MyPackage"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["data"]["name"] == "MyPackage"
    
    def test_create_package_missing_name(self, tool, mock_api):
        """Should require name for create."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.CREATE,
            parameters={"version": "1.0.0"}  # Missing name
        ))
        
        data = result.data
        assert data["success"] is False
        assert "name" in data["message"]
    
    def test_delete_package_requires_confirmation(self, tool, mock_api):
        """Should require confirmation for delete."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.DELETE,
            identifier="test-package",
            confirm_destructive=False
        ))
        
        data = result.data
        assert data["success"] is False
        assert "confirm_destructive" in data["message"]
    
    def test_release_package(self, tool, mock_api):
        """Should release package."""
        mock_api.software.release_package.return_value = True
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.RELEASE,
            identifier="test-package-id"
        ))
        
        data = result.data
        assert data["success"] is True
    
    def test_revoke_package_requires_confirmation(self, tool, mock_api):
        """Should require confirmation for revoke."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.REVOKE,
            identifier="test-package-id",
            confirm_destructive=False
        ))
        
        data = result.data
        assert data["success"] is False
        assert "confirm_destructive" in data["message"]
    
    def test_list_virtual_folders(self, tool, mock_api):
        """Should list virtual folders."""
        mock_folder = MagicMock()
        mock_folder.name = "Production"
        mock_folder.path = "/production"
        mock_api.software.get_virtual_folders.return_value = [mock_folder]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.SOFTWARE,
            operation=OperationType.LIST,
            entity_type="virtual_folder"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1


# =============================================================================
# Process Domain Tests
# =============================================================================

class TestProcessOperations:
    """Tests for process domain operations."""
    
    def test_list_test_operations(self, tool, mock_api):
        """Should list test operations."""
        mock_op = MagicMock()
        mock_op.code = 10
        mock_op.name = "Functional Test"
        mock_op.description = "Main test"
        mock_api.process.get_test_operations.return_value = [mock_op]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PROCESS,
            operation=OperationType.LIST,
            entity_type="test_operation"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1
    
    def test_list_repair_operations(self, tool, mock_api):
        """Should list repair operations."""
        mock_op = MagicMock()
        mock_op.code = 20
        mock_op.name = "Component Repair"
        mock_op.description = "Repair operation"
        mock_api.process.get_repair_operations.return_value = [mock_op]
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PROCESS,
            operation=OperationType.LIST,
            entity_type="repair_operation"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["count"] == 1
    
    def test_get_test_operation(self, tool, mock_api):
        """Should get test operation by code."""
        mock_op = MagicMock()
        mock_op.code = 10
        mock_op.name = "Functional Test"
        mock_op.description = "Main test"
        mock_api.process.get_test_operation.return_value = mock_op
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PROCESS,
            operation=OperationType.GET,
            entity_type="test_operation",
            identifier="10"
        ))
        
        data = result.data
        assert data["success"] is True
        assert data["data"]["code"] == 10
    
    def test_process_read_only_for_create(self, tool, mock_api):
        """Should reject create for processes (read-only)."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.PROCESS,
            operation=OperationType.CREATE,
            entity_type="test_operation",
            parameters={"code": 99, "name": "New Test"}
        ))
        
        data = result.data
        assert data["success"] is False
        assert "read-only" in data["message"].lower()


# =============================================================================
# Error Handling Tests
# =============================================================================

class TestErrorHandling:
    """Tests for error handling."""
    
    def test_unknown_entity_type(self, tool, mock_api):
        """Should handle unknown entity type."""
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST,
            entity_type="unknown_entity"
        ))
        
        data = result.data
        assert data["success"] is False
        assert "unknown" in data["message"].lower()
    
    def test_api_exception(self, tool, mock_api):
        """Should handle API exceptions."""
        mock_api.asset.get_assets.side_effect = Exception("Connection error")
        
        result = tool._execute(ControlPanelInput(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST
        ))
        
        assert result.success is False
        assert "Exception" in result.summary


# =============================================================================
# Helper Method Tests
# =============================================================================

class TestHelperMethods:
    """Tests for helper methods."""
    
    def test_is_uuid_valid(self, tool):
        """Should recognize valid UUIDs."""
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        assert tool._is_uuid(valid_uuid) is True
    
    def test_is_uuid_invalid(self, tool):
        """Should reject invalid UUIDs."""
        assert tool._is_uuid("not-a-uuid") is False
        assert tool._is_uuid("PN001") is False
        assert tool._is_uuid(None) is False
    
    def test_build_summary_success(self, tool):
        """Should build success summary."""
        result = ControlPanelResult(
            domain=ManagementDomain.ASSET,
            operation=OperationType.LIST,
            entity_type="asset",
            success=True,
            message="Found 3 assets",
            items=[{"name": "A"}, {"name": "B"}, {"name": "C"}],
            count=3
        )
        summary = tool._build_summary(result)
        assert "✅" in summary
        assert "ASSET" in summary
        assert "3" in summary
    
    def test_build_summary_failure(self, tool):
        """Should build failure summary."""
        result = ControlPanelResult(
            domain=ManagementDomain.PRODUCT,
            operation=OperationType.CREATE,
            entity_type="product",
            success=False,
            message="Missing required field"
        )
        summary = tool._build_summary(result)
        assert "❌" in summary
        assert "PRODUCT" in summary


# =============================================================================
# Integration Tests
# =============================================================================

class TestToolIntegration:
    """Integration tests for the tool."""
    
    def test_tool_in_registry(self):
        """Tool should be registered in the registry."""
        from pywats_agent.tools._registry import get_tool
        tool_class = get_tool("control_panel")
        assert tool_class is not None
        assert tool_class is ControlPanelTool
    
    def test_tool_in_profiles(self):
        """Tool should be in appropriate profiles."""
        from pywats_agent.tools.variants import PROFILES
        
        # Should be in full profile
        assert "control_panel" in PROFILES["full"].tools
        
        # Should be in admin profile
        assert "control_panel" in PROFILES["admin"].tools
    
    def test_tool_category(self):
        """Tool should be in admin category."""
        from pywats_agent.tools.variants import TOOL_CATEGORIES, ToolCategory
        assert TOOL_CATEGORIES.get("control_panel") == ToolCategory.ADMIN


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
