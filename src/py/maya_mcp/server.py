"""Core FastMCP server setup and initialization."""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

# Import mcp from the parent module to avoid circular imports
# This will be set up in __init__.py
try:
    from maya_mcp import mcp
except ImportError:
    # Fallback if imported before __init__.py sets up mcp
    from fastmcp import FastMCP
    mcp = FastMCP("Maya MCP")


def check_maya_available() -> bool:
    """Check if Maya is available in the current Python environment.
    
    Returns:
        True if Maya is available, False otherwise.
    """
    try:
        import maya.cmds  # noqa: F401
        return True
    except ImportError:
        return False


def get_maya_version() -> str | None:
    """Get the Maya version if available.
    
    Returns:
        Maya version string (e.g., "2024.0") or None if Maya is not available.
    """
    try:
        import maya.cmds as cmds
        return cmds.about(version=True)
    except (ImportError, RuntimeError):
        return None


# Register a basic status tool to verify the server is working
@mcp.tool
def get_server_status() -> dict[str, str | bool]:
    """Get the status of the Maya MCP server.
    
    Returns:
        Dictionary with server status information including:
        - 'status': 'running'
        - 'maya_available': Whether Maya is available
        - 'maya_version': Maya version string if available, None otherwise
    """
    maya_available = check_maya_available()
    maya_version = get_maya_version() if maya_available else None
    
    return {
        'status': 'running',
        'maya_available': maya_available,
        'maya_version': maya_version or 'N/A',
    }


# Register a basic resource for server information
@mcp.resource("maya://server/status")
def server_status_resource() -> dict[str, str | bool]:
    """Get server status as a resource.
    
    Returns:
        Dictionary with server status information.
    """
    return get_server_status()


__all__ = ["check_maya_available", "get_maya_version"]
