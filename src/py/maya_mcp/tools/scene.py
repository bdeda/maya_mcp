"""Scene manipulation tools for Maya."""

from typing import TYPE_CHECKING, Any

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


@mcp.tool
def select_with_mode(
    objects: list[str],
    mode: str = 'replace'
) -> dict[str, Any]:
    """Select objects with different selection modes.
    
    Args:
        objects: List of object names to select.
        mode: Selection mode - 'replace' (default), 'add', 'toggle', 'deselect'.
    
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
            'message': 'No object names provided',
        }
    
    valid_modes = ['replace', 'add', 'toggle', 'deselect']
    if mode not in valid_modes:
        return {
            'status': 'error',
            'message': f'Invalid mode "{mode}". Must be one of: {valid_modes}',
        }
    
    try:
        # Filter to only existing objects
        existing = [name for name in objects if cmds.objExists(name)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        if mode == 'replace':
            cmds.select(existing, replace=True)
        elif mode == 'add':
            cmds.select(existing, add=True)
        elif mode == 'toggle':
            cmds.select(existing, toggle=True)
        elif mode == 'deselect':
            cmds.select(existing, deselect=True)
        
        missing = [name for name in objects if name not in existing]
        message = f'Selected {len(existing)} object(s) (mode: {mode})'
        if missing:
            message += f'. Note: {len(missing)} object(s) not found: {missing}'
        
        return {
            'status': 'success',
            'message': message,
            'selected': existing,
            'missing': missing,
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
def set_selection_mode(mode: str) -> dict[str, Any]:
    """Set the selection mode (object, component, etc.).
    
    Args:
        mode: Selection mode - 'object', 'component', 'root', 'leaf', 'template', 'none'.
    
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
    
    valid_modes = ['object', 'component', 'root', 'leaf', 'template', 'none']
    if mode not in valid_modes:
        return {
            'status': 'error',
            'message': f'Invalid mode "{mode}". Must be one of: {valid_modes}',
        }
    
    try:
        cmds.selectMode(query=False, mode=mode)
        
        return {
            'status': 'success',
            'message': f'Set selection mode to {mode}',
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
def get_selection_mode() -> dict[str, Any]:
    """Get the current selection mode.
    
    Returns:
        Dictionary with 'status', 'mode', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'mode': None,
        }
    
    try:
        mode = cmds.selectMode(query=True, mode=True)
        
        return {
            'status': 'success',
            'message': f'Current selection mode: {mode}',
            'mode': mode,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'mode': None,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'mode': None,
        }


@mcp.tool
def set_selection_type(
    component_type: str,
    enabled: bool = True
) -> dict[str, Any]:
    """Set selection type (what types of components can be selected).
    
    Args:
        component_type: Component type - 'vertex', 'edge', 'face', 'uv', 'facet', 'hull', 'pivot'.
        enabled: If True, enable selection of this type. If False, disable.
    
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
    
    valid_types = ['vertex', 'edge', 'face', 'uv', 'facet', 'hull', 'pivot']
    if component_type not in valid_types:
        return {
            'status': 'error',
            'message': f'Invalid component type "{component_type}". Must be one of: {valid_types}',
        }
    
    try:
        # Map component types to Maya's internal names
        type_map = {
            'vertex': 'vertex',
            'edge': 'edge',
            'face': 'face',
            'uv': 'uv',
            'facet': 'facet',
            'hull': 'hull',
            'pivot': 'pivot',
        }
        
        maya_type = type_map[component_type]
        cmds.selectType(maya_type, state=enabled)
        
        return {
            'status': 'success',
            'message': f'Set selection type {component_type} to {"enabled" if enabled else "disabled"}',
            'component_type': component_type,
            'enabled': enabled,
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
def highlight_object(object_name: str, highlight: bool = True) -> dict[str, Any]:
    """Highlight or unhighlight an object.
    
    Args:
        object_name: Name of the object to highlight/unhighlight.
        highlight: If True, highlight the object. If False, remove highlight.
    
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
        if not cmds.objExists(object_name):
            return {
                'status': 'error',
                'message': f'Object "{object_name}" does not exist',
            }
        
        cmds.hilite(object_name, replace=highlight)
        
        return {
            'status': 'success',
            'message': f'{"Highlighted" if highlight else "Unhighlighted"} {object_name}',
            'object': object_name,
            'highlighted': highlight,
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
def get_selection_preferences() -> dict[str, Any]:
    """Get current selection preferences.
    
    Returns:
        Dictionary with 'status', 'preferences' (dict), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'preferences': {},
        }
    
    try:
        # Query various selection preferences
        preferences = {
            'trackSelectionOrder': cmds.selectPref(query=True, trackSelectionOrder=True),
            'popupSelection': cmds.selectPref(query=True, popupSelection=True),
            'useDepth': cmds.selectPref(query=True, useDepth=True),
            'autoSelectBackfaces': cmds.selectPref(query=True, autoSelectBackfaces=True),
        }
        
        return {
            'status': 'success',
            'message': 'Retrieved selection preferences',
            'preferences': preferences,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'preferences': {},
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'preferences': {},
        }


@mcp.tool
def set_selection_preference(
    preference_name: str,
    value: bool
) -> dict[str, Any]:
    """Set a selection preference.
    
    Args:
        preference_name: Name of the preference - 'trackSelectionOrder', 'popupSelection', 
                        'useDepth', 'autoSelectBackfaces'.
        value: Value to set (True/False).
    
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
    
    valid_preferences = ['trackSelectionOrder', 'popupSelection', 'useDepth', 'autoSelectBackfaces']
    if preference_name not in valid_preferences:
        return {
            'status': 'error',
            'message': f'Invalid preference "{preference_name}". Must be one of: {valid_preferences}',
        }
    
    try:
        kwargs = {preference_name: value}
        cmds.selectPref(**kwargs)
        
        return {
            'status': 'success',
            'message': f'Set selection preference {preference_name} to {value}',
            'preference': preference_name,
            'value': value,
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
    "get_selection",
    "select_objects",
    "select_with_mode",
    "clear_selection",
    "set_selection_mode",
    "get_selection_mode",
    "set_selection_type",
    "highlight_object",
    "get_selection_preferences",
    "set_selection_preference",
]
