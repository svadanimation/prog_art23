'''Reloads all modules in the current package, except for this one.
'''

import sys
import os

from importlib import reload

BASE = 'Z:/vs_code_svad/prog_art23/render_submit'
SCRIPTS = 'scripts'
ENV = os.path.join(BASE, SCRIPTS)
PACKAGE = 'render_submit'
if __name__ == '__main__':
    if ENV not in sys.path:
        sys.path.append(ENV)
    current_package = PACKAGE
else:
    # Get the name of the current package
    current_package = __name__.rpartition('.')[0]

from render_submit import constants
from render_submit import file_grep
from render_submit import render_loop
from render_submit import render_utils
from render_submit import vray_path_translate
from render_submit import vray_mash
from render_submit import vray_submit
from render_submit.ui import single_submit_ui
from render_submit.ui import multi_submit_ui

# Iterate over the modules in sys.modules with the same package name
for module_name in list(sys.modules.keys()):
    if module_name.startswith(current_package + '.'):

        # Reload the module using the importlib.reload() function
        reload(sys.modules[module_name])
        print(f'Module {module_name} has been reloaded...')

print('All modules in package', current_package, 'have been reloaded.')



# vray_submit.vray_submit_jobs(make_movie=True)
submit_ui = single_submit_ui.SubmitUI()
