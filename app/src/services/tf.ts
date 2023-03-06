import * as tf from '@tensorflow/tfjs';

const useTf = () => ({ loadModel, predict });

let _model: tf.LayersModel;

const loadModel = async () => {
  const modelPath = `model/model.json`;
  _model = await tf.loadLayersModel(modelPath);
}

const predict = (sequence: readonly number[][]) => {
  const res = _model.predict(tf.tensor([sequence])) as tf.Tensor;
  return res.dataSync();
} 

export default useTf;