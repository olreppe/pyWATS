# VTE → WATS Integration Project

**Status:** 📋 Planned  
**Completion:** 0%  
**Created:** 2026-02-02  
**Target:** Q2 2026

---

## Overview

Build an official WATS integration adapter for **Keysight VTE** (VEE Test Executive) that extracts test results from VTE's SQL Server database and uploads them to WATS.

**VTE Context:**
- **Product:** Keysight VEE Test Executive 9.31.1
- **Database:** Microsoft SQL Server (VTE 9_3)
- **Vendor:** Keysight Technologies
- **Use Case:** Manufacturing test automation, instrument control, production test logging

**Key Focus:**
- Extract test results from VTE's 21-table schema
- Map VTE data model to WATS report structure
- Incremental sync with idempotency (timestamp-based)
- Production-ready .NET adapter or Python integration
- Handle repair data, numeric/text step results, UUT tracking

---

## Objectives

1. **Data Access Layer** - Build robust VTE database reader (Dapper/.NET or Python)
2. **Data Mapping** - Transform VTE IndexData/TestData to WATS reports
3. **Incremental Sync** - Timestamp-based extraction with watermark tracking
4. **Idempotency** - Use IndexData.Index_GUID as stable key
5. **Production Deployment** - Service/CLI for continuous sync

---

## Success Criteria

- [ ] Adapter extracts test runs from VTE database without errors
- [ ] All step results (numeric, text, other) mapped to WATS correctly
- [ ] Incremental sync processes only new results since last run
- [ ] Duplicate detection via Index_GUID prevents re-upload
- [ ] Adapter handles 1000+ test results per hour
- [ ] Deployment package with configuration and documentation

---

## Stakeholders

**Owner:** Integration Team  
**Users:** Manufacturing sites using Keysight VTE  
**Sponsors:** Customers with VEE/VTE test systems

---

## Timeline

- **Phase 1:** VTE schema analysis & data model design - 1 week
- **Phase 2:** .NET data access library (Dapper) - 2 weeks
- **Phase 3:** WATS mapping & upload logic - 2 weeks
- **Phase 4:** Incremental sync & watermarking - 1 week
- **Phase 5:** Testing & deployment - 1 week

**Estimated Completion:** 7 weeks from start

---

## Dependencies

- VTE 9.31.1 installation with SQL Server access
- VTE database create scripts (schema documentation)
- WATS API credentials for upload
- .NET 8 SDK or Python 3.10+ environment
- pyWATS library (if Python implementation)

---

## Risks

- **High:** VTE schema variations across versions (9.3x vs 9.2x vs 9.1x)
- **Medium:** Timezone handling for IndexData.Timestamp (local vs UTC)
- **Medium:** Large result sets may require batching/paging
- **Low:** Repair data complexity (RepairActions, RepairSyndromes)
- **Low:** TestDataOther format unknown (opaque binary data)

---

## Related Projects

- client-components-polish (active) - May include VTE adapter UI
- performance-optimization (active) - Bulk upload optimization applies

---

## References

- [VTE Integration Guide](VTE_VEE_WATS_integration.md)
- [VTE Database ERD](VTE_VEE_WATS_integration.md#4-entity-relationships-erd)
- [.NET Data Access Skeleton](Vte.DataAccess/README.md)
- Keysight VEE Pro 9.33 documentation
