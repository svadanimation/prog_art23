# Imports
import os
import json
from pprint import pprint

# Dir setup
FILEPATH = 'Z:\\'
TEXT_FILE = 'text_file.txt'
JSON_FILE = 'json_file.json'

# Assigning dir to var
txt_path = os.path.abspath(FILEPATH + TEXT_FILE)
json_path = os.path.abspath(FILEPATH + JSON_FILE)

# Setting text/data constants
TEXT = "he110 w0r1d"
DATA = {
        'value_one' : 1,
        'value_two' : 2,
        'value_three' : 3,
        'value_four' : 4,
        'value_five' : 5, 
        'value_six' : {'inside_value_one' : 'one', 'inside_value_two' : 'two'}
        }

# Write input text to txt file
def write_text(path, text):
    with open(path, 'w+') as f:
        f.write(text)

# Read txt file
def read_text(path):
    with open(txt_path, 'r') as f:
        # print(f'The file \'{path}\' says: \n{f.read()}')
        text = f.read()
        return text

# Write input data to json file
def write_data(path, data):
    with open(json_path, 'w') as f:
        json.dump(data, f)

# Read json file
def read_data(path):
    with open(json_path, 'r') as f:
        pprint(json.load(f))

if __name__ == '__main__':
    write_txt = write_text(txt_path, TEXT)
    read_txt = read_text(txt_path)
    write_dat = write_data(json_path, DATA)
    read_dat = read_data(json_path)
