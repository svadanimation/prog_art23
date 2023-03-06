
import sys
from pprint import pprint
from importlib import reload

# pprint (sys.path)

# 
mod_path = 'Z:/vs_code_svad/prog_art23/file_io'
if not mod_path in sys.path:
    sys.path.append(mod_path)

import np_file_io
reload(np_file_io)


TEXT = 'Hello World'
text_path = 'Z:/text.txt'
np_file_io.rw_text(text_path, content = TEXT)
