import { computed, ref } from "vue";
import * as tf from '@tensorflow/tfjs';

const useTf = () => ({ loadModel, predict, prediction });

let _model: tf.LayersModel;
const SEQUENCE_LENGHT = 10;
const prediction = ref<string>('none');

const loadModel = async (name: string) => {
  const modelPath = `models/model.${name}.json`;
  _model = await tf.loadLayersModel(modelPath);
}

const SIGNS = ['none', 'a', 'b', 'c']
const predict = (sequence: readonly number[][]) => {
  // console.log(tf.tensor([sequence]).shape)
  const res = _model.predict(tf.tensor([sequence])) as tf.Tensor;
  const values = res.dataSync();
  prediction.value = SIGNS[values.indexOf(Math.max(...values))];
  
}

export default useTf;