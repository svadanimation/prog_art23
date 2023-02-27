import json
import os

directory = "Z:\"
filepath = os.path.join(os.path.realpath(C:\'text.json'))
filepath2 = os.path.join(os.path.realpath(C:\'text.txt'))

with open("text.json","w") as f:
    f.write("Google it"\n)
dictionary = {1:"one",
2:"two",3:"three", 4:"four",5:"five", 6:{1:"2nd one",2:"2nd Two"}}

with open(filepath, 'w') as f:
    json.dump(dictionary, f)

with open("filepath", "r") as f:
content = f.read()

if name == 'main':
    print("Always executed")
else:
    print("Executed when imported")

AKM2_file_io.py
