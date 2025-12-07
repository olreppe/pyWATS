# Converter Generator - LLM-Powered Tool Design

## Overview

A standalone tool that uses an LLM to automatically generate pyWATS converters from sample input files. Users provide a sample file and description, and the tool outputs a ready-to-use Python converter module.

## Why a Separate Tool?

| Aspect | Separate Tool | Integrated in Client |
|--------|---------------|---------------------|
| Dependencies | Minimal - just LLM client | Heavy - bundles LLM libs |
| LLM Choice | Flexible (cloud/local) | Fixed at build time |
| Updates | Independent releases | Tied to client releases |
| Usage Pattern | One-time generation | Always available |
| API Costs | Pay per generation | Ongoing costs |

**Recommendation**: Separate tool is cleaner and more flexible.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Converter Generator                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Sample File  │───▶│   Analyzer   │───▶│  LLM Engine  │  │
│  │   + Desc     │    │              │    │              │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│                                                  │          │
│                      ┌──────────────┐            │          │
│                      │   Context    │────────────┘          │
│                      │   Provider   │                       │
│                      │              │                       │
│                      │ • API Schema │                       │
│                      │ • Examples   │                       │
│                      │ • Templates  │                       │
│                      └──────────────┘                       │
│                                                  │          │
│                                                  ▼          │
│                                          ┌──────────────┐   │
│                                          │  Generated   │   │
│                                          │  Converter   │   │
│                                          │    .py       │   │
│                                          └──────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## User Workflow

```
1. User has a sample test log file (CSV, XML, JSON, proprietary format)
2. User runs: converter-generator analyze sample.log
3. Tool shows detected structure and suggests mappings
4. User confirms or adjusts: converter-generator generate sample.log --output my_converter.py
5. User copies converter to pywats_client/converters/ folder
6. Converter runs automatically when files appear in watch folder
```

## Implementation Plan

### Phase 1: Core Generator

```python
# src/converter_generator/__init__.py
"""
pyWATS Converter Generator

LLM-powered tool to create converters from sample files.
"""

__version__ = "0.1.0"
```

```python
# src/converter_generator/generator.py
"""
Main converter generation logic.
"""

from pathlib import Path
from typing import Optional, Protocol
from dataclasses import dataclass


class LLMClient(Protocol):
    """Protocol for LLM backends"""
    def generate(self, prompt: str, max_tokens: int = 4000) -> str: ...


@dataclass
class GenerationResult:
    """Result of converter generation"""
    success: bool
    code: Optional[str] = None
    error: Optional[str] = None
    detected_format: Optional[str] = None
    field_mappings: Optional[dict] = None


class ConverterGenerator:
    """
    Generates pyWATS converters from sample files using an LLM.
    """
    
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self._context = self._load_context()
    
    def _load_context(self) -> str:
        """Load API knowledge, schemas, and examples"""
        return CONVERTER_CONTEXT  # See below
    
    def analyze(self, file_path: Path) -> dict:
        """
        Analyze a sample file and detect its structure.
        
        Returns dict with:
        - format: Detected format (CSV, XML, JSON, etc.)
        - fields: List of detected fields
        - sample_records: First few parsed records
        - suggested_mappings: Suggested WATS field mappings
        """
        content = file_path.read_bytes()
        
        prompt = f"""
        Analyze this file and identify:
        1. File format (CSV, XML, JSON, fixed-width, binary, proprietary)
        2. Structure and fields present
        3. Which fields likely map to WATS report fields
        
        File: {file_path.name}
        Content (first 10KB):
        {content[:10000].decode('utf-8', errors='replace')}
        
        Return a JSON analysis.
        """
        
        response = self.llm.generate(prompt)
        return self._parse_analysis(response)
    
    def generate(
        self, 
        file_path: Path, 
        description: str = "",
        mappings: Optional[dict] = None
    ) -> GenerationResult:
        """
        Generate a converter for the given sample file.
        
        Args:
            file_path: Path to sample input file
            description: User description of the file format
            mappings: Optional explicit field mappings
            
        Returns:
            GenerationResult with generated code or error
        """
        content = file_path.read_bytes()
        
        prompt = f"""
        Create a pyWATS converter for this file format.
        
        {self._context}
        
        ## Sample File
        
        Filename: {file_path.name}
        User description: {description or "No description provided"}
        
        Content (first 10KB):
        ```
        {content[:10000].decode('utf-8', errors='replace')}
        ```
        
        {f"Explicit mappings: {mappings}" if mappings else ""}
        
        ## Requirements
        
        1. Create a class inheriting from ConverterBase
        2. Implement the convert() method
        3. Parse the file format correctly
        4. Map fields to WATS report structure
        5. Handle errors gracefully
        6. Include docstrings and comments
        
        Return ONLY the Python code, no explanations.
        """
        
        try:
            code = self.llm.generate(prompt, max_tokens=4000)
            code = self._extract_code(code)
            
            return GenerationResult(
                success=True,
                code=code,
                detected_format=self._detect_format(file_path)
            )
        except Exception as e:
            return GenerationResult(
                success=False,
                error=str(e)
            )
    
    def _extract_code(self, response: str) -> str:
        """Extract Python code from LLM response"""
        # Handle markdown code blocks
        if "```python" in response:
            start = response.find("```python") + 9
            end = response.find("```", start)
            return response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            return response[start:end].strip()
        return response.strip()
    
    def _detect_format(self, file_path: Path) -> str:
        """Detect file format from extension and content"""
        ext = file_path.suffix.lower()
        format_map = {
            '.csv': 'CSV',
            '.xml': 'XML', 
            '.json': 'JSON',
            '.log': 'Log',
            '.txt': 'Text',
        }
        return format_map.get(ext, 'Unknown')
