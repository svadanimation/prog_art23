#Imports
import os
import json
import re
import pprint as pprint

#Constants
directory = "Z:"
text_file = "text_file.text"
json_file = "json_file.json"

#Paths
text_path = os.path.join(directory, "//Nathanael Perez/Classes/W23/Programming for Artists/", text_file)
json_path = os.path.join(directory, "//Nathanael Perez/Classes/W23/Programming for Artists/", json_file)

#Variables
text = "abc123"
data = {"a": 1, "b": 2, "c": 3, "d": 4, "e": {"everyman": 999}}

#Text Functions
def rw_text(path):
    def write_text(path):
        with open(path, "w") as t:
            t.write(text)
        text_info = None
    def read_text(path):
        with open(path, "r") as t:
            for line in t:  
                match = re.match(r"([a-z]+)([0-9]+)", line)
            if match:
                items = match.groups()
            text_info = t.read()
        print(text_info)
        #return text_info

#Json Functions
def rw_json(path):
    def write_json(path):
        with open(path, "w") as j:
            json.dump(data, j)
        json_info = None
    def read_json(path):
        with open(path, "r") as j:
            json_info = json.load(j)
        print(json_info)
        #return json_info

#Script Execution
if __name__ == "__main__":
    rw_text(text_path)
    rw_json(json_path)