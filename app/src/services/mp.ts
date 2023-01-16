import { Results } from "@mediapipe/hands";

const useMp = () => ({extractKeypointsRH});

const HAND_LANDMARK_COUNT = 21; // https://mediapipe.dev/images/mobile/hand_landmarks.png
const HAND_LANDMARK_POINTS = HAND_LANDMARK_COUNT * 3;

const extractKeypointsRH = ({ multiHandLandmarks, multiHandedness }: Results): number[] => {
  if (
    multiHandLandmarks.length <= 0 ||
    multiHandedness[0].label !== 'Right'
  ) return Array(HAND_LANDMARK_POINTS).fill(0);

  const res: number[] = [];

  for (let i = 0; i < multiHandLandmarks[0].length; i++) {
    const { x, y ,z } = multiHandLandmarks[0][i];
    res.push(x, y, z);
  }

  return res;
}

export default useMp;