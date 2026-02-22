"""Animation layer tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_animation_layer(
    name: str,
    weight: float = 1.0,
    solo: bool = False,
    mute: bool = False
) -> dict[str, Any]:
    """Create an animation layer.
    
    Args:
        name: Name for the animation layer.
        weight: Weight of the layer (0.0 to 1.0).
        solo: If True, solo the layer.
        mute: If True, mute the layer.
    
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
        existing_layers = cmds.ls(type='animLayer')
        if name in existing_layers:
            return {
                'status': 'error',
                'message': f'Animation layer "{name}" already exists',
            }
        
        layer = cmds.animLayer(name=name)
        
        # Set weight
        cmds.animLayer(layer, edit=True, weight=weight)
        
        # Set solo
        if solo:
            cmds.animLayer(layer, edit=True, solo=True)
        
        # Set mute
        if mute:
            cmds.animLayer(layer, edit=True, mute=True)
        
        return {
            'status': 'success',
            'message': f'Created animation layer: {layer}',
            'layer': layer,
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
def add_to_animation_layer(
    layer_name: str,
    attributes: list[str]
) -> dict[str, Any]:
    """Add attributes to an animation layer.
    
    Args:
        layer_name: Name of the animation layer.
        attributes: List of attribute names (e.g., ['pCube1.translateX']).
    
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
        if not cmds.objExists(layer_name):
            return {
                'status': 'error',
                'message': f'Animation layer "{layer_name}" does not exist',
            }
        
        # Filter to only existing attributes
        existing_attrs = [attr for attr in attributes if cmds.objExists(attr)]
        
        if not existing_attrs:
            return {
                'status': 'error',
                'message': f'None of the attributes exist: {attributes}',
            }
        
        cmds.animLayer(layer_name, edit=True, attribute=existing_attrs)
        
        return {
            'status': 'success',
            'message': f'Added {len(existing_attrs)} attribute(s) to layer {layer_name}',
            'layer': layer_name,
            'attributes': existing_attrs,
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
def set_animation_layer_weight(
    layer_name: str,
    weight: float
) -> dict[str, Any]:
    """Set the weight of an animation layer.
    
    Args:
        layer_name: Name of the animation layer.
        weight: Weight value (0.0 to 1.0).
    
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
                'message': f'Animation layer "{layer_name}" does not exist',
            }
        
        weight = max(0.0, min(1.0, weight))  # Clamp to 0-1
        
        cmds.animLayer(layer_name, edit=True, weight=weight)
        
        return {
            'status': 'success',
            'message': f'Set layer {layer_name} weight to {weight}',
            'layer': layer_name,
            'weight': weight,
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
def list_animation_layers() -> dict[str, Any]:
    """List all animation layers in the scene.
    
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
        layers = cmds.ls(type='animLayer') or []
        
        return {
            'status': 'success',
            'message': f'Found {len(layers)} animation layer(s)',
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
    'create_animation_layer',
    'add_to_animation_layer',
    'set_animation_layer_weight',
    'list_animation_layers',
]
