<script setup lang="ts">
  import { onMounted, reactive, ref, watch } from 'vue';
  import { Hands, HAND_CONNECTIONS, VERSION as MP_VERSION } from '@mediapipe/hands'
  import { Camera } from '@mediapipe/camera_utils';
  import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'
  import useMp from '../services/mp';
import useTf from '../services/tf';

const { loadModel, predict, prediction } = useTf();
const { extractKeypointsRH } = useMp();
  const videoEl = ref<HTMLVideoElement>();
  const canvasEl = ref<HTMLCanvasElement>();
  const run = ref(false);
  const toggle = () => run.value = !run.value;

  const resolution = reactive({
    width: 1280,
    height: 720
  });
  
  onMounted(async () => {
    if (!videoEl.value || !canvasEl.value) return;
    const ctx = canvasEl.value.getContext('2d');
    if (ctx === null) return;

    await loadModel('v1');
    const sequence: number[][] = [];
    const SEQUENCE_LENGHT = 10;

    const mpHands = new Hands({
      locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/hands@${MP_VERSION}/${file}`
    });
    mpHands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.75,
      minTrackingConfidence: 0.5
    });

    mpHands.onResults(results => {
      if (!videoEl.value || !canvasEl.value) return;

      ctx.save();

      /// drawing landmarks
      ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height);
      ctx.drawImage(results.image, 0, 0, canvasEl.value.width, canvasEl.value.height);
      
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawConnectors(ctx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 5});
          drawLandmarks(ctx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
      }

      const keypoints = extractKeypointsRH(results);

      sequence.unshift(keypoints);
      if (sequence.length === SEQUENCE_LENGHT) {
        predict(sequence);
        sequence.pop();
      }

      
      ctx.restore();
1

    })
    const camera = new Camera(videoEl.value, {
      onFrame: async () => {
        if (!videoEl.value) return;
        await mpHands.send({ image: videoEl.value });
      },
      width: resolution.width,
      height: resolution.height,
      facingMode: 'user',
    });

    camera.start();
    watch(run, n => {
      n
        ? camera.start()
        : camera.stop();
    });

  });
</script>

<template>
  <div>
    <div class="prediction">
      {{ prediction }}
    </div>
    <video ref="videoEl"/>
    <canvas ref="canvasEl" :width="resolution.width" :height="resolution.height"/>
    <button @click="toggle">
      toggle
    </button>
  </div>
</template>

<style scoped>
  .prediction {
    width: 100%;
    font-size: 64px;
    font-weight: bolder;
    text-align: center;
    color: white;
  }
  video {
    display: none;
  }
</style>
