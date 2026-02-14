# WATS Chart API - Correction Document

## ?? CRITICAL CORRECTION: Chart API Documentation

This document corrects serious errors in the Chart API documentation that was previously provided.

---

## Issues Found

### 1. Incorrect Enum Value
- ? **WRONG**: `ChartType.Linear`
- ? **CORRECT**: `ChartType.Line`

### 2. Non-existent Method
- ? **WRONG**: `chart.AddXYValue(x, y)`
- ? **CORRECT**: `chart.AddSeries(name, xValues, yValues)`

---

## Correct ChartType Enum

```csharp
public enum ChartType : short
{
    /// <summary>
    /// Normal, linear X-Y graph
    /// </summary>
    Line = 0,
    
    /// <summary>
    /// Use logarithmic scaling on both axes
    /// </summary>
    LineLogXY = 1,
    
    /// <summary>
    /// Use logarithmic scaling on X-Axis
    /// </summary>
    LineLogX = 2,
    
    /// <summary>
    /// Use logarithmic scaling on Y-Axis
    /// </summary>
    LineLogY = 3
}
```

**Available Chart Types:**
- `ChartType.Line` - Linear X-Y graph (default)
- `ChartType.LineLogXY` - Logarithmic on both axes
- `ChartType.LineLogX` - Logarithmic X-axis only
- `ChartType.LineLogY` - Logarithmic Y-axis only

---

## Correct Chart Creation

### Creating a Chart

```csharp
// ? CORRECT
Chart chart = step.AddChart(
    chartType: ChartType.Line,          // NOT ChartType.Linear!
    chartLabel: "Frequency Response",
    xLabel: "Frequency",
    xUnit: "Hz",
    yLabel: "Amplitude",
    yUnit: "dB"
);
```

### Chart Properties (Read-Only)

```csharp
// After creating or retrieving a chart
ChartType type = chart.ChartType;      // The chart type
string label = chart.ChartLabel;       // Chart title/label
string xLabel = chart.XLabel;          // X-axis label
string xUnit = chart.XUnit;            // X-axis unit
string yLabel = chart.YLabel;          // Y-axis label
string yUnit = chart.YUnit;            // Y-axis unit
ChartSerie[] series = chart.Series;    // All data series
```

---

## Correct Data Addition Methods

The Chart class has **THREE** `AddSeries()` methods, **NOT** `AddXYValue()`.

### Method 1: Separate X and Y Arrays

```csharp
// ? CORRECT - Most common method
double[] xValues = new double[] { 100, 1000, 10000 };
double[] yValues = new double[] { -3.2, -0.5, -6.1 };

chart.AddSeries(
    seriesName: "Frequency Response",
    xValues: xValues,
    yValues: yValues
);
```

**Signature:**
```csharp
public void AddSeries(string seriesName, double[] xValues, double[] yValues)
```

**Validation:**
- `xValues.Length` must equal `yValues.Length`
- Throws `ApplicationException` if lengths don't match

### Method 2: 2D Array

```csharp
// ? CORRECT - Data in 2D array [2, N]
double[,] data = new double[2, 3]
{
    { 100,  1000,  10000 },  // Row 0: X values
    { -3.2, -0.5,  -6.1  }   // Row 1: Y values
};

chart.AddSeries(
    seriesName: "Frequency Response",
    dataValues: data
);
```

**Signature:**
```csharp
public void AddSeries(string seriesName, double[,] dataValues)
```

**Format:**
- Array must be `[2, N]` where N is number of points
- `dataValues[0, i]` = X values
- `dataValues[1, i]` = Y values

### Method 3: Y Values Only (Auto X)

```csharp
// ? CORRECT - X values auto-generated as 0, 1, 2, ...
double[] yValues = new double[] { -3.2, -0.5, -6.1, -4.8 };

chart.AddSeries(
    seriesName: "Data Series",
    yValues: yValues
);

// Results in points: (0, -3.2), (1, -0.5), (2, -6.1), (3, -4.8)
```

**Signature:**
```csharp
public void AddSeries(string seriesName, double[] yValues)
```

**Behavior:**
- X values automatically generated: 0, 1, 2, 3, ..., N-1
- Useful for time-series or indexed data

---

## Complete Working Examples

### Example 1: Frequency Response (Linear)

```csharp
using Virinco.WATS.Interface;
using System;

// Create step
NumericLimitStep step = root.AddNumericLimitStep("Frequency Response Test");
step.AddTest(0.0, "Sweep");  // Log mode

// Create chart
Chart chart = step.AddChart(
    chartType: ChartType.Line,              // ? Line, not Linear
    chartLabel: "Frequency Response Curve",
    xLabel: "Frequency",
    xUnit: "Hz",
    yLabel: "Gain",
    yUnit: "dB"
);

// Add measured data
double[] frequencies = new double[] { 100, 200, 500, 1000, 2000, 5000, 10000 };
double[] gains = new double[] { -3.0, -1.5, -0.5, -0.1, -0.5, -2.0, -4.5 };

chart.AddSeries(
    seriesName: "Measured Response",
    xValues: frequencies,
    yValues: gains
);

// Add ideal reference
double[] idealGains = new double[] { -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1 };

chart.AddSeries(
    seriesName: "Ideal Response",
    xValues: frequencies,
    yValues: idealGains
);
```

