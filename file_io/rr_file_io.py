import os
import json
from pprint import pprint

FILEPATH = 'Z:\\'
TEXT_FILE = 'text_file.txt'
JSON_FILE = 'json_file.json'

txt_path = os.path.relpath(FILEPATH + TEXT_FILE)
json_path = os.path.relpath(FILEPATH + JSON_FILE)

text = "he110 w0r1d"
data = {
        'value_one' : 1,
        'value_two' : 2,
        'value_three' : 3,
        'value_four' : 4,
        'value_five' : 5, 
        'value_six' : {'inside_value_one' : 'one', 'inside_value_two' : 'two'}
        }

def write_text(text_to_append):
    with open(txt_path, 'w+') as f:
        f.write(text_to_append)

    def read_text():
        with open(txt_path, 'r') as f:
            print(f'The file \'{TEXT_FILE}\' says: \n{f.read()}')

    read_text()

def write_data(data_to_append):
    with open(json_path, 'w') as f:
        json.dump(data, f)

    def read_data():
        with open(json_path, 'r') as f:
            pprint(f.read())
    
    read_data()

if __name__ == '__main__':
    write_text(text)
    write_data(data)

'''

    sep funcs, pass args 'what to append' and 'file' and return

'''