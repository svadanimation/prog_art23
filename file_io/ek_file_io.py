"""
import os
from pprint import pprint
import json 
file_path = os.path.realpath('Z:/texttest.txt')

with open (file_path,"a") as f:
    f.write('addition :)')

with open (file_path, "r") as f:
    text_file = f.readlines()

pprint(text_file)

Writer:
Eleanor Kim
"""
import os
import json
from pprint import pprint

#constants
filepath = os.path.realpath('Z:/')
text_file = 'text_file.txt'
json_file = 'json_file.json'

file_path_t = os.path.realpath(filepath,text_file)
file_path_j = os.path.realpath(filepath,json_file)

ex_string = [3, 4, 'a', 'M', 'ty']
ex_dict = {'name','age'}

