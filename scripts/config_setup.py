import tensorflow as tf
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format
from definitions import *
from os.path import exists

if not exists(CONFIG_PATH): raise f'Place `pipeline.config` file from pre-trained model in {CURRENT_MODEL_DIR}'

config = pipeline_pb2.TrainEvalPipelineConfig()

with tf.io.gfile.GFile(CONFIG_PATH, "r") as f:                                                                                                                                                                                                                     
  proto_str = f.read()                                                                                                                                                                                                                                          
  text_format.Merge(proto_str, config)
    
config.model.ssd.num_classes = len(SIGNS)
config.train_config.batch_size = 4
config.train_config.fine_tune_checkpoint = PRETRAINED_CP_PATH
config.train_config.fine_tune_checkpoint_type = "detection"
config.train_config.use_bfloat16 = False
config.train_input_reader.label_map_path= LABELMAP_PATH
config.train_input_reader.tf_record_input_reader.input_path[:] = [TRAIN_TF_RECORD_PATH]
config.eval_input_reader[0].label_map_path = LABELMAP_PATH
config.eval_input_reader[0].tf_record_input_reader.input_path[:] = [TEST_TF_RECORD_PATH]

config_text = text_format.MessageToString(config)
with tf.io.gfile.GFile(CONFIG_PATH, "wb") as f:
  f.write(config_text)