"""Example script to start the Maya MCP server from within Maya.

To use this script:
1. Copy this file to your Maya scripts directory, or
2. Source it from the Script Editor in Maya, or
3. Add it to your Maya userSetup.py

Usage in Maya Script Editor:
    exec(open(r'F:\git\maya_mcp\examples\start_in_maya.py').read())
"""

import sys
from pathlib import Path

# Add the maya_mcp package to the path
# Adjust this path to match your installation
MAYA_MCP_PATH = Path(__file__).parent.parent / "src" / "py"
if str(MAYA_MCP_PATH) not in sys.path:
    sys.path.insert(0, str(MAYA_MCP_PATH))

try:
    import maya_mcp
    
    # Start the MCP server
    # This will run in the background and handle MCP protocol communication
    print("Starting Maya MCP Server...")
    maya_mcp.__main__.main()
except ImportError as err:
    print(f"Failed to import maya_mcp: {err}")
    print(f"Make sure FastMCP is installed: pip install fastmcp")
except Exception as err:
    print(f"Error starting Maya MCP Server: {err}")
