<script setup lang="ts">
const drawer = ref(false);
</script>

<template>
  <AppBar @toggle="drawer = !drawer" />
  <VMain bg-black row mt-4>
    <AppDrawer v-if="drawer" fade-in-left />
    <RouterView />
  </VMain>
  <AppFooter />
</template>
