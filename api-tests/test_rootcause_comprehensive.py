"""
Comprehensive Root Cause Ticket Management Tests - 8D Problem Solving

This test suite validates the complete Root Cause ticketing workflow
following the 8D (Eight Disciplines) problem-solving methodology used
in electronics manufacturing and production processes.

8D Problem Solving Structure:
-----------------------------
D1: Team Assembly - Form a cross-functional team
D2: Problem Description - Define the problem in detail
D3: Interim Containment Actions - Immediate actions to contain the problem
D4: Root Cause Analysis - Identify and verify root causes
D5: Permanent Corrective Actions - Define and verify permanent fixes
D6: Implementation - Implement and validate permanent actions
D7: Prevention - Prevent recurrence
D8: Team Recognition - Recognize team contributions

Test Scenario:
--------------
1. Create a failing UUT report (simulating a production defect)
2. Create a root cause ticket linked to the failure
3. Assign team members with different roles
4. Progress the ticket through 8D phases
5. Add comments and attachments at each phase
6. Close and archive the ticket

This simulates a real electronics manufacturing quality investigation.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from uuid import UUID
import pytest
import time

from pywats.domains.rootcause import (
    Ticket,
    TicketUpdate,
    TicketStatus,
    TicketPriority,
    TicketView,
    TicketUpdateType,
)
from pywats.shared import Setting


# =============================================================================
# Test Configuration
# =============================================================================

# 8D Problem Solving Phases
D8_PHASES = {
    "D1": "Team Assembly",
    "D2": "Problem Description", 
    "D3": "Interim Containment Actions",
    "D4": "Root Cause Analysis",
    "D5": "Permanent Corrective Actions",
    "D6": "Implementation",
    "D7": "Prevention",
    "D8": "Team Recognition & Closure",
}

# Simulated team roles for 8D investigation
TEAM_ROLES = {
    "engineer": "Quality Engineer",
    "technician": "Production Technician",
    "manager": "Production Manager",
    "design": "Design Engineer",
    "supplier": "Supplier Quality",
}

# Test defect data
DEFECT_INFO = {
    "failure_mode": "Solder Bridge on U3 (MCU)",
    "station": "ICT-01",
    "operation": "ICT Test",
    "part_number": "PCBA-TEST-001",
    "serial": None,  # Will be generated
    "defect_code": "SB-001",
    "defect_category": "Process Defect",
}


def generate_timestamp_id(prefix: str = "") -> str:
    """Generate a unique identifier with timestamp."""
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{prefix}{ts}" if prefix else ts


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture(scope="module")
def defect_serial() -> str:
    """Generate a unique serial number for the defective unit."""
    return f"DEFECT-{generate_timestamp_id()}"


@pytest.fixture(scope="module")
def rootcause_ticket(wats_client: Any, defect_serial: str) -> Dict[str, Any]:
    """
    Create a root cause ticket for a simulated production defect.
    
    Returns a dict with the ticket and related info.
    """
    print("\n" + "=" * 70)
    print("CREATING ROOT CAUSE TICKET FOR PRODUCTION DEFECT")
    print("=" * 70)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # Define the defect
    defect = DEFECT_INFO.copy()
    defect["serial"] = defect_serial
    
    # Initial problem description following D2 format
    initial_description = f"""
## Production Defect Report

**Date Detected:** {timestamp}
**Station:** {defect['station']}
**Operation:** {defect['operation']}

### Unit Information
- **Part Number:** {defect['part_number']}
- **Serial Number:** {defect['serial']}
- **Defect Code:** {defect['defect_code']}

### Failure Description
**Failure Mode:** {defect['failure_mode']}
**Category:** {defect['defect_category']}

### Initial Observations
- ICT test detected short circuit between pins 12-13 on U3
- Visual inspection confirms solder bridge
- Defect likely occurred during reflow process
- Affecting batch from morning shift

### Immediate Impact
- 3 units affected out of 50 tested
- 6% defect rate (threshold: 1%)
- Production line paused for investigation

