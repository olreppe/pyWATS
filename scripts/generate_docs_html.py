#!/usr/bin/env python3
"""
Generate a concatenated HTML document from all official documentation.

Usage:
    python scripts/generate_docs_html.py
    
Output:
    docs/pyWATS_Documentation.html
"""

import re
from pathlib import Path
from datetime import datetime

try:
    import markdown
    from markdown.extensions.toc import TocExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False
    print("Note: 'markdown' package not installed. Using basic conversion.")


# Document structure - order matters for reading flow
DOC_STRUCTURE = [
    # Getting Started
    ("Introduction", [
        "docs/README.md",
        "docs/INDEX.md",
    ]),
    ("Getting Started", [
        "docs/getting-started.md",
        "docs/quick-reference.md",
    ]),
    ("Installation", [
        "docs/installation/README.md",
        "docs/installation/api.md",
        "docs/installation/client.md",
        "docs/installation/gui.md",
        "docs/installation/docker.md",
        "docs/installation/windows-service.md",
        "docs/installation/linux-service.md",
        "docs/installation/macos-service.md",
    ]),
    ("Architecture", [
        "docs/architecture.md",
        "docs/client-architecture.md",
        "docs/integration-patterns.md",
    ]),
    ("Domain Modules", [
        "docs/modules/README.md",
        "docs/modules/report.md",
        "docs/modules/asset.md",
        "docs/modules/process.md",
        "docs/modules/product.md",
        "docs/modules/production.md",
        "docs/modules/analytics.md",
        "docs/modules/rootcause.md",
        "docs/modules/software.md",
        "docs/modules/scim.md",
        "docs/modules/EVENTS.md",
    ]),
    ("Usage Guides", [
        "docs/usage/report-module.md",
        "docs/usage/report-builder.md",
        "docs/usage/asset-module.md",
        "docs/usage/process-module.md",
        "docs/usage/product-module.md",
        "docs/usage/production-module.md",
        "docs/usage/rootcause-module.md",
        "docs/usage/software-module.md",
        "docs/usage/box-build-guide.md",
    ]),
    ("Reference", [
        "docs/env-variables.md",
        "docs/error-catalog.md",
        "docs/wats-domain-knowledge.md",
        "docs/llm-converter-guide.md",
    ]),
]

CSS_STYLES = '''
        /* Reset and base */
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
        }
        
        /* Typography */
        h1 {
            color: #1a5276;
            border-bottom: 3px solid #1a5276;
            padding-bottom: 10px;
            margin-top: 40px;
            page-break-before: always;
        }
        
        h1:first-of-type {
            page-break-before: avoid;
        }
        
        h2 {
            color: #2874a6;
            border-bottom: 1px solid #2874a6;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        
        h3 {
            color: #3498db;
            margin-top: 25px;
        }
        
        h4, h5, h6 {
            color: #555;
            margin-top: 20px;
        }
        
        /* Cover page */
        .cover {
            text-align: center;
            padding: 100px 20px;
            page-break-after: always;
        }
        
        .cover h1 {
            font-size: 3em;
            border: none;
            margin-bottom: 20px;
            page-break-before: avoid;
        }
        
        .cover .subtitle {
            font-size: 1.5em;
            color: #666;
            margin-bottom: 40px;
        }
        
        .cover .version {
            font-size: 1.2em;
            color: #888;
        }
        
        .cover .date {
            margin-top: 60px;
            color: #999;
        }
        
        /* Table of Contents */
        .toc {
            page-break-after: always;
        }
        
        .toc h2 {
            border: none;
            text-align: center;
        }
        
        .toc ul {
            list-style: none;
            padding-left: 0;
        }
        
        .toc > ul > li {
            margin: 15px 0;
        }
        
        .toc > ul > li > a {
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .toc ul ul {
            padding-left: 25px;
            margin-top: 5px;
        }
        
        .toc ul ul li {
            margin: 5px 0;
        }
        
        .toc a {
            color: #2874a6;
            text-decoration: none;
        }
        
        .toc a:hover {
            text-decoration: underline;
        }
        
        /* Section dividers */
        .section-header {
            background: #1a5276;
            color: white;
            padding: 30px;
            margin: 40px -20px;
            text-align: center;
            page-break-before: always;
        }
        
        .section-header h1 {
            color: white;
            border: none;
            margin: 0;
            page-break-before: avoid;
        }
        
        /* Code blocks */
        pre {
            background: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            font-size: 0.9em;
            line-height: 1.4;
        }
        
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        pre code {
            background: none;
            padding: 0;
        }
        
        /* Tables */
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 0.95em;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 10px 12px;
            text-align: left;
        }
        
        th {
            background: #f8f9fa;
            font-weight: 600;
            color: #1a5276;
        }
        
        tr:nth-child(even) {
            background: #fafafa;
        }
        
        /* Blockquotes */
        blockquote {
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background: #f8f9fa;
            color: #555;
        }
        
        /* Links */
        a {
            color: #2874a6;
        }
        
        /* Lists */
        ul, ol {
            padding-left: 25px;
        }
        
        li {
            margin: 5px 0;
        }
        
        /* Images */
        img {
            max-width: 100%;
            height: auto;
        }
        
        /* Horizontal rule */
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }
        
        /* Document separator */
        .doc-separator {
            border-top: 2px dashed #ccc;
            margin: 40px 0;
            padding-top: 20px;
        }
        
        .doc-source {
            color: #999;
            font-size: 0.8em;
            font-style: italic;
            margin-bottom: 20px;
        }
        
        /* Print styles */
        @media print {
            body {
                max-width: none;
                padding: 0;
                font-size: 11pt;
            }
            
            pre {
                white-space: pre-wrap;
                word-wrap: break-word;
            }
            
            .section-header {
                margin: 0;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            
            a {
                color: #333;
                text-decoration: none;
            }
            
            h1, h2, h3, h4 {
                page-break-after: avoid;
            }
            
            pre, table, blockquote {
                page-break-inside: avoid;
            }
        }
        
        /* Syntax highlighting basic */
        .highlight .k { color: #008000; font-weight: bold; }
        .highlight .s { color: #ba2121; }
        .highlight .c { color: #408080; font-style: italic; }
        .highlight .n { color: #333; }
        .highlight .o { color: #666; }
'''


