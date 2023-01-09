import { Options as HandOptions } from "@mediapipe/hands";

export default interface Model {
  name: string,
  signs: string[],
  handsConfig: HandOptions
  weightsPath: string,
}