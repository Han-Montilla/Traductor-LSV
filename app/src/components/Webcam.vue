<script setup lang="ts">
  import { onMounted, Ref, ref, reactive, watch } from 'vue';
  import useStream from '../services/stream';
  import { fitToScreen } from '../util';

  const videoEl = ref<HTMLVideoElement>() as Ref<HTMLVideoElement>;
  const canvasEl = ref<HTMLCanvasElement>() as Ref<HTMLCanvasElement>;
  const loading = ref<boolean>(true);
  const resolution = { width: 960, height: 600 }
  const canvasSize = reactive({ height: 0, width: 0 });
  const cameras = ref<MediaDeviceInfo[]>([]);
  const { currentDeviceId, currentStream, init, getAvailableCameras } = useStream();

  const onCameraChange = (event: Event) => {
    if (!(event.target instanceof HTMLSelectElement)) return;
    currentDeviceId.value = event.target.value;
  }

  onMounted(async () => {
    await init();
    cameras.value = await getAvailableCameras();

    watch(currentStream, async (payload) => {
      const stream = await payload;

      if (!stream) return;

      const settings = stream.getVideoTracks()[0].getSettings();
      const width = settings.width as number;
      const height = settings.height as number;

      const { width: rw, height: rh } = fitToScreen(resolution, { width, height });

      canvasSize.height = rh;
      canvasSize.width = rw;

      videoEl.value.srcObject = stream;

    }, { immediate: true })
  
    let ctx = canvasEl.value.getContext('2d') as CanvasRenderingContext2D;

    videoEl.value.onloadedmetadata = () => {
      videoEl.value.play()
      requestAnimationFrame(tick);
    }
    
    const tick = () => {
      ctx.save();
      ctx.clearRect(0, 0, canvasSize.width, canvasSize.height);
      ctx.drawImage(videoEl.value, 0, 0, canvasSize.width, canvasSize.height);
      ctx.restore();
      requestAnimationFrame(tick);
    }
  });

</script>

<template>
  <div class="container">
    <video ref="videoEl"/>
    <canvas ref="canvasEl" :width="canvasSize.width" :height="canvasSize.height"/>

    <select @change="(event) => onCameraChange(event)" style="width: min-content;">
      <option v-for="{ deviceId, label } in cameras"
        :value="deviceId"
        :selected="currentDeviceId === deviceId"
      >
        {{ label }}
      </option>
    </select>
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
    display: block;
    border: white 1px solid;
    max-width: min-content;
  }
</style>
