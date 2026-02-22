"""Transform manipulation tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def move_object(
    object_name: str,
    x: float | None = None,
    y: float | None = None,
    z: float | None = None,
    relative: bool = False,
    world_space: bool = False
) -> dict[str, Any]:
    """Move an object in 3D space.
    
    Args:
        object_name: Name of the object to move.
        x: X translation value.
        y: Y translation value.
        z: Z translation value.
        relative: If True, move relative to current position.
        world_space: If True, move in world space.
    
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
        
        kwargs = {}
        if relative:
            kwargs['relative'] = True
        if world_space:
            kwargs['worldSpace'] = True
        
        translation = []
        if x is not None:
            translation.append(x)
        if y is not None:
            translation.append(y)
        if z is not None:
            translation.append(z)
        
        if translation:
            if len(translation) == 1:
                cmds.move(translation[0], object_name, **kwargs)
            elif len(translation) == 2:
                cmds.move(translation[0], translation[1], object_name, **kwargs)
            else:
                cmds.move(translation[0], translation[1], translation[2], object_name, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Moved {object_name}',
            'object': object_name,
            'translation': {'x': x, 'y': y, 'z': z},
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
def rotate_object(
    object_name: str,
    x: float | None = None,
    y: float | None = None,
    z: float | None = None,
    relative: bool = False,
    world_space: bool = False
) -> dict[str, Any]:
    """Rotate an object.
    
    Args:
        object_name: Name of the object to rotate.
        x: X rotation in degrees.
        y: Y rotation in degrees.
        z: Z rotation in degrees.
        relative: If True, rotate relative to current rotation.
        world_space: If True, rotate in world space.
    
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
        
        kwargs = {}
        if relative:
            kwargs['relative'] = True
        if world_space:
            kwargs['worldSpace'] = True
        
        rotation = []
        if x is not None:
            rotation.append(x)
        if y is not None:
            rotation.append(y)
        if z is not None:
            rotation.append(z)
        
        if rotation:
            if len(rotation) == 1:
                cmds.rotate(rotation[0], object_name, **kwargs)
            elif len(rotation) == 2:
                cmds.rotate(rotation[0], rotation[1], object_name, **kwargs)
            else:
                cmds.rotate(rotation[0], rotation[1], rotation[2], object_name, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Rotated {object_name}',
            'object': object_name,
            'rotation': {'x': x, 'y': y, 'z': z},
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
def scale_object(
    object_name: str,
    x: float | None = None,
    y: float | None = None,
    z: float | None = None,
    relative: bool = False
) -> dict[str, Any]:
    """Scale an object.
    
    Args:
        object_name: Name of the object to scale.
        x: X scale factor.
        y: Y scale factor.
        z: Z scale factor.
        relative: If True, scale relative to current scale.
    
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
        
        kwargs = {}
        if relative:
            kwargs['relative'] = True
        
        scale = []
        if x is not None:
            scale.append(x)
        if y is not None:
            scale.append(y)
        if z is not None:
            scale.append(z)
        
        if scale:
            if len(scale) == 1:
                cmds.scale(scale[0], object_name, **kwargs)
            elif len(scale) == 2:
                cmds.scale(scale[0], scale[1], object_name, **kwargs)
            else:
                cmds.scale(scale[0], scale[1], scale[2], object_name, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Scaled {object_name}',
            'object': object_name,
            'scale': {'x': x, 'y': y, 'z': z},
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
def parent_objects(
    child_objects: list[str],
    parent_object: str | None = None,
    world: bool = False
) -> dict[str, Any]:
    """Parent objects together.
    
    Args:
        child_objects: List of child object names.
        parent_object: Parent object name. If None and world=False, unparent.
        world: If True, parent to world (unparent).
    
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
    
    if not child_objects:
        return {
            'status': 'error',
            'message': 'No child objects provided',
        }
    
    try:
        # Filter to only existing objects
        existing = [obj for obj in child_objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {child_objects}',
            }
        
        if world or parent_object is None:
            cmds.parent(existing, world=True)
            message = f'Unparented {len(existing)} object(s)'
        else:
            if not cmds.objExists(parent_object):
                return {
                    'status': 'error',
                    'message': f'Parent object "{parent_object}" does not exist',
                }
            cmds.parent(existing, parent_object)
            message = f'Parented {len(existing)} object(s) to {parent_object}'
        
        return {
            'status': 'success',
            'message': message,
            'children': existing,
            'parent': parent_object if not world else None,
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
    'move_object',
    'rotate_object',
    'scale_object',
    'parent_objects',
]
