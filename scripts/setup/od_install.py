from os import name as os_name, environ, pathsep
from sys import path
from os.path import join, realpath, dirname,exists
from subprocess import run
path.append(realpath(join(dirname(__file__), '..'))) # setting root path in scripts

from definitions import *

def main():
  if os_name == 'posix':
    run(['apt-get', 'install', 'protobuf-compiler'])
    run(['protoc', f'{API_OBJECT_DETECTION_DIR}/protos/*.proto', f'--python_out={API_RESEARCH_DIR}'])
    run(['cp', API_SETUP_SCRIPT_PATH, API_RESEARCH_DIR])
    run(['python', '-m', 'pip', 'install', API_RESEARCH_DIR])
    return
    
  if os_name == 'nt':
    run(['pip', 'install', 'wget'])
    from wget import download
    download(PROTOC_URL)
    run(['move', PROTOC_ZIP_NAME, PROTOC_DIR])
    run(['cd', PROTOC_DIR])
    run(['tar', '-xf', PROTOC_ZIP_NAME])
    environ['PATH'] += pathsep + PROTOC_BIN_DIR
    run(['cd', API_OBJECT_DETECTION_DIR])
    run(['protoc', 'protos/*.proto', f'--python_out={API_RESEARCH_DIR}'])
    run(['copy', API_SETUP_SCRIPT_PATH, 'setup.py'])
    run(['python', 'setup.py', 'build'])
    run(['python', 'setup.py', 'install'])
    run(['cd', ROOT_DIR])
    return

if not exists(PROTOC_BIN_DIR):
  main()
else:
  print('didn\'t run')