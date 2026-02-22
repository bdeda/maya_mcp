"""Camera operations for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_camera(
    name: str | None = None,
    orthographic: bool = False,
    focal_length: float = 35.0
) -> dict[str, Any]:
    """Create a camera.
    
    Args:
        name: Optional name for the camera.
        orthographic: If True, create an orthographic camera.
        focal_length: Focal length for perspective camera.
    
    Returns:
        Dictionary with 'status', 'camera' (transform name), and 'shape' (shape name).
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
        
        if orthographic:
            camera = cmds.camera(orthographic=True, **kwargs)
        else:
            camera = cmds.camera(focalLength=focal_length, **kwargs)
        
        transform = camera[0] if camera else None
        shape = camera[1] if len(camera) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created camera: {transform}',
            'camera': transform,
            'shape': shape,
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
def set_camera_focal_length(
    camera_name: str,
    focal_length: float
) -> dict[str, Any]:
    """Set the focal length of a camera.
    
    Args:
        camera_name: Name of the camera transform or shape.
        focal_length: Focal length value.
    
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
        if not cmds.objExists(camera_name):
            return {
                'status': 'error',
                'message': f'Camera "{camera_name}" does not exist',
            }
        
        # Get the shape node if transform was provided
        shape = camera_name
        if cmds.objectType(camera_name) == 'transform':
            shapes = cmds.listRelatives(camera_name, shapes=True, type='camera')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No camera shape found for "{camera_name}"',
                }
            shape = shapes[0]
        
        cmds.setAttr(f'{shape}.focalLength', focal_length)
        
        return {
            'status': 'success',
            'message': f'Set focal length of {camera_name} to {focal_length}',
            'camera': camera_name,
            'focal_length': focal_length,
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
def look_through_camera(camera_name: str) -> dict[str, Any]:
    """Set the active viewport to look through a camera.
    
    Args:
        camera_name: Name of the camera transform or shape.
    
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
        if not cmds.objExists(camera_name):
            return {
                'status': 'error',
                'message': f'Camera "{camera_name}" does not exist',
            }
        
        # Get the transform if shape was provided
        transform = camera_name
        if cmds.objectType(camera_name) == 'camera':
            parents = cmds.listRelatives(camera_name, parent=True)
            if parents:
                transform = parents[0]
        
        cmds.lookThru(transform)
        
        return {
            'status': 'success',
            'message': f'Looking through camera {transform}',
            'camera': transform,
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
def list_cameras() -> dict[str, Any]:
    """List all cameras in the scene.
    
    Returns:
        Dictionary with 'status', 'cameras' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'cameras': [],
        }
    
    try:
        camera_shapes = cmds.ls(type='camera') or []
        transforms = []
        for shape in camera_shapes:
            parents = cmds.listRelatives(shape, parent=True)
            if parents:
                transforms.append(parents[0])
        
        return {
            'status': 'success',
            'message': f'Found {len(transforms)} camera(s)',
            'cameras': transforms,
            'count': len(transforms),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'cameras': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'cameras': [],
        }


@mcp.tool
def view_fit(
    objects: list[str] | None = None,
    all_objects: bool = False
) -> dict[str, Any]:
    """Fit the view to show objects.
    
    Args:
        objects: Optional list of object names to fit view to. If None, fit to selection.
        all_objects: If True, fit view to all objects in scene.
    
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
        if all_objects:
            cmds.viewFit(allObjects=True)
        elif objects:
            existing = [obj for obj in objects if cmds.objExists(obj)]
            if existing:
                cmds.select(existing, replace=True)
                cmds.viewFit()
            else:
                return {
                    'status': 'error',
                    'message': f'None of the objects exist: {objects}',
                }
        else:
            cmds.viewFit()
        
        return {
            'status': 'success',
            'message': 'Fitted view to objects',
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
def view_selected() -> dict[str, Any]:
    """Fit the view to show selected objects.
    
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
        cmds.viewFit()
        
        return {
            'status': 'success',
            'message': 'Fitted view to selected objects',
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
    'create_camera',
    'set_camera_focal_length',
    'look_through_camera',
    'list_cameras',
    'view_fit',
    'view_selected',
]
