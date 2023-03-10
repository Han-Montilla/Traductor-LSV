import * as tf from '@tensorflow/tfjs';

const useTf = () => ({ loadModel, predict });

let _model: tf.LayersModel;

const loadModel = async () => {
  const modelPath = `model/model.json`;
  _model = await tf.loadLayersModel(modelPath);
}

const predict = (sequence: readonly number[][]) => {
  const tensor = tf.tensor([sequence]);
  if (tensor.shape[0] === null, tensor.shape[1] === 10, tensor.shape[2] === 63) {
    const res = _model.predict(tensor) as tf.Tensor;
    return res.dataSync();
  }
  return new Float32Array(27).fill(0);
} 

export default useTf;