const useStream = () => ({getStream, setup, getAvailableDevices});

const getStream = async () => ({
  stream: await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: { facingMode: {ideal: "user"}}
  })
});

const setup = async () => {
  const hi = await navigator.mediaDevices.enumerateDevices();
  return hi;
}

const switchDevice = async () => {

}

const getAvailableDevices = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices();
  return devices.filter(d => d.kind === 'videoinput');
}

export default useStream;