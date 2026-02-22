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


@mcp.tool
def bake_results(
    objects: list[str],
    time_range: tuple[float, float],
    sample_by: float = 1.0,
    attribute: str | None = None
) -> dict[str, Any]:
    """Bake animation results to keyframes.
    
    Args:
        objects: List of object names to bake.
        time_range: (start_time, end_time) tuple.
        sample_by: Sample rate (default 1.0).
        attribute: Optional specific attribute to bake (e.g., 'translateX').
    
    Returns:
        Dictionary with 'status', 'baked_objects', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'baked_objects': [],
        }
    
    if not objects:
        return {
            'status': 'error',
            'message': 'No objects provided',
            'baked_objects': [],
        }
    
    try:
        kwargs = {
            'time': (time_range[0], time_range[1]),
            'sampleBy': sample_by,
        }
        if attribute:
            kwargs['attribute'] = attribute
        
        result = cmds.bakeResults(objects, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Baked animation for {len(objects)} object(s)',
            'baked_objects': result if isinstance(result, list) else [result],
            'time_range': time_range,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'baked_objects': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'baked_objects': [],
        }


@mcp.tool
def bake_simulation(
    objects: list[str],
    time_range: tuple[float, float],
    sample_by: float = 1.0
) -> dict[str, Any]:
    """Bake simulation results to keyframes.
    
    Args:
        objects: List of object names to bake.
        time_range: (start_time, end_time) tuple.
        sample_by: Sample rate (default 1.0).
    
    Returns:
        Dictionary with 'status', 'baked_objects', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'baked_objects': [],
        }
    
    if not objects:
        return {
            'status': 'error',
            'message': 'No objects provided',
            'baked_objects': [],
        }
    
    try:
        kwargs = {
            'time': (time_range[0], time_range[1]),
            'sampleBy': sample_by,
        }
        
        result = cmds.bakeSimulation(objects, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Baked simulation for {len(objects)} object(s)',
            'baked_objects': result if isinstance(result, list) else [result],
            'time_range': time_range,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'baked_objects': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'baked_objects': [],
        }


