import os
import json
from pprint import pprint

FILEPATH = 'Z:/'
TEXT_FILE = 'text_file.txt'
JSON_FILE = 'json_file.json'

text_file_path = os.path.join('Z:/', 'text_file.txt')
json_file_path = os.path.join('Z:/', 'json_file.json')

text = 'chat3gpt4'
data = {
    'walk':'paris',
    'run':'miami',
    'swim':'sydney', 
    'fly':'tokyo',
    'evaporate':'chattanooga', 'who':{
        'a':'jeremy',
        'b':'riri'
    }
}

def write_txt(path):
    with open(path, 'w') as f:
        f.write(text)
def read_txt(path):
    txt = ''
    digits = []
    with open (path, 'r') as f:
        for byte in text:
            if byte.isdigit():
                digits.append(int(byte))
            else:
                txt = txt + (byte)
    return(txt, digits)
def write_dict(path):
    with open(path, 'w') as g:
        json.dump(data, g)
def read_dict(path):
    dict_data = None
    with open(path, 'r') as g:
        dict_data = json.load(g)
    return(dict_data)

if __name__ == '__main__':
    write_txt(f'{text_file_path}')
    pprint(read_txt(f'{text_file_path}'))
    write_dict(f'{json_file_path}')
    pprint(read_dict(f'{json_file_path}'))