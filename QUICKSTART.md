# Quick Start Guide

## Project Structure

```
maya_mcp/
├── src/py/maya_mcp/          # Main package
│   ├── __init__.py          # FastMCP server instance and imports
│   ├── __main__.py          # Entry point (run with: python -m maya_mcp)
│   ├── server.py            # Core server setup and status tools
│   ├── tools/                # Tool implementations
│   │   ├── __init__.py
│   │   └── scene.py         # Scene manipulation tools
│   ├── resources/           # Resource implementations
│   │   └── __init__.py
│   └── prompts/             # Prompt templates
│       └── __init__.py
├── examples/
│   └── start_in_maya.py     # Example script for starting from Maya
├── pyproject.toml           # Project configuration
├── README.md                # Project documentation
├── AGENTS.md                # AI agent guidance
└── .gitignore              # Git ignore rules
```

## Starting the Server

### From Maya Script Editor

```python
import sys
sys.path.insert(0, r'F:\git\maya_mcp\src\py')
import maya_mcp
maya_mcp.__main__.main()
```

### From mayapy Command Line

```bash
cd F:\git\maya_mcp
mayapy -m maya_mcp
```

### After Installation

```bash
pip install -e .
maya-mcp
```

## Available Tools

### Server Status
- `get_server_status()` - Check if server is running and Maya is available

### Scene Operations
- `get_selection()` - Get currently selected objects
- `select_objects(names: list[str])` - Select objects by name
- `clear_selection()` - Clear the current selection

## Adding New Tools

1. Create a new file in `src/py/maya_mcp/tools/` (e.g., `objects.py`)
2. Import `mcp` from `maya_mcp`
3. Use the `@mcp.tool` decorator:

```python
from maya_mcp import mcp

@mcp.tool
def my_new_tool(param: str) -> dict[str, str]:
    """Tool description."""
    try:
        import maya.cmds as cmds
        # Your tool implementation
        return {'status': 'success', 'result': '...'}
    except Exception as err:
        return {'status': 'error', 'message': str(err)}
```

4. Import the module in `src/py/maya_mcp/tools/__init__.py`
5. Import the tools module in `src/py/maya_mcp/__init__.py`

## Development

See [AGENTS.md](AGENTS.md) for detailed development guidelines.
