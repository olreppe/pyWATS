# TEMPLATE Domain Status

> Replace `TEMPLATE` with the module name when duplicating this file (e.g. `REPORT_DOMAIN_STATUS.md`).

## 1. Service Functions
- **Overview:** Describe the domain service(s) serving this module.
- **Key Operations:** List major methods/their intent and highlights from business logic.
- **Open Questions:** Any ambiguity in responsibilities or missing guards.

## 2. Model Surface
- **Model Files:** Enumerate the files defining Pydantic/base models.
- **Class Summary:** Highlight each major class, intent, and relationships (inheritance/composition).
- **Model Quality Notes:** Size concerns, duplication, nested scopes, test coverage gaps, or split opportunities.

## 3. Architecture & Diagrams
- **Class Relationships:** Provide a high-level class diagram or bullet outline of key connections.
- **Refactor Ideas:** Consider splitting oversized modules, isolating model directories, or introducing submodules.

## 4. Inline Documentation
- **Domain Knowledge Additions:** Mention where more context or clarifications were added or should be added.
- **Doc Gaps:** Identify missing docstrings, confusing terminology, or assumptions needing explicit mention.

## 5. Acceptance Testing
- **Test Scenarios:** List consumer-visible flows that should be covered by acceptance tests.
- **Data Setup Notes:** Outline required fixtures, sample data, or environment prep for reliable runs.
- **Verification Steps:** Describe what constitutes success for each scenario.

## 6. Pending Work
- **Next Steps:** One-line reminders for follow-up actions (tests to write, modules to split, docs to update).
- **Blockers:** Any missing context, approvals, or external dependencies.
