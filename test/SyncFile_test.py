from app import SyncFile
import unittest

config_file_empty = 'test/config_empty.txt'
config_file = 'test/config.txt'
config_list = []
destination_path = []
source_path = None
log_file = 'test/log.txt'

class TestReadConfigFile (unittest.TestCase):
     
    def test_read_config_file(self):
        SyncFile.read_config_file(config_file, config_list, config_file)

    def test_read_empty_config_file(self):
        self.assertRaises(Exception, SyncFile.read_config_file(config_file_empty, config_list, config_file_empty))
    
    def test_get_destination_path(self):
        SyncFile.read_config_file(config_file, config_list, config_file)
        SyncFile.get_destination_path(config_list, destination_path)
        self.assertEqual(len(destination_path), 1)
        self.assertEqual(destination_path[0], 'Test Folder/Destination')

    def test_get_source_path(self):
        SyncFile.read_config_file(config_file, config_list, config_file)
        source_path = SyncFile.get_source_path(config_list)
        self.assertEqual(source_path, 'Test Folder/Origin')

class TestReadLogFile(unittest.TestCase):
    def test_create_log_file(self):
        self.assertRaises(Exception,SyncFile.create_log_file(log_file))

