"""Paint operations for Maya - skin weights, attributes, etc."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def get_skin_weights(
    mesh_name: str,
    skin_cluster: str | None = None
) -> dict[str, Any]:
    """Get skin weights for a mesh.
    
    Args:
        mesh_name: Name of the skinned mesh.
        skin_cluster: Optional skin cluster name. If None, finds automatically.
    
    Returns:
        Dictionary with 'status', 'weights' (dict mapping vertices to joint weights), and 'message'.
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
        
        # Find skin cluster if not provided
        if not skin_cluster:
            history = cmds.listHistory(mesh_name)
            skin_clusters = [h for h in history if cmds.nodeType(h) == 'skinCluster']
            if not skin_clusters:
                return {
                    'status': 'error',
                    'message': f'No skin cluster found on "{mesh_name}"',
                }
            skin_cluster = skin_clusters[0]
        
        if not cmds.objExists(skin_cluster):
            return {
                'status': 'error',
                'message': f'Skin cluster "{skin_cluster}" does not exist',
            }
        
        # Get influences (joints)
        influences = cmds.skinCluster(skin_cluster, query=True, influence=True) or []
        
        # Get vertex count
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if shapes:
                shape = shapes[0]
        
        vertex_count = cmds.polyEvaluate(shape, vertex=True)
        
        weights = {}
        for vtx_idx in range(vertex_count):
            vtx_name = f'{shape}.vtx[{vtx_idx}]'
            vtx_weights = {}
            for influence in influences:
                weight = cmds.skinPercent(skin_cluster, vtx_name, query=True, transform=influence, value=True)
                if weight and weight[0] > 0.0:
                    vtx_weights[influence] = weight[0]
            if vtx_weights:
                weights[vtx_idx] = vtx_weights
        
        return {
            'status': 'success',
            'message': f'Retrieved skin weights for {mesh_name}',
            'weights': weights,
            'skin_cluster': skin_cluster,
            'influences': influences,
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
def set_skin_weights(
    mesh_name: str,
    weights: dict[int, dict[str, float]],
    skin_cluster: str | None = None
) -> dict[str, Any]:
    """Set skin weights for vertices on a mesh.
    
    Args:
        mesh_name: Name of the skinned mesh.
        weights: Dictionary mapping vertex indices to dictionaries of joint:weight pairs.
        skin_cluster: Optional skin cluster name. If None, finds automatically.
    
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
        
        # Find skin cluster if not provided
        if not skin_cluster:
            history = cmds.listHistory(mesh_name)
            skin_clusters = [h for h in history if cmds.nodeType(h) == 'skinCluster']
            if not skin_clusters:
                return {
                    'status': 'error',
                    'message': f'No skin cluster found on "{mesh_name}"',
                }
            skin_cluster = skin_clusters[0]
        
        if not cmds.objExists(skin_cluster):
            return {
                'status': 'error',
                'message': f'Skin cluster "{skin_cluster}" does not exist',
            }
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if shapes:
                shape = shapes[0]
        
        # Set weights for each vertex
        for vtx_idx, joint_weights in weights.items():
            vtx_name = f'{shape}.vtx[{vtx_idx}]'
            transform_value_list = []
            for joint, weight in joint_weights.items():
                if cmds.objExists(joint):
                    transform_value_list.append(f'{joint}={weight}')
            
            if transform_value_list:
                cmds.skinPercent(skin_cluster, vtx_name, transformValue=transform_value_list)
        
        return {
            'status': 'success',
            'message': f'Set skin weights for {len(weights)} vertex/vertices on {mesh_name}',
            'skin_cluster': skin_cluster,
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
    'get_skin_weights',
    'set_skin_weights',
]
