type Resolution = { width: number, height: number }
export const fitToScreen = (screen: Resolution, raw: Resolution): Resolution => {
  let scaleFactor = screen.width > screen.height
    ? screen.width / raw.width
    : screen.height / raw.height;

  return { width: raw.width * scaleFactor, height: raw.height * scaleFactor }
}

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