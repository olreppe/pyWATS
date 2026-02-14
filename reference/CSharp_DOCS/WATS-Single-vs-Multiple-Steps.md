# WATS Single vs Multiple Test Steps

## Critical Distinction: Single Test Steps vs Multiple Test Steps

This document explains the **critical difference** between **Single** and **Multiple** test steps in WATS UUT reports.

---

## Table of Contents

1. [Overview](#1-overview)
2. [The Fundamental Rule](#2-the-fundamental-rule)
3. [NumericLimitStep](#3-numericlimitstep)
4. [PassFailStep](#4-passfailstep)
5. [StringValueStep](#5-stringvaluestep)
6. [Common Mistakes](#6-common-mistakes)
7. [Complete Examples](#7-complete-examples)
8. [Migration Guide](#8-migration-guide)

---

## 1. Overview

### What's the Difference?

In WATS, test steps can contain **one** or **multiple** measurements. The API enforces this distinction strictly:

| Aspect | Single Test Step | Multiple Test Step |
|--------|------------------|-------------------|
| **Purpose** | One measurement per step | Multiple measurements per step |
| **Method** | `AddTest()` | `AddMultipleTest()` |
| **Step Type** | `ET_NLT`, `ET_PFT`, `ET_SVT` | `ET_MNLT`, `ET_MPFT`, `ET_MSVT` |
| **Measurement Name** | Not used (empty) | Required for each test |
| **First Call** | Locks step as Single | Locks step as Multiple |
| **Mixing** | ? **FORBIDDEN** | ? **FORBIDDEN** |

### Why It Matters

```csharp
// ? THIS WILL THROW AN EXCEPTION
NumericLimitStep step = root.AddNumericLimitStep("Voltage Test");
step.AddTest(3.3, "V");                        // Locks as SINGLE
step.AddMultipleTest(5.0, "V", "5V Rail");     // ? THROWS InvalidOperationException

// ? CORRECT - Use AddMultipleTest from the start
NumericLimitStep step = root.AddNumericLimitStep("Voltage Test");
step.AddMultipleTest(3.3, "V", "3.3V Rail");   // Locks as MULTIPLE
step.AddMultipleTest(5.0, "V", "5V Rail");     // ? OK
step.AddMultipleTest(12.0, "V", "12V Rail");   // ? OK
```

---

## 2. The Fundamental Rule

### Once Locked, Cannot Change

```csharp
NumericLimitStep step = root.AddNumericLimitStep("Test");

// First call determines the mode
step.AddTest(100, "V");  // ? This locks it as SINGLE

// Now you CANNOT add multiple tests
step.AddMultipleTest(200, "V", "Test2");  // ? THROWS InvalidOperationException:
                                          //    "Cannot add multiple test to single test step."
```

### The Lock Happens On First Add

```csharp
// This is a virgin step - mode not determined yet
NumericLimitStep step = root.AddNumericLimitStep("Voltage Rails");

// Option 1: Lock as SINGLE
step.AddTest(3.3, "V");  
// Step is now SINGLE - cannot add more tests

// Option 2: Lock as MULTIPLE
step.AddMultipleTest(3.3, "V", "3.3V");
step.AddMultipleTest(5.0, "V", "5V");
// Step is now MULTIPLE - can add more tests
```

---

## 3. NumericLimitStep

### 3.1 Single Numeric Limit Step

**Use When:** You have ONE measurement in this step.

```csharp
// ? CORRECT - Single test
NumericLimitStep step = root.AddNumericLimitStep("3.3V Voltage");

step.AddTest(
    numericValue: 3.32,
    compOperator: CompOperatorType.GELE,
    lowLimit: 3.20,
    highLimit: 3.40,
    units: "V"
);

// Internal step type: ET_NLT (Numeric Limit Test)
```

**Properties:**
- Step has ONE test
- Test has no `MeasureName`
- Step type: `ET_NLT`
- Single test directly represents step result

### 3.2 Multiple Numeric Limit Step

**Use When:** You have MULTIPLE measurements in this step.

```csharp
// ? CORRECT - Multiple tests
NumericLimitStep step = root.AddNumericLimitStep("Power Supply Voltages");

// First call locks it as MULTIPLE
step.AddMultipleTest(
    numericValue: 3.32,
    compOperator: CompOperatorType.GELE,
    lowLimit: 3.20,
    highLimit: 3.40,
    units: "V",
    measureName: "3.3V Rail"  // ? measureName required!
);

step.AddMultipleTest(5.05, CompOperatorType.GELE, 4.90, 5.10, "V", "5V Rail");
step.AddMultipleTest(12.1, CompOperatorType.GELE, 11.8, 12.2, "V", "12V Rail");
step.AddMultipleTest(-12.0, CompOperatorType.GELE, -12.2, -11.8, "V", "-12V Rail");

// Internal step type: ET_MNLT (Multiple Numeric Limit Test)
```

**Properties:**
- Step has MULTIPLE tests
- Each test has a unique `MeasureName`
- Step type: `ET_MNLT`
- Step result is aggregate of all tests

### 3.3 AddTest() vs AddMultipleTest()

#### AddTest() - Single Mode

```csharp
// Signature variants (8 overloads)
NumericLimitTest AddTest(double value, CompOperatorType op, double low, double high, string units)
NumericLimitTest AddTest(double value, CompOperatorType op, double low, double high, string units, StepStatusType status)
NumericLimitTest AddTest(double value, CompOperatorType op, double limit, string units)
NumericLimitTest AddTest(double value, CompOperatorType op, double limit, string units, StepStatusType status)
NumericLimitTest AddTest(double value, string units)  // LOG mode
NumericLimitTest AddTest(double value, string units, StepStatusType status)

// NO measureName parameter!
```

#### AddMultipleTest() - Multiple Mode

```csharp
// Signature variants (8 overloads)
NumericLimitTest AddMultipleTest(double value, CompOperatorType op, double low, double high, string units, string measureName)
NumericLimitTest AddMultipleTest(double value, CompOperatorType op, double low, double high, string units, string measureName, StepStatusType status)
NumericLimitTest AddMultipleTest(double value, CompOperatorType op, double limit, string units, string measureName)
NumericLimitTest AddMultipleTest(double value, CompOperatorType op, double limit, string units, string measureName, StepStatusType status)
NumericLimitTest AddMultipleTest(double value, string units, string measureName)  // LOG mode
NumericLimitTest AddMultipleTest(double value, string units, string measureName, StepStatusType status)

// measureName parameter REQUIRED!
```

---

## 4. PassFailStep

### 4.1 Single Pass/Fail Step

```csharp
// ? CORRECT - Single test
PassFailStep step = root.AddPassFailStep("Power On Self Test");

step.AddTest(passed: true);

// Internal step type: ET_PFT (Pass Fail Test)
```

### 4.2 Multiple Pass/Fail Step

```csharp
// ? CORRECT - Multiple tests
PassFailStep step = root.AddPassFailStep("Built-In Self Tests");

step.AddMultipleTest(passed: true, measureName: "RAM Test");
step.AddMultipleTest(passed: true, measureName: "Flash Test");
step.AddMultipleTest(passed: false, measureName: "EEPROM Test");
step.AddMultipleTest(passed: true, measureName: "Watchdog Test");

// Internal step type: ET_MPFT (Multiple Pass Fail Test)
```

### 4.3 Method Signatures

```csharp
// Single mode
PassFailTest AddTest(bool passed)
PassFailTest AddTest(bool passed, StepStatusType status)

// Multiple mode
PassFailTest AddMultipleTest(bool passed, string measureName)
PassFailTest AddMultipleTest(bool passed, string measureName, StepStatusType status)
```

---

## 5. StringValueStep

### 5.1 Single String Value Step

```csharp
// ? CORRECT - Single test
StringValueStep step = root.AddStringValueStep("Firmware Version");

step.AddTest(
    compOperator: CompOperatorType.CASESENSIT,
    stringValue: "v2.5.1",
    expectedValue: "v2.5.1"
);

// Internal step type: ET_SVT (String Value Test)
```

### 5.2 Multiple String Value Step

```csharp
// ? CORRECT - Multiple tests
StringValueStep step = root.AddStringValueStep("Configuration Check");

step.AddMultipleTest(
    compOperator: CompOperatorType.IGNORECASE,
    stringValue: "enabled",
    expectedValue: "enabled",
    measureName: "WiFi Status"
);

step.AddMultipleTest(
    CompOperatorType.CASESENSIT,
    "00:11:22:33:44:55",
    "00:11:22:33:44:55",
    "MAC Address"
);

step.AddMultipleTest(
    CompOperatorType.IGNORECASE,
    "192.168.1.100",
    "192.168.1.100",
    "IP Address"
);

// Internal step type: ET_MSVT (Multiple String Value Test)
```

### 5.3 Method Signatures

```csharp
// Single mode
StringValueTest AddTest(string value)
StringValueTest AddTest(CompOperatorType op, string value, string expected)
StringValueTest AddTest(CompOperatorType op, string value, string expected, StepStatusType status)

// Multiple mode
StringValueTest AddMultipleTest(string value, string measureName)
StringValueTest AddMultipleTest(CompOperatorType op, string value, string expected, string measureName)
StringValueTest AddMultipleTest(CompOperatorType op, string value, string expected, string measureName, StepStatusType status)
```

---

## 6. Common Mistakes

### Mistake 1: Mixing Single and Multiple

```csharp
// ? WRONG - This will crash
NumericLimitStep step = root.AddNumericLimitStep("Voltages");
step.AddTest(3.3, "V");                         // Locks as SINGLE
step.AddMultipleTest(5.0, "V", "5V Rail");      // ? THROWS InvalidOperationException

// ? CORRECT - Choose one approach
NumericLimitStep step = root.AddNumericLimitStep("Voltages");
step.AddMultipleTest(3.3, "V", "3.3V Rail");    // Locks as MULTIPLE
step.AddMultipleTest(5.0, "V", "5V Rail");      // ? OK
```

### Mistake 2: Adding Multiple Single Tests

```csharp
// ? WRONG - Cannot add second single test
NumericLimitStep step = root.AddNumericLimitStep("Test");
step.AddTest(100, "V");     // First single test
step.AddTest(200, "V");     // ? THROWS: "Cannot add multiple single tests to single test step."

// ? CORRECT - Use AddMultipleTest
NumericLimitStep step = root.AddNumericLimitStep("Test");
step.AddMultipleTest(100, "V", "Test 1");
step.AddMultipleTest(200, "V", "Test 2");
```

### Mistake 3: Forgetting MeasureName

```csharp
// ? WRONG - measureName is required for multiple tests
step.AddMultipleTest(3.3, "V", "");  // Empty string might work but bad practice

// ? CORRECT - Provide meaningful names
step.AddMultipleTest(3.3, "V", "3.3V Rail");
step.AddMultipleTest(5.0, "V", "5V Rail");
```

### Mistake 4: Not Planning Ahead

```csharp
// ? POOR DESIGN - Realized too late you need multiple tests
NumericLimitStep step = root.AddNumericLimitStep("Voltage");
step.AddTest(3.3, "V");  // Oops, now I can't add the 5V test!

// ? GOOD DESIGN - Plan your test structure
// If you might add more measurements, use Multiple from the start
NumericLimitStep step = root.AddNumericLimitStep("Voltage Rails");
step.AddMultipleTest(3.3, "V", "3.3V");
// Can add more later if needed
```

---

## 7. Complete Examples

### Example 1: Single Test Per Step

```csharp
using Virinco.WATS.Interface;
using System;

// When each measurement deserves its own step
SequenceCall powerTests = root.AddSequenceCall("Power Supply Tests");

// Each voltage is a separate step with single test
NumericLimitStep v33 = powerTests.AddNumericLimitStep("3.3V Rail");
v33.AddTest(3.32, CompOperatorType.GELE, 3.20, 3.40, "V");

NumericLimitStep v5 = powerTests.AddNumericLimitStep("5V Rail");
v5.AddTest(5.05, CompOperatorType.GELE, 4.90, 5.10, "V");

NumericLimitStep v12 = powerTests.AddNumericLimitStep("12V Rail");
v12.AddTest(12.1, CompOperatorType.GELE, 11.8, 12.2, "V");

/* Result hierarchy:
Power Supply Tests
??? 3.3V Rail (Pass)
?   ??? [Test] 3.32V
??? 5V Rail (Pass)
?   ??? [Test] 5.05V
??? 12V Rail (Pass)
    ??? [Test] 12.1V
*/
```

### Example 2: Multiple Tests in One Step

```csharp
using Virinco.WATS.Interface;
using System;

// When measurements are logically grouped
SequenceCall powerTests = root.AddSequenceCall("Power Supply Tests");

NumericLimitStep voltages = powerTests.AddNumericLimitStep("Voltage Rails");

// All voltage measurements in one step
voltages.AddMultipleTest(3.32, CompOperatorType.GELE, 3.20, 3.40, "V", "3.3V Rail");
voltages.AddMultipleTest(5.05, CompOperatorType.GELE, 4.90, 5.10, "V", "5V Rail");
voltages.AddMultipleTest(12.1, CompOperatorType.GELE, 11.8, 12.2, "V", "12V Rail");
voltages.AddMultipleTest(-12.0, CompOperatorType.GELE, -12.2, -11.8, "V", "-12V Rail");

/* Result hierarchy:
Power Supply Tests
??? Voltage Rails (Pass)
    ??? 3.3V Rail: 3.32V
    ??? 5V Rail: 5.05V
    ??? 12V Rail: 12.1V
    ??? -12V Rail: -12.0V
*/
```

### Example 3: Mixed Approach

```csharp
using Virinco.WATS.Interface;
using System;

SequenceCall tests = root.AddSequenceCall("Production Test");

// Critical tests get their own steps (single test)
NumericLimitStep criticalVoltage = tests.AddNumericLimitStep("Critical 3.3V");
criticalVoltage.AddTest(3.32, CompOperatorType.GELE, 3.25, 3.35, "V");
criticalVoltage.StepGroup = StepGroupEnum.Main;

// Related measurements grouped (multiple tests)
NumericLimitStep auxVoltages = tests.AddNumericLimitStep("Auxiliary Voltages");
auxVoltages.AddMultipleTest(1.8, CompOperatorType.GELE, 1.75, 1.85, "V", "1.8V");
auxVoltages.AddMultipleTest(2.5, CompOperatorType.GELE, 2.45, 2.55, "V", "2.5V");
auxVoltages.AddMultipleTest(1.2, CompOperatorType.GELE, 1.15, 1.25, "V", "1.2V");
auxVoltages.StepGroup = StepGroupEnum.Main;

// Multiple functional tests
PassFailStep selfTests = tests.AddPassFailStep("Self Test Suite");
selfTests.AddMultipleTest(true, "RAM Test");
selfTests.AddMultipleTest(true, "Flash CRC");
selfTests.AddMultipleTest(true, "EEPROM Read");
selfTests.AddMultipleTest(true, "Watchdog");
selfTests.StepGroup = StepGroupEnum.Main;
```

### Example 4: Complex Multi-Channel Test

```csharp
using Virinco.WATS.Interface;
using System;

SequenceCall root = report.GetRootSequenceCall();

// Test 4 channels, each with multiple parameters
for (int channel = 1; channel <= 4; channel++)
{
    // Each channel is a separate step with multiple measurements
    NumericLimitStep channelTest = root.AddNumericLimitStep($"Channel {channel}");
    
    // Voltage
    channelTest.AddMultipleTest(
        numericValue: 3.3 + (channel * 0.01),
        compOperator: CompOperatorType.GELE,
        lowLimit: 3.20,
        highLimit: 3.40,
        units: "V",
        measureName: "Voltage"
    );
    
    // Current
    channelTest.AddMultipleTest(
        numericValue: 0.5 + (channel * 0.1),
        compOperator: CompOperatorType.GELE,
        lowLimit: 0.0,
        highLimit: 2.0,
        units: "A",
        measureName: "Current"
    );
    
    // Temperature
    channelTest.AddMultipleTest(
        numericValue: 45.0 + channel,
        compOperator: CompOperatorType.LE,
        limit: 60.0,
        units: "°C",
        measureName: "Temperature"
    );
    
    // Frequency
    channelTest.AddMultipleTest(
        numericValue: 1000 + channel,
        units: "Hz",
        measureName: "Frequency"  // LOG mode
    );
}

/* Result:
Root
??? Channel 1 (Pass)
?   ??? Voltage: 3.31V
?   ??? Current: 0.6A
?   ??? Temperature: 46°C
?   ??? Frequency: 1001Hz
??? Channel 2 (Pass)
?   ??? Voltage: 3.32V
?   ??? Current: 0.7A
?   ??? Temperature: 47°C
?   ??? Frequency: 1002Hz
??? ...
*/
```

---

## 8. Migration Guide

### From Wrong to Right

#### Scenario 1: Mixed Tests

```csharp
// ? BEFORE (WRONG)
NumericLimitStep step = root.AddNumericLimitStep("Voltages");
step.AddTest(3.3, "V");                    // Locks as single
// Realize you need more tests...
// step.AddMultipleTest(5.0, "V", "5V");   // Would throw!

// ? AFTER (CORRECT)
NumericLimitStep step = root.AddNumericLimitStep("Voltages");
step.AddMultipleTest(3.3, "V", "3.3V");    // Start with multiple
step.AddMultipleTest(5.0, "V", "5V");      // Can add more
step.AddMultipleTest(12.0, "V", "12V");    // And more
```

#### Scenario 2: Loop Creating Single Tests

```csharp
// ? BEFORE (WRONG)
for (int i = 0; i < 4; i++)
{
    NumericLimitStep step = root.AddNumericLimitStep($"Test {i}");
    step.AddTest(100 + i, "V");
    step.AddTest(200 + i, "V");  // ? Would throw on second AddTest!
}

// ? AFTER (CORRECT) - Option 1: Separate steps
for (int i = 0; i < 4; i++)
{
    NumericLimitStep step = root.AddNumericLimitStep($"Test {i}");
    step.AddTest(100 + i, "V");  // Only one test per step
}

// ? AFTER (CORRECT) - Option 2: Multiple tests per step
for (int i = 0; i < 4; i++)
{
    NumericLimitStep step = root.AddNumericLimitStep($"Channel {i}");
    step.AddMultipleTest(100 + i, "V", "Voltage");
    step.AddMultipleTest(200 + i, "A", "Current");
}
```

#### Scenario 3: Adding Tests Conditionally

```csharp
// ? BEFORE (WRONG) - Might mix modes
NumericLimitStep step = root.AddNumericLimitStep("Voltages");
step.AddTest(3.3, "V");  // Starts as single

if (needExtraTests)
{
    step.AddMultipleTest(5.0, "V", "5V");  // ? Would throw!
}

// ? AFTER (CORRECT) - Decide mode upfront
NumericLimitStep step = root.AddNumericLimitStep("Voltages");

if (needExtraTests)
{
    // Use multiple from start
    step.AddMultipleTest(3.3, "V", "3.3V");
    step.AddMultipleTest(5.0, "V", "5V");
    step.AddMultipleTest(12.0, "V", "12V");
}
else
{
    // Single test is fine
    step.AddTest(3.3, "V");
}
```

---

## Quick Reference

### Decision Tree

```
Do you need MORE THAN ONE measurement in this step?
?
?? YES ? Use AddMultipleTest()
?   ?
?   ?? NumericLimitStep: step.AddMultipleTest(value, op, limits, units, measureName)
?   ?? PassFailStep: step.AddMultipleTest(passed, measureName)
?   ?? StringValueStep: step.AddMultipleTest(op, value, expected, measureName)
?
?? NO ? Use AddTest()
    ?
    ?? NumericLimitStep: step.AddTest(value, op, limits, units)
    ?? PassFailStep: step.AddTest(passed)
    ?? StringValueStep: step.AddTest(op, value, expected)
```

### Step Type Reference

| Class | Single Type | Multiple Type |
|-------|-------------|---------------|
| NumericLimitStep | `ET_NLT` | `ET_MNLT` |
| PassFailStep | `ET_PFT` | `ET_MPFT` |
| StringValueStep | `ET_SVT` | `ET_MSVT` |

### Key Rules

1. ? **First call locks the mode** (Single or Multiple)
2. ? **Cannot mix** `AddTest()` and `AddMultipleTest()`
3. ? **Cannot call** `AddTest()` twice on single step
4. ? **Can call** `AddMultipleTest()` many times
5. ? **MeasureName required** for Multiple mode
6. ? **MeasureName not used** for Single mode

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**For WATS Client API Version:** 5.0+  
**Status:** ? VERIFIED AGAINST SOURCE CODE
