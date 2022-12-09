from os import name as os_name
from sys import path
from os.path import join, realpath, dirname
from subprocess import run
path.append(realpath(join(dirname(__file__), '..'))) # setting root path in scripts

from definitions import *

def update():
  import tensorflow as tf
  from object_detection.protos import pipeline_pb2
  from google.protobuf import text_format
  config = pipeline_pb2.TrainEvalPipelineConfig()

  with tf.io.gfile.GFile(CONFIG_PATH, "r") as f:                                                                                                                                                                                                                     
    proto_str = f.read()                                                                                                                                                                                                                                          
    text_format.Merge(proto_str, config)
      
  config.model.ssd.num_classes = len(SIGNS)
  config.train_config.batch_size = BATCH_SIZE
  config.train_config.fine_tune_checkpoint = PRETRAINED_CHECKPOINT_PATH
  config.train_config.fine_tune_checkpoint_type = "detection"
  config.train_config.use_bfloat16 = False
  config.train_input_reader.label_map_path= LABELMAP_PATH
  config.train_input_reader.tf_record_input_reader.input_path[:] = [TRAIN_TF_RECORD_PATH]
  config.eval_input_reader[0].label_map_path = LABELMAP_PATH
  config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [TEST_TF_RECORD_PATH]

  config_text = text_format.MessageToString(config)
  with tf.io.gfile.GFile(CONFIG_PATH, "wb") as f:
    f.write(config_text)

def main():
  if os_name == 'posix':
    run(['cp', PRETRAINED_CONFIG_PATH, MODEL_DIR])
    return
    
  if os_name == 'nt':
    run(['copy', PRETRAINED_CONFIG_PATH, MODEL_DIR])
    return

main()
update()