def get_html_template(date: str, toc: str, content: str) -> str:
    """Generate the complete HTML document."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>pyWATS Documentation</title>
    <style>{CSS_STYLES}
    </style>
</head>
<body>
    <!-- Cover Page -->
    <div class="cover">
        <h1>pyWATS</h1>
        <div class="subtitle">Python API for WATS Test Data Management</div>
        <div class="version">Official Documentation</div>
        <div class="date">Generated: {date}</div>
    </div>
    
    <!-- Table of Contents -->
    <div class="toc">
        <h2>Table of Contents</h2>
        {toc}
    </div>
    
    <!-- Content -->
    {content}
    
    <!-- Footer -->
    <hr>
    <p style="text-align: center; color: #999; font-size: 0.9em;">
        pyWATS Documentation &copy; Virinco AS<br>
        Generated on {date}
    </p>
</body>
</html>
'''


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def convert_md_to_html(content: str) -> str:
    """Convert markdown to HTML."""
    if HAS_MARKDOWN:
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br',
        ])
        return md.convert(content)
    else:
        # Basic conversion without markdown library
        # Convert headers
        content = re.sub(r'^#{6}\s+(.+)$', r'<h6>\1</h6>', content, flags=re.MULTILINE)
        content = re.sub(r'^#{5}\s+(.+)$', r'<h5>\1</h5>', content, flags=re.MULTILINE)
        content = re.sub(r'^#{4}\s+(.+)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)
        content = re.sub(r'^#{3}\s+(.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^#{2}\s+(.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^#\s+(.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        
        # Convert code blocks
        content = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', content, flags=re.DOTALL)
        
        # Convert inline code
        content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
        
        # Convert bold and italic
        content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', content)
        
        # Convert links
        content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
        
        # Convert paragraphs
        paragraphs = content.split('\n\n')
        content = '\n'.join(f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs)
        
        return content


def read_doc(path: Path) -> str:
    """Read and return document content."""
    if path.exists():
        return path.read_text(encoding='utf-8')
    return f"*Document not found: {path}*"


def generate_toc(structure: list) -> str:
    """Generate table of contents HTML."""
    toc_html = ["<ul>"]
    
    for section_name, docs in structure:
        section_id = slugify(section_name)
        toc_html.append(f'<li><a href="#{section_id}">{section_name}</a>')
        toc_html.append('<ul>')
        
        for doc_path in docs:
            doc_name = Path(doc_path).stem.replace('-', ' ').replace('_', ' ').title()
            if doc_name == 'Readme':
                doc_name = 'Overview'
            if doc_name == 'Index':
                continue
            doc_id = slugify(f"{section_name}-{doc_name}")
            toc_html.append(f'<li><a href="#{doc_id}">{doc_name}</a></li>')
        
        toc_html.append('</ul>')
        toc_html.append('</li>')
    
    toc_html.append("</ul>")
    return '\n'.join(toc_html)


def generate_content(base_path: Path, structure: list) -> str:
    """Generate main content HTML."""
    content_parts = []
    
    for section_name, docs in structure:
        section_id = slugify(section_name)
        
        # Section header
        content_parts.append(f'''
<div class="section-header" id="{section_id}">
    <h1>{section_name}</h1>
</div>
''')
        
        for doc_path in docs:
            full_path = base_path / doc_path
            doc_name = Path(doc_path).stem.replace('-', ' ').replace('_', ' ').title()
            if doc_name == 'Readme':
                doc_name = 'Overview'
            if doc_name == 'Index':
                continue
                
            doc_id = slugify(f"{section_name}-{doc_name}")
            
            # Read and convert document
            md_content = read_doc(full_path)
            html_content = convert_md_to_html(md_content)
            
            content_parts.append(f'''
<div class="doc-separator" id="{doc_id}">
    <div class="doc-source">Source: {doc_path}</div>
    {html_content}
</div>
''')
    
    return '\n'.join(content_parts)


def main():
    """Generate the HTML documentation."""
    # Find project root
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent
    
    print(f"Base path: {base_path}")
    print(f"Generating documentation...")
    
    # Generate TOC and content
    toc = generate_toc(DOC_STRUCTURE)
    content = generate_content(base_path, DOC_STRUCTURE)
    
    # Fill template
    html = get_html_template(
        date=datetime.now().strftime("%Y-%m-%d"),
        toc=toc,
        content=content,
    )
    
    # Write output
    output_path = base_path / "docs" / "pyWATS_Documentation.html"
    output_path.write_text(html, encoding='utf-8')
    
    print(f"Documentation generated: {output_path}")
    print(f"Open in browser and print to PDF (Ctrl+P)")


if __name__ == "__main__":
    main()
