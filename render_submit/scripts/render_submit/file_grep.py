'''
Module to grep and sort files.
'''

import glob
import os 
import time

def get_files(directory, types = ('*.ma', '*.mb')):
    directory = os.path.abspath(directory)

    # TODO add isdir
    # TODO rename types file_types
    # TODO ** vs recursive, do we need both

    files = []
    for type in types:
        # files is the list of .ma and .mb files
        file_paths = glob.glob(os.path.join(directory, '**', type), recursive=True)
        for file_path in file_paths:
            file_time = time.ctime(os.path.getmtime(file_path))
            files.append((file_path, file_time))
    return files

# TODO  merge ella
# - filter the list down by substring
# - sort the list by date

if __name__ == '__main__':
    directory = 'Z:'
    print(get_files(directory))