"""Display layer tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_display_layer(
    name: str,
    objects: list[str] | None = None,
    visible: bool = True,
    display_type: str = 'normal'
) -> dict[str, Any]:
    """Create a display layer.
    
    Args:
        name: Name for the display layer.
        objects: Optional list of objects to add to the layer.
        visible: Whether the layer is visible.
        display_type: Display type ('normal', 'template', 'reference').
    
    Returns:
        Dictionary with 'status', 'layer', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        # Check if layer already exists
        if cmds.objExists(name):
            return {
                'status': 'error',
                'message': f'Display layer "{name}" already exists',
            }
        
        layer = cmds.createDisplayLayer(name=name, empty=True)
        
        # Set visibility
        cmds.setAttr(f'{layer}.visibility', visible)
        
        # Set display type
        display_type_map = {
            'normal': 0,
            'template': 1,
            'reference': 2,
        }
        if display_type in display_type_map:
            cmds.setAttr(f'{layer}.displayType', display_type_map[display_type])
        
        # Add objects if provided
        if objects:
            existing_objects = [obj for obj in objects if cmds.objExists(obj)]
            if existing_objects:
                cmds.editDisplayLayerMembers(layer, existing_objects)
        
        return {
            'status': 'success',
            'message': f'Created display layer: {layer}',
            'layer': layer,
            'objects': objects if objects else [],
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
def add_to_display_layer(
    layer_name: str,
    objects: list[str]
) -> dict[str, Any]:
    """Add objects to a display layer.
    
    Args:
        layer_name: Name of the display layer.
        objects: List of objects to add.
    
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
        if not cmds.objExists(layer_name):
            return {
                'status': 'error',
                'message': f'Display layer "{layer_name}" does not exist',
            }
        
        existing_objects = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing_objects:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        cmds.editDisplayLayerMembers(layer_name, existing_objects, noRecurse=True)
        
        return {
            'status': 'success',
            'message': f'Added {len(existing_objects)} object(s) to layer {layer_name}',
            'layer': layer_name,
            'objects': existing_objects,
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
def set_display_layer_visibility(
    layer_name: str,
    visible: bool
) -> dict[str, Any]:
    """Set the visibility of a display layer.
    
    Args:
        layer_name: Name of the display layer.
        visible: Whether the layer should be visible.
    
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
        if not cmds.objExists(layer_name):
            return {
                'status': 'error',
                'message': f'Display layer "{layer_name}" does not exist',
            }
        
        cmds.setAttr(f'{layer_name}.visibility', visible)
        
        return {
            'status': 'success',
            'message': f'Set layer {layer_name} visibility to {visible}',
            'layer': layer_name,
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
def get_display_layer_objects(layer_name: str) -> dict[str, Any]:
    """Get objects in a display layer.
    
    Args:
        layer_name: Name of the display layer.
    
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
        if not cmds.objExists(layer_name):
            return {
                'status': 'error',
                'message': f'Display layer "{layer_name}" does not exist',
                'objects': [],
            }
        
        objects = cmds.editDisplayLayerMembers(layer_name, query=True) or []
        
        return {
            'status': 'success',
            'message': f'Found {len(objects)} object(s) in layer {layer_name}',
            'objects': objects,
            'count': len(objects),
            'layer': layer_name,
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
def list_display_layers() -> dict[str, Any]:
    """List all display layers in the scene.
    
    Returns:
        Dictionary with 'status', 'layers' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'layers': [],
        }
    
    try:
        layers = cmds.ls(type='displayLayer') or []
        # Filter out default layer
        layers = [layer for layer in layers if layer != 'defaultLayer']
        
        return {
            'status': 'success',
            'message': f'Found {len(layers)} display layer(s)',
            'layers': layers,
            'count': len(layers),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'layers': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'layers': [],
        }


__all__ = [
    'create_display_layer',
    'add_to_display_layer',
    'set_display_layer_visibility',
    'get_display_layer_objects',
    'list_display_layers',
]
