import os
import logging
import sys


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
    print("log file created")

def print_config(config_list):
    """ Print the content of the config_list
    config_list: the list we want to print
    """
    for config in config_list:
        print(config)


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
        return
    else:
        for path in destination_path:
            logging.debug(path)

    try:
        source_path = get_source_path(config_list)
    except ValueError as error:
        print(error)
        return
    else:
        logging.debug(source_path)


# Run the main function
if __name__ == "__main__":
    main()
