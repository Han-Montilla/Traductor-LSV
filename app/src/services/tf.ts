import { computed, ref } from "vue";
import * as tf from '@tensorflow/tfjs';

const useTf = () => ({ loadModel, predict });

let _model: tf.LayersModel;
const SEQUENCE_LENGHT = 10;
const prediction = ref<string>('none');
const _certainty = ref<number>(0);
const certainty = computed(() => `${(_certainty.value * 100).toFixed(0)}%`)


const loadModel = async (name: string) => {
  const modelPath = `models/model.${name}.json`;
  _model = await tf.loadLayersModel(modelPath);
}

const SIGNS = ['none', 'a', 'b', 'c']
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