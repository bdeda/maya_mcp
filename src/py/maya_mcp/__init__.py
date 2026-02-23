"""Maya MCP Server - FastMCP-based Model Context Protocol server for Autodesk Maya."""

import sys
import io

# Fix stdio handling for Maya's Python environment BEFORE importing FastMCP
# This must happen early because FastMCP may access sys.stdin.buffer, sys.stdout.buffer, etc. during import
def _fix_maya_stdio_early() -> None:
    """Fix stdio handling for Maya's Python environment (early initialization).
    
    This must be called before importing FastMCP to ensure sys.stdin.buffer,
    sys.stdout.buffer, and sys.stderr.buffer exist when FastMCP tries to access them.
    """
    def _needs_fix(stream) -> bool:
        """Check if a stream needs fixing."""
        if not hasattr(stream, 'buffer'):
            return True
        # Check if stream is a Maya custom object (StandardInput, Output, etc.)
        stream_class_name = getattr(stream.__class__, '__name__', '')
        if stream_class_name in ('StandardInput', 'Output'):
            return True
        return False
    
    def _create_buffer_wrapper(stream_obj, is_input: bool = True):
        """Create a binary buffer wrapper for a stream."""
        class BufferWrapper(io.BufferedIOBase):
            """Binary buffer wrapper for streams that FastMCP can use."""
            def __init__(self, stream):
                super().__init__()
                self._stream = stream
            
            def read(self, size: int = -1) -> bytes:
                """Read bytes from stream."""
                if not is_input:
                    raise OSError("not readable")
                if hasattr(self._stream, 'read'):
                    text = self._stream.read(size if size > 0 else -1)
                    if isinstance(text, str):
                        return text.encode('utf-8')
                    elif isinstance(text, bytes):
                        return text
                return b''
            
            def readline(self, size: int = -1) -> bytes:
                """Read a line of bytes from stream."""
                if not is_input:
                    raise OSError("not readable")
                if hasattr(self._stream, 'readline'):
                    text = self._stream.readline(size if size > 0 else -1)
                    if isinstance(text, str):
                        return text.encode('utf-8')
                    elif isinstance(text, bytes):
                        return text
                return b''
            
            def readlines(self, hint: int = -1) -> list[bytes]:
                """Read all lines from stream."""
                if not is_input:
                    raise OSError("not readable")
                if hasattr(self._stream, 'readlines'):
                    lines = self._stream.readlines(hint if hint > 0 else -1)
                    return [
                        line.encode('utf-8') if isinstance(line, str) else line
                        for line in lines
                    ]
                return []
            
            def write(self, data: bytes) -> int:
                """Write bytes to stream."""
                if is_input:
                    raise OSError("not writable")
                if hasattr(self._stream, 'write'):
                    if isinstance(data, bytes):
                        text = data.decode('utf-8')
                    else:
                        text = str(data)
                    self._stream.write(text)
                    return len(data)
                return 0
            
            def writelines(self, lines: list[bytes]) -> None:
                """Write lines to stream."""
                if is_input:
                    raise OSError("not writable")
                for line in lines:
                    self.write(line)
            
            def flush(self) -> None:
                """Flush the stream."""
                if hasattr(self._stream, 'flush'):
                    self._stream.flush()
            
            def __iter__(self):
                """Make buffer iterable."""
                return self
            
            def __next__(self):
                """Get next line."""
                if not is_input:
                    raise StopIteration
                line = self.readline()
                if not line:
                    raise StopIteration
                return line
            
            def readable(self) -> bool:
                """Check if buffer is readable."""
                return is_input
            
            def writable(self) -> bool:
                """Check if buffer is writable."""
                return not is_input
            
            def seekable(self) -> bool:
                """Check if buffer is seekable."""
                return False
        
        return BufferWrapper(stream_obj)
    
    def _create_stdio_wrapper(original_stream, is_input: bool = True):
        """Create a wrapper for a stdio stream that provides buffer attribute."""
        class StdioWrapper:
            """Wrapper for stdio streams that provides buffer attribute for Maya compatibility."""
            def __init__(self, original):
                self._original = original
                self.buffer = _create_buffer_wrapper(original, is_input=is_input)
            
            def __getattr__(self, name):
                # Delegate all other attributes to the original stream
                return getattr(self._original, name)
            
            # Ensure common file-like methods are available
            if is_input:
                def read(self, size: int = -1) -> str:
                    """Read from stream."""
                    return self._original.read(size)
                
                def readline(self, size: int = -1) -> str:
                    """Read a line from stream."""
                    return self._original.readline(size)
                
                def readlines(self, hint: int = -1) -> list[str]:
                    """Read all lines from stream."""
                    return self._original.readlines(hint)
                
                def __iter__(self):
                    """Make stream iterable."""
                    return iter(self._original)
            else:
                def write(self, text: str) -> int:
                    """Write to stream."""
                    return self._original.write(text)
                
                def writelines(self, lines: list[str]) -> None:
                    """Write lines to stream."""
                    return self._original.writelines(lines)
                
                def flush(self) -> None:
                    """Flush the stream."""
                    return self._original.flush()
        
        return StdioWrapper(original_stream)
    
    # Fix stdin
    if _needs_fix(sys.stdin):
        sys.stdin = _create_stdio_wrapper(sys.stdin, is_input=True)
    
    # Fix stdout
    if _needs_fix(sys.stdout):
        sys.stdout = _create_stdio_wrapper(sys.stdout, is_input=False)
    
    # Fix stderr
    if _needs_fix(sys.stderr):
        sys.stderr = _create_stdio_wrapper(sys.stderr, is_input=False)

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
