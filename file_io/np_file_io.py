#Imports
import os
import json
import re
import pprint as pprint

#Constants
directory = 'Z:'
text_file = 'text_file.txt'
json_file = 'json_file.json'

#Paths
text_path = os.path.join(directory + text_file)
json_path = os.path.join(directory + json_file)

#Variables
text = 'abc123'
data = {
        'a': 1, 
        'b': 2, 
        'c': 3, 
        'd': 4, 
        'e': {'egg': 666, 'everyman': 999}
        }

#Text Functions
def rw_text(path, w = True):
    text_info = None
    if w:
        with open(path, 'w') as t:
            t.write(text)
    else:
        with open(path, 'r') as t:
            for line in t:  
                match = re.match(r'([a-z]+)([0-9]+)', line)
            if match:
                items = match.groups()
            text_info = t.read()
            return text_info

#Json Functions
def rw_json(path, w = True):
    json_info = None
    if w:
         with open(path, 'w') as j:
            json.dump(data, j)
    else:
        with open(path, 'r') as j:
            json_info = json.load(j)
            return json_info

#Script Execution
if __name__ == '__main__':
    rw_text(text_path, True)
    print(rw_text(text_path, False))
    rw_json(json_path, True)
    print(rw_json(json_path, False))