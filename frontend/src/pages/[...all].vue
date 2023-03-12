<script setup lang="ts">
const msg = ref(
  "The resource you requested was not found in the server, please check your spelling and try again."
);
</script>
<template>
  <VCard inset-0>
    <VCardTitle>404</VCardTitle>
    <VCardText>
      {{ msg }}
    </VCardText>
  </VCard>
</template>
