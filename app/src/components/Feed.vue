<script setup lang="ts">
  import { onMounted, reactive, ref } from 'vue';
  import { Hands, HAND_CONNECTIONS, VERSION } from '@mediapipe/hands'
  import { Camera } from '@mediapipe/camera_utils';
  import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils'

  interface FeedProps {

  }

  // const props = defineProps<FeedProps>();

  const videoEl = ref<HTMLVideoElement>();
  const canvasEl = ref<HTMLCanvasElement>();

  const resolution = reactive({
    width: 1280,
    height: 720
  });
  
  onMounted(() => {
    if (!videoEl.value || !canvasEl.value) return;
    console.log(videoEl.value.width)
    const ctx = canvasEl.value.getContext('2d');
    if (ctx === null) return;

    const mpHands = new Hands({
      locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/hands@${VERSION}/${file}`
    });
    mpHands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.1,
      minTrackingConfidence: 0.1
    });

    mpHands.onResults(results => {
      if (!videoEl.value || !canvasEl.value) return;

      ctx.save();
      ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height);
      ctx.drawImage(
          results.image, 0, 0, canvasEl.value.width, canvasEl.value.height);
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
      height: resolution.height
    });
    camera.start();
  });
</script>

<template>
  <div>
    <video ref="videoEl"/>
    <canvas ref="canvasEl" :width="resolution.width" :height="resolution.height"/>
  </div>
</template>

<style scoped>
  video {
    display: none;
  }
</style>
