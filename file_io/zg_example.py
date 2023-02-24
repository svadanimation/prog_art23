"""
What is a file?
- Related information
- Different formats
- Used store content
- Various sizes
- Edit, Save, Delete, Move
- Location = path

What is a file to the comptoor?
- 0010101 byte
- 1111101
- 1 byte is a character
- mega=million bytes



The os sees a file as a handle

"""

import os
import json
from pprint import pprint
filepath = os.path.realpath('Z:/test.json')

my_dict = {'keykey':'monkey'}

with open(filepath, 'w') as f:
    json.dump(my_dict, f)


with open(filepath, 'r') as f:
  data = json.load(f)

print('from file')
pprint(data)

