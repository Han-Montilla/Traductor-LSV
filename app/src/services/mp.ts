import { Results } from "@mediapipe/hands";
import { ref } from "vue";
import { HAND_LANDMARK_COUNT } from "../const";

const useMp = () => ({extractKeypoints});

const extractKeypoints = ({ multiHandWorldLandmarks: multiHandLandmarks, multiHandedness }: Results): { keypoints: number[][], handedness: string } => {

  if (
    multiHandLandmarks.length <= 0
  ) return { keypoints: Array(HAND_LANDMARK_COUNT).fill([0, 0, 0]), handedness: '' };
    
    
  const keypoints: number[][] = [];

  for (let i = 0; i < multiHandLandmarks[0].length; i++) {
    const { x, y ,z } = multiHandLandmarks[0][i];
    keypoints.push([x, y, z]);
  }

  return { keypoints, handedness: multiHandedness[0].label };
}

export default useMp;