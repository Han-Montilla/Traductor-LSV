<script setup lang="ts">
  import { onMounted, reactive, ref, computed } from 'vue';
  // import { Hands, HAND_CONNECTIONS } from '@mediapipe/hands'
  // import { Camera } from '@mediapipe/camera_utils';
  // import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'
  import useMp from '../services/mp';
  import useTf from '../services/tf';

  const { loadModel, predict } = useTf();
  const { extractKeypointsRH } = useMp();
  const videoEl = ref<HTMLVideoElement>();
  const canvasEl = ref<HTMLCanvasElement>();

  const prediction = reactive({
    sign: 'none',
    certainty: 0
  });
  
  const predictionText = computed(
    () => prediction.certainty > 0.75 && prediction.sign !== 'none'
      ? `${prediction.sign} ${(prediction.certainty * 100).toFixed(0)}%` 
      : ``
  );

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

    // @ts-ignore
    const mpHands = new window.Hands({
      // @ts-ignore
      locateFile: file => {
        const res = `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
        return res;
      }
    });
    mpHands.setOptions({
      maxNumHands: 1,
      modelComplexity: 0,
      minDetectionConfidence: 0.75,
      minTrackingConfidence: 0.5
    });

    // @ts-ignore
    mpHands.onResults(results => {
      if (!videoEl.value || !canvasEl.value) return;

      ctx.save();

      /// drawing landmarks
      ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height);
      ctx.drawImage(results.image, 0, 0, canvasEl.value.width, canvasEl.value.height);
      
      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          // @ts-ignore
          window.drawConnectors(ctx, landmarks, window.HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 5});
          // @ts-ignore
          window.drawLandmarks(ctx, landmarks, {color: '#FF0000', lineWidth: 2});
        }
      }

      const { keypoints } = extractKeypointsRH(results);
      sequence.unshift(keypoints);
      if (sequence.length === SEQUENCE_LENGHT) {
        const res = predict(sequence);
        prediction.sign = res.sign;
        prediction.certainty = res.certainty;
        sequence.pop();
      }
      ctx.restore();

    })
    // @ts-ignore
    const camera = new window.Camera(videoEl.value, {
      onFrame: async () => {
        if (!videoEl.value) return;
        await mpHands.send({ image: videoEl.value });
      },
      width: resolution.width,
      height: resolution.height
    });

    camera.start();

  });
</script>

<template>
  <div>
    <div class="prediction">
      {{predictionText}}
    </div>
    <video ref="videoEl"/>
    <canvas ref="canvasEl" :width="resolution.width" :height="resolution.height"/>
  </div>
</template>

<style scoped>
  .prediction {
    width: 100%;
    height: 81px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 64px;
    font-weight: bolder;
    text-align: center;
    color: white;
  }
  video {
    display: none;
  }
</style>
