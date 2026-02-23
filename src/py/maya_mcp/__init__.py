"""Maya MCP Server - FastMCP-based Model Context Protocol server for Autodesk Maya."""

import sys
import io

# Fix stdio handling for Maya's Python environment BEFORE importing FastMCP
# This must happen early because FastMCP may access sys.stdin.buffer, sys.stdout.buffer, etc. during import
def _fix_maya_stdio_early() -> None:
    """Fix stdio handling for Maya's Python environment (early initialization).
    
    This must be called before importing FastMCP to ensure sys.stdin.buffer,
    sys.stdout.buffer, and sys.stderr.buffer exist when FastMCP tries to access them.
    
    Uses file descriptors when available, otherwise creates proper TextIOWrapper/BufferedWriter
    objects that anyio can work with.
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
    
    def _fix_stream(stream, is_input: bool = True, name: str = 'stream'):
        """Fix a stdio stream by creating proper TextIOWrapper/BufferedWriter."""
        try:
            # Try to get file descriptor first (most compatible approach)
            if hasattr(stream, 'fileno'):
                try:
                    fd = stream.fileno()
                    # Create proper binary buffer from file descriptor
                    if is_input:
                        binary_buffer = io.FileIO(fd, 'rb')
                    else:
                        binary_buffer = io.FileIO(fd, 'wb')
                    # Create TextIOWrapper that wraps the binary buffer
                    text_wrapper = io.TextIOWrapper(
                        binary_buffer,
                        encoding='utf-8',
                        line_buffering=not is_input  # Line buffering for output streams
                    )
                    return text_wrapper
                except (OSError, AttributeError, ValueError):
                    # File descriptor approach failed, fall through to wrapper approach
                    pass
        except (AttributeError, OSError):
            # No fileno method, fall through to wrapper approach
            pass
        
        # Fallback: Create wrapper with proper buffer that anyio can use
        class BufferWrapper(io.BufferedIOBase):
            """Binary buffer wrapper for streams that anyio can use."""
            def __init__(self, stream):
                super().__init__()
                self._stream = stream
                self._closed = False
                # Try to get fileno if available
                try:
                    if hasattr(stream, 'fileno'):
                        self._fd = stream.fileno()
                    else:
                        self._fd = None
                except (OSError, AttributeError):
                    self._fd = None
            
            def fileno(self) -> int:
                """Return file descriptor if available."""
                if self._fd is not None:
                    return self._fd
                raise OSError("fileno not available")
            
            def closed(self) -> bool:
                """Check if buffer is closed."""
                return self._closed
            
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
            
            def readinto(self, buffer) -> int:
                """Read bytes into a buffer."""
                if not is_input:
                    raise OSError("not readable")
                data = self.read(len(buffer))
                buffer[:len(data)] = data
                return len(data)
            
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
            
            def close(self) -> None:
                """Close the stream."""
                if not self._closed:
                    self._closed = True
                    if hasattr(self._stream, 'close'):
                        try:
                            self._stream.close()
                        except (OSError, AttributeError):
                            pass
            
            def __enter__(self):
                """Context manager entry."""
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                """Context manager exit."""
                self.close()
                return False
            
            def readable(self) -> bool:
                """Check if buffer is readable."""
                return is_input
            
            def writable(self) -> bool:
                """Check if buffer is writable."""
                return not is_input
            
            def seekable(self) -> bool:
                """Check if buffer is seekable."""
                return False
        
        class StdioWrapper:
            """Wrapper for stdio streams that provides buffer attribute for Maya compatibility."""
            def __init__(self, original):
                self._original = original
                self.buffer = BufferWrapper(original)
                # Try to preserve fileno if available
                try:
                    if hasattr(original, 'fileno'):
                        self.fileno = original.fileno
                except (AttributeError, OSError):
                    pass
            
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
        
        return StdioWrapper(stream)
    
    # Fix stdin
    if _needs_fix(sys.stdin):
        sys.stdin = _fix_stream(sys.stdin, is_input=True, name='stdin')
    
    # Fix stdout
    if _needs_fix(sys.stdout):
        sys.stdout = _fix_stream(sys.stdout, is_input=False, name='stdout')
    
    # Fix stderr
    if _needs_fix(sys.stderr):
        sys.stderr = _fix_stream(sys.stderr, is_input=False, name='stderr')

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
