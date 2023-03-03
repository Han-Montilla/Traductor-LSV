import { createApp } from 'vue'
import App from './App.vue'
import { Hands, LandmarkConnectionArray } from '@mediapipe/hands'
import './style.css'

declare global {
  interface Window {
    Hands: Hands,
    HAND_CONNECTIONS: LandmarkConnectionArray
  }
}

createApp(App).mount('#app')
