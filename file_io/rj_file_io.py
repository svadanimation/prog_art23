'''
File Io Project

~Rileigh Juba
'''

import os
import json
from pprint import pprint

FILEPATH = 'Z:'
TEXT_FILE = 'text_file.txt'
JSON_FILE = 'json_file.json'

text_path = os.path.realpath(f'{FILEPATH}/{TEXT_FILE}')
json_path = os.path.realpath(f'{FILEPATH}/{JSON_FILE}')

TEXT = 'cn87984nb3qjmlku0'
DATA = {'robin': 'dgrayson', 'sfire': 'kori', 
        'cyborg': 'victor', 'bboy': 'garfield', 
        'raven': 'rachel', 'digits':{'a':'25', 'b':'32', 'c':'17'}}

def text_plcmnt(path, text):
    with open(path, 'w') as txt:
        txt.write(text)

def text_rdr(path):
    txt_lets = ''
    txt_digits = []
    with open(path, 'r') as txt:
        read_text = txt.read()
        for f in read_text:
            if f.isdigit():
                txt_digits.append(int(f))
            else:
                txt_lets += f
    return(txt_digits, txt_lets)    

def dict_plcmnt(path, data):
    with open(path, 'w') as dcj:
        json.dump(data, dcj)

def dict_rdr(path):
    dict_info = None
    with open(path, 'r') as dcj:
        dict_info = json.load(dcj)
    return(dict_info)

if __name__ == '__main__':
    text_plcmnt(text_path, TEXT)
    dict_plcmnt(json_path, DATA)
    pprint(text_rdr(text_path))
    pprint(dict_rdr(json_path))