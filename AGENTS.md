# AGENTS.md

This file provides guidance for AI agents when generating, modifying, or reviewing code in the Maya MCP server repository.

## 🎯 Project Overview

Maya MCP is a FastMCP-based Model Context Protocol (MCP) server that provides tools and resources for interacting with Autodesk Maya. It enables AI assistants and other MCP clients to control Maya, query scene data, and perform common 3D operations.

**Key Technologies:**
- Python 3.10+ (3.11+ recommended)
- FastMCP for MCP server framework
- Maya Python API (maya.cmds, maya.OpenMaya, etc.)
- Model Context Protocol (MCP) specification

## 📋 Core Principles

### 1. Follow FastMCP Patterns
- **Use decorators** - Leverage `@mcp.tool`, `@mcp.resource`, and `@mcp.prompt` decorators
- **Keep tools focused** - Each tool should perform a single, well-defined operation
- **Document thoroughly** - Use docstrings to describe what each tool/resource/prompt does
- **Handle errors gracefully** - Catch Maya-specific exceptions and return meaningful error messages

### 2. Code Quality Standards

#### Type Hints
- **Always add type hints** to all functions and methods
- Use Python 3.10+ syntax: `str | None` instead of `Optional[str]`
- Use `from typing import` for complex types (Dict, List, Tuple, etc.)
- Example:
```python
@mcp.tool
def create_cube(name: str, size: float = 1.0) -> dict[str, str]:
    """Create a cube in Maya.
    
    Args:
        name: Name for the cube transform node.
        size: Size of the cube (default: 1.0).
    
    Returns:
        Dictionary with 'status' and 'node' keys.
    """
    ...
```

#### Error Handling
- **Never use bare `except:`** - Always catch specific exceptions
- **Handle Maya errors** - Catch `RuntimeError`, `ValueError`, and Maya-specific exceptions
- **Return structured errors** - Use dictionaries or raise MCP-compatible exceptions
- Example:
```python
@mcp.tool
def select_object(name: str) -> dict[str, str]:
    """Select an object by name."""
    try:
        import maya.cmds as cmds
        if not cmds.objExists(name):
            return {'status': 'error', 'message': f'Object {name} does not exist'}
        cmds.select(name)
        return {'status': 'success', 'message': f'Selected {name}'}
    except RuntimeError as err:
        return {'status': 'error', 'message': f'Maya error: {err}'}
    except Exception as err:
        return {'status': 'error', 'message': f'Unexpected error: {err}'}
```

#### Maya API Usage
- **Prefer maya.cmds** - Use the command API for most operations (simpler, more stable)
- **Use OpenMaya when needed** - For performance-critical or advanced operations
- **Check object existence** - Always verify objects exist before operating on them
- **Handle Maya state** - Be aware of Maya's undo queue and scene state
- Example:
```python
import maya.cmds as cmds

@mcp.tool
def get_selection() -> list[str]:
    """Get currently selected objects."""
    return cmds.ls(selection=True) or []
```

#### Module Layout
- **Public API at the top** - Put public tools, resources, and prompts at the top
- **Internal/private at the bottom** - Put internal helpers and private functions at the bottom
- **Sort alphabetically** - Within each area, keep symbols sorted alphabetically
- **Group by type** - Group tools together, resources together, prompts together
- Example structure:
```python
"""Maya MCP Server - Scene manipulation tools."""

from fastmcp import FastMCP

mcp = FastMCP("Maya MCP")

# --- Tools (alphabetically sorted) ---

@mcp.tool
def create_cube(...):
    ...

@mcp.tool
def delete_object(...):
    ...

# --- Resources (alphabetically sorted) ---

@mcp.resource("maya://scene")
def get_scene_info(...):
    ...

# --- Prompts (alphabetically sorted) ---

@mcp.prompt()
def modeling_prompt(...):
    ...

# --- Internal/private (alphabetically sorted) ---

def _validate_object_name(name: str) -> bool:
    ...
```

