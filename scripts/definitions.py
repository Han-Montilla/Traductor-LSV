from os.path import join, realpath, dirname

# Paths 📂
ROOT_DIR = realpath(join(dirname(__file__), '..'))
TF_MODELS_DIR = join(ROOT_DIR, 'models')
TRAIN_SCRIPT_PATH = join(TF_MODELS_DIR, 'research', 'object_detection', 'model_main_tf2.py')
WORKSPACE_DIR = join(ROOT_DIR, 'workspace')
MODELS_DIR = join(WORKSPACE_DIR, 'models')
PRETRAINED_MODELS_DIR = join(WORKSPACE_DIR, 'pre-trained-models')
SCRIPTS_DIR = join(ROOT_DIR, 'scripts')
GEN_TF_RECORD_SCRIPT_PATH = join(SCRIPTS_DIR, 'generate_tfrecord.py')
GEN_LABELMAP_SCRIPT_PATH = join(SCRIPTS_DIR, 'generate_labelmap.py')
IMAGES_DIR = join(WORKSPACE_DIR, 'images')
TEST_IMAGES_DIR = join(IMAGES_DIR, 'test')
TRAIN_IMAGES_DIR = join(IMAGES_DIR, 'train')
COLLECTED_IMAGES_DIR = join(IMAGES_DIR, 'collected')
ANNOTATIONS_DIR = join(WORKSPACE_DIR, 'annotations')
LABELMAP_PATH = join(ANNOTATIONS_DIR, 'label_map.pbtxt')
TRAIN_TF_RECORD_PATH = join(ANNOTATIONS_DIR, 'train.record')
TEST_TF_RECORD_PATH = join(ANNOTATIONS_DIR, 'test.record')
CURRENT_MODEL_DIR = join(MODELS_DIR, 'my-ssd-mobnet') # nuestro modelo
CURRENT_PRETRAINED_MODEL_DIR = join(PRETRAINED_MODELS_DIR, 'ssd_mobilenet_v2_fpnlite_640x640_coco17_tpu-8') # modelo pre-entrenado que usamos
PRETRAINED_CP_PATH = join(CURRENT_PRETRAINED_MODEL_DIR, 'checkpoint', 'ckpt-0')
CONFIG_PATH = join(CURRENT_MODEL_DIR, 'pipeline.config')

print(PRETRAINED_CP_PATH)

# Settings & Constants 🧮
SIGNS = [
  # letras
  'a', 'b',
  
  # palabras
  # 'hola',
  
  # frases
  
]