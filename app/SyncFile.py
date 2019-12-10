import os
import logging
import sys


# init logging level
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def read_config_file(file_name, config_list):
    try:
        # Open the config file and read line by line
        with open(file_name) as config_file:
            for line in config_file:
                config_list.append(line.rstrip())
    except FileNotFoundError as error:
        print(error)
    else:
        # Raise error if config file is empty
        if len(config_list) == 0:
            raise ValueError('[Error] Config file is empty')


def print_config(config_list):
    for config in config_list:
        print(config)


def get_destination_path(config_list, dest_path):
    for index in range(1, len(config_list)):
        # check if the folder format is TARGETx= with x = 1,2,3...
        if(config_list[index][:8] == 'TARGET' + str(index) + '='):
            dest_path.append(config_list[index][8:])
        else:
            raise ValueError('[Error] Wrong destination folder format')


def get_source_path(config_list, ):
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
    print("SyncFile")

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