#### Imports
- **Prefer imports at the top** - Put `import` statements at the top of the file
- **Deferred Maya imports** - Import `maya.cmds` inside functions if Maya may not be available
- **Group imports** - Standard library, third-party, first-party/local
- Example:
```python
from typing import Dict, List
from fastmcp import FastMCP

# Maya imports may be deferred if running outside Maya
# import maya.cmds as cmds  # Uncomment when Maya is available
```

### 3. Project Structure

```
maya_mcp/
├── src/
│   └── maya_mcp/
│       ├── __init__.py          # Main FastMCP server setup
│       ├── tools/                # Tool implementations
│       │   ├── __init__.py
│       │   ├── scene.py          # Scene manipulation tools
│       │   ├── objects.py        # Object creation/editing tools
│       │   └── animation.py      # Animation tools
│       ├── resources/            # Resource implementations
│       │   ├── __init__.py
│       │   └── scene_info.py     # Scene information resources
│       └── prompts/              # Prompt templates
│           ├── __init__.py
│           └── modeling.py       # Modeling-related prompts
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_tools.py
├── pyproject.toml                # Project configuration
├── README.md                     # Project documentation
└── AGENTS.md                     # This file
```

### 4. FastMCP Server Setup

#### Basic Server Structure
```python
from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Maya MCP")

# Define tools
@mcp.tool
def my_tool(param: str) -> dict:
    """Tool description."""
    return {'result': 'success'}

# Define resources
@mcp.resource("maya://resource-name")
def my_resource() -> str:
    """Resource description."""
    return "resource data"

# Define prompts
@mcp.prompt()
def my_prompt() -> str:
    """Prompt description."""
    return "prompt template"

# Run the server
if __name__ == "__main__":
    mcp.run()
```

#### Tool Design Guidelines
- **Single responsibility** - Each tool should do one thing well
- **Idempotent when possible** - Tools should be safe to call multiple times
- **Return structured data** - Use dictionaries or Pydantic models for complex returns
- **Validate inputs** - Check parameters before performing operations
- **Handle Maya state** - Consider Maya's undo queue and scene state

#### Resource Design Guidelines
- **Read-only** - Resources should not modify Maya state
- **Cacheable** - Resources should be safe to cache by MCP clients
- **URI-based** - Use meaningful URIs like `maya://scene/objects` or `maya://selection`

#### Prompt Design Guidelines
- **Context-aware** - Prompts should guide LLM behavior based on Maya context
- **Reusable** - Prompts should be templates that can be filled with context
- **Descriptive** - Prompts should clearly explain their purpose

### 5. Maya Integration

#### Maya Availability
- **Check Maya availability** - Tools should handle cases where Maya is not running
- **Graceful degradation** - Return helpful error messages when Maya is unavailable
- **Connection handling** - If using Maya standalone or remote, handle connection errors

#### Common Maya Operations
- **Object creation** - Use `maya.cmds.polyCube()`, `maya.cmds.polySphere()`, etc.
- **Selection** - Use `maya.cmds.select()` and `maya.cmds.ls(selection=True)`
- **Query operations** - Use `maya.cmds.getAttr()`, `maya.cmds.listAttr()`, etc.
- **Scene operations** - Use `maya.cmds.file()` for file operations

#### Error Handling for Maya
```python
try:
    import maya.cmds as cmds
except ImportError:
    # Maya not available
    return {'status': 'error', 'message': 'Maya is not available'}

try:
    result = cmds.someCommand()
except RuntimeError as err:
    # Maya-specific error
    return {'status': 'error', 'message': f'Maya error: {err}'}
except Exception as err:
    # Unexpected error
    return {'status': 'error', 'message': f'Unexpected error: {err}'}
```

### 6. Testing

#### Test Structure
- **Unit tests** - Test individual tools in isolation
- **Mock Maya** - Use mocks or test fixtures for Maya API calls
- **Test error cases** - Test error handling and edge cases
- **No Maya dependency** - Tests should not require Maya to be installed

