from sys import path
from os.path import join, realpath, dirname
path.append(realpath(join(dirname(__file__), '..'))) # setting root path in scripts

from definitions import LABELMAP_PATH, SIGNS

print(f'Generating label map with the following signs: {SIGNS}')

with open(LABELMAP_PATH, 'w') as f:
  id = 0
  for sign in SIGNS:
    id += 1
    f.write('item { \n')
    f.write(f'\tname: \'{sign}\'\n')
    f.write(f'\tid: {id}\n')
    f.write('}\n')