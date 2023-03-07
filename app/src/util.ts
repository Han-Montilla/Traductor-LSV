type Resolution = { width: number, height: number }
export const fitToScreen = (screen: Resolution, raw: Resolution): Resolution => {
  const widthScaleFactor = screen.width / raw.width ;
  const heightScaleFactor = screen.height / raw.height;
  
  const scaleFactor = widthScaleFactor < heightScaleFactor
  ? widthScaleFactor : heightScaleFactor;
  
  return { width: raw.width * scaleFactor, height: raw.height * scaleFactor }
}

console.log(fitToScreen({ width: 960, height: 640 }, { width: 960, height: 960 }))

/**
 * @copyright https://rosettacode.org/wiki/Map_range
 * @param {number} value - value to be mapped 
 * @param {[number, number]} from - source range `value` must be in this range
 * @param {[number, number]} to - destination range
 * @returns mapped value to ""`to`" range
 */
export const mapValue = (value: number, from: [number, number], to: [number, number]) => {
  const [a1, a2] = from;
  const [b1, b2] = to;

  return b1 + (((value - a1)*(b2 - b1)) / (a2 - a1));
}

export const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
export const randFloat = (min: number, max: number) => Math.random() * (max - min + 1) + min;

export const findIndexOfMax = (arr: number[]) => {
  let remaining = 1;
  let maxIndex = 0;
  for (let i = 0; i < arr.length; i++) {
    const element = arr[i];

    remaining -= element;

    if (arr[maxIndex] < element) maxIndex = i;

    if (arr[maxIndex] >= remaining) return maxIndex;
  }
  return 0;
}

export const arrAverage = (arr: number[]) => arr.reduce((a, b) => a + b) / arr.length;

type rgbArr = [number, number, number];
export function colorRange(color1: rgbArr, color2: rgbArr, weight: number) {
  var w1 = weight;
  var w2 = 1 - w1;
  var [r, g, b] = [Math.round(color1[0] * w1 + color2[0] * w2),
      Math.round(color1[1] * w1 + color2[1] * w2),
      Math.round(color1[2] * w1 + color2[2] * w2)];
  return `rgb(${r}, ${g}, ${b})`;
}