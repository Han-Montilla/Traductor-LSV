from os.path import join, realpath, dirname

# Settings 🔧
PRETRAINED_MODEL_NAME = 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8'
PRETRAINED_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8.tar.gz'
PRETRAINED_MODEL_ZIP_NAME = f'{PRETRAINED_MODEL_NAME}.tar.gz'
API_MODELS_URL = 'https://github.com/tensorflow/models'
PROTOC_VERSION = '3.15.6'
PROTOC_URL = f'https://github.com/protocolbuffers/protobuf/releases/download/v{PROTOC_VERSION}/protoc-{PROTOC_VERSION}-win64.zip'
PROTOC_ZIP_NAME = f'protoc-{PROTOC_VERSION}-win64.zip'
MODEL_NAME = 'ssd-mobnet-v1' # current model name being used within 'workspace/models' directory
LATEST_CHECKPOINT = 3
BATCH_SIZE = 8
TRAINING_STEPS = 10_000

# Paths 📂
ROOT_DIR = realpath(join(dirname(__file__), '..'))
API_MODELS_DIR = join(ROOT_DIR, 'models')
API_RESEARCH_DIR = join(API_MODELS_DIR, 'research')
API_OBJECT_DETECTION_DIR = join(API_RESEARCH_DIR, 'object_detection')
API_SETUP_SCRIPT_PATH = join(API_OBJECT_DETECTION_DIR, 'packages', 'tf2', 'setup.py')
API_VERIFICATION_SCRIPT_PATH = join(API_OBJECT_DETECTION_DIR, 'builders', 'model_builder_tf2_test.py')
API_SLIM_DIR = join(API_RESEARCH_DIR, 'slim')
PROTOC_DIR = join(ROOT_DIR, 'protoc')
PROTOC_BIN_DIR = join(PROTOC_DIR, 'bin')
TRAIN_SCRIPT_PATH = join(API_MODELS_DIR, 'research', 'object_detection', 'model_main_tf2.py')
WORKSPACE_DIR = join(ROOT_DIR, 'workspace')
MODELS_DIR = join(WORKSPACE_DIR, 'models')
PRETRAINED_MODELS_DIR = join(WORKSPACE_DIR, 'pre-trained-models')
SCRIPTS_DIR = join(ROOT_DIR, 'scripts')
VENDOR_SCRIPTS_DIR = join(SCRIPTS_DIR, 'vendor')
TF_RECORD_SCRIPT_PATH = join(VENDOR_SCRIPTS_DIR, 'generate_tfrecord.py')
LABELMAP_SCRIPT_PATH = join(VENDOR_SCRIPTS_DIR, 'generate_labelmap.py')
IMAGES_DIR = join(WORKSPACE_DIR, 'images')
TEST_IMAGES_DIR = join(IMAGES_DIR, 'test')
TRAIN_IMAGES_DIR = join(IMAGES_DIR, 'train')
VALIDATION_IMAGES_DIR = join(IMAGES_DIR, 'validation')
COLLECTED_IMAGES_DIR = join(IMAGES_DIR, 'collected')
CAPTURED_IMAGES_DIR = join(IMAGES_DIR, 'captured')
ANNOTATIONS_DIR = join(WORKSPACE_DIR, 'annotations')
LABELMAP_PATH = join(ANNOTATIONS_DIR, 'label_map.pbtxt')
TRAIN_TF_RECORD_PATH = join(ANNOTATIONS_DIR, 'train.record')
TEST_TF_RECORD_PATH = join(ANNOTATIONS_DIR, 'test.record')
MODEL_DIR = join(MODELS_DIR, MODEL_NAME)
PRETRAINED_MODEL_DIR = join(PRETRAINED_MODELS_DIR, PRETRAINED_MODEL_NAME)
PRETRAINED_CONFIG_PATH = join(PRETRAINED_MODEL_DIR, 'pipeline.config')
PRETRAINED_CHECKPOINT_PATH = join(PRETRAINED_MODEL_DIR, 'checkpoint', 'ckpt-0')
CONFIG_PATH = join(MODEL_DIR, 'pipeline.config')
CURRENT_CP_PATH = join(MODEL_DIR, f'ckpt-{LATEST_CHECKPOINT}')

# Constants 🧮
SIGNS = [
  # letras
  'a', 'b', 'c',
  
  # palabras
  # 'hola',
  
  # frases
  
]