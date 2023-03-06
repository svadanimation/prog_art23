import sys
from importlib import reload
from pprint import pprint

mod_path = 'Z:/Classes W2023/Programming/VS Code/prog_art23/file_io'

if mod_path not in sys.path:
    sys.path.append(mod_path)

import rj_file_io as rj
reload(rj)

rj.text_plcmnt('Z:/ioimport.txt', 'Impo2rt pract457ice.')
pprint(rj.text_rdr('Z:/ioimport.txt'))