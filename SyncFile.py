import os

config_file = 'config_empty.txt'
config_list = []

def read_config_file(file_name, config_list):
    try:
        with open(file_name) as config_file:
            for line in config_file:
                config_list.append(line.rstrip())
    except FileNotFoundError as error:
        print(error)
    else:
        if len(config_list) == 0:
            raise ValueError('[Error] Config file is empty')

def print_config(config_list):
    for config in config_list:
        print(config)


#Main Function
def main():
    print("SyncFile")
    try: 
        read_config_file(config_file, config_list)
    except ValueError as error:
        print(error)
    else:
        print_config(config_list)

#Run the main function  
if __name__== "__main__":
    main()

