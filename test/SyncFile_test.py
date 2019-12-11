from app import SyncFile
import unittest

config_file_empty = 'config_empty.txt'
config_file_not_exist = 'config_not_exist.txt'
config_file = 'config.txt'
config_list = []

class TestReadConfigFile (unittest.TestCase):
    
    #Read correct file 
    def test_read_config_file(self):
        SyncFile.read_config_file(config_file, config_list)
    
    def test_config_file_not_exist(self):
        self.assertRaises(FileNotFoundError, SyncFile.read_config_file(config_file_not_exist, config_list))

    def test_read_empty_config_file(self):
        self.assertRaises(Exception, SyncFile.read_config_file(config_file_empty, config_list))



