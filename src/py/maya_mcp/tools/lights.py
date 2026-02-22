"""Light creation and manipulation tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_directional_light(
    name: str | None = None,
    intensity: float = 1.0,
    color: tuple[float, float, float] | None = None
) -> dict[str, Any]:
    """Create a directional light.
    
    Args:
        name: Optional name for the light.
        intensity: Light intensity.
        color: Optional RGB color tuple (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'light' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.directionalLight(**kwargs)
        light_transform = result[0] if result else None
        light_shape = result[1] if len(result) > 1 else None
        
        # Set intensity
        if light_shape:
            cmds.setAttr(f'{light_shape}.intensity', intensity)
            
            # Set color if provided
            if color:
                cmds.setAttr(f'{light_shape}.color', color[0], color[1], color[2], type='double3')
        
        return {
            'status': 'success',
            'message': f'Created directional light: {light_transform}',
            'light': light_transform,
            'shape': light_shape,
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
def create_point_light(
    name: str | None = None,
    intensity: float = 1.0,
    color: tuple[float, float, float] | None = None
) -> dict[str, Any]:
    """Create a point light.
    
    Args:
        name: Optional name for the light.
        intensity: Light intensity.
        color: Optional RGB color tuple (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'light' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.pointLight(**kwargs)
        light_transform = result[0] if result else None
        light_shape = result[1] if len(result) > 1 else None
        
        # Set intensity
        if light_shape:
            cmds.setAttr(f'{light_shape}.intensity', intensity)
            
            # Set color if provided
            if color:
                cmds.setAttr(f'{light_shape}.color', color[0], color[1], color[2], type='double3')
        
        return {
            'status': 'success',
            'message': f'Created point light: {light_transform}',
            'light': light_transform,
            'shape': light_shape,
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
def create_spot_light(
    name: str | None = None,
    intensity: float = 1.0,
    color: tuple[float, float, float] | None = None,
    cone_angle: float = 40.0,
    penumbra_angle: float = 0.0
) -> dict[str, Any]:
    """Create a spot light.
    
    Args:
        name: Optional name for the light.
        intensity: Light intensity.
        color: Optional RGB color tuple (0.0 to 1.0).
        cone_angle: Cone angle in degrees.
        penumbra_angle: Penumbra angle in degrees.
    
    Returns:
        Dictionary with 'status', 'light' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.spotLight(**kwargs)
        light_transform = result[0] if result else None
        light_shape = result[1] if len(result) > 1 else None
        
        # Set properties
        if light_shape:
            cmds.setAttr(f'{light_shape}.intensity', intensity)
            cmds.setAttr(f'{light_shape}.coneAngle', cone_angle)
            cmds.setAttr(f'{light_shape}.penumbraAngle', penumbra_angle)
            
            # Set color if provided
            if color:
                cmds.setAttr(f'{light_shape}.color', color[0], color[1], color[2], type='double3')
        
        return {
            'status': 'success',
            'message': f'Created spot light: {light_transform}',
            'light': light_transform,
            'shape': light_shape,
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
def create_area_light(
    name: str | None = None,
    intensity: float = 1.0,
    color: tuple[float, float, float] | None = None
) -> dict[str, Any]:
    """Create an area light.
    
    Args:
        name: Optional name for the light.
        intensity: Light intensity.
        color: Optional RGB color tuple (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'light' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.areaLight(**kwargs)
        light_transform = result[0] if result else None
        light_shape = result[1] if len(result) > 1 else None
        
        # Set intensity
        if light_shape:
            cmds.setAttr(f'{light_shape}.intensity', intensity)
            
            # Set color if provided
            if color:
                cmds.setAttr(f'{light_shape}.color', color[0], color[1], color[2], type='double3')
        
        return {
            'status': 'success',
            'message': f'Created area light: {light_transform}',
            'light': light_transform,
            'shape': light_shape,
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
def set_light_intensity(
    light_name: str,
    intensity: float
) -> dict[str, Any]:
    """Set the intensity of a light.
    
    Args:
        light_name: Name of the light transform or shape.
        intensity: Light intensity value.
    
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
        if not cmds.objExists(light_name):
            return {
                'status': 'error',
                'message': f'Light "{light_name}" does not exist',
            }
        
        # Get shape if transform was provided
        shape = light_name
        if cmds.objectType(light_name) == 'transform':
            shapes = cmds.listRelatives(light_name, shapes=True, type='light')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No light shape found for "{light_name}"',
                }
            shape = shapes[0]
        
        cmds.setAttr(f'{shape}.intensity', intensity)
        
        return {
            'status': 'success',
            'message': f'Set light {light_name} intensity to {intensity}',
            'light': light_name,
            'intensity': intensity,
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
def list_lights() -> dict[str, Any]:
    """List all lights in the scene.
    
    Returns:
        Dictionary with 'status', 'lights' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'lights': [],
        }
    
    try:
        lights = cmds.ls(type='light') or []
        transforms = []
        for light_shape in lights:
            parent = cmds.listRelatives(light_shape, parent=True)
            if parent:
                transforms.append(parent[0])
        
        return {
            'status': 'success',
            'message': f'Found {len(transforms)} light(s)',
            'lights': transforms,
            'count': len(transforms),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'lights': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'lights': [],
        }


__all__ = [
    'create_directional_light',
    'create_point_light',
    'create_spot_light',
    'create_area_light',
    'set_light_intensity',
    'list_lights',
]
