# pywats_ui.widgets - Class Reference

Auto-generated class reference for `pywats_ui.widgets`.

---

## `widgets.new_converter_dialog`

### `NewConverterDialog(QDialog)`

_Dialog for creating new converter files_

**Class Variables:**
- `TEMPLATES`

---

## `widgets.script_editor`

### `CodeNode`

_Represents a node in the code structure_

**Class Variables:**
- `name: str`
- `node_type: NodeType`
- `start_line: int`
- `end_line: int`
- `source: str`
- `docstring: str`
- `decorators: List[...]`
- `parameters: str`
- `return_type: str`
- `is_overridden: bool`
- `is_required: bool`
- `children: List[...]`

**Properties:**
- `signature`

---

### `CodeParser`

_Parses Python source code to extract structure_

**Class Variables:**
- `BASE_CLASS_METHODS`

**Methods:**
- `parse() -> CodeNode`

---

### `NodeType(Enum)`

_Type of node in the code tree_

**Class Variables:**
- `ROOT`
- `CLASS`
- `BASE_CLASS`
- `PROPERTY`
- `ABSTRACT_METHOD`
- `METHOD`
- `HELPER_FUNCTION`
- `IMPORT`
- `CONSTANT`

---

### `PythonSyntaxHighlighter(QSyntaxHighlighter)`

_Syntax highlighter for Python code_

**Class Variables:**
- `KEYWORDS`
- `BUILTINS`

**Methods:**
- `highlightBlock(text: str) -> Any`

---

### `ScriptEditorWidget(QWidget)`

_Advanced script editor for converter files._

**Class Variables:**
- `content_changed`
- `function_saved`

**Methods:**
- `get_source() -> str`
- `is_modified() -> bool`
- `load_file(file_path: str) -> bool`
- `load_source(source: str, file_path: Optional[...]) -> Any`
- `save() -> bool`

---
