# IPC-CFX, Electronics Test Logs, and Asset Integration for WATS

> Expanded reference document – IPC-CFX, electronics test/inspection log formats, and asset integration  
> Generated: Jan 2026

---

## 1. Scope and intent

This document serves three purposes:

1. Provide a reference scan of test / inspection / repair log formats used in electronics manufacturing (ATE, ICT, AOI, SPI, functional test, burn-in, manual inspection).
2. Summarize relevant standards (official and de‑facto) that can be leveraged by a Test Data Management platform.
3. Elaborate in detail on IPC‑CFX (IPC‑2591) as a mechanism to connect production equipment and instruments to a WATS Asset Manager.

---

## 2. IPC‑CFX (IPC‑2591) – overview and official references

### Official references

- IPC‑2591 overview: https://www.electronics.org/ipc-2591-connected-factory-exchange-cfx
- Mandatory & optional message capabilities (PDF): https://www.electronics.org/media/4944/download
- IPC‑CFX self‑validation system: https://www.electronics.org/ipc-cfx-equipment-self-validation-system
- Certification directory: https://certification.connectedfactoryexchange.com/certification-directory

---

## 3. IPC‑CFX as an asset integration layer

### Asset identity
CFX resource identifiers map to canonical WATS asset IDs.

### Calibration & maintenance
CFX provides state/fault signals; WATS owns schedules and policies.

### Usage tracking
Start/stop and throughput events feed asset utilization analytics.

### Alarms
CFX fault/clear messages become asset health events.

---

## 4. Electronics test & inspection log formats

### Semiconductor ATE
- STDF: https://en.wikipedia.org/wiki/Standard_Test_Data_Format

### Automated Test Markup Language
- ATML: https://www.ni.com/docs/en-US/bundle/teststand-atml-toolkit/page/atml-td-standards-146.html

### ICT example
- Keysight i3070 log format: https://www.keysight.com/us/en/assets/9018-07549/user-manuals/9018-07549.pdf

### Functional test
- TestExec SL XML logging: https://www.keysight.com/us/en/assets/7018-02229/application-notes/5990-4367.pdf

---

End of document.