@mcp.tool
def copy_keyframes(
    attributes: list[str],
    time_range: tuple[float, float] | None = None
) -> dict[str, Any]:
    """Copy keyframes to clipboard.
    
    Args:
        attributes: List of attribute names to copy keyframes from.
        time_range: Optional (start_time, end_time) tuple. If None, copy all keyframes.
    
    Returns:
        Dictionary with 'status', 'copied_count', and 'message'.
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
        
        result = cmds.copyKey(attributes, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Copied keyframes from {len(attributes)} attribute(s)',
            'copied_count': len(result) if isinstance(result, list) else 1,
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


@mcp.tool
def paste_keyframes(
    attributes: list[str],
    time: float | None = None,
    option: str = 'replace'
) -> dict[str, Any]:
    """Paste keyframes from clipboard.
    
    Args:
        attributes: List of attribute names to paste keyframes to.
        time: Optional time to paste at. If None, paste at current time.
        option: Paste option: 'replace', 'insert', 'merge', 'scale', 'fit'.
    
    Returns:
        Dictionary with 'status', 'pasted_count', and 'message'.
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
        kwargs = {
            'option': option,
        }
        if time is not None:
            kwargs['time'] = time
        
        result = cmds.pasteKey(attributes, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Pasted keyframes to {len(attributes)} attribute(s)',
            'pasted_count': len(result) if isinstance(result, list) else 1,
            'attributes': attributes,
            'option': option,
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
def scale_keyframes(
    attributes: list[str],
    time_range: tuple[float, float],
    scale_factor: float = 1.0,
    pivot_time: float | None = None
) -> dict[str, Any]:
    """Scale keyframes in time.
    
    Args:
        attributes: List of attribute names.
        time_range: (start_time, end_time) tuple to scale.
        scale_factor: Scale factor (default 1.0).
        pivot_time: Optional pivot time. If None, use start of range.
    
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
        kwargs = {
            'time': (time_range[0], time_range[1]),
            'scale': scale_factor,
        }
        if pivot_time is not None:
            kwargs['pivot'] = pivot_time
        
        cmds.scaleKey(attributes, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Scaled keyframes for {len(attributes)} attribute(s)',
            'attributes': attributes,
            'scale_factor': scale_factor,
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
def snap_keyframes(
    attributes: list[str],
    time_range: tuple[float, float] | None = None,
    snap_to: float = 1.0
) -> dict[str, Any]:
    """Snap keyframes to nearest time unit.
    
    Args:
        attributes: List of attribute names.
        time_range: Optional (start_time, end_time) tuple. If None, snap all keyframes.
        snap_to: Snap interval (default 1.0).
    
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
        kwargs = {
            'snapTime': snap_to,
        }
        if time_range:
            kwargs['time'] = (time_range[0], time_range[1])
        
        cmds.snapKey(attributes, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Snapped keyframes for {len(attributes)} attribute(s)',
            'attributes': attributes,
            'snap_to': snap_to,
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
def select_keyframes(
    attributes: list[str],
    time_range: tuple[float, float] | None = None,
    add: bool = False
) -> dict[str, Any]:
    """Select keyframes.
    
    Args:
        attributes: List of attribute names.
        time_range: Optional (start_time, end_time) tuple. If None, select all keyframes.
        add: If True, add to selection. If False, replace selection.
    
    Returns:
        Dictionary with 'status', 'selected_count', and 'message'.
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
        kwargs = {
            'add': add,
        }
        if time_range:
            kwargs['time'] = (time_range[0], time_range[1])
        
        result = cmds.selectKey(attributes, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Selected keyframes for {len(attributes)} attribute(s)',
            'selected_count': len(result) if isinstance(result, list) else 1,
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


@mcp.tool
def query_keyframe_info(
    attribute: str,
    time_range: tuple[float, float] | None = None,
    info_type: str = 'time'
) -> dict[str, Any]:
    """Query keyframe information using keyframe command.
    
    Args:
        attribute: Attribute name (e.g., 'pCube1.translateX').
        time_range: Optional (start_time, end_time) tuple.
        info_type: Type of info to query: 'time', 'value', 'tangent', 'inTangentType', 'outTangentType'.
    
    Returns:
        Dictionary with 'status', 'info' (list), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'info': [],
        }
    
    try:
        if not cmds.objExists(attribute):
            return {
                'status': 'error',
                'message': f'Attribute "{attribute}" does not exist',
                'info': [],
            }
        
        kwargs = {
            'query': True,
        }
        if time_range:
            kwargs['time'] = (time_range[0], time_range[1])
        
        # Map info_type to maya.cmds.keyframe parameter
        if info_type == 'time':
            kwargs['timeChange'] = True
        elif info_type == 'value':
            kwargs['valueChange'] = True
        elif info_type == 'tangent':
            kwargs['tangent'] = True
        elif info_type == 'inTangentType':
            kwargs['inTangentType'] = True
        elif info_type == 'outTangentType':
            kwargs['outTangentType'] = True
        else:
            return {
                'status': 'error',
                'message': f'Invalid info_type: {info_type}',
                'info': [],
            }
        
        result = cmds.keyframe(attribute, **kwargs) or []
        
        return {
            'status': 'success',
            'message': f'Queried {info_type} for {attribute}',
            'info': result if isinstance(result, list) else [result],
            'attribute': attribute,
            'info_type': info_type,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'info': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'info': [],
        }


__all__ = [
    'set_keyframe',
    'get_keyframe_times',
    'set_current_time',
    'get_current_time',
    'delete_keyframes',
    'bake_results',
    'bake_simulation',
    'copy_keyframes',
    'paste_keyframes',
    'scale_keyframes',
    'snap_keyframes',
    'select_keyframes',
    'query_keyframe_info',
]
