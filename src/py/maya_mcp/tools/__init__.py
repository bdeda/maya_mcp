"""Maya MCP tools - Functions that LLM clients can invoke to perform actions in Maya."""

# Import tools to register them with the MCP server
from maya_mcp.tools import animation  # noqa: F401
from maya_mcp.tools import animation_layers  # noqa: F401
from maya_mcp.tools import attributes  # noqa: F401
from maya_mcp.tools import cameras  # noqa: F401
from maya_mcp.tools import constraints  # noqa: F401
from maya_mcp.tools import deformers  # noqa: F401
from maya_mcp.tools import display  # noqa: F401
from maya_mcp.tools import display_layers  # noqa: F401
from maya_mcp.tools import file  # noqa: F401
from maya_mcp.tools import lights  # noqa: F401
from maya_mcp.tools import materials  # noqa: F401
from maya_mcp.tools import mesh  # noqa: F401
from maya_mcp.tools import mesh_editing  # noqa: F401
from maya_mcp.tools import nurbs  # noqa: F401
from maya_mcp.tools import objects  # noqa: F401
from maya_mcp.tools import paint  # noqa: F401
from maya_mcp.tools import query  # noqa: F401
from maya_mcp.tools import rendering  # noqa: F401
from maya_mcp.tools import rigging  # noqa: F401
from maya_mcp.tools import scene  # noqa: F401
from maya_mcp.tools import sets  # noqa: F401
from maya_mcp.tools import skinning  # noqa: F401
from maya_mcp.tools import transform  # noqa: F401
from maya_mcp.tools import usd  # noqa: F401
from maya_mcp.tools import uv  # noqa: F401

__all__: list[str] = []
