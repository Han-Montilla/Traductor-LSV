<script setup lang="ts">
  import Feed from './components/Feed.vue';
  import useTf from './services/tf';

  const tf = useTf();

</script>

<template>
  <main>
    <Feed />
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
