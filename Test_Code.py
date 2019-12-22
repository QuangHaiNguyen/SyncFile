from dirsync import sync
from zipfile import ZipFile 
import os 
import hashlib
from datetime import datetime
#Dealing with zip file

def get_all_file_paths(directory): 
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory):
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths       


#hash part
def get_digest(file_path):
    h = hashlib.sha256()

    with open('my_python_files.zip', 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()

#hash a folder
def hash_directory(path):
    digest = hashlib.sha256()

    for root, dirs, files in os.walk(path):
        for names in files:
            file_path = os.path.join(root, names)

            # Hash the path and add to the digest to account for empty files/directories
            digest.update(hashlib.sha1(file_path[len(path):].encode()).digest())

            # Per @pt12lol - if the goal is uniqueness over repeatability, this is an alternative method using 'hash'
            # digest.update(str(hash(file_path[len(path):])).encode())

            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f_obj:
                    while True:
                        buf = f_obj.read(1024 * 1024)
                        if not buf:
                            break
                        digest.update(buf)

    return digest.hexdigest()


print('All files zipped successfully!') 

#print(get_digest('my_python_files.zip'))
print(hash_directory('Test Folder/Origin'))
today = datetime.now()

# path to folder which needs to be zipped 
directory = 'Test Folder/Origin'

# calling function to get all file paths in the directory 
file_paths = get_all_file_paths(directory) 

# printing the list of all files to be zipped 
print('Following files will be zipped:') 
for file_name in file_paths: 
    print(file_name) 

# writing files to a zipfile 
#zip_name = today.strftime("%Y") + today.strftime("%m") + today.strftime("%d") + '_'+ today.strftime("%H%M%S") + '_' + hash_directory('Test Folder/Origin') + '.zip'
#print(zip_name)
#with ZipFile(zip_name,'w') as zip: 
    # writing each file one by one 
    #for file in file_paths: 
        #zip.write(file) 

sync('Test Folder/Origin', 'Test Folder/Destination', 'diff', purge = True, content = True, create = True)
sync('Test Folder/Origin', 'Test Folder/Destination', 'sync', purge = True, content = True, create = True)