'''
Module to grep and sort files.
'''

import glob
import os 
import time

def get_files(directory, file_types = ('*.ma', '*.mb')):
    directory = os.path.isdir(directory) 
    directory = os.path.abspath(directory)
    files = []
    for file_type in file_types:
        glob.glob(os.path.join(directory, "**", file_type), recursive = True)
        #for file_path in file_paths:
            #file_time = time.ctime(os.path.getmtime(file_path))
            #files.append((file_path, file_time))
    return files

# TODO  merge ella
# - filter the list down by substring
# - sort the list by date

if __name__ == '__main__':
    print(get_files(directory))