from sys import path
from os.path import join, realpath, dirname
from subprocess import run
path.append(realpath(join(dirname(__file__), '..'))) # setting root path in scripts

from definitions import *

def main():
  run(['python', API_VERIFICATION_SCRIPT_PATH])

main()