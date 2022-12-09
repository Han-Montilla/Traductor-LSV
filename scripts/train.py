from subprocess import run
from definitions import *

def main():
  run(['tensorboard', f'--logdir={MODEL_DIR}'])
  run([
    'python', # executing python script
    TRAIN_SCRIPT_PATH,
    f'--model_dir={MODEL_DIR}',
    f'--pipeline_config_path={CONFIG_PATH}',
    f'--num_train_steps={TRAINING_STEPS}' # TODO: setup steps in definition.py
  ])
main()