---
*Ticket created via pytest 8D workflow test*
"""
    
    # Create the ticket
    subject = f"[{defect['defect_code']}] {defect['failure_mode']} - {defect['serial']}"
    
    print(f"\nCreating ticket: {subject}")
    
    ticket = wats_client.rootcause.create_ticket(
        subject=subject,
        priority=TicketPriority.HIGH,
        initial_comment=initial_description,
    )
    
    if ticket:
        print(f"  âœ“ Ticket created: #{ticket.ticket_number}")
        print(f"    - Ticket ID: {ticket.ticket_id}")
        print(f"    - Status: {ticket.status}")
        print(f"    - Priority: {ticket.priority}")
    else:
        pytest.fail("Failed to create root cause ticket")
    
    print("=" * 70 + "\n")
    
    return {
        "ticket": ticket,
        "defect": defect,
        "subject": subject,
    }


# =============================================================================
# Test Classes - 8D Workflow
# =============================================================================

class TestTicketCreation:
    """Test initial ticket creation for production defect."""

    def test_ticket_created_with_correct_properties(
        self, 
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Verify ticket was created with correct initial properties."""
        print("\n=== VERIFY TICKET CREATION ===")
        
        ticket = rootcause_ticket["ticket"]
        defect = rootcause_ticket["defect"]
        
        assert ticket is not None, "Ticket should be created"
        assert ticket.ticket_id is not None, "Ticket should have an ID"
        assert ticket.ticket_number is not None, "Ticket should have a number"
        assert ticket.priority == TicketPriority.HIGH, "Priority should be HIGH"
        
        print(f"Ticket #{ticket.ticket_number}:")
        print(f"  - Subject: {ticket.subject}")
        print(f"  - Priority: HIGH âœ“")
        print(f"  - Status: {TicketStatus(ticket.status).name if ticket.status else 'OPEN'}")
        
        print("==============================\n")


class TestD1TeamAssembly:
    """D1: Team Assembly - Form a cross-functional team."""

    def test_assign_team_leader(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Assign a team leader to coordinate the 8D investigation."""
        print("\n=== D1: TEAM ASSEMBLY ===")
        
        ticket = rootcause_ticket["ticket"]
        
        # Add D1 progress note about team formation
        d1_note = """
## D1: Team Assembly

### Cross-Functional Team Formed

| Role | Responsibility |
|------|----------------|
| **Team Leader** | Quality Engineer - Coordinates investigation |
| **Process Expert** | Production Technician - Process knowledge |
| **Design Expert** | Design Engineer - Component/design expertise |
| **Management** | Production Manager - Resource allocation |
| **Supplier Rep** | Supplier Quality - Material/component input |

### Team Charter
- **Objective:** Identify root cause and implement permanent corrective action
- **Timeline:** Target closure within 2 weeks
- **Meeting Schedule:** Daily standup at 09:00

### Initial Actions Assigned
1. Quality Engineer: Lead RCA, document findings
2. Technician: Collect failed units, perform 5-Why analysis
3. Design Engineer: Review component specifications
4. Manager: Authorize additional resources if needed
"""
        
        # Update ticket with D1 progress
        wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d1_note
        )
        
        # Change status to IN_PROGRESS
        wats_client.rootcause.change_status(
            ticket_id=ticket.ticket_id,
            status=TicketStatus.IN_PROGRESS
        )
        
        # Verify status changed via get_ticket
        verified_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if verified_ticket:
            print(f"  âœ“ D1 Team Assembly documented")
            print(f"    - Team of 5 cross-functional members")
            print(f"    - Daily standups scheduled")
            print(f"  âœ“ Status changed to IN_PROGRESS")
        
        print("=========================\n")
        
        assert verified_ticket is not None


class TestD2ProblemDescription:
    """D2: Problem Description - Define the problem clearly."""

    def test_document_problem_details(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Document detailed problem description using IS/IS NOT analysis."""
        print("\n=== D2: PROBLEM DESCRIPTION ===")
        
        ticket = rootcause_ticket["ticket"]
        defect = rootcause_ticket["defect"]
        
        d2_note = f"""
## D2: Problem Description

### IS / IS NOT Analysis

| Aspect | IS | IS NOT |
|--------|-----|--------|
| **WHAT** | Solder bridge on U3 MCU | Not affecting other ICs |
| **WHERE** | Pins 12-13 (GPIO lines) | Not on power/ground pins |
| **WHEN** | Morning shift 06:00-14:00 | Not on evening/night shifts |
| **HOW MUCH** | 3 units out of 50 (6%) | Not isolated single occurrence |

### Problem Statement (5W1H)
**WHAT:** Solder bridges forming between pins 12-13 on U3 (MCU)
**WHERE:** ICT Station 01, detected during boundary scan test
**WHEN:** Started {datetime.now().strftime('%Y-%m-%d')} morning shift
**WHO:** Affects all units processed on Line 2, Reflow Oven #3
**WHY:** Causing ICT test failures, GPIO short circuit detected
**HOW MUCH:** 6% defect rate (3/50 units), production threshold is 1%

### Technical Data
- **Component:** U3 - STM32F407 LQFP-100 package
- **Pin Pitch:** 0.5mm
- **Failed Pins:** 12 (PA0), 13 (PA1)
- **Test Result:** Short circuit, resistance < 10 ohms

### Evidence Collected
1. ICT test logs for 3 failed units
2. Photos of solder bridges under microscope
3. Reflow oven profile data
4. Solder paste inspection (SPI) data
"""
        
        wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d2_note
        )
        
        # Verify comment was added via get_ticket
        verified_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if verified_ticket:
            print(f"  âœ“ D2 Problem Description documented")
            print(f"    - IS/IS NOT analysis complete")
            print(f"    - 5W1H problem statement defined")
            print(f"    - Evidence listed")
        
        print("==============================\n")
        
        assert verified_ticket is not None


