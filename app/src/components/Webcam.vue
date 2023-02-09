<script setup lang="ts">
  import { onMounted, Ref, ref } from 'vue';
  import useStream from '../services/stream';

  const videoEl = ref<HTMLVideoElement>() as Ref<HTMLVideoElement>;
  const canvasEl = ref<HTMLCanvasElement>() as Ref<HTMLCanvasElement>;

  onMounted(async () => {
    const { getStream, setup } = useStream();
  
    let ctx = canvasEl.value.getContext('2d') as CanvasRenderingContext2D;
    const { stream } = await getStream();
    const { width, height } = {
      width: stream.getVideoTracks()[0].getSettings().width as number, 
      height: stream.getVideoTracks()[0].getSettings().height as number
    }

    canvasEl.value.height = height;
    canvasEl.value.width = width;

    videoEl.value.srcObject = stream;
    videoEl.value.onloadedmetadata = () => {
      videoEl.value.play()
      requestAnimationFrame(tick);
    }
    
    const tick = () => {
      ctx.save();
      ctx.clearRect(0, 0, width, height);
      ctx.drawImage(videoEl.value, 0, 0, width, height);
      ctx.restore();
      requestAnimationFrame(tick);
    }
  });

</script>

<template>
  <div class="container">
    <video ref="videoEl"/>
    <canvas ref="canvasEl"/>
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }
  video {
    display: none;
  }
  canvas {
    border: white 1px solid;
  }
</style>
