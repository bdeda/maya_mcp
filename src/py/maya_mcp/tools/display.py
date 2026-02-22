"""Display and viewport tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def set_display_mode(
    objects: list[str],
    mode: str = 'wireframe'
) -> dict[str, Any]:
    """Set the display mode for objects.
    
    Args:
        objects: List of object names.
        mode: Display mode ('wireframe', 'shaded', 'boundingBox', 'points', etc.).
    
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
    
    if not objects:
        return {
            'status': 'error',
            'message': 'No objects provided',
        }
    
    try:
        # Filter to only existing objects
        existing = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        for obj in existing:
            cmds.setAttr(f'{obj}.overrideDisplayType', 2)  # Wireframe
            if mode == 'shaded':
                cmds.setAttr(f'{obj}.overrideDisplayType', 0)  # Normal
            elif mode == 'boundingBox':
                cmds.setAttr(f'{obj}.overrideDisplayType', 1)  # Bounding box
            elif mode == 'points':
                cmds.setAttr(f'{obj}.overrideDisplayType', 3)  # Points
        
        return {
            'status': 'success',
            'message': f'Set display mode "{mode}" for {len(existing)} object(s)',
            'objects': existing,
            'mode': mode,
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
def set_visibility(
    objects: list[str],
    visible: bool = True
) -> dict[str, Any]:
    """Set the visibility of objects.
    
    Args:
        objects: List of object names.
        visible: If True, make objects visible; if False, hide them.
    
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
    
    if not objects:
        return {
            'status': 'error',
            'message': 'No objects provided',
        }
    
    try:
        # Filter to only existing objects
        existing = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        for obj in existing:
            cmds.setAttr(f'{obj}.visibility', visible)
        
        return {
            'status': 'success',
            'message': f'Set visibility to {visible} for {len(existing)} object(s)',
            'objects': existing,
            'visible': visible,
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
def refresh_viewport() -> dict[str, Any]:
    """Refresh all viewports.
    
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
        cmds.refresh()
        
        return {
            'status': 'success',
            'message': 'Refreshed viewports',
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
    'set_display_mode',
    'set_visibility',
    'refresh_viewport',
]
