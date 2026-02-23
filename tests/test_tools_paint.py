"""Tests for paint tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import paint


class TestPaintTools(unittest.TestCase):
    """Test cases for paint tools."""

    def test_get_skin_weights_no_maya(self):
        """Test get_skin_weights when Maya is not available."""
        with mock_maya_unavailable():
            result = paint.get_skin_weights('pCube1')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_get_skin_weights_success(self):
        """Test get_skin_weights successfully retrieves weights."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'transform'
            mock_cmds.listRelatives.return_value = ['pCubeShape1']
            mock_cmds.listHistory.return_value = ['skinCluster1']
            mock_cmds.nodeType.return_value = 'skinCluster'
            mock_cmds.skinCluster.return_value = ['joint1', 'joint2']
            mock_cmds.polyEvaluate.return_value = 2
            mock_cmds.skinPercent.return_value = [0.5]
            
            result = paint.get_skin_weights('pCube1')
            
            self.assertEqual(result['status'], 'success')
            self.assertIn('weights', result)

    def test_set_skin_weights_success(self):
        """Test set_skin_weights successfully sets weights."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.objectType.return_value = 'transform'
            mock_cmds.listRelatives.return_value = ['pCubeShape1']
            mock_cmds.listHistory.return_value = ['skinCluster1']
            mock_cmds.nodeType.return_value = 'skinCluster'
            
            weights = {0: {'joint1': 0.8, 'joint2': 0.2}}
            result = paint.set_skin_weights('pCube1', weights)
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.skinPercent.assert_called()


if __name__ == '__main__':
    unittest.main()
