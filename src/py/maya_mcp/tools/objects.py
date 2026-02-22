"""Object creation and manipulation tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_polygon_cube(
    name: str | None = None,
    width: float = 1.0,
    height: float = 1.0,
    depth: float = 1.0,
    subdivisions_x: int = 1,
    subdivisions_y: int = 1,
    subdivisions_z: int = 1
) -> dict[str, Any]:
    """Create a polygonal cube.
    
    Args:
        name: Optional name for the transform node.
        width: Width of the cube.
        height: Height of the cube.
        depth: Depth of the cube.
        subdivisions_x: Number of subdivisions along X axis.
        subdivisions_y: Number of subdivisions along Y axis.
        subdivisions_z: Number of subdivisions along Z axis.
    
    Returns:
        Dictionary with 'status', 'transform' (node name), and 'shape' (shape node name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {
            'width': width,
            'height': height,
            'depth': depth,
            'subdivisionsX': subdivisions_x,
            'subdivisionsY': subdivisions_y,
            'subdivisionsZ': subdivisions_z,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.polyCube(**kwargs)
        transform = result[0]
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'transform': transform,
            'shape': shape,
            'message': f'Created cube: {transform}',
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
def create_polygon_sphere(
    name: str | None = None,
    radius: float = 1.0,
    subdivisions_x: int = 20,
    subdivisions_y: int = 20
) -> dict[str, Any]:
    """Create a polygonal sphere.
    
    Args:
        name: Optional name for the transform node.
        radius: Radius of the sphere.
        subdivisions_x: Number of subdivisions along X axis (longitude).
        subdivisions_y: Number of subdivisions along Y axis (latitude).
    
    Returns:
        Dictionary with 'status', 'transform', and 'shape'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {
            'radius': radius,
            'subdivisionsX': subdivisions_x,
            'subdivisionsY': subdivisions_y,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.polySphere(**kwargs)
        transform = result[0]
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'transform': transform,
            'shape': shape,
            'message': f'Created sphere: {transform}',
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
def create_polygon_plane(
    name: str | None = None,
    width: float = 1.0,
    height: float = 1.0,
    subdivisions_x: int = 1,
    subdivisions_y: int = 1
) -> dict[str, Any]:
    """Create a polygonal plane.
    
    Args:
        name: Optional name for the transform node.
        width: Width of the plane.
        height: Height of the plane.
        subdivisions_x: Number of subdivisions along X axis.
        subdivisions_y: Number of subdivisions along Y axis.
    
    Returns:
        Dictionary with 'status', 'transform', and 'shape'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {
            'width': width,
            'height': height,
            'subdivisionsX': subdivisions_x,
            'subdivisionsY': subdivisions_y,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.polyPlane(**kwargs)
        transform = result[0]
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'transform': transform,
            'shape': shape,
            'message': f'Created plane: {transform}',
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
def create_polygon_cylinder(
    name: str | None = None,
    radius: float = 1.0,
    height: float = 2.0,
    subdivisions_x: int = 20,
    subdivisions_y: int = 1,
    subdivisions_z: int = 1
) -> dict[str, Any]:
    """Create a polygonal cylinder.
    
    Args:
        name: Optional name for the transform node.
        radius: Radius of the cylinder.
        height: Height of the cylinder.
        subdivisions_x: Number of subdivisions around the axis.
        subdivisions_y: Number of subdivisions along the height.
        subdivisions_z: Number of radial subdivisions.
    
    Returns:
        Dictionary with 'status', 'transform', and 'shape'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {
            'radius': radius,
            'height': height,
            'subdivisionsX': subdivisions_x,
            'subdivisionsY': subdivisions_y,
            'subdivisionsZ': subdivisions_z,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.polyCylinder(**kwargs)
        transform = result[0]
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'transform': transform,
            'shape': shape,
            'message': f'Created cylinder: {transform}',
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
def create_transform(name: str, parent: str | None = None) -> dict[str, Any]:
    """Create an empty transform node.
    
    Args:
        name: Name for the transform node.
        parent: Optional parent transform.
    
    Returns:
        Dictionary with 'status' and 'transform'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {'name': name}
        if parent and cmds.objExists(parent):
            kwargs['parent'] = parent
        
        transform = cmds.createNode('transform', **kwargs)
        
        return {
            'status': 'success',
            'transform': transform,
            'message': f'Created transform: {transform}',
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
def delete_objects(names: list[str]) -> dict[str, Any]:
    """Delete objects from the scene.
    
    Args:
        names: List of object names to delete.
    
    Returns:
        Dictionary with 'status', 'deleted' (list), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'deleted': [],
        }
    
    if not names:
        return {
            'status': 'error',
            'message': 'No object names provided',
            'deleted': [],
        }
    
    try:
        # Filter to only existing objects
        existing = [name for name in names if cmds.objExists(name)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {names}',
                'deleted': [],
            }
        
        cmds.delete(existing)
        
        missing = [name for name in names if name not in existing]
        message = f'Deleted {len(existing)} object(s)'
        if missing:
            message += f'. Note: {len(missing)} object(s) not found: {missing}'
        
        return {
            'status': 'success',
            'message': message,
            'deleted': existing,
            'missing': missing,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'deleted': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'deleted': [],
        }


@mcp.tool
def duplicate_objects(
    names: list[str],
    name: str | None = None,
    instance: bool = False,
    smart_transform: bool = False
) -> dict[str, Any]:
    """Duplicate objects.
    
    Args:
        names: List of object names to duplicate.
        name: Optional name for the duplicated object(s).
        instance: If True, create an instance instead of a copy.
        smart_transform: If True, use smart transform.
    
    Returns:
        Dictionary with 'status', 'duplicated' (list), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'duplicated': [],
        }
    
    if not names:
        return {
            'status': 'error',
            'message': 'No object names provided',
            'duplicated': [],
        }
    
    try:
        # Filter to only existing objects
        existing = [name_obj for name_obj in names if cmds.objExists(name_obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {names}',
                'duplicated': [],
            }
        
        kwargs = {}
        if instance:
            kwargs['instance'] = True
        if smart_transform:
            kwargs['smartTransform'] = True
        
        result = cmds.duplicate(existing, **kwargs)
        
        if name and len(result) == 1:
            result = [cmds.rename(result[0], name)]
        
        return {
            'status': 'success',
            'message': f'Duplicated {len(existing)} object(s)',
            'duplicated': result,
            'original': existing,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'duplicated': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'duplicated': [],
        }


__all__ = [
    'create_polygon_cube',
    'create_polygon_sphere',
    'create_polygon_plane',
    'create_polygon_cylinder',
    'create_transform',
    'delete_objects',
    'duplicate_objects',
]
