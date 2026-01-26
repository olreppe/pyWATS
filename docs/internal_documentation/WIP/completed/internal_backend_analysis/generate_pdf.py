#!/usr/bin/env python3
"""
Generate a printable HTML from the internal endpoints analysis markdown.
Open the HTML in a browser and use Print -> Save as PDF.
"""

import markdown2
from pathlib import Path

# Paths
script_dir = Path(__file__).parent
md_file = script_dir / "internal_endpoints_status.md"
html_file = script_dir / "internal_endpoints_status.html"

# Read markdown
md_content = md_file.read_text(encoding="utf-8")

# Convert to HTML with extras for tables, code blocks, etc.
html_body = markdown2.markdown(
    md_content,
    extras=[
        "tables",
        "fenced-code-blocks",
        "code-friendly",
        "cuddled-lists",
        "header-ids",
        "strike",
        "task_list",
    ]
)

# Full HTML with print-friendly CSS
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Internal Backend Endpoints Analysis - pyWATS</title>
    <style>
        /* Base styles */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
            background: #fff;
        }}
        
        /* Headers */
        h1 {{
            color: #1a365d;
            border-bottom: 3px solid #3182ce;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        
        h2 {{
            color: #2c5282;
            border-bottom: 2px solid #90cdf4;
            padding-bottom: 8px;
            margin-top: 40px;
            page-break-after: avoid;
        }}
        
        h3 {{
            color: #2b6cb0;
            margin-top: 30px;
            page-break-after: avoid;
        }}
        
        h4 {{
            color: #3182ce;
            margin-top: 20px;
            page-break-after: avoid;
        }}
        
        /* Blockquotes (metadata) */
        blockquote {{
            background: #ebf8ff;
            border-left: 4px solid #3182ce;
            margin: 20px 0;
            padding: 15px 20px;
            font-style: normal;
        }}
        
        blockquote strong {{
            color: #2c5282;
        }}
        
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9em;
            page-break-inside: avoid;
        }}
        
        th {{
            background: #2c5282;
            color: white;
            padding: 12px 10px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 10px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        tr:nth-child(even) {{
            background: #f7fafc;
        }}
        
        tr:hover {{
            background: #ebf8ff;
        }}
        
        /* Code */
        code {{
            background: #edf2f7;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
            color: #c53030;
        }}
        
        pre {{
            background: #1a202c;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 0.85em;
            line-height: 1.5;
            page-break-inside: avoid;
        }}
        
        pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}
        
        /* Lists */
        ul, ol {{
            padding-left: 25px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        /* Horizontal rules */
        hr {{
            border: none;
            border-top: 2px solid #e2e8f0;
            margin: 40px 0;
        }}
        
        /* Status indicators */
        td:first-child {{
            font-family: 'Consolas', monospace;
            font-size: 0.85em;
        }}
        
        /* Emoji styling */
        .emoji {{
            font-style: normal;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                padding: 0;
                font-size: 11pt;
                max-width: none;
            }}
            
            h1 {{
                font-size: 24pt;
            }}
            
            h2 {{
                font-size: 18pt;
                margin-top: 30px;
            }}
            
            h3 {{
                font-size: 14pt;
            }}
            
            pre {{
                background: #f5f5f5 !important;
                color: #333 !important;
                border: 1px solid #ddd;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            table {{
                font-size: 9pt;
            }}
            
            th {{
                background: #333 !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            blockquote {{
                background: #f5f5f5 !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            /* Page breaks */
            h2 {{
                page-break-before: auto;
            }}
            
            table, pre, blockquote {{
                page-break-inside: avoid;
            }}
            
            tr {{
                page-break-inside: avoid;
            }}
        }}
        
        /* Cover page info */
        .cover-info {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        .cover-info h1 {{
            border: none;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .cover-info .subtitle {{
            color: #718096;
            font-size: 1.2em;
        }}
        
        /* Footer */
        .footer {{
            margin-top: 60px;
            padding-top: 20px;
            border-top: 2px solid #e2e8f0;
            text-align: center;
            color: #718096;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="cover-info">
        <h1>🔌 Internal Backend Endpoints Analysis</h1>
        <div class="subtitle">pyWATS API Documentation</div>
    </div>
    
    {html_body}
    
    <div class="footer">
        <p>Generated from pyWATS project documentation</p>
        <p>Branch: feature/separate-service-gui-mode | January 2026</p>
    </div>
</body>
</html>
"""

# Write HTML
html_file.write_text(html_template, encoding="utf-8")
print(f"✅ HTML generated: {html_file}")
print(f"\n📄 To create PDF:")
print(f"   1. Open the HTML file in your browser")
print(f"   2. Press Ctrl+P (or Cmd+P on Mac)")
print(f"   3. Select 'Save as PDF' as destination")
print(f"   4. Click Save")
