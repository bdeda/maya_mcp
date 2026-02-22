"""Query tools for Maya - Safe read-only operations."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def list_objects(
    type_filter: str | None = None,
    long_names: bool = False,
    selection: bool = False
) -> dict[str, Any]:
    """List objects in the Maya scene.
    
    Args:
        type_filter: Optional type filter (e.g., 'mesh', 'transform', 'joint').
        long_names: Whether to return long names (full path).
        selection: If True, only list selected objects.
    
    Returns:
        Dictionary with 'status', 'objects' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'objects': [],
        }
    
    try:
        kwargs = {}
        if type_filter:
            kwargs['type'] = type_filter
        if long_names:
            kwargs['long'] = True
        if selection:
            kwargs['selection'] = True
        
        objects = cmds.ls(**kwargs) or []
        
        return {
            'status': 'success',
            'objects': objects,
            'count': len(objects),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'objects': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'objects': [],
        }


@mcp.tool
def object_exists(name: str) -> dict[str, bool | str]:
    """Check if an object exists in the scene.
    
    Args:
        name: Name of the object to check.
    
    Returns:
        Dictionary with 'status', 'exists' (bool), and optionally 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'exists': False,
        }
    
    try:
        exists = cmds.objExists(name)
        return {
            'status': 'success',
            'exists': exists,
            'name': name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'exists': False,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'exists': False,
        }


@mcp.tool
def get_object_type(name: str) -> dict[str, str]:
    """Get the type of an object.
    
    Args:
        name: Name of the object.
    
    Returns:
        Dictionary with 'status', 'type' (object type), and optionally 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'type': '',
        }
    
    try:
        if not cmds.objExists(name):
            return {
                'status': 'error',
                'message': f'Object "{name}" does not exist',
                'type': '',
            }
        
        obj_type = cmds.objectType(name)
        return {
            'status': 'success',
            'type': obj_type,
            'name': name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'type': '',
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'type': '',
        }


@mcp.tool
def get_attribute_value(
    object_name: str,
    attribute: str,
    time: float | None = None
) -> dict[str, Any]:
    """Get the value of an attribute.
    
    Args:
        object_name: Name of the object.
        attribute: Name of the attribute (e.g., 'translateX', 'visibility').
        time: Optional time value for animated attributes.
    
    Returns:
        Dictionary with 'status', 'value', and optionally 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'value': None,
        }
    
    try:
        if not cmds.objExists(object_name):
            return {
                'status': 'error',
                'message': f'Object "{object_name}" does not exist',
                'value': None,
            }
        
        attr_name = f'{object_name}.{attribute}'
        if not cmds.objExists(attr_name):
            return {
                'status': 'error',
                'message': f'Attribute "{attr_name}" does not exist',
                'value': None,
            }
        
        if time is not None:
            value = cmds.getAttr(attr_name, time=time)
        else:
            value = cmds.getAttr(attr_name)
        
        return {
            'status': 'success',
            'value': value,
            'attribute': attr_name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'value': None,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'value': None,
        }


@mcp.tool
def list_attributes(
    object_name: str,
    keyable: bool = False,
    readable: bool = False,
    writable: bool = False,
    multi: bool = False,
    scalar: bool = False,
    numeric: bool = False
) -> dict[str, Any]:
    """List attributes of an object.
    
    Args:
        object_name: Name of the object.
        keyable: If True, only list keyable attributes.
        readable: If True, only list readable attributes.
        writable: If True, only list writable attributes.
        multi: If True, only list multi attributes.
        scalar: If True, only list scalar attributes.
        numeric: If True, only list numeric attributes.
    
    Returns:
        Dictionary with 'status', 'attributes' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'attributes': [],
        }
    
    try:
        if not cmds.objExists(object_name):
            return {
                'status': 'error',
                'message': f'Object "{object_name}" does not exist',
                'attributes': [],
            }
        
        kwargs = {}
        if keyable:
            kwargs['keyable'] = True
        if readable:
            kwargs['readable'] = True
        if writable:
            kwargs['writable'] = True
        if multi:
            kwargs['multi'] = True
        if scalar:
            kwargs['scalar'] = True
        if numeric:
            kwargs['numeric'] = True
        
        attrs = cmds.listAttr(object_name, **kwargs) or []
        
        return {
            'status': 'success',
            'attributes': attrs,
            'count': len(attrs),
            'object': object_name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'attributes': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'attributes': [],
        }


@mcp.tool
def get_connection_info(
    attribute: str,
    source: bool = True,
    destination: bool = False
) -> dict[str, Any]:
    """Get connection information for an attribute.
    
    Args:
        attribute: Full attribute name (e.g., 'pCube1.translateX').
        source: If True, get source connections.
        destination: If True, get destination connections.
    
    Returns:
        Dictionary with 'status', 'connections' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'connections': [],
        }
    
    try:
        if not cmds.objExists(attribute):
            return {
                'status': 'error',
                'message': f'Attribute "{attribute}" does not exist',
                'connections': [],
            }
        
        connections = []
        if source:
            src_conns = cmds.listConnections(attribute, source=True, destination=False) or []
            connections.extend([{'type': 'source', 'attribute': attr} for attr in src_conns])
        
        if destination:
            dst_conns = cmds.listConnections(attribute, source=False, destination=True) or []
            connections.extend([{'type': 'destination', 'attribute': attr} for attr in dst_conns])
        
        return {
            'status': 'success',
            'connections': connections,
            'count': len(connections),
            'attribute': attribute,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'connections': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'connections': [],
        }


__all__ = [
    'list_objects',
    'object_exists',
    'get_object_type',
    'get_attribute_value',
    'list_attributes',
    'get_connection_info',
]
