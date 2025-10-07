# Module Implementation Phases

Based on analysis of REST API coverage and complexity, this document outlines the phased implementation approach for pyWATS modules.

## Analysis Summary

| Module | Functions Analyzed | Clear REST Mapping | Percentage Match | Implementation Priority |
|--------|-------------------|-------------------|------------------|----------------------|
| **Report** | 5 | 5 | **100%** | Phase 1 |
| **Product** | 8 | 5 | **62%** | Phase 1 |
| **Production** | 10 | 5 | **50%** | Phase 1 |
| **Asset** | 10 | 4 | **40%** | Phase 2 |
| **Workflow** | 15 | 0 | **0%** | Phase 3 |
| **Software** | 8 | 0 | **0%** | Phase 3 |
| **Overall** | **56** | **19** | **34%** | - |

---

## Phase 1: Core CRUD Operations (High REST Coverage)

**Target Modules**: Report, Product, Production
**Estimated Coverage**: 19/56 functions (34% of total API)
**Implementation Focus**: Direct REST API integration with model returns

### Report Module (100% Coverage)
| Function | Return Type | REST API Call | Status |
|----------|-------------|---------------|---------|
| `get_report(report_id)` | `Report` | `GET /api/report/{report_id}` | ✅ Ready |
| `get_reports(...)` | `List[Report]` | `GET /api/report?filter=...` | ✅ Ready |
| `create_report(...)` | `Report` | `POST /api/report` | ✅ Ready |
| `update_report(...)` | `Report` | `PUT /api/report/{report_id}` | ✅ Ready |
| `delete_report(...)` | `bool` | `DELETE /api/report/{report_id}` | ✅ Ready |

### Product Module (62% Coverage)
| Function | Return Type | REST API Call | Status |
|----------|-------------|---------------|---------|
| `get_product_info(part_number, revision)` | `ProductInfo` | `GET /api/productinfo/{part_number}/{revision}` | ✅ Ready |
| `get_product_infos(...)` | `List[ProductInfo]` | `GET /api/productinfo?filter=...` | ✅ Ready |
| `create_product_info(...)` | `ProductInfo` | `POST /api/productinfo` | ✅ Ready |
| `update_product_info(...)` | `ProductInfo` | `PUT /api/productinfo/{part_number}/{revision}` | ✅ Ready |
| `delete_product_info(...)` | `bool` | `DELETE /api/productinfo/{part_number}/{revision}` | ✅ Ready |
| `get_bom(...)` | `List[BomItem]` | Custom BOM endpoint needed | ⏳ Phase 2 |
| `get_processes(...)` | `List[Process]` | Custom process endpoint needed | ⏳ Phase 2 |
| `identify_product(...)` | `ProductInfo` | Custom identification logic | ⏳ Phase 3 |

### Production Module (50% Coverage)
| Function | Return Type | REST API Call | Status |
|----------|-------------|---------------|---------|
| `get_unit_info(serial_number)` | `UnitInfo` | `GET /api/unitinfo/{serial_number}` | ✅ Ready |
| `get_unit_infos(...)` | `List[UnitInfo]` | `GET /api/unitinfo?filter=...` | ✅ Ready |
| `create_unit_info(...)` | `UnitInfo` | `POST /api/unitinfo` | ✅ Ready |
| `update_unit_info(...)` | `UnitInfo` | `PUT /api/unitinfo/{serial_number}` | ✅ Ready |
| `delete_unit_info(...)` | `bool` | `DELETE /api/unitinfo/{serial_number}` | ✅ Ready |
| `get_production_lot(...)` | `ProductionLot` | Custom lot management needed | ⏳ Phase 2 |
| `create_production_lot(...)` | `ProductionLot` | Custom lot management needed | ⏳ Phase 2 |
| `generate_serial_numbers(...)` | `List[str]` | Custom SN generation needed | ⏳ Phase 3 |
| `get_unit_position(...)` | `UnitPosition` | Custom positioning logic | ⏳ Phase 3 |
| `set_unit_position(...)` | `bool` | Custom positioning logic | ⏳ Phase 3 |

---

## Phase 2: Extended Operations (Moderate REST Coverage)

**Target Modules**: Asset (extended), Product (BOM/Process), Production (Lots)
**Implementation Focus**: Custom endpoints + business logic

### Asset Module Extensions
- Asset type management
- Parent/child relationships  
- Usage tracking and counters
- Calibration and maintenance workflows

### Product Module Extensions
- BOM (Bill of Materials) management
- Process definitions and workflows
- Product hierarchy navigation

### Production Module Extensions
- Production lot management
- Unit positioning and tracking
- Batch operations

---

## Phase 3: Advanced Business Logic (Low REST Coverage)

**Target Modules**: Workflow, Software, Production (Advanced), Product (Advanced)
**Implementation Focus**: Custom business logic + workflow engines

### Workflow Module
- Test lifecycle management
- Repair workflows and tracking
- State management and transitions
- Business rule validation

### Software Module  
- Package management and deployment
- Version control and rollback
- Installation tracking and status

### Advanced Production Features
- Serial number generation strategies
- Advanced unit positioning
- Production analytics

### Advanced Product Features
- Interactive product identification
- Dynamic process selection
- Context-aware operations

---

## Implementation Strategy

### Phase 1 Approach
1. **Model-First Design**: Return typed models instead of dictionaries
2. **REST API Integration**: Direct mapping to existing REST endpoints
3. **Error Handling**: Proper exception handling and response validation
4. **Type Safety**: Full type annotations and Pydantic validation

### Response Pattern
```python
def get_product_info(self, part_number: str, revision: str = "") -> ProductInfo:
    """Get product information."""
    try:
        response = self._http_client.get(f"/api/productinfo/{part_number}/{revision}")
        data = self._extract_data(response)
        return ProductInfo.from_dict(data)
    except Exception as e:
        self._handle_api_error(e, f"Get product info {part_number}")
        raise
```

### Success Metrics
- All Phase 1 functions return proper model types
- Full type safety with IDE autocompletion
- Comprehensive error handling
- 100% test coverage for implemented functions
- Performance benchmarks established

### Timeline
- **Phase 1**: 2-3 weeks (Core CRUD operations)
- **Phase 2**: 3-4 weeks (Extended operations)
- **Phase 3**: 4-6 weeks (Advanced business logic)

**Total Estimated Timeline**: 9-13 weeks for complete implementation