"""Entry point for running the Maya MCP server."""

import sys
from pathlib import Path

# Add the package to the path if running as a script
if __name__ == "__main__":
    # Ensure we can import maya_mcp
    # __file__ is src/py/maya_mcp/__main__.py
    # We need src/py in the path to import maya_mcp
    package_dir = Path(__file__).parent.parent  # src/py
    if str(package_dir) not in sys.path:
        sys.path.insert(0, str(package_dir))

from maya_mcp import mcp


def main() -> None:
    """Run the Maya MCP server.
    
    This can be called from:
    - Within Maya: import maya_mcp; maya_mcp.__main__.main()
    - From mayapy: python -m maya_mcp
    - As a script: maya-mcp (if installed)
    """
    try:
        # Check if Maya is available
        try:
            import maya.cmds as cmds
            maya_available = True
            print("Maya MCP Server: Maya is available", file=sys.stderr)
        except ImportError:
            maya_available = False
            print(
                "Maya MCP Server: Warning - Maya is not available. "
                "Some tools may not work.",
                file=sys.stderr
            )
        
        # Run the MCP server
        mcp.run()
    except KeyboardInterrupt:
        print("\nMaya MCP Server: Shutting down...", file=sys.stderr)
        sys.exit(0)
    except Exception as err:
        print(f"Maya MCP Server: Error - {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
