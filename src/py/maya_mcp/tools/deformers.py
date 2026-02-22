"""Deformer operations for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_blend_shape(
    base_mesh: str,
    target_meshes: list[str],
    name: str | None = None
) -> dict[str, Any]:
    """Create a blend shape deformer.
    
    Args:
        base_mesh: Base mesh name.
        target_meshes: List of target mesh names.
        name: Optional name for the blend shape node.
    
    Returns:
        Dictionary with 'status', 'blend_shape', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not target_meshes:
        return {
            'status': 'error',
            'message': 'No target meshes provided',
        }
    
    try:
        if not cmds.objExists(base_mesh):
            return {
                'status': 'error',
                'message': f'Base mesh "{base_mesh}" does not exist',
            }
        
        # Filter to only existing targets
        existing_targets = [mesh for mesh in target_meshes if cmds.objExists(mesh)]
        
        if not existing_targets:
            return {
                'status': 'error',
                'message': f'None of the target meshes exist: {target_meshes}',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        blend_shape = cmds.blendShape(existing_targets, base_mesh, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created blend shape with {len(existing_targets)} target(s)',
            'blend_shape': blend_shape[0] if blend_shape else None,
            'base_mesh': base_mesh,
            'targets': existing_targets,
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
def create_cluster(
    objects: list[str],
    name: str | None = None
) -> dict[str, Any]:
    """Create a cluster deformer.
    
    Args:
        objects: List of object names to cluster.
        name: Optional name for the cluster.
    
    Returns:
        Dictionary with 'status', 'cluster' (cluster handle), 'deformer' (deformer node), and 'message'.
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
        # Filter to only existing objects
        existing = [obj for obj in objects if cmds.objExists(obj)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the objects exist: {objects}',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.cluster(existing, **kwargs)
        cluster_handle = result[0] if result else None
        deformer = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created cluster for {len(existing)} object(s)',
            'cluster': cluster_handle,
            'deformer': deformer,
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
def create_lattice(
    object_name: str,
    divisions: tuple[int, int, int] = (5, 5, 5),
    name: str | None = None
) -> dict[str, Any]:
    """Create a lattice deformer.
    
    Args:
        object_name: Name of the object to deform.
        divisions: Number of divisions (S, T, U).
        name: Optional name for the lattice.
    
    Returns:
        Dictionary with 'status', 'lattice' (lattice transform), 'base' (base transform), 'ffd' (ffd node), and 'message'.
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
        
        kwargs = {
            'divisions': f'{divisions[0]} {divisions[1]} {divisions[2]}',
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.lattice(object_name, **kwargs)
        lattice = result[0] if result else None
        base = result[1] if len(result) > 1 else None
        ffd = result[2] if len(result) > 2 else None
        
        return {
            'status': 'success',
            'message': f'Created lattice deformer for {object_name}',
            'lattice': lattice,
            'base': base,
            'ffd': ffd,
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
def create_bend_deformer(
    object_name: str,
    curvature: float = 0.0,
    low_bound: float = -1.0,
    high_bound: float = 1.0,
    name: str | None = None
) -> dict[str, Any]:
    """Create a bend (non-linear) deformer.
    
    Args:
        object_name: Name of the object to deform.
        curvature: Curvature value.
        low_bound: Low bound value.
        high_bound: High bound value.
        name: Optional name for the deformer.
    
    Returns:
        Dictionary with 'status', 'deformer' (deformer handle), and 'message'.
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
        
        kwargs = {
            'curvature': curvature,
            'lowBound': low_bound,
            'highBound': high_bound,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.nonLinear(object_name, type='bend', **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created bend deformer for {object_name}',
            'deformer': deformer,
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
def create_twist_deformer(
    object_name: str,
    start_angle: float = 0.0,
    end_angle: float = 0.0,
    low_bound: float = -1.0,
    high_bound: float = 1.0,
    name: str | None = None
) -> dict[str, Any]:
    """Create a twist (non-linear) deformer.
    
    Args:
        object_name: Name of the object to deform.
        start_angle: Start angle in degrees.
        end_angle: End angle in degrees.
        low_bound: Low bound value.
        high_bound: High bound value.
        name: Optional name for the deformer.
    
    Returns:
        Dictionary with 'status', 'deformer' (deformer handle), and 'message'.
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
        
        kwargs = {
            'startAngle': start_angle,
            'endAngle': end_angle,
            'lowBound': low_bound,
            'highBound': high_bound,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.nonLinear(object_name, type='twist', **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created twist deformer for {object_name}',
            'deformer': deformer,
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
def create_sine_deformer(
    object_name: str,
    amplitude: float = 0.0,
    wavelength: float = 2.0,
    low_bound: float = -1.0,
    high_bound: float = 1.0,
    name: str | None = None
) -> dict[str, Any]:
    """Create a sine (non-linear) deformer.
    
    Args:
        object_name: Name of the object to deform.
        amplitude: Amplitude value.
        wavelength: Wavelength value.
        low_bound: Low bound value.
        high_bound: High bound value.
        name: Optional name for the deformer.
    
    Returns:
        Dictionary with 'status', 'deformer' (deformer handle), and 'message'.
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
        
        kwargs = {
            'amplitude': amplitude,
            'wavelength': wavelength,
            'lowBound': low_bound,
            'highBound': high_bound,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.nonLinear(object_name, type='sine', **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created sine deformer for {object_name}',
            'deformer': deformer,
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
def create_squash_deformer(
    object_name: str,
    factor: float = 0.0,
    low_bound: float = -1.0,
    high_bound: float = 1.0,
    name: str | None = None
) -> dict[str, Any]:
    """Create a squash (non-linear) deformer.
    
    Args:
        object_name: Name of the object to deform.
        factor: Squash factor value.
        low_bound: Low bound value.
        high_bound: High bound value.
        name: Optional name for the deformer.
    
    Returns:
        Dictionary with 'status', 'deformer' (deformer handle), and 'message'.
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
        
        kwargs = {
            'factor': factor,
            'lowBound': low_bound,
            'highBound': high_bound,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.nonLinear(object_name, type='squash', **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created squash deformer for {object_name}',
            'deformer': deformer,
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
def list_deformers(object_name: str) -> dict[str, Any]:
    """List all deformers on an object.
    
    Args:
        object_name: Name of the object.
    
    Returns:
        Dictionary with 'status', 'deformers' (list), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
            'deformers': [],
        }
    
    try:
        if not cmds.objExists(object_name):
            return {
                'status': 'error',
                'message': f'Object "{object_name}" does not exist',
                'deformers': [],
            }
        
        history = cmds.listHistory(object_name)
        deformer_types = [
            'blendShape', 'cluster', 'ffd', 'nonLinear', 'wire', 'sculpt',
            'jiggle', 'softMod', 'tension', 'deltaMush', 'shrinkWrap', 'wrap'
        ]
        
        deformers = []
        for node in history or []:
            node_type = cmds.nodeType(node)
            if node_type in deformer_types:
                deformers.append(node)
        
        return {
            'status': 'success',
            'message': f'Found {len(deformers)} deformer(s) on {object_name}',
            'deformers': deformers,
            'count': len(deformers),
        }
    except RuntimeError as err:
        return {
            'status': 'error',
            'message': f'Maya error: {err}',
            'deformers': [],
        }
    except Exception as err:
        return {
            'status': 'error',
            'message': f'Unexpected error: {err}',
            'deformers': [],
        }


__all__ = [
    'create_blend_shape',
    'create_cluster',
    'create_lattice',
    'create_bend_deformer',
    'create_twist_deformer',
    'create_sine_deformer',
    'create_squash_deformer',
    'list_deformers',
]
