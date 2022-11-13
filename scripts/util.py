import os

def mkdir(path: str, debug=False):
  if not os.path.exists(path):
    os.mkdir(path)
  else:
    if debug:
      print(f'{path} already exists!')