"""Script to update all test files to use the test helpers."""

import re
import os
from pathlib import Path

TEST_DIR = Path(__file__).parent

# Pattern to replace
OLD_PATTERN = r"with patch\('maya_mcp\.tools\.(\w+)\.maya', side_effect=ImportError\('No module named maya'\)\):"
NEW_PATTERN = "with mock_maya_unavailable():"

OLD_PATTERN2 = r"@patch\('maya_mcp\.tools\.(\w+)\.maya'\)\s+def (\w+)\(self, mock_maya\):"
NEW_PATTERN2 = r"def \2(self):"

def update_test_file(filepath):
    """Update a test file to use helpers."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import if not present
    if 'from tests.test_helpers import' not in content:
        # Find the last import
        import_match = re.search(r'(from unittest.mock import[^\n]+\n)', content)
        if import_match:
            content = content[:import_match.end()] + 'from tests.test_helpers import mock_maya_available, mock_maya_unavailable\n' + content[import_match.end():]
    
    # Replace patterns
    content = re.sub(
        r"with patch\('maya_mcp\.tools\.\w+\.maya', side_effect=ImportError\('No module named maya'\)\):",
        "with mock_maya_unavailable():",
        content
    )
    
    content = re.sub(
        r"with patch\('maya\.cmds', side_effect=ImportError\('No module named maya'\)\):",
        "with mock_maya_unavailable():",
        content
    )
    
    # Replace @patch decorators
    content = re.sub(
        r"@patch\('maya_mcp\.tools\.\w+\.maya'\)\s+def (\w+)\(self, mock_maya\):",
        r"def \1(self):",
        content
    )
    
    content = re.sub(
        r"@patch\('maya\.cmds'\)\s+def (\w+)\(self, mock_cmds\):",
        r"def \1(self):\n        with mock_maya_available() as mock_cmds:",
        content
    )
    
    # Fix mock_maya.cmds references
    content = re.sub(
        r'mock_maya\.cmds',
        'mock_cmds',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    for test_file in TEST_DIR.glob('test_*.py'):
        if test_file.name != 'test_helpers.py' and test_file.name != 'update_all_tests.py':
            print(f"Updating {test_file.name}...")
            update_test_file(test_file)
