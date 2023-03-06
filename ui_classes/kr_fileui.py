import sys
from pprint import pprint
from importlib import reload

mod_path = 'Z:/Kaleb-Animation_23\winter_23/programming_4_artists/prog_art23/prog_art23/file_io'
if mod_path not in sys.path:
    sys.path.append(mod_path)

import kr_file_io
reload (kr_file_io)

TEXT = 'my world'
text_path = 'Z:/text_file.txt'

kr_file_io.write_txt(text_path, TEXT)

# pprint(sys.path)