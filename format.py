import os
import sys
import subprocess
from pathlib import Path
from re import match
from shutil import which

# ANSI esacpe sequence set in order to print colored text
# [ref](https://stackoverflow.com/a/287944)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Get file path
dir = Path(os.path.dirname(__file__))

# astyle formatter configuration paths
astyle_config = Path('astylerc')
astyle_path = Path.joinpath(dir, Path('.vscode'))

# Find a file (`filename`) from given the search path (`search_path`)
def find_files(filename, search_path):
    result = []
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result

# Check `astyle` command is exist
if which('astyle') is None:
    sys.exit(bcolors.FAIL + '\'astyle\' command does not exist.' + bcolors.ENDC)

# Check the astyle option file (configraution file) is exist
if not find_files(str(astyle_config), str(astyle_path)):
    sys.exit(bcolors.FAIL + 'Cannot find %s file in \'%s\'.' % (astyle_config, astyle_path) + bcolors.ENDC)

# Apply to every each *.c and *.h files given the format option except the files that in the Git related folders (submodules, etc.)
dir_list = list(filter(lambda name: not name.startswith('.'), os.listdir(dir)))
for item in dir_list:
    dir_absolute_path = Path.joinpath(dir, Path(item))
    if os.path.isdir(dir_absolute_path) and not find_files(str('.git'), str(dir_absolute_path)):
        subprocess.run(['astyle',
                        '--options=%s' % str(Path.joinpath(astyle_path, astyle_config)),
                        '--recursive',
                        str(Path.joinpath(dir_absolute_path, Path('*.c,*.h')))])

# Apply to every each *.c and *.h files from the root of the project folder
print('------------------------------------------------------------')
print('Finding *.c and *.h files from the root of \'%s\'' % (dir))
print('------------------------------------------------------------')
files_in_root_dir = list(filter(lambda v: match('.*\.[ch]', v), dir_list))

if not files_in_root_dir:
    print("Nothing to change.")
else:
    for item in files_in_root_dir:
        subprocess.run(['astyle',
                        '--options=%s' % str(Path.joinpath(astyle_path, astyle_config)),
                        str(Path.joinpath(dir, Path(item)))])

# Print a finish message
print(bcolors.OKGREEN + "\nFormat completed." + bcolors.ENDC)
