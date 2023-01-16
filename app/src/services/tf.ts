import { computed, ref } from "vue";
import * as tf from '@tensorflow/tfjs';

const useTf = () => ({ loadModel, predict });

let _model: tf.LayersModel;
const SEQUENCE_LENGHT = 10;

const loadModel = async (name: string) => {
  const modelPath = `models/model.${name}.json`;
  _model = await tf.loadLayersModel(modelPath);

}

const predict = () => {
  // _model.predict()
}

export default useTf;