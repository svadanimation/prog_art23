import os
from pprint import pprint
file_path = os.path.realpath('Z:/texttest.txt')

with open (file_path,"a") as f:
    f.write('addition :)')

with open (file_path, "r") as f:
    text_file = f.readlines()

pprint(text_file)