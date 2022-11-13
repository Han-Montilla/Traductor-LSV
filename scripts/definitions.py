import os

# Paths 📂
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
WORKSPACE_DIR = os.path.join(ROOT_DIR, 'workspace')
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
IMAGES_DIR = os.path.join(WORKSPACE_DIR, 'images')
TEST_IMAGES_DIR = os.path.join(IMAGES_DIR, 'test')
TRAIN_IMAGES_DIR = os.path.join(IMAGES_DIR, 'train')
COLLECTED_IMAGES_DIR = os.path.join(IMAGES_DIR, 'collected')
ANNOTATIONS_DIR = os.path.join(WORKSPACE_DIR, 'annotations')
LABEL_MAP_PATH = os.path.join(ANNOTATIONS_DIR, 'label_map.pbtxt')

# Settings & Constants 🧮
SIGNS = [
  # letras
  'a', 'b', 'c',
  
  # palabras
  'hola',
  
  # frases
  
]