#### Running Tests
```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=src/maya_mcp --cov-report=term-missing
```

### 7. Installation and Distribution

#### Development Installation
```bash
# Using pip
pip install -e .

# Using uv
uv pip install -e .
```

#### Distribution
- **Version management** - Use semantic versioning
- **Dependencies** - List all required dependencies in `pyproject.toml`
- **Entry points** - Define entry points for running the server
- **Documentation** - Keep README.md updated with usage examples

### 8. Common Tasks

#### Adding a New Tool
1. Create or edit a file in `src/maya_mcp/tools/`
2. Import FastMCP instance: `from maya_mcp import mcp`
3. Define the tool with `@mcp.tool` decorator
4. Add type hints and docstring
5. Implement error handling
6. Add tests in `tests/test_tools.py`

#### Adding a New Resource
1. Create or edit a file in `src/maya_mcp/resources/`
2. Import FastMCP instance: `from maya_mcp import mcp`
3. Define the resource with `@mcp.resource("maya://uri")` decorator
4. Return the resource data
5. Add tests if needed

#### Adding a New Prompt
1. Create or edit a file in `src/maya_mcp/prompts/`
2. Import FastMCP instance: `from maya_mcp import mcp`
3. Define the prompt with `@mcp.prompt()` decorator
4. Return the prompt template
5. Document the prompt's purpose

### 9. Code Review Checklist

Before submitting code, ensure:
- [ ] Type hints added to all functions
- [ ] No bare `except:` clauses
- [ ] Proper error handling for Maya operations
- [ ] Docstrings added to all tools/resources/prompts
- [ ] Follows FastMCP patterns
- [ ] Tests added for new functionality
- [ ] Maya availability checked where needed
- [ ] Cross-platform compatibility considered (Windows/Mac/Linux)
- [ ] No hardcoded paths
- [ ] Resources are read-only
- [ ] Tools are idempotent when possible

### 10. Common Pitfalls to Avoid

#### ❌ Don't Do This:
```python
# Bare exception
@mcp.tool
def bad_tool():
    try:
        cmds.polyCube()
    except:  # Bad!
        pass

# Missing type hints
@mcp.tool
def bad_tool(name):  # Missing type hint
    ...

# Modifying state in resources
@mcp.resource("maya://bad")
def bad_resource():
    cmds.polyCube()  # Resources should be read-only!
    return "data"

# No error handling
@mcp.tool
def bad_tool(name: str):
    cmds.select(name)  # What if name doesn't exist?
```

#### ✅ Do This Instead:
```python
# Specific exceptions
@mcp.tool
def good_tool(name: str) -> dict[str, str]:
    """Select an object by name."""
    try:
        import maya.cmds as cmds
        if not cmds.objExists(name):
            return {'status': 'error', 'message': f'{name} does not exist'}
        cmds.select(name)
        return {'status': 'success', 'message': f'Selected {name}'}
    except RuntimeError as err:
        return {'status': 'error', 'message': f'Maya error: {err}'}

# Read-only resources
@mcp.resource("maya://good")
def good_resource() -> dict:
    """Get scene information."""
    import maya.cmds as cmds
    return {
        'object_count': len(cmds.ls()),
        'selected': cmds.ls(selection=True)
    }
```

### 11. Documentation

#### Docstrings
- Use Google or NumPy style docstrings
- **Add Args, Returns, and Raises sections** to docstrings where appropriate
- Example:
```python
@mcp.tool
def create_sphere(name: str, radius: float = 1.0) -> dict[str, str]:
    """Create a polygonal sphere in Maya.
    
    Args:
        name: Name for the sphere transform node.
        radius: Radius of the sphere (default: 1.0).
    
    Returns:
        Dictionary with 'status' ('success' or 'error') and 'message' keys.
        On success, 'node' key contains the created node name.
    
    Raises:
        RuntimeError: If Maya is not available or command fails.
    """
    ...
```

### 12. References