### Example 2: Logarithmic Chart

```csharp
// Create chart with log X-axis
Chart chart = step.AddChart(
    chartType: ChartType.LineLogX,     // ? Logarithmic X-axis
    chartLabel: "Bode Plot",
    xLabel: "Frequency",
    xUnit: "Hz",
    yLabel: "Magnitude",
    yUnit: "dB"
);

// Generate logarithmic sweep
double[] frequencies = new double[50];
double[] magnitudes = new double[50];

for (int i = 0; i < 50; i++)
{
    frequencies[i] = Math.Pow(10, i / 10.0);  // 10^0 to 10^5
    magnitudes[i] = -20 * Math.Log10(frequencies[i] / 1000);
}

chart.AddSeries("Magnitude", frequencies, magnitudes);
```

### Example 3: Multiple Series

```csharp
// Create multi-channel test chart
Chart chart = step.AddChart(
    chartType: ChartType.Line,
    chartLabel: "Multi-Channel Voltage",
    xLabel: "Time",
    xUnit: "s",
    yLabel: "Voltage",
    yUnit: "V"
);

double[] time = new double[] { 0, 1, 2, 3, 4, 5 };

// Channel 1
double[] ch1 = new double[] { 3.3, 3.31, 3.29, 3.3, 3.32, 3.3 };
chart.AddSeries("Channel 1", time, ch1);

// Channel 2
double[] ch2 = new double[] { 5.0, 5.02, 4.98, 5.0, 5.01, 5.0 };
chart.AddSeries("Channel 2", time, ch2);

// Channel 3
double[] ch3 = new double[] { 12.0, 12.05, 11.95, 12.0, 12.03, 12.0 };
chart.AddSeries("Channel 3", time, ch3);
```

### Example 4: Using 2D Array

```csharp
Chart chart = step.AddChart(
    chartType: ChartType.Line,
    chartLabel: "Temperature Profile",
    xLabel: "Time",
    xUnit: "min",
    yLabel: "Temperature",
    yUnit: "°C"
);

// Prepare data as [2, N] array
double[,] tempData = new double[2, 6]
{
    { 0,   5,   10,  15,  20,  25  },  // Time (X)
    { 25,  45,  65,  85,  105, 125 }   // Temp (Y)
};

chart.AddSeries("Heating Curve", tempData);
```

### Example 5: Auto-Indexed Data

```csharp
Chart chart = step.AddChart(
    chartType: ChartType.Line,
    chartLabel: "Voltage Samples",
    xLabel: "Sample Index",
    xUnit: "",
    yLabel: "Voltage",
    yUnit: "V"
);

// Y values only - X will be 0, 1, 2, 3, ...
double[] samples = new double[] { 5.01, 5.02, 4.99, 5.00, 5.03, 4.98 };

chart.AddSeries("Voltage", samples);
// Creates points: (0, 5.01), (1, 5.02), (2, 4.99), etc.
```

---

## Reading Chart Data

### Retrieving Chart from Step

```csharp
// Get chart (if exists)
Chart chart = step.Chart;

if (chart != null)
{
    // Read metadata
    Console.WriteLine($"Chart: {chart.ChartLabel}");
    Console.WriteLine($"Type: {chart.ChartType}");
    Console.WriteLine($"X: {chart.XLabel} ({chart.XUnit})");
    Console.WriteLine($"Y: {chart.YLabel} ({chart.YUnit})");
}
```

### Reading Series Data

```csharp
// Get all series
ChartSerie[] series = chart.Series;

Console.WriteLine($"Number of series: {series.Length}");

foreach (var serie in series)
{
    // Get series name
    string name = serie.PlotName;
    
    // Get X and Y values
    serie.GetValues(out double[] xValues, out double[] yValues);
    
    Console.WriteLine($"\nSeries: {name}");
    Console.WriteLine($"  Points: {xValues.Length}");
    
    for (int i = 0; i < xValues.Length; i++)
    {
        Console.WriteLine($"  ({xValues[i]}, {yValues[i]})");
    }
}
```

---

## Restrictions and Limits

### Series Limit

```csharp
// Maximum series per chart (configurable)
int maxSeries = api.proxy.MaxChartSeries;

// Validation depends on ValidationMode
try
{
    chart.AddSeries("Series 1", xValues1, yValues1);
    chart.AddSeries("Series 2", xValues2, yValues2);
    // ... up to MaxChartSeries
    chart.AddSeries("Too Many", xValues, yValues);  // May throw
}
catch (InvalidOperationException ex)
{
    // ValidationMode = ThrowExceptions
    Console.WriteLine($"Error: {ex.Message}");
}

// ValidationMode = AutoTruncate: silently ignores excess series
```

### Chart per Step Limit

**Only ONE chart per step allowed**

