"""NURBS operations for Maya - curves and surfaces."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_nurbs_circle(
    name: str | None = None,
    radius: float = 1.0,
    degree: int = 3
) -> dict[str, Any]:
    """Create a NURBS circle.
    
    Args:
        name: Optional name for the circle.
        radius: Radius of the circle.
        degree: Degree of the curve (1=linear, 2=quadratic, 3=cubic).
    
    Returns:
        Dictionary with 'status', 'circle' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {
            'radius': radius,
            'degree': degree,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.circle(**kwargs)
        transform = result[0] if result else None
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created NURBS circle: {transform}',
            'circle': transform,
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
def create_nurbs_sphere(
    name: str | None = None,
    radius: float = 1.0,
    start_sweep: float = 0.0,
    end_sweep: float = 360.0
) -> dict[str, Any]:
    """Create a NURBS sphere.
    
    Args:
        name: Optional name for the sphere.
        radius: Radius of the sphere.
        start_sweep: Start sweep angle in degrees.
        end_sweep: End sweep angle in degrees.
    
    Returns:
        Dictionary with 'status', 'sphere' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {
            'radius': radius,
            'startSweep': start_sweep,
            'endSweep': end_sweep,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.sphere(**kwargs)
        transform = result[0] if result else None
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created NURBS sphere: {transform}',
            'sphere': transform,
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
def create_curve_from_points(
    points: list[tuple[float, float, float]],
    degree: int = 3,
    name: str | None = None
) -> dict[str, Any]:
    """Create a NURBS curve from a list of points.
    
    Args:
        points: List of (x, y, z) tuples defining curve points.
        degree: Degree of the curve (1=linear, 2=quadratic, 3=cubic).
        name: Optional name for the curve.
    
    Returns:
        Dictionary with 'status', 'curve' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not points:
        return {
            'status': 'error',
            'message': 'No points provided',
        }
    
    try:
        # Flatten points list
        point_list = []
        for point in points:
            point_list.extend(point)
        
        kwargs = {
            'degree': degree,
            'point': point_list,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.curve(**kwargs)
        transform = result[0] if result else None
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created curve from {len(points)} point(s): {transform}',
            'curve': transform,
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
def loft_surfaces(
    curves: list[str],
    name: str | None = None,
    uniform: bool = True,
    close: bool = False
) -> dict[str, Any]:
    """Create a NURBS surface by lofting curves.
    
    Args:
        curves: List of curve names to loft.
        name: Optional name for the lofted surface.
        uniform: If True, use uniform parameterization.
        close: If True, close the loft.
    
    Returns:
        Dictionary with 'status', 'surface' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not curves:
        return {
            'status': 'error',
            'message': 'No curves provided',
        }
    
    try:
        # Filter to only existing curves
        existing = [curve for curve in curves if cmds.objExists(curve)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the curves exist: {curves}',
            }
        
        kwargs = {
            'uniform': uniform,
            'close': close,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.loft(existing, **kwargs)
        transform = result[0] if result else None
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Lofted {len(existing)} curve(s)',
            'surface': transform,
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
def revolve_curve(
    curve_name: str,
    axis: tuple[float, float, float] = (0.0, 1.0, 0.0),
    pivot: tuple[float, float, float] = (0.0, 0.0, 0.0),
    start_angle: float = 0.0,
    end_angle: float = 360.0,
    name: str | None = None
) -> dict[str, Any]:
    """Create a NURBS surface by revolving a curve.
    
    Args:
        curve_name: Name of the curve to revolve.
        axis: Axis of revolution (default: (0, 1, 0) - Y axis).
        pivot: Pivot point for revolution.
        start_angle: Start angle in degrees.
        end_angle: End angle in degrees.
        name: Optional name for the revolved surface.
    
    Returns:
        Dictionary with 'status', 'surface' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(curve_name):
            return {
                'status': 'error',
                'message': f'Curve "{curve_name}" does not exist',
            }
        
        kwargs = {
            'axis': axis,
            'pivot': pivot,
            'startAngle': start_angle,
            'endAngle': end_angle,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.revolve(curve_name, **kwargs)
        transform = result[0] if result else None
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Revolved curve {curve_name}',
            'surface': transform,
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
def create_nurbs_cylinder(
    name: str | None = None,
    radius: float = 1.0,
    height: float = 2.0
) -> dict[str, Any]:
    """Create a NURBS cylinder.
    
    Args:
        name: Optional name for the cylinder.
        radius: Radius of the cylinder.
        height: Height of the cylinder.
    
    Returns:
        Dictionary with 'status', 'cylinder' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {
            'radius': radius,
            'heightRatio': height / radius,
        }
        if name:
            kwargs['name'] = name
        
        result = cmds.cylinder(**kwargs)
        transform = result[0] if result else None
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created NURBS cylinder: {transform}',
            'cylinder': transform,
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
def attach_curves(
    curve1: str,
    curve2: str,
    name: str | None = None
) -> dict[str, Any]:
    """Attach two NURBS curves together.
    
    Args:
        curve1: First curve name.
        curve2: Second curve name.
        name: Optional name for the result.
    
    Returns:
        Dictionary with 'status', 'curve' (result curve), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(curve1):
            return {
                'status': 'error',
                'message': f'Curve "{curve1}" does not exist',
            }
        
        if not cmds.objExists(curve2):
            return {
                'status': 'error',
                'message': f'Curve "{curve2}" does not exist',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.attachCurve(curve1, curve2, **kwargs)
        curve = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Attached curves {curve1} and {curve2}',
            'curve': curve,
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
def close_curve(
    curve_name: str
) -> dict[str, Any]:
    """Close a NURBS curve.
    
    Args:
        curve_name: Name of the curve to close.
    
    Returns:
        Dictionary with 'status', 'curve' (closed curve), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(curve_name):
            return {
                'status': 'error',
                'message': f'Curve "{curve_name}" does not exist',
            }
        
        result = cmds.closeCurve(curve_name)
        curve = result[0] if result else None
        
        return {
            'status': 'success',
            'message': f'Closed curve {curve_name}',
            'curve': curve,
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
def create_planar_surface(
    curves: list[str],
    name: str | None = None
) -> dict[str, Any]:
    """Create a planar NURBS surface from curves.
    
    Args:
        curves: List of curve names forming a closed boundary.
        name: Optional name for the surface.
    
    Returns:
        Dictionary with 'status', 'surface' (transform name), and 'shape' (shape name).
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    if not curves:
        return {
            'status': 'error',
            'message': 'No curves provided',
        }
    
    try:
        existing = [curve for curve in curves if cmds.objExists(curve)]
        
        if not existing:
            return {
                'status': 'error',
                'message': f'None of the curves exist: {curves}',
            }
        
        kwargs = {}
        if name:
            kwargs['name'] = name
        
        result = cmds.planar(existing, **kwargs)
        transform = result[0] if result else None
        shape = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created planar surface from {len(existing)} curve(s)',
            'surface': transform,
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


__all__ = [
    'create_nurbs_circle',
    'create_nurbs_sphere',
    'create_nurbs_cylinder',
    'create_curve_from_points',
    'attach_curves',
    'close_curve',
    'loft_surfaces',
    'revolve_curve',
    'create_planar_surface',
]
