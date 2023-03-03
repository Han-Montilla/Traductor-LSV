import { computed, ref } from "vue";
import * as tf from '@tensorflow/tfjs';

const useTf = () => ({ loadModel, predict });

let _model: tf.LayersModel;
const SEQUENCE_LENGHT = 10;
const prediction = ref<string>('nothing');
const _certainty = ref<number>(0);
const certainty = computed(() => `${(_certainty.value * 100).toFixed(0)}%`);

const loadModel = async () => {
  const modelPath = `model/model.json`;
  _model = await tf.loadLayersModel(modelPath);
}

const SIGNS = ['nothing', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
const predict = (sequence: readonly number[][]) => {
  const res = _model.predict(tf.tensor([sequence])) as tf.Tensor;
  const values = res.dataSync();
  const certainty = Math.max(...values);
  const sign = SIGNS[values.indexOf(certainty)];
  return {
    sign,
    certainty,
  }
}

export default useTf;