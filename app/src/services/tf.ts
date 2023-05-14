import * as tf from '@tensorflow/tfjs';
import { HAND_LANDMARK_COUNT, POINT_COMPONENT_COUNT, SIGNS } from '../const';

const useTf = () => ({ loadModel, predict });

let _model: tf.LayersModel;

const loadModel = async () => {
  const modelPath = `model/model.json`;
  _model = await tf.loadLayersModel(modelPath);
}

function normalizePoints(points: number[][]): tf.Tensor {

  const pointsTensor = tf.tensor2d(points);

  // Compute the centroid
  const centroid = pointsTensor.mean(0);

  // Translate the points to the centroid
  const translatedLandmarks = pointsTensor.sub(centroid);

  // Compute the scaling factor
  const norms = translatedLandmarks.norm('euclidean', 1);
  const scaleFactor = norms.max();

  // If scale factor is zero, return translated landmarks
  if (scaleFactor.arraySync() === 0) {
    return translatedLandmarks;
  }

  // Normalize the points
  const normalizedLandmarks = translatedLandmarks.div(scaleFactor);

  return normalizedLandmarks;
}

const predict = (points: number[][]) => {
  const tensor = normalizePoints(points).reshape([1, -1, 3]);
  if (tensor.shape[0] === 1, tensor.shape[1] === HAND_LANDMARK_COUNT, tensor.shape[2] === POINT_COMPONENT_COUNT) {
    const res = _model.predict(tensor) as tf.Tensor;
    return res.dataSync();
  }
  return new Float32Array(SIGNS.length).fill(0);
} 

export default useTf;