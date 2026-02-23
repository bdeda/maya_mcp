"""Material creation and assignment tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_lambert_material(
    name: str | None = None,
    color: tuple[float, float, float] | None = None
) -> dict[str, Any]:
    """Create a Lambert material.
    
    Args:
        name: Optional name for the material.
        color: Optional RGB color tuple (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'material' (shading engine), and 'shader' (shader node).
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
        
        shader = cmds.shadingNode('lambert', asShader=True, **kwargs)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        
        # Set color if provided
        if color:
            cmds.setAttr(f'{shader}.color', color[0], color[1], color[2], type='double3')
        
        return {
            'status': 'success',
            'message': f'Created Lambert material: {shader}',
            'material': shading_group,
            'shader': shader,
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
def create_phong_material(
    name: str | None = None,
    color: tuple[float, float, float] | None = None,
    specular_color: tuple[float, float, float] | None = None,
    cosine_power: float = 20.0
) -> dict[str, Any]:
    """Create a Phong material.
    
    Args:
        name: Optional name for the material.
        color: Optional RGB color tuple (0.0 to 1.0).
        specular_color: Optional specular RGB color tuple (0.0 to 1.0).
        cosine_power: Cosine power for specular highlight.
    
    Returns:
        Dictionary with 'status', 'material' (shading engine), and 'shader' (shader node).
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
        
        shader = cmds.shadingNode('phong', asShader=True, **kwargs)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        
        # Set color if provided
        if color:
            cmds.setAttr(f'{shader}.color', color[0], color[1], color[2], type='double3')
        
        # Set specular color if provided
        if specular_color:
            cmds.setAttr(f'{shader}.specularColor', specular_color[0], specular_color[1], specular_color[2], type='double3')
        
        # Set cosine power
        cmds.setAttr(f'{shader}.cosinePower', cosine_power)
        
        return {
            'status': 'success',
            'message': f'Created Phong material: {shader}',
            'material': shading_group,
            'shader': shader,
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
def create_blinn_material(
    name: str | None = None,
    color: tuple[float, float, float] | None = None,
    specular_color: tuple[float, float, float] | None = None,
    eccentricity: float = 0.3
) -> dict[str, Any]:
    """Create a Blinn material.
    
    Args:
        name: Optional name for the material.
        color: Optional RGB color tuple (0.0 to 1.0).
        specular_color: Optional specular RGB color tuple (0.0 to 1.0).
        eccentricity: Eccentricity value (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'material' (shading engine), and 'shader' (shader node).
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
        
        shader = cmds.shadingNode('blinn', asShader=True, **kwargs)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        
        # Set color if provided
        if color:
            cmds.setAttr(f'{shader}.color', color[0], color[1], color[2], type='double3')
        
        # Set specular color if provided
        if specular_color:
            cmds.setAttr(f'{shader}.specularColor', specular_color[0], specular_color[1], specular_color[2], type='double3')
        
        # Set eccentricity
        cmds.setAttr(f'{shader}.eccentricity', eccentricity)
        
        return {
            'status': 'success',
            'message': f'Created Blinn material: {shader}',
            'material': shading_group,
            'shader': shader,
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
def assign_material(
    material_name: str,
    objects: list[str]
) -> dict[str, Any]:
    """Assign a material to objects.
    
    Args:
        material_name: Name of the material (shading engine).
        objects: List of object names to assign the material to.
    
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
        if not cmds.objExists(material_name):
            return {
                'status': 'error',
                'message': f'Material "{material_name}" does not exist',
            }
        
        # Filter to only existing objects
        existing = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        # Get shapes for assignment
        shapes_to_assign = []
        for obj in existing:
            if cmds.objectType(obj) == 'transform':
                shapes = cmds.listRelatives(obj, shapes=True, type='mesh')
                if shapes:
                    shapes_to_assign.extend(shapes)
            elif cmds.objectType(obj) == 'mesh':
                shapes_to_assign.append(obj)
        
        if shapes_to_assign:
            cmds.sets(shapes_to_assign, edit=True, forceElement=material_name)
        
        return {
            'status': 'success',
            'message': f'Assigned material {material_name} to {len(existing)} object(s)',
            'material': material_name,
            'objects': existing,
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
def get_assigned_material(object_name: str) -> dict[str, Any]:
    """Get the material assigned to an object.
    
    Args:
        object_name: Name of the object.
    
    Returns:
        Dictionary with 'status', 'material', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'material': None,
        }
    
    try:
        if not cmds.objExists(object_name):
            return {
                'status': 'error',
                'message': f'Object "{object_name}" does not exist',
                'material': None,
            }
        
        # Get the shape node if transform was provided
        shape = object_name
        if cmds.objectType(object_name) == 'transform':
            shapes = cmds.listRelatives(object_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{object_name}"',
                    'material': None,
                }
            shape = shapes[0]
        
        # Get assigned shading groups
        shading_groups = cmds.listConnections(shape, type='shadingEngine') or []
        
        if not shading_groups:
            return {
                'status': 'success',
                'message': f'No material assigned to {object_name}',
                'material': None,
            }
        
        return {
            'status': 'success',
            'message': f'Found material: {shading_groups[0]}',
            'material': shading_groups[0],
            'object': object_name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'material': None,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'material': None,
        }


@mcp.tool
def list_materials() -> dict[str, Any]:
    """List all materials in the scene.
    
    Returns:
        Dictionary with 'status', 'materials' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'materials': [],
        }
    
    try:
        shading_groups = cmds.ls(type='shadingEngine') or []
        # Filter out default shading groups
        materials = [sg for sg in shading_groups if sg not in ['initialShadingGroup', 'initialParticleSE']]
        
        return {
            'status': 'success',
            'message': f'Found {len(materials)} material(s)',
            'materials': materials,
            'count': len(materials),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'materials': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'materials': [],
        }


@mcp.tool
def create_file_texture(
    file_path: str,
    name: str | None = None
) -> dict[str, Any]:
    """Create a file texture node.
    
    Args:
        file_path: Path to the texture file.
        name: Optional name for the file texture node.
    
    Returns:
        Dictionary with 'status', 'texture' (file node name), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {'imageName': file_path}
        if name:
            kwargs['name'] = name
        
        file_node = cmds.shadingNode('file', asTexture=True, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created file texture: {file_node}',
            'texture': file_node,
            'file_path': file_path,
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
def create_ramp_texture(
    name: str | None = None
) -> dict[str, Any]:
    """Create a ramp texture node.
    
    Args:
        name: Optional name for the ramp texture node.
    
    Returns:
        Dictionary with 'status', 'texture' (ramp node name), and 'message'.
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
        
        ramp_node = cmds.shadingNode('ramp', asTexture=True, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created ramp texture: {ramp_node}',
            'texture': ramp_node,
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
def create_place2d_texture(
    name: str | None = None
) -> dict[str, Any]:
    """Create a 2D texture placement node.
    
    Args:
        name: Optional name for the placement node.
    
    Returns:
        Dictionary with 'status', 'placement' (placement node name), and 'message'.
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
        
        placement_node = cmds.shadingNode('place2dTexture', asUtility=True, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created 2D texture placement: {placement_node}',
            'placement': placement_node,
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
def create_surface_shader(
    name: str | None = None,
    color: tuple[float, float, float] | None = None
) -> dict[str, Any]:
    """Create a surface shader material.
    
    Args:
        name: Optional name for the material.
        color: Optional RGB color tuple (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'material' (shading engine), and 'shader' (shader node).
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
        
        shader = cmds.shadingNode('surfaceShader', asShader=True, **kwargs)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        
        # Set color if provided
        if color:
            cmds.setAttr(f'{shader}.outColor', color[0], color[1], color[2], type='double3')
        
        return {
            'status': 'success',
            'message': f'Created surface shader: {shader}',
            'material': shading_group,
            'shader': shader,
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
def create_use_background_shader(
    name: str | None = None,
    specular_color: tuple[float, float, float] | None = None,
    reflectivity: float = 0.5
) -> dict[str, Any]:
    """Create a use background shader.
    
    Args:
        name: Optional name for the material.
        specular_color: Optional specular RGB color tuple (0.0 to 1.0).
        reflectivity: Reflectivity value (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'material' (shading engine), and 'shader' (shader node).
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
        
        shader = cmds.shadingNode('useBackground', asShader=True, **kwargs)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        
        # Set specular color if provided
        if specular_color:
            cmds.setAttr(f'{shader}.specularColor', specular_color[0], specular_color[1], specular_color[2], type='double3')
        
        # Set reflectivity
        cmds.setAttr(f'{shader}.reflectivity', reflectivity)
        
        return {
            'status': 'success',
            'message': f'Created use background shader: {shader}',
            'material': shading_group,
            'shader': shader,
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
def create_layered_shader(
    name: str | None = None
) -> dict[str, Any]:
    """Create a layered shader material.
    
    Args:
        name: Optional name for the material.
    
    Returns:
        Dictionary with 'status', 'material' (shading engine), and 'shader' (shader node).
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
        
        shader = cmds.shadingNode('layeredShader', asShader=True, **kwargs)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        
        return {
            'status': 'success',
            'message': f'Created layered shader: {shader}',
            'material': shading_group,
            'shader': shader,
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
def create_ramp_shader(
    name: str | None = None,
    color: tuple[float, float, float] | None = None
) -> dict[str, Any]:
    """Create a ramp shader material.
    
    Args:
        name: Optional name for the material.
        color: Optional RGB color tuple (0.0 to 1.0).
    
    Returns:
        Dictionary with 'status', 'material' (shading engine), and 'shader' (shader node).
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
        
        shader = cmds.shadingNode('rampShader', asShader=True, **kwargs)
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
        cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')
        
        # Set color if provided
        if color:
            cmds.setAttr(f'{shader}.color', color[0], color[1], color[2], type='double3')
        
        return {
            'status': 'success',
            'message': f'Created ramp shader: {shader}',
            'material': shading_group,
            'shader': shader,
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
def create_shading_node(
    node_type: str,
    as_shader: bool = False,
    as_texture: bool = False,
    as_utility: bool = False,
    name: str | None = None
) -> dict[str, Any]:
    """Create a generic shading node.
    
    Args:
        node_type: Type of shading node to create (e.g., 'lambert', 'file', 'noise').
        as_shader: If True, create as a shader node.
        as_texture: If True, create as a texture node.
        as_utility: If True, create as a utility node.
        name: Optional name for the node.
    
    Returns:
        Dictionary with 'status', 'node' (node name), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not (as_shader or as_texture or as_utility):
        return {
            'status': 'error',
            'message': 'Must specify one of: as_shader, as_texture, or as_utility',
        }
    
    try:
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        if as_shader:
            node = cmds.shadingNode(node_type, asShader=True, **kwargs)
        elif as_texture:
            node = cmds.shadingNode(node_type, asTexture=True, **kwargs)
        else:  # as_utility
            node = cmds.shadingNode(node_type, asUtility=True, **kwargs)
        
        node_type_str = 'shader' if as_shader else ('texture' if as_texture else 'utility')
        
        return {
            'status': 'success',
            'message': f'Created {node_type_str} node: {node}',
            'node': node,
            'node_type': node_type,
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
    'create_lambert_material',
    'create_phong_material',
    'create_blinn_material',
    'create_surface_shader',
    'create_use_background_shader',
    'create_layered_shader',
    'create_ramp_shader',
    'create_shading_node',
    'create_file_texture',
    'create_ramp_texture',
    'create_place2d_texture',
    'assign_material',
    'get_assigned_material',
    'list_materials',
]
