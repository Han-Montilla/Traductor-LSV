<script setup lang="ts">
  import Webcam from './components/Webcam.vue'
  import Feed from './components/Feed.vue'
</script>

<template>
  <main>
    <Webcam />
    <!-- <Feed /> -->
  </main>
</template>

<style scoped>
  main {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
