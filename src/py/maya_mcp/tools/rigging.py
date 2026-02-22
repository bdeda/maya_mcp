"""Rigging tools for Maya - joints, IK, constraints."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import maya.cmds  # type: ignore[import-untyped]

from maya_mcp import mcp


@mcp.tool
def create_joint(
    name: str | None = None,
    position: tuple[float, float, float] | None = None,
    parent: str | None = None
) -> dict[str, Any]:
    """Create a joint.
    
    Args:
        name: Optional name for the joint.
        position: Optional (x, y, z) position for the joint.
        parent: Optional parent joint.
    
    Returns:
        Dictionary with 'status', 'joint' (joint name), and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        kwargs = {}
        if name:
            kwargs['name'] = name
        if parent and cmds.objExists(parent):
            kwargs['parent'] = parent
        
        joint = cmds.joint(**kwargs)
        
        if position:
            cmds.move(position[0], position[1], position[2], joint, absolute=True)
        
        return {
            'status': 'success',
            'message': f'Created joint: {joint}',
            'joint': joint,
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
def create_ik_handle(
    start_joint: str,
    end_joint: str,
    name: str | None = None,
    solver: str = 'ikRPsolver'
) -> dict[str, Any]:
    """Create an IK handle between two joints.
    
    Args:
        start_joint: Start joint name.
        end_joint: End joint name.
        name: Optional name for the IK handle.
        solver: IK solver type ('ikRPsolver', 'ikSCsolver', 'ikSplineSolver').
    
    Returns:
        Dictionary with 'status', 'ik_handle', 'effector', and 'message'.
    """
    try:
        import maya.cmds as cmds
    except ImportError:
        return {
            'status': 'error',
            'message': 'Maya is not available',
        }
    
    try:
        if not cmds.objExists(start_joint):
            return {
                'status': 'error',
                'message': f'Start joint "{start_joint}" does not exist',
            }
        
        if not cmds.objExists(end_joint):
            return {
                'status': 'error',
                'message': f'End joint "{end_joint}" does not exist',
            }
        
        kwargs = {'startJoint': start_joint, 'endEffector': end_joint, 'solver': solver}
        if name:
            kwargs['name'] = name
        
        result = cmds.ikHandle(**kwargs)
        ik_handle = result[0] if result else None
        effector = result[1] if len(result) > 1 else None
        
        return {
            'status': 'success',
            'message': f'Created IK handle: {ik_handle}',
            'ik_handle': ik_handle,
            'effector': effector,
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
def create_parent_constraint(
    target: str,
    constrained: str,
    maintain_offset: bool = True,
    name: str | None = None
) -> dict[str, Any]:
    """Create a parent constraint.
    
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
        
        constraint = cmds.parentConstraint(constrained, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created parent constraint: {constraint[0] if constraint else None}',
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
def create_point_constraint(
    target: str,
    constrained: str,
    maintain_offset: bool = True,
    name: str | None = None
) -> dict[str, Any]:
    """Create a point constraint.
    
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
        
        constraint = cmds.pointConstraint(constrained, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created point constraint: {constraint[0] if constraint else None}',
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
def create_orient_constraint(
    target: str,
    constrained: str,
    maintain_offset: bool = True,
    name: str | None = None
) -> dict[str, Any]:
    """Create an orient constraint.
    
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
        
        constraint = cmds.orientConstraint(constrained, **kwargs)
        
        return {
            'status': 'success',
            'message': f'Created orient constraint: {constraint[0] if constraint else None}',
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


__all__ = [
    'create_joint',
    'create_ik_handle',
    'create_parent_constraint',
    'create_point_constraint',
    'create_orient_constraint',
]
