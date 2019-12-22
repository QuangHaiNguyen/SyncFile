from app import SyncFile
import unittest

config_file_empty = 'test/config_empty.txt'
config_file = 'test/config.txt'
config_list = []
destination_path = []
source_path = None

class TestReadConfigFile (unittest.TestCase):
     
    def test_read_config_file(self):
        SyncFile.read_config_file(config_file, config_list)

    def test_read_empty_config_file(self):
        self.assertRaises(Exception, SyncFile.read_config_file(config_file_empty, config_list))
    
    def test_get_destination_path(self):
        SyncFile.read_config_file(config_file, config_list)
        SyncFile.get_destination_path(config_list, destination_path)
        self.assertEqual(len(destination_path), 1)
        self.assertEqual(destination_path[0], 'Test Folder/Destination')

    def test_get_source_path(self):
        SyncFile.read_config_file(config_file, config_list)
        source_path = SyncFile.get_source_path(config_list)
        self.assertEqual(source_path, 'Test Folder/Origin')



