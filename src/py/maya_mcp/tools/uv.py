"""UV editing tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def get_uv_coordinates(
    mesh_name: str,
    uv_set: str = 'map1'
) -> dict[str, Any]:
    """Get UV coordinates for a mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        uv_set: Name of the UV set to query.
    
    Returns:
        Dictionary with 'status', 'uvs' (list of [u, v] coordinates), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'uvs': [],
        }
    
    try:
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
                'uvs': [],
            }
        
        # Get the shape node if transform was provided
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                    'uvs': [],
                }
            shape = shapes[0]
        
        # Get UV count
        uv_count = cmds.polyEvaluate(shape, uv=True)
        
        # Get UV coordinates
        uvs = []
        for i in range(uv_count):
            u = cmds.polyListComponentConversion(f'{shape}.map[{i}]', fromUV=True, toUV=True, query=True)
            if u:
                uv_coords = cmds.polyEditUV(u[0], query=True, u=True, v=True)
                if uv_coords:
                    uvs.append([uv_coords[0], uv_coords[1]])
        
        return {
            'status': 'success',
            'message': f'Found {len(uvs)} UV coordinate(s)',
            'uvs': uvs,
            'count': len(uvs),
            'mesh': mesh_name,
            'uv_set': uv_set,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'uvs': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'uvs': [],
        }


@mcp.tool
def set_uv_coordinates(
    mesh_name: str,
    uv_indices: list[int],
    u_values: list[float],
    v_values: list[float],
    uv_set: str = 'map1'
) -> dict[str, Any]:
    """Set UV coordinates for specific UVs.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        uv_indices: List of UV indices to modify.
        u_values: List of U values.
        v_values: List of V values.
        uv_set: Name of the UV set to modify.
    
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
    
    if len(uv_indices) != len(u_values) or len(uv_indices) != len(v_values):
        return {
            'status': 'error',
            'message': 'UV indices, U values, and V values must have the same length',
        }
    
    try:
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
            }
        
        # Get the shape node if transform was provided
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        # Set UV coordinates
        for i, uv_idx in enumerate(uv_indices):
            uv_component = f'{shape}.map[{uv_idx}]'
            if cmds.objExists(uv_component):
                cmds.polyEditUV(uv_component, u=u_values[i], v=v_values[i], relative=False)
        
        return {
            'status': 'success',
            'message': f'Set {len(uv_indices)} UV coordinate(s)',
            'mesh': mesh_name,
            'uv_set': uv_set,
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
def create_uv_snapshot(
    mesh_name: str,
    file_path: str,
    resolution: int = 512,
    uv_set: str = 'map1'
) -> dict[str, Any]:
    """Create a UV snapshot image.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        file_path: Path to save the UV snapshot image.
        resolution: Resolution of the snapshot (default: 512).
        uv_set: Name of the UV set to snapshot.
    
    Returns:
        Dictionary with 'status' and 'message'.
    """
    try:
        import maya.cmds as cmds
        from pathlib import Path
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
            }
        
        # Get the shape node if transform was provided
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        # Create UV snapshot
        cmds.polyUVSnapshot(
            shape,
            fileName=file_path,
            xResolution=resolution,
            yResolution=resolution,
            uvSetName=uv_set
        )
        
        return {
            'status': 'success',
            'message': f'Created UV snapshot: {file_path}',
            'file_path': file_path,
            'mesh': mesh_name,
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
def layout_uvs(
    mesh_name: str,
    method: str = 'linear',
    scale: float = 1.0,
    rotate: int = 0
) -> dict[str, Any]:
    """Layout UVs for a mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        method: Layout method ('linear', 'sawtooth', 'circular').
        scale: Scale factor for the layout.
        rotate: Rotation angle in degrees (0, 90, 180, 270).
    
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
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
            }
        
        # Get the shape node if transform was provided
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        # Layout UVs
        cmds.polyLayoutUV(
            shape,
            layoutMethod=method,
            scale=scale,
            rotateForBestFit=rotate
        )
        
        return {
            'status': 'success',
            'message': f'Laid out UVs for {mesh_name}',
            'mesh': mesh_name,
            'method': method,
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
    'get_uv_coordinates',
    'set_uv_coordinates',
    'create_uv_snapshot',
    'layout_uvs',
]
