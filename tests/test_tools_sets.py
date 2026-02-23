"""Tests for sets and partitions tools."""

import unittest
from unittest.mock import MagicMock

from tests.test_helpers import mock_maya_available, mock_maya_unavailable
from maya_mcp.tools import sets


class TestSetsTools(unittest.TestCase):
    """Test cases for sets and partitions tools."""

    def test_create_set_no_maya(self):
        """Test create_set when Maya is not available."""
        with mock_maya_unavailable():
            result = sets.create_set(['pCube1'])
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_set_success(self):
        """Test create_set successfully creates set."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.sets.return_value = 'set1'
            
            result = sets.create_set(['pCube1', 'pSphere1'], name='mySet')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['set'], 'set1')
            mock_cmds.sets.assert_called_once()

    def test_create_partition_no_maya(self):
        """Test create_partition when Maya is not available."""
        with mock_maya_unavailable():
            result = sets.create_partition('myPartition')
            self.assertEqual(result['status'], 'error')
            self.assertIn('not available', result['message'])

    def test_create_partition_success(self):
        """Test create_partition successfully creates partition."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.partition.return_value = 'partition1'
            
            result = sets.create_partition('myPartition')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['partition'], 'partition1')
            mock_cmds.partition.assert_called_once()

    def test_add_to_set_success(self):
        """Test add_to_set successfully adds objects to set."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = sets.add_to_set('set1', ['pCube1', 'pSphere1'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.sets.assert_called_once()

    def test_remove_from_set_success(self):
        """Test remove_from_set successfully removes objects from set."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            
            result = sets.remove_from_set('set1', ['pCube1'])
            
            self.assertEqual(result['status'], 'success')
            mock_cmds.sets.assert_called_once()

    def test_list_sets_success(self):
        """Test list_sets successfully lists sets."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.ls.return_value = ['set1', 'set2', 'defaultObjectSet']
            
            result = sets.list_sets()
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['sets']), 2)  # Excludes defaultObjectSet

    def test_get_set_members_success(self):
        """Test get_set_members successfully gets set members."""
        with mock_maya_available() as mock_cmds:
            mock_cmds.objExists.return_value = True
            mock_cmds.sets.return_value = ['pCube1', 'pSphere1']
            
            result = sets.get_set_members('set1')
            
            self.assertEqual(result['status'], 'success')
            self.assertEqual(len(result['members']), 2)


if __name__ == '__main__':
    unittest.main()