- **FastMCP Documentation** - https://gofastmcp.com/
- **MCP Specification** - https://modelcontextprotocol.io/
- **Maya Python API** - Autodesk Maya documentation
- **Python Type Hints** - PEP 484, PEP 526

### 13. Git Workflow

#### Branch Management
- **NEVER push directly to main branch** - Always create a feature or bugfix branch first
- **Feature branches** - For new features, enhancements, or additions
  - Format: `feature/descriptive-name`
  - Examples: `feature/add-polygon-extrude`, `feature/add-camera-operations`
- **Bugfix branches** - For bug fixes and corrections
  - Format: `bugfix/descriptive-name` or `fix/descriptive-name`
  - Examples: `bugfix/fix-test-assertion`, `fix/correct-type-hint`

#### Workflow Steps
1. **Check current branch**: `git branch --show-current`
2. **Create feature/bugfix branch**: `git checkout -b feature/name` or `git checkout -b bugfix/name`
3. **Make changes** - Edit files, add tests, update documentation
4. **Stage changes**: `git add <files>` or `git add -A`
5. **Commit changes**: `git commit -m "feat: description"` or `git commit -m "fix: description"`
6. **Push to feature branch**: `git push -u origin feature/name` (NOT main!)
7. **Create Pull Request** - Use GitHub UI or `gh pr create`

#### Commit Message Format
- **Features**: `feat: Add polygon extrude tool`
- **Bugfixes**: `fix: Correct type hint in safety module`
- **Documentation**: `docs: Add missing functionality analysis`
- **Tests**: `test: Add tests for polygon operations`
- **Refactoring**: `refactor: Improve error handling`

#### Important Rules
- ✅ **DO**: Create feature/bugfix branches for all changes
- ✅ **DO**: Push to feature branches, then create PRs
- ❌ **DON'T**: Commit or push directly to `main` branch
- ❌ **DON'T**: Force push to shared branches
- ❌ **DON'T**: Skip creating a branch for "small" changes

### 14. Quick Reference

#### Common Imports
```python
from typing import Dict, List, Optional
from fastmcp import FastMCP
import maya.cmds as cmds  # When Maya is available
```

#### Common Patterns
```python
# Tool pattern
@mcp.tool
def my_tool(param: str) -> dict[str, str]:
    """Tool description."""
    try:
        import maya.cmds as cmds
        # Tool implementation
        return {'status': 'success', 'result': '...'}
    except Exception as err:
        return {'status': 'error', 'message': str(err)}

# Resource pattern
@mcp.resource("maya://my-resource")
def my_resource() -> dict:
    """Resource description."""
    import maya.cmds as cmds
    return {'data': '...'}

# Prompt pattern
@mcp.prompt()
def my_prompt() -> str:
    """Prompt description."""
    return "Prompt template with {placeholders}"
```

## 🚀 Quick Start for Agents

When asked to modify or add code:

1. **Create a feature or bugfix branch** - NEVER commit directly to main
   - Feature branches: `feature/descriptive-name`
   - Bugfix branches: `bugfix/descriptive-name` or `fix/descriptive-name`
   - Example: `git checkout -b feature/add-polygon-extrude-tool`
2. **Read the relevant files** - Understand the existing code structure
3. **Follow FastMCP patterns** - Use decorators and follow MCP conventions
4. **Add type hints** - Always include type information
5. **Handle errors** - Use specific exceptions and return structured errors
6. **Test Maya availability** - Check if Maya is available before using it
7. **Add tests** - Write tests for new functionality
8. **Update docs** - Add/update docstrings as needed
9. **Run tests** - Ensure tests pass before submitting
10. **Commit and push to feature branch** - Never push directly to main
    - Commit: `git commit -m "feat: description"` or `git commit -m "fix: description"`
    - Push: `git push -u origin feature/branch-name`

---

**Last Updated:** 2026-02-22
**Python Version:** 3.10+ (3.11+ recommended)
**FastMCP Version:** 2.0+
