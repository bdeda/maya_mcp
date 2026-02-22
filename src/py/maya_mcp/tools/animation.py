"""Animation tools for Maya - keyframes, time, curves."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def set_keyframe(
    attributes: list[str],
    time: float | None = None,
    value: Any | None = None
) -> dict[str, Any]:
    """Set a keyframe on attributes.
    
    Args:
        attributes: List of attribute names (e.g., ['pCube1.translateX']).
        time: Optional time value. If None, use current time.
        value: Optional value to set. If None, use current attribute value.
    
    Returns:
        Dictionary with 'status', 'keyframes' (list), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'keyframes': [],
        }
    
    if not attributes:
        return {
            'status': 'error',
            'message': 'No attributes provided',
            'keyframes': [],
        }
    
    try:
        kwargs = {}
        if time is not None:
            kwargs['time'] = time
        if value is not None:
            kwargs['value'] = value
        
        keyframes = cmds.setKeyframe(attributes, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Set keyframe(s) on {len(attributes)} attribute(s)',
            'keyframes': keyframes if isinstance(keyframes, list) else [keyframes],
            'attributes': attributes,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'keyframes': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'keyframes': [],
        }


@mcp.tool
def get_keyframe_times(
    attribute: str,
    time_range: tuple[float, float] | None = None
) -> dict[str, Any]:
    """Get keyframe times for an attribute.
    
    Args:
        attribute: Attribute name (e.g., 'pCube1.translateX').
        time_range: Optional (start_time, end_time) tuple.
    
    Returns:
        Dictionary with 'status', 'times' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'times': [],
        }
    
    try:
        if not cmds.objExists(attribute):
            return {
                'status': 'error',
                'message': f'Attribute "{attribute}" does not exist',
                'times': [],
            }
        
        kwargs = {}
        if time_range:
            kwargs['time'] = (time_range[0], time_range[1])
        
        times = cmds.keyframe(attribute, query=True, timeChange=True, **kwargs) or []
        
        return {
            'status': 'success',
            'message': f'Found {len(times)} keyframe(s)',
            'times': times,
            'count': len(times),
            'attribute': attribute,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'times': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'times': [],
        }


@mcp.tool
def set_current_time(time: float) -> dict[str, Any]:
    """Set the current time in the timeline.
    
    Args:
        time: Time value to set.
    
    Returns:
        Dictionary with 'status', 'time', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        cmds.currentTime(time)
        
        return {
            'status': 'success',
            'message': f'Set current time to {time}',
            'time': time,
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
def get_current_time() -> dict[str, Any]:
    """Get the current time in the timeline.
    
    Returns:
        Dictionary with 'status' and 'time'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'time': None,
        }
    
    try:
        time = cmds.currentTime(query=True)
        
        return {
            'status': 'success',
            'time': time,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'time': None,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'time': None,
        }


@mcp.tool
def delete_keyframes(
    attributes: list[str],
    time_range: tuple[float, float] | None = None
) -> dict[str, Any]:
    """Delete keyframes from attributes.
    
    Args:
        attributes: List of attribute names.
        time_range: Optional (start_time, end_time) tuple. If None, delete all keyframes.
    
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
    
    if not attributes:
        return {
            'status': 'error',
            'message': 'No attributes provided',
        }
    
    try:
        kwargs = {}
        if time_range:
            kwargs['time'] = (time_range[0], time_range[1])
        
        cmds.cutKey(attributes, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Deleted keyframes from {len(attributes)} attribute(s)',
            'attributes': attributes,
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
    'set_keyframe',
    'get_keyframe_times',
    'set_current_time',
    'get_current_time',
    'delete_keyframes',
]