```

### Phase 2: Context Provider

```python
# src/converter_generator/context.py
"""
Knowledge context for the LLM.
"""

CONVERTER_CONTEXT = '''
## pyWATS Converter Framework

### ConverterBase Interface

```python
from abc import ABC, abstractmethod
from typing import BinaryIO
from dataclasses import dataclass

@dataclass
class ConverterResult:
    success: bool
    report: dict = None  # WATS report dict
    error: str = None

class ConverterBase(ABC):
    """Base class for all converters"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable converter name"""
        
    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this converter handles"""
        
    @property
    @abstractmethod
    def extensions(self) -> list[str]:
        """File extensions this converter handles, e.g. ['.csv', '.log']"""
    
    @abstractmethod
    def convert(self, file: BinaryIO, filename: str) -> ConverterResult:
        """
        Convert input file to WATS report format.
        
        Args:
            file: Binary file object to read from
            filename: Original filename
            
        Returns:
            ConverterResult with success status and report dict
        """
```

### WATS Report Schema (UUT Report)

```python
{
    "type": "Test",           # Required: "Test" for UUT reports
    "pn": "PART-NUMBER",      # Required: Part number
    "sn": "SERIAL-NUMBER",    # Required: Serial number
    "rev": "A",               # Optional: Revision
    "result": "P",            # Required: "P" (Pass), "F" (Fail), "E" (Error)
    "start": "2024-01-15T10:30:00",  # Required: ISO timestamp
    "machineName": "Station1", # Optional: Test station name
    "processCode": "10",      # Optional: Process code
    "operatorName": "John",   # Optional: Operator
    "root": {                 # Required: Root sequence
        "status": "P",        # Required: "P", "F", "D" (Done), "S" (Skipped)
        "stepType": "SequenceCall",
        "group": "Main",
        "steps": [...]        # Array of test steps
    }
}
```

### Step Types

#### NumericLimitTest
```python
{
    "stepType": "NumericLimitTest",
    "name": "Voltage Test",
    "status": "P",
    "group": "Electrical",
    "numericMeas": [{
        "name": "Voltage",
        "status": "P",
        "value": 5.02,
        "unit": "V",
        "lowLimit": 4.5,
        "highLimit": 5.5
    }]
}
```

#### StringValueTest
```python
{
    "stepType": "StringValueTest",
    "name": "Firmware Check",
    "status": "P",
    "group": "Configuration",
    "stringMeas": [{
        "name": "Version",
        "status": "P",
        "value": "1.2.3",
        "expected": "1.2.3"
    }]
}
```

#### PassFailTest
```python
{
    "stepType": "PassFailTest",
    "name": "Visual Inspection",
    "status": "P",
    "group": "Visual"
}
```

#### SequenceCall (nested steps)
```python
{
    "stepType": "SequenceCall",
    "name": "Power Tests",
    "status": "P",
    "group": "Tests",
    "steps": [
        # Nested steps here
    ]
}
```

### Common Field Mappings

| Source Field | WATS Field | Notes |
|--------------|------------|-------|
| Serial, SN, SerialNumber | sn | Serial number |
| Part, PN, PartNumber | pn | Part number |
| Pass/Fail, Result, Status | result | P/F/E |
| Timestamp, Date, Time | start | ISO format |
| Station, Machine, Tester | machineName | |
| Operator, User | operatorName | |
| Test Name, Measurement | step.name | |
| Value, Reading, Result | numericMeas.value | |
| Units, Unit | numericMeas.unit | |
| Min, Low, LowLimit | numericMeas.lowLimit | |
| Max, High, HighLimit | numericMeas.highLimit | |

### Example: CSV Converter

```python
"""CSV Test Results Converter"""
import csv
from io import TextIOWrapper
from datetime import datetime
from typing import BinaryIO

from pywats_client.converters import ConverterBase, ConverterResult


class CSVConverter(ConverterBase):
    @property
    def name(self) -> str:
        return "CSV Test Results"
    
    @property
    def description(self) -> str:
        return "Converts CSV files with test measurements"
    
    @property
    def extensions(self) -> list[str]:
        return [".csv"]
    
    def convert(self, file: BinaryIO, filename: str) -> ConverterResult:
        try:
            reader = csv.DictReader(TextIOWrapper(file, 'utf-8'))
            rows = list(reader)
            
            if not rows:
                return ConverterResult(False, error="Empty CSV")
            
            first = rows[0]
            report = {
                "type": "Test",
                "pn": first.get("part_number", "UNKNOWN"),
                "sn": first.get("serial_number", "UNKNOWN"),
                "result": self._overall_result(rows),
                "start": datetime.now().isoformat(),
                "root": {
                    "status": self._overall_result(rows),
                    "stepType": "SequenceCall",
                    "group": "Main",
                    "steps": [self._row_to_step(r) for r in rows]
                }
            }
            
            return ConverterResult(True, report=report)
            
        except Exception as e:
            return ConverterResult(False, error=str(e))
    
    def _overall_result(self, rows) -> str:
        for r in rows:
            if r.get("status", "").upper() in ["F", "FAIL"]:
                return "F"
        return "P"
    
    def _row_to_step(self, row: dict) -> dict:
        status = "P" if row.get("status", "").upper() in ["P", "PASS"] else "F"
        return {
            "stepType": "NumericLimitTest",
            "name": row.get("test_name", "Test"),
            "status": status,
            "group": "Tests",
            "numericMeas": [{
                "name": row.get("test_name", "Measurement"),
                "status": status,
                "value": float(row.get("value", 0)),
                "unit": row.get("unit", ""),
            }]
        }
```
'''
```

### Phase 3: CLI Interface

```python
# src/converter_generator/cli.py
"""
Command-line interface for converter generator.
"""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Generate pyWATS converters from sample files"
    )
    subparsers = parser.add_subparsers(dest="command")
    
    # Analyze command
    analyze = subparsers.add_parser("analyze", help="Analyze a sample file")
    analyze.add_argument("file", type=Path, help="Sample file to analyze")
    
    # Generate command
    generate = subparsers.add_parser("generate", help="Generate a converter")
    generate.add_argument("file", type=Path, help="Sample file")
    generate.add_argument("-o", "--output", type=Path, help="Output file")
    generate.add_argument("-d", "--description", help="File format description")
    generate.add_argument("--provider", default="openai", 
                         choices=["openai", "anthropic", "local"],
                         help="LLM provider")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        run_analyze(args)
    elif args.command == "generate":
        run_generate(args)
    else:
        parser.print_help()


