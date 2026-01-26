# Electronics test/repair log formats & standards scan (Jan 2026)

This document summarizes **common log/result formats** from off‑the‑shelf electronics test equipment and **relevant standards** that can help a Test & Repair Data Management platform integrate broadly across factories.

> Scope: AOI / SPI / AXI, ICT & flying probe, functional test, boundary scan, burn‑in & reliability stress, and manual inspection/repair.

---

## 1) Key takeaway

There is **no single universal log format** across all PCB/PCBA test and inspection domains.

Instead, you typically combine:

1. **Equipment connectivity/event standard** (for shop‑floor integration): *IPC‑CFX (IPC‑2591)*  
2. **Test results interchange standard** (especially for ATE / formal test systems): *IEEE ATML / IEEE 1636.1*  
3. **Domain‑specific de‑facto standards**:
   - Semiconductor ATE results: *STDF / ATDF*
   - Boundary scan: *IEEE 1149.1 / 1149.6* (data often vendor‑specific, but test *protocols* standardized)
   - Substrate/wafer mapping & host comms: *SEMI E142 + SECS/GEM ecosystem*
4. **Vendor report formats** (CSV/XML/TXT/DB) for the rest.

Your platform should treat those as **ingestion/export protocols**, mapping everything into a **canonical test/repair data model**.

---

## 2) IPC‑CFX (IPC‑2591) – the “connect production equipment” layer

**What it’s good for**
- Standardized **event messages** from equipment for line integration (state, activity, faults, counts, etc.).
- Increasingly adopted by inspection vendors (AOI/SPI/AXI) as an integration interface.

**Reality check**
- CFX is primarily an equipment connectivity/event layer, **not** a deep measurement schema for every tester’s result detail.

**Useful hint**
- Some industry discussions highlight CFX “attachments” for SPI/AOI measurement payloads, but implementations vary by vendor.

References:
- About CFX / IPC‑2591: https://www.electronics.org/about-cfx-global-standard-smart-manufacturing-enablement
- Example AOI/SPI/AXI vendor support: https://www.viscom.com/en/products/ipc-cfx/
- Example inspection vendor announcement: https://www.goepel.com/en/news/read/inspection-solutions-with-ipc-cfx-standard

---

## 3) Off‑the‑shelf equipment formats (examples you asked for)

### 3.1 Keysight (examples)
**Keysight i3070 ICT**
- Outputs **text log files** per board; Keysight provides a document describing the **log record format**.
- Reference: https://www.keysight.com/us/en/assets/9018-07549/user-manuals/9018-07549.pdf

**Keysight TestExec SL (functional test executive)**
- Data logging defaults to **XML files** (customizable) that can be imported into databases.
- Reference: https://www.keysight.com/us/en/assets/7018-02229/application-notes/5990-4367.pdf

### 3.2 Teradyne (examples)
**Semiconductor ATE heritage → STDF**
- STDF originated with Teradyne and is widely used as a **de‑facto** semiconductor test datalog format.
- Reference overview: https://en.wikipedia.org/wiki/Standard_Test_Data_Format  
- Example STDF spec copy found online: https://www.kanwoda.com/wp-content/uploads/2015/05/std-spec.pdf

**ICT / board test (TestStation family)**
- Teradyne board test environments have their own program/data tooling; **result exports are often configurable** and commonly integrate via MES/DB interfaces, but a single public “universal Teradyne ICT log standard” is not commonly published.
- Product family context: https://www.teradyne.com/applications/in-circuit-testing/

**Boundary scan**
- Teradyne’s boundary scan tooling references IEEE boundary scan standards (1149.1 / 1149.6).
- Reference: https://www.teradyne.com/scan-pathfinder-ii-faq/

### 3.3 Seica (examples)
Seica documentation commonly discusses **test program preparation/export packages** used by their software ecosystem.
- Example “Seica export” package for creating test programs: https://manual.pcb-investigator.com/posts/Seica_Export

> Note: For Seica (and many flying probe/ICT vendors), **program inputs** often rely on design/manufacturing data packages (ODB++ / IPC‑2581), while **results logs** are frequently vendor‑specific (CSV/TXT/DB/XML) and/or integrated via MES interfaces or CFX where supported.

---

## 4) Other standards worth considering for your platform

### 4.1 IEEE ATML (Automatic Test Markup Language) – a real “test information interchange” family
ATML is a family of **XML schemas** aimed at exchanging test descriptions, instruments, UUT descriptions, and **test results** across ATE ecosystems.

Why you should care:
- If you want a “portable” way to represent **test results and associated context** beyond any single vendor, ATML is one of the closest things to an “official” standard.

References:
- NI overview referencing IEEE 1671 framework and “dot” standards: https://www.ni.com/docs/en-US/bundle/teststand-atml-toolkit/page/atml-td-standards-146.html
- IEEE 1671.1 page (Test Descriptions): https://standards.ieee.org/ieee/1671.1/4928/
- ATML background (secondary): https://en.wikipedia.org/wiki/ATML

### 4.2 STDF / ATDF – semiconductor ATE results (high value if you touch IC test)
- **STDF** (binary) + **ATDF** (ASCII conversion) are widely used for semiconductor ATE logs and yield analytics.
- If you plan to ingest device‑level IC test, this is essential.

