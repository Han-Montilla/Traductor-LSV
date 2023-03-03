<script setup lang="ts">
  import { onMounted, reactive, ref, computed, Ref } from 'vue';
  // import { Hands, HAND_CONNECTIONS } from '@mediapipe/hands'
  // import { Camera } from '@mediapipe/camera_utils';
  // import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'
  import useMp from '../services/mp';
  import useTf from '../services/tf';

  const { loadModel, predict } = useTf();
  const { extractKeypointsRH } = useMp();
  const videoEl = ref<HTMLVideoElement>() as Ref<HTMLVideoElement>;
  const canvasEl = ref<HTMLCanvasElement>() as Ref<HTMLCanvasElement>;

  const prediction = reactive({
    sign: 'none',
    certainty: 0
  });

  const delta = ref(0);
  const deltaHistory = ref<number[]>([]);
  const lastTime = ref<number>(Date.now());
  
  const predictionText = computed(
    () => prediction.certainty > 0.50
      ? `${prediction.sign} ${(prediction.certainty * 100).toFixed(0)}%` 
      : ``
  );

  const resolution = reactive({
    width: 1280,
    height: 720
  });
  
  onMounted(async () => {
    const ctx = canvasEl.value.getContext('2d') as CanvasRenderingContext2D;

    await loadModel();
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
      const thisTime = Date.now();
      delta.value = 1000 / (thisTime - lastTime.value);
      lastTime.value = thisTime;

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

      const { keypoints, handedness } = extractKeypointsRH(results);
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
        await mpHands.send({ image: videoEl.value });
      },
      width: resolution.width,
      height: resolution.height,
      facingMode: 'user'
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
    <div class="fps-counter">
      fps: {{ delta.toFixed(0) }}
    </div>
  </div>
</template>

<style scoped>
  .prediction {
    width: 100%;
    height: 128px;
    font-family: 'Courier New', Courier, monospace;
    line-height: 1;
    font-size: 128px;
    font-weight: bolder;
    text-align: center;
    color: white;
  }
  video {
    display: none;
  }
  .fps-counter {
    position: absolute;
    top: 0px;
    left: 0px;
    font-size: 64px;
    color: white;
    font-family: 'Courier New', Courier, monospace;
  }
</style>
