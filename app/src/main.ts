import { createApp } from 'vue'
import App from './App.vue'
import { Hands, LandmarkConnectionArray } from '@mediapipe/hands';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils';
import './style.css'

declare global {
  interface Window {
    Hands: typeof Hands,
    HAND_CONNECTIONS: LandmarkConnectionArray
    drawConnectors: typeof drawConnectors
    drawLandmarks: typeof drawLandmarks
  }
}

createApp(App).mount('#app')
