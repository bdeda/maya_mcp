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
            'jiggle', 'softMod', 'tension', 'deltaMush', 'shrinkWrap', 'wrap',
            'wrinkle'
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


@mcp.tool
def create_sculpt_deformer(
    object_name: str,
    name: str | None = None
) -> dict[str, Any]:
    """Create a sculpt deformer.
    
    Args:
        object_name: Name of the object to deform.
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
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.sculpt(object_name, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created sculpt deformer for {object_name}',
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
def create_wire_deformer(
    object_name: str,
    wire_curve: str,
    name: str | None = None
) -> dict[str, Any]:
    """Create a wire deformer.
    
    Args:
        object_name: Name of the object to deform.
        wire_curve: Name of the curve to use as wire.
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
        
        if not cmds.objExists(wire_curve):
            return {
                'status': 'error',
                'message': f'Wire curve "{wire_curve}" does not exist',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.wire(object_name, wire=wire_curve, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created wire deformer for {object_name}',
            'deformer': deformer,
            'wire_curve': wire_curve,
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
def create_wrinkle_deformer(
    object_name: str,
    name: str | None = None
) -> dict[str, Any]:
    """Create a wrinkle deformer.
    
    Args:
        object_name: Name of the object to deform.
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
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.wrinkle(object_name, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created wrinkle deformer for {object_name}',
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
def create_jiggle_deformer(
    object_name: str,
    stiffness: float = 0.5,
    damping: float = 0.5,
    name: str | None = None
) -> dict[str, Any]:
    """Create a jiggle deformer.
    
    Args:
        object_name: Name of the object to deform.
        stiffness: Stiffness value (0-1).
        damping: Damping value (0-1).
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
            'stiffness': stiffness,
            'damping': damping,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.jiggle(object_name, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created jiggle deformer for {object_name}',
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
def create_soft_mod_deformer(
    object_name: str,
    falloff_radius: float = 5.0,
    name: str | None = None
) -> dict[str, Any]:
    """Create a soft modification deformer.
    
    Args:
        object_name: Name of the object to deform.
        falloff_radius: Falloff radius for the soft modification.
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
            'falloffRadius': falloff_radius,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.softMod(object_name, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created soft modification deformer for {object_name}',
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
def create_tension_deformer(
    object_name: str,
    low_value: float = 0.0,
    high_value: float = 1.0,
    name: str | None = None
) -> dict[str, Any]:
    """Create a tension deformer.
    
    Args:
        object_name: Name of the object to deform.
        low_value: Low tension value.
        high_value: High tension value.
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
            'lowBound': low_value,
            'highBound': high_value,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.tension(object_name, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created tension deformer for {object_name}',
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
def create_delta_mush_deformer(
    object_name: str,
    smoothing_iterations: int = 10,
    smoothing_step: float = 0.5,
    name: str | None = None
) -> dict[str, Any]:
    """Create a delta mush deformer.
    
    Args:
        object_name: Name of the object to deform.
        smoothing_iterations: Number of smoothing iterations.
        smoothing_step: Smoothing step value.
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
            'smoothingIterations': smoothing_iterations,
            'smoothingStep': smoothing_step,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.deltaMush(object_name, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created delta mush deformer for {object_name}',
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
def create_shrink_wrap_deformer(
    object_name: str,
    target_mesh: str,
    name: str | None = None
) -> dict[str, Any]:
    """Create a shrink wrap deformer.
    
    Args:
        object_name: Name of the object to deform.
        target_mesh: Name of the target mesh to shrink wrap to.
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
        
        if not cmds.objExists(target_mesh):
            return {
                'status': 'error',
                'message': f'Target mesh "{target_mesh}" does not exist',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.shrinkWrap(object_name, target=target_mesh, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created shrink wrap deformer for {object_name}',
            'deformer': deformer,
            'target_mesh': target_mesh,
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
def create_wrap_deformer(
    object_name: str,
    driver_mesh: str,
    name: str | None = None
) -> dict[str, Any]:
    """Create a wrap deformer.
    
    Args:
        object_name: Name of the object to deform.
        driver_mesh: Name of the driver mesh.
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
        
        if not cmds.objExists(driver_mesh):
            return {
                'status': 'error',
                'message': f'Driver mesh "{driver_mesh}" does not exist',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.wrap(object_name, driver=driver_mesh, **kwargs)
        deformer = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Created wrap deformer for {object_name}',
            'deformer': deformer,
            'driver_mesh': driver_mesh,
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
    'create_blend_shape',
    'create_cluster',
    'create_lattice',
    'create_bend_deformer',
    'create_twist_deformer',
    'create_sine_deformer',
    'create_squash_deformer',
    'create_sculpt_deformer',
    'create_wire_deformer',
    'create_wrinkle_deformer',
    'create_jiggle_deformer',
    'create_soft_mod_deformer',
    'create_tension_deformer',
    'create_delta_mush_deformer',
    'create_shrink_wrap_deformer',
    'create_wrap_deformer',
    'list_deformers',
]
