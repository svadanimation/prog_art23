import os
import pprint
file_prac = os.path.realpath('Z:/Classes W2023/ospractice.txt')

with open(file_prac, 'w') as prac:
    prac.write("How\'s it going?")

lines = []
with open(file_prac, 'r') as prac:
    lines.append(prac.readlines())

lines.append("/n Today is such a nice day.")
lines.append("/n Zip-a-dee-doo-da")

pprint(lines)