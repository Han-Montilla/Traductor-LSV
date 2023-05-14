export const SIGNS = ['nada', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'] as const;
export const SEQUENCE_LENGHT = 10;

export const POINT_COMPONENT_COUNT = 3; // x, y, z
export const HAND_LANDMARK_COUNT = 21; // https://mediapipe.dev/images/mobile/hand_landmarks.png
export const HAND_LANDMARK_POINTS = HAND_LANDMARK_COUNT * POINT_COMPONENT_COUNT;