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


@mcp.tool
def split_faces(
    mesh_name: str,
    faces: list[int] | None = None
) -> dict[str, Any]:
    """Split faces on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        faces: Optional list of face indices to split. If None, split selected faces.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        if faces:
            face_selection = [f'{shape}.f[{i}]' for i in faces]
            cmds.select(face_selection, replace=True)
        
        cmds.polySplit(shape)
        
        return {
            'status': 'success',
            'message': f'Split faces on {mesh_name}',
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
def collapse_edges(
    mesh_name: str,
    edges: list[int] | None = None
) -> dict[str, Any]:
    """Collapse edges on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        edges: Optional list of edge indices to collapse. If None, collapse selected edges.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        if edges:
            edge_selection = [f'{shape}.e[{i}]' for i in edges]
            cmds.select(edge_selection, replace=True)
        
        cmds.polyCollapseEdge(shape)
        
        return {
            'status': 'success',
            'message': f'Collapsed edges on {mesh_name}',
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
def triangulate_mesh(
    mesh_name: str
) -> dict[str, Any]:
    """Triangulate a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        cmds.polyTriangulate(shape)
        
        return {
            'status': 'success',
            'message': f'Triangulated mesh {mesh_name}',
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
def separate_mesh(
    mesh_name: str
) -> dict[str, Any]:
    """Separate a polygon mesh into separate objects.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
    
    Returns:
        Dictionary with 'status', 'separated_meshes', and 'message'.
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        result = cmds.polySeparate(shape)
        
        return {
            'status': 'success',
            'message': f'Separated mesh {mesh_name}',
            'separated_meshes': result if isinstance(result, list) else [result],
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
def set_polygon_normals(
    mesh_name: str,
    normal_mode: str = 'user'
) -> dict[str, Any]:
    """Set polygon normals on a mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        normal_mode: Normal mode - 'user', 'face', 'vertex', 'vertexFace'.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        cmds.polyNormal(shape, normalMode=normal_mode)
        
        return {
            'status': 'success',
            'message': f'Set polygon normals on {mesh_name} (mode: {normal_mode})',
            'mesh': mesh_name,
            'normal_mode': normal_mode,
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
def quadrangulate_mesh(
    mesh_name: str,
    angle_threshold: float = 30.0
) -> dict[str, Any]:
    """Convert triangles to quads on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        angle_threshold: Angle threshold in degrees for quadrangulation.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        cmds.polyQuadrangulate(shape, angleThreshold=angle_threshold)
        
        return {
            'status': 'success',
            'message': f'Quadrangulated mesh {mesh_name}',
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
def reduce_polygon_count(
    mesh_name: str,
    percentage: float = 50.0,
    keep_quads: bool = True
) -> dict[str, Any]:
    """Reduce polygon count on a mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        percentage: Reduction percentage (0-100).
        keep_quads: If True, try to keep quads during reduction.
    
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
            'percentage': percentage,
            'keepQuadsWeight': 1.0 if keep_quads else 0.0,
        }
        
        cmds.polyReduce(shape, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Reduced polygon count on {mesh_name} by {percentage}%',
            'mesh': mesh_name,
            'percentage': percentage,
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
def remesh_polygon(
    mesh_name: str,
    target_face_count: int = 1000,
    smooth_level: int = 1
) -> dict[str, Any]:
    """Remesh a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        target_face_count: Target number of faces.
        smooth_level: Smoothing level (0-3).
    
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
            'targetFaceCount': target_face_count,
            'smoothLevel': smooth_level,
        }
        
        cmds.polyRemesh(shape, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Remeshed {mesh_name} to {target_face_count} faces',
            'mesh': mesh_name,
            'target_face_count': target_face_count,
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
def flip_uvs(
    mesh_name: str,
    direction: str = 'u',
    uv_set: str = 'map1'
) -> dict[str, Any]:
    """Flip UVs on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        direction: Direction to flip - 'u' or 'v'.
        uv_set: Name of the UV set to flip.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        if direction not in ['u', 'v']:
            return {
                'status': 'error',
                'message': f'Invalid direction "{direction}". Must be "u" or "v"',
            }
        
        kwargs = {
            'flipType': 0 if direction == 'u' else 1,
            'uvSetName': uv_set,
        }
        
        cmds.polyFlipUV(shape, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Flipped UVs on {mesh_name} in {direction} direction',
            'mesh': mesh_name,
            'direction': direction,
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
def normalize_uvs(
    mesh_name: str,
    uv_set: str = 'map1'
) -> dict[str, Any]:
    """Normalize UVs on a polygon mesh (fit to 0-1 range).
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        uv_set: Name of the UV set to normalize.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        cmds.polyNormalizeUV(shape, uvSetName=uv_set)
        
        return {
            'status': 'success',
            'message': f'Normalized UVs on {mesh_name}',
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
def planar_projection_uvs(
    mesh_name: str,
    projection_axis: tuple[float, float, float] = (0.0, 1.0, 0.0),
    uv_set: str = 'map1'
) -> dict[str, Any]:
    """Apply planar UV projection to a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        projection_axis: Projection axis vector (default: (0, 1, 0) - Y axis).
        uv_set: Name of the UV set to create/modify.
    
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
            'projectionAxis': projection_axis,
            'uvSetName': uv_set,
        }
        
        cmds.polyPlanarProjection(shape, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Applied planar UV projection to {mesh_name}',
            'mesh': mesh_name,
            'projection_axis': projection_axis,
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
def apply_uv_projection(
    mesh_name: str,
    projection_type: str = 'planar',
    uv_set: str = 'map1'
) -> dict[str, Any]:
    """Apply various UV projections to a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        projection_type: Type of projection - 'planar', 'cylindrical', 'spherical'.
        uv_set: Name of the UV set to create/modify.
    
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
    
    valid_types = ['planar', 'cylindrical', 'spherical']
    if projection_type not in valid_types:
        return {
            'status': 'error',
            'message': f'Invalid projection type "{projection_type}". Must be one of: {valid_types}',
        }
    
    try:
        if not cmds.objExists(mesh_name):
            return {
                'status': 'error',
                'message': f'Mesh "{mesh_name}" does not exist',
            }
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        kwargs = {'uvSetName': uv_set}
        
        if projection_type == 'planar':
            cmds.polyProjection(shape, type=0, **kwargs)
        elif projection_type == 'cylindrical':
            cmds.polyProjection(shape, type=1, **kwargs)
        elif projection_type == 'spherical':
            cmds.polyProjection(shape, type=2, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Applied {projection_type} UV projection to {mesh_name}',
            'mesh': mesh_name,
            'projection_type': projection_type,
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
def smooth_faces(
    mesh_name: str,
    faces: list[int] | None = None,
    divisions: int = 1
) -> dict[str, Any]:
    """Smooth specific faces on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        faces: Optional list of face indices to smooth. If None, smooth selected faces.
        divisions: Number of smoothing divisions.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        if faces:
            face_selection = [f'{shape}.f[{i}]' for i in faces]
            cmds.select(face_selection, replace=True)
        
        cmds.polySmoothFace(shape, divisions=divisions)
        
        return {
            'status': 'success',
            'message': f'Smoothed faces on {mesh_name}',
            'mesh': mesh_name,
            'divisions': divisions,
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
def soften_edges(
    mesh_name: str,
    edges: list[int] | None = None,
    angle: float = 30.0
) -> dict[str, Any]:
    """Soften edges on a polygon mesh.
    
    Args:
        mesh_name: Name of the mesh transform or shape.
        edges: Optional list of edge indices to soften. If None, soften selected edges.
        angle: Angle threshold in degrees for softening.
    
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
        
        shape = mesh_name
        if cmds.objectType(mesh_name) == 'transform':
            shapes = cmds.listRelatives(mesh_name, shapes=True, type='mesh')
            if not shapes:
                return {
                    'status': 'error',
                    'message': f'No mesh shape found for "{mesh_name}"',
                }
            shape = shapes[0]
        
        if edges:
            edge_selection = [f'{shape}.e[{i}]' for i in edges]
            cmds.select(edge_selection, replace=True)
        
        cmds.polySoftEdge(shape, angle=angle)
        
        return {
            'status': 'success',
            'message': f'Softened edges on {mesh_name}',
            'mesh': mesh_name,
            'angle': angle,
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
def transfer_attributes(
    source_mesh: str,
    target_mesh: str,
    transfer_uvs: bool = True,
    transfer_colors: bool = False,
    transfer_normals: bool = False
) -> dict[str, Any]:
    """Transfer attributes (UVs, colors, normals) from one mesh to another.
    
    Args:
        source_mesh: Source mesh name.
        target_mesh: Target mesh name.
        transfer_uvs: If True, transfer UVs.
        transfer_colors: If True, transfer vertex colors.
        transfer_normals: If True, transfer normals.
    
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
        if not cmds.objExists(source_mesh):
            return {
                'status': 'error',
                'message': f'Source mesh "{source_mesh}" does not exist',
            }
        
        if not cmds.objExists(target_mesh):
            return {
                'status': 'error',
                'message': f'Target mesh "{target_mesh}" does not exist',
            }
        
        # Get shape nodes
        source_shape = source_mesh
        if cmds.objectType(source_mesh) == 'transform':
            shapes = cmds.listRelatives(source_mesh, shapes=True, type='mesh')
            if shapes:
                source_shape = shapes[0]
        
        target_shape = target_mesh
        if cmds.objectType(target_mesh) == 'transform':
            shapes = cmds.listRelatives(target_mesh, shapes=True, type='mesh')
            if shapes:
                target_shape = shapes[0]
        
        kwargs = {
            'uvSets': transfer_uvs,
            'colorSets': transfer_colors,
            'sampleSpace': 0,  # World space
        }
        
        if transfer_normals:
            kwargs['normals'] = True
        
        cmds.polyTransfer(target_shape, source=source_shape, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Transferred attributes from {source_mesh} to {target_mesh}',
            'source_mesh': source_mesh,
            'target_mesh': target_mesh,
            'transferred': {
                'uvs': transfer_uvs,
                'colors': transfer_colors,
                'normals': transfer_normals,
            },
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
    'split_faces',
    'collapse_edges',
    'triangulate_mesh',
    'separate_mesh',
    'set_polygon_normals',
    'quadrangulate_mesh',
    'reduce_polygon_count',
    'remesh_polygon',
    'flip_uvs',
    'normalize_uvs',
    'planar_projection_uvs',
    'apply_uv_projection',
    'smooth_faces',
    'soften_edges',
    'transfer_attributes',
]
