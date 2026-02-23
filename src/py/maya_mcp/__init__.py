"""Maya MCP Server - FastMCP-based Model Context Protocol server for Autodesk Maya."""

import sys
import io

# Fix stdio handling for Maya's Python environment BEFORE importing FastMCP
# This must happen early because FastMCP may access sys.stdin.buffer during import
def _fix_maya_stdio_early() -> None:
    """Fix stdio handling for Maya's Python environment (early initialization).
    
    This must be called before importing FastMCP to ensure sys.stdin.buffer
    exists when FastMCP tries to access it.
    """
    # Check if we're in Maya's Python environment and need to fix stdin
    needs_fix = False
    
    # Check if stdin doesn't have a buffer attribute
    if not hasattr(sys.stdin, 'buffer'):
        needs_fix = True
    else:
        # Check if stdin is a StandardInput object (Maya's custom stdin)
        stdin_class_name = getattr(sys.stdin.__class__, '__name__', '')
        if stdin_class_name == 'StandardInput':
            needs_fix = True
    
    if needs_fix:
        # Create a wrapper that provides a buffer attribute compatible with FastMCP
        class StdioWrapper:
            """Wrapper for sys.stdin that provides buffer attribute for Maya compatibility."""
            def __init__(self, original_stdin):
                self._original = original_stdin
                # Create a binary buffer wrapper that inherits from BufferedIOBase
                class BufferWrapper(io.BufferedIOBase):
                    """Binary buffer wrapper for stdin that FastMCP can use."""
                    def __init__(self, stdin_obj):
                        super().__init__()
                        self._stdin = stdin_obj
                    
                    def read(self, size: int = -1) -> bytes:
                        """Read bytes from stdin."""
                        if hasattr(self._stdin, 'read'):
                            text = self._stdin.read(size if size > 0 else -1)
                            if isinstance(text, str):
                                return text.encode('utf-8')
                            elif isinstance(text, bytes):
                                return text
                        return b''
                    
                    def readline(self, size: int = -1) -> bytes:
                        """Read a line of bytes from stdin."""
                        if hasattr(self._stdin, 'readline'):
                            text = self._stdin.readline(size if size > 0 else -1)
                            if isinstance(text, str):
                                return text.encode('utf-8')
                            elif isinstance(text, bytes):
                                return text
                        return b''
                    
                    def readlines(self, hint: int = -1) -> list[bytes]:
                        """Read all lines from stdin."""
                        if hasattr(self._stdin, 'readlines'):
                            lines = self._stdin.readlines(hint if hint > 0 else -1)
                            return [
                                line.encode('utf-8') if isinstance(line, str) else line
                                for line in lines
                            ]
                        return []
                    
                    def __iter__(self):
                        """Make buffer iterable."""
                        return self
                    
                    def __next__(self):
                        """Get next line."""
                        line = self.readline()
                        if not line:
                            raise StopIteration
                        return line
                    
                    def readable(self) -> bool:
                        """Check if buffer is readable."""
                        return True
                    
                    def writable(self) -> bool:
                        """Check if buffer is writable."""
                        return False
                    
                    def seekable(self) -> bool:
                        """Check if buffer is seekable."""
                        return False
                
                self.buffer = BufferWrapper(original_stdin)
            
            def __getattr__(self, name):
                # Delegate all other attributes to the original stdin
                return getattr(self._original, name)
            
            # Ensure common file-like methods are available
            def read(self, size: int = -1) -> str:
                """Read from stdin."""
                return self._original.read(size)
            
            def readline(self, size: int = -1) -> str:
                """Read a line from stdin."""
                return self._original.readline(size)
            
            def readlines(self, hint: int = -1) -> list[str]:
                """Read all lines from stdin."""
                return self._original.readlines(hint)
            
            def __iter__(self):
                """Make stdin iterable."""
                return iter(self._original)
        
        # Replace sys.stdin with our wrapper
        sys.stdin = StdioWrapper(sys.stdin)

# Apply the fix early, before importing FastMCP
_fix_maya_stdio_early()

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
