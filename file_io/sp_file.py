ps='bruh\n843\n2.45'
print(ps)

def str_to_text_file(filename):
    f = open(filename, "w")
    f.write(ps)
    f.close()

str_to_text_file("god.txt")

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def read_text(filepath):
    result = []
    with open(filepath, 'r') as f:
        contents = f.read()
        for string in contents.splitlines():
            if is_float(string):
                result.append(float(string))
            else:
                result.append(string)
    return result
print(read_text('god.txt'))
read_text('god.txt')

saul = {
    "birthday": "may 6",
    "sports": "soccer,basket",
    "fav color": "Dark blue",
    "food": "pizza",
    "skin": "brown",
    "countries": {
        "USA": "United States of America",
        "VZLA": "Venezuela"

    }
}

def dict_to_text_file(saul, filename):
    with open(filename, "w") as f:
        f.write(str(saul))

def read_dict(filename):
    with open(filename, "r") as f:
        return f.read()
    return None

dict_to_text_file(saul, 'yo.txt')
#print(read_dict('dict.txt'))