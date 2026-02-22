"""Safety filters and helpers for Maya MCP tools.

This module provides functions to filter out dangerous Maya commands
and ensure safe operation of the MCP server.
"""

# Commands that should never be exposed via MCP
BLOCKED_COMMANDS = {
    'scriptNode',  # Creates script nodes that execute code
    'eval',  # Executes arbitrary MEL/Python code
    'evalDeferred',  # Executes deferred code
    'evalEcho',  # Echoes eval output
    'python',  # Executes Python code
    'mel',  # Executes MEL code
    'source',  # Sources script files
    'scriptJob',  # Creates script callbacks
    'callbacks',  # Manages callbacks
    'callback',  # Creates callbacks
    'eval',  # General eval command
    'dgeval',  # Dependency graph evaluation
}

# Commands that create callbacks (should be blocked)
CALLBACK_COMMANDS = {
    'scriptJob',
    'callbacks',
    'callback',
    'addCallback',
    'removeCallback',
    'callbackManager',
}

# Commands that execute scripts (should be blocked)
SCRIPT_EXECUTION_COMMANDS = {
    'scriptNode',
    'eval',
    'evalDeferred',
    'evalEcho',
    'python',
    'mel',
    'source',
    'runTimeCommand',  # Creates runtime commands
    'nameCommand',  # Creates name commands
}


def is_command_blocked(command_name: str) -> bool:
    """Check if a command should be blocked from MCP exposure.
    
    Args:
        command_name: Name of the Maya command to check.
    
    Returns:
        True if the command should be blocked, False otherwise.
    """
    command_lower = command_name.lower()
    
    # Check exact matches
    if command_lower in BLOCKED_COMMANDS:
        return True
    
    # Check if it's a callback-related command
    if 'callback' in command_lower and command_lower in CALLBACK_COMMANDS:
        return True
    
    # Check if it's a script execution command
    if command_lower in SCRIPT_EXECUTION_COMMANDS:
        return True
    
    # Block commands that contain dangerous patterns
    dangerous_patterns = ['script', 'eval', 'execute', 'source']
    for pattern in dangerous_patterns:
        if pattern in command_lower and command_lower not in {
            'scriptEditorInfo',  # Safe - just queries script editor
            'scriptedPanel',  # Safe - UI panel management
            'scriptedPanelType',  # Safe - panel type registration
        }:
            # Additional check: only block if it's actually dangerous
            if command_lower in BLOCKED_COMMANDS or command_lower in SCRIPT_EXECUTION_COMMANDS:
                return True
    
    return False


def safe_maya_command(command_name: str, *args, **kwargs) -> dict[str, str | any]:
    """Safely execute a Maya command with error handling.
    
    Args:
        command_name: Name of the Maya command to execute.
        *args: Positional arguments for the command.
        **kwargs: Keyword arguments for the command.
    
    Returns:
        Dictionary with 'status' ('success' or 'error'), 'result' (if success),
        and 'message' (if error).
    
    Raises:
        ValueError: If the command is blocked for safety reasons.
    """
    if is_command_blocked(command_name):
        raise ValueError(
            f'Command "{command_name}" is blocked for safety reasons. '
            'Script execution and callback creation are not allowed via MCP.'
        )
    
    try:
        import maya.cmds as cmds
        
        # Get the command function
        if not hasattr(cmds, command_name):
            return {
                'status': 'error',
                'message': f'Command "{command_name}" does not exist',
            }
        
        cmd_func = getattr(cmds, command_name)
        
        # Execute the command
        result = cmd_func(*args, **kwargs)
        
        return {
            'status': 'success',
            'result': result,
        }
    except ValueError as err:
        # Re-raise safety errors
        raise
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
    'is_command_blocked',
    'safe_maya_command',
    'BLOCKED_COMMANDS',
    'CALLBACK_COMMANDS',
    'SCRIPT_EXECUTION_COMMANDS',
]
