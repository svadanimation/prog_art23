import os
import json
from pprint import pprint

FILEPATH = 'Z:/'
TEXT_FILE = 'text_file_SPLODEY.txt'
JSON_FILE = 'json_file.json'

text_file_path = os.path.join(FILEPATH, TEXT_FILE)
json_file_path = os.path.join(FILEPATH, JSON_FILE)

TEXT = 'chat3gpt4'
DATA = {
    'walk':'paris',
    'run':'miami',
    'swim':'sydney', 
    'fly':'tokyo',
    'evaporate':'chattanooga', 'who':{
        'a':'jeremy',
        'b':'riri'
    }
}

def write_txt(path, text):
    with open(path, 'w') as f:
        f.write(text)
def read_txt(path):
    txt = ''
    digits = []
    with open (path, 'r') as f:
        text = f.read()
        for char in text:
            if char.isdigit():
                digits.append(int(char))
            else:
                txt += char
    return(txt, digits)

def write_dict(path, data):
    with open(path, 'w') as g:
        json.dump(data, g)
def read_dict(path):
    dict_data = None
    with open(path, 'r') as g:
        dict_data = json.load(g)
    return(dict_data)

if __name__ == '__main__':
    write_txt(text_file_path, TEXT)
    chars, nums = read_txt(text_file_path)
    print(f'My nums are {nums}, and my chars are {str(chars)}')
    write_dict(json_file_path, DATA)
    pprint(read_dict(json_file_path))