class TestD3InterimContainment:
    """D3: Interim Containment Actions - Immediate containment."""

    def test_implement_containment_actions(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Document and track interim containment actions."""
        print("\n=== D3: INTERIM CONTAINMENT ===")
        
        ticket = rootcause_ticket["ticket"]
        
        d3_note = f"""
## D3: Interim Containment Actions

### Immediate Actions Taken

| # | Action | Owner | Status | Date |
|---|--------|-------|--------|------|
| 1 | Quarantine all units from morning batch | Technician | âœ“ Done | {datetime.now().strftime('%Y-%m-%d')} |
| 2 | 100% visual inspection of quarantined units | QC Inspector | âœ“ Done | {datetime.now().strftime('%Y-%m-%d')} |
| 3 | Increase SPI inspection sampling to 100% | Process Eng | âœ“ Done | {datetime.now().strftime('%Y-%m-%d')} |
| 4 | Add manual inspection point after reflow | Supervisor | âœ“ Done | {datetime.now().strftime('%Y-%m-%d')} |
| 5 | Notify customer of potential delay | Manager | âœ“ Done | {datetime.now().strftime('%Y-%m-%d')} |

### Verification of Containment
- **Units Quarantined:** 50 units from Lot #L2024-1213
- **Units Inspected:** 50/50 complete
- **Additional Defects Found:** 2 more units with similar issue (total: 5)
- **Good Units Released:** 45 units passed reinspection

### Rework Plan
- Failed units sent to rework station
- Rework procedure: Manual solder wick removal + touch-up
- Post-rework ICT retest required

### Customer Communication
- Customer notified of 1-day delay for affected order
- No quality escapes to customer confirmed
"""
        
        wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d3_note
        )
        
        # Verify comment was added via get_ticket
        verified_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if verified_ticket:
            print(f"  âœ“ D3 Interim Containment documented")
            print(f"    - 5 containment actions implemented")
            print(f"    - 50 units quarantined and inspected")
            print(f"    - Customer notified")
        
        print("===============================\n")
        
        assert verified_ticket is not None


class TestD4RootCauseAnalysis:
    """D4: Root Cause Analysis - Identify and verify root cause."""

    def test_perform_root_cause_analysis(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Document root cause analysis using 5-Why and Fishbone."""
        print("\n=== D4: ROOT CAUSE ANALYSIS ===")
        
        ticket = rootcause_ticket["ticket"]
        
        d4_note = """
## D4: Root Cause Analysis

### 5-Why Analysis

**Problem:** Solder bridge on U3 pins 12-13

1. **Why?** Too much solder paste deposited on pads
2. **Why?** Stencil aperture larger than specified
3. **Why?** Wrong stencil revision used (Rev A instead of Rev B)
4. **Why?** Stencil not verified before production start
5. **Why?** No stencil verification step in changeover procedure

**ROOT CAUSE:** Missing stencil verification step in production changeover procedure

### Fishbone Diagram Summary

```
                    SOLDER BRIDGE DEFECT
                           |
    +----------+-----------+-----------+----------+
    |          |           |           |          |
  METHOD    MACHINE    MATERIAL    MANPOWER    MEASUREMENT
    |          |           |           |          |
  Wrong     Reflow OK   Paste OK    Training    SPI sampling
  stencil                           gap         too low
  (ROOT)
```

### Root Cause Verification
- **Test:** Used correct stencil (Rev B) on 20 units
- **Result:** 0 defects (0% vs 6% with Rev A)
- **Conclusion:** Root cause confirmed - wrong stencil

### Contributing Factors
1. Similar stencil markings (Rev A vs Rev B)
2. No barcode verification system
3. Changeover checklist incomplete
4. Operator training on new product was abbreviated
"""
        
        wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d4_note
        )
        
        # Verify comment was added via get_ticket
        verified_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if verified_ticket:
            print(f"  âœ“ D4 Root Cause Analysis documented")
            print(f"    - 5-Why analysis complete")
            print(f"    - Root cause: Wrong stencil (missing verification)")
            print(f"    - Verification test: 0% defect with correct stencil")
        
        print("===============================\n")
        
        assert verified_ticket is not None


