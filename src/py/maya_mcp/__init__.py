"""Maya MCP Server - FastMCP-based Model Context Protocol server for Autodesk Maya."""

from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("Maya MCP")

# Import server module to register basic tools and resources
from maya_mcp import server  # noqa: F401, E402

# Import tools, resources, and prompts to register them
# Tools are imported via maya_mcp.tools.__init__
from maya_mcp import tools  # noqa: F401, E402

# Additional tools will be imported here as features are developed
# from maya_mcp.resources import scene_info
# from maya_mcp.prompts import modeling

__all__ = ["mcp"]
