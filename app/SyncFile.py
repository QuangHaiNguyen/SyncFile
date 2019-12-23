import os
import logging
import sys
import hashlib
from datetime import datetime
from dirsync import sync

# init logging level
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def read_config_file(file_name, config_list):
    """ Read the config file and parse the content of config file into a list
    file_name: path to the config file
    config_list: list to store the content of config file
    """
    try:
        # Open the config file and read line by line
        with open(file_name) as config_file:
            for line in config_file:
                config_list.append(line.rstrip())
    except FileNotFoundError as error:
        print(error)
        create_config_file()
        sys.exit(0)
    else:
        # Raise error if config file is empty
        if len(config_list) == 0:
            raise ValueError('[Error] Config file is empty')

def create_config_file():
    """ Create a config file with a template
    and asking user to modify the source and destination path
    """
    config_file = open("app/config.txt",'w')
    config_file.write("SOURCE=FULL_PATH_TO_YOUR_SOURCE_FILE\n")
    config_file.write("TARGET1=FULL_PATH_TO_YOUR_DESTINATION_FILE\n")
    config_file.write("TARGET2=FULL_PATH_TO_YOUR_DESTINATION_FILE\n")
    config_file.close()
    print('A config file is created')
    print('Please modify the path and re run the code')

def create_log_file():
    """ Create an empty log file
    """
    config_file = open("app/log.txt",'w')
    config_file.write("------------------------Sync File------------------------\n")
    config_file.close()
    print("log file created")

def print_config(config_list):
    """ Print the content of the config_list
    config_list: the list we want to print
    """
    for config in config_list:
        print(config)

def hash_directory(path):
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

def logging_backup_time_stamp(hash_tag):
    today = datetime.now()
    str_date_time = today.strftime("%Y") + today.strftime("%m") + today.strftime("%d") + '_'+ today.strftime("%H%M%S")
    try:
        with open('app/log.txt', 'a') as file:
            file.write(str_date_time + '_' + hash_tag + '\n')
    except FileNotFoundError as error:
        print(error)
        create_log_file()
        with open('app/log.txt', 'a') as file:
            file.write(str_date_time + '_' + hash_tag + '\n')
    print('logging done')
        

def get_destination_path(config_list, dest_path):
    """ Get the path of the folder, where we want to store the data to
    multiple destinations are accepted
    """
    for index in range(1, len(config_list)):
        # check if the folder format is TARGETx= with x = 1,2,3...
        if(config_list[index][:8] == 'TARGET' + str(index) + '='):
            dest_path.append(config_list[index][8:])
        else:
            raise ValueError('[Error] Wrong destination folder format')


def get_source_path(config_list, ):
    """ Get the path of the folder, which we want to be backed up
    we accept only one source path
    """
    if(config_list[0][:7] == 'SOURCE='):
        return config_list[0][7:]
    else:
        raise ValueError('[Error] Wrong source folder format')

# Main Function
def main():
    config_file = 'app/config.txt'
    config_list = []
    source_path = None
    destination_path = []
    print("SyncFile Application")

    try:
        read_config_file(config_file, config_list)
    except ValueError as error:
        print(error)
        sys.exit(0)
        

    print_config(config_list)
    
    try:
        get_destination_path(config_list, destination_path)
    except ValueError as error:
        print(error)
        sys.exit(0)
    else:
        for path in destination_path:
            logging.debug(path)

    try:
        source_path = get_source_path(config_list)
    except ValueError as error:
        print(error)
        sys.exit(0)
    else:
        logging.debug(source_path)

    tag = hash_directory(source_path)
    logging_backup_time_stamp(tag)
    for path in destination_path:
        sync(source_path, path, 'diff', purge = True, content = True, create = True)
        sync(source_path, path, 'sync', purge = True, content = True, create = True)

# Run the main function
if __name__ == "__main__":
    main()
