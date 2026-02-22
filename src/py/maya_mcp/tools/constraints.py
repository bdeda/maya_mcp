"""Advanced constraint operations for Maya."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_aim_constraint(
    target: str,
    constrained: str,
    aim_vector: tuple[float, float, float] = (1.0, 0.0, 0.0),
    up_vector: tuple[float, float, float] = (0.0, 1.0, 0.0),
    maintain_offset: bool = True,
    name: str | None = None
) -> dict[str, Any]:
    """Create an aim constraint.
    
    Args:
        target: Target object name.
        constrained: Constrained object name.
        aim_vector: Aim vector (default: (1, 0, 0)).
        up_vector: Up vector (default: (0, 1, 0)).
        maintain_offset: If True, maintain offset between objects.
        name: Optional name for the constraint.
    
    Returns:
        Dictionary with 'status', 'constraint', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(target):
            return {
                'status': 'error',
                'message': f'Target "{target}" does not exist',
            }
        
        if not cmds.objExists(constrained):
            return {
                'status': 'error',
                'message': f'Constrained object "{constrained}" does not exist',
            }
        
        kwargs = {
            'target': target,
            'aimVector': aim_vector,
            'upVector': up_vector,
            'maintainOffset': maintain_offset,
        }
        if name:
            kwargs['name'] = name
        
        constraint = cmds.aimConstraint(constrained, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created aim constraint: {constraint[0] if constraint else None}',
            'constraint': constraint[0] if constraint else None,
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
def create_scale_constraint(
    target: str,
    constrained: str,
    maintain_offset: bool = True,
    name: str | None = None
) -> dict[str, Any]:
    """Create a scale constraint.
    
    Args:
        target: Target object name.
        constrained: Constrained object name.
        maintain_offset: If True, maintain offset between objects.
        name: Optional name for the constraint.
    
    Returns:
        Dictionary with 'status', 'constraint', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(target):
            return {
                'status': 'error',
                'message': f'Target "{target}" does not exist',
            }
        
        if not cmds.objExists(constrained):
            return {
                'status': 'error',
                'message': f'Constrained object "{constrained}" does not exist',
            }
        
        kwargs = {'target': target, 'maintainOffset': maintain_offset}
        if name:
            kwargs['name'] = name
        
        constraint = cmds.scaleConstraint(constrained, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created scale constraint: {constraint[0] if constraint else None}',
            'constraint': constraint[0] if constraint else None,
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
def create_geometry_constraint(
    target: str,
    constrained: str,
    maintain_offset: bool = True,
    name: str | None = None
) -> dict[str, Any]:
    """Create a geometry constraint.
    
    Args:
        target: Target object name (surface/mesh).
        constrained: Constrained object name.
        maintain_offset: If True, maintain offset between objects.
        name: Optional name for the constraint.
    
    Returns:
        Dictionary with 'status', 'constraint', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(target):
            return {
                'status': 'error',
                'message': f'Target "{target}" does not exist',
            }
        
        if not cmds.objExists(constrained):
            return {
                'status': 'error',
                'message': f'Constrained object "{constrained}" does not exist',
            }
        
        kwargs = {'target': target, 'maintainOffset': maintain_offset}
        if name:
            kwargs['name'] = name
        
        constraint = cmds.geometryConstraint(constrained, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created geometry constraint: {constraint[0] if constraint else None}',
            'constraint': constraint[0] if constraint else None,
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
def remove_constraint(constraint_name: str) -> dict[str, Any]:
    """Remove a constraint.
    
    Args:
        constraint_name: Name of the constraint to remove.
    
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
        if not cmds.objExists(constraint_name):
            return {
                'status': 'error',
                'message': f'Constraint "{constraint_name}" does not exist',
            }
        
        cmds.delete(constraint_name)
        
        return {
            'status': 'success',
            'message': f'Removed constraint: {constraint_name}',
            'constraint': constraint_name,
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
    'create_aim_constraint',
    'create_scale_constraint',
    'create_geometry_constraint',
    'remove_constraint',
]
