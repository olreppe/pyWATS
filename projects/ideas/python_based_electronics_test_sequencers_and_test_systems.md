# Python-Based Electronics Test Sequencers and Test Systems

This document lists **notable electronics test sequencers and test systems** that are either **Python-based** or **support Python as a first-class integration language**. 

> **NI products (TestStand, LabVIEW ecosystems)** have been intentionally excluded, as requested.

The list is split into **Open Source** and **Commercial** systems, with notes on maturity and typical usage.

---

## 1. Open Source – Python-Based

### Flojoy Studio
- **Type:** GUI test sequencer / test executive
- **Language:** Python (core + user tests)
- **License:** Open source (GPL-style)
- **Description:**
  Flojoy Studio is one of the few modern, open-source attempts at a **TestStand-like** environment using Python. It provides a graphical flow editor, hardware nodes, and execution engine, while allowing Python scripts, pytest tests, and Robot Framework tests to be embedded.
- **Strengths:**
  - Operator-facing UI
  - Visual sequencing
  - Python-first
- **Limitations:**
  - Younger ecosystem
  - Rapid evolution; APIs may change

---

### OpenHTF (Open Hardware Testing Framework)
- **Type:** Code-first test execution framework
- **Language:** Python
- **License:** Apache 2.0
- **Origin:** Google (manufacturing test)
- **Description:**
  OpenHTF is a mature Python framework for building **structured hardware tests**. It provides phases/steps, measurements, limits, attachments, and standardized test records, but deliberately avoids defining a UI or flow editor.
- **Strengths:**
  - Proven in real manufacturing environments
  - Clean execution model
  - Excellent data model
- **Limitations:**
  - No built-in operator UI
  - Sequencing is code-defined, not graphical

---

### ATE (Python package)
- **Type:** Lightweight test sequence executor / template
- **Language:** Python
- **License:** Open source
- **Description:**
  ATE is a small Python-based test execution framework aimed at building manufacturing or validation test systems. It focuses on test flow execution and logging, leaving UI and infrastructure decisions to the integrator.
- **Strengths:**
  - Simple and lightweight
  - Easy to embed
- **Limitations:**
  - Small community
  - Minimal tooling around sequencing and reporting

---

### pytest-based Hardware Test Systems (Ecosystem Pattern)
- **Type:** Code-first execution engine
- **Language:** Python
- **License:** Open source (pytest)
- **Description:**
  While pytest is not a test sequencer by itself, it is widely used as the **de facto Python test runner** in electronics manufacturing and validation. Many companies layer fixtures, hardware abstractions, station control, and reporting on top of pytest to create full ATE systems.
- **Strengths:**
  - Extremely mature
  - Massive ecosystem
  - Easy CI/CD integration
- **Limitations:**
  - No built-in operator UI
  - Sequencing is implicit via code structure

---

### Robot Framework (Hardware Usage)
- **Type:** Keyword-driven test framework
- **Language:** Python (core + libraries)
- **License:** Apache 2.0
- **Description:**
  Robot Framework is sometimes used in electronics testing when a **keyword-driven**, semi-graphical or tabular test definition is desired. Hardware access is typically implemented via Python libraries.
- **Strengths:**
  - Readable test definitions
  - Non-programmer-friendly
- **Limitations:**
  - Less natural for complex hardware state management
  - Not manufacturing-focused by default

---

## 2. Commercial Systems (Python-Supported)

### OpenTAP (Core is .NET, Python Supported)
- **Type:** Modular test sequencer / test executive
- **Language:** .NET core, **Python supported via SDK/plugins**
- **License:** Open source core (MPL 2.0)
- **Description:**
  OpenTAP is a modular, plugin-based test sequencer originally developed by Keysight. While the core is .NET, Python is supported for test step development via SDKs and plugins.
- **Strengths:**
  - Strong sequencing model
  - Plugin architecture
- **Limitations:**
  - Python is not the native language

---

### Keysight PathWave Test Automation (PWTA)
- **Type:** Commercial test executive built on OpenTAP
- **Language:** .NET core, Python SDK supported
- **Description:**
  PWTA is Keysight’s commercial packaging of OpenTAP with enterprise features, installers, and support. Python is supported for test development, but the platform itself is not Python-native.
- **Strengths:**
  - Industrial-grade tooling
  - Vendor-backed support
- **Limitations:**
  - Commercial licensing
  - Still fundamentally OpenTAP/.NET

---

### Rohde & Schwarz QuickStep
- **Type:** Commercial test executive / sequencer
- **Language:** Native environment with **Python-based test function support**
- **Description:**
  QuickStep is a full test executive aimed at production and validation environments. It provides sequencing, reporting, and execution control, with the ability to develop custom test functions in Python.
- **Strengths:**
  - Traditional test executive features
  - Python supported for test logic
- **Limitations:**
  - Commercial and vendor-centric
  - Python is an extension language, not the core

---

### JTAG Technologies ProVision
- **Type:** Production test environment (boundary-scan focused)
- **Language:** Python extensibility
- **Description:**
  ProVision is a production test platform primarily focused on boundary-scan and structural test, with scripting and extensibility options including Python for custom logic.
- **Strengths:**
  - Strong in PCB/structural test
  - Integrated sequencing
- **Limitations:**
  - Domain-specific
  - Not Python-first

---

## 3. Summary View

| Category | Python-First | GUI Sequencer | Production-Proven |
|--------|-------------|---------------|-------------------|
| Flojoy Studio | Yes | Yes | Emerging |
| OpenHTF | Yes | No | Yes |
| pytest-based systems | Yes | No | Yes |
| Robot Framework | Yes | Limited | Mixed |
| OpenTAP / PWTA | Partial | Yes | Yes |
| R&S QuickStep | Partial | Yes | Yes |

---

## 4. Practical Takeaway

- **If you want a Python-native execution engine:** OpenHTF or pytest-based systems
- **If you want a TestStand-like GUI without NI:** Flojoy Studio or OpenTAP-based systems
- **If you want vendor-backed production tooling with Python hooks:** QuickStep or PWTA

This landscape strongly suggests that **Python excels as a test execution language**, but true **Python-native graphical test sequencers remain rare**, which explains why many teams build custom systems on top of OpenHTF or pytest.
