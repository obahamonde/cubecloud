<script setup lang="ts">
const emit = defineEmits(["toggle"]);
const router = useRouter();
</script>
<template>
  <VAppBar app color="#36465D" pa-2>
    <img
      src="/logo.gif"
      class="rf x2 m-2 cp scale hover:animate-spin"
      @click="emit('toggle')"
    />
    <h1 class="row center font-mono text-2xl m-2 text-white">
      Cube Cloud

      <Dark />
    </h1>
  </VAppBar>
</template>
