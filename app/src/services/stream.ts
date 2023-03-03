import { computed, ref } from "vue";

const useStream = () => ({ init, currentStream, getAvailableCameras, currentDeviceId });

const getAvailableCameras = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices();
  return devices.filter(({ kind, deviceId }) => kind === 'videoinput' && deviceId !== '');
}

const init = async () => {
  const devices = await getAvailableCameras();
  if (!devices.length) return;
  currentDeviceId.value = devices[0].deviceId;
}
const currentDeviceId = ref<string>('');
const currentStream = computed(async () => {
  try {
    const id = currentDeviceId.value;
    const t = await navigator.mediaDevices.getUserMedia({
      audio: false,
      video: {
        facingMode: { ideal: "user" },
        deviceId: { ideal: id }
      }
    })
    return t;
  } catch (e) {
    if (e instanceof DOMException) {
      console.log(e.message);
    }
    return null;
  }
});

export default useStream;