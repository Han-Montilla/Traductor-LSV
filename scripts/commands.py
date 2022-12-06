from definitions import *

print('\nExecute the following commands:\n')

# generate train tf record
print(' '.join([
    'python', # executing python script
    GEN_TF_RECORD_SCRIPT_PATH, # script path
    '-x', TRAIN_IMAGES_DIR, # input images dir + their labelimg xml generate files
    '-l', LABELMAP_PATH, # labelmap path
    '-o', TRAIN_TF_RECORD_PATH # tfrecord output file path
  ]).replace('\\', '/')
)

# generate test tf record
print('\n')
print(' '.join([
    'python', # executing python script
    GEN_TF_RECORD_SCRIPT_PATH, # script path
    '-x', TEST_IMAGES_DIR, # input images dir + their labelimg xml generate files
    '-l', LABELMAP_PATH, # labelmap path
    '-o', TEST_TF_RECORD_PATH # tfrecord output file path
  ]).replace('\\', '/')
)

# train
print('\n')
print(' '.join([
    'python', # executing python script
    TRAIN_SCRIPT_PATH,
    f'--model_dir={CURRENT_MODEL_DIR}',
    f'--pipeline_config_path={CONFIG_PATH}',
    f'--num_train_steps={20000}' # TODO: setup steps in definition.py
  ]).replace('\\', '/')
)

# monitor training
print('\n')
print(' '.join([
    'tensorboard', # executing tersorboard
    f'--logdir={CURRENT_MODEL_DIR}'
  ]).replace('\\', '/')
)
