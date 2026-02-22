"""Rendering tools for Maya - playblast and software rendering."""

from typing import TYPE_CHECKING, Any
from pathlib import Path

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_playblast(
    file_path: str,
    start_frame: float | None = None,
    end_frame: float | None = None,
    width: int = 1920,
    height: int = 1080,
    format: str = 'qt',
    quality: int = 100,
    compression: str = 'H.264'
) -> dict[str, Any]:
    """Create a playblast (viewport render) of the animation.
    
    Args:
        file_path: Path to save the playblast file.
        start_frame: Optional start frame. If None, use current time.
        end_frame: Optional end frame. If None, use current time.
        width: Width in pixels (default: 1920).
        height: Height in pixels (default: 1080).
        format: Output format ('qt', 'image', 'avi').
        quality: Quality percentage (0-100, default: 100).
        compression: Compression codec for video formats.
    
    Returns:
        Dictionary with 'status', 'file_path', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        # Get time range if not provided
        if start_frame is None:
            start_frame = cmds.playbackOptions(query=True, minTime=True)
        if end_frame is None:
            end_frame = cmds.playbackOptions(query=True, maxTime=True)
        
        kwargs = {
            'filename': file_path,
            'startTime': start_frame,
            'endTime': end_frame,
            'width': width,
            'height': height,
            'format': format,
            'quality': quality,
            'compression': compression,
            'forceOverwrite': True,
        }
        
        result = cmds.playblast(**kwargs)
        
        return {
            'status': 'success',
            'message': f'Created playblast: {file_path}',
            'file_path': file_path,
            'start_frame': start_frame,
            'end_frame': end_frame,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


@mcp.tool
def render_software(
    file_path: str,
    start_frame: float | None = None,
    end_frame: float | None = None,
    width: int = 1920,
    height: int = 1080,
    camera: str | None = None,
    renderer: str = 'mayaSoftware'
) -> dict[str, Any]:
    """Render using Maya Software Renderer.
    
    Args:
        file_path: Path to save the rendered image(s). Use # for frame numbers (e.g., 'render.####.png').
        start_frame: Optional start frame. If None, use current time.
        end_frame: Optional end frame. If None, use current time.
        width: Width in pixels (default: 1920).
        height: Height in pixels (default: 1080).
        camera: Optional camera name. If None, use active camera.
        renderer: Renderer to use ('mayaSoftware', 'mayaHardware2', 'mayaVector').
    
    Returns:
        Dictionary with 'status', 'file_path', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        # Set render settings
        cmds.setAttr('defaultResolution.width', width)
        cmds.setAttr('defaultResolution.height', height)
        
        # Set renderer
        cmds.setAttr('defaultRenderGlobals.currentRenderer', renderer, type='string')
        
        # Get time range if not provided
        if start_frame is None:
            start_frame = cmds.playbackOptions(query=True, minTime=True)
        if end_frame is None:
            end_frame = cmds.playbackOptions(query=True, maxTime=True)
        
        # Set frame range
        cmds.setAttr('defaultRenderGlobals.startFrame', start_frame)
        cmds.setAttr('defaultRenderGlobals.endFrame', end_frame)
        
        # Set output file
        cmds.setAttr('defaultRenderGlobals.imageFilePrefix', file_path.replace('#', '<f>'), type='string')
        
        # Set camera if provided
        if camera:
            if not cmds.objExists(camera):
                return {
                    'status': 'error',
                    'message': f'Camera "{camera}" does not exist',
                }
            cmds.setAttr('defaultRenderGlobals.camera', camera, type='string')
        
        # Render
        cmds.render()
        
        return {
            'status': 'success',
            'message': f'Rendered frames {start_frame} to {end_frame}',
            'file_path': file_path,
            'start_frame': start_frame,
            'end_frame': end_frame,
            'renderer': renderer,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


@mcp.tool
def render_current_frame(
    file_path: str,
    width: int = 1920,
    height: int = 1080,
    camera: str | None = None,
    renderer: str = 'mayaSoftware'
) -> dict[str, Any]:
    """Render the current frame using Maya Software Renderer.
    
    Args:
        file_path: Path to save the rendered image.
        width: Width in pixels (default: 1920).
        height: Height in pixels (default: 1080).
        camera: Optional camera name. If None, use active camera.
        renderer: Renderer to use ('mayaSoftware', 'mayaHardware2', 'mayaVector').
    
    Returns:
        Dictionary with 'status', 'file_path', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        current_frame = cmds.currentTime(query=True)
        
        # Set render settings
        cmds.setAttr('defaultResolution.width', width)
        cmds.setAttr('defaultResolution.height', height)
        
        # Set renderer
        cmds.setAttr('defaultRenderGlobals.currentRenderer', renderer, type='string')
        
        # Set single frame
        cmds.setAttr('defaultRenderGlobals.startFrame', current_frame)
        cmds.setAttr('defaultRenderGlobals.endFrame', current_frame)
        
        # Set output file
        cmds.setAttr('defaultRenderGlobals.imageFilePrefix', file_path, type='string')
        
        # Set camera if provided
        if camera:
            if not cmds.objExists(camera):
                return {
                    'status': 'error',
                    'message': f'Camera "{camera}" does not exist',
                }
            cmds.setAttr('defaultRenderGlobals.camera', camera, type='string')
        
        # Render
        cmds.render()
        
        return {
            'status': 'success',
            'message': f'Rendered frame {current_frame}',
            'file_path': file_path,
            'frame': current_frame,
            'renderer': renderer,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


@mcp.tool
def set_render_resolution(
    width: int,
    height: int
) -> dict[str, Any]:
    """Set the render resolution.
    
    Args:
        width: Width in pixels.
        height: Height in pixels.
    
    Returns:
        Dictionary with 'status' and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        cmds.setAttr('defaultResolution.width', width)
        cmds.setAttr('defaultResolution.height', height)
        
        return {
            'status': 'success',
            'message': f'Set render resolution to {width}x{height}',
            'width': width,
            'height': height,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
        }


__all__ = [
    'create_playblast',
    'render_software',
    'render_current_frame',
    'set_render_resolution',
]
