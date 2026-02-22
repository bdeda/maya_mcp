"""Scene manipulation tools for Maya."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def get_selection() -> dict[str, list[str] | str]:
    """Get currently selected objects in Maya.
    
    Returns:
        Dictionary with 'status' ('success' or 'error'), 'selection' (list of object names),
        and optionally 'message' for errors.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'selection': [],
        }
    
    try:
        selection = cmds.ls(selection=True) or []
        return {
            'status': 'success',
            'selection': selection,
            'count': len(selection),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'selection': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'selection': [],
        }


@mcp.tool
def select_objects(names: list[str]) -> dict[str, str]:
    """Select objects by name in Maya.
    
    Args:
        names: List of object names to select.
    
    Returns:
        Dictionary with 'status' ('success' or 'error') and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not names:
        return {
            'status': 'error',
            'message': 'No object names provided',
        }
    
    try:
        # Filter to only existing objects
        existing = [name for name in names if cmds.objExists(name)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {names}',
            }
        
        cmds.select(existing, replace=True)
        
        missing = [name for name in names if name not in existing]
        message = f'Selected {len(existing)} object(s)'
        if missing:
            message += f'. Note: {len(missing)} object(s) not found: {missing}'
        
        return {
            'status': 'success',
            'message': message,
            'selected': existing,
            'missing': missing,
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
def clear_selection() -> dict[str, str]:
    """Clear the current selection in Maya.
    
    Returns:
        Dictionary with 'status' ('success' or 'error') and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        cmds.select(clear=True)
        return {
            'status': 'success',
            'message': 'Selection cleared',
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


__all__ = ["get_selection", "select_objects", "clear_selection"]