def run_analyze(args):
    """Run file analysis"""
    from .generator import ConverterGenerator
    from .llm import get_llm_client
    
    llm = get_llm_client()
    gen = ConverterGenerator(llm)
    
    print(f"Analyzing {args.file}...")
    result = gen.analyze(args.file)
    
    print(f"\nDetected format: {result.get('format', 'Unknown')}")
    print(f"Fields found: {result.get('fields', [])}")
    print(f"\nSuggested mappings:")
    for src, dest in result.get('mappings', {}).items():
        print(f"  {src} → {dest}")


def run_generate(args):
    """Run converter generation"""
    from .generator import ConverterGenerator
    from .llm import get_llm_client
    
    llm = get_llm_client(args.provider)
    gen = ConverterGenerator(llm)
    
    print(f"Generating converter for {args.file}...")
    result = gen.generate(args.file, args.description or "")
    
    if result.success:
        output = args.output or Path(f"{args.file.stem}_converter.py")
        output.write_text(result.code)
        print(f"✓ Converter saved to {output}")
    else:
        print(f"✗ Generation failed: {result.error}")


if __name__ == "__main__":
    main()
```

### Phase 4: LLM Backends

```python
# src/converter_generator/llm.py
"""
LLM client implementations.
"""

import os
from typing import Optional