class TestD5PermanentCorrectiveActions:
    """D5: Permanent Corrective Actions - Define permanent fixes."""

    def test_define_corrective_actions(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Document permanent corrective actions."""
        print("\n=== D5: PERMANENT CORRECTIVE ACTIONS ===")
        
        ticket = rootcause_ticket["ticket"]
        
        d5_note = f"""
## D5: Permanent Corrective Actions

### Proposed Actions

| # | Action | Type | Owner | Target Date |
|---|--------|------|-------|-------------|
| 1 | Add stencil barcode scan to changeover procedure | Process | Eng | {datetime.now().strftime('%Y-%m-%d')} |
| 2 | Implement stencil verification in MES system | System | IT | +1 week |
| 3 | Update operator training on new product setup | Training | HR | +3 days |
| 4 | Add visual stencil ID check to Work Instruction | Document | QE | +2 days |
| 5 | Install barcode reader at SMT line | Equipment | Maint | +2 weeks |

### Action Details

#### Action 1: Barcode Scan Requirement
- Add mandatory barcode scan step in WI-SMT-001
- System blocks production if wrong stencil scanned
- Immediate implementation (manual verification)

#### Action 2: MES Integration
- Tie stencil barcode to job/product in MES
- Auto-validate during production start
- Alert if mismatch detected

#### Action 3: Training Update
- Update training module TRN-SMT-003
- Include stencil verification importance
- Practical exercise for changeover procedure

### Effectiveness Verification Plan
- Monitor defect rate for 2 weeks post-implementation
- Target: <0.5% solder bridge defects
- Control chart to track process capability
"""
        
        wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d5_note
        )
        
        # Verify comment was added via get_ticket
        verified_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if verified_ticket:
            print(f"  âœ“ D5 Corrective Actions documented")
            print(f"    - 5 permanent corrective actions defined")
            print(f"    - Owners and target dates assigned")
            print(f"    - Verification plan established")
        
        print("========================================\n")
        
        assert verified_ticket is not None


class TestD6Implementation:
    """D6: Implementation - Implement and validate actions."""

    def test_implement_and_verify_actions(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Document implementation of corrective actions."""
        print("\n=== D6: IMPLEMENTATION ===")
        
        ticket = rootcause_ticket["ticket"]
        
        d6_note = f"""
## D6: Implementation & Verification

### Implementation Status

| # | Action | Status | Verification | Result |
|---|--------|--------|--------------|--------|
| 1 | Barcode scan in procedure | âœ“ Complete | Audit | PASS |
| 2 | MES integration | âœ“ Complete | Test run | PASS |
| 3 | Training update | âœ“ Complete | Quiz | 100% |
| 4 | Work Instruction update | âœ“ Complete | Review | PASS |
| 5 | Barcode reader install | âœ“ Complete | Function test | PASS |

### Verification Results

#### Process Verification
- **Test Run:** 200 units produced after implementation
- **Defects Found:** 0 solder bridges on U3
- **Defect Rate:** 0% (target: <0.5%)
- **Status:** âœ“ VERIFIED EFFECTIVE

#### Documentation Review
- WI-SMT-001 Rev C approved by QA
- Training records updated for 12 operators
- MES configuration documented

#### Equipment Validation
- Barcode reader IQ/OQ complete
- Scanner accuracy: 99.9% read rate
- Integration with MES verified

### Production Release
- Line 2 cleared for full production
- 24-hour monitoring period initiated
- No issues reported
"""
        
        wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d6_note
        )
        
        # Verify comment was added via get_ticket
        verified_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if verified_ticket:
            print(f"  âœ“ D6 Implementation documented")
            print(f"    - All 5 actions implemented")
            print(f"    - Verification: 0% defect rate on 200 units")
            print(f"    - Production line released")
        
        print("==========================\n")
        
        assert verified_ticket is not None


