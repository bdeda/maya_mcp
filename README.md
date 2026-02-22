# maya_mcp

FastMCP-based Model Context Protocol (MCP) server for Autodesk Maya. This server enables AI assistants and other MCP clients to interact with an active Maya session, control scene objects, and perform common 3D operations.

## Features

- **FastMCP Framework**: Built on FastMCP for easy tool, resource, and prompt registration
- **Maya Integration**: Communicate with active Maya sessions via maya.cmds API
- **Flexible Deployment**: Can be started from within Maya or from a mayapy process
- **Extensible**: Easy to add new tools, resources, and prompts

## Installation

### Development Installation

```bash
# Using pip
pip install -e .

# Using uv
uv pip install -e .
```

### Requirements

- Python 3.10+ (3.11+ recommended)
- FastMCP >= 2.0.0
- Autodesk Maya (for running the server with Maya)

## Usage

### Starting the Server from Maya

1. Open Maya
2. In the Maya Script Editor, run:
```python
import sys
sys.path.insert(0, r'F:\git\maya_mcp\src\py')  # Adjust path as needed
import maya_mcp
maya_mcp.__main__.main()
```

### Starting the Server from mayapy

```bash
# Using mayapy directly
mayapy -m maya_mcp

# Or if installed as a package
mayapy -c "from maya_mcp import mcp; mcp.run()"
```

### Starting as a Standalone Script

If installed via pip/uv:
```bash
maya-mcp
```

Note: The server will warn if Maya is not available, but some tools may not work.

## Available Tools

### Server Status
- `get_server_status()` - Get the status of the Maya MCP server

### Scene Operations
- `get_selection()` - Get currently selected objects
- `select_objects(names)` - Select objects by name
- `clear_selection()` - Clear the current selection

More tools will be added as the project develops.

## Project Structure

```
maya_mcp/
├── src/
│   └── py/
│       └── maya_mcp/
│           ├── __init__.py          # Main FastMCP server setup
│           ├── __main__.py          # Entry point for running the server
│           ├── server.py            # Core server setup and status tools
│           ├── tools/               # Tool implementations
│           │   ├── __init__.py
│           │   └── scene.py         # Scene manipulation tools
│           ├── resources/            # Resource implementations
│           │   └── __init__.py
│           └── prompts/              # Prompt templates
│               └── __init__.py
├── tests/                            # Unit tests (to be added)
├── pyproject.toml                    # Project configuration
├── README.md                         # This file
└── AGENTS.md                         # AI agent guidance
```

## Development

See [AGENTS.md](AGENTS.md) for detailed guidance on developing and extending the Maya MCP server.

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=src/py/maya_mcp --cov-report=term-missing
```

## License

Apache License 2.0

## Author

Ben Deda
