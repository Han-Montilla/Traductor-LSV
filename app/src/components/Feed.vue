<script setup lang="ts">
  import { onMounted, reactive, ref, watch } from 'vue';
  import { Hands, HAND_CONNECTIONS, VERSION as MP_VERSION } from '@mediapipe/hands'
  import { Camera } from '@mediapipe/camera_utils';
  import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'
import useMp from '../services/mp';

  const videoEl = ref<HTMLVideoElement>();
  const canvasEl = ref<HTMLCanvasElement>();
  const run = ref(false);
  const toggle = () => run.value = !run.value;

  const resolution = reactive({
    width: 1280,
    height: 720
  });
  
  onMounted(() => {
    if (!videoEl.value || !canvasEl.value) return;
    const ctx = canvasEl.value.getContext('2d');
    if (ctx === null) return;

    const sequence: number[] = [];
    const { extractKeypointsRH } = useMp();

    const mpHands = new Hands({
      locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/hands@${MP_VERSION}/${file}`
    });
    mpHands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });

    mpHands.onResults(results => {
      if (!videoEl.value || !canvasEl.value) return;

      ctx.save();

      /// drawing landmarks
      ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height);
      ctx.drawImage(results.image, 0, 0, canvasEl.value.width, canvasEl.value.height);
      const keypoints = extractKeypointsRH(results);
      
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawConnectors(ctx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 5});
          drawLandmarks(ctx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
      }

      ctx.restore();


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
    <video ref="videoEl"/>
    <canvas ref="canvasEl" :width="resolution.width" :height="resolution.height"/>
    <button @click="toggle">
      toggle
    </button>
  </div>
</template>

<style scoped>
  video {
    display: none;
  }
</style>