def get_llm_client(provider: str = "openai"):
    """Get an LLM client for the specified provider"""
    if provider == "openai":
        return OpenAIClient()
    elif provider == "anthropic":
        return AnthropicClient()
    elif provider == "local":
        return LocalClient()
    else:
        raise ValueError(f"Unknown provider: {provider}")


class OpenAIClient:
    """OpenAI API client"""
    
    def __init__(self):
        import openai
        self.client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
    
    def generate(self, prompt: str, max_tokens: int = 4000) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content


class AnthropicClient:
    """Anthropic Claude API client"""
    
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
    
    def generate(self, prompt: str, max_tokens: int = 4000) -> str:
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


class LocalClient:
    """Local LLM client (e.g., Ollama, llama.cpp)"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def generate(self, prompt: str, max_tokens: int = 4000) -> str:
        import requests
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": "codellama",
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]
```

## Dependencies

```toml
# pyproject.toml addition
[project.optional-dependencies]
generator = [
    "openai>=1.0.0",
    "anthropic>=0.18.0",
    "requests>=2.28.0",
]

[project.scripts]
converter-generator = "converter_generator.cli:main"
```

## Usage Examples

```bash
# Analyze a sample file
converter-generator analyze sample_test_log.csv

# Generate with OpenAI (default)
converter-generator generate sample.csv -o my_converter.py

# Generate with Claude
converter-generator generate sample.xml --provider anthropic -d "XML test results from LabVIEW"

# Generate with local model
converter-generator generate sample.log --provider local
```

## Future Enhancements

1. **Interactive mode**: Ask clarifying questions about ambiguous fields
2. **Validation**: Test generated converter against sample file
3. **Template library**: Pre-built converters for common formats (NI TestStand, LabVIEW, JUnit)
4. **GUI**: Simple drag-and-drop interface
5. **MCP integration**: Expose as MCP tools for Claude/GPT integration

## File Structure

```
src/converter_generator/
├── __init__.py
├── __main__.py        # Entry point
├── cli.py             # CLI interface
├── generator.py       # Main generation logic
├── context.py         # LLM knowledge context
├── llm.py             # LLM client implementations
└── templates/         # Converter templates
    ├── csv_template.py
    ├── xml_template.py
    └── json_template.py
```
