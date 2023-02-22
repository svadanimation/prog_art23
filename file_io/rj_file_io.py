import os

filepath = 'Z:'
text_file = 'text_file.txt'
json_file = 'json_file.json'

text_path = os.path.realpath(f'{filepath}/{text_file}')
json_path = os.path.realpath(f'{filepath}/{json_file}')

'''
-----
'''

text = 'cn87984nb3qjmlku0'
data = {'robin': 'dgrayson', 'sfire': 'kori', 
        'cyborg': 'victor', 'bboy': 'garfield', 
        'raven': 'rachel', 'digits':{'a':'25', 'b':'32', 'c':'17'}}

def text_plcmnt():
    with open(text_path, 'w') as txt:
        txt.write(text)
        