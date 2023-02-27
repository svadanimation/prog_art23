"""
file_io

Author:
Eleanor Kim
"""
import os
import json
from pprint import pprint
 
#constants
filepath = 'Z:'
text_file = 'text_file.txt'
json_file = 'json_file.json'

file_path_t = os.path.realpath(f'{filepath}/{text_file}')
file_path_j = os.path.realpath(f'{filepath}/{json_file}')

text = '34aMty570534gths'
data = {
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

#opens file to write text
def open_text():
    with open (file_path_t,"w") as txt:
            txt.write(text)
#reads string from file name
def read_string():
    letters = ""
    numbers = ""
    with open (file_path_t, "r") as f:
        read_text=f.readlines()
        for i in text:
                if(i.isdigit()):
                    letters+=i
                else:
                    numbers+=i
        pprint(letters, numbers)
#writes dictionary to disk as json
def open_json():
    with open(file_path_j, 'w') as outfile:
        json.dump(data, outfile)
#reads dict from json file
def read_json():
    with open(file_path_j, 'r') as openfile:
        read_json=json.load(openfile)
        pprint(read_json)

def ek_file_io():
     open_text()
     open_json()
     read_string()
     read_json()

if __name__ == "__main__":
     ek_file_io()
     pprint(text_file)
     pprint(json_file)