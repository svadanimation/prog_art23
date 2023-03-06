import sys
from pprint import pprint
from importlib import reload
import os


mod_path = (r'Z:\Documents\Winter 2023\programing for artists\vs code ek\git-and-github-fundamentals-EllaAKim\prog_art23')
mod_path = os.path.normpath(mod_path)
if mod_path not in sys.path:
    sys.path.append(mod_path)

import ek_file_io
reload(ek_file_io)

TEXT = 'test run.'
file_path_t = 'Z:/text_file.txt'
ek_file_io.open_text(file_path_t, TEXT)