# AI Chat Pilot - Requirements Placeholder

**Status:** 🔜 Awaiting user input  
**Application:** pyWATS AI Chat (LLM-powered test data analysis)

---

## 📋 Overview

LLM-powered application for analyzing manufacturing test data with natural language interface. Users can ask questions about test results, process capability, SPC violations, and root causes using plain English.

---

## 🎯 Core Features (To Be Detailed)

### 1. Process Capability Analysis
- Cp, Cpk, Pp, Ppk calculations
- Capability histograms with spec limits
- Sigma level analysis
- **User to provide:** Specific capability requirements, target Cpk values

### 2. Statistical Process Control (SPC)
- Control charts (X-bar, R, I-MR)
- Control limit calculations (UCL, LCL)
- Violation detection (Western Electric rules)
- Trend analysis
- **User to provide:** SPC rules to implement, chart preferences

### 3. Root Cause Analysis (RCA)
- LLM-powered failure pattern recognition
- Correlation analysis across parameters
- Suggested root causes with confidence scores
- Historical failure comparisons
- **User to provide:** RCA methodology, prompt engineering guidance

### 4. Interactive Chat Interface
- Natural language queries ("What's the Cpk for ICT over last week?")
- Conversation context (remembers previous queries)
- Data visualization in chat (embedded charts)
- Export results (PDF, CSV, images)
- **User to provide:** Example queries, UI preferences

---

## 🔌 LLM Integration (To Be Specified)

### LLM Provider Options
- **OpenAI (GPT-4):** High quality, API-based, requires key
- **Anthropic (Claude):** Alternative API provider
- **Local models:** llama.cpp, Ollama (privacy, no API costs)
- **Azure OpenAI:** Enterprise option

**User to provide:**
- Preferred LLM provider
- API key management strategy
- Budget considerations (API costs)
- Privacy requirements (local vs cloud)

---

## 📊 Data Sources

### pyWATS Analytics APIs
- `api.analytics.get_yield_statistics()` - Yield data
- `api.analytics.get_measurement_statistics()` - Measurement values
- `api.report.get_reports()` - Raw test reports
- `api.analytics.get_alarm_history()` - Alarm data

**User to provide:**
- Specific data points to analyze
- Time ranges for analysis (last hour, day, week)
- Products/processes to focus on

---

## 🎨 User Interface (To Be Designed)

### Chat Window Layout
```
┌─────────────────────────────────────────────┐
│ 🤖 pyWATS AI Chat                  [Theme] │
├─────────────────────────────────────────────┤
│ Chat History                                │
│ ┌─────────────────────────────────────────┐ │
│ │ User: What's the Cpk for ICT?           │ │
│ │                                         │ │
│ │ AI: The Cpk for ICT process over the   │ │
│ │     last 100 units is 1.45.             │ │
│ │     [Chart: Capability Histogram]       │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Input: [Type your question...]   [Send]    │
│                                             │
│ Quick Actions:                              │
│ [Analyze Last 100] [SPC Check] [RCA]       │
└─────────────────────────────────────────────┘
```

**User to provide:**
- UI preferences (chat style, layout)
- Quick action buttons needed
- Visualization preferences

---

## 🔒 Security & Privacy

**Considerations:**
- API key secure storage (not in code)
- Data anonymization before sending to LLM?
- Local LLM option for sensitive data
- Audit logging (what queries were made)

**User to provide:**
- Privacy requirements
- Compliance considerations (GDPR, etc.)
- Data sharing policies

---

## 🧪 Example Use Cases (To Be Expanded)

### Use Case 1: Quick Capability Check
**User:** "What's the Cpk for resistor R23 on ICT?"  
**AI:** "Cpk for R23 (ICT) = 1.67 over last 200 units. Process is capable."  
**Chart:** Histogram with spec limits

### Use Case 2: SPC Violation Alert
**User:** "Any SPC violations in the last shift?"  
**AI:** "3 violations detected on FCT process. 2 points above UCL on temperature sensor."  
**Chart:** Control chart with violations highlighted

### Use Case 3: Root Cause Analysis
**User:** "Why did we have 10 failures on connector test?"  
**AI:** "Analysis suggests correlation with solder temperature. 8/10 failures had temp >245°C."  
**Action:** Shows temperature distribution, suggests temp adjustment

**User to provide:**
- Additional use cases
- Specific prompt examples
- Expected AI responses

---

## 📦 Dependencies (Estimated)

```toml
[project.optional-dependencies]
gui = [
    "PySide6>=6.6.0",
    "openai>=1.0.0",          # If using OpenAI
    "anthropic>=0.8.0",       # If using Anthropic
    # ... other LLM providers
]
```

**User to provide:**
- Specific LLM library preferences
- Version constraints

---

## ⏱️ Timeline

- **Week 1:** LLM integration research, provider selection
- **Week 2-3:** Framework + Configurator (parallel work)
- **Week 4:** AI Chat implementation (UI + LLM + Analytics)
- **Week 5:** Testing and documentation

**User to provide:**
- Deadline constraints
- Priority features (MVP vs full implementation)

---

## 📝 Open Questions for User

1. **LLM Provider:** OpenAI GPT-4, Anthropic Claude, local model, or multiple?
2. **Capability Analysis:** Standard Cp/Cpk or custom formulas?
3. **SPC Rules:** Western Electric rules, Nelson rules, or custom?
4. **RCA Methodology:** Specific RCA framework to follow?
5. **UI Preferences:** Chat-style, tabbed interface, or something else?
6. **Privacy:** Can test data be sent to cloud LLMs or must stay local?
7. **Budget:** API costs acceptable or need local model?
8. **Example Queries:** What questions should users be able to ask?

---

**Status:** 🔜 Waiting for user input on requirements  
**Next Step:** User provides details, then begin Phase 0 research
