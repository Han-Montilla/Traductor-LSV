<script setup lang="ts">
  import { Options } from '@mediapipe/hands';
  import { onMounted, Ref, ref, reactive, watch, computed } from 'vue';
  import useStream from '../services/stream';
  import { fitToScreen, randFloat, sleep } from '../util';
  import Spinner from './Spinner.vue';
  import FlipIcon from './FlipIcon.vue';

  const videoEl = ref<HTMLVideoElement>() as Ref<HTMLVideoElement>;
  const canvasEl = ref<HTMLCanvasElement>() as Ref<HTMLCanvasElement>;
  const loading = reactive({
    mp: true,
    camera: true
  });
  const fps = ref<number>(60);
  const resolution = { width: 960, height: 600 }
  const canvasSize = reactive({ height: 0, width: 0 });
  const cameras = ref<MediaDeviceInfo[]>([]);
  const { Hands, HAND_CONNECTIONS, drawConnectors, drawLandmarks } = window;
  const { currentDeviceId, currentStream, init, getAvailableCameras } = useStream();
  const options = reactive<{
    flip: boolean,
    showLandmarks: boolean,
    showFps: boolean,
    precisionThreshhold: number,
    mode: 'single' | 'complete'
  }>({
    flip: false,
    showLandmarks: true,
    showFps: false,
    precisionThreshhold: 0.75,
    mode: 'single'
  });
  const mpOptions = reactive<Required<Options>>({
    maxNumHands: 1,
    modelComplexity: 0,
    minDetectionConfidence: 0.75,
    minTrackingConfidence: 0.5,
    selfieMode: true
  });
  const mpOptionsIndicators = reactive({...mpOptions});

  const updateMpOptions = () => {
    for (const key in mpOptionsIndicators) {
      const option = key as keyof typeof mpOptions;
      // @ts-ignore
      mpOptions[option] = mpOptionsIndicators[option];
    }
  }

  const onCameraChange = (event: Event) => {
    if (!(event.target instanceof HTMLSelectElement)) return;
    currentDeviceId.value = event.target.value;
  }

  onMounted(async () => {
    await init();
    cameras.value = await getAvailableCameras();
    const mpHands = new Hands({ locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}` });
    await mpHands.initialize();
    mpHands.setOptions(mpOptions);

    watch(mpOptions, async o => {
      loading.camera = true;
      await sleep(1);
      mpHands.setOptions(o)
      loading.camera = false;
    });

    watch(currentStream, async (payload) => {
      loading.camera = true;
      const stream = await payload;
      
      if (!stream) return;

      const settings = stream.getVideoTracks()[0].getSettings();
      const width = settings.width as number;
      const height = settings.height as number;

      const { width: rw, height: rh } = fitToScreen(resolution, { width, height });

      canvasSize.height = rh;
      canvasSize.width = rw;
      
      videoEl.value.srcObject = stream;
      await sleep(randFloat(250, 1000));
      loading.camera = false;
    }, { immediate: true })
  
    let ctx = canvasEl.value.getContext('2d') as CanvasRenderingContext2D;

    videoEl.value.onloadedmetadata = () => {
      videoEl.value.play()
      requestAnimationFrame(tick);
    }
  
    const tick = async () => {
      ctx.save();
      if (options.flip) {
        ctx.translate(canvasSize.width, 0);
        ctx.scale(-1, 1);
      }
      ctx.drawImage(videoEl.value, 0, 0, canvasSize.width, canvasSize.height);
      // await mpHands.send({ image: canvasEl.value });
      ctx.restore();

      if (loading.mp) loading.mp = false
      requestAnimationFrame(tick);
    }

    mpHands.onResults(results => {

      if (results.multiHandedness.length) console.log(results.multiHandedness[0].label);

      /// drawing landmarks
      ctx.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height);
      if (options.flip) {
        ctx.translate(canvasSize.width, 0);
        ctx.scale(-1, 1);
      }
      ctx.drawImage(results.image, 0, 0, canvasEl.value.width, canvasEl.value.height);
      
      if (results.multiHandLandmarks && options.showLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawConnectors(ctx, landmarks, HAND_CONNECTIONS, { color: '#00FF00', lineWidth: 5 });
          drawLandmarks(ctx, landmarks, {color: '#FF0000', lineWidth: 2 });
        }
      }

      // const { keypoints, handedness } = extractKeypointsRH(results);
      // sequence.unshift(keypoints);
      // if (sequence.length === SEQUENCE_LENGHT) {
      //   const res = predict(sequence);
      //   prediction.sign = res.sign;
      //   prediction.certainty = res.certainty;
      //   sequence.pop();
      // }

    });
  });

  const parseRangeValue = ({ target }: Event) => Number.parseFloat((target as HTMLInputElement).value);

</script>

<template>
  <div class="main">
    <video ref="videoEl"/>
    <div :style="{ display: loading.mp ? 'none' : undefined }" class="container">
      <div class="camera">
        <div :style="{
          width: `${canvasSize.width}px`, height: `${canvasSize.height}px`,
          position: 'relative',
          display: loading.camera ? 'none' : undefined
        }">
          <canvas ref="canvasEl" :width="canvasSize.width" :height="canvasSize.height"/>
          <div v-if="options.showFps" v-text="fps" class="fps"/>
          <FlipIcon class="flip-button" @click="() => options.flip = !options.flip" 
            :style="{ transform: options.flip ? `scaleX(-1)` : '' }"
          />
        </div>
        <Spinner v-if="loading.camera" style="width: 64px; height: 64px;"/>
      </div>
      <div class="options">
        <label v-text="`Device`" style="line-height: 0;"/>
        <select :disabled="loading.camera" @change="(event) => onCameraChange(event)" style="width: min-content;">
          <option v-for="{ deviceId, label } in cameras"
            :value="deviceId"
            :selected="currentDeviceId === deviceId"
          >
            {{ label }}
          </option>
        </select>
        <div class="spacer"/>
        <div class="toggle-item">
          <input :disabled="loading.camera" type="checkbox" v-model="options.showFps"/>
          <label v-text="`Show FPS`"/>
        </div>
        <div class="toggle-item">
          <input :disabled="loading.camera" type="checkbox" v-model="options.showLandmarks"/>
          <label v-text="`Show Landmarks`"/>
        </div>
        <div class="radio-item">
          <label v-text="`Mode`"/>
          <div class="radio-options">
            <div class="radio-option">
              <input type="radio" value="single" v-model="options.mode"/>
              <label v-text="`single`"/>
            </div>
            <div class="radio-option">
              <input type="radio" value="complete" v-model="options.mode"/>
              <label v-text="`complete`"/>
            </div>
          </div>
        </div>
        <div class="slider-item">
          <label v-text="`Precision Threshold`"/>
          <div class="slider-container">
            <input 
              class="slider"
              :disabled="loading.camera"
              type="range" min="0" max=1.00 step=0.01
              v-model.number="options.precisionThreshhold"
            />
            <div class="slider-value" v-text="`${(options.precisionThreshhold * 100).toFixed(0)}%`"/>
          </div>
        </div>
        <div class="spacer"/>
        <div class="slider-item">
          <label v-text="`Detection Confidence`"/>
          <div class="slider-container">
            <input 
              class="slider"
              :disabled="loading.camera"
              type="range" min="0" max=1.00 step=0.01
              :value="mpOptionsIndicators.minDetectionConfidence"
              @input="e => mpOptionsIndicators.minDetectionConfidence = parseRangeValue(e)"
              @change="updateMpOptions"
            />
            <div class="slider-value" v-text="`${(mpOptionsIndicators.minDetectionConfidence * 100).toFixed(0)}%`"/>
          </div>
        </div>
        <div class="slider-item">
          <label v-text="`Tracking Confidence`"/>
          <div class="slider-container">
            <input 
              class="slider"
              :disabled="loading.camera"
              type="range" min="0" max=1.00 step=0.01
              :value="mpOptionsIndicators.minTrackingConfidence"
              @input="e => mpOptionsIndicators.minTrackingConfidence = parseRangeValue(e)"
              @change="updateMpOptions"
            />
            <div class="slider-value" v-text="`${(mpOptionsIndicators.minTrackingConfidence * 100).toFixed(0)}%`"/>
          </div>
        </div>
      </div>
      <div class="history">

      </div>
    </div>
    <!-- <Spinner v-if="loading" class="spinner"/> -->
    <div v-if="loading.mp" v-text="`loading...`" style="color: white;"/>
  </div>
</template>

<style scoped>
  .main {
    display: flex;
    justify-content: center;
    justify-items: center;
    align-items: center;
    width: 100%;
    height: 100%;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  .container {
    width: 100%;
    height: 100%;
    padding: 16px;
    display: grid;
    place-items: center;
    justify-items: center;
    grid-template-columns: 5fr 1fr;
    grid-template-rows: 2fr 1fr;
    grid-template-areas: 
      'camera options'
      'history history'
    ;
  }

  .camera {
    justify-content: center;
    justify-items: center;
    align-items: center;
    grid-area: camera;
    --pad: 8px;
  }
  .fps {
    position: absolute;
    font-family: 'Courier New', Courier, monospace;
    line-height: 1;
    font-weight: bolder;
    bottom: var(--pad);
    right: var(--pad);
    padding: 4px;
    padding-top: 6px;
    padding-bottom: 0px;
    border-radius: 8px;
    color: black;
    background: rgba(255, 255, 255, 0.35);
    font-size: 32px;
  }
  .flip-button {
    position: absolute;
    top: var(--pad);
    right: var(--pad);
    width: 48px;
    height: 48px;
    color: rgba(255, 255, 255, 0.5);
  }
  .options {
    grid-area: options;
    display: grid;
    --same-line-gap: 8px;
  }
  .options > * + * {
    margin-top: 12px;
  }
  .options label {
    font-weight: bold;
    font-size: 18px;
    line-height: 0.5;
  }

  .toggle-item {
    display: flex;
    align-items: center;
    line-height: 0;
  }
  .toggle-item > * + *  {
    margin-left: var(--same-line-gap);
  }

  .toggle-item label {
    font-weight: normal;
  }

  .slider-container {
    display: flex;
    align-items: center;
    line-height: 1;
  }
  
  .slider-container > * + * {
    margin-left: var(--same-line-gap);
  }

  .slider-value {
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    font-size: 16px;
    margin-top: 2px;
    text-align: right;
    min-width: 39px;
    text-align: right;
  }

  .slider {
    width: 100%;
  }

  .radio-options > * + * {
    margin-top: 8px;
  }

  .radio-option {
    display: flex;
    align-items: center;
  }
  .radio-option > * + * {
    margin-left: var(--same-line-gap);
  }

  .radio-option label {
    font-weight: normal;
  }

  .spacer {
    margin-top: 16px;
  }

  .history {
    grid-area: history;
    width: 100%;
    height: 100%;
    background-color: cadetblue;
  }
  .spinner {
    height: 64px;
    widows: 64px;
  }
  video {
    display: none;
  }
  canvas {
    display: block;
    max-width: min-content;
  }
</style>
