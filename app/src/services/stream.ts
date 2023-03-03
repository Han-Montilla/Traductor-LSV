import { computed, ref } from "vue";

const useStream = () => ({ init, currentStream, getAvailableCameras, currentDeviceId });

const getAvailableCameras = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices();
  return devices.filter(d => d.kind === 'videoinput');
}

const init = async () => {
  const devices = await getAvailableCameras();
  if (!devices.length) return;
  currentDeviceId.value = devices[0].deviceId;
}
const currentDeviceId = ref<string>('');
const currentStream = computed(async () => {
  try {
    let t = await navigator.mediaDevices.getUserMedia({
      audio: false,
      video: {
        facingMode: { ideal: "user" },
        deviceId: { exact: currentDeviceId.value }
      }
    })
    return t;
  } catch {
    return null;
  }
});

export default useStream;