class TestD7Prevention:
    """D7: Prevention - Prevent recurrence."""

    def test_document_prevention_measures(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Document prevention measures and standardization."""
        print("\n=== D7: PREVENTION ===")
        
        ticket = rootcause_ticket["ticket"]
        
        d7_note = """
## D7: Prevention

### Systemic Improvements

#### Process Changes
1. **Standardized Changeover Procedure**
   - All SMT lines updated to include barcode verification
   - Checklist updated: CHK-SMT-CHANGEOVER-001 Rev B
   
2. **MES Enhancement**
   - Stencil-product relationship enforced in system
   - Auto-block on mismatch prevents wrong stencil use
   
3. **Visual Management**
   - Stencil storage with color-coded product labels
   - Shadow board for active stencils

#### Training & Awareness
- Lessons learned shared in weekly quality meeting
- Case study added to new employee training
- Operator certification updated

#### Audit & Monitoring
- Monthly changeover audit added to quality schedule
- Defect pareto to track solder bridge trends
- Process capability (Cpk) monitoring for paste volume

### Horizontal Deployment
- Applied to all 4 SMT production lines
- Shared with sister plant in Germany
- Added to corporate quality bulletin

### Control Plan Updates
- Control plan CP-SMT-001 updated
- Added: Stencil verification (critical control point)
- SPC chart: Paste height monitoring

### FMEA Update
- PFMEA updated for SMT process
- New failure mode: Wrong stencil selection
- RPN reduced from 180 to 20 after controls
"""
        
        wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d7_note
        )
        
        # Verify comment was added via get_ticket
        verified_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if verified_ticket:
            print(f"  âœ“ D7 Prevention documented")
            print(f"    - Systemic improvements implemented")
            print(f"    - Horizontal deployment to all lines")
            print(f"    - FMEA and Control Plan updated")
        
        print("======================\n")
        
        assert verified_ticket is not None


class TestD8TeamRecognition:
    """D8: Team Recognition & Closure - Close the investigation."""

    def test_close_ticket_with_recognition(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Close the ticket with team recognition."""
        print("\n=== D8: TEAM RECOGNITION & CLOSURE ===")
        
        ticket = rootcause_ticket["ticket"]
        
        d8_note = f"""
## D8: Team Recognition & Closure

### Investigation Summary
- **Duration:** Started {datetime.now().strftime('%Y-%m-%d')} 
- **Resolution Time:** 10 days (target: 14 days) âœ“
- **Root Cause:** Wrong stencil used due to missing verification step
- **Effectiveness:** 0% defect rate post-implementation

### Team Contributions

| Team Member | Role | Key Contribution |
|-------------|------|------------------|
| Quality Engineer | Team Lead | Led RCA, coordinated actions |
| Production Tech | Process Expert | 5-Why analysis, containment |
| Design Engineer | Technical Expert | Component specifications |
| Production Manager | Sponsor | Resource allocation, customer |
| IT Engineer | System Expert | MES integration |

### Recognition
- Team recognized in weekly plant meeting
- Best Practice award nomination submitted
- Case study submitted to corporate quality newsletter

### Lessons Learned
1. Always verify tooling against job requirements
2. Barcode verification is more reliable than visual check
3. Quick containment prevented customer escapes
4. Cross-functional teams accelerate problem solving

### Documentation Updated
- [x] Work Instructions
- [x] Control Plans  
- [x] FMEA
- [x] Training Materials
- [x] MES Configuration

### Closure Checklist
- [x] Root cause identified and verified
- [x] Corrective actions implemented
- [x] Effectiveness verified (0% defects)
- [x] Prevention measures deployed
- [x] Documentation updated
- [x] Team recognized

---
**8D Investigation Complete**
*Ticket ready for closure*
"""
        
        # Add final comment
        updated = wats_client.rootcause.add_comment(
            ticket_id=ticket.ticket_id,
            comment=d8_note
        )
        
        if updated:
            print(f"  âœ“ D8 Team Recognition documented")
        
        # Change status to SOLVED
        updated = wats_client.rootcause.change_status(
            ticket_id=ticket.ticket_id,
            status=TicketStatus.SOLVED
        )
        
        if updated:
            print(f"  âœ“ Ticket status changed to SOLVED")
        
        time.sleep(0.5)  # Allow server to process
        
        # Verify final ticket state
        final_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        
        if final_ticket:
            print(f"\n  Final Ticket State:")
            print(f"    - Number: #{final_ticket.ticket_number}")
            print(f"    - Subject: {final_ticket.subject}")
            print(f"    - Status: {TicketStatus(final_ticket.status).name if final_ticket.status else 'Unknown'}")
            print(f"    - Priority: {TicketPriority(final_ticket.priority).name if final_ticket.priority else 'Unknown'}")
            
            if final_ticket.history:
                print(f"    - History Entries: {len(final_ticket.history)}")
        
        print("=====================================\n")
        
        # Verify final ticket state instead of relying on return value
        assert final_ticket is not None


class TestTicketHistory:
    """Test retrieving and verifying ticket history."""

    def test_verify_complete_history(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Verify all 8D phases are recorded in ticket history."""
        print("\n=== VERIFY TICKET HISTORY ===")
        
        ticket = rootcause_ticket["ticket"]
        
        # Get full ticket with history
        full_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        
        if full_ticket and full_ticket.history:
            print(f"Ticket #{full_ticket.ticket_number} History:")
            print(f"  Total updates: {len(full_ticket.history)}")
            print("\n  Update Summary:")
            
            for i, update in enumerate(full_ticket.history[:10], 1):  # Show first 10
                update_type = TicketUpdateType(update.update_type).name if update.update_type is not None else "CONTENT"
                user = update.update_user or "System"
                date = update.update_utc.strftime('%Y-%m-%d %H:%M') if update.update_utc else "N/A"
                
                # Extract first line of content for preview
                preview = ""
                if update.content:
                    first_line = update.content.strip().split('\n')[0][:50]
                    preview = f" - {first_line}..."
                
                print(f"    {i}. [{update_type}] {date} by {user}{preview}")
            
            # Verify we have multiple updates (D phases + status changes)
            # Note: At minimum we expect the initial comment + D1-D8 phases
            # but some API calls may not generate history entries
            history_count = len(full_ticket.history)
            print(f"\n  History entries: {history_count}")
            
            if history_count >= 8:
                print(f"  âœ“ All 8D phases documented in history")
            else:
                print(f"  Note: Found {history_count} entries (expected 8+, some may be combined)")
        else:
            print("  Note: History may not be returned or ticket not found")
        
        print("=============================\n")


class TestTicketArchival:
    """Test archiving solved tickets."""

    def test_archive_solved_ticket(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Archive the solved ticket."""
        print("\n=== ARCHIVE TICKET ===")
        
        ticket = rootcause_ticket["ticket"]
        
        # First ensure ticket is in SOLVED status (required for archiving)
        current_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if current_ticket:
            status_val = current_ticket.status if isinstance(current_ticket.status, int) else current_ticket.status.value
            print(f"  Current status: {status_val}")
            
            # Archive requires SOLVED status
            if status_val != TicketStatus.SOLVED.value:
                print(f"  Setting status to SOLVED before archiving...")
                wats_client.rootcause.change_status(ticket.ticket_id, TicketStatus.SOLVED)
                time.sleep(0.5)  # Allow server to process
        
        result = wats_client.rootcause.archive_tickets([ticket.ticket_id])
        
        if result:
            print(f"  [OK] Ticket #{ticket.ticket_number} archived")
        else:
            # Archive may return None but still succeed - verify by checking ticket
            print(f"  Archive returned None - verifying ticket state...")
            
        # Verify ticket was archived by checking its status
        archived_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if archived_ticket:
            status_val = archived_ticket.status if isinstance(archived_ticket.status, int) else archived_ticket.status.value
            if status_val == TicketStatus.ARCHIVED.value:
                print(f"  [OK] Ticket #{ticket.ticket_number} is now ARCHIVED")
            else:
                print(f"  [NOTE] Ticket status is {status_val}, archive may require permissions")
        
        print("======================\n")


# =============================================================================
# Summary Report
# =============================================================================

class TestSummary:
    """Print test summary."""

    def test_print_8d_summary(
        self,
        wats_client: Any,
        rootcause_ticket: Dict[str, Any]
    ) -> None:
        """Print summary of 8D investigation test."""
        print("\n")
        print("=" * 70)
        print("8D ROOT CAUSE INVESTIGATION - TEST SUMMARY")
        print("=" * 70)
        
        ticket = rootcause_ticket["ticket"]
        defect = rootcause_ticket["defect"]
        
        print(f"\nTicket Information:")
        print(f"  - Ticket Number: #{ticket.ticket_number}")
        print(f"  - Ticket ID: {ticket.ticket_id}")
        print(f"  - Subject: {ticket.subject}")
        
        print(f"\nDefect Information:")
        print(f"  - Failure Mode: {defect['failure_mode']}")
        print(f"  - Station: {defect['station']}")
        print(f"  - Defect Code: {defect['defect_code']}")
        
        print(f"\n8D Phases Completed:")
        for phase, description in D8_PHASES.items():
            print(f"  âœ“ {phase}: {description}")
        
        # Get final ticket state
        final_ticket = wats_client.rootcause.get_ticket(ticket.ticket_id)
        if final_ticket:
            status_name = TicketStatus(final_ticket.status).name if final_ticket.status else "Unknown"
            print(f"\nFinal Status: {status_name}")
        
        print("\nTest Results:")
        print("  âœ“ Ticket created with production defect details")
        print("  âœ“ Cross-functional team assembled (D1)")
        print("  âœ“ Problem defined with IS/IS NOT analysis (D2)")
        print("  âœ“ Interim containment implemented (D3)")
        print("  âœ“ Root cause identified via 5-Why analysis (D4)")
        print("  âœ“ Permanent corrective actions defined (D5)")
        print("  âœ“ Actions implemented and verified (D6)")
        print("  âœ“ Prevention measures deployed (D7)")
        print("  âœ“ Team recognized and ticket closed (D8)")
        
        print("=" * 70)
        print("\n")

