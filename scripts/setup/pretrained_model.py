from os import name as os_name
from sys import path
from os.path import join, realpath, dirname, exists
from subprocess import run
path.append(realpath(join(dirname(__file__), '..'))) # setting root path in scripts

from definitions import *

def main():
  if exists(PRETRAINED_MODEL_DIR):
    print('model already exists.')
  else:
    if os_name == 'posix':
      run(['wget', PRETRAINED_MODEL_URL])
      run(['mv', PRETRAINED_MODEL_ZIP_NAME, PRETRAINED_MODELS_DIR])
      run(['cd', PRETRAINED_MODELS_DIR])
      run(['tar', '-zxvf', PRETRAINED_MODEL_ZIP_NAME])
      run(['cd', ROOT_DIR])
      return
      
    if os_name == 'nt':
      run(['pip', 'install', 'wget'])
      from wget import download
      download(PRETRAINED_MODEL_URL)
      run(['move', PRETRAINED_MODEL_ZIP_NAME, PRETRAINED_MODELS_DIR])
      run(['cd', PRETRAINED_MODELS_DIR])
      run(['tar', '-zxvf', PRETRAINED_MODEL_ZIP_NAME])
      run(['cd', ROOT_DIR])
      return

main()
print(f'Model {PRETRAINED_MODEL_NAME} successfully created at {PRETRAINED_MODELS_DIR}')