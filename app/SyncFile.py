""" Application Description here
# TODO: write description
# TODO: readme
"""
import os
import logging
import sys
import hashlib
from datetime import datetime
from dirsync import sync
import time
import progressbar


# init logging level
# set logging level to DEBUG for DEBUG message
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

config_file = 'app/config.txt'
log_file = 'app/log.txt'
config_list = []
source_path = None
destination_path = []

def read_config_file(file_name, config_list, config_file_path):
    """ Read the config file and parse the content of config file into a list

    Parameters
    ----------
    file_name:      path to the config file
    config_list:    list to store the content of config file
    """
    
    try:
        # Open the config file and read line by line
        with open(file_name) as config_file:
            for line in config_file:
                config_list.append(line.rstrip())
    except FileNotFoundError as error:
        print("Could not find any configuration file. New configuration file is being created...")
        create_config_file(config_file_path)
        print("please press any key to close the application")
        input() #pause the application, waiting for user input
        sys.exit(0)
    else:
        # Raise error if config file is empty
        if len(config_list) == 0:
            raise ValueError('[Error] Config file is empty')

def create_config_file(config_file_path):
    """ Create a config file with a template
    
    After template is created the code will ask the user to modify 
    the path of the source and destination folder

    Parameters
    ----------
    config_file_path:   Path where config file will be created. 
                        Normally it should locate in the same folder
    """

    try:
        config_file = open(config_file_path,'w')
        config_file.write("SOURCE=FULL_PATH_TO_YOUR_SOURCE_FILE\n")
        config_file.write("TARGET1=FULL_PATH_TO_YOUR_DESTINATION_FILE\n")
        config_file.write("TARGET2=FULL_PATH_TO_YOUR_DESTINATION_FILE\n")
        config_file.close()
        print('A config file is created')
        print('Please modify the path and re-run the code')
    except Exception as error:
        print("An error has occured, please press any key to close the application")
        print(error)
        input()#pause the application, waiting for user input
        sys.exit(0)

def create_log_file(log_file_path):
    """ Create an empty log file if the log file has not existed

    Parameters
    ----------
    log_file_path:  path where log file will be created
                    Normally it should locate in the in the same folder
    """

    config_file = open(log_file_path,'a')
    config_file.write("Sync File\n")
    config_file.close()
    print("log file created")

def print_config(config_list):
    """ Print the content of the config_list

    Parameters
    ----------
    config_list: the list we want to print
    """
    for config in config_list:
        print(config)

def hash_directory(path):
    """ Hash a directory and its child folders

    Parameter:
    path:   path to directory
    return: SHA256 of that directory
    """

    digest = hashlib.sha256()
    for root, dirs, files in os.walk(path):
        for names in files:
            file_path = os.path.join(root, names)

            # Hash the path and add to the digest to account for empty files/directories
            digest.update(hashlib.sha1(file_path[len(path):].encode()).digest())

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f_obj:
                    while True:
                        buf = f_obj.read(1024 * 1024)
                        if not buf:
                            break
                        digest.update(buf)

    return digest.hexdigest()

def logging(hash_tag, log_file_path):
    """ Logging info into log file

    The log file contains date, time when the folder is backed up 
    and the hash value of the source folder at that moment.

    The method also checks if the log file exists. If it does not exist,
    the method will create a new one before logging info
    
    Parameters
    ----------
    hash_tag:       the hash value of the source folder
    log_file_path:  the path to log file
    """

    print("Logging data...")
    if os.path.exists(log_file_path) == False:
        print("Log file does not exist. Create a new log file")
        create_log_file(log_file_path)

    today = datetime.now()
    str_date_time = today.strftime("%Y") + today.strftime("%m") + today.strftime("%d") + '_'+ today.strftime("%H%M%S")
    try:
        log_file = open(log_file_path,'a')
        log_file.write("------------------------------------------------------\n")
        log_file.write("DATE: " + str_date_time + '\n')
        log_file.write("HASH: " + hash_tag + "\n")
        log_file.close()
    except Exception as error:
        # Does not expect any error here but we catch and print any error just in case
        print("An error has occured, please press any key to close the application")
        print(error)
        input() #pause the application, waiting for user input
        sys.exit(0)

    print('Logging is completed')
        

def get_destination_path(config_list, dest_path):
    """ Get the folder path, where the backup data will locate, out of the config list
    
    The destination folders are supposed to start from the second line of the 
    configuration file

    The method will verify if the destination path is correct. If not, it will
    throw error. The format shall be TARGETx=PATH_TO_DESTINATION_FOLDER where
    x = 1,2,3,4. It also implies that, there may be multiple destination folders

    Parameters
    ----------
    config_list:    the list storing the path
    dest_path:      te list storing the destination paths (output)
    """

    for index in range(1, len(config_list)):
        # check if the folder format is TARGETx= with x = 1,2,3...
        if(config_list[index][:8] == 'TARGET' + str(index) + '='):
            dest_path.append(config_list[index][8:])
        
        #skip any empty line
        elif config_list[index][:8] == "":
            continue
        else:
            print("destination folder: " + (config_list[index][:8]))
            raise ValueError('[Error] Wrong destination folder format')


def get_source_path(config_list):
    """ Get the folder path, which we want to backup out of the config list
    
    The source folder is supposed to be at the first line of the 
    configuration file

    The method will verify if the source path is correct. If not, it will
    throw error. The format shall be SOURCE=PATH_TO_SOURCE_FOLDER

    Parameters
    ----------
    config_list:    the list storing the path
    return :        path of source folder
    """

    if(config_list[0][:7] == 'SOURCE='):
        return config_list[0][7:]
    else:
        raise ValueError('[Error] Wrong source folder format')

# Main Function
def main():
    
    print("SyncFile Application")

    try:
        read_config_file(config_file, config_list, config_file)
    except ValueError as error:
        print("An error has occured, please press any key to close the application")
        print(error)
        input()#pause the application, waiting for user input
        sys.exit(0)
    
    print_config(config_list)
    
    try:
        get_destination_path(config_list, destination_path)
    except ValueError as error:
        print("An error has occured, please press any key to close the application")
        print(error)
        input()#pause the application, waiting for user input
        sys.exit(0)

    try:
        source_path = get_source_path(config_list)
    except ValueError as error:
        print("An error has occured, please press any key to close the application")
        print(error)
        input()#pause the application, waiting for user input
        sys.exit(0)

    tag = hash_directory(source_path)
    logging(tag, log_file)
    print("Backing up data...")
    for path in destination_path:
        print("BACKUP DESTINATION: " + path + "\n")
        sync(source_path, path, 'sync', purge = True, content = True, create = True)

# Run the main function
if __name__ == "__main__":
    main()
    print("Application completed! Please press any key to close the application")
    input() #pause the application, waiting for user input