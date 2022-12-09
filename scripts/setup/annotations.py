from os import name as os_name, environ, pathsep
from sys import path
from os.path import join, realpath, dirname,exists
from subprocess import run
path.append(realpath(join(dirname(__file__), '..'))) # setting root path in scripts

from definitions import *

def main():
  run(['python', LABELMAP_SCRIPT_PATH])
  run(['python', TF_RECORD_SCRIPT_PATH, '-x', TEST_IMAGES_DIR, '-l', LABELMAP_PATH, '-o', TEST_TF_RECORD_PATH])
  run(['python', TF_RECORD_SCRIPT_PATH, '-x', TRAIN_IMAGES_DIR, '-l', LABELMAP_PATH, '-o', TRAIN_TF_RECORD_PATH])

main()