```csharp
NumericLimitStep step = root.AddNumericLimitStep("Test");

// First chart - OK
Chart chart1 = step.AddChart(
    ChartType.Line, "Chart 1", "X", "x", "Y", "y"
);

// Second chart - THROWS EXCEPTION
Chart chart2 = step.AddChart(
    ChartType.Line, "Chart 2", "X", "x", "Y", "y"
);
// ? InvalidOperationException: Step already has a chart
```

### Data Format Requirements

| Method | Requirement |
|--------|-------------|
| `AddSeries(name, xValues, yValues)` | Arrays must have same length |
| `AddSeries(name, dataValues)` | Array must be `[2, N]` format |
| `AddSeries(name, yValues)` | Any length, X auto-generated |

---

## Common Mistakes

| ? Wrong | ? Correct |
|---------|-----------|
| `ChartType.Linear` | `ChartType.Line` |
| `chart.AddXYValue(x, y)` | `chart.AddSeries(name, xValues, yValues)` |
| `chart.AddPoint(x, y)` | `chart.AddSeries(name, new[]{x}, new[]{y})` |
| Multiple charts per step | Only one chart per step |
| Mismatched array lengths | Ensure `xValues.Length == yValues.Length` |

---

## Chart Data Storage

### Internal Format

Charts are stored in the WRML schema as `Chart_type` objects with:

```csharp
// Metadata (idx=0)
Chart_type {
    StepID,           // Links to parent step
    idx = 0,          // Metadata record
    ChartType,        // "Line", "LineLogX", etc.
    Label,            // Chart label
    XLabel, XUnit,    // X-axis
    YLabel, YUnit     // Y-axis
}

// Series data (idx=1, 2, 3, ...)
Chart_type {
    StepID,           // Links to parent step
    idx = 1,          // Series 1
    PlotName,         // Series name
    Data,             // Byte array (binary double values)
    DataType = "XYG"  // X-Y Graph
}
```

### Binary Data Format

Each XY pair stored as 16 bytes:
- Bytes 0-7: X value (double, little-endian)
- Bytes 8-15: Y value (double, little-endian)

```csharp
// Example: 3 points stored as 48 bytes (3 × 16)
Point (100, -3.2)   ? 16 bytes
Point (1000, -0.5)  ? 16 bytes
Point (10000, -6.1) ? 16 bytes
```

---

## Migration Guide

### If You Used Wrong API

```csharp
// ? OLD (WRONG) CODE
Chart chart = step.AddChart(
    chartType: ChartType.Linear,  // WRONG
    chartLabel: "Test",
    xLabel: "X", xUnit: "unit",
    yLabel: "Y", yUnit: "unit"
);
chart.AddXYValue(100, -3.2);     // WRONG
chart.AddXYValue(1000, -0.5);    // WRONG

// ? NEW (CORRECT) CODE
Chart chart = step.AddChart(
    chartType: ChartType.Line,    // CORRECT
    chartLabel: "Test",
    xLabel: "X", xUnit: "unit",
    yLabel: "Y", yUnit: "unit"
);

double[] xValues = new double[] { 100, 1000 };
double[] yValues = new double[] { -3.2, -0.5 };
chart.AddSeries("Data", xValues, yValues);  // CORRECT
```

---

## Quick Reference

### Chart Creation
```csharp
Chart chart = step.AddChart(ChartType.Line, label, xLabel, xUnit, yLabel, yUnit);
```

### Add Data - Method 1 (Most Common)
```csharp
chart.AddSeries(seriesName, xValues, yValues);
```

### Add Data - Method 2 (2D Array)
```csharp
double[,] data = new double[2, N] { {x0,x1,x2}, {y0,y1,y2} };
chart.AddSeries(seriesName, data);
```

### Add Data - Method 3 (Auto X)
```csharp
chart.AddSeries(seriesName, yValues);  // X = 0, 1, 2, ...
```

### Read Data
```csharp
ChartSerie[] series = chart.Series;
serie.GetValues(out double[] x, out double[] y);
```

---

## API Reference

### ChartType Enum
```csharp
public enum ChartType : short
{
    Line = 0,        // Linear X-Y
    LineLogXY = 1,   // Log both axes
    LineLogX = 2,    // Log X only
    LineLogY = 3     // Log Y only
}
```

### Chart Class Methods
```csharp
// Add series with separate arrays
public void AddSeries(string seriesName, double[] xValues, double[] yValues)

// Add series with 2D array [2, N]
public void AddSeries(string seriesName, double[,] dataValues)

// Add series with Y only (X = 0, 1, 2, ...)
public void AddSeries(string seriesName, double[] yValues)
```

### Chart Class Properties
```csharp
public ChartType ChartType { get; }
public string ChartLabel { get; }
public string XLabel { get; }
public string XUnit { get; }
public string YLabel { get; }
public string YUnit { get; }
public ChartSerie[] Series { get; }
```

### ChartSerie Class
```csharp
public string PlotName { get; }
public void GetValues(out double[] xValues, out double[] yValues)
```

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**For WATS Client API Version:** 5.0+  
**Status:** ? VERIFIED AGAINST SOURCE CODE
