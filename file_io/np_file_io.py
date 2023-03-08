#Imports
import os
import json
import re
import pprint

#Constants
DIRECTORY = 'Z:'
TEXT_FILE = 'text_file.txt'
JSON_FILE = 'json_file.json'

#Paths
text_path = os.path.join(DIRECTORY, TEXT_FILE)
json_path = os.path.join(DIRECTORY, JSON_FILE)

#Variables
TEXT = 'abc123'
DATA = {
        'a': 1, 
        'b': 2, 
        'c': 3, 
        'd': 4, 
        'e': {'egg': 666, 'everyman': 999}
        }

#Text Functions
def rw_text(path, content = ''):
    text_info = None
    if content:
        with open(path, 'w') as t:
            t.write(content)
    else:
        with open(path, 'r') as t:
            for line in t:  
                match = re.match(r'([a-z]+)([0-9]+)', line)
            if match:
                text_info = match.groups()
    print(f'The file named {TEXT_FILE} says: {text_info}')
    return(str(text_info))

#Json Functions
def rw_json(path, content = ''):
    json_info = None
    if content:
         with open(path, 'w') as j:
            json.dump(content, j)
    else:
        with open(path, 'r') as j:
            json_info = json.load(j)
    return json_info

#Script Execution
if __name__ == '__main__':
    rw_text(text_path, content = TEXT)
    print(rw_text(text_path, content = ''))
    rw_json(json_path, content = DATA)
    pprint.pprint(rw_json(json_path, content = ''))