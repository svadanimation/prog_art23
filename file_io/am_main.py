import json
import os

filepath = os.path.join(os.path.realpath('C:/Visual Studio/text.json'))
filepath2 = os.path.join(os.path.realpath('C:\\Visual Studio\\text.txt'))

def txt_write(filepath, text):
    with open(filepath,"w") as f:
        success = f.write(text)
    return success


with open("text.json","w") as f:
    f.write("Google it")
dictionary = {1:"one",
2:"two",3:"three", 4:"four",5:"five", 6:{1:"2nd one",2:"2nd Two"}}

with open('filepath', 'w') as f:
    json.dump(dictionary, f)

with open('filepath', 'r') as f:
    content = f.read()

__name__ = '__main__'
if __name__ == '__main__':
    am_main.py()