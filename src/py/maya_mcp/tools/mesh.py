"""Mesh manipulation tools for Maya - optimized with OpenMaya API for expensive operations."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]
    import maya.api.OpenMaya  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def get_mesh_vertices(
    mesh_name: str,
    world_space: bool = False
) -> dict[str, Any]:
    """Get vertex positions of a mesh using OpenMaya API for performance.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        world_space: If True, return positions in world space.
    
    Returns:
        Dictionary with 'status', 'vertices' (list of [x, y, z] positions), and 'count'.
    """
    try:
        import maya.cmds as cmds
        import maya.api.OpenMaya as om
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'vertices': [],
        }
    
    try:
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
                'vertices': [],
            }
        
        # Get the shape node if transform was provided
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                    'vertices': [],
                }
            shape = shapes[0]
        
        # Use OpenMaya API for performance
        selection = om.MSelectionList()
        selection.add(shape)
        dag_path = om.MDagPath()
        selection.getDagPath(0, dag_path)
        
        mesh_fn = om.MFnMesh(dag_path)
        space = om.MSpace.kWorld if world_space else om.MSpace.kObject
        
        vertices = om.MPointArray()
        mesh_fn.getPoints(vertices, space)
        
        vertex_list = []
        for i in range(vertices.length()):
            point = vertices[i]
            vertex_list.append([point.x, point.y, point.z])
        
        return {
            'status': 'success',
            'vertices': vertex_list,
            'count': len(vertex_list),
            'mesh': mesh_name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'vertices': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'vertices': [],
        }


@mcp.tool
def get_mesh_face_count(mesh_name: str) -> dict[str, Any]:
    """Get the number of faces in a mesh using OpenMaya API.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
    
    Returns:
        Dictionary with 'status', 'face_count', and 'mesh'.
    """
    try:
        import maya.cmds as cmds
        import maya.api.OpenMaya as om
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'face_count': 0,
        }
    
    try:
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
                'face_count': 0,
            }
        
        # Get the shape node if transform was provided
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                    'face_count': 0,
                }
            shape = shapes[0]
        
        # Use OpenMaya API
        selection = om.MSelectionList()
        selection.add(shape)
        dag_path = om.MDagPath()
        selection.getDagPath(0, dag_path)
        
        mesh_fn = om.MFnMesh(dag_path)
        face_count = mesh_fn.numPolygons()
        
        return {
            'status': 'success',
            'face_count': face_count,
            'mesh': mesh_name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'face_count': 0,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'face_count': 0,
        }


@mcp.tool
def get_mesh_edge_count(mesh_name: str) -> dict[str, Any]:
    """Get the number of edges in a mesh using OpenMaya API.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
    
    Returns:
        Dictionary with 'status', 'edge_count', and 'mesh'.
    """
    try:
        import maya.cmds as cmds
        import maya.api.OpenMaya as om
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'edge_count': 0,
        }
    
    try:
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
                'edge_count': 0,
            }
        
        # Get the shape node if transform was provided
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                    'edge_count': 0,
                }
            shape = shapes[0]
        
        # Use OpenMaya API
        selection = om.MSelectionList()
        selection.add(shape)
        dag_path = om.MDagPath()
        selection.getDagPath(0, dag_path)
        
        mesh_fn = om.MFnMesh(dag_path)
        edge_count = mesh_fn.numEdges()
        
        return {
            'status': 'success',
            'edge_count': edge_count,
            'mesh': mesh_name,
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'edge_count': 0,
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'edge_count': 0,
        }


@mcp.tool
def combine_meshes(
    mesh_names: list[str],
    name: str | None = None,
    merge_vertices: bool = True
) -> dict[str, Any]:
    """Combine multiple meshes into one.
    
    Args:
        mesh_names: List of mesh transform names to combine.
        name: Optional name for the combined mesh.
        merge_vertices: If True, merge vertices at the same location.
    
    Returns:
        Dictionary with 'status', 'combined_mesh', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not mesh_names:
        return {
            'status': 'error',
            'message': 'No mesh names provided',
        }
    
    try:
        # Filter to only existing meshes
        existing = [mesh for mesh in mesh_names if cmds.objExists(mesh)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the meshes exist: {mesh_names}',
            }
        
        kwargs = {}
        if merge_vertices:
            kwargs['mergeVertices'] = True
        
        result = cmds.polyUnite(existing, **kwargs)
        combined = result[0] if result else None
        
        if name and combined:
            combined = cmds.rename(combined, name)
        
        return {
            'status': 'success',
            'message': f'Combined {len(existing)} mesh(es)',
            'combined_mesh': combined,
            'source_meshes': existing,
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
    'get_mesh_vertices',
    'get_mesh_face_count',
    'get_mesh_edge_count',
    'combine_meshes',
]
