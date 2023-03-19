<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { loginWithRedirect } = useAuth0();
</script>

<template>
  <VCard
    class="col center p-24 shadow-black shadow-lg bg-transparent backdrop-blur-md rf"
  >
    <h1 class="text-title m-4">Welcome to Cube Cloud</h1>
    <img
      src="/logo.gif"
      class="rf x6 m-4 cp scale hover:animate-spin"
      title="Get Started"
      @click="loginWithRedirect()"
    />
    <h1 class="text-white text-2xl font-mono m-4">Experimental Cloud IDE</h1>
    <button
      class="m-4 px-4 py-2 sh cp scale text-#1AA61A bg-#000200 rounded-lg hover:bg-#1AA61A hover:text-#000200"
      @click="loginWithRedirect()"
    >
      Get Started
    </button>
  </VCard>
</template>
