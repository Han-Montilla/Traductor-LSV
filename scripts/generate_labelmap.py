from definitions import LABEL_MAP_PATH, SIGNS

with open(LABEL_MAP_PATH, 'w') as f:
  id = 0
  for sign in SIGNS:
    id += 1
    f.write('item { \n')
    f.write(f'\tname: \'{sign}\'\n')
    f.write(f'\tid: {id}\n')
    f.write('}\n')