References:
- STDF overview: https://en.wikipedia.org/wiki/Standard_Test_Data_Format

### 4.3 SEMI standards for substrate mapping / equipment interfaces (semiconductor fabs)
- SEMI E142 defines **substrate/wafer map** data exchange via the SEMI SECS/GEM ecosystem.

References:
- SEMI E142 overview article (secondary): https://www.semi.org/en/standards-watch-2020Sept/revision-to-semi-e142

### 4.4 QIF (Quality Information Framework) – inspection/metrology result exchange
Not electronics-test-specific, but relevant when you want a **standard for measurement/inspection results**, characteristics, and traceability links.

References:
- QIF overview: https://qifstandards.org/overview/

### 4.5 Design/manufacturing data packages that influence test generation
These are not “test logs” but drive **test program creation** and traceability:
- **IPC‑2581**: open XML design-to-manufacturing exchange (often includes test‑relevant info like netlists and variants).
- **ODB++**: widely used manufacturing package (vendor-controlled), often used for AOI/SPI programming inputs and some flying probe workflows.

---

## 5) What exists (and what doesn’t) by process type

### AOI / SPI / AXI
- **Connectivity/event integration:** increasingly **IPC‑CFX** (vendor-dependent).
- **Result files:** often **CSV/XML/proprietary DB**, sometimes with “defect images” and measurement attachments.

### ICT / Flying probe
- **Program inputs:** ODB++ / IPC‑2581 / netlists, plus vendor-specific recipe/program structures.
- **Result files:** often text logs, CSV, proprietary exports. Example: Keysight i3070 has documented text log record format.

### Functional test (ATE-lite to full ATE)
- **Test executives:** frequently produce XML/CSV/HTML reports (e.g., TestExec SL XML logging).
- **Formal ATE interchange:** ATML is the closest “standard family”.

### Boundary scan
- **Protocols/structures standardized:** IEEE 1149.x family.
- **Logs/results:** typically vendor-specific, but mapping to canonical “boundary scan results” is straightforward.

### Burn-in / reliability / stress testing
- **Test methods & qualification standards exist** (JEDEC/IEC/MIL families), but log formats are usually bespoke (equipment + lab system).
- Treat as “environmental profile + periodic measurements + disposition”.

### Manual inspection & repair
- Rarely standardized logs.
- Best practice is to implement a **structured repair/inspection schema** (symptom, cause, action, part replaced, time, operator, photos, references) and then map any external systems into it.

---

## 6) Practical integration strategy for your platform

### Step A — define your canonical model (don’t start with vendor formats)
Create a **canonical “Test/Repair Event + Measurement”** model:
- identity (product/UUT/serial), revision, configuration
- station/resource, operator, time, work order/route/step
- result summaries (pass/fail, codes, disposition)
- measurements (name, units, value, limits, uncertainty)
- attachments (images/waveforms/log blobs)
- traceability links (consumed parts/tools/fixtures/software versions)

### Step B — implement 3 connector classes
1. **CFX ingestion/export connector** (factory events)
2. **ATML/STDF ingestion** (where relevant)
3. **Vendor report connectors** (Keysight i3070 logs, TestExec SL XML, etc.)

### Step C — stabilize your IDs and versioning
Your biggest future cost isn’t parsing files; it’s identity:
- stable serial/UID mapping
- product + revision + variant
- tester/station/fixture/tool calibration identity
- test program + software version identity

---

## 7) Suggested next research/POC targets
If you want quick learning with real data:
1. Ingest **Keysight i3070 log record** sample and map to your canonical model.
2. Ingest **TestExec SL XML** sample.
3. Implement a minimal **CFX event ingestion** pipeline (even if just for station state + start/complete).
4. Add an **STDF parser** only if semiconductor device testing is in-scope.

---

## References (URLs)
- IPC‑CFX / IPC‑2591: https://www.electronics.org/about-cfx-global-standard-smart-manufacturing-enablement
- Viscom IPC‑CFX: https://www.viscom.com/en/products/ipc-cfx/
- Göpel IPC‑CFX: https://www.goepel.com/en/news/read/inspection-solutions-with-ipc-cfx-standard
- Keysight i3070 log record format: https://www.keysight.com/us/en/assets/9018-07549/user-manuals/9018-07549.pdf
- Keysight TestExec SL XML logging note: https://www.keysight.com/us/en/assets/7018-02229/application-notes/5990-4367.pdf
- STDF overview: https://en.wikipedia.org/wiki/Standard_Test_Data_Format
- Teradyne ICT overview: https://www.teradyne.com/applications/in-circuit-testing/
- Teradyne boundary scan standards: https://www.teradyne.com/scan-pathfinder-ii-faq/
- ATML & IEEE 1671 info: https://www.ni.com/docs/en-US/bundle/teststand-atml-toolkit/page/atml-td-standards-146.html
- IEEE 1671.1 page: https://standards.ieee.org/ieee/1671.1/4928/
- QIF overview: https://qifstandards.org/overview/
- Seica export package example: https://manual.pcb-investigator.com/posts/Seica_Export
