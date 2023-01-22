import { Results } from "@mediapipe/hands";
import { ref } from "vue";

const useMp = () => ({extractKeypointsRH});

const HAND_LANDMARK_COUNT = 21; // https://mediapipe.dev/images/mobile/hand_landmarks.png
const HAND_LANDMARK_POINTS = HAND_LANDMARK_COUNT * 3;

const extractKeypointsRH = ({ multiHandLandmarks, multiHandedness }: Results): { keypoints: number[], handedness: string } => {

  if (
    multiHandLandmarks.length <= 0
  ) return { keypoints: Array(HAND_LANDMARK_POINTS).fill(0), handedness: '' };
    
    
  const keypoints: number[] = [];

  for (let i = 0; i < multiHandLandmarks[0].length; i++) {
    const { x, y ,z } = multiHandLandmarks[0][i];
    keypoints.push(x, y, z);
  }

  return { keypoints, handedness: multiHandedness[0].label };
}

export default useMp;