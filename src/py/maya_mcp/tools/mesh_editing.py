"""Advanced polygon mesh editing tools for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def extrude_faces(
    mesh_name: str,
    faces: list[int] | None = None,
    offset: float = 0.0,
    thickness: float = 0.0,
    divisions: int = 1
) -> dict[str, Any]:
    """Extrude faces on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        faces: Optional list of face indices to extrude. If None, extrude selected faces.
        offset: Offset distance for extrusion.
        thickness: Thickness for extrusion.
        divisions: Number of divisions for extrusion.
    
    Returns:
        Dictionary with 'status', 'extruded_faces', and 'message'.
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
        
        # Build face selection
        if faces:
            face_selection = [f'{shape}.f[{i}]' for i in faces]
            cmds.select(face_selection, replace=True)
        
        kwargs = {
            'offset': offset,
            'thickness': thickness,
            'divisions': divisions,
        }
        
        result = cmds.polyExtrudeFacet(**kwargs)
        
        return {
            'status': 'success',
            'message': f'Extruded faces on {mesh_name}',
            'mesh': mesh_name,
            'extruded_faces': result if isinstance(result, list) else [result],
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
def extrude_edges(
    mesh_name: str,
    edges: list[int] | None = None,
    offset: float = 0.0,
    thickness: float = 0.0,
    divisions: int = 1
) -> dict[str, Any]:
    """Extrude edges on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        edges: Optional list of edge indices to extrude. If None, extrude selected edges.
        offset: Offset distance for extrusion.
        thickness: Thickness for extrusion.
        divisions: Number of divisions for extrusion.
    
    Returns:
        Dictionary with 'status', 'extruded_edges', and 'message'.
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
        
        # Build edge selection
        if edges:
            edge_selection = [f'{shape}.e[{i}]' for i in edges]
            cmds.select(edge_selection, replace=True)
        
        kwargs = {
            'offset': offset,
            'thickness': thickness,
            'divisions': divisions,
        }
        
        result = cmds.polyExtrudeEdge(**kwargs)
        
        return {
            'status': 'success',
            'message': f'Extruded edges on {mesh_name}',
            'mesh': mesh_name,
            'extruded_edges': result if isinstance(result, list) else [result],
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
def bevel_edges(
    mesh_name: str,
    edges: list[int] | None = None,
    offset: float = 0.2,
    segments: int = 1,
    auto_fit: bool = True
) -> dict[str, Any]:
    """Bevel edges on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        edges: Optional list of edge indices to bevel. If None, bevel selected edges.
        offset: Offset distance for bevel.
        segments: Number of segments for bevel.
        auto_fit: If True, auto-fit bevel.
    
    Returns:
        Dictionary with 'status', 'beveled_edges', and 'message'.
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
        
        # Build edge selection
        if edges:
            edge_selection = [f'{shape}.e[{i}]' for i in edges]
            cmds.select(edge_selection, replace=True)
        
        kwargs = {
            'offset': offset,
            'segments': segments,
            'autoFit': auto_fit,
        }
        
        result = cmds.polyBevel(**kwargs)
        
        return {
            'status': 'success',
            'message': f'Beveled edges on {mesh_name}',
            'mesh': mesh_name,
            'beveled_edges': result if isinstance(result, list) else [result],
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
def smooth_mesh(
    mesh_name: str,
    divisions: int = 1,
    smoothness: float = 1.0
) -> dict[str, Any]:
    """Smooth a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        divisions: Number of smoothing divisions.
        smoothness: Smoothness value (0.0 to 1.0).
    
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
        
        kwargs = {
            'divisions': divisions,
            'smoothness': smoothness,
        }
        
        cmds.polySmooth(shape, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Smoothed mesh {mesh_name}',
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
def boolean_union(
    mesh1: str,
    mesh2: str,
    name: str | None = None
) -> dict[str, Any]:
    """Perform a boolean union operation on two meshes.
    
    Args:
        mesh1: First mesh name.
        mesh2: Second mesh name.
        name: Optional name for the result.
    
    Returns:
        Dictionary with 'status', 'result_mesh', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(mesh1):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh1}" does not exist',
            }
        
        if not cmds.objExists(mesh2):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh2}" does not exist',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.polyUnite(mesh1, mesh2, **kwargs)
        result_mesh = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Boolean union of {mesh1} and {mesh2}',
            'result_mesh': result_mesh,
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
def boolean_difference(
    mesh1: str,
    mesh2: str,
    name: str | None = None
) -> dict[str, Any]:
    """Perform a boolean difference operation (mesh1 - mesh2).
    
    Args:
        mesh1: First mesh name (base).
        mesh2: Second mesh name (to subtract).
        name: Optional name for the result.
    
    Returns:
        Dictionary with 'status', 'result_mesh', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(mesh1):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh1}" does not exist',
            }
        
        if not cmds.objExists(mesh2):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh2}" does not exist',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.polyBoolOp(mesh1, mesh2, op=2, **kwargs)  # op=2 is difference
        result_mesh = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Boolean difference: {mesh1} - {mesh2}',
            'result_mesh': result_mesh,
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
def boolean_intersection(
    mesh1: str,
    mesh2: str,
    name: str | None = None
) -> dict[str, Any]:
    """Perform a boolean intersection operation on two meshes.
    
    Args:
        mesh1: First mesh name.
        mesh2: Second mesh name.
        name: Optional name for the result.
    
    Returns:
        Dictionary with 'status', 'result_mesh', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(mesh1):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh1}" does not exist',
            }
        
        if not cmds.objExists(mesh2):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh2}" does not exist',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.polyBoolOp(mesh1, mesh2, op=1, **kwargs)  # op=1 is intersection
        result_mesh = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Boolean intersection of {mesh1} and {mesh2}',
            'result_mesh': result_mesh,
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
def merge_vertices(
    mesh_name: str,
    vertices: list[int] | None = None,
    distance: float = 0.0001
) -> dict[str, Any]:
    """Merge vertices on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        vertices: Optional list of vertex indices to merge. If None, merge all vertices within distance.
        distance: Distance threshold for merging.
    
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
        
        kwargs = {'distance': distance}
        
        if vertices:
            vertex_selection = [f'{shape}.vtx[{i}]' for i in vertices]
            cmds.select(vertex_selection, replace=True)
            cmds.polyMergeVertex(**kwargs)
        else:
            cmds.polyMergeVertex(shape, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Merged vertices on {mesh_name}',
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


__all__ = [
    'extrude_faces',
    'extrude_edges',
    'bevel_edges',
    'smooth_mesh',
    'boolean_union',
    'boolean_difference',
    'boolean_intersection',
    'merge_vertices',
]
