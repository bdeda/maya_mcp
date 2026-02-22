"""Attribute manipulation tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def set_attribute(
    attribute: str,
    value: Any,
    type: str | None = None
) -> dict[str, Any]:
    """Set the value of an attribute.
    
    Args:
        attribute: Full attribute name (e.g., 'pCube1.translateX').
        value: Value to set.
        type: Optional attribute type (e.g., 'double', 'string', 'int').
    
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
        if not cmds.objExists(attribute):
            return {
                'status': 'error',
                'message': f'Attribute "{attribute}" does not exist',
            }
        
        kwargs = {}
        if type:
            kwargs['type'] = type
        
        cmds.setAttr(attribute, value, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Set {attribute} = {value}',
            'attribute': attribute,
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


@mcp.tool
def add_attribute(
    object_name: str,
    attribute_name: str,
    attribute_type: str = 'double',
    default_value: Any = 0.0,
    min_value: float | None = None,
    max_value: float | None = None,
    keyable: bool = True
) -> dict[str, Any]:
    """Add a dynamic attribute to an object.
    
    Args:
        object_name: Name of the object.
        attribute_name: Name of the attribute to add.
        attribute_type: Type of attribute ('double', 'string', 'int', 'bool', etc.).
        default_value: Default value for the attribute.
        min_value: Optional minimum value.
        max_value: Optional maximum value.
        keyable: Whether the attribute is keyable.
    
    Returns:
        Dictionary with 'status', 'attribute' (full name), and 'message'.
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
        
        attr_name = f'{object_name}.{attribute_name}'
        if cmds.objExists(attr_name):
            return {
                'status': 'error',
                'message': f'Attribute "{attr_name}" already exists',
            }
        
        kwargs = {
            'longName': attribute_name,
            'attributeType': attribute_type,
            'defaultValue': default_value,
            'keyable': keyable,
        }
        
        if min_value is not None:
            kwargs['minValue'] = min_value
        if max_value is not None:
            kwargs['maxValue'] = max_value
        
        cmds.addAttr(object_name, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Added attribute {attr_name}',
            'attribute': attr_name,
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
def connect_attributes(
    source: str,
    destination: str,
    force: bool = False
) -> dict[str, Any]:
    """Connect two attributes.
    
    Args:
        source: Source attribute (e.g., 'pCube1.translateX').
        destination: Destination attribute (e.g., 'pCube2.translateX').
        force: If True, force the connection even if destination is already connected.
    
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
        if not cmds.objExists(source):
            return {
                'status': 'error',
                'message': f'Source attribute "{source}" does not exist',
            }
        
        if not cmds.objExists(destination):
            return {
                'status': 'error',
                'message': f'Destination attribute "{destination}" does not exist',
            }
        
        kwargs = {}
        if force:
            kwargs['force'] = True
        
        cmds.connectAttr(source, destination, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Connected {source} -> {destination}',
            'source': source,
            'destination': destination,
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
def disconnect_attributes(
    source: str,
    destination: str | None = None
) -> dict[str, Any]:
    """Disconnect attributes.
    
    Args:
        source: Source attribute.
        destination: Optional destination attribute. If None, disconnect all connections.
    
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
        if not cmds.objExists(source):
            return {
                'status': 'error',
                'message': f'Source attribute "{source}" does not exist',
            }
        
        if destination:
            if not cmds.objExists(destination):
                return {
                    'status': 'error',
                    'message': f'Destination attribute "{destination}" does not exist',
                }
            cmds.disconnectAttr(source, destination)
            message = f'Disconnected {source} -> {destination}'
        else:
            cmds.disconnectAttr(source)
            message = f'Disconnected all connections from {source}'
        
        return {
            'status': 'success',
            'message': message,
            'source': source,
            'destination': destination,
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
    'set_attribute',
    'add_attribute',
    'connect_attributes',
    'disconnect_attributes',
]
