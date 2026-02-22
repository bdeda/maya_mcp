"""Skinning tools for Maya - skin clusters and skin weights."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def bind_skin(
    mesh: str,
    joints: list[str],
    name: str | None = None,
    bind_method: str = 'closestPoint',
    skin_method: str = 'classicLinear'
) -> dict[str, Any]:
    """Bind a mesh to joints (create a skin cluster).
    
    Args:
        mesh: Mesh transform or shape name.
        joints: List of joint names to bind.
        name: Optional name for the skin cluster.
        bind_method: Binding method ('closestPoint', 'heatMap', 'geodesicVoxel').
        skin_method: Skinning method ('classicLinear', 'dualQuaternion', 'weightBlended').
    
    Returns:
        Dictionary with 'status', 'skin_cluster', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not joints:
        return {
            'status': 'error',
            'message': 'No joints provided',
        }
    
    try:
        if not cmds.objExists(mesh):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh}" does not exist',
            }
        
        # Get the shape node if transform was provided
        shape = mesh
        if cmds.objectType(mesh) == 'transform':
            shapes = cmds.listRelatives(mesh, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh}"',
                }
            shape = shapes[0]
        
        # Filter to only existing joints
        existing_joints = [j for j in joints if cmds.objExists(j)]
        
        if not existing_joints:
            return {
                'status': 'error',
                'message': f'None of the joints exist: {joints}',
            }
        
        kwargs = {
            'bindMethod': bind_method,
            'skinMethod': skin_method,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.skinCluster(existing_joints, shape, **kwargs)
        skin_cluster = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Bound skin to {len(existing_joints)} joint(s)',
            'skin_cluster': skin_cluster,
            'mesh': mesh,
            'joints': existing_joints,
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
def get_skin_cluster(mesh: str) -> dict[str, Any]:
    """Get the skin cluster associated with a mesh.
    
    Args:
        mesh: Mesh transform or shape name.
    
    Returns:
        Dictionary with 'status', 'skin_cluster', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'skin_cluster': None,
        }
    
    try:
        if not cmds.objExists(mesh):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh}" does not exist',
                'skin_cluster': None,
            }
        
        # Get the shape node if transform was provided
        shape = mesh
        if cmds.objectType(mesh) == 'transform':
            shapes = cmds.listRelatives(mesh, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh}"',
                    'skin_cluster': None,
                }
            shape = shapes[0]
        
        skin_clusters = cmds.ls(cmds.listHistory(shape), type='skinCluster')
        
        if not skin_clusters:
            return {
                'status': 'success',
                'message': f'No skin cluster found for "{mesh}"',
                'skin_cluster': None,
            }
        
        return {
            'status': 'success',
            'message': f'Found skin cluster: {skin_clusters[0]}',
            'skin_cluster': skin_clusters[0],
            'mesh': mesh,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'skin_cluster': None,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'skin_cluster': None,
        }


@mcp.tool
def get_skin_cluster_joints(skin_cluster: str) -> dict[str, Any]:
    """Get the joints associated with a skin cluster.
    
    Args:
        skin_cluster: Skin cluster node name.
    
    Returns:
        Dictionary with 'status', 'joints' (list), and 'count'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'joints': [],
        }
    
    try:
        if not cmds.objExists(skin_cluster):
            return {
                'status': 'error',
                'message': f'Skin cluster "{skin_cluster}" does not exist',
                'joints': [],
            }
        
        joints = cmds.skinCluster(skin_cluster, query=True, influence=True) or []
        
        return {
            'status': 'success',
            'message': f'Found {len(joints)} joint(s)',
            'joints': joints,
            'count': len(joints),
            'skin_cluster': skin_cluster,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'joints': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'joints': [],
        }


__all__ = [
    'bind_skin',
    'get_skin_cluster',
    'get_skin_cluster_joints',
]
