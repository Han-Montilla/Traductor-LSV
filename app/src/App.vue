<script setup lang="ts">
  import { Options } from '@mediapipe/hands';
  import { onMounted, Ref, ref, reactive, watch, computed } from 'vue';
  import useStream from './services/stream';
  import useMp from './services/mp';
  import useTf from './services/tf';
  import { fitToScreen, randFloat, sleep, findIndexOfMax, arrAverage, colorRange } from './util';
  import Spinner from './components/Spinner.vue';
  import FlipIcon from './components/FlipIcon.vue';
  import { SEQUENCE_LENGHT, SIGNS } from './const';

  const videoEl = ref<HTMLVideoElement>() as Ref<HTMLVideoElement>;
  const canvasEl = ref<HTMLCanvasElement>() as Ref<HTMLCanvasElement>;
  const historialLogEl = ref<HTMLDivElement>() as Ref<HTMLDivElement>;
  const deltaHistory = ref<number[]>([]);
  const fps = computed(() => {
    if (options.showFps) {
      return arrAverage(deltaHistory.value);
    }
    return 0;
  });
  const lastTime = ref<number>(Date.now());
  const loading = reactive({
    mp: true,
    camera: true
  });
  const resolution = { width: 960, height: 600 }
  const canvasSize = reactive({ height: 0, width: 0 });
  const cameras = ref<MediaDeviceInfo[]>([]);
  const { Hands, HAND_CONNECTIONS, drawConnectors, drawLandmarks } = window;
  const { currentDeviceId, currentStream, init, getAvailableCameras } = useStream();
  const { extractKeypoints } = useMp();
  const { predict, loadModel } = useTf();
  const options = reactive<{
    flip: boolean,
    showLandmarks: boolean,
    showFps: boolean,
    precisionThreshhold: number,
    mode: 'single' | 'complete',
    intervalCooldown: number,
  }>({
    flip: false,
    showLandmarks: true,
    showFps: false,
    precisionThreshhold: 0.75,
    mode: 'single',
    intervalCooldown: 1500,
  });
  const intervalCooldownIndicator = ref(options.intervalCooldown);
  const mpOptions = reactive<Required<Options>>({
    maxNumHands: 1,
    modelComplexity: 0,
    minDetectionConfidence: 0.75,
    minTrackingConfidence: 0.5,
    selfieMode: true
  });
  const mpOptionsIndicators = reactive({...mpOptions});

  const historial = ref<string[]>([]);
  const predictionArray = ref<number[]>(Array(27).fill(0));
  const predictionIndex = computed(() => findIndexOfMax(predictionArray.value));
  const certainty = computed(() => predictionArray.value[predictionIndex.value]);
  const formatedCertainty = computed(() => (certainty.value * 100).toFixed(0));
  const prediction = computed(() => SIGNS[predictionIndex.value]);
  const handedness = ref<string>('');
  const formatedHandedness = computed(() => {
    return handedness.value === ''
      ? 'ninguna'
      : handedness.value === 'Left'
        ? 'Izquierda'
        : 'Derecha';
  })

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

  let intervalId: NodeJS.Timer;
  const intervalTick = () => {
    if (prediction.value !== SIGNS[0] && certainty.value > options.precisionThreshhold && handedness.value === 'Right') {
      historial.value.push(prediction.value);
      const lastChild = historialLogEl.value.lastElementChild;
      if (lastChild) {
        lastChild.scrollIntoView({ behavior: 'smooth'});
      }
    }
  }

  onMounted(async () => {
    await init();
    await loadModel();
    cameras.value = await getAvailableCameras();
    const mpHands = new Hands({ locateFile: file => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}` });
    await mpHands.initialize();
    mpHands.setOptions(mpOptions);

    watch(mpOptions, async o => {
      loading.camera = true;
      await sleep(5);
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

    videoEl.value.onloadedmetadata = async () => {
      await videoEl.value.play()
      requestAnimationFrame(tick);
    }
  
    const tick = async () => {
      const thisTime = Date.now();
      deltaHistory.value.push(1000 / (thisTime - lastTime.value));
      if (deltaHistory.value.length > 10) deltaHistory.value.shift();
      lastTime.value = thisTime;

      ctx.save();
      if (options.flip) {
        ctx.translate(canvasSize.width, 0);
        ctx.scale(-1, 1);
      }
      ctx.drawImage(videoEl.value, 0, 0, canvasSize.width, canvasSize.height);
      await mpHands.send({ image: canvasEl.value });
      ctx.restore();

      if (loading.mp) loading.mp = false
      requestAnimationFrame(tick);
    }

    watch(options, ({ intervalCooldown }) => {
      // console.log(`cooldown: ${intervalCooldown}`)
      if (intervalId !== null) clearInterval(intervalId);
      if (intervalCooldown !== 0) {
        intervalId = setInterval(intervalTick, intervalCooldown);
      }
    }, { immediate: true });

    const _rawSequence: number[][] = [];

    mpHands.onResults(results => {

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

      const { keypoints, handedness: _handedness } = extractKeypoints(results);
      handedness.value = _handedness;
      _rawSequence.unshift(keypoints);
      if (_rawSequence.length === SEQUENCE_LENGHT) {
        predictionArray.value = Array.from(predict(_rawSequence));
        _rawSequence.pop();
      }
    });
  });

  const parseRangeValue = ({ target }: Event) => Number.parseFloat((target as HTMLInputElement).value);
  const clearHistorial = () => {
    historial.value.splice(0, historial.value.length);
  }
</script>

<template>
  <main>
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
            <div v-if="options.showFps" v-text="fps.toFixed(0)" class="fps"/>
            <FlipIcon class="flip-button" @click="() => options.flip = !options.flip" 
              :style="{ transform: options.flip ? `scaleX(-1)` : '' }"
            />
          </div>
          <Spinner v-if="loading.camera" style="width: 64px; height: 64px;"/>
        </div>
        <div class="options">
          <label v-text="`Dispositivo`" style="line-height: 0;"/>
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
            <label v-text="`Mostrar FPS`"/>
          </div>
          <div class="toggle-item">
            <input :disabled="loading.camera" type="checkbox" v-model="options.showLandmarks"/>
            <label v-text="`Mostrar Landmarks`"/>
          </div>
          <div class="radio-item">
            <label v-text="`Modo`"/>
            <div class="radio-options">
              <div class="radio-option">
                <input type="radio" value="single" v-model="options.mode"/>
                <label v-text="`singular`"/>
              </div>
              <div class="radio-option">
                <input type="radio" value="complete" v-model="options.mode"/>
                <label v-text="`completo`"/>
              </div>
            </div>
          </div>
          <div class="slider-item">
            <label v-text="`Certeza Mínima`"/>
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
          <div class="slider-item">
            <label v-text="`Intervalo Historial`"/>
            <div class="slider-container">
              <input 
                class="slider"
                :disabled="loading.camera"
                type="range" min="0" max=10000 step=500
                :value="intervalCooldownIndicator"
                @input="e => intervalCooldownIndicator = parseRangeValue(e)"
                @change="_ => options.intervalCooldown = intervalCooldownIndicator"
              />
              <div class="slider-value-time" v-text="`${
                intervalCooldownIndicator != 0
                ? `${(intervalCooldownIndicator / 1000).toFixed(1)}s`
                : `off`
              }`"/>
            </div>
          </div>
          <div class="spacer"/>
          <div class="slider-item">
            <label v-text="`Confianza de detección`"/>
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
            <label v-text="`Confianza de Tracking`"/>
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
        <div class="log">
          <div class="prediction-area">
            <div v-if="options.mode == 'single'" class="single-prediction">
              <span v-text="`Prediciendo: `"/>
              <span :class="`${ prediction === SIGNS[0] ? 'highlighter-text-wrong' : 'highlighter-text'}`" v-text="prediction"/>
              <br/>
              <span v-text="`Certeza: `"/>
              <span :class="`${ certainty < options.precisionThreshhold ? 'highlighter-text-wrong' : 'highlighter-text'}`" v-text="`${formatedCertainty}%`"/>
              <br/>
              <span v-text="`Con mano: `"/>
              <span :class="`${ handedness === 'Left' ? 'highlighter-text-wrong' : 'highlighter-text'}`" v-text="`${formatedHandedness}`"/>
            </div>
            <div v-else class="complete-prediction">
              <div v-for="sign, i in SIGNS" class="sign-segment">
                  <div class="sign-bar" :style="{
                    height: `${(predictionArray[i] * 100).toFixed(0)}%`,
                    backgroundColor: colorRange([61, 117, 221], [221, 66, 61], predictionArray[i])
                  }">
                    <span class="sign-bar-prob" v-text="`${(predictionArray[i] * 100).toFixed(0)}%`"/>
                  </div>
                <div class="sign-text" :style="{backgroundColor: colorRange([61, 117, 221], [221, 66, 61], predictionArray[i])}">
                  {{  sign }}
                </div>
              </div>
            </div>
          </div>
          <div class="history-area">
            <button v-if="historial.length" class="historial-reset-btn" @click="clearHistorial" v-text="`clear`"/>
            <span v-text="`Historial:`" class="historial-label"/>
            <div class="historial-logs" ref="historialLogEl">
              <span v-for="sign in historial" v-text="`${sign}&nbsp;`"/>
            </div>
          </div>
        </div>
      </div>
      <!-- <Spinner v-if="loading" class="spinner"/> -->
      <div v-if="loading.mp" v-text="`loading...`" style="color: white;"/>
    </div>
  </main>
</template>

<style scoped>
  main {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .main {
    display: flex;
    justify-content: center;
    justify-items: center;
    align-items: center;
    width: 100%;
    max-width: 1500px;
    height: 100%;
    color: white;
    /* overflow: hidden; */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  .container {
    width: 100%;
    height: 100%;
    padding: 16px;
    display: grid;
    place-items: center;
    justify-items: center;
    grid-template-columns: 3fr 1fr;
    grid-template-rows: 3fr 2fr;
    grid-template-areas: 
      'camera options'
      'log log'
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
  
  .slider-value-time {
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    font-size: 16px;
    margin-top: 2px;
    text-align: right;
    min-width: 48px;
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

  .log {
    grid-area: log;
    width: 100%;
    height: 100%;
    max-height: 100%;
    padding: 16px;
    
    display: grid;
    place-items: center;
    justify-items: start;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
    grid-template-areas:
      'prediction'
      'history'
    ;
  }
  .prediction-area {
    grid-area: prediction;
    width: 100%;
    height: 215px;
  }
  .single-prediction {
    font-size: 42px;
    font-family: 'Courier New', Courier, monospace;
    line-height: 1.25;
    height: 100%;
  }
  
  .highlighter-text {
    font-weight: bolder;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    color: rgb(61, 117, 221);
  }
  
  .highlighter-text-wrong {
    font-weight: bolder;
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    color: rgb(221, 66, 61);

  }

  .complete-prediction {
    display: grid;
    grid-template-columns: repeat(27, 1fr);
    width: 100%;
    height: 215px;
  }

  .sign-segment {
    height: 100%;
    max-height: 215px;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 9fr 1fr;
    border: rgba(255, 255, 255, 0.1) solid 1px;
  }
  .sign-bar {
    align-self: end;
    width: 100%;
    background-color: rgb(51, 51, 51);
    position: relative;
  }

  .sign-bar-prob {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    font-family: 'Courier New', Courier, monospace;
    text-align: center;
  }
  .sign-text {
    text-align: center;
  }
  
  .history-area {
    grid-area: history;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    max-height: 215px;
    widows: 100%;
    position: relative;
  }

  .historial-reset-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 20px;
    border-radius: 16px;
    padding: 12px;
    padding-top: 8px;
    padding-bottom: 4px;
  }

  .historial-label {
    font-size: 42px;
    font-family: 'Courier New', Courier, monospace;
  }

  .historial-logs {
    font-size: 42px;
    display: flex;
    flex-wrap: wrap;
    justify-items: start;
    align-items: start;
    line-height: 1;
    overflow-y: scroll;
    -ms-overflow-style: none; /* for Internet Explorer, Edge */
    scrollbar-width: none; /* for Firefox */
  }

  .historial-logs::-webkit-scrollbar {
    display: none;
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