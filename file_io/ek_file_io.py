"""
file_io

Author:
Eleanor Kim
"""
import os
import json
from pprint import pprint

#constants
FILEPATH = 'Z:'
TEXT_FILE = 'text_file.txt'
JSON_FILE = 'json_file.json'


TEXT = '34aMty570534gths'
DATA = {
 'dog': {
    'name': "Fido",
    'age': 2
    },
'cat': {
    'name': "Garfield",
    'age': 3
    },
'fish': {
    'name': "Bubbles",
    'age': "3 months"
    }
}

file_path_t = os.path.realpath(f'{FILEPATH}/{TEXT_FILE}')
file_path_j = os.path.realpath(f'{FILEPATH}/{JSON_FILE}')

#opens file to write text
def open_text(file_path, text):
    with open (file_path,"w") as txt:
            txt.write(text)
#reads string from file name
def read_string(file_path):
    letters = ""
    numbers = ""
    with open (file_path, "r") as f:
        read_text=f.read()
        for i in read_text:
            if(i.isdigit()):
                numbers+=i
            else:
                letters+=i
    return(letters, numbers)
#writes dictionary to disk as json
def open_json(file_path, data):
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)
#reads dict from json file
def read_json(file_path):
    with open(file_path, 'r') as openfile:
        read_json=json.load(openfile)
        pprint(read_json)

def ek_file_io():
     pprint(TEXT_FILE)
     open_text(file_path_t, TEXT)
     pprint(read_string(file_path_t))
     pprint(JSON_FILE)
     open_json(file_path_j, DATA)
     read_json(file_path_j)

if __name__ == "__main__":
     ek_file_io()