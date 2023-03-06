import sys
from pprint import pprint
from importlib import reload

mod_path = "Z:/Classes/W23/Programming for Artists/VS Code Workspace/prog_art23/file_io"
if mod_path not in sys.path:
    sys.path.append(mod_path)


# pprint(sys.path)

import np_file_io
reload(np_file_io)

TEXT = 'Greetings, earthlings!'
text_path = 'Z:/ui_test.txt'
np_file_io.rw_text(text_path, content = TEXT)