from definitions import *
from util import mkdir

# Generando estructura de archivos del proyecto
mkdir(WORKSPACE_DIR)
mkdir(ANNOTATIONS_DIR)
mkdir(IMAGES_DIR)
mkdir(TEST_IMAGES_DIR)
mkdir(TRAIN_IMAGES_DIR)
mkdir(COLLECTED_IMAGES_DIR)

import generate_labelmap